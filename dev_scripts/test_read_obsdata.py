#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 12:43:26 2018

@author: jonasg
"""


from pyaerocom import const
import pyaerocom.io as pio
import pandas
import numpy as np
RELOAD = False
if __name__=="__main__":
    try:
        read
    except:
        RELOAD = True
    if RELOAD:
        read = pio.ReadObsData(const.AERONET_SUN_V2L2_AOD_DAILY_NAME)
        read.read_daily()
        
        print('Latitudes:')
        print(read.latitude)
        print('Longitudes:')
        print(read.longitude)
        print('station names')
        print(read)
        # This returns all stations
        all = read.to_timeseries()
        # this returns a single station in a dictionary using the station name as key
        test = read.to_timeseries('AOE_Baotou')
        print(test)
        #This returns a dictionary with more elements
        test_list = read.to_timeseries(['AOE_Baotou','Karlsruhe'])
        print(test_list)
    
    path = read.infiles[0][0]
    
    with open(path) as f:
        data = f.readlines()
        