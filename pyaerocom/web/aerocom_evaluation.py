#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fnmatch import fnmatch
import glob
import os
import numpy as np
from pathlib import Path
import shutil
import simplejson
from traceback import format_exc

# internal pyaerocom imports
from pyaerocom._lowlevel_helpers import (check_dirs_exist, dict_to_str,
                                         chk_make_subdir)
from pyaerocom import const
from pyaerocom.colocation_auto import ColocationSetup, Colocator
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.helpers import isnumeric

from pyaerocom.io.helpers import save_dict_json

from pyaerocom.web.helpers import (ObsConfigEval, ModelConfigEval,
                                   read_json, write_json)

from pyaerocom.web.const import (HEATMAP_FILENAME_EVAL_IFACE_DAILY,
                                 HEATMAP_FILENAME_EVAL_IFACE_MONTHLY,
                                 HEATMAP_FILENAME_EVAL_IFACE_YEARLY)
from pyaerocom.web.helpers_evaluation_iface import (
    update_menu_evaluation_iface,
    make_info_table_evaluation_iface,
    compute_json_files_from_colocateddata,
    delete_experiment_data_evaluation_iface,
    make_info_str_eval_setup)

from pyaerocom.web.web_naming_conventions import VAR_MAPPING



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
    exp_descr : str
        string that explains in more detail what this project is about.
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
    modelorder_from_config : bool
        if True, then the order of the models in the menu file (i.e. on the
        website) will be the same as defined in :attr:`model_config`.
    obsorder_from_config : bool
        if True, then the order of the observations in the menu file (i.e. on
        the website) will be the same as defined in :attr:`obs_config`.

    Parameters
    ----------
    proj_id : str, optional
        ID of project
    exp_id : str, optional
        experiment ID
    config_dir : str, optional
        directory where config json file is located. Needed if the configuration
        is supposed to be load from a configuration file. The name of that file
        is automatically inferred from input `proj_id` and `exp_id`, which need
        to be specified.
    try_load_json : bool
        if True, and if a config json file can be inferred and found from the
        former 3 input args, this configuration is loaded automatically.
        Note also that settings can be provided via arg `**settings` when
        instantiating the class. These are updated *after* the reading of the
        json file, which will overwrite affected attributes defined in the json
        file.
    init_output_dirs : bool
        if True, all required output directories for json files and colocated
        NetCDF files are already created when instantiating the class. This is
        recommended if you intend to use individual methods of this class such
        as :func:`run_colocation` or :func:`find_coldata_files` and is of
        particular relevance for the storage location of the colocated data
        files. Defaults to True.
    """
    OUT_DIR_NAMES = ['map', 'ts', 'ts/dw', 'scat', 'hm', 'profiles',
                     'contour']

    #: Vertical layer ranges
    VERT_LAYERS = {'0-2km'  :   [0, 2000],
                   '2-5km'  :   [2000, 5000],
                   '5-10km' :   [5000, 10000]}

    #: Allowed options for vertical codes
    VERT_CODES = ['Surface', 'Column']
    VERT_CODES.extend(VERT_LAYERS)

    #: vertical schemes that may be used for colocation
    VERT_SCHEMES = {'Surface' : 'surface'}

    JSON_SUPPORTED_VERT_SCHEMES = ['Column', 'Surface']
    #: Attributes that are ignored when writing setup to json file
    JSON_CFG_IGNORE = ['add_methods', '_log', 'out_dirs']

    _OPTS_NAMES_OUTPUT = {
            'clear_existing_json' : 'Delete existing json files before reanalysis',
            'reanalyse_existing'  : 'Reanalyse existing colocated NetCDF files',
            'only_colocation'     : 'Run only colocation (no json files computed)',
            'raise_exceptions'    : 'Raise exceptions if they occur'
    }

    #: status of experiment
    EXP_STATUS_VALS = ['public', 'experimental']

    #: attributes that are not supported by this interface
    FORBIDDEN_ATTRS = ['basedir_coldata']
    def __init__(self, proj_id, exp_id, config_dir=None,
                 try_load_json=True, init_output_dirs=False, **settings):

        self._log = const.print_log

        self.proj_id = proj_id

        self.exp_id = exp_id

        self.exp_name = None

        self.exp_descr = ''

        self.exp_status = 'experimental'

        self.clear_existing_json = True

        self.only_colocation = False
        self.only_json = False

        self.weighted_stats=False
        self.annual_stats_constrained=False

        #: Base directory for output
        self.out_basedir = os.path.join(const.OUTPUTDIR, 'aeroval')

        #: Base directory to store colocated data (sub dirs for proj and
        #: experiment will be created automatically)
        self.coldata_basedir = None

        #: Directory that contains configuration files
        self.config_dir = config_dir

        #: If True, process also model maps
        self.add_maps = False

        self.maps_res_deg = 5
        self.maps_vmin_vmax = None

        #: If True, process only maps (skip obs evaluation)
        self.only_maps = False

        #: Output directories for different types of json files (will be filled
        #: in :func:`init_json_output_dirs`)
        self._out_dirs = {}

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
        self.var_mapping.update(VAR_MAPPING)
        self.var_order_menu = []

        self.regions_how = 'default'
        self.resample_how = None

        self.zeros_to_nan = False

        self.summary_str = ''
        self._valid_obs_vars = {}

        self.modelorder_from_config = True
        self.obsorder_from_config = True

        if (len(settings)==0 and try_load_json and isinstance(proj_id, str)
            and isinstance(exp_id, str)):
            try:
                self.load_config(proj_id, exp_id, config_dir)
                const.print_log.info(
                    f'Found and imported config file for project {proj_id}, '
                    f'experiment {exp_id}'
                    )

            except Exception:
                const.print_log.warning(
                    f'Failed to import config file for project {proj_id}, '
                    f'experiment {exp_id}. Reason:\n{format_exc()}'
                    )
        self.update(**settings)
        self._check_init_col_outdir()
        if init_output_dirs:
            self.init_json_output_dirs()

    @property
    def proj_dir(self):
        """Project directory"""
        return os.path.join(self.out_basedir, self.proj_id)

    @property
    def exp_dir(self):
        """Experiment directory"""
        return os.path.join(self.proj_dir, self.exp_id)

    @property
    def coldata_dir(self):
        """Base directory for colocated data files"""
        return self.colocation_settings['basedir_coldata']

    @property
    def out_dirs(self):
        if len(self._out_dirs) == 0:
            self.init_json_output_dirs()
        return self._out_dirs

    @property
    def regions_file(self):
        """json file containing region specifications"""
        return os.path.join(self.exp_dir, 'regions.json')

    @property
    def menu_file(self):
        """json file containing region specifications"""
        return os.path.join(self.proj_dir, 'menu.json')

    @property
    def model_order_menu(self):
        """Order of models in menu

        Note
        ----
        Returns empty list if no specific order is to be used in which case
        the models will be alphabetically ordered
        """
        order = []
        if self.modelorder_from_config:
            order.extend(self.model_config.keys())
        return order

    @property
    def obs_order_menu(self):
        """Order of observations in menu

        Note
        ----
        Returns empty list if no specific order is to be used in which case
        the observations will be alphabetically ordered
        """
        order = []
        if self.obsorder_from_config:
            order.extend(self.obs_config.keys())
        return order

    @property
    def all_model_names(self):
        """List of all model names"""
        return list(self.model_config)

    @property
    def all_obs_names(self):
        """List of all obs names"""
        return list(self.obs_config)

    @property
    def all_obs_vars(self):
        """List of all obs variables"""
        obs_vars = []
        for oname, ocfg in self.obs_config.items():
            obs_vars.extend(ocfg['obs_vars'])
        return sorted(list(np.unique(obs_vars)))

    @property
    def all_modelmap_vars(self):
        """List of variables to be processed for model map display

        Note
        ----
        For now this is just a wrapper for :attr:`all_obs_vars`
        """
        return self.all_obs_vars

    @property
    def all_map_files(self):
        """List of all existing map files"""
        if not os.path.exists(self.out_dirs['map']):
            raise FileNotFoundError('No data available for this experiment')
        return os.listdir(self.out_dirs['map'])

    @property
    def raise_exceptions(self):
        """Boolean specifying whether exceptions should be raised in analysis
        """
        return self.colocation_settings['raise_exceptions']

    @raise_exceptions.setter
    def raise_exceptions(self, val):
        self.colocation_settings['raise_exceptions'] =  val

    @property
    def reanalyse_existing(self):
        """Specifies whether existing colocated data files should be reanalysed
        """
        return self.colocation_settings['reanalyse_existing']

    @reanalyse_existing.setter
    def reanalyse_existing(self, val):
        self.colocation_settings['reanalyse_existing'] = val

    @property
    def all_model_map_files(self):
        """List of all jsoncontour and json files associated with model maps"""
        if not os.path.exists(self.out_dirs['contour']):
            raise FileNotFoundError('No data available for this experiment')
        return os.listdir(self.out_dirs['contour'])

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

    def update_summary_str(self):
        """Updates :attr:`summary_str` using :func:`make_info_str_eval_setup`"""
        try:
            self.summary_str = make_info_str_eval_setup(self,
                                                        add_header=False)
        except Exception as e:
            const.print_log.warning(
                'Failed to create automatic summary string of AerocomEvaluation '
                f'setup class. Reason: {e}')

    def update(self, **settings):
        """Update current setup"""
        for k, v in settings.items():
            self[k] = v
        self.check_config()
        self.update_summary_str()

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
        if key in self.FORBIDDEN_ATTRS:
            raise AttributeError(
                f'Attr {key} is not allowed in AerocomEvaluation'
                )
        elif key in self.colocation_settings:
            self.colocation_settings[key] = val
        elif key == 'obs_config':
            self._set_obsconfig(val)
        elif key == 'model_config':
            self._set_modelconfig(val)
        elif key == 'colocation_settings':
            self.colocation_settings.update(**val)
        elif key == 'var_mapping':
            self.var_mapping.update(val)
        elif isinstance(key, str) and isinstance(val, dict):
            if 'obs_id' in val:
                self.obs_config[key] = ObsConfigEval(**val)
            elif 'model_id' in val:
                self.model_config[key] = ModelConfigEval(**val)
            else:
                self.__dict__[key] = val
        elif key in self.__dict__:
            self.__dict__[key] = val

        else:
            const.print_log.warning(
                f'Invalid input key {key} for AerocomEvaluation. Will be '
                f'ignored'
            )

    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        elif key in self.colocation_settings:
            return self.colocation_settings[key]

    def init_json_output_dirs(self, out_basedir=None):
        """Check and create directories for json files"""
        if out_basedir is not None:
            self.out_basedir = out_basedir
        if not os.path.exists(self.out_basedir):
            os.mkdir(self.out_basedir)
        check_dirs_exist(self.out_basedir, self.proj_dir, self.exp_dir)
        outdirs = {}
        for dname in self.OUT_DIR_NAMES:
            outdirs[dname] = os.path.join(self.exp_dir, dname)
        check_dirs_exist(**outdirs)
        self._out_dirs = outdirs
        return outdirs

    def _check_init_col_outdir(self):
        cs = self.colocation_settings

        cbd = self.coldata_basedir
        if cbd is None:
            # this will make sure the base directory exists (or crash) and
            # returns a string
            cbd = cs._check_basedir_coldata()
        elif isinstance(cbd, Path):
            cbd = str(cbd)

        if not os.path.exists(cbd):
            os.mkdir(cbd)

        add_dirs = f'{self.proj_id}/{self.exp_id}'
        if cbd.endswith(add_dirs):
            col_out = cbd
        else:
            col_out = os.path.join(cbd, add_dirs)
        if not os.path.exists(col_out):
            const.print_log.info(
                f'Creating output directory for colocated data files: {col_out}')
            os.makedirs(col_out, exist_ok=True)
        else:
            const.print_log.info(
                f'Setting output directory for colocated data files to:\n{col_out}'
                )
        self.coldata_basedir = cbd
        self.colocation_settings['basedir_coldata'] = col_out

    def check_config(self):
        if not isinstance(self.proj_id, str):
            raise AttributeError(f'proj_id must be str, '
                                 f'(current value: {self.proj_id})')

        if not isinstance(self.exp_id, str):
            raise AttributeError(f'exp_id must be str, '
                                 f'(current value: {self.exp_id})')

        if not isinstance(self.exp_descr, str):
            raise AttributeError(f'exp_descr must be specified, '
                                 f'(current value: {self.exp_descr})')

        elif not len(self.exp_descr.split()) > 5:
            const.print_log.warning(
                f'Experiment description (attr. exp_descr) is either missing or '
                f'rather short (less than 5 words). Consider providing more '
                f'information here! Current: {self.exp_descr}'
                )

        if not isinstance(self.exp_status, str):
            raise AttributeError(f'exp_status must be specified, '
                                 f'(current value: {self.exp_status})')
        elif not self.exp_status in self.EXP_STATUS_VALS:
            raise ValueError(
                f'Invalid input for exp_status ({self.exp_status}). '
                f'Choose from: {self.EXP_STATUS_VALS}.')


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

    def get_model_name(self, model_id):
        """Get model name for input model ID

        Parameters
        ----------
        model_id : str
            AeroCom ID of model

        Returns
        -------
        str
            name of model

        Raises
        ------
        AttributeError
            if no match could be found
        """
        for mname, mcfg in self.model_config.items():
            if mname == model_id or mcfg['model_id'] == model_id:
                return mname
        raise AttributeError('No match could be found for input name {}'
                             .format(model_id))

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

    def get_diurnal_only(self,obs_name,colocated_data):
        """

        Parameters
        ----------
        obs_name : string
            Name of observational subset
        colocated_data : ColocatedData
            A ColocatedData object that will be checked for the presence of
            parameter 'diurnal_only'.

        Raises
        ------
        ValueError
            Raised if colocated_data has 'diurnal_only' set, but it is not a boolean
        NotImplementedError
            Raised if colocated_data has ts_type != 'hourly'

        Returns
        -------
        diurnal_only : bool


        """
        try:
            diurnal_only = self.obs_config[obs_name]['diurnal_only']
        except:
            diurnal_only = False
        if not isinstance(diurnal_only,bool):
            raise ValueError(f'Need Boolean dirunal_only for {obs_name}, got {type(diurnal_only)}')
        ts_type = colocated_data.ts_type
        try:
            if diurnal_only and ts_type != 'hourly':
                raise NotImplementedError
        except:
            print(f'Diurnal processing is only available for ColocatedData with ts_type=hourly. Got diurnal_only={diurnal_only} for {obs_name} with ts_type {ts_type}.')
        return diurnal_only

    def compute_json_files_from_colocateddata(self, coldata, obs_name,
                                              model_name):
        """Creates all json files for one ColocatedData object"""
        vert_code = self.get_vert_code(obs_name, coldata.metadata['var_name'][0])
        try:
            web_iface_name = self.obs_config[obs_name]['web_interface_name']
        except:
            web_iface_name = obs_name
        diurnal_only = self.get_diurnal_only(obs_name,coldata)

        col = Colocator()
        col.update(**self.colocation_settings)
        col.update(**self.obs_config[obs_name])
        col.update(**self.get_model_config(model_name))

        return compute_json_files_from_colocateddata(
                coldata=coldata,
                obs_name=obs_name,
                model_name=model_name,
                use_weights=self.weighted_stats,
                colocation_settings=col,
                vert_code=vert_code,
                out_dirs=self.out_dirs,
                regions_json=self.regions_file,
                web_iface_name=web_iface_name,
                diurnal_only=diurnal_only,
                regions_how=self.regions_how,
                zeros_to_nan=self.zeros_to_nan,
                annual_stats_constrained=self.annual_stats_constrained
                )


    def get_vert_code(self, obs_name, obs_var):
        """Get vertical code name for obs / var combination"""
        info =  self.obs_config[obs_name]['obs_vert_type']
        if isinstance(info, str):
            return info
        return info[obs_var]

    @property
    def _heatmap_files(self):

        return dict(daily=os.path.join(self.out_dirs['hm'], HEATMAP_FILENAME_EVAL_IFACE_DAILY),
                    monthly=os.path.join(self.out_dirs['hm'], HEATMAP_FILENAME_EVAL_IFACE_MONTHLY),
                    yearly=os.path.join(self.out_dirs['hm'], HEATMAP_FILENAME_EVAL_IFACE_YEARLY))

    def update_heatmap_json(self):
        """
        Synchronise content of heatmap json files with content of menu.json

        Raises
        ------
        ValueError
            if this experiment (:attr:`exp_id`) is not registered in menu.json
        """
        for freq, fp in self._heatmap_files.items():
            if not os.path.exists(fp):
                #raise FileNotFoundError(fp)
                const.print_log.warning('Skipping heatmap file {} (for {} freq). '
                                        'File does not exist'.format(fp, freq))
                continue
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

            with open(fp, 'w') as f:
                simplejson.dump(hm, f, ignore_nan=True)

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
                    if var_name is not None:
                        try:
                            var_name = self.model_config[model_name]['model_use_vars'][var_name]
                        except:
                            pass
                        if not m['var_name'] == var_name:
                            match = False
                    if match:
                        files.append(os.path.join(coldata_dir, fname))
                except Exception:
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


        if colocator is not None:
            files = self._check_process_colfiles(files, colocator)

        if len(files) == 0:
            const.print_log.info('Nothing to do...')
            return converted
        for file in files:
            const.print_log.info('Processing file {}'.format(file))
            d = ColocatedData(file)
            self.compute_json_files_from_colocateddata(d, obs_name, model_name)
            converted.append(file)
        return converted

    def _check_process_colfiles(self, files, colocator):
        remaining = []
        for file in files:
            fname = os.path.basename(file)
            if not fname in colocator.file_status:
                const.print_log.info('Skipping computation of json files from '
                                     'colocated data file {}. This file is not '
                                     'part of this experiment (obs config)'
                                     .format(fname))
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
            remaining.append(file)
        return remaining

    def delete_all_colocateddata_files(self, model_name, obs_name):
        """
        Delete all
        Parameters
        ----------
        model_name : TYPE
            DESCRIPTION.
        obs_name : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
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

        col = Colocator(**self.colocation_settings)

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
            raise KeyError(
                f'No observations could be found that match input '
                f'{name_or_pattern}. Choose from {list(self.obs_config.keys())}'
                )
        return matches

    def _check_and_get_iface_names(self):
        """
        Get web interface names of all observations.

        Raises
        ------
        ValueError
            if value of one obsentry name is not a string.

        Returns
        -------
        iface_names : list
            list of obs names used in the web interface.

        """
        obs_list = list(self.obs_config)
        iface_names = []
        for obs_name in obs_list:
            try:
                if self.obs_config[obs_name]['web_interface_name'] == None:
                    self.obs_config[obs_name]['web_interface_name'] = obs_name
                else:
                    pass
            except KeyError:
                self.obs_config[obs_name]['web_interface_name'] = obs_name
            if not isinstance(self.obs_config[obs_name]['web_interface_name'], str):
                raise ValueError(
                    f'Invalid value for web_iface_name in {obs_name}. Need str.'
                    )
            iface_names.append(self.obs_config[obs_name]['web_interface_name'])
        iface_names = list(set(iface_names))
        return iface_names

    @property
    def iface_names(self):
        """
        List of observation dataset names used in web interface
        """
        return self._check_and_get_iface_names()

    def _run_superobs_entry_var(self, model_name, superobs_name, var_name,
                                try_colocate_if_missing):
        """
        Run evaluation of superobs entry

        Parameters
        ----------
        model_name : str
            name of model in :attr:`model_config`
        superobs_name : str
            name of super observation in :attr:`obs_config`
        var_name : str
            name of variable to be processed.
        try_colocate_if_missing : bool
            if True, then missing colocated data objects are computed on the
            fly.

        Raises
        ------
        ValueError
            If multiple (or no) colocated data objects are available for
            individual obs datasets of which the superobservation is comprised.

        Returns
        -------
        None
        """
        coldata_files = []
        coldata_resolutions = []
        vert_codes = []
        obs_needed = self.obs_config[superobs_name]['obs_id']
        for obs_name in obs_needed:
            if self.reanalyse_existing:
                self.run_colocation(model_name, obs_name, var_name)
                cdf = self.find_coldata_files(model_name, obs_name, var_name)
            else:
                cdf = self.find_coldata_files(model_name, obs_name, var_name)
                if len(cdf) == 0 and try_colocate_if_missing:
                    self.run_colocation(model_name, obs_name, var_name)
                    cdf = self.find_coldata_files(model_name, obs_name, var_name)

            if len(cdf) != 1:
                raise ValueError(
                    f'Fatal: Found multiple colocated data objects for '
                    f'{model_name}, {obs_name}, {var_name}: {cdf}...'
                    )
            fp = cdf[0]
            coldata_files.append(fp)
            meta = ColocatedData.get_meta_from_filename(fp)
            coldata_resolutions.append(meta['ts_type'])
            vc = self.get_vert_code(obs_name, var_name)
            vert_codes.append(vc)

        if len(np.unique(vert_codes)) > 1 or vert_codes[0] != self.get_vert_code(superobs_name, var_name):
            raise ValueError(
                "Cannot merge observations with different vertical types into "
                "super observation...")
        vert_code = vert_codes[0]
        if not len(coldata_files) == len(obs_needed):
            raise ValueError(f'Could not retrieve colocated data files for '
                             f'all required observations for super obs '
                             f'{superobs_name}')

        coldata = []
        from pyaerocom.helpers import get_lowest_resolution
        to_freq = get_lowest_resolution(*coldata_resolutions)
        import xarray as xr
        darrs = []
        for fp in coldata_files:
            data = ColocatedData(fp)
            if data.ts_type != to_freq:
                meta = data.metadata
                try:
                    rshow = meta['resample_how']
                except KeyError:
                    rshow = None

                data.resample_time(
                    to_ts_type=to_freq,
                    how=rshow,
                    apply_constraints=meta['apply_constraints'],
                    min_num_obs=meta['min_num_obs'],
                    colocate_time=meta['colocate_time'],
                    inplace=True)
            arr = data.data
            ds = arr['data_source'].values
            source_new = [superobs_name, ds[1]]
            arr['data_source'] = source_new #obs, model_id
            arr.attrs['data_source'] = source_new
            darrs.append(arr)

        merged = xr.concat(darrs, dim='station_name')
        coldata = ColocatedData(merged)
        return compute_json_files_from_colocateddata(
                coldata=coldata,
                obs_name=superobs_name,
                model_name=model_name,
                use_weights=self.weighted_stats,
                colocation_settings=coldata.get_time_resampling_settings(),
                vert_code=vert_code,
                out_dirs=self.out_dirs,
                regions_json=self.regions_file,
                web_iface_name=superobs_name,
                diurnal_only=False,
                regions_how=self.regions_how,
                zeros_to_nan=self.zeros_to_nan,
                annual_stats_constrained=self.annual_stats_constrained
                )

    def _run_superobs_entry(self, model_name, superobs_name, var_name=None,
                            try_colocate_if_missing=True):
        if not superobs_name in self.obs_config:
            raise AttributeError(
                f'No such super-observation {superobs_name}'
                )
        sobs_cfg = self.obs_config[superobs_name]
        if not sobs_cfg['is_superobs']:
            raise ValueError(f'Obs config entry for {superobs_name} is not '
                             f'marked as a superobservation. Please add '
                             f'is_superobs in config entry...')
        if isinstance(var_name, str):
            process_vars = [var_name]
        else:
            process_vars = sobs_cfg['obs_vars']
        for var_name in process_vars:
            try:
                self._run_superobs_entry_var(model_name,
                                             superobs_name,
                                             var_name,
                                             try_colocate_if_missing)
            except Exception:
                if self.raise_exceptions:
                    raise
                const.print_log.warning(
                    f'Failed to process superobs entry for {superobs_name},  '
                    f'{model_name}, var {var_name}. Reason: {format_exc()}')

    def _process_map_var(self, model_name, var, reanalyse_existing):
        """
        Process model data to create map json files

        Parameters
        ----------
        model_name : str
            name of model
        var : str
            name of variable
        reanalyse_existing : bool
            if True, already existing json files will be reprocessed

        Raises
        ------
        ValueError
            If vertical code of data is invalid or not set
        AttributeError
            If the data has the incorrect number of dimensions or misses either
            of time, latitude or longitude dimension.
        """
        from pyaerocom.web.web_maps_helpers import (calc_contour_json,
                                                    griddeddata_to_jsondict)

        data = self.read_model_data(model_name, var)

        vc = data.vert_code
        if not isinstance(vc, str) or vc=='':
            raise ValueError(f'Invalid vert_code {vc} in GriddedData')
        elif vc == 'ModelLevel':
            if not data.ndim == 4:
                raise ValueError('Invalid ModelLevel file, needs to have '
                                 '4 dimensions (time, lat, lon, lev)')
            data = data.extract_surface_level()
            vc = 'Surface'
        elif not vc in self.JSON_SUPPORTED_VERT_SCHEMES:
            raise ValueError(f'Cannot process {vc} files. Supported vertical '
                             f'codes are {self.JSON_SUPPORTED_VERT_SCHEMES}')
        if not data.has_time_dim:
            raise AttributeError('Data needs to have time dimension...')
        elif not data.has_latlon_dims:
            raise AttributeError('Data needs to have lat and lon dimensions')
        elif not data.ndim == 3:
            raise AttributeError('Data needs to be 3-dimensional')

        outdir = self.out_dirs['contour']
        outname = f'{var}_{vc}_{model_name}'

        fp_json = os.path.join(outdir, f'{outname}.json')
        fp_geojson = os.path.join(outdir, f'{outname}.geojson')

        if not reanalyse_existing:
            if os.path.exists(fp_json) and os.path.exists(fp_geojson):
                const.print_log.info(
                    f'Skipping processing of {outname}: data already exists.'
                    )
                return


        if not data.ts_type == 'monthly':
            data = data.resample_time('monthly')

        data.check_unit()

        vminmax = self.maps_vmin_vmax
        if isinstance(vminmax, dict) and var in vminmax:
            vmin, vmax = vminmax[var]
        else:
            vmin, vmax = None, None

        # first calcualate and save geojson with contour levels
        contourjson = calc_contour_json(data, vmin=vmin, vmax=vmax)

        # now calculate pixel data json file (basically a json file
        # containing monthly mean timeseries at each grid point at
        # a lower resolution)
        if isnumeric(self.maps_res_deg):
            lat_res = self.maps_res_deg
            lon_res = self.maps_res_deg
        else:
            lat_res = self.maps_res_deg['lat_res_deg']
            lon_res = self.maps_res_deg['lon_res_deg']


        datajson = griddeddata_to_jsondict(data,
                                           lat_res_deg=lat_res,
                                           lon_res_deg=lon_res)

        save_dict_json(contourjson, fp_geojson)
        save_dict_json(datajson, fp_json)

    def run_map_eval(self, model_name, var_name, reanalyse_existing,
                     raise_exceptions):
        """Run evaluation of map processing

        Create json files for model-maps display. This analysis does not
        require any observation data but processes model output at all model
        grid points, which is then displayed on the website in the maps
        section.

        Parameters
        ----------
        model_name : str
            name of model to be processed
        var_name : str, optional
            name of variable to be processed. If None, all available
            observation variables are used.
        reanalyse_existing : bool
            if True, existing json files will be reprocessed
        raise_exceptions : bool
            if True, any exceptions that may occur will be raised
        """
        if var_name is None:
            all_vars = self.all_modelmap_vars
        else:
            all_vars = [var_name]

        model_cfg = self.get_model_config(model_name)
        settings = {}
        settings.update(self.colocation_settings)
        settings.update(model_cfg)

        for var in all_vars:
            const.print_log.info(f'Processing model maps for '
                                 f'{model_name} ({var})')

            try:
                self._process_map_var(model_name, var,
                                      reanalyse_existing)

            except Exception:
                if raise_exceptions:
                    raise
                const.print_log.warning(
                    f'Failed to process maps for {model_name} {var} data. '
                    f'Reason: {format_exc()}')

    def run_evaluation(self, model_name=None, obs_name=None, var_name=None,
                       update_interface=True,
                       reanalyse_existing=None, raise_exceptions=None,
                       clear_existing_json=None, only_colocation=None,
                       only_json=None, only_maps=None):
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
        raise_exceptions : bool, optional
            if True, exceptions during colocation will be raised if they occur
            (for debugging). If None, the class default will be used (defined
            in config file)
        clear_existing_json : bool, optional
            if True, existing json files for model / obs combination will be
            deleted before rerun. If None, the
            class default will be used (defined in config file)
        only_colocation : bool, optional
            if True, only colocation will be performed and no json files will
            be created. If None, the class default will be used (defined in
            config file)
        only_json : bool, optional
            if True, no colocation will be performed and only existing
            colocated data files will be re-processed.

        Returns
        -------
        list
            list containing all colocated data objects that have been converted
            to json files.
        """
        res = None
        if reanalyse_existing is not None:
            self.reanalyse_existing = reanalyse_existing
        if raise_exceptions is not None:
            self.raise_exceptions = raise_exceptions
        if clear_existing_json is not None:
            self.clear_existing_json = clear_existing_json
        if only_colocation is not None:
            self.only_colocation = only_colocation
        if only_json is not None:
            self.only_json = only_json
        if only_maps is not None:
            self.only_maps = only_maps

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

        # compute model maps (completely independent of obs-eval
        # processing below)
        if self.add_maps:
            for model_name in model_list:
                self.run_map_eval(model_name, var_name,
                                  reanalyse_existing=reanalyse_existing,
                                  raise_exceptions=raise_exceptions)

        if not self.only_maps:
            for obs_name in obs_list:
                if obs_name in self.obs_ignore:
                    self._log.info('Skipping observation {}'.format(obs_name))
                    continue
                for model_name in model_list:
                    if model_name == obs_name:
                        msg = ('Cannot run same dataset against each other'
                               '({} vs. {})'.format(model_name, model_name))
                        self._log.info(msg)
                        const.print_log.info(msg)
                        continue

                    if model_name in self.model_ignore:
                        self._log.info('Skipping model {}'.format(model_name))
                        continue
                    if self.obs_config[obs_name]['is_superobs']:
                        try:
                            self._run_superobs_entry(model_name, obs_name, var_name,
                                                     try_colocate_if_missing=True)
                        except Exception as e:
                            if raise_exceptions:
                                raise
                            const.print_log.warning(
                                'failed to process superobs...')
                    elif self.obs_config[obs_name]['only_superobs']:
                        const.print_log.info(
                            f'Skipping json processing of {obs_name}, as this is '
                            f'marked to be used only as part of a superobs '
                            f'network')
                    else:
                        if not self.only_json:
                            col = self.run_colocation(model_name, obs_name, var_name)
                        else:
                            col = None
                        if only_colocation:
                            self._log.info('Skipping computation of json files for {}'
                                           '/{}'.format(obs_name, model_name))
                            continue
                        res = self.make_json_files(model_name, obs_name, var_name,
                                                   colocator=col)

        if update_interface:
            self.update_interface()
        const.print_log.info('Finished processing.')
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

    def check_read_model(self, model_name, var_name,  **kwargs):
        const.print_log.warning(DeprecationWarning('Deprecated name of method '
                                                   'read_model_data. Please '
                                                   'use new name'))

        return self.read_model_data(model_name, var_name,  **kwargs)

    def read_model_data(self, model_name, var_name,
                        **kwargs):
        """Read model variable data

        """
        if not model_name in self.model_config:
            raise ValueError('No such model available {}'.format(model_name))
        #mcfg = self.get_model_config(model_name)

        col = Colocator()
        col.update(**self.colocation_settings)
        col.update(**self.get_model_config(model_name))
        #col.update(**kwargs)

        data = col.read_model_data(var_name, **kwargs)

        return data

    def read_ungridded_obsdata(self, obs_name, vars_to_read=None):
        """Read observation network"""

        col = Colocator()
        col.update(**self.colocation_settings)
        col.update(**self.obs_config[obs_name])

        data = col.read_ungridded(vars_to_read)
        return data

    @staticmethod
    def _info_from_map_file(filename):
        f = filename
        obs_info = f.split('OBS-')[1].split('_MOD')[0].split('_')
        obs_name, obs_var = obs_info[0].split(':')
        vert_code = obs_info[1]
        mod_name, mod_var =  f.split('MOD-')[1].split('.json')[0].split(':')
        return (obs_name, obs_var, vert_code, mod_name, mod_var)

    def get_web_overview_table(self):
        """Computes overview table based on existing map files"""
        iface_names = self.iface_names
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
                    const.print_log.warning('Found outdated json map file: {}. '
                                            'Will be ignored'.format(f))
                    continue
                elif not obs_name in iface_names:
                    const.print_log.warning('Found outdated json map file: {}. '
                                            'Will be ignored'.format(f))
                    continue
                mcfg = self.model_config[mod_name]
                if 'model_use_vars' in mcfg and obs_var in mcfg['model_use_vars']:
                    if mcfg['model_use_vars'][obs_var] != mod_var:
                        const.print_log.warning('Ignoring map file {}'
                                                .format(f))
                        continue
                tab.append([obs_var, obs_name, vert_code, mod_name, mod_var])
        if len(tab) == 0:
            raise FileNotFoundError('No json files could be found')
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
        except Exception:
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
        try:
            self.make_info_table_web()
            self.update_heatmap_json()
            self.to_json(self.exp_dir)
        except KeyError: # if no data is available for this experiment
            pass

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
        output = {}
        for k, cfg in self.obs_config.items():
            as_dict = {}
            as_dict.update(**cfg)
            output[k] = as_dict
        return output

    def _model_config_asdict(self):
        output = {}
        for k, cfg in self.model_config.items():
            as_dict = {}
            as_dict.update(**cfg)
            output[k] = as_dict
        return output

    def delete_experiment_data(self, base_dir=None, proj_id=None, exp_id=None,
                               also_coldata=True):
        """Delete all data associated with a certain experiment

        Parameters
        ----------
        base_dir : str, optional
            basic output direcory (containing subdirs of all projects)
        proj_name : str, optional
            name of project, if None, then this project is used
        exp_name : str, optional
            name experiment, if None, then this project is used
        also_coldata : bool
            if True and if output directory for colocated data is default and
            specific for input experiment ID, then also all associated colocated
            NetCDF files are deleted. Defaults to True.
        """
        if proj_id is None:
            proj_id = self.proj_id
        if exp_id is None:
            exp_id = self.exp_id
        if base_dir is None:
            base_dir = self.out_basedir
        try:
            delete_experiment_data_evaluation_iface(base_dir, proj_id, exp_id)
        except NameError:
            pass
        if also_coldata:
            coldir = self.colocation_settings['basedir_coldata']
            chk = os.path.normpath(f'{self.proj_id}/{self.exp_id}')
            if os.path.normpath(coldir).endswith(chk) and os.path.exists(coldir):
                const.print_log.info(f'Deleting everything under {coldir}')
                shutil.rmtree(coldir)
        self.update_menu()

    def _clean_modelmap_files(self):
        all_vars = self.all_modelmap_vars
        all_mods = self.all_model_names
        out_dir = self.out_dirs['contour']

        for file in os.listdir(out_dir):
            spl = file.replace('.', '_').split('_')
            if not len(spl) == 4:
                raise ValueError(f'Invalid json map filename {file}')
            var, vc, mod_name = spl[:3]
            rm = (not var in all_vars or
                  not mod_name in all_mods or
                  not vc in self.JSON_SUPPORTED_VERT_SCHEMES)
            if rm:
                const.print_log.info(
                    f'Removing invalid model maps file {file}'
                    )
                os.remove(os.path.join(out_dir, file))

    def clean_json_files(self, update_interface=False):
        """Checks all existing json files and removes outdated data

        This may be relevant when updating a model name or similar.
        """
        self._clean_modelmap_files()

        for file in self.all_map_files:
            (obs_name, obs_var, vc,
             mod_name, mod_var) = self._info_from_map_file(file)

            remove=False
            if not (obs_name in self.iface_names and
                    mod_name in self.model_config):
                remove = True
            elif not obs_var in self._get_valid_obs_vars(obs_name):
                remove = True
            elif not vc in self.JSON_SUPPORTED_VERT_SCHEMES:
                remove = True
            else:
                mcfg = self.model_config[mod_name]
                if 'model_use_vars' in mcfg and obs_var in mcfg['model_use_vars']:
                    if not mod_var == mcfg['model_use_vars'][obs_var]:
                        remove=True

            if remove:
                const.print_log.info(f'Removing outdated map file: {file}')
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
        obs_var, vc, _ = spl[1].replace('.', '_').split('_')
        rm = (not vc in self.JSON_SUPPORTED_VERT_SCHEMES or
              not obs_name in self.obs_config or
              not obs_var in self._get_valid_obs_vars(obs_name))
        if rm:
            const.print_log.info('Removing outdated ts file: {}'.format(fp))
            os.remove(fp)
            return
        try:
            data = read_json(fp)
        except Exception:
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

    @property
    def name_config_file(self):
        """
        File name of config file (without file ending specification)

        Returns
        -------
        str
            name of config file
        """
        return 'cfg_{}_{}'.format(self.proj_id, self.exp_id)

    @property
    def name_config_file_json(self):
        """
        File name of config file (with json ending)

        Returns
        -------
        str
            name of config file
        """
        return '{}.json'.format(self.name_config_file)

    def to_json(self, output_dir, ignore_nan=True, indent=3):
        """Convert analysis configuration to json file and save

        Parameters
        ----------
        output_dir : str
            directory where the config json file is supposed to be stored
        ignore_nan : bool
            set NaNs to Null when writing


        """
        self.update_summary_str()
        asdict = self.to_dict()
        out_name = self.name_config_file_json

        save_dict_json(asdict, os.path.join(output_dir, out_name),
                       ignore_nan=ignore_nan,
                       indent=indent)

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
        self.update_summary_str()
        indent = 2
        _indent_str = indent*' '
        head = f"pyaerocom {type(self).__name__}"
        underline = len(head)*"-"
        out_dirs = dict_to_str(self.out_dirs, indent=indent)
        s = f"\n{head}\n{underline}"
        s += (
            f'\nProject ID (proj_id): {self.proj_id}'
            f'\nExperiment ID (exp_id): {self.exp_id}'
            f'\nExperiment name (exp_name): {self.exp_name}'
            f'\nOutput directories for json files: {out_dirs}'
            )
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
    import pyaerocom as pya

    config_dir = pya.const.OUTPUTDIR

    stp = AerocomEvaluation(config_dir=config_dir)
    name = 'A useless experiment called blub, in the bla project.'
    descr = 'This experiment is indeed, completely useless!'
    stp = AerocomEvaluation('bla', 'blub', exp_name=name,
                            exp_descr=descr, exp_status='experimental')


