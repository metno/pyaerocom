#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 14:18:21 2018

@author: jonasg
"""
import pyaerocom
import numpy as np
from collections import OrderedDict as od
from time import time
import iris

if __name__=="__main__":

    lons = np.linspace(-180, 180, 20)
    lats = np.linspace(-80, 80, 20)
    times = []
    
    sample_lats = 10
    sample_lons = 10
    
    #load data
    data = pyaerocom.GriddedData()
    data._init_testdata_default()
    
    # Crop data
    cropped = data.crop(lon_range=(8,12), lat_range=(8,12))
    
    # Interpolate using Neareast
    scheme = iris.analysis.Nearest()
    t0 =time()
    interpolator = scheme.interpolator(cropped.grid, ('latitude', 'longitude'))
    interpolated_cube = interpolator((sample_lats, sample_lons))
    print("Elapsed time, nearest: {:.3f} s".format(time() - t0))
    
    cropped = data.crop(lon_range=(8,12), lat_range=(8,12))
    
    t0 =time()
    #the same using linear interpolation
    scheme = iris.analysis.Linear()
    interpolator = scheme.interpolator(cropped.grid, ('latitude', 'longitude'))
    interpolated_cube = interpolator((sample_lats, sample_lons))
    print("Elapsed time, linear: {:.3f} s".format(time() - t0))
    
    DO_ALL = False
    if DO_ALL:
        #now run some tests with uncropped data
        d = od(one_pt           = od(lons = [10],
                                     lats = [10]),
               two_pt_close     = od(lons = [10,11],
                                     lats = [10,11]),
               two_pt_far       = od(lons = [10,-170],
                                     lats = [50,-50]),
               twenty_pt_far    = od(lons = lons,
                                     lats = lats))
        for name, coords in d.items():
            
            data = pyaerocom.GriddedData()
            data._init_testdata_default()
            num = len(coords['lats'])
            sample_points = [('latitude', coords['lats']),
                             ('longitude', coords['lons'])]
            print("Current: {}, (#={})".format(name, num))
            t0 =time()
            data.interpolate(sample_points)
            dt = time() - t0
            print("Elapsed time: {:.3f} s".format(dt))
            times.append(dt)
            
        
        from iris.analysis import Nearest
        
        data = pyaerocom.GriddedData()
        data._init_testdata_default()
                
        scheme = Nearest()
        t0 = time()
        coords, points = zip(*sample_points)
        interp = scheme.interpolator(data.grid, coords)
        t1 = time()
        interp(points, collapse_scalar=True)
        print("Create interpolator: {:.3f} s".format(t1 -t0))
        print("Total: {:.3f} s".format(time() -t0))
    