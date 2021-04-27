#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:00:44 2019
"""
import os, glob, shutil
import simplejson
from pyaerocom import const
from pyaerocom.helpers import start_stop_str
from pyaerocom._lowlevel_helpers import sort_dict_by_name
from pyaerocom.web.helpers import read_json, write_json
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.colocation_auto import Colocator
from pyaerocom.tstype import TsType
from pyaerocom.exceptions import TemporalResolutionError

def heatmap_filename(ts_type):
    return 'glob_stats_{ts_type}.json'

def make_info_str_eval_setup(stp, add_header=True):
    """
    Convert instance of :class:`AerocomEvaluation` into a descriptive string

    Note
    ----
    UNDER DEVELOPMENT -> this might crash!!

    Parameters
    ----------
    stp : AerocomEvaluation
        Instance of configuration class

    Returns
    -------
    str
        Long string representation of the input configuration.

    """
    modelnum = len(stp.model_config)
    obsnum = len(stp.obs_config)
    varnum = len(stp.all_obs_vars)
    colstp = stp.colocation_settings

    if modelnum > 0:

        _modpost = 'model' if modelnum==1 else 'models'
        modstr = f'the following {modelnum} {_modpost}: '
        for mod in stp.model_config:
            modstr += f'{mod}, '

        modstr = modstr[:-2]
        modstr += '. '
    else:
        modstr = '0 models. '
    obsvarstr = ''
    if obsnum > 0:
        obsvarstr += 'These are: '
        for oname, ocfg in stp.obs_config.items():
            obsvarstr += f'{oname} ('
            for var in ocfg['obs_vars']:
                obsvarstr += f'{var}, '
            obsvarstr = obsvarstr[:-2]
            obsvarstr += '), '
        obsvarstr = obsvarstr[:-2]
        obsvarstr += '. '

    obs_alt_time = []
    try:
        startstop = start_stop_str(colstp.start,
                                   colstp.stop)

        obs_alt_time.append(startstop)

        timeinfo = (f'The evaluation is done for the following time '
                    f'interval: {startstop}. ')
    except ValueError:
        # no start / stop time specified
        timeinfo = (
            'No specific time interval is specified for the analysis. Thus, '
            'the interval is determined for each model and observation dataset '
            '(and variable) individually, based on data availability. '
            )

    try:
        freq = str(TsType(colstp.ts_type))
        flexfreq = colstp.flex_ts_type_gridded
        freqinfo = f'The default colocation frequency is {freq}'
        if flexfreq:
            freqinfo += (
                ', however, this requirement is flexible, that is, if a model '
                '(or obs) is available in lower resolution it will still be '
                'colocated, but then the computed statistics are only available '
                'in that resolution. ')
        else:
            freqinfo += '. '

    except TemporalResolutionError:
        freqinfo = (
        'The analysis is performed in the highest available '
        'resolution. '
        )

    freqinfo += (
        'Note, however, that the minimum required resolution for the analysis '
        'is monthly.'
        )


    obsaltinfo = {}
    for oname, ocfg in stp.obs_config.items():
        col = Colocator(**colstp)
        col.update(**ocfg)
        tst = start_stop_str(col.start,
                             col.stop)
        if not tst in obs_alt_time:
            obs_alt_time.append(tst)

    st = (
        f'The experiment contains {modstr}'
        f'These models are evaluated against {obsnum} observational '
        f'dataset(s) and a total of {varnum} variables. '
        f'{obsvarstr}{timeinfo}{freqinfo}')
    if add_header:
        st =  f'{stp.exp_id}: {stp.exp_name}\n{stp.exp_descr}\n' + st
    return st

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

    basedir = os.path.join(base_dir, proj_id, exp_id)
    if not os.path.exists(basedir):
        const.print_log.info('Nothing there to delete...')
        return
    const.print_log.info(f'Deleting everything under {basedir}')
    shutil.rmtree(basedir)

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
            const.logger.warning('Invalid config file name ', file)
            continue
        proj, exp = spl[1], spl[2].split('.')[0]
        if not proj in results:
            results[proj] = {}
        results[proj][exp] = file
    return results

def reorder_experiments_menu_evaluation_iface(menu_file, exp_order=None):
    """Reorder experiment order in evaluation interface

    Puts experiment list into order as specified by `exp_order`, all
    remaining experiments are sorted alphabetically.

    Parameters
    ----------
    menu_file : str
        file path of menu.json file
    exp_order : str or list, optional
        desired experiment order (must not contain all available experiments
        in menu)
    """
    current = read_json(menu_file)
    if exp_order is None:
        exp_order = []
    elif isinstance(exp_order, str):
        exp_order = [exp_order]
    if not isinstance(exp_order, list):
        raise ValueError('Invalid input for exp_order, need None, str or list')

    new = sort_dict_by_name(current, pref_list=exp_order)
    write_json(new, menu_file, indent=4)

def _get_available_results_dict(config):
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
        obs_var, obs_name, vert_code, mod_name, mod_var = info
        if not obs_var in new:
            new[obs_var] = d = var_dummy()
            name, tp, cat = config.get_obsvar_name_and_type(obs_var)

            d['name'] = name
            d['type'] = tp
            d['cat']  = cat
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
            const.print_log.warning('Overwriting old entry for {}: {}'
                                    .format(mod_name, dobs_vert[mod_name]))
        dobs_vert[mod_name] = {'dir' : mod_name,
                               'id'  : config.model_config[mod_name]['model_id'],
                               'var' : mod_var}
    return new

def _sort_menu_entries(avail, config):
    """
    Used in method :func:`update_menu_evaluation_iface`

    Sorts results of different menu entries (i.e. variables, observations
    and models).

    Parameters
    ----------
    avail : dict
        nested dictionary contining info about available results
    config : AerocomEvaluation
        Configuration class

    Returns
    -------
    dict
        input dictionary sorted in variable, obs and model layers. The order
        of variables, observations and models may be specified in
        AerocomEvaluation class and if not, alphabetic order is used.

    """
    # sort first layer (i.e. variables)
    avail = sort_dict_by_name(avail, pref_list=config.var_order_menu)

    new_sorted = {}
    for var, info in avail.items():
        new_sorted[var] = info
        obs_order = config.obs_order_menu
        sorted_obs = sort_dict_by_name(info['obs'],
                                       pref_list=obs_order)
        new_sorted[var]['obs'] = sorted_obs
        for obs_name, vert_codes in sorted_obs.items():
            vert_codes_sorted = sort_dict_by_name(vert_codes)
            new_sorted[var]['obs'][obs_name] = vert_codes_sorted
            for vert_code, models in vert_codes_sorted.items():
                model_order = config.model_order_menu
                models_sorted = sort_dict_by_name(models,
                                                  pref_list=model_order)
                new_sorted[var]['obs'][obs_name][vert_code] = models_sorted
    return new_sorted

def _check_load_current_menu(config, ignore_experiments):
    """
    Load current menu.json file and return as dictionary

    This is a private method used in :func:`update_menu_evaluation_iface`. It
    also checks for outdated experiments for which no json files are
    available anymore.

    Parameters
    ----------
    config : AerocomEvaluation
        instance of config class that has all relevant paths specified
    ignore_experiments : list, optional
        list of experiments that are supposed to be removed from the current
        menu.

    Returns
    -------
    dict
        current menu as dictionary (cleared of outdated entries)


    """
    if ignore_experiments is None:
        ignore_experiments = []
    menu_file = config.menu_file
    # toplevel directory under which all experiments for this project are
    # stored. the menu.json is in there and contains all available experiments
    # in addition to the on that is updated here.
    basedir = os.path.dirname(menu_file)

    # list of available experiments (sub directories in basedir)
    available_exps = os.listdir(basedir)
    menu = {}
    if os.path.exists(menu_file):
        current = read_json(menu_file)
        for exp, submenu in current.items():
            if exp in ignore_experiments or len(submenu) == 0:
                continue
            elif not exp in available_exps:
                const.print_log.info('Removing outdated experiment {} from '
                                     'menu.json'.format(exp))
                continue
            menu[exp] = submenu

    if config.exp_id in menu:
        const.print_log.warning('Sub menu for experiment {} already exists in '
                                'menu.json and will be overwritten'
                                .format(config.exp_id))
    return menu

def update_menu_evaluation_iface(config, ignore_experiments=None,
                                 delete_mode=False):
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
    delete_mode : bool
        if True, then no attempts are being made to find json files for the
        experiment specified in `config`.

    """
    avail = {}
    if not delete_mode:
        try:
            avail.update(**_get_available_results_dict(config))
        except FileNotFoundError:
            pass


    avail = _sort_menu_entries(avail, config)

    menu = _check_load_current_menu(config, ignore_experiments)
    if len(avail) > 0:
        menu[config.exp_id] = avail

    with open(config.menu_file, 'w+') as f:
        f.write(simplejson.dumps(menu, indent=4))

def make_info_table_evaluation_iface(config):
    """
    Make an information table for an web experiment based on available results

    Parameters
    ----------
    config : AerocomEvaluation
        instance of evaluation class for the experiment

    Returns
    -------
    dict
        dictionary containing meta information

    """
    import glob
    menu = config.menu_file

    SKIP_META = ['data_source', 'var_name', 'lon_range',
                 'lat_range', 'alt_range']
    with open(menu, 'r') as f:
        menu = simplejson.load(f)
    if not config.exp_id in menu:
        raise KeyError(f'No menu entry available for experiment {config.exp_id}')
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
                    except Exception:
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
                    for k, v in coldata.metadata.items():
                        if not k in SKIP_META:
                            if isinstance(v, (list, tuple)):
                                if len(v) == 2:
                                    motab['{}_obs'.format(k)] = str(v[0])
                                    motab['{}_mod'.format(k)] = str(v[1])
                                else:
                                    motab[k] = ';'.join([str(x) for x in v])
                            else:
                                motab[k] = str(v)
    return table