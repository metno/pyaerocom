#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 13:15:09 2018

@author: jonasg
"""

import pyaerocom as pya
from time import time
if __name__=='__main__':
    
    r = pya.io.ReadUngridded(['AeronetSunV2Lev2.daily', 
                              'AeronetSunV3Lev2.daily'],
                             'od550aer')
    data = r.read()
    
    print(data.contains_datasets, data.contains_vars)
    
    f = pya.Filter(region='EUROPE', altitude_filter='noMOUNTAINS')
    
    stat_lon_range = f.lon_range
    stat_lat_range = f.lat_range
    stat_alt_range = f.alt_range
    
    aeronet2 = data.filter_by_meta(dataset_name='AeronetSunV2Lev2.daily')
    
    aeronet2_europe = f(aeronet2)
    
    print(aeronet2)
    print(aeronet2_europe)