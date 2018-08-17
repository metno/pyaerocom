#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 13:15:09 2018

@author: jonasg
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xarray

def create_fake_data(num_stations=1000, num_tstamps=365, num_data_dim=2):
    
    data = np.empty((num_data_dim, num_tstamps, num_stations))
    
    # supposed to be like station coordinate, i.e. the final data type
    lons = np.linspace(10, 40, num_stations)
    lats = np.linspace(30, 50, num_stations)
    
    times = np.linspace(1,30, num_tstamps).astype('datetime64[D]')
    
    model = np.ones(num_tstamps).reshape((num_tstamps,1)) * np.linspace(1, 2, num_stations)
    
    obs = np.ones(num_tstamps).reshape((num_tstamps,1))*2 * np.linspace(1, 1.5, num_stations)
    
    data[0] = model
    data[1] = obs
    
    meta = {'ts_type'   : 'daily',
            'year'      : 1970, 
            'model_id'  : 'ECMWF_OSUITE',
            'obs_id'    : 'AeronetSunV2L2.daily',
            'var_name'  : 'od550aer'}
    
    return data, lons, lats, times, meta
    
if __name__=='__main__':
    plt.close('all')
    
    data, lons, lats, tstamps, meta = create_fake_data()
    
    fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 8))
    disp = ax1.imshow(data[0], vmin=0, vmax=3)
    ax1.set_title('Model')
    plt.colorbar(disp, ax=ax1)
    
    disp = ax2.imshow(data[1], vmin=0, vmax=3)
    ax2.set_title('Obs')
    plt.colorbar(disp, ax=ax2)
    
    
    arr = xarray.DataArray(data, coords={'source'   : [meta['model_id'],
                                                       meta['obs_id']], 
                                         'time'     : tstamps, 
                                         'longitude': lons,
                                         'latitude' : ('longitude', lats)},
                            dims=['source', 'time', 'longitude'],
                            name=meta['var_name'])
    arr.attrs.update(**meta)
    print(arr)
    