#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 09:04:03 2018

@author: jonasg
"""

import iris

from shutil import rmtree
from os.path import exists, join
from os import mkdir
import numpy as np

EXP = lambda num: int(np.floor(np.log10(abs(num)))) 

def custom_mpl(mpl_rcparams, **kwargs):
    small = 10
    medium = 12
    big = 14
    
    default = {'font.size'          :   small, 
               'axes.titlesize'     :   big,
               'axes.labelsize'     :   medium, 
               'xtick.labelsize'    :   medium, 
               'ytick.labelsize'    :   medium, 
               'legend.fontsize'    :   small, 
               'figure.titlesize'   :   big}
    
    for k, v in default.items():
        try:
            mpl_rcparams[k] = kwargs[k]
        except:
            mpl_rcparams[k] = v
    return mpl_rcparams
    
def daystring(cube, day_idx, year_str="2018"):
    return str((np.datetime64(year_str) + 
                np.timedelta64(int(cube.coord("time").points[day_idx]), "D")))\
                .replace("-", "")

def var_str(cube):
    s = cube.var_name
    return (s[:5] + "_" + s[5:]).upper()
    
def save_name(cube, day_idx, region_id="WORLD", year_str="2018"):
    return ("%s_an%s_d%s_%s_MAP.ps.png" 
            %(var_str(cube), year_str, 
              daystring(cube, day_idx),
              region_id))

def crop_cube_lonlat(cube, lon_range=(0, 360), lat_range=(-90, 90)):
    """Crop cube in certain longitude / latitude range
    
    Parameters
    ----------
    cube : iris.cube.Cube
        Cube containing data
    
    Returns
    -------
    iris.cube.Cube
        Cropped cube
    
    Raises
    ------
    ValueError
        if cropping failed (e.g. due to invalid input for longitude range)
    """
    lats = cube.coord("latitude")
    lons = cube.coord("longitude")
    if not lats.has_bounds():
        lats.guess_bounds()
    if not lons.has_bounds():
        lons.guess_bounds()
        
    result = cube.intersection(longitude=lon_range, latitude=lat_range)
    if not isinstance(cube, iris.cube.Cube):
        raise ValueError("Failed to apply lon / lat constraint for region "
                         "%s. It might be due to longitude range of data "
                         "(i.e. check whether -180 <= lon <= 180 or "
                         "0 <= lon <= 360 and constraint definition for "
                         "region)")
    return result

def area_weighted_mean(cube):
    lats = cube.coord("latitude")
    lons = cube.coord("longitude")

    if not lats.has_bounds():
        lats.guess_bounds()
    if not lons.has_bounds():
        lons.guess_bounds()
    ws = iris.analysis.cartography.area_weights(cube)
    return np.average(cube.data, weights=ws)

def init_save_dirs(cubes, regions, base_dir_out):
    dirs = {}
    for cube in cubes:
        var = var_str(cube)
        dirs[var] = {}
        base_dir = join(base_dir_out, var)
        # remove old plotted stuff for current type...
        if exists(base_dir):
            rmtree(base_dir)
        # ... and create new empty dictionary where the results for this 
        # species are saved
        mkdir(base_dir)
# =============================================================================
#         d = join(base_dir, "WORLD")
#         mkdir(d)
#         dirs[var]["WORLD"] = d
# =============================================================================
        for region in regions:
            d = join(base_dir, region)
            mkdir(d)
            dirs[var][region]=d
    return dirs

def guess_bounds(cubes):
    for cube in cubes:
        for var in cube.coords():
            if not var.has_bounds():
                var.guess_bounds()
    return cubes


def init_cmap_levels(vmin, vmax, num_per_mag=10):
    """Initiate discrete colormap levels for several orders of magnitude"""
    high = EXP(vmax)
    low = -3 if vmin == 0 else EXP(vmin)
    lvls =[0]
    if 1%vmax*10**(-high) == 0: 
        low+=1
        high-=1
    for mag in range(low, high):
        lvls.extend(np.linspace(1, 10, num_per_mag-1, endpoint=0)*10**(mag))
    lvls.extend(np.linspace(1, vmax*10**(-high), num_per_mag, endpoint=1)*10**(high))
    
    return lvls

def get_cmap_ticks(lvls, num_per_mag=3):
    low = EXP(lvls[1]) # second entry (first is 0)
    vmax = lvls[-1]
    high = EXP(vmax)
    
    ticks = [0]
    if 1%vmax*10**(-high) == 0: 
        for mag in range(low, high-1):
            ticks.extend(np.linspace(1, 10, num_per_mag, endpoint=0)*10**(mag))
        ticks.extend(np.linspace(1, 10, num_per_mag+1, endpoint=1)*10**(high-1))
    else:
        for mag in range(low, high):
            ticks.extend(np.linspace(1, 10, num_per_mag, endpoint=0)*10**(mag))
        ticks.extend(np.linspace(1, vmax*10**(-high), 
                     num_per_mag+1, endpoint=1)*10**(high))
        
    return ticks