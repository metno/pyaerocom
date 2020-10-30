#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2018 met.no
# Contact information:
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# E-mail: jan.griesfeller@met.no, jonas.gliss@met.no
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA

"""
main program with a command line interface for pyaerocom

OUTDATED    OUTDATED    OUTDATED    OUTDATED    OUTDATED    OUTDATED
"""

import argparse
import sys
# import os
import getpass
import socket
#import pdb
import pandas as pd
import numpy as np
from pyaerocom import const

def cli():
    """Pyaerocom command line interface (CLI)

    Pyaerocom is a Python package for the Aerocom project

    Example
    -------
    >>> import pyaerocom.io as pio
    >>> import pyaerocom as pa
    >>> import itertools
    >>> import matplotlib.pyplot as plt
    >>> import pandas as pd
    >>> model = 'IASI_MAPIR.v3.x.merged.AN'
    >>> startdate = '2007-01-01'
    >>> enddate = '2012-12-31'
    >>> obsnetwork_to_read = 'EARLINET'
    >>> plot_min = 500
    >>> plot_max = 5000
    >>> var_to_read = 'zdust'
    >>> model_obj = pio.ReadGridded(name = model, start = startdate, stop = enddate, verbose=True)
    >>> model_data = model_obj.read_var(var_name=var_to_read, ts_type="daily")
    >>> obs_data = pyaerocom.io.readungridded.ReadUngridded(dataset_to_read = obsnetwork_to_read, vars_to_retrieve = var_to_read, verbose=True)
    >>> obs_data.read()
    >>> pa.helpers.griesie_dataframe_testing(model_data, obs_data, startdate, enddate)

    >>> obs_data_as_series = obs_data.to_timeseries(start_date=startdate, end_date=enddate, freq='D')
    >>> obs_lats = obs_data.latitude
    >>> obs_lons = obs_data.longitude
    >>> obs_lats=[obs_data_as_series[i]['latitude'] for i in range(len(obs_data_as_series))]
    >>> obs_lons=[obs_data_as_series[i]['longitude'] for i in range(len(obs_data_as_series))]
    >>> obs_names=[obs_data_as_series[i]['station_name'] for i in range(len(obs_data_as_series))]
    >>> model_station_data = model_data.interpolate([("latitude", obs_lats),("longitude", obs_lons)])
    >>> times_as_dt64 = pa.helpers.cftime_to_datetime64(model_station_data.time)
    >>> model_data_as_series = pa.helpers.to_time_series_griesie(model_station_data.grid.data, obs_lats, obs_lons, times_as_dt64)
    >>> # single station
    >>> df = pd.DataFrame(obs_data_as_series[1]['zdust'], columns=['obs'])
    >>> df['model'] = model_data_as_series[1]['zdust']
    >>> # remove points where any of the df is NaN
    >>> #df = df.dropna(axis=0, how='any')
    >>> correlation = df.corr(method='pearson')
    >>> plot = df.plot.scatter('obs','model')
    >>> df.show()

    >>> # all stations
    >>> df_all=pd.DataFrame(columns=['obs', 'model'])
    >>>

    >>> # model time series at obs times with NaNs removed
    >>> model_series_at_obs_times = [model_data_as_series[i]['zdust'][obs_data_as_series[i]['zdust'].index].dropna()*1E3 for i in range(len(obs_data_as_series))]
    >>> #obs data at non NaN model data times
    >>> obs_series_at_model_times = [obs_data_as_series[i]['zdust'][model_series_at_obs_times[i].index] for i in range(len(model_series_at_obs_times))]

    >>> # model_at_obs_times = model_data_as_series[0]['zdust'][obs_data_as_series[0]['zdust'].index]
    >>> model_at_obs_times = list(itertools.chain.from_iterable([model_data_as_series[i]['zdust'][obs_data_as_series[i]['zdust'].index]*1E3 for i in range(len(obs_data_as_series))]))
    >>> obs_as_list = list(itertools.chain.from_iterable([obs_data_as_series[i]['zdust'].values for i in range(len(obs_data_as_series))]))
    >>> plot = plt.plot(obs_as_list, model_at_obs_times, 'go', linestyle='None')
    >>> plt.plot([plot_min,plot_max],[plot_min,plot_max], 's-')
    >>> plt.axes().set_aspect('equal')
    >>> plt.xlim((plot_min,plot_max))
    >>> plt.ylim((plot_min,plot_max))
    >>> plt.show()
    """
    user = getpass.getuser()
    from pyaerocom import const
    import pyaerocom.io as pio
    import pyaerocom as pa
    supported_obs_networks = ", ".join(pio.ReadUngridded().SUPPORTED_DATASETS)
    import pyaerocom.plot

    # command line interface using argparse
    options = {}
    parser = argparse.ArgumentParser(
        description='pyaerocom.py\n\n\n')
    parser.add_argument("model",
                        help="model names to use; can be a comma separated "
                              "list; use " + const.NOMODELNAME +
                             " for observations only",nargs="+")
    parser.add_argument("-v", "--verbose", help="switch on verbosity",
                        action='store_true')
    parser.add_argument("--variable", help="list of variables; comma seperated.")
    parser.add_argument("--modelyear",
                        help='model years to run; use 9999 for climatology, '
                             'leave out for all years; comma separated list; '
                             'Use this to limit the plotting of the '
                             'OBSERVATION-ONLY model to certain years.')
    parser.add_argument("--obsyear",
                        help='observation years to run; use 9999 for '
                             'climatology, leave out for same as model year')
    parser.add_argument("--startdate", help="startdate as YYYY-MM-DD e.g. 2012-01-01", default='2007-01-01')
    parser.add_argument("--enddate", help="enddate  as YYYY-MM-DD e.g. 2012-12-31", default='2015-12-31')

    parser.add_argument("--nosend", help="switch off webserver upload", action='store_false')
    parser.add_argument("--debug", help="switch on debug mode: Do NOT start idl, just print what would be done",
                        action='store_true')
    parser.add_argument("--numcpu",
                        help="Number of Processes to start. Default is using half of the number of logical cores available.",
                        type=int)
    parser.add_argument("--obsnetwork",
                        help=const.NOMODELNAME + " mode: run all variables for a certain obs network; model mode: Run a variable with a non standard obs network. Supported are " + supported_obs_networks)
    parser.add_argument("--forecast", help="forecast mode for CAMS; daily maps only, nothing else", action='store_true')
    parser.add_argument("--htapfilters",
                        help="also run the htap filters; model has to have 1x1 degree resolution at the moment",
                        action='store_true')
    parser.add_argument("--aodtrends", help="run the AODTREND filters AODTREND95TO12,AODTREND,AODTREND95",
                        action='store_true')
    parser.add_argument("--plotdailyts", help="also plot daily time series", action='store_true')
    parser.add_argument("--plotscatter", help="plot scatter plot", action='store_true')
    parser.add_argument("--plotsitelocation", help="plot sirelocation plot", action='store_true')
    # parser.add_argument("--", help="")

    args = parser.parse_args()

    if args.numcpu:
        options['NumCPU'] = args.numcpu

    if args.variable:
        options['VariablesToRun'] = args.variable.split(',')
        # now build a dict with var as key, and the 'real var name as value
        # used to make special variable model possible
        # e.g. od550aer_Forecast
        # dict_Vars = {}
        # for Var in dict_Param['VariablesToRun']:
        #     if Var in IniFileData['VariableAliases']:
        #         dict_Vars[Var] = IniFileData['VariableAliases'][Var]
        #     else:
        #         dict_Vars[Var] = Var

    if args.model:
        options['ModelName'] = args.model

    if args.startdate:
        options['StartDate'] = args.startdate

    if args.enddate:
        options['EndDate'] = args.enddate

    if args.htapfilters:
        options['HTAPFILTERS'] = args.htapfilters

    if args.aodtrends:
        options['AODTRENDS'] = args.aodtrends

    if args.debug:
        options['DEBUG'] = args.debug

    if args.nosend:
        options['NOSEND'] = args.nosend

    if args.verbose:
        options['VERBOSE'] = args.verbose

    if args.modelyear:
        options['ModelYear'] = args.modelyear.split(',')
    else:
        options['ModelYear'] = 'all'

    if args.obsyear:
        options['ObsYear'] = args.obsyear
    else:
        options['ObsYear'] = '0000'

    if args.obsnetwork:
        options['ObsnetworksToRun'] = args.obsnetwork.split(',')
        # use the 1st for model plotting for now
        options['ObsNetworkName'] = args.obsnetwork.split(',')

    if args.forecast:
        options['FORECAST'] = args.forecast

    if args.plotdailyts:
        options['PLOTDAILYTIMESERIES'] = args.plotdailyts

    if args.plotscatter:
        options['PLOTSCATTER'] = args.plotscatter
    else:
        options['PLOTSCATTER'] = False

    if args.plotsitelocation:
        options['PLOTSITELOCATION'] = args.plotsitelocation
    else:
        options['PLOTSITELOCATION'] = False

    hostname = socket.gethostname()
    model_obj = []
    model_data = []
    for model_name in args.model:
        print(model_name)
        if model_name != const.NOMODELNAME:
            # start model read

            model_obj = pio.ReadGridded(name=model_name, start=args.startdate, stop=args.enddate, verbose=True)
            model_data = model_obj.read_var(var_name=options['VariablesToRun'][0], ts_type="daily")
            obs_data = pyaerocom.io.readungridded.ReadUngridded(dataset_to_read=options['ObsNetworkName'][0], vars_to_retrieve=[options['VariablesToRun'][0]],
                                                                verbose=True)
            model_obj = pio.ReadGridded(name=model_name, start=args.startdate, stop=args.enddate, verbose=True)
            model_data = model_obj.read_var(var_name=options['VariablesToRun'][0], ts_type="daily")
            obs_data = pyaerocom.io.readungridded.ReadUngridded(
                dataset_to_read=options['ObsNetworkName'][0],
                vars_to_retrieve=[options['VariablesToRun'][0]],
                verbose=True)
            obs_data.read()

            # obs_lats = obs_data.latitude
            # obs_lons = obs_data.longitude

            # obs_data_as_series = obs_data.to_timeseries(start_date=args.startdate, end_date=args.enddate, freq='D')
            # obs_lats = [obs_data_as_series[i]['latitude'] for i in range(len(obs_data_as_series))]
            # obs_lons = [obs_data_as_series[i]['longitude'] for i in range(len(obs_data_as_series))]
            if options['PLOTSCATTER']:
                pyaerocom.plot.plotscatter(model_name, model_data, obs_data, options)

            if options['PLOTSITELOCATION']:
                pyaerocom.plot.plotsitelocation(model_name, model_data, obs_data, options)

            # print('xarray...')
            # # xarray
            # import xarray
            # filename = '/lustre/storeA/project/aerocom/aerocom-users-database/CCI-Aerosol/CCI_AEROSOL_Phase2/AATSR_SU_v4.3/renamed/aerocom.AATSR_SU_v4.3.daily.od550aer.2008.nc'
            # xarray_ds = xarray.open_dataset(filename, decode_times=True)
            # model_station_data_xarray_single = xarray_ds.sel(latitude=obs_lats[0], longitude=obs_lons[0], method='nearest')
            #
            # model_station_data_xarray_all = pa.helpers.griesie_xarray_to_timeseries(xarray_ds, obs_lats, obs_lons,
            #                                                                         vars_to_retrieve=[
            #                                                                             Options['VariablesToRun'][0]])
            #
            #
            # print('pyaerocom...')
            # # obs_names = [obs_data_as_series[i]['station_name'] for i in range(len(obs_data_as_series))]
            # # model_station_data = model_data.interpolate([("latitude", obs_data.latitude), ("longitude", obs_data.longitude)])
            # model_station_data = model_data.interpolate([("latitude", obs_lats), ("longitude", obs_lons)])
            # model_data_as_series = model_data.to_time_series([("latitude", obs_lats), ("longitude", obs_lons)])
            #
            # sample_points = [('latitude', obs_lats), ('longitude', obs_lons)]
            # sample_points_single = [('latitude', obs_lats[0]), ('longitude', obs_lons[0])]
            # # read and colocate with iris directly
            # print('iris...')
            # import iris
            # cube = iris.load(filename)
            # model_station_data_cube_all = cube[0].interpolate(sample_points, iris.analysis.Nearest())
            # model_station_data_cube_single = cube[0].interpolate(sample_points_single, iris.analysis.Nearest())
            # print('Summary:')
            # print("pyaerocom griddata:")
            # print(model_station_data.grid.data[50:60,0,0])
            # print("cube all:")
            # print(model_station_data_cube_all.data[50:60,0,0])
            # print("cube single:")
            # print(model_station_data_cube_single.data[50:60])
            #
            # print("xarray single:")
            # print(np.float_(model_station_data_xarray_single[Options['VariablesToRun'][0]][50:60]))
            # print("xarray all:")
            # print(np.float_(model_station_data_xarray_all[0][Options['VariablesToRun'][0]][50:60]))
            #
            # var_to_run = Options['VariablesToRun'][0]
            # obs_network_name = Options['ObsNetworkName'][0]
            # #Model = Options['ModelName']
            # # times_as_dt64 = pa.helpers.cftime_to_datetime64(model_station_data.time)
            # # model_data_as_series = pa.helpers.to_time_series_griesie(model_station_data.grid.data, obs_lats, obs_lons,
            # #                                                          times_as_dt64, var_name=[var_to_run])
            #
            #
            # df_points = pd.DataFrame()
            # df_time = pd.DataFrame()
            # df_xarray_time = pd.DataFrame()
            # station_no = 0
            # # for i in range(len(obs_data_as_series)):
            # for i in range(len(model_station_data_xarray_all)):
            #     if len(obs_data_as_series[i][var_to_run]) > 0:
            #         station_no += 1
            #         print('non NaN station:',i)
            #     else:
            #         continue
            #
            #     # station_no += 1
            #     # put obs and model in DataFrame to make them use the same time index
            #     df_time_temp = pd.DataFrame(obs_data_as_series[i][var_to_run],
            #                                 columns=[obs_network_name])
            #
            #     # df_time_temp[model_name] = model_data_as_series[i][var_to_run]*1.E3
            #     df_time_temp[model_name] = (model_data_as_series[i][var_to_run] *
            #                                 const.PLT_PARAM[var_to_run]['scale_factor'])
            #     df_time_temp['xarray_'+model_name] = (model_station_data_xarray_all[i][var_to_run] *
            #                                 const.PLT_PARAM[var_to_run]['scale_factor'])
            #     # df_time has now all time steps where either one of the obs or model data have data
            #     #
            #     df_points = df_points.append(pd.DataFrame(np.float_(df_time_temp.values), columns=df_time_temp.columns))
            #     df_time = df_time.append(pd.DataFrame(df_time_temp, columns=df_time_temp.columns))
            #
            # # remove all indices where either one of the data pairs is NaN
            # # df_time = df_time.dropna(axis=0, how='any')
            #
            # filter_name = 'WORLD'
            # correlation_coeff = df_time.corr()
            # print('R: ', correlation_coeff.values[0, 1])
            #
            # df_xarray_all = model_station_data_xarray_all.to_dataframe()
            # df_xarray_single = model_station_data_xarray_single.to_dataframe()
            #
            #
            #
            #

        else:
            # observations only
            # 1st check if the obs network string is right
            # pa.readungridded.ReadUngridded(dataset_to_read = obsnetwork_to_read, vars_to_retrieve = var_to_read, verbose=True)
            # if options['ObsNetworkName'][0] in pyaerocom.io.readungridded.ReadUngridded.SUPPORTED_DATASETS:
            # pa.nogriddata.NoGridData(dataset_to_read = obsnetwork_to_read, vars_to_retrieve = var_to_read, verbose=True)
            if options['ObsNetworkName'][0] in pio.ReadUngridded.SUPPORTED_DATASETS:
                # start Obs reading
                ObsData = pio.ReadUngridded(dataset_to_read = options['ObsNetworkName'][0],
                                                                   vars_to_retrieve = [options['VariablesToRun'][0]],
                                                                   verbose= args.verbose)
                ObsData.read()

                # print('Latitudes:')
                # print(ObsData.latitude)
                # print('Longitudes:')
                # print(ObsData.longitude)
                # print('station_names')
                # print(ObsData)
                # This returns all stations
                TimeSeriesSingle = ObsData.to_timeseries(station_name="L'Aquila, Italy",start_date = args.startdate, end_date=args.enddate)
                TimeSeries = ObsData.to_timeseries(start_date = args.startdate, end_date=args.enddate)
                for series in TimeSeries:
                    print(series['station_name'])
                    # print(series[options['VariablesToRun'][0]])

                # this returns a single station in a dictionary using the station_name as key
                # test = ObsData.to_timeseries('AOE_Baotou')
                # print(test)
                # #This returns a dictionary with more elements
                # test_list = ObsData.to_timeseries(['AOE_Baotou','Karlsruhe'])
                # print(test_list)
                #return ObsData

            else:
                sys.stdout.write(
                    "ERROR: {0} is not a supported observation network name.\n".format(options['ObsNetworkName'][0]))
                sys.stdout.write("Supported are: {0}".format(supported_obs_networks))
###########################################################################################################################
if __name__ == '__main__':
    cli()
