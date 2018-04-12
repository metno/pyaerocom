#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Copyright (C) 2017 met.no
#Contact information:
#Norwegian Meteorological Institute
#Box 43 Blindern
#0313 OSLO
#NORWAY
#E-mail: jan.griesfeller@met.no, jonas.gliss@met.no
#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#MA 02110-1301, USA

"""Global constants for pyaerocom library"""

from pandas import Timestamp
from iris.cube import Cube

VERBOSE = True
FIRST_DATE = Timestamp(1900,1,1)
LAST_DATE = Timestamp(2200,1,1)


SUPPORTED_DATA_TYPES_MODEL = [Cube]
# If True, pre-existing time bounds in data files are removed on 
# import
DEL_TIME_BOUNDS = True 

TS_TYPES = ["hourly", "3hourly", "daily", "monthly"]

#relative tolerance for test session
TEST_RTOL = 1e-7

