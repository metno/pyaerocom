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
from iris import load_cube, Constraint, load
from pyaerocom.helpers import get_lon_constraint
from pyaerocom.test_files import get

if __name__=="__main__":
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
    
    constraint1_cci = get_lon_constraint(crop_range1, meridian_centre=True)
    c1_cci = constraint1_cci.extract(cci)
    lons = c1_cci.coord("longitude")
    print(lons.points.min(), lons.points.max())
    
    constraint2_cci = get_lon_constraint(crop_range2, meridian_centre=True)
    c2_cci = constraint2_cci.extract(cci)
    lons = c2_cci.coord("longitude")
    print(lons.points.min(), lons.points.max())
    
    constraint1_osuite = get_lon_constraint(crop_range1, meridian_centre=False)
    c1_osuite = constraint1_osuite.extract(osuite)
    lons = c1_osuite.coord("longitude")
    print(lons.points.min(), lons.points.max())
    
    constraint2_osuite = get_lon_constraint(crop_range2, meridian_centre=False)
    c2_osuite = constraint2_osuite.extract(osuite)
    lons = c2_osuite.coord("longitude")
    print(lons.points.min(), lons.points.max())

    for item in [cci_intersect1, cci_intersect2, osuite_intersect1, osuite_intersect2]:
        lons = item.coord("longitude")
        print(lons.points.min(), lons.points.max())    
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
    
    
    
    