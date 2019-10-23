#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fnmatch import fnmatch
import glob
import os
import numpy as np
import simplejson

# internal pyaerocom imports
from pyaerocom._lowlevel_helpers import (check_dirs_exist, dict_to_str)
from pyaerocom import const
from pyaerocom import __version__ as pyaerocom_version
from pyaerocom.mathutils import calc_statistics
from pyaerocom.region import (get_all_default_region_ids, 
                              find_closest_region_coord,
                              Region)
from pyaerocom.io.helpers import save_dict_json

from pyaerocom.web.helpers import (ObsConfigEval, ModelConfigEval, 
                                   update_menu_evaluation_iface, 
                                   make_info_table_evaluation_iface, 
                                   read_json, write_json)
from pyaerocom import ColocationSetup, ColocatedData, Colocator

from pyaerocom.web.obs_config_default import OBS_SOURCES, OBS_DEFAULTS
from pyaerocom.exceptions import DataDimensionError

# ToDo: complete docstring
class AerocomEvaluation(object):
    """Class for creating json files for Aerocom Evaluation interface
    
    High level interface for computation of colocated netcdf files and json
    files for `Aerocom Evaluation interface 
    <https://aerocom-trends.met.no/evaluation/web/>`__. The processing is 
    done *per experiment*. See class attributes for setup options.
    An *experiment* denotes a setup comprising one or more observation 
    networks (specified in :attr:`obs_config`) and the specification of one 
    or more model runs via :attr:`model_config`. These two configuration 
    attributes are dictionaries, where keys correspond to the name of the
    obs / model (as it should appear online) and values specify relevant 
    information for importing the data (see also classes 
    :class:`ModelConfigEval` and :class:`ObsConfigEval`).
    
    In addition to :attr:`model_config, obs_config`, there are more setup 
    settings and options, some of which NEED to be specified (e.g. 
    :attr:`proj_id, exp_id, out_basedir`) and others that may be explicitly 
    specified if desired (e.g. :attr:`harmonise_units, remove_outliers, 
    clear_existing_json`).
    
    The analysis (which can be run via :func:`run_evaluation`) can be summarised
    as follows: for each combination of *variable / obs / model* create one 
    colocated NetCDF file and based on this colocated (single variable) NetCDF 
    file compute all relevant json files for the interface. 
    
    General settings for the colocation (e.g. colocation frequency, start / 
    stop time) can be specified in :attr:`colocation_settings` (for details 
    see :class:`pyaerocom.ColocationSetup`). The colocation routine uses the 
    variables specified in the obs_config entry of the observation network that 
    is supposed to be colocated. If these variables are not provided in a 
    model run or are named differently, then the corresponding model variable 
    that is supposed to be colocated with the observation variable can be 
    specified in the corresponding model entry in :attr:`model_config` via 
    model_use_vars (mapping). Note that this may lead to unit conversion errors 
    if the mapped model variable has a different AeroCom default unit and if 
    outlier ranges are not specified explicitely (see info below).
    
    If :attr:`remove_outliers` is True, then custom outlier ranges for 
    individual variables may be specified in corresponding entry of model in 
    :attr:`model_config`, or, for observation variables
    in :attr:`obs_config`, respectively. 
    NOTE: for each variable that has not specified an outlier range here, the 
    AeroCom default is used, which is specified in pyaerocom data file 
    variables.ini. In the latter case, a unit check is performed in order to 
    make sure the retrieved default outlier ranges are valid. This can cause 
    errors in the colocation if, for instance, a model variable name is used
    that has a different AerocCom default unit than the used observation 
    variable.
    
    Attributes
    ----------
    proj_id : str
        ID of project
    exp_id : str
        ID of experiment
    exp_name : :obj:`str`, optional
        name of experiment 
    clear_existing_json : bool
        Boolean specifying whether existing json files should be deleted for
        var / obs / model combination before rerunning
    out_basedir : str
        basic output directory which defines all further output paths for json
        files 
    out_dirs : dict
        dictionary that specifies the output paths for the different types of
        json files (e.g. map, ts, etc.). Is filled automatically using 
        :attr:`out_basedir, proj_id, exp_id`. Non existing paths are 
        automatically created.
    colocation_settings : dict
        dictionary specifying settings and options for the colocation routine
        (cf. :class:`pyaerocom.ColocationSetup` for available options). 
        Note: the options that are specified in this dictionary are to be 
        understood as global colocation options (for all model / obs 
        combinations defining this experiment). They may be refined or 
        overwritten as required on an individual basis in the definitions for 
        the observations (:attr:`obs_config`) and / or in the model definitions
        (:attr:`model_config`), respectively. The logical order that defines 
        the colocation settings for a certain run (that is, a combination of 
        `var_name, obs_name, model_name`) is:
        is:
            
            1. Import `dict` :attr:`colocation_settings` (global)
            2. Update `dict` with settings from :attr:`obs_config` for \
            `obs_name` (defines `var_name`)
            3. Update `dict` with settings from :attr:`model_config` for \
            `model_name`
     
    add_methods_file : str, optional
        file specifying custom reading methods
    add_methods : dict
        dictionary containing additional reading method
    obs_config : dict
        dictionary containing configuration details for individual observations
        (i.e. instances of :class:`ObsConfigEval` for each observation) used 
        for the analysis.
    obs_ignore : list, optional
        list of observations that are supposed to be ignored in analysis 
        (keys from :attr:`obs_config`)
    model_config : dict
        dictionary containing configuration details for individual models
        (i.e. instances of :class:`ModelConfigEval` for each model) used 
        for the analysis.
    model_ignore : list, optional
        list of models that are supposed to be ignored in analysis 
        (keys from :attr:`model_config`)
    var_mapping : dict
        mapping of variable names for menu in interface
    var_order_menu : list, optional
        order of variables in menu
    """
    OUT_DIR_NAMES = ['map', 'ts', 'scat', 'hm', 'profiles']
    
    
    #: Vertical layer ranges
    VERT_LAYERS = {'0-2km'  :   [0, 2000],
                   '2-5km'  :   [2000, 5000],
                   '5-10km' :   [5000, 10000]}
    
    #: Allowed options for vertical codes
    VERT_CODES = ['Surface', 'Column']
    VERT_CODES.extend(VERT_LAYERS)
    
    #: vertical schemes that may be used for colocation
    VERT_SCHEMES = {'Surface' : 'surface'}
    
    #: Attributes that are ignored when writing setup to json file
    JSON_CFG_IGNORE = ['add_methods', '_log', 'out_dirs']
    
    _OPTS_NAMES_OUTPUT = {
            'clear_existing_json' : 'Delete existing json files before reanalysis',
            'reanalyse_existing'  : 'Reanalyse existing colocated NetCDF files',
            'only_colocation'     : 'Run only colocation (no json files computed)',
            'raise_exceptions'    : 'Raise exceptions if they occur'
    }
                          
    def __init__(self, proj_id=None, exp_id=None, config_dir=None, 
                 try_load_json=True, **settings):
        
        self._log = const.print_log
        
        self.proj_id = proj_id
        
        self.exp_id = exp_id
        
        self.exp_name = None
        
        self.clear_existing_json = True
        
        self.only_colocation = False
        
        #: Base directory for output
        self.out_basedir = None
        
        #: Directory that contains configuration files
        self.config_dir = config_dir
        
        #: Output directories for different types of json files (will be filled
        #: in :func:`init_dirs`)
        self.out_dirs = {}
        
        #: Dictionary specifying default settings for colocation
        self.colocation_settings = ColocationSetup()
        
        self.add_methods_file = None
        self.add_methods = {}
        
        #: Dictionary containing configurations for observations
        self.obs_config = {}
        self.obs_ignore = []
        
        #: Dictionary containing configurations for models
        self.model_config = {}
        self.model_ignore = []
        
        self.var_mapping = {}
        self.var_order_menu = []
        
        self._valid_obs_vars = {}
        if try_load_json and proj_id is not None:
            try:
                self.load_config(self.proj_id, self.exp_id, config_dir)
                const.print_log.warn('Found and imported config file for {} / {}'
                                     .format(self.proj_id, self.exp_id))
            except:
                pass
        self.update(**settings)
        
    
    @property
    def proj_dir(self):
        """Project directory"""
        return os.path.join(self.out_basedir, self.proj_id)
    
    
    @property
    def exp_dir(self):
        """Project directory"""
        return os.path.join(self.proj_dir, self.exp_id)
    
    @property
    def coldata_dir(self):
        """Base directory for colocated data files"""
        return self.colocation_settings['basedir_coldata']
    
    @property
    def regions_file(self):
        """json file containing region specifications"""
        return os.path.join(self.out_basedir, 'regions.json')
    
    @property
    def menu_file(self):
        """json file containing region specifications"""
        return os.path.join(self.proj_dir, 'menu.json')
    
    @property
    def all_model_names(self):
        """List of all model names"""
        return list(self.model_config)
    
    @property
    def all_obs_names(self):
        """List of all obs names"""
        return list(self.obs_config)
    
    @property
    def all_map_files(self):
        """List of all existing map files"""
        if not os.path.exists(self.out_dirs['map']):
            raise FileNotFoundError('No data available for this experiment')
        return os.listdir(self.out_dirs['map'])
    
    def _update_custom_read_methods(self):
        for mcfg in self.model_config.values():
            if not 'model_read_aux' in mcfg:
                continue
            maux = mcfg['model_read_aux']
            if maux is None:
                continue
            elif not isinstance(maux, dict):
                raise ValueError('Require dict, got {}'.format(maux))
            for varcfg in maux.values():
                err_msg_base = ('Invalid definition of model_read_aux')
                if not isinstance(varcfg, dict):
                    raise ValueError('{}: value needs to be dictionary'
                                     .format(err_msg_base))
                if not all([x in varcfg for x in ['vars_required', 'fun']]):
                    raise ValueError('{}: require specification of keys '
                                     'vars_required and fun'
                                     .format(err_msg_base))
                if not isinstance(varcfg['fun'], str):
                    raise ValueError('Names of custom methods need to be strings')
                    
                name = varcfg['fun']
                fun = self.get_custom_read_method_model(name)
                if not name in self.add_methods:
                    self.add_methods[name] = fun
                
                    
    def get_custom_read_method_model(self, method_name):
        """Get custom read method for computation of model variables during read
        
        Parameters
        ----------
        method_name : str
            name of method
            
        Returns
        -------
        callable
            corresponding python method
        
        Raises
        ------
        ValueError
            if no method with the input name can be accessed
        """
        if method_name in self.add_methods:
            fun = self.add_methods[method_name]
        else:
            import sys, importlib
            fp = self.add_methods_file
            
            if fp is None or not os.path.exists(fp):
                raise ValueError('Failed to access custom read method {}'
                                 .format(method_name))
            try:
                moddir = os.path.dirname(fp)
                if not moddir in sys.path:
                    sys.path.append(moddir)
                modname = os.path.basename(fp).split('.')[0]
                if '.' in modname:
                    raise NameError('Invalid name for module: {} (file name must '
                                    'not contain .)'.format(fp))
                mod = importlib.import_module(modname)
            except Exception as e:
                raise ImportError('Failed to import module containing '
                                  'additional custom model read methods '
                                  '.Error: {}'.format(repr(e)))
            if not method_name in mod.FUNS:
                raise ValueError('File {} does not contain custom read '
                                 'method: {}'.format(fp, method_name))
            fun = mod.FUNS[method_name]
        #fun = self.add_methods[name]
        if not callable(fun):
            raise TypeError('{} ({}) is not a callable object'.format(fun, 
                            method_name))
        return fun
        
    def update(self, **settings):
        """Update current setup"""
        for k, v in settings.items():
            self[k] = v
        self.check_config()
        self.init_dirs()
        self._update_custom_read_methods()
        
    def _set_obsconfig(self, val):
        cfg = {}
        for k, v in val.items():
            cfg[k] = ObsConfigEval(**v)
        
        self.obs_config = cfg
        
    def _set_modelconfig(self, val):
        cfg = {}
        for k, v in val.items():
            cfg[k] = ModelConfigEval(**v)
        self.model_config = cfg
        self._update_custom_read_methods()
    
            
    def __setitem__(self, key, val):
        if key in self.colocation_settings:
            self.colocation_settings[key] = val
        elif key == 'obs_config':
            self._set_obsconfig(val)
        elif key == 'model_config':
            self._set_modelconfig(val)
        elif key == 'colocation_settings':
            self.colocation_settings.update(**val)
        elif isinstance(key, str) and isinstance(val, dict):
            if 'obs_id' in val:
                if key in self.obs_config:
                    self._log.warn('Obs config for key {}  already exists and '
                                   'will be overwritten {}'.format(key))
                self.obs_config[key] = ObsConfigEval(**val)
            elif 'model_id' in val:
                if key in self.model_config:
                    self._log.warn('Model config for key {}  already exists and '
                                   'will be overwritten {}'.format(key))
                self.model_config[key] = ModelConfigEval(**val)
            else:
                self.__dict__[key] = val
        elif key in self.__dict__:
            self.__dict__[key] = val
        else:
            raise KeyError('Invalid input key {}. Cannot assign {}'
                           .format(key, val))
                
    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        elif key in self.colocation_settings:
            return self.colocation_settings[key]
    
    def init_dirs(self, out_basedir=None):
        """Check and create directories"""
        if out_basedir is not None:
            self.out_basedir = out_basedir
        if self.out_basedir is None:
            self.out_basedir = const.OUTPUTDIR
        check_dirs_exist(self.out_basedir, self.proj_dir, self.exp_dir)
        outdirs = {}
        for dname in self.OUT_DIR_NAMES:
            outdirs[dname] = os.path.join(self.exp_dir, dname)
        check_dirs_exist(**outdirs)
        self.out_dirs = outdirs
    
    
    
    def check_config(self):
        if not isinstance(self.proj_id, str):
            raise ValueError('proj_id must be string, got {}'.format(self.proj_id))
        
        if not isinstance(self.exp_id, str):
            raise ValueError('exp_id must be string, got {}'.format(self.exp_id))
            
        if not isinstance(self.exp_name, str):
            const.print_log.warning('exp_name must be string, got {}. Using '
                                    'exp_id {} for experiment name'
                                    .format(self.exp_name, self.exp_id))
            self.exp_name = self.exp_id
        
        for k, v in self.model_config.items():
            if '_' in k or ':' in k:
                raise NameError('Model config name must not contain _ (underscore) or colon.')
            elif len(k) > 20:
                print('Long model ID: {}. Consider renaming'.format(k))
            elif len(k) > 25:
                raise ValueError('Too long model ID: {} (max 20 chars)'.format(k))
            elif not 'model_id' in v:
                raise KeyError('Model configuration for {} does not contain '
                               'model_id'.format(k))
        for k, v in self.obs_config.items():
            if '_' in k or ':' in k:
                raise NameError('Obs config name must not contain _ (underscore) or colon')
            elif len(k) > 15:
                print('Long obs ID: {}. Consider renaming'.format(k))
            elif len(k) > 20:
                raise ValueError('Too long obs ID: {} (max 20 chars)'.format(k))
            elif not 'obs_id' in v:
                raise KeyError('Obs configuration for {} does not contain '
                               'obs_id'.format(k))
                
    def get_model_id(self, model_name):
        """Get AeroCom ID for model name
        """
        for name, info in self.model_config.items():
            if name == model_name:
                return info['model_id']
        raise KeyError('Cannot find setup for ID {}'.format(model_name))
    
    def get_obs_id(self, obs_name):
        """Get AeroCom ID for obs name
        """
        for name, info in self.obs_config.items():
            if name == obs_name:
                return info['obs_id']
        raise KeyError('Cannot find setup for ID {}'.format(obs_name))
    
    def find_obs_name(self, obs_id, obs_var):
        """Find web menu name of obs dataset based on obs_id and variable
        """
        matches = []
        for obs_name, info in self.obs_config.items():
            if info['obs_id'] == obs_id and obs_var in info['obs_vars']:
                matches.append(obs_name)
        if len(matches) == 1:
            return matches[0]
        raise ValueError('Could not identify unique obs name')
    
    def find_model_name(self, model_id):
        """Find web menu name of model dataset based on model_id
        """
        matches = []
        for model_name, info in self.model_config.items():
            if info['model_id'] == model_id:
                matches.append(model_name)
        if len(matches) == 1:
            return matches[0]
        raise ValueError('Could not identify unique model name')
            
    def make_regions_json(self):
        """Creates file regions.ini for web interface"""
        regs = {}
        for regname in get_all_default_region_ids():
            reg = Region(regname)
            regs[regname] = r = {}
            latr = reg.lat_range
            r['minLat'] = latr[0]
            r['maxLat'] = latr[1]
            lonr = reg.lon_range
            r['minLon'] = lonr[0]
            r['maxLon'] = lonr[1]
        save_dict_json(regs, self.regions_file)
        return regs
    
    def compute_json_files_from_colocateddata(self, coldata, obs_name=None, 
                                              model_name=None):
        """Creates all json files for one ColocatedData object"""
        if not isinstance(coldata, ColocatedData):
            raise ValueError('Need ColocatedData object, got {}'
                             .format(type(coldata)))
        stats_dummy = {}
        
        for k in calc_statistics([1], [1]):
            stats_dummy[k] = np.nan
        
        stacked = False
        if 'altitude' in coldata.data.dims:
            raise NotImplementedError('Cannot yet handle profile data')
        if not 'station_name' in coldata.data.coords:
            if not coldata.data.ndim == 4:
                raise DataDimensionError('Invalid number of dimensions. '
                                         'Need 4, got: {}'
                                         .format(coldata.data.dims))
            elif not 'latitude' in coldata.data.dims and 'longitude' in coldata.data.dims:
                raise DataDimensionError('Need latitude and longitude '
                                         'dimension. Got {}'
                                         .format(coldata.data.dims))
            coldata.data = coldata.data.stack(station_name=('latitude', 
                                                            'longitude'))
            stacked = True
            
        ts_types_order = const.GRID_IO.TS_TYPES
        to_ts_types = ['daily', 'monthly', 'yearly']
        
        data_arrs = dict.fromkeys(to_ts_types)
        jsdate = dict.fromkeys(to_ts_types)
        
        ts_type = coldata.meta['ts_type']
        for freq in to_ts_types:
            if ts_types_order.index(freq) < ts_types_order.index(ts_type):
                data_arrs[freq] = None
            elif ts_types_order.index(freq) == ts_types_order.index(ts_type):
                data_arrs[freq] = coldata.data
                
                js = (coldata.data.time.values.astype('datetime64[s]') - 
                      np.datetime64('1970', '[s]')).astype(int) * 1000
                jsdate[freq] = js.tolist()
                
            else:
                colstp = self.colocation_settings
                _a = coldata.resample_time(to_ts_type=freq,
                                     apply_constraints=colstp.apply_time_resampling_constraints, 
                                     min_num_obs=colstp.min_num_obs,
                                     colocate_time=colstp.colocate_time,
                                     inplace=False).data
                data_arrs[freq] = _a #= resample_time_dataarray(arr, freq=freq)
                js = (_a.time.values.astype('datetime64[s]') - 
                      np.datetime64('1970', '[s]')).astype(int) * 1000
                jsdate[freq] = js.tolist()      
        
        #print(jsdate)
    
        obs_id = coldata.meta['data_source'][0]
        model_id = coldata.meta['data_source'][1]
        
        obs_var = coldata.meta['var_name'][0]
        model_var = coldata.meta['var_name'][1]
        
        if obs_name is None:
            obs_name = self.find_obs_name(obs_id, obs_var)
            
        if model_name is None:
            model_name = self.find_model_name(model_id)
    
        ts_objs = []
        
        map_data = []
        scat_data = {}
        hm_data = {}
        
        
        #ts_type = coldata.meta['ts_type']
        vert_code = self.get_vert_code(obs_name, obs_var)
        
        # data used for heatmap display in interface
        if stacked:    
            hmd = ColocatedData(data_arrs['monthly'].unstack('station_name'))
        else:
            hmd = ColocatedData(data_arrs['monthly'])
