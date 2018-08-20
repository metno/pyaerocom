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

def plot_scatter(model_vals, obs_vals, model_id=None, var_name=None, 
                 obs_id=None, start=None, stop=None, 
                 ts_type=None, stations_ok=None, filter_name=None, 
                 statistics=None, savefig=False, save_dir=None, save_name=None,
                 add_data_missing_note=False, ax=None):
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(10,8))
    if var_name is None:
        var_name = 'n/d'
    
    if statistics is None:
        statistics = calc_statistics(model_vals, obs_vals)
    
    ax.loglog(obs_vals, model_vals, ' k+')
    
    
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
    try:
        VAR_PARAM = const.VAR_PARAM[var_name]
    except:
        VAR_PARAM = const.VAR_PARAM.DEFAULT
    ax.set_xlim(VAR_PARAM['scat_xlim'])
    ax.set_ylim(VAR_PARAM['scat_ylim'])
    ax.set_xlabel('Obs: {}'.format(obs_id), fontsize=14)
    ax.set_ylabel('{}'.format(model_id), fontsize=14)
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
    ax.annotate('Obs: {:.3f}'.format(statistics['refdata_mean']),
                        xy=xypos[xypos_index], xycoords='axes fraction', 
                        fontsize=10, color='red')
    xypos_index += 1
    ax.annotate('Mod: {:.3f}'.format(statistics['data_mean']),
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
    ax.annotate('R: {:.3f}'.format(statistics['R']),
                        xy=xypos[xypos_index], xycoords='axes fraction', 
                        fontsize=10, color='red')
    xypos_index += 1
    ax.annotate('RMS: {:.3f}'.format(statistics['rms']),
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
    if add_data_missing_note:
        ax.annotate('NO MODEL DATA',
                    xy=(0.4, 0.3), xycoords='axes fraction', ha='center', 
                    fontsize=20, color='red')
    ax.set_aspect('equal')
    
    if savefig:
        if any([x is None for x in (save_dir, save_name)]):
            raise IOError
            
        fig.savefig(os.path.join(save_dir, save_name))
    return ax
    

