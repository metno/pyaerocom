#!/usr/bin/env python3

################################################################
# readoddata_testing.py
#
# demostrator of how to use the observational data reading class
#
# this file is part of the aerocom_pt package
#
#################################################################
# Created 20171024 by Jan Griesfeller for Met Norway
#
# Last changed: See git log
#################################################################

# Copyright (C) 2017 met.no
# Contact information:
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# E-mail: jan.griesfeller@met.no
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


import pdb
# import numpy as np

#import aerocom_pt.config as const
#import aerocom_pt

###################################################################################
from pyaerocom.read.readmodeldata import ReadModelData
from pyaerocom.plot import plotmaps

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='command line interface to the readmodeldata class')
    parser.add_argument("model", help="model to read")

    args = parser.parse_args()
    if args.model:
        model = args.model


    test = ReadModelData(model, '2010-01-01','2011-12-31', VerboseFlag=True)
    test.Read('od550aer')

    plotmaps(test.data, VerboseFlag=True, plotdir="./")

    pdb.set_trace()
    test.data[model].coord('time').bounds

    print(test)


# pdb.set_trace()
