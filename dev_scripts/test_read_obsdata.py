#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 12:43:26 2018

@author: jonasg
"""


from pyaerocom import const
import pyaerocom

RELOAD = False
if __name__=="__main__":
    try:
        read
    except:
        RELOAD = True
    if RELOAD:
        data = pyaerocom.io.readungridded.ReadUngridded(const.AERONET_SUN_V2L2_AOD_DAILY_NAME)
        data.read()
        
        print('Latitudes:')
        print(data.latitude)
        print('Longitudes:')
        print(data.longitude)
        print('station names')
        print(data)
        # This returns all stations
        all = data.to_timeseries()
        # this returns a single station in a dictionary using the station name as key
        test = data.to_timeseries('AOE_Baotou')
        print(test)
        #This returns a dictionary with more elements
        test_list = data.to_timeseries(['AOE_Baotou','Karlsruhe'])
        print(test_list)

        
