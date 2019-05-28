#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:00:44 2019

@author: jonasg
"""
import os, glob
import simplejson
from pyaerocom import const
from pyaerocom._lowlevel_helpers import BrowseDict, sort_dict_by_name

def get_all_config_files(config_dir):
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
        print(spl)
        proj, exp = spl[1], spl[2].split('.')[0]
        if not proj in results:
            results[proj] = {}
        results[proj][exp] = file
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
    SUPPORTED_VERT_CODES = ['Column', 'ModelLevel', 'Surface']
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
        if self.obs_vert_type is None:
            raise ValueError('obs_vert_type is not defined. Please specify '
                             'using either of the available codes: {}. '
                             'It may be specified for all variables (as string) '
                             'or per variable using a dict'
                             .format(self.SUPPORTED_VERT_CODES))
            if (isinstance(self.obs_vert_type, str) and 
                not self.obs_vert_type in self.SUPPORTED_VERT_CODES):
                    raise ValueError('Invalid value for obs_vert_type: {}. '
                                     'Supported codes are {}.'
                                     .format(self.obs_vert_type,
                                             self.SUPPORTED_VERT_CODES))
            elif isinstance(self.obs_vert_type, dict):
                for var_name, val in self.obs_vert_type.items():
                    if not val in self.SUPPORTED_VERT_CODES:
                        raise ValueError('Invalid value for obs_vert_type: {} '
                                         '(variable {}). Supported codes are {}.'
                                         .format(self.obs_vert_type,
                                                 var_name,
                                                 self.SUPPORTED_VERT_CODES))
                        
                
        
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
            
def update_menu(config, ignore_experiments=None):
    """Include experiment into menu.json file for web menu
    
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
                'name'      :   '',
                'longname'  :   '',
                'obs'       :   {}}
        
    new = {}
    if ignore_experiments is None:
        ignore_experiments = []
    tab = config.get_web_overview_table()
    
    for index, info in tab.iterrows():
        obs_var, obs_name, vert_code, mod_name, mod_var = info
        if not obs_var in new:
            const.print_log.info('Adding new observation variable: {}'
                                 .format(obs_var))
            new[obs_var] = d = var_dummy()
            name, tp = config.get_obsvar_name_and_type(obs_var)
    
            d['name'] = name
            d['type'] = tp
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
    if os.path.exists(config.menu_file):
        with open(config.menu_file, 'r') as f:
            current = simplejson.load(f)
        for exp, submenu in current.items():
            if exp in ignore_experiments:
                continue
            new_menu[exp] = submenu
    
    if config.exp_id in new_menu:
        const.print_log.warning('Sub menu for experiment {} already exists in '
                                'menu.json and will be overwritten'
                                .format(config.exp_id))
    
    new_menu[config.exp_id] = new_sorted
    
    with open(config.menu_file, 'w+') as f:
        f.write(simplejson.dumps(new_menu, indent=4))
        
def make_info_table(config):
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
                    motab['obs_id'] = obs_id = config.get_obs_id(obs_name)
                    files = glob.glob('{}/{}/{}*REF-{}*.nc'
                                      .format(config.coldata_dir, 
                                              model_id, mvar, obs_id))
                    file = None
                    if len(files) == 1:
                        file = files[0]
                    else: 
                        if len(files) > 1:
                            motab['MULTIFILES'] = len(files)
                        else:
                            raise Exception('No colocated data file found...')
                    if file is not None:
                        coldata = ColocatedData(file)
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
    cfg_dir = '/home/jonasg/github/aerocom_evaluation/data_new/config_files/'
    
    results = get_all_config_files(cfg_dir)
    
    for proj, exps in results.items():
        print('Project:', proj)
        for exp, path in exps.items():
            print('Exp.', exp, ':', path)