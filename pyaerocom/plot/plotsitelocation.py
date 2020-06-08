#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains scatter plot routines for Aerocom data.
"""

from pyaerocom import const#, BASEMAP_AVAILABLE
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

# TODO: Not used currently, required??
# text positions for the annotations
XYPOS=[]
XYPOS.append((.01, 0.95))
XYPOS.append((0.01, 0.90))
XYPOS.append((0.3, 0.90))
XYPOS.append((0.01, 0.86))
XYPOS.append((0.3, 0.86))
XYPOS.append((0.01, 0.82))
XYPOS.append((0.3, 0.82))
XYPOS.append((0.01, 0.78))
XYPOS.append((0.3, 0.78))
XYPOS.append((0.8, 0.1))
XYPOS.append((0.8, 0.06))

def plotsitelocation(model_name, model_data=None, obs_data=None, options=None,
                     verbose=True):
    """method to plot scatterplots"""

    plt_name = 'SITELOCATION'
    var_to_run = options['VariablesToRun'][0]
    obs_network_name = options['ObsNetworkName'][0]
    obs_data_as_series = obs_data.to_timeseries(start_date=options['StartDate'],
                                                end_date=options['EndDate'],
                                                freq='D')
    obs_lats = [obs_data_as_series[i]['latitude']
                for i in range(len(obs_data_as_series))]
    obs_lons = [obs_data_as_series[i]['longitude']
                for i in range(len(obs_data_as_series))]
    obs_names = [obs_data_as_series[i]['station_name']
                 for i in range(len(obs_data_as_series))]
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
        df_time_temp[model_name] = ( model_data_as_series[i][var_to_run] *
                                const.VARS[var_to_run]['scat_scale_factor'])
        # df_time has now all time steps where either one of the obs or model data have data
        #
        # df_points = df_points.append(pd.DataFrame(np.float_(df_time_temp.values), columns=df_time_temp.columns))
        df_time = df_time.append(pd.DataFrame(df_time_temp,
                                              columns=df_time_temp.columns))

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
        title = "{} {} station list {}-{}".format(var_to_run, filter_name, years_covered[0], years_covered[-1])
    else:
        figname = '{}_{}_an{}_{}_{}_{}_{}.png'.format(model_name,
                                                      var_to_run,years_covered[0],
                                                      time_step_name, filter_name, plt_name,
                                                      obs_network_name)
        plotname = "{} {}".format(years_covered[0], 'daily')
        title = "{} {} station list {}".format(var_to_run, filter_name, years_covered[0])

    if verbose:
        sys.stdout.write(figname+"\n")

    lat_low = -90
    lat_high = 90.
    lon_low = -180.
    lon_high = 180.

    # TODO: review basemap dependency
    basemap_flag=False
    if basemap_flag and const.BASEMAP_AVAILABLE:
        m = Basemap(projection='cyl', llcrnrlat=lat_low, urcrnrlat=lat_high,
                    llcrnrlon=lon_low, urcrnrlon=lon_high, resolution='c', fix_aspect=False)

        x, y = m(obs_lons, obs_lats)
        # m.drawmapboundary(fill_color='#99ffff')
        # m.fillcontinents(color='#cc9966', lake_color='#99ffff')
        plot = m.scatter(x, y, 4, marker='o', color='r', )
        m.drawmeridians(np.arange(-180,220,40),labels=[0,0,0,1], fontsize=10)
        m.drawparallels(np.arange(-90,120,30),labels=[1,1,0,0], fontsize=10)
        # axis = plt.axis([LatsToPlot.min(), LatsToPlot.max(), LonsToPlot.min(), LonsToPlot.max()])
        ax = plot.axes
        m.drawcoastlines()
    else:
        ax = plt.axes([0.15,0.1,0.8,0.8],projection=ccrs.PlateCarree())
        ax.set_ylim([lat_low, lat_high])
        ax.set_xlim([lon_low, lon_high])
        #ax.set_aspect(2)

        ax.coastlines()
        plot = plt.scatter(obs_lons, obs_lats, 8, marker='o', color='r')
        #plot.axes.set_aspect(1.8)

        # lon_formatter = LongitudeFormatter(number_format='.1f', degree_symbol='')
        # lat_formatter = LatitudeFormatter(number_format='.1f', degree_symbol='')
        # ax.xaxis.set_major_formatter(lon_formatter)
        # ax.yaxis.set_major_formatter(lat_formatter)
        xticks = ax.set_xticks([-180., -120., -60., 0., 60, 120, 180])
        yticks = ax.set_yticks([-90., -60, -30, 0., 30, 60, 90])
        # ax.annotate('source: AEROCOM', xy=(0.93, 0.04), xycoords='figure fraction',
        #             horizontalalignment='right', fontsize=9, bbox=dict(boxstyle='square', facecolor='none',
        #                                                                 edgecolor='black'))
        ax.annotate('longitude', xy=(0.55, 0.12), xycoords='figure fraction',
                    horizontalalignment='center', fontsize=12, )
        ax.annotate('latitude', xy=(0.07, 0.55), xycoords='figure fraction', rotation=90,
                    horizontalalignment='center', fontsize=12, )
        # ax.set_xlabel = 'longitude'
        # ax.set_ylabel = 'latitude'
        ax.annotate(model_name, xy=(174., -83.), xycoords='data', horizontalalignment='right', fontsize=13,
                    fontweight='bold',
                    color='black', bbox=dict(boxstyle='square', facecolor='white', edgecolor='none', alpha=0.7))
        ax.annotate("No of stations: {}".format(station_no), xy=(-174., -83.), xycoords='data',
                    fontweight='bold',
                    horizontalalignment='left', fontsize=13,
                    color='black', bbox=dict(boxstyle='square', facecolor='white', edgecolor='none', alpha=0.7))

    plt.title(title, fontsize=13)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.xlabel = 'longitude'
    plt.ylabel = 'latitude'

    plt.savefig(figname, dpi=300)
    plt.close()
