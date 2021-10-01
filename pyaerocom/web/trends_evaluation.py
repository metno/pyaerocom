#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToDos
-----

- Review outlier removal
"""
from collections import OrderedDict as od
import datetime
from fnmatch import fnmatch
import numpy as np
import os, glob
import pandas as pd
from scipy.stats import kendalltau
from scipy.stats.mstats import theilslopes
import simplejson

from pyaerocom import const, __version__
from pyaerocom._lowlevel_helpers import (check_dirs_exist, dict_to_str)
from pyaerocom.region import Region
from pyaerocom.helpers import isnumeric
from pyaerocom.trends_helpers import (_init_trends_result_dict,
                                      _compute_trend_error,
                                      _get_season, _mid_season,
                                      _find_area, _years_from_periodstr)
from pyaerocom.tstype import TsType
from pyaerocom.io.helpers import save_dict_json
from pyaerocom.io import ReadGridded
from pyaerocom.web.var_groups import var_groups
from pyaerocom.web.helpers import (ObsConfigEval, ModelConfigEval,
                                   read_json)
from pyaerocom.web.helpers_trends_iface import (update_menu_trends_iface,
                                                get_all_config_files_trends_iface)

from pyaerocom.exceptions import DataCoverageError, TemporalResolutionError

const.print_log.warning(DeprecationWarning(
    'Module pyaerocom/web/trends_evaluation.py will be removed as of '
    'release 0.12.0 which will incorporate trends computation in AeroVal '
    'interface (via AerocomEvaluation class)'))

class TrendsEvaluation(object):
    """High-level analysis class to compute json files for trends interface

    Web: https://aerocom-trends.met.no/

    Attributes
    ----------

    name : str
        name of this configuration setup
    config_dir : str, optional
        directory containing available configuration files
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
    model_config : dict
        dictionary specifying models or satellites to be used for colocation
        with the observations.
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
    obs_order_menu_cfg : bool
        where applicable and if True, then order observations with common
        variables in the menu in the same order as they appear in
        :attr:`obs_config`. If False, order alphabetically.
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

    Parameters
    ----------
    config_file : str, optional
        if provided and valid, then configuration is loaded from this file
    **settings
        configuration settings
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
    #: ToDo: this should not be needed and the web tools should use the same
    #: conventions as pyaerocom
    KEYMAP = od(var_name        = 'var_name',
                station_name    = 'station',
                latitude        = 'lat',
                longitude       = 'lon',
                altitude        = 'alt',
                data_id         = 'data_id',
                dataset_name    = 'dataset',
                data_product    = 'product',
                framework       = 'framework',
                data_version    = 'data_version',
                data_level      = 'data_level',
                website         = 'website',
                instrument_name = 'instrument',
                ts_type_src     = 'freq_src',
                ts_type         = 'freq',
                PI              = 'PI',
                wavelength      = 'wavelength',
                units           = 'unit',
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
            #'CHINA': 'China',
            'AUSTRALIA': 'Australia',
            'NAFRICA': 'N-Africa',
            'SAFRICA': 'S-Africa',
            #'INDIA': 'India',
            'WORLD': 'World'
    }
    SEASONS = ['spring','summer','autumn','winter','all']

    JSON_CFG_IGNORE = ['regions', '_log', 'out_dirs']

    GRIDDED_TS_TYPE = 'monthly'
    def __init__(self, config_file=None, **settings):

        self.name = None
        self._log = const.print_log

        self.config_dir = None
        self.out_basedir = None
        self.out_dirs = {}

        self.obs_config = {}
        self.obs_ignore = []

        self.model_config = {}

        self.periods = []
        self.regions = {}
        self._add_regions = {}

        self.var_mapping = {}
        self.var_order_menu = []

        self.obs_order_menu_cfg = True

        # options
        self.slope_alpha = 0.68
        self.min_dim = 5
        self.avg_how = 'mean'

        self.delete_outdated = True
        self.clear_existing_json = True
        self.write_logfiles = True
        self.logdir = None

        # initialise
        if config_file is not None: # user provided configuration file
            self.from_json(config_file)
        else: # user maybe provided full config via dict, or only name
            self.update(**settings)

    def __setitem__(self, key, val):

        if key == 'obs_config':
            self._set_obsconfig(val)
        elif key == 'model_config':
            self._set_modelconfig(val)
        elif isinstance(key, str) and isinstance(val, dict):
            if 'obs_id' in val:
                if key in self.obs_config:
                    self._log.warning(
                        f'Obs config for key {key} already exists and '
                        f'will be overwritten')
                self.obs_config[key] = ObsConfigEval(**val)
            elif 'model_id' in val:
                if not 'mtype' in val:
                    raise KeyError('Need key "mtype" in specfication of model {}'
                                   .format(key))
                if key in self.model_config:
                    self._log.warning(f'Model config for key {key} already '
                                      f'exists and will be overwritten')
                self.model_config[key] = ModelConfigEval(**val)
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
                s = dict_to_str(val, s)
            else:
                s += '\n{}: {}'.format(key, val)
        s += obs_cfg
        return s

    def get_config_files(self, config_dir):
        """Get all available configuration files

        Parameters
        ----------
        config_dir : str
            directory containing configuration files

        Returns
        -------
        dict
            dictionary containing all available configuration files

        Raises
        ------
        FileNotFoundError
            if no config files could be found in input directory
        """
        files = get_all_config_files_trends_iface(config_dir)
        if len(files) > 0:
            return files
        raise FileNotFoundError('Could not find any configuration files')

    @property
    def menu_file(self):
        """json file containing region specifications"""
        return os.path.join(self.out_basedir, 'menu.json')

    @property
    def all_obs_names(self):
        """List of all obs names"""
        return list(self.obs_config)

    @property
    def all_map_files(self):
        """List of all existing map files"""
        return sorted([f for f in os.listdir(self.out_dirs['map'])
                       if f.endswith('.json') and f.startswith('OBS-')])

    def check_config(self):
        """Check if there are any problems in the configuration

        Returns
        -------
        bool
            True if all is good, False, if configuration settings are missing

        Raises
        ------
        ValueError
            if one of the provided period strings is invalid
        AttributeError
            if model configuration is missing
        AssertionError
            if there is a problem with EBAS default configuration
        """
        if len(self.periods) == 0:
            return False
        elif len(self.obs_config) == 0:
            return False
        for p in self.periods:
            try:
                start, stop = _years_from_periodstr(p)
            except Exception:
                raise ValueError('Invalid input for period: {}. '
                                 'Need string in format "2010-2019"'.format(p))

        for run, cfg in self.obs_config.items():
            if '_' in run:
                raise AttributeError('Invalid name: {} (no underscores allowed)'
                                     .format(run))
            if cfg.obs_id == 'EBASMC':
                check_ebas_default()
            if 'models' in cfg:
                for model in cfg['models']:
                    if not model in self.model_config:
                        raise AttributeError('No such model with name {} '
                                             'available in model_config...'
                                             .format(model))
        return True

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
            list of model names that available in :attr:`model_config`.
        vars_to_retrieve : list
            list of variable names that are supposed to be checked in models

        Returns
        -------
        dict
            keys are models and values are lists of variables that are
            available in each of these models
        """
        maccess = {}
        for model_name in models:
            if not model_name in self.model_config:
                raise AttributeError('No model {} available in model_config'
                                     .format(model_name))
            mcfg = self.model_config[model_name]
            model_id = mcfg['model_id']
            try:
                r = ReadGridded(model_id)
                vars_avail = {}
                for obs_var in vars_to_retrieve:
                    try:
                        mod_var = mcfg['model_use_vars'][obs_var]
                    except KeyError:
                        mod_var = obs_var
                    if mod_var in r.vars_provided:
                        vars_avail[obs_var] = mod_var
                if len(vars_avail) > 0:
                    maccess[model_name] = dict(model_id=model_id,
                                               vars_avail=vars_avail)
            except Exception:
                self._log.warning('Model {} does not provide any of the req. '
                                  'variables {}'.format(model_name,
                                                        vars_to_retrieve))

        return maccess

    def read_ungridded_obsdata(self, obs_name, vars_to_read=None):
        """Load obsdata into instance of :class:`pyaerocom.UngriddedData`

        Wrapper
        Parameters
        ----------
        obs_name : str
            Name of observation network
        vars_to_read
            str or list / tuple of strings specifying AEROCOM variables that are
            supposed to be imported

        Returns
        -------
        UngriddedData
            loaded data object
        """
        from pyaerocom import Colocator
        col = Colocator()
        col.update(**self.obs_config[obs_name])
        data = col.read_ungridded(vars_to_read)
        return data

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
        if self.delete_outdated:
            self.delete_outdated_json_files()

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

        self.make_regions_json()
        self.to_json()
        if update_menu:
            self.update_menu()

        return result

    def get_var_groups(self, obs_name):
        """Split list of variables of obs into variable sublists

        Splitting is done based on predefined var groups, defined in
        :mod:`var_groups`, where available.

        Parameters
        ----------
        obs_id : str
            Name of obsdata source (key of :attr:`obs_config`)

        Returns
        -------
        list
            list containing sublists for different variable groups
        """
        obs_id = self.obs_config[obs_name]['obs_id']
        vars_to_retrieve = self.obs_config[obs_name]['obs_vars']
        if not obs_id in var_groups:
            return [vars_to_retrieve]
        result = []
        groups =  var_groups[obs_id]
        added = []
        for group in groups:
            subset = list(np.intersect1d(vars_to_retrieve, group))
            if any([x in added for x in subset]):
                raise ValueError('Fatal: one variable appears to exist in 2 groups')
            added.extend(subset)
            if len(subset) > 0:
                result.append(subset)
        rest = [x for x in vars_to_retrieve if not x in added]
        if len(rest) > 0:
            result.append(rest)
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

        self._log.info('Running {} (NETWORK {})'.format(obs_name, obs_name))

        constraints = config['read_opts_ungridded']
        if constraints is None:
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

        var_lists = self.get_var_groups(obs_name)
        for vars_to_retrieve in var_lists:
            ungridded_data = self.read_ungridded_obsdata(obs_name,
                                                         vars_to_retrieve)

            if 'obs_filters' in config:
                filters=config['obs_filters']
                ungridded_data = ungridded_data.apply_filters(
                    var_outlier_ranges=min_max,
                    **filters)

            if config['obs_vert_type']=='Profile':
                files_created = self._run_single_3d(ungridded_data=ungridded_data,
                                                    vars_to_retrieve=vars_to_retrieve,
                                                    min_dim=min_dim,
                                                    models=models,
                                                    name=obs_name,
                                                    files_created=files_created,
                                                    err_log=err_log)
            else:
                files_created = self._run_single_2d(ungridded_data=ungridded_data,
                                                    vars_to_retrieve=vars_to_retrieve,
                                                    min_dim=min_dim,
                                                    models=models,
                                                    name=obs_name,
                                                    vert_which=config['obs_vert_type'],
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

    def update_menu(self):
        """Update menu.json based on available runs"""
        update_menu_trends_iface(self)

    @property
    def regions_file(self):
        """File path of regions.json file"""
        return os.path.join(self.out_basedir, 'regions.json')

    def make_regions_json(self):
        """Make regions.json file for web interface"""
        regs = {}
        for regname, reg in self.regions.items():

            regs[regname] = r = {}

            latr = reg.lat_range
            lonr = reg.lon_range
            r['minLat'] = latr[0]
            r['maxLat'] = latr[1]
            r['minLon'] = lonr[0]
            r['maxLon'] = lonr[1]
        save_dict_json(regs, self.regions_file)
        return regs

    def update(self, **settings):
        """Update current setup"""
        for k, v in settings.items():
            self[k] = v
        if self.out_basedir is not None:
            self._init_dirs()
        self._init_regions()
        if not self.check_config():
            self._log.info('Setup is incomplete')

    def search_config_file(self, autoload=True):
        """Try to find valid configuration file"""
        if self.name is None:
            raise AttributeError('Attr. name needs to be specified')
        name = self.name
        file = None
        if self.config_dir is not None:
            try:
                files = self.get_config_files(self.config_dir)
                if not name in files:
                    raise FileNotFoundError('No config {} in {}'.format(name,
                                            self.config_dir))
                file = files[name]
            except Exception:
                pass
        else:
            try:
                files = self.get_config_files('.')
                if not name in files:
                    raise FileNotFoundError('No config {} in current '
                                            'directory'.format(name))
                file = files[name]
            except Exception:
                pass
        if file is None:
            raise FileNotFoundError('Could not find a valid configuration file')
        if autoload:
            self._log.info('Importing configuration from {}'.format(file))
            self.from_json(file)
        return file

    def from_json(self, config_file):
        """Load configuration from json config file"""

        current = read_json(config_file)
        self.update(**current)

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

    def to_json(self, output_dir=None, filename=None):
        """Convert configuration to json ini file"""
        if filename is None:
            if self.name is None:
                raise ValueError('Attr. "name" needs to be specified')
            filename = 'cfg_{}.json'.format(self.name)
        if not filename.startswith('cfg_'):
            raise ValueError('json configuration file MUST start with cfg_')
        elif not filename.endswith('.json'):
            filename.split('.')[0] += '.json'
        if output_dir is None:
            output_dir = self.out_basedir
        d = self.to_dict()

        fp = os.path.join(output_dir, filename)
        save_dict_json(d, fp, indent=3)
        return fp

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
                except Exception:
                    print('Failed to check for existing runs for ID {}'.format(run))
            print()

    def _get_meta_from_json(self, f):
        """Extract meta information from json file

        Parameters
        ----------
        f : str
            map or ts json file

        Returns
        -------
        str
            obs_name
        str
            obs_var
        str
            vert_code
        str
            mod_name
        str
            mod_var
        """

        obs_info = f.split('OBS-')[1].split('_MOD')[0].split('_')
        obs_name, obs_var = obs_info[0].split(':')
        vert_code = obs_info[1]
        mod_name, mod_var =  f.split('MOD-')[1].split('.json')[0].split(':')

        return (obs_name, obs_var, vert_code, mod_name, mod_var)

    def get_web_overview_table(self):
        """Computes overview table based on existing map files

        Note
        ----
        Ignores map files that belong to runs which are not specified in this
        configuration.
        """
        tab = []
        header = ['obs_name' , 'obs_id', 'obs_var',
                  'vert', 'mod_name', 'mod_id', 'mod_var', 'mod_type',
                  'periods']
        periods = self.get_periods_from_map_files()
        for f in self.all_map_files:
            (obs_name, obs_var,
             vert_code,
             mod_name, mod_var) = self._get_meta_from_json(f)

            if not obs_name in self.obs_config:
                continue

            obs_id = self.obs_config[obs_name]['obs_id']

            mod_id, mod_type = None, None
            if mod_name != 'None':
                mod_id = self.model_config[mod_name]['model_id']
                mod_type = self.model_config[mod_name]['mtype']
            else:
                mod_var = None

            #os.path.exists(t.out_dirs['map'] + '/' + t.all_map_files[0])
            tab.append([obs_name, obs_id, obs_var, vert_code,
                        mod_name, mod_id, mod_var, mod_type, periods[f]])

        return pd.DataFrame(tab, columns=header)

    def delete_outdated_json_files(self):
        """Delete all json files that are not part of this configuration"""
        for f in self.all_map_files:
            (obs_name, obs_var,
             vert_code,
             mod_name, mod_var) = self._get_meta_from_json(f)

            if not obs_name in self.obs_config:
                ts_files = glob.glob('{}/OBS-{}:{}_{}_MOD-{}:{}*.json'
                                     .format(self.out_dirs['ts'],
                                             obs_name, obs_var, vert_code,
                                             mod_name, mod_var))
                self._log.info('REMOVING {} files in ts directory for {} ({})'
                               .format(len(ts_files), obs_name, obs_var))
                for file in ts_files:
                    os.remove(file)

                self._log.info('REMOVING map file {}'.format(f))
                os.remove(os.path.join(self.out_dirs['map'], f))

    def get_periods_from_map_files(self):
        """Get data periods covered for each of the map files

        Returns
        -------
        dict
            keys are filenames of map files, values are list of periods
            covered
        """
        res = {}
        for fname in self.all_map_files:
            fpath = os.path.join(self.out_dirs['map'], fname)
            current = read_json(fpath)
            res[fname] = list(current[0]['all'].keys())
        return res

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
        except Exception:
            name, tp, cat = obs_var, 'UNDEFINED', 'UNDEFINED'
            self._log.warning('Missing menu name definition for var {}. '
                              'Using variable name'.format(obs_var))
        return (name, tp, cat)

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
                    os.remove(os.path.join(d, f))

    def _init_regions(self):
        """Initiate regions to assign lat / lon coordinates"""
        regs = {}
        for reg_id, reg_name in self.DEFAULT_REGIONS.items():
            regs[reg_name] = Region(reg_id)
        for reg_name, info in self._add_regions.items():
            try:
                regs[reg_name] = Region(reg_name,
                                        lat_range=info['lat_range'],
                                        lon_range=info['lon_range'])
            except Exception:
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

    def _set_obsconfig(self, val):
        cfg = {}
        for k, v in val.items():
            cfg[k] = ObsConfigEval(**v)
        self.obs_config = cfg

    def _set_modelconfig(self, val):
        cfg = {}
        for k, v in val.items():
            if not 'mtype' in v:
                raise KeyError('Need key "mtype" in specfication of model {}'
                               .format(k))
            cfg[k] = ModelConfigEval(**v)
        self.model_config = cfg

    def _save_map_json(self, map_data, obs_name, obs_var, vert_which,
                       mod_name=None, mod_var=None):
        map_outname = ('OBS-{}:{}_{}_MOD-{}:{}.json'.format(obs_name,
                                                            obs_var,
                                                            vert_which,
                                                            mod_name,
                                                            mod_var))

        outfile_map =  os.path.join(self.out_dirs['map'], map_outname)
        with open(outfile_map, 'w') as f:
            simplejson.dump(map_data, f, ignore_nan=True)
        return map_outname

    def _save_stat_json(self, trends_stat, obs_var, obs_name, vert_which,
                        mod_name=None, mod_var=None):
        """Save station json file

        Parameters
        ----------
        trends_stat

        var_name

        network_id

        vert_which

        """
        station_name = trends_stat['station']
        filename = ('OBS-{}:{}_{}_MOD-{}:{}_{}.json'.format(obs_name,
                                                            obs_var,
                                                            vert_which,
                                                            mod_name,
                                                            mod_var,
                                                            station_name))

        outfile = os.path.join(self.out_dirs['ts'], filename)
        try:
            df = pd.DataFrame(trends_stat)
            df.T.reset_index().to_json(outfile, double_precision=5)
        except ValueError as e:
            raise ValueError('FATAL: could not save station time-series trends '
                             'data to json. Reason: {}'.format(repr(e)))
        return filename

    def _remove_outliers(self, stat, var_name, min_max, logfile=None):
        """Remove outliers from StationData objects

        NOTE
        ----
        This method is deprecated since 26.6.2019, since outlier removal is now
        done already in UngriddedData object.
        """

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
        except Exception:
            pass

        if not len(stat[var_name]) == len0:
            raise Exception('Length mismatch of input and output arrays, developers, please check')
        elif all(np.isnan(stat[var_name])):
            raise DataCoverageError('No valid data remains after removing outliers')
        return stat

    def _station_to_timeseries(self, station, var_name, **alt_range):
        # load additional information about data source (if applicable)
        station.load_dataset_info()
        keymap = self.KEYMAP
        vardata = {}
        try:
            vardata['data_revision'] = station.data_revision
        except Exception:
            vardata['data_revision'] = None
        vardata['pyaerocom_version'] = __version__
        vardata['data_overlap'] = False
        vardata['var_name'] = var_name

        if var_name in station.overlap:
            vardata['data_overlap'] = True
        if var_name in station['var_info']:
            var_info =  station['var_info'][var_name]
        else:
            var_info = {}
        for k, v in keymap.items():
            val = None
            if v in ['var_name', 'data_overlap']:
                continue
            elif v in vardata:
                raise Exception('Key {} already exists... please debug...'
                                .format(k))
            try: # longitude, latitude and altitude are @property decorators in StationData
                val = station[k]
            except Exception:
                if k in var_info:
                    val = var_info[k]
            if isinstance(val, (list, tuple)):
                val = '; '.join([str(x) for x in val])
            vardata[v] = val

        # this is necessary, as e.g. altitude attribute of input station data
        # is not necessarily the station coordinate!
        for cname, cval in station.get_station_coords().items():
            if not isnumeric(cval):
                raise ValueError

            vardata[keymap[cname]] = np.float64(cval)
        # the actual sampling frequency
        tst = vardata['freq']
        try:
            freq = TsType(tst)
        except TemporalResolutionError:
            raise TemporalResolutionError(
                f'Skipping processing of {station.station_name} trend for var '
                f'{var_name} since temporal resolution {tst} is invalid')
        if vardata['wavelength'] is None:
            try:
                wvl = '{} nm'.format(const.VARS[var_name].wavelength_nm)
                vardata['wavelength'] = wvl
            except Exception:
                pass
        if tst=='native' or freq>=TsType('daily'):
            to_freq = 'daily'
            freq_name = 'dobs'
        elif freq >= TsType('monthly'):
            to_freq = 'monthly'
            freq_name = 'mobs'
        else:
            raise TemporalResolutionError(
                f'Skipping processing of {station.station_name} since temporal '
                f'resolution {freq} is too low (need at least monthly)')

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
    def _init_trends_result_dict(start_yr):
        return _init_trends_result_dict(start_yr)

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
        return _compute_trend_error(m, m_err, v0, v0_err)

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

        mobs['season'] = mobs.apply(lambda row: _get_season(row['month'],
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

                dates.append(_mid_season(seas, yr))

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
                start_yr, stop_yr = _years_from_periodstr(period)

                start_date = _mid_season(seas, start_yr)
                stop_date = _mid_season(seas, stop_yr)

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

        reg = _find_area(data['lat'], data['lon'],
                         regions_dict=self.DEFAULT_REGIONS)
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

    def _run_single_2d(self, ungridded_data, vars_to_retrieve,
                       min_dim, models, name, vert_which, files_created,
                       err_log):

        files_created = self._run_single_helper(ungridded_data=ungridded_data,
                                                vars_to_retrieve=vars_to_retrieve,
                                                name=name,
                                                vert_which=vert_which,
                                                files_created=files_created,
                                                min_dim=min_dim,
                                                models=models,
                                                err_log=err_log)
        return files_created

    def _run_single_3d(self, ungridded_data, vars_to_retrieve,
                       min_dim, models, name, files_created, err_log):
        if models is not None:
            raise NotImplementedError('Cannot yet colocate 3D observations '
                                      'with model data ...')
        for add_name, alt_range in self.VERT_LAYERS.items():
            files_created = self._run_single_helper(ungridded_data=ungridded_data,
                                                    vars_to_retrieve=vars_to_retrieve,
                                                    min_dim=min_dim,
                                                    models=models,
                                                    name=name,
                                                    vert_which=add_name,
                                                    files_created=files_created,
                                                    err_log=err_log,
                                                    altitude=alt_range)
        return files_created

    def _run_single_helper(self, ungridded_data, vars_to_retrieve,
                           name, vert_which, files_created, min_dim,
                           models, err_log=None, **alt_range):
        from pyaerocom.exceptions import DataCoverageError

        if isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]

        model_access = {}
        if models is not None and len(models) > 0:
            model_access = self.check_model_access(models,
                                                   vars_to_retrieve)

        for var in vars_to_retrieve:

            all_stats = ungridded_data.to_station_data_all(vars_to_convert=var,
                                                           by_station_name=True)
            stations = all_stats['stats']

            var_out = var
            stats_processed = []
            map_data = []

            stats_ok = []
            lats_ok = []
            lons_ok = []

            for stat in stations:
                stat_name = stat['station_name']
                print(var, stat['station_name'], name)
                if stat_name in stats_processed:
                    raise Exception('Unexpected Error, please check')

                try:
                    data_dict = self._station_to_timeseries(stat,
                                                            var_name=var,
                                                            **alt_range)
                    (trends_stat,
                     map_stat) = self._compute_trends_station(data_dict,
                                                              min_dim=min_dim)

                    fname = self._save_stat_json(trends_stat,
                                                 obs_var=var_out,
                                                 obs_name=name,
                                                 vert_which=vert_which)
                    files_created['ts'].append(fname)

                    stats_ok.append(stat_name)
                    lats_ok.append(stat['latitude'])
                    lons_ok.append(stat['longitude'])
                    if map_stat:
                        map_data.append(map_stat)

                except DataCoverageError as e:
                    msg = 'Error: {} {}, {}'.format(var, stat.station_name,repr(e))
                    print(msg)
                    if err_log:
                        err_log.write(msg + '\n')

            # Add to map only if at least one station is available
            if len(stats_ok) > 0:
                map_outname = self._save_map_json(map_data, obs_name=name,
                                                  obs_var=var_out,
                                                  vert_which=vert_which)
                files_created['map'].append(map_outname)

            for mod_name, mod_info in model_access.items():
                if not var in mod_info['vars_avail']:
                    continue
                mod_var=mod_info['vars_avail'][var]
                self._run_gridded(obs_name=name, obs_var=var,
                                  mod_name=mod_name, mod_var=mod_var,
                                  stat_lats=lats_ok,
                                  stat_lons=lons_ok,
                                  stat_names=stats_ok,
                                  min_dim=min_dim,
                                  vert_which=vert_which,
                                  files_created=files_created,
                                  err_log=err_log,
                                  **alt_range)
        return files_created

    def _run_gridded(self, obs_name, obs_var, mod_name, mod_var, stat_lats,
                     stat_lons, stat_names, min_dim, vert_which, files_created,
                     err_log=None, **alt_range):
        mcfg = self.model_config[mod_name]
        data_id = mcfg['model_id']

        reader = ReadGridded(data_id=data_id)

        rf = mcfg['model_ts_type_read']

        read_freq = self.GRIDDED_TS_TYPE
        if rf is not None:
            if isinstance(rf, str):
                read_freq = rf
            elif isinstance(rf, dict) and mod_var in rf:
                    read_freq = read_freq[mod_var]

        data = reader.read_var(mod_var, ts_type=read_freq,
                               ts_type_flex=True)

        data = data.resample_time(to_ts_type=self.GRIDDED_TS_TYPE)
        stations = data.to_time_series(longitude=stat_lons,
                                       latitude=stat_lats,
                                       add_meta=dict(station_name=stat_names))

        stats_processed = []
        map_data = []

        got_one = False
        for stat in stations:
            stat_name = stat['station_name']
            print(mod_var, stat['station_name'], obs_name, mod_name)
            if stat_name in stats_processed:
                raise Exception('Unexpected Error, please check')

            try:

                data_dict = self._station_to_timeseries(stat,
                                                        var_name=mod_var,
                                                        **alt_range)
                (trends_stat,
                 map_stat) = self._compute_trends_station(data_dict,
                                                          min_dim=min_dim)

                fname = self._save_stat_json(trends_stat,
                                             obs_var=obs_var,
                                             obs_name=obs_name,
                                             vert_which=vert_which,
                                             mod_name=mod_name,
                                             mod_var=mod_var)
                files_created['ts'].append(fname)
                got_one = True

                if map_stat:
                    map_data.append(map_stat)

            except DataCoverageError as e:
                msg = ('Error: {} {}, {}'.format(mod_var, stat.station_name,
                                                 repr(e)))
                print(msg)
                if err_log:
                    err_log.write(msg + '\n')

        # Add to map only if at least one station is available
        if got_one:
            map_outname = self._save_map_json(map_data,
                                              obs_name=obs_name,
                                              obs_var=obs_var,
                                              vert_which=vert_which,
                                              mod_name=mod_name,
                                              mod_var=mod_var)
            files_created['map'].append(map_outname)

        return files_created

def check_ebas_default():
    """Make sure the EBAS default configuration has not changed"""
    from pyaerocom.io import ReadEbas
    r = ReadEbas()
    assert r.opts.eval_flags
    assert r.opts.keep_aux_vars == False

if __name__ == '__main__':
    t = TrendsEvaluation()
