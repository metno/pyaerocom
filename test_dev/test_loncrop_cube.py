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
from pyaerocom.helpers import get_constraint
import iris.quickplot as qplt

from GLOB import TEST_FILE

if __name__=="__main__":
    
    cubes = load(TEST_FILE)
    
    var = "od550aer"
    
    constraint = Constraint(cube_func=lambda c: c.var_name==var)
    
    c = load_cube(TEST_FILE, constraint=constraint)
    
    # lons are defined 0 <= lon <= 360
    print(c.coord("longitude"))
    
    # over meridian in -180 <= lon <= 180 definition
    crop_range1 = (-30, 30)
    crop_range2 = (150, 210)
    
    # First example: use cube intersection method
    crop1_intersect = c.intersection(longitude=crop_range1)
    crop2_intersect = c.intersection(longitude=crop_range2)
    
    # Second example: use iris.Constraint
    low, high = crop_range1
    constraint1 = Constraint(longitude=lambda v: low%360 < v < 360 or 0 < v < high)
    
    crop1_constraint = c.extract(constraint1)
    
    low, high = crop_range2
    constraint2 = Constraint(longitude=lambda v: low%360 < v < 360 or 0 < v < high)
    
    crop1_constraint = c.extract(constraint1)
    
    