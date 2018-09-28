#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains scatter plot routines for Aerocom data.
"""
from matplotlib.ticker import ScalarFormatter
import os
import matplotlib.pyplot as plt
import numpy as np
from pyaerocom import const
from pyaerocom.helpers import to_pandas_timestamp, TS_TYPE_TO_NUMPY_FREQ
from pyaerocom.mathutils import calc_statistics

def plot_scatter(x_vals, y_vals, var_name=None, var_name_ref=None, 
                 x_name=None, y_name=None, start=None, stop=None, ts_type=None, 
                 unit=None,stations_ok=None, 
                 filter_name=None, lowlim_stats=None, highlim_stats=None, 
                 loglog=True, savefig=False, save_dir=None, save_name=None, 
                 ax=None, figsize=None):
    """Method that performs a scatter plot of data in AEROCOM format
    
    Parameters
    ----------
    y_vals : ndarray
        1D array (or list) of model data points (y-axis)
    x_vals : ndarray
        1D array (or list) of observation data points (x-axis)
    var_name : :obj:`str`, optional
        name of variable that is plotted
    var_name_ref : :obj:`str`, optional
        name of variable of reference data
    x_name : :obj:`str`, optional
        Name of observation network
    y_name : :obj:`str`, optional
        Name / ID of model
    start : :obj:`str` or :obj`datetime` or similar
        start time of data
    stop : :obj:`str` or :obj`datetime` or similar
        stop time of data
    
    
    """
    
    if isinstance(y_vals, list):
        y_vals = np.asarray(y_vals)
    if isinstance(x_vals, list):
        x_vals = np.asarray(x_vals)
    try:
        VAR_PARAM = const.VAR_PARAM[var_name]
    except:
        VAR_PARAM = const.VAR_PARAM.DEFAULT
    xlim = VAR_PARAM['scat_xlim']
    ylim = VAR_PARAM['scat_ylim'] 
    if ax is None:
        if figsize is None:
            figsize = (10,8)
        fig, ax = plt.subplots(figsize=figsize)
    if var_name is None:
        var_name = 'n/d'

    
    statistics = calc_statistics(y_vals, x_vals,
                                 lowlim_stats, highlim_stats)
    
    if loglog:
        ax.loglog(x_vals, y_vals, ' k+')
    else:
        ax.plot(x_vals, y_vals, ' k+')
    
    try:
        freq_np =TS_TYPE_TO_NUMPY_FREQ[ts_type]
    except:
        freq_np = 'n/d'
    try:
        start, stop = to_pandas_timestamp(start), to_pandas_timestamp(stop)
        start_str = np.datetime64(start).astype('datetime64[{}]'.format(freq_np))
        stop_str = np.datetime64(stop).astype('datetime64[{}]'.format(freq_np))
    except:
        start_str = 'n/d'
        stop_str = 'n/d'
    
    if not loglog:
        xlim[0] = 0
        ylim[0] = 0
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    xlbl = '{}'.format(x_name)
    if var_name_ref is not None:
        xlbl += ' ({})'.format(var_name_ref)
    ax.set_xlabel(xlbl, fontsize=14)
    ax.set_ylabel('{}'.format(y_name), fontsize=14)
    if ts_type == 'yearly':
        ax.set_title(start.year)
    else:
        ax.set_title('{} - {} ({})'.format(start_str, stop_str, ts_type))
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_major_formatter(ScalarFormatter())
    
    plt.plot(VAR_PARAM['scat_xlim'], VAR_PARAM['scat_ylim'], '-', 
             color='grey')
    
    xypos =   {'var_info'       :   (0.01, .95),
               'refdata_mean'   :   (0.01, 0.90),
               'data_mean'      :   (0.01, 0.86),
               'nmb'            :   (0.01, 0.82),
               'mnmb'           :   (0.35, 0.82),
               'R'              :   (0.01, 0.78),
               'rms'            :   (0.35, 0.78),
               'R_kendall'      :   (0.01, 0.74),
               'fge'            :   (0.35, 0.74),
               'ts_type'        :   (0.8, 0.1),
               'filter_name'    :   (0.8, 0.06)}
    
    var_str = var_name# + VAR_PARAM.unit_str

    if unit is not None and unit != 1:
        var_str += ' [{}]'.format(unit)

    ax.annotate("{} #: {} # st: {}".format(var_str, 
                        statistics['success'], stations_ok),
                        xy=xypos['var_info'], xycoords='axes fraction', 
                        fontsize=14, color='red')

    ax.annotate('Mean (x-data): {:.3f}'.format(statistics['refdata_mean']),
                        xy=xypos['refdata_mean'], xycoords='axes fraction', 
                        fontsize=10, color='red')
    
    ax.annotate('Mean (y-data): {:.3f}'.format(statistics['data_mean']),
                        xy=xypos['data_mean'], xycoords='axes fraction', 
                        fontsize=10, color='red')
    
    ax.annotate('NMB: {:.1f}%'.format(statistics['nmb']),
                        xy=xypos['nmb'], xycoords='axes fraction', 
                        fontsize=10, color='red')
    
    ax.annotate('MNMB: {:.1f}%'.format(statistics['mnmb']),
                        xy=xypos['mnmb'], xycoords='axes fraction', 
                        fontsize=10, color='red')
    
    ax.annotate('R (Pearson): {:.3f}'.format(statistics['R']),
                        xy=xypos['R'], xycoords='axes fraction', 
                        fontsize=10, color='red')

    ax.annotate('RMS: {:.3f}'.format(statistics['rms']),
                        xy=xypos['rms'], xycoords='axes fraction', 
                        fontsize=10, color='red')
    
    ax.annotate('R (Kendall): {:.3f}%'.format(statistics['R_kendall']),
                        xy=xypos['R_kendall'], xycoords='axes fraction', 
                        fontsize=10, color='red')
    
    
    ax.annotate('FGE: {:.1f}%'.format(statistics['fge']),
                        xy=xypos['fge'], xycoords='axes fraction', 
                        fontsize=10, color='red')
    # right lower part
    ax.annotate('{}'.format(ts_type),
                        xy=xypos['ts_type'], xycoords='axes fraction', 
                        ha='center', 
                        fontsize=10, color='black')
    ax.annotate('{}'.format(filter_name),
                        xy=xypos['filter_name'], xycoords='axes fraction', ha='center', 
                        fontsize=10, color='black')
    
    ax.set_aspect('equal')
    
    if savefig:
        if any([x is None for x in (save_dir, save_name)]):
            raise IOError
            
        fig.savefig(os.path.join(save_dir, save_name))
    return ax
    

