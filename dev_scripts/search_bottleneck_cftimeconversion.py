#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 14:22:34 2018

@author: jonasg
"""

from pyaerocom.helpers import cftime_to_datetime64
from pyaerocom.io.testfiles import get
from pyaerocom import GriddedData

if __name__=="__main__":
    times = GriddedData(get()["models"]["ecmwf_osuite"], var_name="od550aer").time
    
    for k in range(1000):
        ts = cftime_to_datetime64(times.points,times.units)    
    