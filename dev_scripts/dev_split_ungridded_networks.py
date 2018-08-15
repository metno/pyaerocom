#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 13:15:09 2018

@author: jonasg
"""

import pyaerocom as pya

if __name__=='__main__':
    
    r = pya.io.ReadUngridded(['AeronetSunV2Lev2.daily',
                              'AeronetSunV3Lev2.daily'], 'od550aer')
    data = r.read()
    
    print(data.contains_datasets, data.contains_vars)
    
    sub = data.extract_dataset('AeronetSunV2Lev2.daily')