#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains scatter plot routines for Aerocom data.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyaerocom import const, logger, change_verbosity

# text positions for the annotations
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

def plotscatter(model_name, model_data=None, obs_data=None, opts=None,
                verbose=True):
    """Method to plot scatterplots

    Todo
    ----

    Complete docstring, review code

    """
    if verbose:
        change_verbosity(new_level='debug')

    plt_name = 'SCATTERLOG'
    var_to_run = opts['VariablesToRun'][0]

    # global settings (including plot settings) for variable
    VARS = const.VARS[var_to_run]

    obs_network_name = opts['ObsNetworkName'][0]
    obs_data_as_series = obs_data.to_timeseries(start_date=opts['StartDate'],
                                                end_date=opts['EndDate'],
                                                freq='D')
    obs_lats = [obs_data_as_series[i]['latitude'] for i in range(len(obs_data_as_series))]
    obs_lons = [obs_data_as_series[i]['longitude'] for i in range(len(obs_data_as_series))]
    obs_names = [obs_data_as_series[i]['station_name'] for i in range(len(obs_data_as_series))]
    # model_station_data = model_data.interpolate([("latitude", obs_lats), ("longitude", obs_lons)])
    # times_as_dt64 = pa.helpers.cftime_to_datetime64(model_station_data.time)
    # model_data_as_series = pa.helpers.to_time_series_griesie(model_station_data.grid.data, obs_lats, obs_lons,
    #                                                          times_as_dt64, var_name = [var_to_run])

    model_data_as_series = model_data.to_time_series([("latitude", obs_lats),
                                                      ("longitude", obs_lons)])

    df_time = pd.DataFrame()
    df_points = pd.DataFrame()
    station_no = 0
    for i in range(len(obs_data_as_series)):
        _len = len(obs_data_as_series[i][var_to_run])
        # print('{} length: {}'.format(obs_names[i],_len))
        if _len > 0:
            _nansum = np.nansum(obs_data_as_series[i][var_to_run])
            # _isnan = np.isnan(_nansum)
            # print('{} nansum: {:.3f}'.format(obs_names[i],np.nansum(obs_data_as_series[i][var_to_run])))
            # print('{} isnan: {}'.format(obs_names[i],_isnan))
            if _nansum > np.float_(0.):
                station_no += 1
                # print('{} station_no: {}'.format(obs_names[i],station_no))
            else:
                print('{} removed due to NaNs only'.format(obs_names[i]))
        else:
            continue
        # put obs and model in DataFrame to make them use the same time index
        df_time_temp = pd.DataFrame(obs_data_as_series[i][var_to_run],
                                    columns=[obs_network_name])
        df_points = df_points.append(df_time_temp)
        # df_time_temp[model_name] = model_data_as_series[i][var_to_run]*1.E3
        df_time_temp[model_name] = (model_data_as_series[i][var_to_run] *
                                    VARS['scat_scale_factor'])
        # df_time has now all time steps where either one of the obs or model data have data
        #
        # df_points = df_points.append(pd.DataFrame(np.float_(df_time_temp.values), columns=df_time_temp.columns))
        df_time = df_time.append(pd.DataFrame(df_time_temp, columns=df_time_temp.columns))

    # remove all indices where either one of the data pairs is NaN
    # mainly done to get the number of days right.
    # df_time.corr() gets it right without
    df_time = df_time.dropna(axis=0, how='any')
    df_points = df_points.dropna()
    print('# of measurements: {}'.format(len(df_points)))

    filter_name = 'WORLD-wMOUNTAINS'
    filter_name = 'WORLD'
    time_step_name = 'mALLYEARdaily'
    # OD550_AER_an2008_YEARLY_WORLD_SCATTERLOG_AeronetSunV3Lev2.0.daily.ps.png
    # if df_time[model_name].index[0].year != df_time[model_name].index[-1].year:
    years_covered = df_time[model_name].index[:].year.unique().sort_values()
    if len(years_covered) > 1:
        figname = '{}_{}_an{}-{}_{}_{}_{}_{}.png'.format(model_name,
                                                         var_to_run,years_covered[0],
                                                      years_covered[-1],
                                                      time_step_name, filter_name, plt_name,
                                                      obs_network_name)
        plotname = "{}-{} {}".format(years_covered[0], years_covered[-1], 'daily')
    else:
        figname = '{}_{}_an{}_{}_{}_{}_{}.png'.format(model_name,
                                                      var_to_run,years_covered[0],
                                                      time_step_name, filter_name, plt_name,
                                                      obs_network_name)
        plotname = "{} {}".format(years_covered[0], 'daily')

    logger.info(figname)

    mean = df_time.mean()
    correlation_coeff = df_time.corr()
    # IDL: rms=sqrt(total((f_YData-f_Xdata)^2)/n_elements(f_YData))
    #sum = df_time.sum()
    # nmb=total(f_YData-f_Xdata)/total(f_Xdata)*100.
    # c=n_elements(f_YData)
    # f_temp=(f_YData-f_Xdata)/(f_YData+f_Xdata)
    # mnmb=2./c*total(f_temp)*100.
    # fge=2./c*total(abs(f_temp))*100.
    # f_YDatabc=f_YData*(total(f_Xdata,/nan)/total(f_YData,/nan)) ; bias corrected model data
    # rmsbc=sqrt(total((f_YDatabc-f_Xdata)^2)/n_elements(f_YDatabc))
    difference = df_time[model_name] - df_time[obs_network_name]
    num_points = len(df_time)
    rms = np.sqrt(np.nansum(np.power(difference.values, 2)) / num_points)
    nmb = np.sum(difference)/np.sum(df_time[obs_network_name])*100.
    tmp = (df_time[model_name] - df_time[obs_network_name])/(df_time[model_name] + df_time[obs_network_name])
    mnmb = 2./num_points * np.sum(tmp) * 100.
    fge = 2./np.sum(np.abs(tmp)) * 100.

    df_time.plot.scatter(obs_network_name, model_name,
                         loglog=VARS['scat_loglog'],
                         marker='+',
                         color='black')
    # plot the 1 by 1 line
    plt.plot(VARS['scat_xlim'],
             VARS['scat_ylim'], '-', color='grey')
    plt.axes().set_aspect('equal')

    plt.xlim(VARS['scat_xlim'])
    plt.ylim(VARS['scat_ylim'])
    xypos_index = 0
    var_str = var_to_run + VARS.unit_str
    plt.axes().annotate("{} #: {} # st: {}".format(var_str,
                        len(df_time), station_no),
                        xy=xypos[xypos_index], xycoords='axes fraction',
                        fontsize=14, color='red')
    xypos_index += 1
    plt.axes().annotate('Obs: {:.3f}'.format(mean[obs_network_name]),
                        xy=xypos[xypos_index], xycoords='axes fraction',
                        fontsize=10, color='red')
    xypos_index += 1
    plt.axes().annotate('Mod: {:.3f}'.format(mean[model_name]),
                        xy=xypos[xypos_index], xycoords='axes fraction',
                        fontsize=10, color='red')
    xypos_index += 1
    plt.axes().annotate('NMB: {:.1f}%'.format(nmb),
                        xy=xypos[xypos_index], xycoords='axes fraction',
                        fontsize=10, color='red')
    xypos_index += 1
    plt.axes().annotate('MNMB: {:.1f}%'.format(mnmb),
                        xy=xypos[xypos_index], xycoords='axes fraction',
                        fontsize=10, color='red')
    xypos_index += 1
    plt.axes().annotate('R: {:.3f}'.format(correlation_coeff.values[0, 1]),
                        xy=xypos[xypos_index], xycoords='axes fraction',
                        fontsize=10, color='red')
    xypos_index += 1
    plt.axes().annotate('RMS: {:.3f}'.format(rms),
                        xy=xypos[xypos_index], xycoords='axes fraction',
                        fontsize=10, color='red')
    xypos_index += 1
    plt.axes().annotate('FGE: {:.3f}'.format(fge),
                        xy=xypos[xypos_index], xycoords='axes fraction',
                        fontsize=10, color='red')
    # right lower part
    plt.axes().annotate('{}'.format(plotname),
                        xy=xypos[-2], xycoords='axes fraction', ha='center',
                        fontsize=10, color='black')
    plt.axes().annotate('{}'.format(filter_name),
                        xy=xypos[-1], xycoords='axes fraction', ha='center',
                        fontsize=10, color='black')

    plt.savefig(figname, dpi=300)
    plt.close()
