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
"""

import argparse
import sys
# import os
import getpass
import socket

def cli():
    """Pyaerocom command line interface (CLI)
    
    Pyaerocom is a Python package for the Aerocom project 
    """
    user = getpass.getuser()
    from pyaerocom import const
    import pyaerocom.io as pio
    supported_obs_networks = ",".join(pio.ReadObsData.SUPPORTED_DATASETS)

    # command line interface using argparse
    Options = {}
    parser = argparse.ArgumentParser(
        description='pyaerocom.py\n\n\n')
    parser.add_argument("model",
                        help="model names to use; can be a comma separated "
                              "list; use " + const.NOMODELNAME +
                             " for observations only",nargs="+")
    parser.add_argument("-v", "--verbose", help="switch on verbosity", action='store_true')
    parser.add_argument("--variable", help="list of variables; comma seperated.")
    parser.add_argument("--modelyear",
                        help="model years to run; use 9999 for climatology, leave out for all years; comma separated list; Use this to limit the plotting of the OBSERVATION-ONLY model to certain years.")
    parser.add_argument("--obsyear",
                        help="observation years to run; use 9999 for climatology, leave out for same as model year")
    parser.add_argument("--startdate", help="startdate as YYYY-MM-DD e.g. 2012-01-01", default='2011-01-01')
    parser.add_argument("--enddate", help="enddate  as YYYY-MM-DD e.g. 2012-12-31", default='2012-12-31')

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
    # parser.add_argument("--", help="")

    args = parser.parse_args()

    if args.numcpu:
        Options['NumCPU'] = args.numcpu

    if args.variable:
        Options['VariablesToRun'] = args.variable.split(',')
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
        Options['ModelName'] = args.model

    if args.htapfilters:
        Options['HTAPFILTERS'] = args.htapfilters

    if args.aodtrends:
        Options['AODTRENDS'] = args.aodtrends

    if args.debug:
        Options['DEBUG'] = args.debug

    if args.nosend:
        Options['NOSEND'] = args.nosend

    if args.verbose:
        Options['VERBOSE'] = args.verbose

    if args.modelyear:
        Options['ModelYear'] = args.modelyear.split(',')
    else:
        Options['ModelYear'] = 'all'

    if args.obsyear:
        Options['ObsYear'] = args.obsyear
    else:
        Options['ObsYear'] = '0000'

    if args.obsnetwork:
        Options['ObsnetworksToRun'] = args.obsnetwork.split(',')
        # use the 1st for model plotting for now
        Options['ObsNetworkName'] = args.obsnetwork.split(',')

    if args.forecast:
        Options['FORECAST'] = args.forecast

    if args.plotdailyts:
        Options['PLOTDAILYTIMESERIES'] = args.plotdailyts

    hostname = socket.gethostname()
    model_obj = []
    model_data = []
    for Model in args.model:
        print(Model)
        if Model != const.NOMODELNAME:
            # start model read
            model_obj.append(pio.ReadGrid(model_id = Model,
                                     start_time = args.startdate,
                                     stop_time = args.enddate,
                                     verbose=Options['VERBOSE']))

            print(model_obj[0])
            model_data.append(model_obj[0].read_var(var_name=Options['VariablesToRun'][0], ts_type="daily"))
            print(model_data[0])
        else:
            # observations only
            # 1st check if the obs network string is right
            if Options['ObsNetworkName'][0] in pio.ReadObsData.SUPPORTED_DATASETS:
                # start Obs reading
                ObsData = pio.ReadObsData(data_set_to_read = const.EARLINET_NAME,
                                          vars_to_read = Options['VariablesToRun'][0],
                                          verbose= args.verbose)
                ObsData.read_daily()

                # print('Latitudes:')
                # print(ObsData.latitude)
                # print('Longitudes:')
                # print(ObsData.longitude)
                # print('station names')
                # print(ObsData)
                # This returns all stations
                TimeSeriesSingle = ObsData.to_timeseries(station_name="L'Aquila, Italy",start_date = args.startdate, end_date=args.enddate)
                TimeSeries = ObsData.to_timeseries(start_date = args.startdate, end_date=args.enddate)
                for series in TimeSeries:
                    print(series['station name'])
                    print(series[Options['VariablesToRun'][0]])

                # this returns a single station in a dictionary using the station name as key
                # test = ObsData.to_timeseries('AOE_Baotou')
                # print(test)
                # #This returns a dictionary with more elements
                # test_list = ObsData.to_timeseries(['AOE_Baotou','Karlsruhe'])
                # print(test_list)
                #return ObsData


            else:
                sys.stdout.write(
                    "ERROR: {0} is not a supported observation network name.\n".format(Options['ObsNetworkName'][0]))
                sys.stdout.write("Supported are: {0}".format(supported_obs_networks))
###########################################################################################################################
if __name__ == '__main__':
    cli()
    

