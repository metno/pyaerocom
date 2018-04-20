#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:17:51 2018

@author: jonasg
"""

import os
from pyaerocom import config as const
from iris import Constraint, load_cube, load

try:
    from GLOB import OUT_DIR
except:
    OUT_DIR = "./out"
    
ALL_FILES = os.path.join(OUT_DIR, "test_files_all.txt")
LOADED_FILES = os.path.join(OUT_DIR, "test_files_loaded.txt")
FAILED_FILES = os.path.join(OUT_DIR, "test_files_failed.txt")

def get_and_save_test_files(var_name):
    #search patterns
    p1 = ".%s." %var_name
    p2 = "_%s_" %var_name
    test_files = open(ALL_FILES, "w")
    for mdir in const.MODELDIRS:
        print("\n%s\n" %mdir)
        sub = os.listdir(mdir)
        for item in sub:
            path = os.path.join(mdir, item, "renamed")
            if os.path.isdir(path):
                print("\n%s\n" %path)
                files = os.listdir(path)
                for f in files:
                    if f.endswith(".nc") and any([x in f for x in (p1, p2)]):
                        test_files.write("%s\n" %os.path.join(path, f))
                    break
    test_files.close()
    
if __name__=="__main__":
    var_name = "od550aer"
    
    if not os.path.exists(OUT_DIR):
        os.mkdir(OUT_DIR)
        
    if not os.path.exists(ALL_FILES):
        get_and_save_test_files(var_name)
    
    if os.path.exists(LOADED_FILES):
        os.remove(LOADED_FILES)
    if os.path.exists(FAILED_FILES):
        os.remove(FAILED_FILES)
        
    loaded_files = open(LOADED_FILES, "w")
    failed_files = open(FAILED_FILES, "w")
    
    loaded = []
    failed = []
    exceptions = []
    var_constraint = Constraint(cube_func=lambda c: c.var_name==var_name)
    
    
    with open(ALL_FILES) as f:
        files = [line.rstrip() for line in f]
        for fpath in files:
            try:
                load_cube(fpath, var_constraint)
                loaded.append(fpath)
                loaded_files.write("%s\n" %fpath)
                print("LOADED %s" %os.path.basename(fpath))
            except Exception as e:
                failed.append(fpath)
                #failed_files.write("%s\n%s\n\n" %(fpath, repr(e)))
                failed_files.write("%s\n" %fpath)
                failed_files.write("Error: %s\n" %repr(e))
                try:
                    var_names = "Variable names in file: "
                    cubes = load(fpath)
                    for cube in cubes:
                        var_names += "%s " %cube.var_name
                except Exception as e:
                    var_names = "Failed to open CubeList: %s" %repr(e)
                failed_files.write("%s\n" %var_names)
                
                exceptions.append(repr(e))
                print("FAILED %s" %os.path.basename(fpath))
    print()
    for k in range(len(failed)):
        print("Failed: %s" %failed[k])
        print("Error: %s" %exceptions[k])
    
    print("\nOpened %d of %d files\nSuccess rate: %.1f %%" 
          %(len(loaded), len(files), len(loaded)/len(files)*100))
    failed_files.close()
    loaded_files.close()
    