#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:00:44 2019

TO BE DELETED
"""
import os, glob

from pyaerocom import const
from pyaerocom.helpers import start_stop_str
from pyaerocom._lowlevel_helpers import sort_dict_by_name, read_json, write_json
from pyaerocom.colocation_auto import Colocator
from pyaerocom.tstype import TsType
from pyaerocom.exceptions import TemporalResolutionError

# ToDo: rewrite or delete before v0.12.0
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
    raise NotImplementedError('Under revision')
    modelnum = len(stp.model_config)
    obsnum = len(stp.obs_config)
    varnum = len(stp.all_obs_vars)
    colstp = stp.colocation_opts

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
        flexfreq = colstp.flex_ts_type
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

# ToDo: rewrite or delete before v0.12.0
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

# ToDo: rewrite or delete before v0.12.0
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

def _check_statistics_periods(periods: list) -> list:
    """
    Check input list of period strings is valid

    Parameters
    ----------
    periods : list
        list containing period strings to be checked.

    Raises
    ------
    ValueError
        if input is not a list or any of the provided periods in that list is
        not a string or invalid.

    Returns
    -------
    list
        list of periods

    """
    checked = []
    if not isinstance(periods, list):
        raise ValueError('statistics_periods needs to be a list')
    for per in periods:
        if not isinstance(per, str):
            raise ValueError('All periods need to be strings')
        spl = [x.strip() for x in per.split('-')]
        if len(spl) > 2:
            raise ValueError(
                f'Invalid value for period ({per}), can be either single '
                f'years or period of years (e.g. 2000-2010).'
                )
        _per = '-'.join([str(int(val)) for val in spl])
        checked.append(_per)
    return checked

def _period_str_to_timeslice(period: str) -> slice:
    """
    Convert input period to a time slice

    Parameters
    ----------
    period : str
        period, e.g. "2000-2010"

    Raises
    ------
    ValueError
        if input period is invalid

    Returns
    -------
    slice
        slice containing start and end strings.
    """
    spl = period.split('-')
    if len(spl) == 1:
        return slice(spl[0],spl[0])
    elif len(spl) == 2:
        return slice(*spl)
    raise ValueError(period)

def _get_min_max_year_periods(statistics_periods):
    """Get lowest and highest available year from all periods

    Parameters
    ----------
    statistics_periods : list
        list of periods for experiment

    Returns
    -------
    int
        start year
    int
        stop year (may be the same as start year, e.g. if periods suggest
        single year analysis).
    """
    startyr, stopyr = 1e6, -1e6
    for per in statistics_periods:
        sl = _period_str_to_timeslice(per)
        perstart, perstop = int(sl.start), int(sl.stop)
        if perstart < startyr:
            startyr = perstart
        if perstop > stopyr:
            stopyr = perstop
    return startyr, stopyr