# =============================================================================
#         if ts_type == 'monthly':
#             hmd = coldata
#         else:
#             cs = self.colocation_settings
#             ac = cs.apply_time_resampling_constraints
#             if ac is None:
#                 ac = const.OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS
#                 
#             if ac:
#                 mo = cs.min_num_obs
#                 if cs.min_num_obs is None:
#                     mo = const.OBS_MIN_NUM_RESAMPLE
#                 
#             hmd  = coldata.resample_time(to_ts_type='monthly',
#                                    apply_constraints=ac,
#                                    min_num_obs=mo,
#                                    colocate_time=cs['colocate_time'], 
#                                    inplace=False)
#                                    
# =============================================================================
        for reg in get_all_default_region_ids():
            filtered = hmd.apply_latlon_filter(region_id=reg)
            stats = filtered.calc_statistics()
            for k, v in stats.items():
                stats[k] = np.float64(v)
            
            hm_data[reg] = stats
        
        self._write_heatmap_json(hm_data, obs_name, obs_var, vert_code, 
                                 model_name, model_var)
        
        if vert_code == 'ModelLevel':
            raise NotImplementedError('Coming soon...')
        const.print_log.info('Computing json files for {} vs. {}'
                             .format(model_name, obs_name))
        for i, stat_name in enumerate(coldata.data.station_name.values):
            _disp = ('{} - {} ({}) vs. {} ({})'
                     .format(stat_name, model_name, 
                             coldata.meta['var_name'][1],
                             obs_name, coldata.meta['var_name'][0]))
            has_data = False
            ts_data = {}
            ts_data['station_name'] = stat_name
            ts_data['pyaerocom_version'] = pyaerocom_version
            ts_data['obs_name'] = obs_name
            ts_data['model_name'] = model_name
            ts_data['obs_var'] = coldata.meta['var_name'][0]
            ts_data['obs_unit'] = coldata.meta['var_units'][0]
            ts_data['vert_code'] = vert_code
            ts_data['obs_freq_src'] = coldata.meta['ts_type_src'][0]
            ts_data['obs_revision'] = coldata.meta['revision_ref']
            
            ts_data['mod_var'] = coldata.meta['var_name'][1]
            ts_data['mod_unit'] = coldata.meta['var_units'][1]
            ts_data['mod_freq_src'] = coldata.meta['ts_type_src'][1]
            
            stat_lat = np.float64(coldata.data.latitude[i])
            stat_lon = np.float64(coldata.data.longitude[i])
            if 'altitude' in coldata.data.coords:
                stat_alt = np.float64(coldata.data.altitude[i])
            else:
                stat_alt = np.nan
            region = find_closest_region_coord(stat_lat, stat_lon)
            
            # station information for map view
            map_stat = {'site'      : stat_name, 
                        'lat'       : stat_lat, 
                        'lon'       : stat_lon,
                        'alt'       : stat_alt,
                        'region'    : region}
            
            for tres, arr in data_arrs.items():
                map_stat['{}_statistics'.format(tres)] = {}
                if arr is None:
                    ts_data['{}_date'.format(tres)] = []
                    ts_data['{}_obs'.format(tres)] = []
                    ts_data['{}_mod'.format(tres)] = []
                    map_stat['{}_statistics'.format(tres)].update(stats_dummy)
                    continue
        
                obs_vals = arr.sel(data_source=obs_id, 
                                   station_name=stat_name).values

                if all(np.isnan(obs_vals)):
                    _disp += ': No obs data'
                    ts_data['{}_date'.format(tres)] = []
                    ts_data['{}_obs'.format(tres)] = []
                    ts_data['{}_mod'.format(tres)] = []
                    map_stat['{}_statistics'.format(tres)].update(stats_dummy)
                    continue
                has_data = True
                mod_vals = arr.sel(data_source=model_id, 
                                   station_name=stat_name).values
                
                if not len(jsdate[tres]) == len(obs_vals):
                    raise Exception('Please debug...')
                
                ts_data['{}_date'.format(tres)] = jsdate[tres]
                ts_data['{}_obs'.format(tres)] = obs_vals.tolist()
                ts_data['{}_mod'.format(tres)] = mod_vals.tolist()
                
                station_statistics = calc_statistics(mod_vals, obs_vals)
                for k, v in station_statistics.items():
                    station_statistics[k] = np.float64(v)
                map_stat['{}_statistics'.format(tres)] = station_statistics
            
            if has_data:
                _disp += ': OK'
                ts_objs.append(ts_data)
                map_data.append(map_stat)
                scat_data[str(stat_name)] = sc = {}
                sc['obs'] = ts_data['monthly_obs']
                sc['mod'] = ts_data['monthly_mod']
                sc['region'] = region
            const.print_log.info(_disp)
        dirs = self.out_dirs
    
        map_name = self.get_json_mapname(obs_name, obs_var, model_name, 
                                         model_var, vert_code)
        
        outfile_map =  os.path.join(dirs['map'], map_name)
        with open(outfile_map, 'w') as f:
            simplejson.dump(map_data, f, ignore_nan=True)
        
        outfile_scat =  os.path.join(dirs['scat'], map_name)
        with open(outfile_scat, 'w') as f:
            simplejson.dump(scat_data, f, ignore_nan=True)
            
        for ts_data in ts_objs:
            #writes json file
            self._write_stationdata_json(ts_data)
         
    def get_vert_code(self, obs_name, obs_var):
        """Get vertical code name for obs / var combination"""
        info =  self.obs_config[obs_name]['obs_vert_type']
        if isinstance(info, str):
            return info
        return info[obs_var]
    
    @property
    def _heatmap_file(self):
        return os.path.join(self.out_dirs['hm'], 'glob_stats.json')
    
    def update_heatmap_json(self):
        fp = self._heatmap_file
        if not os.path.exists(fp):
            raise FileNotFoundError(fp)
            
        with open(self.menu_file, 'r') as f:
            menu = simplejson.load(f)
        with open(fp, 'r') as f:
            data = simplejson.load(f)
        if not self.exp_id in menu:
            raise ValueError('No entry found in menu.json for experiment {}'
                             .format(self.exp_id))
        
        menu = menu[self.exp_id]
        hm = {}
        for var, info in menu.items():
            obs_dict = info['obs']
            if not var in hm:
                hm[var] = {}
            for obs, vdict in obs_dict.items():
                if not obs in hm[var]:
                    hm[var][obs] = {}
                for vc, mdict in vdict.items():
                    if not vc in hm[var][obs]:
                        hm[var][obs][vc] = {}
                    for mod, minfo in mdict.items():
                        if not mod in hm[var][obs][vc]:
                            hm[var][obs][vc][mod] = {}
                        modvar = minfo['var']
                        if not modvar in hm[var][obs][vc][mod]:
                            hm[var][obs][vc][mod][modvar] = {}
                        hm_data = data[var][obs][vc][mod][modvar]
                        hm[var][obs][vc][mod][modvar] = hm_data
                            
                            
