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
# import sys
# import os
import getpass
import socket
#import pdb

def cli():
    """Pyaerocom command line interface (CLI)
    
    Pyaerocom is a Python package for the Aerocom project 
    """
    user = getpass.getuser()
    from pyaerocom import config as const
    import pyaerocom.io as pio
    SupportedObsNetworks = ''

    # command line interface using argparse
    Options = {}
    parser = argparse.ArgumentParser(
        description='pyaerocom.py\n\n\n')
    parser.add_argument("model",
                        help="model names to use; can be a comma separated "
                              "list; use " + const.NOMODELNAME +
                             " for observations only",nargs="+")
    parser.add_argument("--variable", help="list of variables; comma seperated.")
    parser.add_argument("--modelyear",
                        help="model years to run; use 9999 for climatology, leave out for all years; comma separated list; Use this to limit the plotting of the OBSERVATION-ONLY model to certain years.")
    parser.add_argument("--obsyear",
                        help="observation years to run; use 9999 for climatology, leave out for same as model year")
    parser.add_argument("--nosend", help="switch off webserver upload", action='store_true')
    parser.add_argument("-v", "--verbose", help="switch on verbosity", action='store_false')
    parser.add_argument("--debug", help="switch on debug mode: Do NOT start idl, just print what would be done",
                        action='store_true')
    parser.add_argument("--numcpu",
                        help="Number of Processes to start. Default is using half of the number of logical cores available.",
                        type=int)
    parser.add_argument("--obsnetwork",
                        help=const.NOMODELNAME + " mode: run all variables for a certain obs network; model mode: Run a variable with a non standard obs network. Supported are " + SupportedObsNetworks)
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
    for Model in args.model:
        print(Model)
        if Model != const.NOMODELNAME:
            # start model read
            continue

        # start Obs reading
        ObsData = pio.ReadObsData(const.AERONET_SUN_V2L2_AOD_DAILY_NAME,
                                  verboseflag = Options['VERBOSE'])
        ObsData.read_daily()
        test = ObsData.to_timeseries()
        return ObsData

###########################################################################################################################
if __name__ == '__main__':
    cli()
    

