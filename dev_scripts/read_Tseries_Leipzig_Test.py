#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 11:41:00 2018

@author: jonasg
"""

import pyaerocom
import cf_units
from time import time

if __name__=="__main__":
    
    var_name = "od550aer"
    
    dat = pyaerocom.ModelData()
    dat._init_testdata_default()
    
    fname = dat.suppl_info["from_files"][0]

    tres = dat.time.units.name
    
    tres_alt_test = "hours" + tres[3:]
    
    u_alt_test = cf_units.Unit(tres_alt_test, calendar="gregorian")
    
    ts_test = u_alt_test.num2date([0,1,2])
    print(ts_test)
    
    t0 = time()
    read = pyaerocom.io.ReadModelData(model_id="ECMWF_CAMS_REAN",
                                      start_time="1-1-2003",
                                      stop_time="31.12.2007", 
                                      verbose=True)
    t1=time()
    
    data = read.read_var("od550aer")
    t2=time()
    glob_mean = data.area_weighted_mean()
    t3=time()
    leipzig = data.interpolate([("latitude",51.35), ("longitude", 12.44)])
    t4 = time()
    
    
    print("Time to find all files for model: %3f s" %(t1 - t0))
    print("Time to read all files t-interval: %3f s" %(t2 - t1))
    print("Time to compute global mean t-series: %3f s" %(t3 - t2))    
    print("Time to compute Leipzig: %3f s" %(t4 - t3))
        
    print("Total time: %3f s" %(t4 - t0))
    print("Total time (without global mean): %3f s" %(t4 - t0 - (t3-t2)))

    
    