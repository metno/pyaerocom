#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 10:49:29 2018

@author: jonasg
"""
import matplotlib.pyplot as plt
import os
import matplotlib.dates as dates

def plot_series_year(obs_data, model_data, var_name, savefig=True,
                     save_dir=None):
    """Plot one year time series overlay of model and station data

    Creates default plot of Aerocom time series overlay (see e.g. `here
    <http://aerocom.met.no/DATA/SURFOBS/TM5_AP3-CTRL2016/plots/
    OD550_AER_an2010_mALLYEAR_ARMDarwin_SERIES_AERONETSun2.0.ps.png>`__ for
    an example)

    Note
    ----
    This is a beta version and thus, might undergo major changes

    Todo
    ----
    - Review y axis limits (default variable info)
    - Check date and time formatting

    Parameters
    ----------
    obs_data : :obj:`StationData`
        dictionary containing station meta info and data
    model_data : :obj:`dict`
        dictionary containing model meta info and data at location of obs
        station
    var_name : str
        variable name

    Returns
    -------
    axes
        matplotlib axes instance

    Raises
    ------
    IOError
        if variable data is not available in input model or obsdata
    """
    if not var_name in model_data:
        raise IOError('Missing {} in model data'.format(var_name))
    elif not var_name in obs_data:
        raise IOError('Missing {} in station data'.format(var_name))

    fig = plt.figure(figsize=(12,8))
    ax = fig.add_axes([0.1, 0.1, 0.85, 0.8])

    mseries = model_data[var_name]
    oseries = obs_data[var_name]
    idx = mseries.index

    #ax.plot()

    ax.plot_date(idx.to_pydatetime(), mseries, 'rs--',
                 markersize=8, markerfacecolor='none')
    ax.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15,
                                                  interval=1))

    ax.xaxis.set_minor_formatter(dates.DateFormatter('%b'))
    ax.xaxis.grid(True, which="minor")
    ax.yaxis.grid()
    ax.xaxis.set_major_locator(dates.YearLocator(month=6, day=15))
    ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n%Y'))

    ax.plot(oseries, '-vb', markersize=8, markerfacecolor='none')
    ylim = ax.get_ylim()
    # add some space for printing legend
    ax.set_ylim([0, ylim[1]*1.1])
    ax.set_ylabel(var_name)
    ax.annotate('source: AEROCOM', xy=(0.95, 0.025),
                xycoords='figure fraction',
                horizontalalignment='right',
                verticalalignment='center',
                fontsize=10,
                bbox=dict(boxstyle='square', facecolor='none',
                          edgecolor='black'))

    ax.annotate('Obs: {}'.format(obs_data['data_id']),
                xy=(0.97, 0.1),
                xycoords='figure fraction',
                rotation='vertical',
                horizontalalignment='right',
                verticalalignment='bottom',
                fontsize=10)

    ax.annotate('PI: {}'.format(obs_data['PI']),
                xy=(0.985, 0.1),
                xycoords='figure fraction',
                rotation='vertical',
                horizontalalignment='right',
                verticalalignment='bottom',
                fontsize=10)

    ax.annotate(model_data['name'], xy=(0.105, 0.89),
                xycoords='figure fraction',
                horizontalalignment='left',
                verticalalignment='top',
                fontsize=16,
                color='r')

    ax.annotate('Obs: {}'.format(obs_data['data_id']),
                xy=(0.945, 0.89),
                xycoords='figure fraction',
                horizontalalignment='right',
                verticalalignment='top',
                fontsize=16,
                color='b')

    ax.set_title('{} ({:.2f}; {:.2f}; {:.0f}m)'
                 .format(obs_data['station_name'],
                         obs_data['latitude'],
                         obs_data['longitude'],
                         obs_data['altitude']))

    if savefig:
        if not os.path.exists(save_dir):
            raise IOError('Ouptut directory {} does not exist'.format(save_dir))

        name = '{}_an{}_freq{}_{}_SERIES_{}.png'.format(var_name,
                                                          idx[0].year,
                                                          idx.freqstr,
                                                          obs_data['station_name'],
                                                          obs_data['data_id'])
        fig.savefig(os.path.join(save_dir, name))

    return ax
