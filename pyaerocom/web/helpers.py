#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:00:44 2019

ToDo
----
- the configuration classes could inherit from a base class or could be more unified

"""
import os, glob, shutil
import simplejson
from pyaerocom import const
from pyaerocom._lowlevel_helpers import BrowseDict, sort_dict_by_name

def delete_experiment_data_evaluation_iface(base_dir, proj_id, exp_id):
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
    
    p = os.path.join(base_dir, proj_id, exp_id)
    if not os.path.exists(p):
        raise NameError('No such data directory found: {}'.format(p))
    
    shutil.rmtree(p)
    
def get_all_config_files_evaluation_iface(config_dir):
    """
    
    Note
    ----
    This code only checks json configuration files, not .py module files
    containing configuration.
    
    Parameters
    ----------
    config_dir : str
        directory containing config json files for AerocomEvaluation interface
        
    Returns
    -------
    dict
        nested dictionary containing file paths of all config files that were
        detected, where first level of dict id `proj_id` and second level 
        is `exp_id`.
    """
    
    results = {}
    
    for file in glob.glob('{}/*.json'.format(config_dir)):
        spl = os.path.basename(file).split('_')
        if not len(spl) == 3 or not spl[0] =='cfg':
            raise NameError('Invalid config file name ', file)
        proj, exp = spl[1], spl[2].split('.')[0]
        if not proj in results:
            results[proj] = {}
        results[proj][exp] = file
    return results

def get_all_config_files_trends_iface(config_dir):
    """Get all configuration files of trends interface
    
    Note
    ----
    This code only checks json configuration files, not .py module files
    containing configuration.
    
    Parameters
    ----------
    config_dir : str
        directory containing config json files for AerosolTrends interface
        
    Returns
    -------
   dictionary
        keys are configuration names, values are corresponding file paths
    """
    results = {}
    for file in  glob.glob('{}/cfg_*.json'.format(config_dir)):
        spl = os.path.basename(file).split('_')
        if not len(spl) == 2 or not spl[0] =='cfg':
            raise NameError('Invalid config file name ', file)
        results[spl[1].split('.')[0]] = file
    return results
      
class ObsConfigEval(BrowseDict):
    """Observation configuration for evaluation (dictionary)
    
    Note
    ----
    Only :attr:`obs_id` and `obs_vars` are mandatory, the rest is optional.
    
    Attributes
    ----------
    obs_id : str
        ID of observation network in AeroCom database 
        (e.g. 'AeronetSunV3Lev2.daily')
    obs_vars : list
        list of pyaerocom variable names that are supposed to be analysed
        (e.g. ['od550aer', 'ang4487aer'])
    obs_ts_type_read : :obj:`str` or :obj:`dict`, optional
        may be specified to explicitly define the reading frequency of the 
        observation data (so far, this does only apply to gridded obsdata such
        as satellites). For ungridded reading, the frequency may be specified
        via :attr:`obs_id`, where applicable (e.g. AeronetSunV3Lev2.daily).
        Can be specified variable specific in form of dictionary.
    obs_vert_type : :obj:`str` or :obj:`dict`, optional
        Aerocom vertical code encoded in the model filenames (only AeroCom 3 
        and later). Specifies which model file should be read in case there are
        multiple options (e.g. surface level data can be read from a 
        *Surface*.nc file as well as from a *ModelLevel*.nc file). If input is 
        string (e.g. 'Surface'), then the corresponding vertical type code is 
        used for reading of all variables that are colocated (i.e. that are 
        specified in :attr:`obs_vars`). Else (if input is dictionary, e.g. 
        `obs_vert_type=dict(od550aer='Column', ec550aer='ModelLevel')`), 
        information is extracted variable specific, for those who are defined
        in the dictionary, for all others, `None` is used.
    read_opts_ungridded : :obj:`dict`, optional
        dictionary that specifies reading constraints for ungridded reading
        (c.g. :class:`pyaerocom.io.ReadUngridded`).
    """
    SUPPORTED_VERT_CODES = ['Column', 'Profile', 'Surface']
    ALT_NAMES_VERT_CODES = dict(ModelLevel = 'Profile')
    def __init__(self, **kwargs):
        
        self.obs_id = None
        self.obs_vars = None
        self.obs_ts_type_read = None
        self.obs_vert_type = None
        
        self.read_opts_ungridded = None
        
        self.update(**kwargs)
        self.check_cfg()
    
    def check_cfg(self):
        """Check that minimum required attributes are set and okay"""
        if not isinstance(self.obs_id, str):
            raise ValueError('Invalid value for obs_id: {}. Need str.'
                             .format(self.obs_id))
        if isinstance(self.obs_vars, str):
            self.obs_vars = [self.obs_vars]
        elif not isinstance(self.obs_vars, list):
            raise ValueError('Invalid input for obs_vars. Need list or str, '
                             'got: {}'.format(self.obs_vars))
        ovt = self.obs_vert_type
        if ovt is None:
            raise ValueError('obs_vert_type is not defined. Please specify '
                             'using either of the available codes: {}. '
                             'It may be specified for all variables (as string) '
                             'or per variable using a dict'
                             .format(self.SUPPORTED_VERT_CODES))
        elif (isinstance(ovt, str) and not ovt in self.SUPPORTED_VERT_CODES):
            self.obs_vert_type = self._check_ovt(ovt)
        elif isinstance(self.obs_vert_type, dict):
            for var_name, val in self.obs_vert_type.items():
                if not val in self.SUPPORTED_VERT_CODES:
                    raise ValueError('Invalid value for obs_vert_type: {} '
                                     '(variable {}). Supported codes are {}.'
                                     .format(self.obs_vert_type,
                                             var_name,
                                             self.SUPPORTED_VERT_CODES))
    def _check_ovt(self, ovt):
        """Check if obs_vert_type string is valid alias
        
        Parameters
        ----------
        ovt : str
            obs_vert_type string
        
        Returns
        -------
        str
            valid obs_vert_type
        
        Raises
        ------
        ValueError
            if `ovt` is invalid
        """
        if ovt in self.ALT_NAMES_VERT_CODES:
            _ovt = self.ALT_NAMES_VERT_CODES[ovt]
            const.print_log.warning('Please use {} for obs_vert_code '
                                        'and not {}'.format(_ovt, ovt))
            return _ovt
        valid = self.SUPPORTED_VERT_CODES + list(self.ALT_NAMES_VERT_CODES.keys())
        raise ValueError('Invalid value for obs_vert_type: {}. '
                         'Supported codes are {}.'
                         .format(self.obs_vert_type,
                                 valid))
            
        
class ModelConfigEval(BrowseDict):
    """Modeln configuration for evaluation (dictionary)
    
    Note
    ----
    Only :attr:`model_id` is mandatory, the rest is optional.
    
    Attributes
    ----------
    model_id : str
        ID of model run in AeroCom database (e.g. 'ECMWF_CAMS_REAN')
    model_ts_type_read : :obj:`str` or :obj:`dict`, optional
        may be specified to explicitly define the reading frequency of the 
        model data. Not to be confused with :attr:`ts_type`, which specifies 
        the frequency used for colocation. Can be specified variable specific 
        by providing a dictionary.
    model_use_vars : :obj:`dict`, optional
        dictionary that specifies mapping of model variables. Keys are 
        observation variables, values are the corresponding model variables 
        (e.g. model_use_vars=dict(od550aer='od550csaer'))
    model_read_aux : :obj:`dict`, optional
        may be used to specify additional computation methods of variables from
        models. Keys are obs variables, values are dictionaries with keys 
        `vars_required` (list of required variables for computation of var 
        and `fun` (method that takes list of read data objects and computes
        and returns var)    
    """
    def __init__(self, model_id, **kwargs):
        self.model_id = model_id
        self.model_ts_type_read = None
        self.model_use_vars = {}
        self.model_read_aux = {}
        
        self.update(**kwargs)
        self.check_cfg()
    
    def check_cfg(self):
        """Check that minimum required attributes are set and okay"""
        if not isinstance(self.model_id, str):
            raise ValueError('Invalid input for model_id {}. Need str.'
                             .format(self.model_id))
            
def update_menu_evaluation_iface(config, ignore_experiments=None):
    """Update menu for Aerocom Evaluation interface
    
    The menu.json file is created based on the available json map files in the
    map directory of an experiment.
    
    Parameters
    ----------
    config : AerocomEvaluation
        instance of config class that has all relevant paths specified
    ignore_experiments : list, optional
        list containing experiment IDs that may be in the current menu.json 
        file and that are supposed to be removed from it.
    """
    def var_dummy():
        """Helper that creates empty dict for variable info"""
        return {'type'      :   '',
                'cat'       :   '',
                'name'      :   '',
                'longname'  :   '',
                'obs'       :   {}}
        
    new = {}
    if ignore_experiments is None:
        ignore_experiments = []
    try:
        tab = config.get_web_overview_table()
    except FileNotFoundError:
        import pandas as pd
        tab = pd.DataFrame()
    
    for index, info in tab.iterrows():
        obs_var, obs_name, vert_code, mod_name, mod_var = info
        if not obs_var in new:
            const.print_log.info('Adding new observation variable: {}'
                                 .format(obs_var))
            new[obs_var] = d = var_dummy()
            name, tp, cat = config.get_obsvar_name_and_type(obs_var)
    
            d['name'] = name
            d['type'] = tp
            d['cat']  =cat
            d['longname'] = const.VARS[obs_var].description
        else:
            d = new[obs_var]
        
        if not obs_name in d['obs']:
            d['obs'][obs_name] = dobs = {}
        else:
            dobs = d['obs'][obs_name]
        
        if not vert_code in dobs:
            dobs[vert_code] = dobs_vert = {}
        else:
            dobs_vert = dobs[vert_code]
        if mod_name in dobs_vert:
            raise Exception
        dobs_vert[mod_name] = {'dir' : mod_name,
                               'id'  : config.model_config[mod_name]['model_id'],
                               'var' : mod_var}
        
    _new = {}
    for var in config.var_order_menu:
        try:
            _new[var] = new[var]
        except:
            const.print_log.info('No variable {} found'.format(var))
    for var, info in new.items():
        if not var in _new:
            _new[var] = info
    new = _new
    new_sorted = {}
    for var, info in new.items():
        new_sorted[var] = info
        sorted_obs = sort_dict_by_name(info['obs'])
        new_sorted[var]['obs'] = sorted_obs
        for obs_name, vert_codes in sorted_obs.items():
            vert_codes_sorted = sort_dict_by_name(vert_codes)
            new_sorted[var]['obs'][obs_name] = vert_codes_sorted
            for vert_code, models in vert_codes_sorted.items():
                models_sorted = sort_dict_by_name(models)
                new_sorted[var]['obs'][obs_name][vert_code] = models_sorted
    new_menu = {}
    basedir = os.path.dirname(config.menu_file)
    available_exps = os.listdir(basedir)
    if os.path.exists(config.menu_file):
        current = read_json(config.menu_file)
        for exp, submenu in current.items():
            if exp in ignore_experiments:
                continue
            elif not exp in available_exps:
                const.print_log.info('Removing outdated experiment {} from '
                                     'menu.json'.format(exp))
                continue
            new_menu[exp] = submenu
    
    if config.exp_id in new_menu:
        const.print_log.warning('Sub menu for experiment {} already exists in '
                                'menu.json and will be overwritten'
                                .format(config.exp_id))
    
    new_menu[config.exp_id] = new_sorted
    
    with open(config.menu_file, 'w+') as f:
        f.write(simplejson.dumps(new_menu, indent=4))
 
def read_json(file_path):
    """Read json file
    
    Parameters
    ----------
    file_path : str
        json file path
    
    Returns
    -------
    dict
        content as dictionary
    """
    with open(file_path, 'r') as f:
        data = simplejson.load(f)
    return data

def write_json(data_dict, file_path, indent=4):
    """Save json file
    
    Parameters
    ----------
    data_dict : dict
        dictionary that can be written to json file
    file_path : str
        output file path
    """
    with open(file_path, 'w+') as f:
        f.write(simplejson.dumps(data_dict, indent=4))

def update_menu_trends_iface(config):
    """Update menu for Aerosol trends interface
    
    The menu.json file is created based on the available json map files in the
    map directory of an experiment.
    
    Parameters
    ----------
    config : AerocomEvaluation
        instance of config class that has all relevant paths specified
    """
    def var_dummy():
        """Helper that creates empty dict for variable info"""
        return {'type'      :   '',
                'cat'       :   '',
                'name'      :   '',
                'longname'  :   '',
                'obs'       :   {}}
        
    new = {}
    
    tab = config.get_web_overview_table()
    
    for index, info in tab.iterrows():
        (obs_name, obs_id, obs_var, 
         vert_code, 
         mod_name, mod_id, mod_var, mod_type, 
         periods) = info
        if not obs_var in new:
            const.print_log.info('Adding new observation variable: {}'
                                 .format(obs_var))
            new[obs_var] = d = var_dummy()
            name, tp, cat = config.get_obsvar_name_and_type(obs_var)
    
            d['name'] = name
            d['type'] = tp
            d['cat'] = cat
            d['longname'] = const.VARS[obs_var].description
        else:
            d = new[obs_var]
        
        if not obs_name in d['obs']:
            d['obs'][obs_name] = dobs = {}
        else:
            dobs = d['obs'][obs_name]
        
        if not vert_code in dobs:
            dobs[vert_code] = dobs_vert = dict(obs_id=obs_id,
                                               period=periods,
                                               modsat= {})
        else:
            dobs_vert = dobs[vert_code]
        if mod_name is not None:
            if mod_name in dobs_vert['modsat']:
                raise KeyError('Model {} already exists in {}. This should '
                               'not occur. please debug...'.format(mod_name, dobs))
            dobs_vert['modsat'][mod_name] = dict(var= mod_var,
                                                 mtype=mod_type,
                                                 mid=mod_id)
        
    _new = {}
    for var in config.var_order_menu:
        try:
            _new[var] = new[var]
        except:
            const.print_log.info('No variable {} found'.format(var))
    for var, info in new.items():
        if not var in _new:
            _new[var] = info
    new = _new
    if config.obs_order_menu_cfg:
        pref_obs_order = list(config.obs_config)
    else:
        pref_obs_order = []
    new_sorted = {}
    for var, info in new.items():
        new_sorted[var] = info
        sorted_obs = sort_dict_by_name(info['obs'],
                                       pref_list=pref_obs_order)
        new_sorted[var]['obs'] = sorted_obs
        for obs_name, vert_codes in sorted_obs.items():
            vert_codes_sorted = sort_dict_by_name(vert_codes)
            new_sorted[var]['obs'][obs_name] = vert_codes_sorted
            for vert_code, models in vert_codes_sorted.items():
                models_sorted = sort_dict_by_name(models)
                new_sorted[var]['obs'][obs_name][vert_code] = models_sorted
    
    with open(config.menu_file, 'w+') as f:
        f.write(simplejson.dumps(new_sorted, indent=4))
        
def make_info_table_evaluation_iface(config):
    from pyaerocom import ColocatedData
    import glob
    menu = config.menu_file
        
        
    SKIP_META = ['data_source', 'var_name', 'lon_range',
                 'lat_range', 'alt_range']
    with open(menu, 'r') as f:
        menu = simplejson.load(f)
    if not config.exp_id in menu:
        raise KeyError('No menu entry available for experiment {}'
                       .format(config.exp_id))
    table = {}
    exp = menu[config.exp_id]
    for obs_var, info in exp.items():
        for obs_name, vert_types in info['obs'].items():
            for vert_type, models in vert_types.items():
                for mname, minfo in models.items():
                    if not mname in table:
                        table[mname] = mi = {}
                        mi['id'] = model_id = minfo['id']
                    else:
                        mi = table[mname]
                        model_id = mi['id']
                        if minfo['id'] != mi['id']:
                            raise KeyError('Unexpected error: conflict in model ID and name')
                    
                    try:
                        mo = mi['obs']
                    except:
                        mi['obs'] = mo = {}
                    if 'var' in minfo:
                        mvar = minfo['var']
                    else:
                        mvar = obs_var
                    if not obs_var in mo:
                        mo[obs_var] = oi = {}
                    else: 
                        oi = mo[obs_var]
                    if obs_name in oi:
                        raise Exception
                    oi[obs_name] = motab = {}
                    motab['model_var'] = mvar
                    motab['obs_id'] = config.get_obs_id(obs_name)
                    files = glob.glob('{}/{}/{}*REF-{}*.nc'
                                      .format(config.coldata_dir, 
                                              model_id, mvar, obs_name))
                    
                    if not len(files) == 1:
                        if len(files) > 1:
                            motab['MULTIFILES'] = len(files)
                        else:
                            motab['NOFILES'] = True
                        continue
                    
                    coldata = ColocatedData(files[0])
                    for k, v in coldata.meta.items():
                        if not k in SKIP_META:
                            if isinstance(v, (list, tuple)):
                                if not len(v) == 2:
                                    raise Exception
                            
                                motab['{}_obs'.format(k)] = str(v[0])
                                motab['{}_mod'.format(k)] = str(v[1])
                            else:
                                motab[k] = str(v)
    return table

if __name__ == '__main__':
    print()
    