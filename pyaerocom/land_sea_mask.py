#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 13:01:34 2019

author: hannas@met.no
"""

#import os 
import glob
import numpy as np
import xarray as xr

from pyaerocom import const
from iris import load_cube

def load_region_mask_xr(region_id='PANhtap'):
    """    
    Returns
    ---------
    mask : xarray.DataArray containing the masks. 
    
    TODO : Update this one to send in a list and return the sum of the list. 
    
    pya.const.OUTPUTDIR
    """
    path = const.OUTPUTDIR
    path  = '/home/hannas/MyPyaerocom/htap_masks/'  # TODO : this should be MyPyaerocom ..... get from config
    path = "/home/hannas/Desktop/htap/"
    
    if isinstance(region_id, list):
        for i, r in enumerate(region_id):
            fil =  glob.glob(path + r + '*0.1*.nc')[0]
            if i == 0:
                masks = xr.open_dataset(fil)[region_id]
            else:
                masks += xr.open_dataset(fil)[region_id]
    else:
        fil =  glob.glob(path + region_id + '*0.1*.nc')[0]
        masks = xr.open_dataset(fil)[region_id]
    return masks

def load_region_mask_iris(region_id='PANhtap'):
    """    
    Returns
    ---------
    mask : xarray.DataArray containing the masks. 
    
    TODO : Update this one to send in a list and return the sum of the list. 
    
    pya.const.OUTPUTDIR
    """
    #path = const.OUTPUTDIR
    #path  = '/home/hannas/MyPyaerocom/htap_masks/'  # TODO : this should be MyPyaerocom ..... get from config
    #path = "/home/hannas/Desktop/htap/"
    
    path = '/home/hannas/Desktop/htap/' 
    fil =  glob.glob(path + region_id + '*0.1*.nc')[0]
    masks = load_cube(fil)
    return masks

def available_region_mask():
    """
    Returns
    ----------
    arr : List[str]
        Returns a list of available htap region masks.
    """
    return const.HTAP_REGIONS

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
    
    if isinstance(mask, xr.DataArray):
        mask_pixel = mask.sel(lat = slice(la + 0.1, la), long = slice(lo - 0.1, lo))
        m = mask_pixel.values[0][0]  
        return m
    else:
        print("Please provide masks of type xarray dataset, not {}".format(type(mask)))
        return

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
if __name__ == '__main__':
    print(load_region_mask(region_id='PANhtap'))