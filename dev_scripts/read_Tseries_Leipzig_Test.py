#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 11:41:00 2018

@author: jonasg
"""

import pyaerocom
from iris.coords import DimCoord
from datetime import datetime
from numpy import datetime64, asarray, arange
import cf_units

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
    
    read = pyaerocom.io.ReadModelData(model_id="ECMWF_CAMS_REAN",
                                      start_time="1-1-2003",
                                      stop_time="31.12.2007", 
                                      verbose=True)
    
    data = read.read_var("od550aer")
        
    
    

    
    