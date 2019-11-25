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

from pyaerocom.helpers import numpy_to_cube

from iris import load_cube

def load_region_mask_xr(region_id='PAN'):
    """    
    Creates a dataset of the union of regions sent as input.
    
    Parameters
    ------------------
    region_id : str or List[str]
        The region id or ids you want to filter your data with.
    
    Returns
    ---------
    mask : xarray.DataArray 
        containing the masks. 
    """
    from pyaerocom import const
    path = '/home/hannas/Desktop/pyaerocom-suppl/htap_masks/'
    path = const.FILTERMASKKDIR
    #path = os.path.join(const.FILTERMASKKDIR, 'htap_masks/')
    #print("region_id {}".format(region_id))
    if isinstance(region_id, list):
        for i, r in enumerate(region_id):
            if r not in const.OLD_AEROCOM_REGIONS:
                print(r)
                fil =  glob.glob( os.path.join( path, '{}*.nc'.format(r)))[0]
                if i == 0:
                    masks = xr.open_dataset(fil)[r+'htap']
                else:
                    masks += xr.open_dataset(fil)[r+'htap']
        masks = masks.where(masks < 1, 1)
    else:
        #region_id  = region_id.split("HTAP")[0]
        print(region_id)
        if region_id not in const.OLD_AEROCOM_REGIONS:
            fil =  glob.glob( os.path.join( path, '{}*.nc'.format(region_id)))[0]
            masks = xr.open_dataset(fil)[region_id+'htap']
        else:
            raise ValueError("Not a valids region")
    return masks

def load_region_mask_iris(region_id='PAN'):
    """    
    Returns
    ---------
    mask : xarray.DataArray containing the masks. 

    Load : each cube seperatly and merge then after updating var_name
    """
    from pyaerocom import const
    path = const.FILTERMASKKDIR
    
    files = []
    cubes = []

    if isinstance(region_id, list):
        for r in region_id:
            #print("   øksdhfja")
            if r not in const.OLD_AEROCOM_REGIONS:
                #print(glob.glob(path + r + '*.nc'))
                #print("   øksdhfja")
                path = os.path.join(path, r)
                fil = glob.glob(path + '*.nc')[0]
                files.append(fil)
                masks = load_cube(fil)
                cubes.append(masks)
                
        merged = np.max([x.data for x in cubes], axis = 0)
        merged_cube = numpy_to_cube(merged, dims=(cubes[0].coords()[0], cubes[0].coords()[1]))
    else:
        path = os.path.join(path, region_id)
        fil = glob.glob(path + '*.nc')[0]
        merged_cube = load_cube(fil)
        return merged_cube

def available_region_mask():
    """
    Returns
    ----------
    arr : List[str]
        Returns a list of available htap region masks.
    """
    from pyaerocom import const
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

def download_mask():
    #from urllib.request import urlopen
    from pyaerocom import const
    import requests
    
    path_out = const.FILTERMASKKDIR
    bse_url = 'https://pyaerocom.met.no/pyaerocom-suppl/htap_masks/'

    for region in const.HTAP_REGIONS:
        filename = '{}htap.0.1x0.1deg.nc'.format(region)      
        url = os.path.join(bse_url, filename)
        file_out = os.path.join(path_out, filename)
        r = requests.get(url)
        open(file_out, 'wb').write(r.content) 
    return 

if __name__ == '__main__':
   print(load_region_mask_xr())
   print(load_region_mask_iris())
   #download_mask()
   print('hello')