#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 11:34:03 2018

@author: jonasg
"""
from matplotlib.pyplot import close
from pyaerocom.test_files import get
from pyaerocom import GriddedData
from pyaerocom.plot.mapping import plot_map

if __name__=="__main__":
    close("all")
    files = get()
    data = GriddedData(files['models']['aatsr_su_v4.3'], var_name="od550aer")
    
    # =============================================================================
    # data_cropped = data.crop(lat_range=(-60, 60), lon_range=(160, 220),
    #                          time_range=("2008-02-01", "2008-02-15"))
    # =============================================================================
    #print(data_cropped.shape)
    
    data.quickplot_map(vmin=0, vmax=1)
    
    crop = data.grid.intersection(longitude=(160, 220))
    
    plot_map(crop, vmin=0, vmax=1)
    
    crop_rolled = crop.intersection(longitude=(-180, 180))
    crop_rolled.coord("longitude").guess_bounds()
    plot_map(crop_rolled, vmin=0, vmax=1)
