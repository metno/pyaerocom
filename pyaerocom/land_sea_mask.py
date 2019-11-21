#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 13:01:34 2019

author: hannas@met.no
"""

import os 
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
    path = const.FILTERMASKKDIR
    path = '/home/hannas/Desktop/pyaerocom-suppl/htap_masks/'
    
    if isinstance(region_id, list):
        for i, r in enumerate(region_id):
            r = r.split("HTAP")[0]
            fil =  glob.glob( os.path.join( path, '{}*0.1*.nc'.format(r)))[0]
            if i == 0:
                masks = xr.open_dataset(fil)[r+'htap']
            else:
                masks += xr.open_dataset(fil)[r+'htap']
    else:
        region_id  = region_id.split("HTAP")[0]
        fil =  glob.glob( os.path.join( path, '{}*0.1*.nc'.format(region_id)))[0]
        masks = xr.open_dataset(fil)[region_id+'htap']
    return masks

def load_region_mask_iris(region_id='PANhtap'):
    """    
    Returns
    ---------
    mask : xarray.DataArray containing the masks. 
    
    TODO : Update this one to send in a list and return the sum of the list. 
    
    pya.const.OUTPUTDIR
    """
    path = const.FILTERMASKKDIR
    path = '/home/hannas/Desktop/pyaerocom-suppl/htap_masks/'
    
    if isinstance(region_id, list):
        raise NotImplementedError("Not implemented yet.") 
    
    region_id = region_id.split("HTAP")[0]
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

def download_mask_urllib():
    #from urllib.request import urlopen
    from urllib.request import urlretrieve
    from zipfile import ZipFile
    path_out = const.FILTERMASKKDIR
    url = 'https://github.com/metno/pyaerocom-suppl/tree/master/htap_masks.zip'

    name = os.path.basename(url)
    #print(name)
    file = os.path.join(path_out, name)
    urlretrieve(url, file)
    print(file)
    with ZipFile(file, 'r') as zipObj:
        print(zipObj)
        # Extract all the contents of zip file in current directory
        zipObj.extractall()
    
    print("Succesfully downloaded masks.")
    return 

def download_mask():
    import requests

    path_out = const.FILTERMASKKDIR
    url = 'http://github.com/metno/pyaerocom-suppl/blob/master/htap_masks/'
    
    regions = const.HTAP_REGIONS
    
    for region in regions:
        filename = "{}htap.0.1x0.1deg.nc".format(region)
        url_file = os.path.join(url, filename)
        #name     = os.path.basename(url)
        file     = os.path.join(path_out, filename)
        myfile   = requests.get(url_file)
        
        with open(file, 'wb') as data:
            data.write(myfile.content)
        
    print("Succesfully downloaded masks.")
    return 

if __name__ == '__main__':
    print(load_region_mask_xr(region_id='PAN'))
    #download_mask()