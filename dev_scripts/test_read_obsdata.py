#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 12:43:26 2018

@author: jonasg
"""


from pyaerocom import const
import pyaerocom.io as pio

if __name__=="__main__":
    ObsData = pio.ReadObsData(const.AERONET_SUN_V2L2_AOD_DAILY_NAME)
    
    
# =============================================================================
#     ObsData.read_daily()
#     
#     print('Latitudes:')
#     print(ObsData.latitude)
#     print('Longitudes:')
#     print(ObsData.longitude)
#     print('station names')
#     print(ObsData)
#     # This returns all stations
#     all = ObsData.to_timeseries()
#     # this returns a single station in a dictionary using the station name as key
#     test = ObsData.to_timeseries('AOE_Baotou')
#     print(test)
#     #This returns a dictionary with more elements
#     test_list = ObsData.to_timeseries(['AOE_Baotou','Karlsruhe'])
#     print(test_list)
# =============================================================================
