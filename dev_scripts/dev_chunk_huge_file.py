#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 14:17:46 2018

@author: jonasg
"""

import xarray
import iris
from time import time
import pyaerocom as pya
import numpy as np
import os

MODEL_ID = 'SPRINTARS-T213_AP3-CTRL2016-PD'

VAR = 'ec550aer3d'

FP1 = '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/SPRINTARS-T213_AP3-CTRL2016-PD/renamed/aerocom3_SPRINTARS-T213_AP3-CTRL2016-PD_ec550aer3d_Modellevel_2010_3hourly.nc'

TEST_OUT = 'out/TEST.nc'

if __name__ == '__main__':
    
    reader = pya.io.ReadGridded(MODEL_ID)
    t0 = time()
    data_pya = reader.read_var(VAR)
    print('Elapsed time open pyaerocom: {:.2f} s'.format(time() - t0))
    
    t0 = time()
    data_iris = iris.load(FP1)[0]
    print('Elapsed time open iris: {:.2f} s'.format(time() - t0))
    
    t0 = time()
    ds = xarray.open_dataset(FP1, chunks={'time':30})
    
    print('Elapsed time open xarray: {:.2f} s'.format(time() - t0))
    
    xarr = ds['ec550aer3d']
    
    lon_sample = np.linspace(-40, 40, 10)
    lat_sample = np.linspace(-20, 60, 10)
    
    lons = data_iris.coord('longitude').points
    lats = data_iris.coord('latitude').points
    
    lon_idx = []
    lat_idx = []
    
    
    def closest_idx(val, source):
        return np.argmin(np.abs(source - val))
    
    for lat, lon in zip(lat_sample, lon_sample):
        lon_idx.append(closest_idx(lon, lons))
        lat_idx.append(closest_idx(lat, lats))
    
    surf = data_iris[:,0]
    
    surf_at_stats = surf[:, lat_idx][:,:,lon_idx]
      
    if not os.path.exists(TEST_OUT):
        iris.save(surf_at_stats, TEST_OUT)
        
    coll = iris.load(TEST_OUT)
    print(coll)
    #data_pya.interpolate(longitude=lon_sample, latitude=lat_sample)
    
    
    
    
    
    
    
    
    