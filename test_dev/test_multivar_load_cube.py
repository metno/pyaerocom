#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 09:53:28 2018

@author: jonasg
"""
import warnings
warnings.filterwarnings('ignore')
from iris import load_cube, Constraint, load

from GLOB import TEST_FILE

if __name__=="__main__":
    
    cubes = load(TEST_FILE)
    for cube in cubes:
        print(cube.var_name)
        
    var = "od550aer"
    var_names = ["od550aer", "od550dust"]
    
    constraint = Constraint(cube_func=lambda c: c.var_name==var)
    
    constraint_multivar = Constraint(cube_func=lambda c: c.var_name in var_names)
    
    c = load_cube(TEST_FILE, constraint=constraint)
    
    multi_cube = load(TEST_FILE, constraint_multivar)
    
    cc = (constraint 
          & Constraint(latitude=lambda x: 20 < x< 30) 
          & Constraint(longitude=lambda x: 10 < x< 60))
    
    cubes = load(TEST_FILE)
    
    cube=cubes.extract(cc)[0]
    print(cube)
    
    
    
    
    
