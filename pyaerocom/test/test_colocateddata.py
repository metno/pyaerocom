#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import numpy as np
import numpy.testing as npt
from pandas import Timestamp
from pyaerocom import ColocatedData

def test_meta_access_filename():
    name = 'absc550aer_REF-EBAS-Lev3_MOD-CAM5-ATRAS_20100101_20101231_daily_WORLD-noMOUNTAINS.nc'
    
    meta = {'var_name': 'absc550aer', 
            'ts_type': 'daily', 
            'filter_name': 'WORLD-noMOUNTAINS', 
            'start': Timestamp('2010-01-01 00:00:00'), 
            'stop': Timestamp('2010-12-31 00:00:00'), 
            'data_source': ['EBAS-Lev3', 'CAM5-ATRAS']}
    for k, v in ColocatedData.get_meta_from_filename(name).items():
        assert meta[k] == v
    
    
if __name__=="__main__":
    
    test_meta_access_filename()
    