# =============================================================================
#         new = sort_dict_by_name(data, pref_list=self.var_order_menu)
#         new_sorted = {}
#         for var, obs_dict in new.items():
#             sorted_obs = sort_dict_by_name(obs_dict)
#             new_sorted[var] = sorted_obs
#             for obs_name, vert_codes in sorted_obs.items():
#                 vert_codes_sorted = sort_dict_by_name(vert_codes)
#                 new_sorted[var][obs_name] = vert_codes_sorted
#                 for vert_code, models in vert_codes_sorted.items():
#                     models_sorted = sort_dict_by_name(models)
#                     new_sorted[var][obs_name][vert_code] = models_sorted
# =============================================================================
        with open(fp, 'w') as f:
            simplejson.dump(hm, f, ignore_nan=True)
        
    def _write_heatmap_json(self, result, obs_name, obs_var, vert_code, 
                            model_name, model_var):
        fp = self._heatmap_file
        if os.path.exists(fp):
            try:
                with open(fp, 'r') as f:
                    current = simplejson.load(f)
            except Exception as e:
                raise Exception('Fatal: could not open existing json file: {}. '
                                'Reason: {}'.format(fp, repr(e)))
        else:
            current = {}
        if not obs_var in current:
            current[obs_var] = {}
        ov = current[obs_var]
        if not obs_name in ov:
            ov[obs_name] = {}
        on = ov[obs_name]
        if not vert_code in on:
            on[vert_code] = {}
        ovc = on[vert_code]
        if not model_name in ovc:
            ovc[model_name] = {}
        mn = ovc[model_name]
        if model_var in mn:
            const.print_log.info('Overwriting existing heatmap statistics for '
                                 'model {}/{} ({}, {}, {}) in glob_stats.json'
                                 .format(model_name, model_var, obs_var, obs_name, 
                                         vert_code))
        mn[model_var] = result
        with open(fp, 'w') as f:
            simplejson.dump(current, f, ignore_nan=True)
        
    def _write_stationdata_json(self, ts_data):
        
        filename = self.get_stationfile_name(ts_data['station_name'], 
                                             ts_data['obs_name'],
                                             ts_data['obs_var'],
                                             ts_data['vert_code'])
    
        fp = os.path.join(self.out_dirs['ts'], filename)
        if os.path.exists(fp):
            try:
                with open(fp, 'r') as f:
                    current = simplejson.load(f)
            except Exception as e:
                raise Exception('Fatal: could not open existing json file: {}. '
                                'Reason: {}'.format(fp, repr(e)))
        else:
            current = {}
        current[ts_data['model_name']] = ts_data
        with open(fp, 'w') as f:
            simplejson.dump(current, f, ignore_nan=True)
            
    def get_stationfile_name(self, station_name, obs_name, obs_var, vert_code):
        """Get name of station timeseries file"""
        return ('{}_OBS-{}:{}_{}.json'
                .format(station_name, obs_name, obs_var, vert_code))
    
    
    def get_json_mapname(self, obs_name, obs_var, model_name, model_var, 
                           vert_code):
        """Get name base name of json file""" 
        return ('OBS-{}:{}_{}_MOD-{}:{}.json'
                .format(obs_name, obs_var, vert_code, model_name, model_var))
    
    def find_coldata_files(self, model_name, obs_name, var_name=None):
        """Find colocated data files for a certain model/obs/var combination
        
        Parameters
        ----------
        model_name : str
            name of model
        obs_name : str
            name of observation network
        var_name : str, optional
            name of variable.
            
        Returns
        -------
        list
            list of file paths of ColocatedData files that match input specs
        """
        
        files = []
        model_id = self.get_model_id(model_name)
        coldata_dir = os.path.join(self.coldata_dir, model_id)
        if os.path.exists(coldata_dir):
            for fname in os.listdir(coldata_dir):
                try:
                    m = ColocatedData.get_meta_from_filename(fname)
                    match = (m['data_source'][0] == obs_name and
                             m['data_source'][1] == model_name)
                    if match:
                        files.append(os.path.join(coldata_dir, fname))
                except:
                    const.print_log.warning('Invalid file {} in coldata dir'
                                            .format(fname))

        if len(files) == 0:
            msg = ('Could not find any colocated data files for model {}, '
                   'obs {}'
                   .format(model_name, obs_name))
            if self.colocation_settings['raise_exceptions']:
                raise IOError(msg)
            else:
                self._log.warning(msg)
        return files
    
    def make_json_files(self, model_name, obs_name, var_name=None,
                        colocator=None):
        """Convert colocated data file(s) in model data directory into json
        
        Parameters
        ----------
        model_name : str
            name of model run
        obs_name : str
            name of observation network
        var_name : str, optional
            name of variable supposed to be analysed. If None, then all
            variables available for observation network are used (defined in 
            :attr:`obs_config` for each entry). Defaults to None.
        colocator : Colocator, optional
            instance of colocator class containing information about which
            files to process (e.g. created in :func:`run_evaluation`). If None,
            than all colocated data files are processed that are located in the
            corresponding colocation data directory and that match the input 
            specs.
        
        Returns
        -------
        list
            list of colocated data files that were converted
        """
        converted = []
        
        files = self.find_coldata_files(model_name, obs_name, var_name)
        for file in files:
            fname = os.path.basename(file)
            if not fname in colocator.file_status:
                const.print_log.info('Skipping computation of json files from '
                                     'colocated data file {}. This file is not '
                                     'part of this experiment (obs config)'
                                     .format(fname, self.obs_config[obs_name]))
                continue
            if colocator.file_status[fname] == 'skipped':
                const.print_log.info('Recomputing json files for existing '
                                     'colocated data file')
            elif not colocator.file_status[fname] == 'saved':
                const.print_log.info('Skipping computation of json files from '
                                     'colocated data file {}. Colocator object '
                                     'has marked this file as {} (need either '
                                     'status skipped or saved)'
                                     .format(fname, colocator.file_status[fname]))
                continue
            const.print_log.info('Processing file {}'.format(file))
            d = ColocatedData(file)
            self.compute_json_files_from_colocateddata(d, obs_name, model_name)
            converted.append(file)
        return converted
    
    def delete_all_colocateddata_files(self, model_name, obs_name):
        #model_id = self.get_model_id(model_name)
        #obs_id = self.get_obs_id(obs_name)
        obs_vars = self.obs_config[obs_name]['obs_vars']
    
        for obs_var in obs_vars:
            files = glob.glob('{}/{}/{}*REF-{}*.nc'
                              .format(self.coldata_dir, model_name, obs_var, 
                                      obs_name))
            for file in files:
                const.print_log.info('DELETING FILE: {}'.format(file))
                os.remove(file)
            
    def run_colocation(self, model_name, obs_name, var_name=None):
        """Run colocation for model / obs combination
        
        Parameters
        ----------
        model_name : str or list, optional
            Name or pattern specifying model that is supposed to be analysed.
            Can also be a list of names or patterns to specify multiple models.
            If None (default), then all models are run that are part of this
            experiment.
        obs_name : :obj:`str`, or :obj:`list`, optional
            Like :attr:`model_name`, but for specification(s) of observations
            that are supposed to be used. If None (default) all observations 
            are used.
        var_name : str, optional
            name of variable supposed to be analysed. If None, then all
            variables available for observation network are used (defined in 
            :attr:`obs_config` for each entry). Defaults to None.
            
        Returns
        -------
        Colocator
            instance of colocation class
        """
        if self.colocation_settings['reanalyse_existing']:
            self.delete_all_colocateddata_files(model_name, obs_name)
            
        col = Colocator()
        col.update(**self.colocation_settings)
        
        if not model_name in self.model_config:
            raise KeyError('No such model name in configuration: {}. Available '
                           'names: {}'.format(model_name, 
                                              self.all_model_names))
        elif not obs_name in self.obs_config:
            raise KeyError('No such obs name in configuration: {}. Available '
                           'names: {}'.format(obs_name, self.all_obs_names))
            
        obs_cfg = self.obs_config[obs_name]
        if obs_cfg['obs_vert_type'] in self.VERT_SCHEMES and not 'vert_scheme' in obs_cfg:
            obs_cfg['vert_scheme'] = self.VERT_SCHEMES[obs_cfg['obs_vert_type']]
        col.update(**obs_cfg)
        col.update(**self.get_model_config(model_name))
        
        const.print_log.info('Running colocation of {} against {}'
                             .format(model_name, obs_name))
        # for specifying the model and obs names in the colocated data file
        col.model_name = model_name
        col.obs_name = obs_name
        
        # run colocation
        col.run(var_name)
        
        return col
    
    def get_model_config(self, model_name):
        """Get model configuration
        
        Since the configuration files for experiments are in json format, they
        do not allow the storage of executable custom methods for model data
        reading. Instead, these can be specified in a python module that may
        be specified via :attr:`add_methods_file` and that contains a 
        dictionary `FUNS` that maps the method names with the callable methods.
        
        As a result, this means that, by default, custom read methods for 
        individual models in :attr:`model_config` do not contain the 
        callable methods but only the names. This method will take care of 
        handling this and will return a dictionary where potential custom 
        method strings have been converted to the corresponding callable 
        methods.
        
        Parameters
        ----------
        model_name : str
            name of model run
            
        Returns 
        -------
        dict
            Dictionary that specifies the model setup ready for the analysis
        """
        mcfg = self.model_config[model_name]
        outcfg = {}
        if not 'model_id' in mcfg:
            raise ValueError('Model configuration for {} is missing '
                             'specification of model_id '.format(model_name))
        for key, val in mcfg.items():
            
            if key != 'model_read_aux':
                outcfg[key] = val
            else:
                outcfg[key] = d = {}
                for var, rcfg in val.items():
                    d[var] = {}
                    d[var]['vars_required'] = rcfg['vars_required']
                    fun_str = rcfg['fun']
                    if not isinstance(fun_str, str):
                        raise Exception('Unexpected error. Custom method defs. '
                                        'need to be strings, got {}'.format(fun_str))
                    d[var]['fun'] = self.get_custom_read_method_model(fun_str)
        return outcfg
            
    def find_model_matches(self, name_or_pattern):
        """Find model names that match input search pattern(s)
        
        Parameters
        ----------
        name_or_pattern : :obj:`str`, or :obj:`list`
            Name or pattern specifying model search string. Can also be a list 
            of names or patterns to search for multiple models.
            
        Returns
        -------
        list
            list of model names (i.e. keys of :attr:`model_config`) that match 
            the input search string(s) or pattern(s)
            
        Raises
        ------
        KeyError
            if no matches can be found
        """
        
        
        if isinstance(name_or_pattern, str):
            name_or_pattern = [name_or_pattern]
        from fnmatch import fnmatch
        matches = []
        for search_pattern in name_or_pattern:
            for mname in self.model_config:
                if fnmatch(mname, search_pattern) and not mname in matches:
                    matches.append(mname)
        if len(matches) == 0:
            raise KeyError('No models could be found that match input {}'
                           .format(name_or_pattern))
        return matches
    
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
            raise KeyError('No observations could be found that match input {}'
                           .format(name_or_pattern))
        return matches
    
    def run_evaluation(self, model_name=None, obs_name=None, var_name=None, 
                       update_interface=True, 
                       reanalyse_existing=None, raise_exceptions=None, 
                       clear_existing_json=None, only_colocation=None):
        """Create colocated data and json files for model / obs combination
        
        Parameters
        ----------
        model_name : str or list, optional
            Name or pattern specifying model that is supposed to be analysed.
            Can also be a list of names or patterns to specify multiple models.
            If None (default), then all models are run that are part of this
            experiment.
        obs_name : :obj:`str`, or :obj:`list`, optional
            Like :attr:`model_name`, but for specification(s) of observations
            that are supposed to be used. If None (default) all observations 
            are used.
        var_name : str, optional
            name of variable supposed to be analysed. If None, then all
            variables available for observation network are used (defined in 
            :attr:`obs_config` for each entry). Defaults to None.
        update_interface : bool
            if true, relevant json files that determine what is displayed 
            online are updated after the run, including the the menu.json file 
            and also, the model info table (minfo.json) file is created and
            saved in :attr:`exp_dir`.
        reanalyse_existing : Bool, optional
            if True, existing colocated data files are ignored. If None, the
            class default will be used (defined in config file)
        raise_exceptions : Bool, optional
            if True, exceptions during colocation will be raised if they occur 
            (for debugging). If None, the class default will be used (defined 
            in config file)
        clear_existing_json : Bool, optional
            if True, existing json files for model / obs combination will be 
            deleted before rerun. If None, the
            class default will be used (defined in config file)
        only_colocation : Bool, optional
            if True, only colocation will be performed and no json files will
            be created. If None, the class default will be used (defined in 
            config file)
            
        Returns
        -------
        list
            list containing all colocated data objects that have been converted
            to json files.
        """
        res = None
        if reanalyse_existing is not None:
            self.colocation_settings['reanalyse_existing'] = reanalyse_existing
        if raise_exceptions is not None:
            self.colocation_settings['raise_exceptions'] = raise_exceptions
        if clear_existing_json is not None:
            self.clear_existing_json = clear_existing_json
        if only_colocation is not None:
            self.only_colocation = only_colocation
        
        if self.clear_existing_json:
            self.clean_json_files()
            
        if model_name is None:
            model_list = list(self.model_config)
        else:
            model_list = self.find_model_matches(model_name)
        
        if obs_name is None:
            obs_list = list(self.obs_config)
        else:
            obs_list = self.find_obs_matches(obs_name)
        self._log.info(self.info_string_evalrun(obs_list, model_list))
        
        self._update_custom_read_methods()
        
        for obs_name in obs_list:
            if obs_name in self.obs_ignore:
                self._log.info('Skipping observation {}'.format(obs_name))
                continue
            for model_name in model_list:
                if model_name in self.model_ignore:
                    self._log.info('Skipping model {}'.format(model_name))
                    continue
            
                col = self.run_colocation(model_name, obs_name, var_name)
                if only_colocation:
                    self._log.info('Skipping computation of json files for {}'
                                   '/{}'.format(obs_name, model_name))
                    continue
                res = self.make_json_files(model_name, obs_name, var_name,
                                           colocator=col)
        
        if update_interface:
            #self.clean_json_files()
            self.update_interface()

        return res            
        
    def info_string_evalrun(self, obs_list, model_list):
        """Short information string that summarises settings for evaluation run
        
        Parameters
        ----------
        obs_list
            list of observation names supposed to be processed
        model_list : list
            list of model names supposed to be processed
            
        Returns
        -------
        str
            info string
        """
        s = ('\nRunning analysis:\n'
             'Obs. names: {}\n'
             'Model names: {}\n'
             'Remove outliers: {}\n'
             'Harmonise units: {}'
             .format(obs_list, model_list, self['remove_outliers'], 
                     self['harmonise_units']))
        for k, i in self._OPTS_NAMES_OUTPUT.items():
            s += '\n{}: {}'.format(i, self[k]) 
        s += '\n'
        return s
    
    def check_read_model(self, model_name, var_name, **kwargs):
        if not model_name in self.model_config:
            raise ValueError('No such model available {}'.format(model_name))
        mcfg = self.get_model_config(model_name)
        
        from pyaerocom.io import ReadGridded
        r = ReadGridded(mcfg['model_id'])
        try:
            var_name = mcfg['model_use_vars'][var_name]
        except:
            pass
        
        if 'model_read_aux' in mcfg and var_name in mcfg['model_read_aux']:
            aa = mcfg['model_read_aux'][var_name]
            
        
            r.add_aux_compute(var_name, vars_required=aa['vars_required'], 
                              fun=aa['fun'])
        return r.read_var(var_name, **kwargs)
        
    def _info_from_map_file(self, filename):
        f = filename
        obs_info = f.split('OBS-')[1].split('_MOD')[0].split('_')
        obs_name, obs_var = obs_info[0].split(':')
        vert_code = obs_info[1]
        mod_name, mod_var =  f.split('MOD-')[1].split('.json')[0].split(':')
        return (obs_name, obs_var, vert_code, mod_name, mod_var)
    
    def get_web_overview_table(self):
        """Computes overview table based on existing map files"""
        tab = []
        from pandas import DataFrame
        for f in self.all_map_files:
            if f.endswith('.json') and f.startswith('OBS'):
                (obs_name, obs_var, 
                 vert_code, 
                 mod_name, mod_var) = self._info_from_map_file(f)
                if mod_name in self.model_ignore:
                    continue
                elif not mod_name in self.model_config:
                    const.print_log.warning('Found outdated json map file: {}'
                                            'Will be ignored'.format(f))
                    continue
                elif not obs_name in self.obs_config:
                    const.print_log.warning('Found outdated json map file: {}'
                                            'Will be ignored'.format(f))
                    continue
                mcfg = self.model_config[mod_name]
                if 'model_use_vars' in mcfg and obs_var in mcfg['model_use_vars']:
                    if mcfg['model_use_vars'][obs_var] != mod_var:
                        const.print_log.warning('Ignoring map file {}'
                                                .format(f))
                        continue
                tab.append([obs_var, obs_name, vert_code, mod_name, mod_var])
        return DataFrame(tab, columns=['Var' , 'Obs', 'vert',
                                       'Model', 'Model var'])
    
    def get_obsvar_name_and_type(self, obs_var):
        """Get menu name and type of observation variable
        
        Parameters
        ----------
        obs_var : str
            Name of observation variable
        
        Returns
        -------
        str
            menu name of this variable
        str
            menu category of this variable
        """
        
        try:
            name, tp, cat = self.var_mapping[obs_var]
        except:
            name, tp, cat = obs_var, 'UNDEFINED', 'UNDEFINED'
            self._log.warning('Missing menu name definition for var {}. '
                              'Using variable name'.format(obs_var))
        return (name, tp, cat)
    
    def update_interface(self, **opts):
        """Update web interface
        
        Things done here:
            
            - Update menu file
            - Make web info table json (tab informations in interface)
            - update and order heatmap file
        """
        self.update_menu(**opts)
        self.make_info_table_web()
        self.update_heatmap_json()
        
    def update_menu(self, **opts):
        """Updates menu.json based on existing map json files"""
        update_menu_evaluation_iface(self, **opts)
        
        
    def make_info_table_web(self):
        """Make and safe table with detailed infos about processed data files
        
        The table is stored in as file minfo.json in directory :attr:`exp_dir`.
        """
        table = make_info_table_evaluation_iface(self)
        outname = os.path.join(self.exp_dir, 'minfo.json')       
        with open(outname, 'w+') as f:
            f.write(simplejson.dumps(table, indent=2))
        return table
    
    def _obs_config_asdict(self):
        d = {}
        for k, cfg in self.obs_config.items():
            as_dict = {}
            as_dict.update(**cfg)
            d[k] = as_dict
        return d
    
    def _model_config_asdict(self):
        d = {}
        for k, cfg in self.model_config.items():
            as_dict = {}
            as_dict.update(**cfg)
            d[k] = as_dict
        return d        
    
    def delete_experiment_data(self, base_dir=None, proj_id=None, exp_id=None):
        """Delete all data associated with a certain experiment
        
        Parameters
        ----------
        base_dir : str, optional
            basic output direcory (containg subdirs of all projects)
        proj_name : str, optional
            name of project, if None, then this project is used
        exp_name : str, optional
            name experiment, if None, then this project is used
        """
        from pyaerocom.web.helpers import delete_experiment_data_evaluation_iface
        if proj_id is None:
            proj_id = self.proj_id
        if exp_id is None:
            exp_id = self.exp_id
        if base_dir is None:
            base_dir = self.out_basedir
        delete_experiment_data_evaluation_iface(base_dir, proj_id, exp_id)
        self.update_interface()
        
    def clean_json_files(self, update_interface=False):
        """Checks all existing json files and removes outdated data
        
        This may be relevant when updating a model name or similar.
        """
        
        for file in self.all_map_files:
            (obs_name, obs_var, 
             vert_code, 
             mod_name, mod_var) = self._info_from_map_file(file)
            remove=False
            obs_vars = self._get_valid_obs_vars(obs_name)
        
            if not (obs_name in self.obs_config and
                    mod_name in self.model_config and
                    obs_var in obs_vars):
                remove = True
            
            mcfg = self.model_config[mod_name]
            if 'model_use_vars' in mcfg and obs_var in mcfg['model_use_vars']:
                if not mod_var == mcfg['model_use_vars'][obs_var]:
                    remove=True
                    
            if remove:
                const.print_log.info('Removing outdated map file: {}'.format(file))
                os.remove(os.path.join(self.out_dirs['map'], file))
        for fp in glob.glob('{}/*.json'.format(self.out_dirs['ts'])):
            self._check_clean_ts_file(fp)
        if update_interface:
            self.update_interface()
    
    def _get_valid_obs_vars(self, obs_name):
        if obs_name in self._valid_obs_vars:
            return self._valid_obs_vars[obs_name]
    
        obs_vars = self.obs_config[obs_name]['obs_vars']
        add = []
        for mname, mcfg in self.model_config.items():
            if 'model_add_vars' in mcfg:
                for ovar, mvar in mcfg['model_add_vars'].items():
                    if ovar in obs_vars and not mvar in add:
                        add.append(mvar)
        obs_vars.extend(add)
        self._valid_obs_vars[obs_name]  = obs_vars
        return obs_vars
    
    def _check_clean_ts_file(self, fp):
        spl = os.path.basename(fp).split('OBS-')[-1].split(':')
        obs_name = spl[0]
        obs_var = spl[1].split('_')[0]
        if not (obs_name in self.obs_config and 
                obs_var in self._get_valid_obs_vars(obs_name)):
            const.print_log.info('Removing outdated ts file: {}'.format(fp))
            os.remove(fp)
            return
        try:
            data = read_json(fp)
        except:
            const.print_log.exception('FATAL: detected corrupt json file: {}. '
                                      'Removing file...'.format(fp))
            os.remove(fp)
            return
        if all([x in self.model_config for x in list(data.keys())]):
            return
        data_new = {}
        for mod_name in data.keys():
            if not mod_name in self.model_config:
                const.print_log.info('Removing model {} from {}'
                                .format(mod_name, os.path.basename(fp)))
                continue
            
            data_new[mod_name] = data[mod_name]
        
        write_json(data_new, fp)
            
                
                
        
    def to_dict(self):
        """Convert configuration to dictionary"""
        d = {}
        for key, val in self.__dict__.items():
            if key in self.JSON_CFG_IGNORE:
                continue
            elif isinstance(val, dict):
                if key == 'model_config':
                    sub = self._model_config_asdict()
                elif key == 'obs_config':
                    sub = self._obs_config_asdict()
                else:
                    sub = {}
                    for k, v in val.items():
                        if v is not None:
                            sub[k] = v
                d[key] = sub
            else:
                d[key] = val
        return d
    
    def to_json(self, output_dir):
        """Convert configuration to json ini file"""
        d = self.to_dict()
        out_name = 'cfg_{}_{}.json'.format(self.proj_id, self.exp_id)
        
        save_dict_json(d, os.path.join(output_dir, out_name), indent=3)
        return d
        
    def load_config(self, proj_id, exp_id, config_dir=None):
        """Load configuration json file"""
        if config_dir is None:
            if self.config_dir is not None:
                config_dir = self.config_dir
            else:
                config_dir = '.'
        files = glob.glob('{}/cfg_{}_{}.json'.format(config_dir, proj_id, 
                          exp_id))
        if len(files) == 0:
            raise ValueError('No config file could be found in {} for '
                             'project {} and experiment {}'.format(config_dir, 
                              proj_id, exp_id))
        self.from_json(files[0])
        
    def from_json(self, config_file):
        """Load configuration from json config file"""
        with open(config_file, 'r') as f:
            current = simplejson.load(f)
        self.update(**current)
        
    def __str__(self):
        indent = 2
        _indent_str = indent*' '
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}".format(head, len(head)*"-")
        s += ('\nProject ID: {}'
              '\nEperiment ID: {}'
              '\nExperiment name: {}'
              .format(self.proj_id, self.exp_id, self.exp_name))
        s += '\ncolocation_settings: (will be updated for each run from model_config and obs_config entry)'
        for k, v in self.colocation_settings.items():
            s += '\n{}{}: {}'.format(_indent_str, k, v)
        s += '\n\nobs_config:'
        for k, v in self.obs_config.items():
            s += '\n\n{}{}:'.format(_indent_str, k)
            s = dict_to_str(v, s, indent=indent+2)
        s += '\n\nmodel_config:'
        for k, v in self.model_config.items():
            s += '\n\n{}{}:'.format(_indent_str,  k)
            s = dict_to_str(v, s, indent=indent+2)
    
        return s
    
if __name__ == '__main__':    
    cfg_dir = '/home/jonasg/github/aerocom_evaluation/data_new/config_files/'
    stp = AerocomEvaluation('aerocom', 'PIII-optics', config_dir=cfg_dir)
    #stp.make_info_table_web()
    
    stp.make_regions_json()