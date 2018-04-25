#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file tests and highlights possibilities to crop a cube in longitudal 
direction over the border of the longitude definition array which may either
be 0 <= lon <= 360 (border array at prime meridian, case below) or in the 
-180 <= lon <= 180 definition.
"""
import warnings
warnings.filterwarnings('ignore')
from iris import load_cube, Constraint
from pyaerocom.helpers import get_lon_constraint_buggy
from pyaerocom.io.testfiles import get
import iris.quickplot as qplt
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from pyaerocom.plot.config import COLOR_THEME

def plot_first_day(cube, name):
    dat = cube[0]

    qplt.pcolormesh(dat, cmap=COLOR_THEME.cmap_map)
    plt.gca().coastlines(color=COLOR_THEME.color_coastline)
    #things that do not need to be done when day is updated
    
    plt.gca().set_xlim((-180, 180))
    plt.gca().set_ylim((-90, 90))
    
    plt.gca().set_yticks([-60, -30, 0, 30, 60], crs=ccrs.PlateCarree())
    plt.gca().set_xticks([-180, -90, 0, 90, 180], crs=ccrs.PlateCarree())

    plt.title(name)

if __name__=="__main__":
    plt.close("all")
    var = 'od550aer'
    
    # get test file dictionary
    test_files = get()
    
    constraint = Constraint(cube_func=lambda c: c.var_name==var)
    
    #longitudes OK
    cci = load_cube(test_files['models']['aatsr_su_v4.3'], 
                    constraint=constraint)
    
    osuite = load_cube(test_files['models']['ecmwf_osuite'],
                       constraint=constraint)
    
    # over meridian in -180 <= lon <= 180 definition
    crop_range1 = (-30, 30)
    crop_range2 = (150, 210)
    
    # First example: use cube intersection method
    cci_intersect1 = cci.intersection(longitude=crop_range1)
    cci_intersect2 = cci.intersection(longitude=crop_range2)
    
    osuite_intersect1 = osuite.intersection(longitude=crop_range1)
    osuite_intersect2 = osuite.intersection(longitude=crop_range2)
    
    constraint1_cci = get_lon_constraint_buggy(crop_range1, meridian_centre=True)
    c1_cci = constraint1_cci.extract(cci)
    lons = c1_cci.coord("longitude")
    print(lons.points.min(), lons.points.max())
    
    constraint2_cci = get_lon_constraint_buggy(crop_range2, meridian_centre=True)
    c2_cci = constraint2_cci.extract(cci)
    lons = c2_cci.coord("longitude")
    print(lons.points.min(), lons.points.max())
    
    constraint1_osuite = get_lon_constraint_buggy(crop_range1, meridian_centre=False)
    c1_osuite = constraint1_osuite.extract(osuite)
    lons = c1_osuite.coord("longitude")
    print(lons.points.min(), lons.points.max())
    
    constraint2_osuite = get_lon_constraint_buggy(crop_range2, meridian_centre=False)
    c2_osuite = constraint2_osuite.extract(osuite)
    lons = c2_osuite.coord("longitude")
    print(lons.points.min(), lons.points.max())
    
# =============================================================================
#     clon = Constraint(longitude = lambda lon : 290 < lon < 360 or 0 < lon < 20)
#     
#     osuite_crop = clon.extract(osuite)
# =============================================================================

    for item in [cci_intersect1, cci_intersect2, osuite_intersect1, 
                 osuite_intersect2]:
        lons = item.coord("longitude")
        print(lons.points.min(), lons.points.max())   
        
    fig, axes = plt.subplots(2, 2, figsize=(22, 10))
    plt.sca(axes[0,0])
    plot_first_day(cci_intersect1, "cci_intersect1: (%s, %s)" %crop_range1)
    
    plt.sca(axes[1,0])
    plot_first_day(cci_intersect2, "cci_intersect2: (%s, %s)" %crop_range2)
    
    plt.sca(axes[0,1])
    plot_first_day(c1_cci, "constraint1_cci: (%s, %s)" %crop_range1)
    
    plt.sca(axes[1,1])
    plot_first_day(c2_cci, "constraint2_cci: (%s, %s)" %crop_range2)
    fig.tight_layout()
    
    fig, axes = plt.subplots(2, 2, figsize=(22, 10))
    plt.sca(axes[0,0])
    plot_first_day(osuite_intersect1, "osuite_intersect1: (%s, %s)" %crop_range1)
    
    plt.sca(axes[1,0])
    plot_first_day(osuite_intersect2, "osuite_intersect2: (%s, %s)" %crop_range2)
    
    plt.sca(axes[0,1])
    plot_first_day(c1_osuite, "constraint1_osuite: (%s, %s)" %crop_range1)
    
    plt.sca(axes[1,1])
    plot_first_day(c2_osuite, "constraint2_osuite: (%s, %s)" %crop_range2)
    fig.tight_layout()
# =============================================================================
#     
#     # Second example: use iris.Constraint
#     low, high = crop_range1
#     constraint1 = Constraint(longitude=lambda v: low%360 < v < 360 or 0 < v < high)
#     
#     crop1_constraint = c.extract(constraint1)
#     
#     low, high = crop_range2
#     constraint2 = Constraint(longitude=lambda v: low%360 < v < 360 or 0 < v < high)
#     
#     crop1_constraint = c.extract(constraint1)
#     
# =============================================================================
    
    
    
    