#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:00:44 2019
"""
import os, glob, shutil
from pyaerocom import const
from pyaerocom.helpers import start_stop_str
from pyaerocom._lowlevel_helpers import sort_dict_by_name
from pyaerocom.web.helpers import read_json, write_json
from pyaerocom.colocation_auto import Colocator
from pyaerocom.tstype import TsType
from pyaerocom.exceptions import TemporalResolutionError

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

