#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 11:41:00 2018

@author: jonasg
"""

import pyaerocom
from time import time
import socket
if __name__=="__main__":    
    
    print(pyaerocom.const)
    msgs = []
    with open("read_tseries_leipzig_performance_test.txt", "a") as f:
        
        msgs.append("Machine: {}".format(socket.gethostname()))

        t0 = time()
        read = pyaerocom.io.ReadModelData(model_id="ECMWF_CAMS_REAN",
                                          start_time="1-1-2003",
                                          stop_time="31-12-2007", 
                                          verbose=True)
        t1=time()
        
        data = read.read_var("od550aer")
        t2=time()
        glob_mean = data.area_weighted_mean()
        t3=time()
        leipzig = data.interpolate([("latitude",51.35), ("longitude", 12.44)])
        t4 = time()
        
        msgs.append("Time to find all files for model: %3f s" %(t1 - t0))
        msgs.append("Time to read all files t-interval: %3f s" %(t2 - t1))
        msgs.append("Time to compute global mean t-series: %3f s" %(t3 - t2))    
        msgs.append("Time to compute Leipzig: %3f s" %(t4 - t3))
            
        msgs.append("Total time: %3f s" %(t4 - t0))
        msgs.append("Total time (without global mean): %3f s" %(t4 - t0 - (t3-t2)))
    
        for msg in msgs:
            print(msg)
            f.write(msg + "\n")
        f.write("\n")
    f.close()
        
    