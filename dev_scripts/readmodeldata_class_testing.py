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

from pyaerocom.io.readgridded import ReadGridded
from pyaerocom.plot import plotmaps
from GLOB import OUT_DIR_MAPS # import standard output directory

if __name__ == '__main__':

    import argparse
    default_model = "AATSR_SU_v4.3"
    
    parser = argparse.ArgumentParser(description='command line interface to the readgrid class')
    parser.add_argument("model", help="model to read", nargs="?", 
                        const=default_model, default=default_model, type=str)

    args = parser.parse_args()
    if args.model:
        model = args.model

    var = "od550aer"

    # Create data import object
    test = ReadGridded(model, '2010-01-01','2011-12-31', verbose=True)
    
    print(test.vars)
    
    data = test.read_var("od550aer", ts_type="daily")
        
    
    #plotmaps(data, VerboseFlag=True, plotdir=OUT_DIR_MAPS)