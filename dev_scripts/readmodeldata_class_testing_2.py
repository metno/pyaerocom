#!/usr/bin/env python3
###############################################################################
# Copyright (C) 2017 met.no
# Contact information: see Email below
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# E-mail: jan.griesfeller@met.no; jonas.gliss@met.no
#
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
###############################################################################

"""Simple script that illustrates how to extract multiple model data

The main class used to import model results for multiple models (and variables)
is MultiGriddedData (part of pyaerocom.io.readgridded.py module).
"""
from pyaerocom.io.readgridded import ReadGriddedMulti

if __name__ == '__main__':
    
    # define two models
    models = ["AATSR_SU_v4.3", "CAM5.3-Oslo_CTRL2016"]
    
    # create and initiate read object 
    read = ReadGriddedMulti(models, '2010-01-01','2011-12-31', verbose=True)
    
    # define a bunch of test variables that are supposed to be loaded for 
    # each model (i.e. that must be contained in both input models)
    test_vars = ["od550aer", "od550dust"]

    # read all variables for all models
    read.read(test_vars)
    
    # print some information about the different data objects
    for name, result in read.results.items():
        print("Current model: %s" %name)
        for var_name, data in result.data.items():
            print("\nCurrent variable: %s" %var_name)
            # data is of type pyaerocom.GriddedData which has a nice string representation
            print(repr(data))
        
    
    # now arbitrarily crop the last data object
    dat_crop = data.crop(lon_range=(-30, 30),
                         lat_range=(0, 45),
                         time_range=('2010-03-15','2010-06-22'))
    
    print("\nStart / stop before crop: %s - %s\n"
          %(data.grid.coord("time").cell(0).point,
            data.grid.coord("time").cell(-1).point))
    
    print("Start / stop after crop: %s - %s"
          %(dat_crop.grid.coord("time").cell(0).point,
            dat_crop.grid.coord("time").cell(-1).point))
# pdb.set_trace()
