#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:00:44 2019
"""
import os, glob
import simplejson
from pyaerocom import const
from pyaerocom._lowlevel_helpers import sort_dict_by_name

from warnings import warn

const.print_log.warning(DeprecationWarning(
    'Module pyaerocom/web/helpers_trends_interface.py will be removed as of '
    'release 0.12.0 which will incorporate trends computation in AeroVal '
    'interface (via AerocomEvaluation class)'))

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
        except Exception:
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

if __name__ == '__main__':
    print()
