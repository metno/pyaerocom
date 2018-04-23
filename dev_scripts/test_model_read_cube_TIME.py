#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 15:17:51 2018

@author: jonasg
"""
import warnings
warnings.simplefilter("ignore")
import os
import pyaerocom
from iris.coords import DimCoord
from iris import Constraint, load_cube, load

from read_Tseries_Leipzig_Michael import check_time_coord

try:
    from GLOB import OUT_DIR
except:
    OUT_DIR = "./out"
    
FILES = os.path.join(OUT_DIR, "test_files_loaded.txt")
            
if __name__=="__main__":
    var_name = "od550aer"
    
    if not os.path.exists(FILES):
        raise IOError("File %s does not exist, please run script "
                      "test_model_read_cube.py first")
      
        
    loaded_files = open(FILES, "r")
    
    var_constraint = Constraint(cube_func=lambda c: c.var_name==var_name)
    
    fconv = pyaerocom.io.FileConventionRead()
    
    DOALL = 1
    not_ok = []
    success = []
    with open(FILES) as f:
        files = [line.rstrip() for line in f]
        if DOALL:
            
            for fpath in files:
                print("\n")
                dat = load_cube(fpath, var_constraint)
                fconv = fconv.from_file(fpath)
                d = fconv.get_info_from_file(fpath)
                year, ts_type = d["year"], d["ts_type"]
                ok = True
                print(dat.shape)
                [print(c.name()) for c in dat.coords()]
                try:
                    t = dat.coord("time")
                    print(t.units.name)
                    print(len(t.points))
                    
                
                    try:
                        print(t.units.num2date(0))
                    except:
                        ok=False
                    if ts_type == "3hourly":
                        print(t.points[:4])
                except:
                    ok = False
                print("%s\n%s, %s\nOK=%s" %(os.path.basename(fpath), year, 
                                            ts_type, ok))
                if ok:
                    success.append(os.path.basename(fpath))
                else:
                    not_ok.append(os.path.basename(fpath))
            
        else:
            import xarray
            d = xarray.open_dataset(files[0])
            
            c = load_cube(files[0])
            ok = check_time_coord(c, files[0])
                
            
