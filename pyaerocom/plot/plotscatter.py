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
from pyaerocom.helpers import start_stop_str
from pyaerocom.mathutils import calc_statistics, exponent

def plot_scatter(x_vals, y_vals, **kwargs):
    """Scatter plot

    Currently a wrapper for high-level method plot_scatter_aerocom (same module,
    see there for details)
    """
    return plot_scatter_aerocom(x_vals, y_vals, **kwargs)

def plot_scatter_aerocom(x_vals, y_vals, var_name=None, var_name_ref=None,
                         x_name=None, y_name=None, start=None, stop=None,
                         ts_type=None, unit=None, stations_ok=None,
                         filter_name=None, lowlim_stats=None,
                         highlim_stats=None, loglog=None, ax=None, figsize=None,
                         fontsize_base=11, fontsize_annot=None,
                         marker='+', color='k', alpha=0.5,
                         **kwargs):
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

    Returns
    -------
    matplotlib.axes.Axes
        plot axes
    """

    if isinstance(y_vals, list):
        y_vals = np.asarray(y_vals)
    if isinstance(x_vals, list):
        x_vals = np.asarray(x_vals)
    try:
        var = const.VARS[var_name]
    except Exception:
        var = const.VARS.DEFAULT

    try:
        var_ref = const.VARS[var_name_ref]
    except Exception:
        var_ref = const.VARS.DEFAULT

    if loglog is None:
        loglog = var_ref.scat_loglog

    xlim = var['scat_xlim']
    ylim = var_ref['scat_ylim']

    if xlim is None or ylim is None:
        low  =  np.min([np.nanmin(x_vals), np.nanmin(y_vals)])
        high =  np.max([np.nanmax(x_vals), np.nanmax(y_vals)])

        xlim = [low, high]
        ylim = [low, high]

    if ax is None:
        if figsize is None:
            figsize = (10,8)
        fig, ax = plt.subplots(figsize=figsize)
    if var_name is None:
        var_name = 'n/d'

    statistics = calc_statistics(y_vals, x_vals,
                                 lowlim_stats, highlim_stats)

    if loglog:
        ax.loglog(x_vals, y_vals, ls='none', color=color, marker=marker,
                  alpha=alpha, **kwargs)
    else:
        ax.plot(x_vals, y_vals, ls='none', color=color, marker=marker,
                  alpha=alpha, **kwargs)

    try:
        title = start_stop_str(start, stop, ts_type)
        if ts_type is not None:
            title += ' ({})'.format(ts_type)
    except Exception:
        title = ''

    if not loglog:
        xlim[0] = 0
        ylim[0] = 0
    elif any(x[0] < 0 for x in [xlim, ylim]):
        low = np.nanmin(y_vals)
        if low != 0:
            low = 10**(float(exponent(abs(low)) - 1))
        xlim[0] = low
        ylim[0] = low
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    xlbl = '{}'.format(x_name)
    if var_name_ref is not None:
        xlbl += ' ({})'.format(var_name_ref)
    ax.set_xlabel(xlbl, fontsize=fontsize_base+4)
    ax.set_ylabel('{}'.format(y_name), fontsize=fontsize_base+4)

    ax.set_title(title, fontsize=fontsize_base+4)

    ax.tick_params(labelsize=fontsize_base)

    ax.plot(xlim, ylim, '--', color='#cccccc')

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

    var_str = var_name
    _ndig = abs(exponent(statistics['refdata_mean']) - 2)
    if unit is None:
        unit = 'N/D'
    if not str(unit) in ['1', 'no_unit']:
        var_str += ' [{}]'.format(unit)

    if fontsize_annot is None:
        fontsize_annot = fontsize_base
    ax.annotate("{} #: {} # st: {}".format(var_str,
                        statistics['num_valid'], stations_ok),
                        xy=xypos['var_info'], xycoords='axes fraction',
                        fontsize=fontsize_annot+4, color='red')

    ax.annotate('Mean (x-data): {:.{}f}; Rng: [{:.{}f}, {:.{}f}]'
                .format(statistics['refdata_mean'], _ndig,
                        np.nanmin(x_vals),_ndig,
                        np.nanmax(x_vals), _ndig),
                xy=xypos['refdata_mean'], xycoords='axes fraction',
                fontsize=fontsize_annot,
                color='red')

    ax.annotate('Mean (y-data): {:.{}f}; Rng: [{:.{}f}, {:.{}f}]'
                .format(statistics['data_mean'], _ndig,
                        np.nanmin(y_vals),_ndig,
                        np.nanmax(y_vals), _ndig),
                xy=xypos['data_mean'], xycoords='axes fraction',
                fontsize=fontsize_annot,
                color='red')

    ax.annotate('NMB: {:.1f}%'.format(statistics['nmb']*100),
                        xy=xypos['nmb'], xycoords='axes fraction',
                        fontsize=fontsize_annot, color='red')

    ax.annotate('MNMB: {:.1f}%'.format(statistics['mnmb']*100),
                        xy=xypos['mnmb'], xycoords='axes fraction',
                        fontsize=fontsize_annot, color='red')

    ax.annotate('R (Pearson): {:.3f}'.format(statistics['R']),
                        xy=xypos['R'], xycoords='axes fraction',
                        fontsize=fontsize_annot, color='red')

    ax.annotate('RMS: {:.3f}'.format(statistics['rms']),
                        xy=xypos['rms'], xycoords='axes fraction',
                        fontsize=fontsize_annot, color='red')

    ax.annotate('R (Kendall): {:.3f}'.format(statistics['R_kendall']),
                        xy=xypos['R_kendall'], xycoords='axes fraction',
                        fontsize=fontsize_annot, color='red')

    ax.annotate('FGE: {:.1f}'.format(statistics['fge']),
                        xy=xypos['fge'], xycoords='axes fraction',
                        fontsize=fontsize_annot, color='red')
    # right lower part
    ax.annotate('{}'.format(ts_type),
                        xy=xypos['ts_type'], xycoords='axes fraction',
                        ha='center',
                        fontsize=fontsize_annot, color='black')
    ax.annotate('{}'.format(filter_name),
                        xy=xypos['filter_name'], xycoords='axes fraction',
                        ha='center',
                        fontsize=fontsize_annot, color='black')

    ax.set_aspect('equal')
    return ax
