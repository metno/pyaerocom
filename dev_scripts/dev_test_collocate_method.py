#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 13:35:07 2018

@author: jonasg
"""
import pyaerocom
from pandas import Timestamp
import numpy as np
if __name__ == "__main__":

    data = pyaerocom.GriddedData()
    data._init_testdata_default()
    
    start = Timestamp("2018-1-22")
    stop = Timestamp("2018-2-5")
    
    lons = np.linspace(-10, 30, 20)
    lats = np.linspace(40, 80, 20)
    data = data.crop(lon_range=(lons[0], lons[-1]), 
                        lat_range=(lats[0], lats[-1]), 
                        time_range=(start, stop))
    
    fig = data.quickplot_map()
    fig.suptitle("CROPPED")

    sample_points=[("longitude", lons), ("latitude", lats)]
    
    coords_avail = data.coords_order
    
    idx_data = np.arange(len(coords_avail))
        
    indices = []
    
    # get length of sample points array of first coordinate
    ref_len = len(sample_points[0][1])
    
    for name, values in sample_points:
        if not name in coords_avail:
            raise KeyError("Coordinate {} does not exist in data, existing "
                           "coordinates are {}".format(name, coords_avail))
        elif not len(values) == ref_len:
            raise ValueError("Length of coordinate arrays must be the "
                             "same...")
        indices.append(coords_avail.index(name))
        
    ### interpolate grid to new coordinates
    sub = data.interpolate(sample_points)
    
    arr = sub.grid.data
    
    #total number of points in grid
    totnum_grid = np.prod(arr.shape)
    
    #get the number of parameters spanned by the subspace
    subnum_grid = ref_len**len(sample_points)
    
    #put reduced dimension into first index, so we can loop over it
    arr_dimred = arr.reshape(subnum_grid, int(totnum_grid / subnum_grid))
    
    #remove first item in sample_points (used to iterate over all points)
    first_coord, values = sample_points.pop(0)
    
    