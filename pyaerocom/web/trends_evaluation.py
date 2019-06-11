#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToDos
-----

- Review outlier removal
- 
"""
from collections import OrderedDict as od
import datetime
from fnmatch import fnmatch
import numpy as np
import os
import pandas as pd
from pyaerocom import const, __version__
from pyaerocom._lowlevel_helpers import (check_dirs_exist, dict_to_str)
from pyaerocom.helpers import isnumeric
from pyaerocom.io import ReadGridded
from pyaerocom.web.helpers import ObsConfigEval
from pyaerocom.exceptions import DataCoverageError
from pyaerocom.region import Region, find_closest_region_coord
from scipy.stats import kendalltau
from scipy.stats.mstats import theilslopes
import simplejson

class TrendsEvaluation(object):
    """High-level analysis class to compute json files for trends interface
    
    Web: https://aerocom-trends.met.no/
    
    Attributes
    ----------
    
    out_basedir : str
        basic output directory
    out_dirs : dict
        dictionary containing output directories relative to `out_basedir`
        (will be filled automatically in :func:`init_dirs`)
    obs_config : dict
        dictionary containing configuration details for individual observations
        (i.e. instances of :class:`ObsConfigEval` for each observation) used 
        for the analysis.
    obs_ignore : list, optional
        list of observations that are supposed to be ignored in analysis 
        (keys from :attr:`obs_config`)
    periods : list
        list of periods used for the trends analysis
    regions : dict
        dictionary containing regions used for regional statistics. Keys 
        are region names as displayed in web interface and values are 
        instances of :class:`pyaerocom.Region` for each of the regions.
    var_mapping : dict
        mapping of variable names for menu in interface
    var_order_menu : list, optional
        order of variables in menu.
    slope_alpha : float
        desired confidence of trends slope retrieval (`alpha` parameter 
        in :func:`scipy.stats.theilslopes`), e.g. .68 corresponds to 1sigma
        confidence (68%).
    min_dim : int
        minimum number of measurements per month in order to compute monthly
        averages (does not apply for input data that is already aggregated to
        monthly).
    avg_how : str
        averaging method for temporal aggregation (see :attr:`AVG_OPTS` for 
        allowed values).
    clear_existing_json : bool
        If true, then existing json files for a given run will be deleted 
        before rerunning (per entry in :attr:`obs_config`).
    write_logfiles : bool
        if True, then logfiles will be written for outliers that were 
        identified, errors that occurred and files that were created in the 
        analysis (per entry in :attr:`obs_config`).
    logdir : str
        directory where logfiles are stored.
    """
    #: Vertical layer ranges
    VERT_LAYERS = {'0-2km'  :   [0, 2000],
                   '2-5km'  :   [2000, 5000],
                   '5-10km' :   [5000, 10000]}
    
    #: Names of output directories relative to :attr:`out_basedir`
    OUT_DIR_NAMES = ['ts', 'map']
    
    #: available averaging options for timeseries
    AVG_OPTS = ['mean', 'median']
    
    #: mapping of metadata names between pyaerocom (keys) and json trends files
    #: (values)
    KEYMAP = od(var_name        = 'var_name',
                station_name    = 'station',
                latitude        = 'lat',
                longitude       = 'lon',
                altitude        = 'alt',
                dataset_name    = 'dataset',
                instrument_name = 'instrument',
                ts_type_src     = 'freq_src',
                ts_type         = 'freq',
                PI              = 'PI',
                wavelength      = 'wavelength',
                unit            = 'unit',
                statistics      = 'statistics',
                matrix          = 'size_info',
                overlap_info    = 'data_overlap')
    
    #: supported frequency codes
    TS_TYPES = const.GRID_IO.TS_TYPES
    
    #: Definition of regions for trends interface
    # ToDo: use pyaerocom regions
    DEFAULT_REGIONS = {
            'NAMERICA': 'N-America',
            'SAMERICA': 'S-America',
            'EUROPE': 'Europe',
            'ASIA': 'Asia',
            'CHINA': 'China',
            'AUSTRALIA': 'Australia',
            'NAFRICA': 'N-Africa',
            'SAFRICA': 'S-Africa',
            'INDIA': 'India',
            'WORLD': 'World'
    }
    SEASONS = ['spring','summer','autumn','winter','all']
    def __init__(self, **settings):
        
        self._log = const.print_log
        
        self.out_basedir = None
        self.out_dirs = {}
        
        self.obs_config = {}
        self.obs_ignore = []
        
        self.periods = []
        self.regions = {}
        self._add_regions = {}
        
        self.var_mapping = {}
        self.var_order_menu = []
        
        # options
        self.slope_alpha = 0.68 
        self.min_dim = 5
        self.avg_how = 'mean'
        
        self.clear_existing_json = True
        self.write_logfiles = True
        self.logdir = None
        # initialise
        self.update(**settings)
        if len(self.out_dirs) == 0:
            self._init_dirs()
        self._init_regions()
        self.check_config()
    
    def __setitem__(self, key, val):

        if key == 'obs_config':
            self._set_obsconfig(val)
        elif isinstance(key, str) and isinstance(val, dict):
            if 'obs_id' in val:
                if key in self.obs_config:
                    self._log.warn('Obs config for key {}  already exists and '
                                   'will be overwritten {}'.format(key))
                self.obs_config[key] = ObsConfigEval(**val)
            else:
                self.__dict__[key] = val
        elif key in self.__dict__:
            self.__dict__[key] = val
        else:
            raise KeyError('Invalid input key {}. Cannot assign {}'
                           .format(key, val))
                
    def __getitem__(self, key):
        if not key in self.__dict__:
            raise KeyError('No such key available: {}'.format(key))
        return self.__dict__[key]
        
    def __str__(self):
        indent = 2
        _indent_str = indent*' '
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}".format(head, len(head)*"-")
        obs_cfg = ''
        
        for key, val in self.__dict__.items():
            if key[0] == '_':
                continue
            elif key == 'obs_config':
                for k, v in val.items():
                    obs_cfg += '\n\n{}{}:'.format(_indent_str, k)
                    obs_cfg = dict_to_str(v, obs_cfg, 
                                          indent=indent+2)
            elif isinstance(val, dict):
                s += '\n{}:'.format(key)
                s+= dict_to_str(val, s)
            else:
                s += '\n{}: {}'.format(key, val)
        s += obs_cfg
        return s
    
    def check_config(self):
        """Check if there are any problems in the configuration"""
        for run, cfg in self.obs_config.items():
            if '_' in run:
                raise AttributeError('Invalid name: {} (no underscores allowed)'
                                     .format(run))
            if cfg.obs_id == 'EBASMC':
                check_ebas_default()
    
    def find_obs_matches(self, name_or_pattern):
        """Find model names that match input search pattern(s)
        
        Parameters
        ----------
        name_or_pattern : :obj:`str`, or :obj:`list`
            Name or pattern specifying obs search string. Can also be a list 
            of names or patterns to search for multiple obs networks.
            
        Returns
        -------
        list
            list of model names (i.e. keys of :attr:`obs_config`) that match 
            the input search string(s) or pattern(s)
            
        Raises
        ------
        KeyError
            if no matches can be found
        """
        
        
        if isinstance(name_or_pattern, str):
            name_or_pattern = [name_or_pattern]
        matches = []
        for search_pattern in name_or_pattern:
            for mname in self.obs_config:
                if fnmatch(mname, search_pattern) and not mname in matches:
                    matches.append(mname)
        if len(matches) == 0:
            raise KeyError('No models could be found that match input {}'
                           .format(name_or_pattern))
        return matches
    
    def check_model_access(self, models, vars_to_retrieve):
        """Check availability of input variables in input model IDs
        
        Parameters
        ----------
        models : list
            list of model IDs that can be accessed via class
            :class:`pyaerocom.io.ReadGridded`
        vars_to_retrieve : list
            list of variable names that are supposed to be checked in models
            
        Returns
        -------
        dict
            keys are models and values are lists of variables that are 
            available in each of these models
        """
        maccess = {}
        for model_id in models:
            maccess[model_id] = []
            r = ReadGridded(model_id)
            for var in vars_to_retrieve:
                if var in r.vars_provided:
                    maccess[model_id].append(var)
                    
        return maccess
    
    def load_ungridded(self, network_id, vars_to_retrieve, **constraints):
        """Load obsdata into instance of :class:`pyaerocom.UngriddedData`
        
        Parameters
        ----------
        network_id : str
            Name of network (if you don't know the options, check 
            `pyaerocom.const.OBS_IDS`)
        vars_to_retrieve 
            str or list / tuple of strings specifying AEROCOM variables that are 
            supposed to be imported
        **constraints
            Further reading constraints passed to :func:`UngriddedData.read` and
            from there, further passed to :func:`read`  of respective network
            reading class. 
            
        Returns
        -------
        UngriddedData
        """
        import pyaerocom as pya
        r = pya.io.ReadUngridded()
        return r.read(datasets_to_read=network_id,
                      vars_to_retrieve=vars_to_retrieve,
                      **constraints)
        
    def run_evaluation(self, obs_name=None, update_menu=True, 
                       write_logfiles=None, clear_existing_json=None):
        """Run trends evaluation (main function of this interface)
        
        Note
        ----
        Individual runs are / can be specified in :attr:`obs_config`
        
        Parameters
        -----------
        obs_name : str or list, optional
            name(s) of run(s). If None, then all runs available in 
            :attr:`obs_config` are used.
        update_menu : bool
            if True, the menu.json file is automatically updated (if 
            applicable)
        write_logfiles : bool, optional
            option to write logfiles (uses :attr:`write_logfiles` if None,
            else, updates the latter)
        clear_existing_json : bool, optional
            option to write logfiles (uses :attr:`clear_existing_json` if None,
            else, updates the latter)
        
        Returns 
        -------
        dict
            nested dictionary containing information about the individual runs 
            (keys), that is, the output from :func:`run_single` for each of the 
            runs.
        """
        if write_logfiles is not None:
            self.write_logfiles = write_logfiles
        if clear_existing_json is not None:
            self.clear_existing_json = clear_existing_json
        if obs_name is None:
            obs_list = list(self.obs_config)
        else:
            obs_list = self.find_obs_matches(obs_name)
        result = {}
        
        for obs_name in obs_list:
            result[obs_name] = self.run_single(obs_name, write_logfiles)
        for name, files_written in result.items():
            print('Files written:')
            print('RUN: {}'.format(name))
            for k, v in files_written.items():
                print('Folder: {}'.format(k))
                print('Files: {}'.format(v))
        return result
    
    def run_single(self, obs_name, write_logfiles):
        """Run one of the config entries in :attr:`obs_config`
        
        Parameters
        ----------
        obs_name : str
            name of run (key in :attr:`obs_config`)
        write_logfiles : bool
            write logfiles
        
        Returns
        -------
        dict
            map and ts files that were created
        """
        
        if not obs_name in self.obs_config:
            raise ValueError('No such run with name {}'.format(obs_name))
        config = self.obs_config[obs_name]
        if self.clear_existing_json:
            print('Deleting existing files for run {}'.format(obs_name))
            self.clear_existing(obs_name)
            
        vars_to_retrieve = config['obs_vars']
        obs_id = config['obs_id']
        
        self._log.info('Running {} (NETWORK {})'.format(obs_name, obs_id))
            
        try:
            constraints = config['read_opts_ungridded']
        except:
            constraints = {}
        
        outlier_log, err_log, files_log = None, None, None
        if write_logfiles:
            outlier_log, err_log, files_log = self._init_logfiles(obs_name)
            
        if 'var_outlier_ranges' in config:
            min_max = config['var_outlier_ranges']
        else:
            min_max = {}
        if 'min_dim' in config:
            min_dim = config['min_dim']
        else:
            min_dim = self.min_dim
        if 'models' in config:
            models = config['models']
        else:
            models = None
            
        files_created = {'ts'  : [],
                         'map' : []}
        
        ungridded_data = self.load_ungridded(obs_id, vars_to_retrieve, 
                                             **constraints)
        
        if config['obs_vert_type']=='Profile':
            files_created = self._run_single_3d(ungridded_data=ungridded_data, 
                                                vars_to_retrieve=vars_to_retrieve,
                                                min_max=min_max, 
                                                min_dim=min_dim,
                                                models=models, 
                                                name=obs_name, 
                                                files_created=files_created, 
                                                err_log=err_log)
        else:
            files_created = self._run_single_2d(ungridded_data=ungridded_data, 
                                                vars_to_retrieve=vars_to_retrieve,
                                                min_max=min_max, 
                                                min_dim=min_dim,
                                                models=models, 
                                                name=obs_name, 
                                                files_created=files_created, 
                                                err_log=err_log)
        
        if write_logfiles:
            files_log.write('MAP files\n---------------------------\n')
            for f in files_created['map']:
                files_log.write('{}\n'.format(f))
            files_log.write('Station ts files\n---------------------------\n')
            for f in files_created['ts']:
                files_log.write('{}\n'.format(f))
                
        if write_logfiles:
            outlier_log.close()
            err_log.close()
            files_log.close()
        return files_created
    
    def update(self, **settings):
        """Update current setup"""
        for k, v in settings.items():
            self[k] = v
    
    def from_json(self, config_file):
        """Load configuration from json config file"""
        with open(config_file, 'r') as f:
            current = simplejson.load(f)
        self.update(**current)  
    
    def print_run_ids(self, check_existing=True, detailed=False):
        """Prints all available run ID's 
        
        Parameters
        ----------
        check_existing : bool
            if True, a check is performed for each run ID, whether .json files 
            exist in the data repository
        detailed : bool
            if True, the corresponding settings for the run are printed too
        """
        for run, info in self.obs_config.items():
            print('Run ID: {}'.format(run))
            if detailed:
                for item, value in info.items():
                    print('{}: {}'.format(item, value))
    
            if check_existing:
                there = False
                try:
                    files = os.listdir(self.out_dirs['map'])
                    for file in files:
                        if run in file:
                            there = True
                            break
                    print('data files (json) exist: {}'.format(there))
                except:
                    print('Failed to check for existing runs for ID {}'.format(run))
            print()
            
    def clear_existing(self, obs_name):
        """Delete existing json files for a certain run
        
        Note
        ----
        Clearing old files is recommended before a new run is started 
        for this ID.
        
        Parameters
        ----------
        obs_name : str
            name of observation (key of :attr:`obs_config`)
        """
        
        for d in self.out_dirs.values():
            for f in os.listdir(d):
                if f.split('_')[0] == obs_name:
                    self._log.info('Removing file {}'.format(f))
                    os.remove(d+f)
                    
    def _init_regions(self):
        """Initiate regions to assign lat / lon coordinates"""
        regs = {}
        for reg_id, reg_name in self.DEFAULT_REGIONS.items():
            regs[reg_name] = Region(reg_id)
        for reg_name, info in self._add_regions.items():
            try:
                regs[reg_name] = Region(name=reg_name, 
                                        lat_range=info['lat_range'],
                                        lon_range=info['lon_range'])
            except:
                self._log.warning('Failed to add region {}: {}'
                                  .format(reg_name, info))
        self.regions = regs
                  
    def _init_dirs(self, out_basedir=None):
        """Check and create directories"""
        if out_basedir is not None:
            self.out_basedir = out_basedir
        if self.out_basedir is None:
            self.out_basedir = const.OUTPUTDIR
        check_dirs_exist(self.out_basedir)
        outdirs = {}
        for dname in self.OUT_DIR_NAMES:
            outdirs[dname] = os.path.join(self.out_basedir, dname)
        check_dirs_exist(**outdirs)
        self.out_dirs = outdirs
        
        if self.logdir is None:
            self.logdir = os.path.join(const.OUTPUTDIR, 'logfiles')
        check_dirs_exist(self.logdir)
        self._check_output_dirs()
    
    def _check_output_dirs(self):
        """Check if relevant output directories for json files exist"""
        dirs = self.out_dirs
        for k, d in dirs.items():
            if not os.path.exists(d):
                raise IOError('Directory does not exist: {}'.format(d))
            elif not os.access(d, os.W_OK):
                raise PermissionError('Cannot write to {}'.format(d))
            
    
    
    def _set_obsconfig(self, val):
        cfg = {}
        for k, v in val.items():
            cfg[k] = ObsConfigEval(**v)
        self.obs_config = cfg
            
    def _get_season(self, m, yr):
        if m in [3,4,5]:
            return 'spring-{}'.format(int(yr))
        if m in [6,7,8]:
            return 'summer-{}'.format(int(yr))
        if m in [9,10,11]:
            return 'autumn-{}'.format(int(yr))
        if m in [12]:
            return 'winter-{}'.format(int(yr)+1)
        if m in [1,2]:
            return 'winter-{}'.format(int(yr))
        raise ValueError('Failed to retrieve season for m={}, yr={}'
                         .format(m, yr))
    
    def _mid_season(self, seas, yr):
        if seas=='spring':
            return np.datetime64('{}-04-15'.format(yr))    
        if seas=='summer':
            return np.datetime64('{}-07-15'.format(yr))
        if seas=='autumn':
            return np.datetime64('{}-10-15'.format(yr))    
        if seas=='winter':
            return np.datetime64('{}-01-15'.format(yr))    
        if seas=='all':
            return np.datetime64('{}-06-15'.format(yr))    
        raise ValueError('Invalid input for season (seas):', seas)
    
    def _find_area(self, lat, lon):
        """Find area corresponding to input lat/lon coordinate
        
        Parameters
        ----------
        lat : float
            latitude
        lon : float
            longitude
        
        Returns
        -------
        str
            name of region
        """
        reg = find_closest_region_coord(lat, lon)
        if reg in self.DEFAULT_REGIONS:
            return self.DEFAULT_REGIONS[reg]
        return reg
    
    def _save_stat_json(self, trends_stat, var_name, network_id):
        """Save station json file
        
        Parameters
        ----------
        trends_stat 
            
        var_name
        
        network_id
        
        outputdir
            
        """
        #writes json file
        station_name = trends_stat['station']
        filename = '{}_{}_{}.json'.format(network_id, var_name, station_name)
        outfile = os.path.join(self.out_dirs['ts'], filename)
        
        pd.DataFrame(trends_stat).T.reset_index().to_json(outfile,
                                                          double_precision=5) 
    
        return filename
    
    def _remove_outliers(self, stat, var_name, min_max, logfile=None):
        """Remove outliers from StationData objects"""
        
        raw = stat[var_name]
        len0 =  len(raw)
        notnan = ~np.isnan(raw)
        
        vals = raw[notnan]
        
        notok = np.logical_or(vals<min_max[0], vals>min_max[1])
        #notok = ~((vals > min_max[0]) & (vals < min_max[1]))
        vals_invalid = vals[notok]
        
        if len(vals_invalid) == 0:
            return stat
        
        if logfile is not None:        
            for dtime, val in vals_invalid.iteritems():
                logfile.write('{},{},{},{},{:.3f}\n'.format(stat.dataset_name, 
                                                        stat.station_name, 
                                                        var_name,
                                                        dtime,
                                                        val))
                
        try:
            stat[var_name].ix[vals_invalid.index] = np.nan
        except:
            pass
        
        if not len(stat[var_name]) == len0:
            raise Exception('Length mismatch of input and output arrays, developers, please check')
        elif all(np.isnan(stat[var_name])):
            raise DataCoverageError('No valid data remains after removing outliers')
        return stat
    
    def _station_to_timeseries(self, station, var_name, **alt_range):
        
        keymap = self.KEYMAP
        vardata = {}
        try:
            vardata['data_revision'] = station.data_revision
        except:
            vardata['data_revision'] = None
        vardata['pyaerocom_version'] = __version__
        vardata['data_overlap'] = False
        
        if var_name in station.overlap:
            vardata['data_overlap'] = True
        if var_name in station['var_info']:
            var_info =  station['var_info'][var_name]
        else:
            var_info = {}
        for k, v in keymap.items():
            if v in vardata and not v == 'data_overlap':
                raise Exception('Please debug...')
            try: # longitude, latitude and altitude are @property decorators in StationData
                vardata[v] = station[k]
            except:   
                if k in var_info:
                    vardata[v] = var_info[k]
        # fill up missing keys
        for v in keymap.values():
            if not v in vardata:
                vardata[v] = None
                
        # this is necessary, as e.g. altitude attribute of input station data 
        # is not necessarily the station coordinate!
        for cname, cval in station.get_station_coords().items():
            if not isnumeric(cval):
                raise ValueError
                
            vardata[keymap[cname]] = np.float64(cval)
        # the actual sampling frequency
        freq = vardata['freq']
        
        ts_types = self.TS_TYPES
        if freq in ts_types:
            #raise AttributeError('Invalid temporal resolution code {}'.format(freq))
            if ts_types.index(freq) <= ts_types.index('daily'):
                to_freq = 'daily'
                freq_name = 'dobs'
            elif ts_types.index(freq) <= ts_types.index('monthly'):
                to_freq = 'monthly'
                freq_name = 'mobs'
            else:
                raise NotImplementedError
        elif freq == 'n/d':
            to_freq = 'daily'
            freq_name = 'dobs'
        else:
            raise AttributeError('Invalid ts_type {} in data...')
        
        s = station.to_timeseries(var_name, freq=to_freq,
                                  resample_how=self.avg_how, 
                                  **alt_range)
        
        if len(s) == 0 or all(np.isnan(s)):
            raise DataCoverageError('Failed to retrieve timeseries')
        values = s.values
        index = s.index.values
        
        jsdate = self._to_jsdate(index)
        dates = pd.DatetimeIndex(index)
        
        
        d = od(year=dates.year,
               month=dates.month,
               day=dates.day,
               value=values,
               date=index,
               jsdate=jsdate)    
    
        vardata[freq_name] = pd.DataFrame(d)
        
        return vardata
    
    def _daily2monthly(self, daily, min_dim):
        """Helper to convert daily to monthly 
        """
        # Group data first by year, then by month
        g = daily.groupby(["year", "month"])
        # For each group, calculate the average of value
        _m = g.aggregate({"value":np.mean})
        numdays = g.size()
        
        # NOTE: BEFORE 16.5.19
        #invalid_mask = numdays <= min_dim
        # NOTE: AFTER 16.5.19
        invalid_mask = numdays < min_dim
        _m['value'].loc[invalid_mask] = np.nan
        
        
        #js date
        _m.reset_index(inplace=True)
        if not len(_m['value']) > 0:
            raise DataCoverageError('Derived monthly averages do not contain '
                                    'data')
        # Todo: check this, this seems cumbersome
        dates = _m.apply(lambda row: datetime.datetime(int(row['year']),
                                                       int(row['month']), 
                                                       15), axis=1)
     
        
        monthly = pd.Series(_m.value.values, dates.values)#.resample('MS').mean()
        monthly = monthly.resample('MS').mean()
        monthly.index = monthly.index.shift(14, 'D')
        
        dates = monthly.index
        jsdate = self._to_jsdate(monthly.index.values)
        
        return pd.DataFrame(od(year=dates.year,
                               month=dates.month,
                               day=dates.day,
                               value=monthly.values,
                               date=dates,
                               jsdate=jsdate))
    
    def _check_frequency_and_prep_mobs(self, data, min_dim):
        """Check frequency in data and if higher than monthly, create and append monthly
        
        Parameters
        ----------
        data : dict
            return value from :func:`_station_to_timeseries`
            
        Returns
        -------
        tuple
            2-element tuple, containing
            
            - str, granularity (daily, monthly)
            - DataFrame, containing monthly results
        """
        if 'dobs' in data:
            granulo = 'daily'
    
            #monthly avg
            #drop na values
            # FOLLOWING LINE COMMENTED OUT BY JGLISS (17.12.2018)
            daily = data['dobs'].dropna(subset=['value'])
            if len(daily) == 0:
                raise DataCoverageError('{}: Derived daily averages do not contain '
                                        'data'.format(data['station']))
            
            mobs = self._daily2monthly(daily, min_dim)
            data['mobs'] = mobs
            
        elif 'mobs' in data:
            granulo = 'monthly'
            mobs = data['mobs'].reset_index()
        else:
            raise Exception('Unexpected Error. Data should either contain daily '
                            'or monthly averages, please check function '
                            '_station_to_timeseries and debug')
        return (granulo, data)
    
    @staticmethod
    def _to_jsdate(dates):
        """Convert datetime vector to jsdate vector"""
        epoch = np.datetime64('1970-01-01')
        
        return (dates - epoch).astype('timedelta64[ms]').astype(int)
    
    @staticmethod
    def _years_from_periodstr(period):
        """Convert period str to start / stop years
        
        Parameters
        ----------
        period : str
            period str, e.g. '1990-2010'
            
        Returns
        -------
        int
            start year
        int 
            stop year
        """
        return [int(x) for x in period.split('-')]
    
    @staticmethod
    def _init_trends_result_dict(start_yr):
        keys = ['pval', 'm', 'm_err', 
                'n', 'y_mean', 'y_min', 'y_max', 'coverage',
                'slp', 'slp_err', 'reg0', 't0', # data specific
                'slp_{}'.format(start_yr), # period specific
                'slp_{}_err'.format(start_yr), # period specific
                'reg0_{}'.format(start_yr) # period specific
                ]
        return dict.fromkeys(keys)
    
    @staticmethod
    def _compute_trend_error(m, m_err, v0, v0_err):
        """Computes error of trend estimate using gaussian error propagation
        
        The (normalised) trend is computed as T = m / v0
        
        where m denotes the slope of a regression line and v0 denotes the 
        normalistation value. This method computes the uncertainty of T (delta_T)
        using gaussian error propagation of uncertainties accompanying m and v0.
        
        Parameters
        ----------
        m : float
            slope in units of <U> yr-1 (where <U> denotes the unit of the data).
            (m -> "montant").
        m_err : float
            slope error (same unit as `m`)
        v0 : float
            normalisation value in units of <U>
        v0_err : float
            error of `v0` (same units as `v0`)
        
        Returns
        -------
        float
            error of T in computed using gaussian error propagation of trend 
            formula in units of %/yr
        """
        delta_sl = m_err / v0
        delta_ref = m * v0_err / v0**2
        return np.sqrt(delta_sl**2 + delta_ref**2) * 100
    
    @staticmethod
    def _compute_trend_error_alt(reg, residual_magnitude, dt):
        """Alternative way to compute error of trend estimate 
        
        Parameters
        ----------
        m : float
            slope in units of <U> yr-1 (where <U> denotes the unit of the data).
            (m -> "montant").
        
        Returns
        -------
        float
            error of T computed using gaussian error propagation of trend formula
        """
        v0 = reg[0]
        vlast = reg[-1]
        v0_low = v0 - residual_magnitude
        v0_high = v0 + residual_magnitude
        
        vlast_low = vlast - residual_magnitude
        vlast_high = vlast + residual_magnitude
        
        T1 = (vlast_low - v0_high) / (dt * v0_high) *100
        T2 = (vlast_high - v0_low) / (dt * v0_low) * 100
        
        return (T1, T2)
    
    def _compute_trends_helper(self, data, periods, seasons):
        #trends with yearly and seasonal averages
         #add season to monthly data
        mobs = data['mobs']
        
        mobs['season'] = mobs.apply(lambda row: self._get_season(row['month'],
                                                                 row['year']), 
                                    axis=1)
        
        mobs = mobs.dropna(subset=['value'])
        # FOLLOWING LINE COMMENTED OUT BY JGLISS (17.12.2018)
        #data['dobs'].dropna(subset=['value'],inplace=True)
        # Group data first by year, then by month
        
        yrs = np.unique(mobs['year'])
        
        for i, seas in enumerate(seasons):
            dates = []
            
            #initialize seasonal object
            data[seas] = {'date'    : [], 
                          'jsdate'  : [], 
                          'val'     : [],
                          'trends'  : {}}
            #filter the months
            for yr in yrs:
                if seas == 'all': #yearly trends
                    catch = mobs[mobs['year'] == yr]
                else:
                    catch = mobs[mobs['season'].str.contains('{}-{}'.format(seas, yr))]
                
                dates.append(self._mid_season(seas, yr))
    
                #needs 4 seasons to compute seasonal average to avoid biases
                if seas=='all' and len(np.unique(catch['season'].values)) < 4:
                    data[seas]['val'].append(np.nan)
                else:
                    data[seas]['val'].append(np.nanmean(catch['value']))
            
            # assign dates and jsdates vector to data dict
            data[seas]['date'] = np.asarray(dates)
            if len(dates) > 0:
                data[seas]['jsdate'] = self._to_jsdate(data[seas]['date'])
            else:
                data[seas]['jsdate'] = np.asarray([])
            
            #filter period
            for period in periods:
                # init dictionary that will contain trends results for this period
                data[seas]['trends'][period] = {}
                
                # desired start / stop year (note, that this may change if first 
                # or last value in tseries (or both) is NaN)
                start_yr, stop_yr = self._years_from_periodstr(period)
                
                start_date = self._mid_season(seas, start_yr)
                stop_date = self._mid_season(seas, stop_yr)
                
                period_index = pd.date_range(start=start_date,
                                             end=stop_date, 
                                             freq=pd.DateOffset(years=1))
                
                num_dates_period = period_index.values.astype('datetime64[Y]').astype(np.float64)
                
                #filtering to the period limit
                jsp0 = self._to_jsdate(np.datetime64('{}-01-01'.format(start_yr)))
                jsp1 = self._to_jsdate(np.datetime64('{}-12-31'.format(stop_yr)))
                
                # vector containing numerical timestamps in javascript format
                jsdate = data[seas]['jsdate']
                dates = data[seas]['date']
                
                # get period filter mask
                tmask = np.logical_and(jsdate>=jsp0, jsdate<=jsp1) 
                
                # apply period mask to jsdate vector and value vector
                jsdate_data = jsdate[tmask]
                dates_data = dates[tmask]
                
                # vector containing data values
                vals = np.asarray(data[seas]['val'])[tmask]
                
                valid = ~np.isnan(vals)
                
                #works only on not nan values
                jsdate_data = jsdate_data[valid].astype(np.float64)
                dates_data = dates_data[valid]
                
                num_dates_data = dates_data.astype('datetime64[Y]').astype(np.float64)
                
                vals = vals[valid]           
                
                result = self._init_trends_result_dict(start_yr)
                
                #TODO: len(y) is number of years - 1 due to midseason averages
                result['n'] = len(vals)
                
                if len(vals) > 2:
                    result['y_mean'] = np.nanmean(vals)
                    result['y_min'] = np.nanmin(vals)
                    result['y_max'] = np.nanmax(vals)
                    
                    #Mann / Kendall test
                    [tau, pval] = kendalltau(x=num_dates_data, y=vals)
                    
                    
                    (slope, 
                     yoffs, 
                     slope_low, 
                     slope_up) = theilslopes(y=vals, x=num_dates_data, 
                                             alpha=self.slope_alpha)
                    
                    # estimate error of slope at input confidence level
                    slope_err = np.mean([abs(slope - slope_low), 
                                         abs(slope - slope_up)])
                    
                    reg_data = slope * num_dates_data + yoffs
                    reg_period = slope * num_dates_period  + yoffs
                    
                    
                    # value used for normalisation of slope to compute trend T
                    # T=m / v0
                    v0_data = reg_data[0]
                    v0_period = reg_period[0]
                    
                    # Compute the mean residual value, which is used to estimate
                    # the uncertainty in the normalisation value used to compute
                    # trend
                    mean_residual = np.mean(np.abs(vals - reg_data))
                    
                    # trend is slope normalised by first reference value. 
                    # 2 trends are computed, 1. the trend using the first value of
                    # the regression line at the first available data year, 2. the
                    # trend corresponding to the value corresponding to the first
                    # year of the considered period.
                    
                    trend_data = slope / v0_data * 100
                    trend_period =  slope / v0_period * 100
                    
                    # Compute errors of normalisation values
                    v0_err_data = mean_residual
                    t0_data, tN_data = num_dates_data[0], num_dates_data[-1]
                    t0_period = num_dates_period[0]
                    
                    # sanity check
                    assert t0_data < tN_data
                    assert t0_period <= t0_data
                    
                    dt_ratio = (t0_data - t0_period) / (tN_data - t0_data)
                    
                    v0_err_period = v0_err_data * (1 + dt_ratio)
                    
                    trend_data_err = self._compute_trend_error(m=slope,
                                                               m_err=slope_err,
                                                               v0=v0_data,
                                                               v0_err=v0_err_data)
                                                              
                    trend_period_err = self._compute_trend_error(m=slope,
                                                                 m_err=slope_err,
                                                                 v0=v0_period,
                                                                 v0_err=v0_err_period)
                                    
                    result['pval'] = pval
                    result['m'] = slope
                    result['m_err'] =slope_err
                    
                    result['slp'] = trend_data
                    result['slp_err'] = trend_data_err
                    result['reg0'] = v0_data
                    result['t0'] = jsdate_data[0]
                    if v0_period > 0:
                        result['slp_{}'.format(start_yr)] = trend_period
                        result['slp_{}_err'.format(start_yr)] = trend_period_err
                        result['reg0_{}'.format(start_yr)] = v0_period
                
                data[seas]['trends'][period] = result
        return data
    
    def _compute_trends_station(self, data, min_dim):
        """Compute trends for station
        
        Slightly modified code from original trends interface developed by 
        A. Mortier.
        
        Main changes applied:
            
            - Keep NaNs
        """
        granulo, data = self._check_frequency_and_prep_mobs(data, min_dim)
        
        seasons = self.SEASONS
        # get monthly values for display in interface ('mobs' is modified in 
        # _compute_trends_helper, e.g. NaNs are removed from it)
        jsdate = data['mobs'].jsdate.values
        monthly_vals = data['mobs'].value.values
        
        data = self._compute_trends_helper(data, self.periods, seasons)        
    
        #creates dictionary
        trends_stat = {'daily': {}, 'monthly': {}, 'season': {}}
        
        trends_stat['data_revision'] = data['data_revision']
        trends_stat['pyaerocom_version'] = data['pyaerocom_version']
        metakeys = self.KEYMAP.values()
        for metakey in metakeys:
            if metakey in data:
                trends_stat[metakey] = data[metakey]
        
        if granulo=='daily':
            trends_stat['daily']['date'] = data['dobs']['jsdate'].values
            trends_stat['daily']['val'] =  data['dobs']['value'].values
        elif granulo=='monthly':
            trends_stat['daily']['date'] = []
            trends_stat['daily']['val'] =  []
            
        trends_stat['monthly']['date'] = jsdate
        trends_stat['monthly']['val'] =  monthly_vals
        for seas in seasons:
            trends_stat['season'][seas] = {'date'  : data[seas]['jsdate'], 
                                           'val'   : data[seas]['val'], 
                                           'trends': data[seas]['trends']}
        
        reg = self._find_area(data['lat'], data['lon'])
        if reg == 'WORLD':
            reg = None
        # station information for map view
        map_stat = {'site'      : data['station'], 
                    'lat'       : data['lat'], 
                    'lon'       : data['lon'], 
                    'alt'       : data['alt'], 
                    'region'    : reg}
        
        
        for seas in seasons:
            map_stat[seas] = data[seas]['trends']
    
        return trends_stat, map_stat
    
    def _init_logfiles(self, obs_name):
        from datetime import datetime
        nowstr = datetime.strftime(datetime.now(), '%Y%m%d')
        
        outlier_log = open(os.path.join(self.logdir,
                                        'Run_{}_outliers_{}.log'
                                        .format(obs_name, nowstr), 'w+'))
        err_log = open(os.path.join(self.logdir,
                                        'Run_{}_errors_{}.log'
                                        .format(obs_name, nowstr), 'w+'))
        files_log = open(os.path.join(self.logdir,
                                        'Run_{}_outfiles_{}.log'
                                        .format(obs_name, nowstr), 'w+'))
        return (outlier_log, err_log, files_log)
    
    def _run_single_2d(self, ungridded_data, vars_to_retrieve, min_max,
                       min_dim, models, name, files_created, err_log):
        if models is not None and len(models) > 0:
            model_access = self.check_model_access(models,
                                                   vars_to_retrieve)
              
            for model_id, vars_avail in model_access.items():
                raise NotImplementedError
    
        files_created = self._run_single_helper(ungridded_data=ungridded_data, 
                                                vars_to_retrieve=vars_to_retrieve, 
                                                min_max=min_max, 
                                                name=name, 
                                                files_created=files_created,
                                                min_dim=min_dim, 
                                                err_log=err_log)
        return files_created
    
    def _run_single_3d(self, ungridded_data, vars_to_retrieve, min_max,
                       min_dim, models, name, files_created, err_log):
        if models is not None:
            raise NotImplementedError('Cannot yet colocate 3D observations '
                                      'with model data ...')
        for add_name, alt_range in self.VERT_LAYERS.items():
            files_created = self._run_single_helper(ungridded_data=ungridded_data, 
                                                    vars_to_retrieve=vars_to_retrieve, 
                                                    min_max=min_max, 
                                                    min_dim=min_dim,     
                                                    name=name, 
                                                    files_created=files_created,
                                                    add_name=add_name, 
                                                    err_log=err_log,
                                                    altitude=alt_range)
        return files_created
    
    def _run_single_helper(self, ungridded_data, vars_to_retrieve, min_max,
                           name, files_created, min_dim, add_name=None,
                           err_log=None, **alt_range):
        from pyaerocom.exceptions import DataCoverageError
        if add_name is None:
            add_name = ''
        else:
            add_name = ':{}'.format(add_name)
        for var in vars_to_retrieve:
            
            stations = ungridded_data.to_station_data_all(vars_to_convert=var,
                                                          merge_if_multi=True,
                                                          by_station_name=True)['stats']
    
            var_out = var
            stats_processed = []
            MAP = []
            rng = None
            if var in min_max:
                rng = min_max[var]
            
            got_one = False
            for stat in stations:
                stat_name = stat['station_name']
                print(var, stat['station_name'], name)
                if stat_name in stats_processed:
                    raise Exception('Unexpected Error, please check')
                
                try:
                    if rng is not None:
                        stat = self._remove_outliers(stat, var_name=var, 
                                                     min_max=rng)
                    
                    data_dict = self._station_to_timeseries(stat, 
                                                            var_name=var, 
                                                            **alt_range)
                    (trends_stat, 
                     map_stat) = self._compute_trends_station(data_dict,
                                                              min_dim=min_dim)
                    vname = var_out + add_name
                    fname = self._save_stat_json(trends_stat, 
                                                 var_name=vname, 
                                                 network_id=name)
                    files_created['ts'].append(fname)
                    got_one = True        
                        
                    if map_stat:
                        MAP.append(map_stat)
                        
                except DataCoverageError as e:
                    msg = 'Error: {} {}, {}'.format(var, stat.station_name,repr(e))
                    print(msg)
                    if err_log:
                        err_log.write(msg + '\n')
                
                
         
            # Add to map only if at least one station is available
            if got_one:
                map_outname = '{}_{}.json'.format(name, var_out + add_name)
                
                outfile_map =  os.path.join(self.out_dirs['map'], map_outname)
                with open(outfile_map, 'w') as f:
                    simplejson.dump(MAP, f, ignore_nan=True)
                files_created['map'].append(map_outname)
        
        return files_created
    
def check_ebas_default():
    """Make sure the EBAS default configuration has not changed"""
    from pyaerocom.io import ReadEbas
    r = ReadEbas()
    assert r.opts.remove_invalid_flags
    assert r.opts.datalevel == None
    assert r.opts.keep_aux_vars == False
    
if __name__ == '__main__':    
    t = TrendsEvaluation()