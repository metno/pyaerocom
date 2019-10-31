#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 13:01:34 2019

author: hannas@met.no
"""

import os 
import glob

#from pyaerocom.region import Region
#from pyaerocom.filter import Filter
import numpy as np
import xarray as xr

def load_region_mask(region_id='PANhtap'):
    """    
    Returns
    ---------
    mask : xarray.DataArray containing the masks. 
    
    """

    path  = '//home/hannas/Desktop/htap/'  # get from config
    fil =  glob.glob(path + region_id + '*0.1*.nc')[0]
    print(fil)
    masks = xr.open_dataset(fil)
    return masks[region_id]

def available_region_mask():
    """
    Returns
    ----------
    arr : List[str]
        Returns a list of available htap region masks.
    """
    arr = []
    path = '//home/hannas/Desktop/htap/' # TODO update
    files =  glob.glob(path + '*0.1*.nc')
    for fil in files:
        arr.append(os.path.basename(fil).split('.')[0])
    return arr

def get_mask(lat, lon, mask):
    """
    lat : float
    lon : float
    mask : xarray dataset  
    
    Returns
    --------
    m : float 
        pixel mask is either zero or 1
    
    """
    la = np.around(lat, 2)
    lo = np.around(lon, 2) 
  
    mask_pixel = mask.sel(lat = slice(la + 0.1, la), long = slice(lo - 0.1, lo))
    m = mask_pixel.values[0][0]  
    return m

"""
class LandSeaMask(object):
    MASK_FILENAMSE = {'EUROPE' : 'XY.nc'}
    def __init__(self, name):
        # call super
        self._name = None
        self.name = name
    
    @property
    def name(self):
        return self.name
    
    @name.setter
    def name(self, value):
        if not self._name_exists(value):
            raise ValueError()
        self._name = value
        
    def load_mask_file(self):
        from pyaerocom import const
        try:
            data_dir = const.SUPPLDIRS['landseamasks']
        except KeyError:
            raise 
            
    def real_hpt_region():
        pass
    
    # need def apply filter to ungridded, gridded and 
    
"""
    