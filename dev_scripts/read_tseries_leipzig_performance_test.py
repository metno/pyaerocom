#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 11:41:00 2018

@author: jonasg
"""

import pyaerocom
from time import time
import socket
import numpy as np

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--n", nargs='?', const=10, default=10)

def run():

    ts = []
    ts.append(time())
    read = pyaerocom.io.ReadGridded(name="ECMWF_CAMS_REAN",
                                      start="1-1-2003",
                                      stop="31-12-2007",
                                      verbose=True)
    ts.append(time())
    
    data = read.read_var("od550aer")
    ts.append(time())
    data.area_weighted_mean()
    ts.append(time())
    data.interpolate([("latitude",51.35), ("longitude", 12.44)])
    ts.append(time())
    
    ts = np.asarray(ts)
    return ts[1:] - ts[:-1]

if __name__=="__main__":    
    
    
    args = parser.parse_args()
    msgs = []
    msgs.append("Machine: {} (repitions: {})".format(socket.gethostname(),
                                                    args.n))
    dts = np.zeros((args.n, 4))*np.nan
    for k in range(args.n):
        dts[k] = run()
        print("CURRENT: {}".format(k))
    dts_avg = np.average(dts, axis=0)
    
    
    msgs.append("Avg. time to find all files for model: %3f s" %(dts_avg[0]))
    msgs.append("Avg. time to read all files t-interval: %3f s" %(dts_avg[1]))
    msgs.append("Avg. time to compute global mean t-series: %3f s" %(dts_avg[2]))    
    msgs.append("Avg. time to compute Leipzig: %3f s" %(dts_avg[3]))
        
    msgs.append("Total avg. time: %3f s" %(dts_avg.sum()))
    msgs.append("Total avg. time (without global mean): %3f s" %(dts_avg.sum() - dts_avg[2]))

    
    with open("read_tseries_leipzig_performance_test.txt", "a") as f:
        for msg in msgs:
            print(msg)
            f.write(msg + "\n")
        f.write("\n")
    f.close()
        
    