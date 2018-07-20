#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 13:12:12 2018

@author: jonasg
"""
import numpy as np
import abc

class BrowseDict(dict):
    def __getattr__(self, key):
        return self[key]
    
    def __setattr__(self, key, val):
        self[key] = val
        
class Station(BrowseDict):
    def __init__(self, *args, **kwargs):
        super(Station, self).__init__(*args, **kwargs)
        # meta data (strings, lists or arrays)
        self.dataset_name = ''
        self.station_name = ''
        self.PI = ''
        
        # coordinate data (floats, lists or arrays)
        self.latitude = np.nan
        self.longitude = np.nan
        self.altitude = np.nan 
    
class Profile(BrowseDict):
    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self.z = []
        
class Timeseries(BrowseDict):
    def __init__(self, *args, **kwargs):
        super(Timeseries, self).__init__(*args, **kwargs)
        self.dtime = []
        
class StationProfileData(Station, Profile):
    def __init__(self, *args, **kwargs):
        super(StationProfileData, self).__init__(*args, **kwargs)

class StationTimeseriesData(Station, Timeseries):
    def __init__(self, *args, **kwargs):
        super(StationTimeseriesData, self).__init__(*args, **kwargs)    
    
if __name__=="__main__":
    sp = StationProfileData()
    st = StationTimeseriesData()
    
    print(sp)
    print(st)
    
    print(isinstance(sp, Timeseries))
    
        
        
        
        