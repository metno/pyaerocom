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

def plot_scatter(x_vals, y_vals, var_name=None, x_name=None, y_name=None,
                 start=None, stop=None, ts_type=None, stations_ok=None, 
                 filter_name=None, lowlim_stats=None, highlim_stats=None, 
                 loglog=True, savefig=False, save_dir=None, save_name=None, 
                 ax=None):
    """Method that performs a scatter plot of data in AEROCOM format
    
    Parameters
    ----------
    y_vals : ndarray
        1D array (or list) of model data points (y-axis)
    x_vals : ndarray
        1D array (or list) of observation data points (x-axis)
    y_name : :obj:`str`, optional
        Name / ID of model
    var_name : :obj:`str`, optional
        name of variable that is plotted
    x_name : :obj:`str`, optional
        Name of observation network
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
        fig, ax = plt.subplots(figsize=(10,8))
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
    ax.set_xlabel('{}'.format(x_name), fontsize=14)
    ax.set_ylabel('{}'.format(y_name), fontsize=14)
    ax.set_title('{} - {} ({})'.format(start_str, stop_str, ts_type))
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_major_formatter(ScalarFormatter())
    
    plt.plot(VAR_PARAM['scat_xlim'], VAR_PARAM['scat_ylim'], '-', 
             color='grey')
    
    # text positions for the scatter plot annotations
    xypos=[]
    xypos.append((.01, 0.95))
    xypos.append((0.01, 0.90))
    xypos.append((0.3, 0.90))
    xypos.append((0.01, 0.86))
    xypos.append((0.3, 0.86))
    xypos.append((0.01, 0.82))
    xypos.append((0.3, 0.82))
    xypos.append((0.01, 0.78))
    xypos.append((0.3, 0.78))
    xypos.append((0.8, 0.1))
    xypos.append((0.8, 0.06))
    xypos_index = 0
    
    var_str = var_name + VAR_PARAM.unit_str

    ax.annotate("{} #: {} # st: {}".format(var_str, 
                        statistics['success'], stations_ok),
                        xy=xypos[xypos_index], xycoords='axes fraction', 
                        fontsize=14, color='red')
    xypos_index += 1
    ax.annotate('Mean (x-data): {:.3f}'.format(statistics['refdata_mean']),
                        xy=xypos[xypos_index], xycoords='axes fraction', 
                        fontsize=10, color='red')
    xypos_index += 1
    ax.annotate('Mean (y-data): {:.3f}'.format(statistics['data_mean']),
                        xy=xypos[xypos_index], xycoords='axes fraction', 
                        fontsize=10, color='red')
    xypos_index += 1
    ax.annotate('NMB: {:.1f}%'.format(statistics['nmb']),
                        xy=xypos[xypos_index], xycoords='axes fraction', 
                        fontsize=10, color='red')
    xypos_index += 1
    ax.annotate('MNMB: {:.1f}%'.format(statistics['mnmb']),
                        xy=xypos[xypos_index], xycoords='axes fraction', 
                        fontsize=10, color='red')
    xypos_index += 1
    ax.annotate('R (Pearson): {:.3f}'.format(statistics['R']),
                        xy=xypos[xypos_index], xycoords='axes fraction', 
                        fontsize=10, color='red')
    xypos_index += 1
    ax.annotate('RMS: {:.3f}'.format(statistics['rms']),
                        xy=xypos[xypos_index], xycoords='axes fraction', 
                        fontsize=10, color='red')
    xypos_index += 1
    ax.annotate('R (Kendall): {:.3f}%'.format(statistics['R_kendall']),
                        xy=xypos[xypos_index], xycoords='axes fraction', 
                        fontsize=10, color='red')
    
    xypos_index += 1
    ax.annotate('FGE: {:.1f}%'.format(statistics['fge']),
                        xy=xypos[xypos_index], xycoords='axes fraction', 
                        fontsize=10, color='red')
    # right lower part
    ax.annotate('{}'.format(ts_type),
                        xy=xypos[-2], xycoords='axes fraction', 
                        ha='center', 
                        fontsize=10, color='black')
    ax.annotate('{}'.format(filter_name),
                        xy=xypos[-1], xycoords='axes fraction', ha='center', 
                        fontsize=10, color='black')
    
    ax.set_aspect('equal')
    
    if savefig:
        if any([x is None for x in (save_dir, save_name)]):
            raise IOError
            
        fig.savefig(os.path.join(save_dir, save_name))
    return ax
    

