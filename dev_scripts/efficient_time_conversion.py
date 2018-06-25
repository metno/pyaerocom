#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script that investigates different options to convert netCDF times as stored 
in the iris Cube object, into datetime64 objects
"""
import warnings
warnings.filterwarnings('ignore')
from pyaerocom.io.testfiles import get
from pyaerocom import GriddedData
from matplotlib.pyplot import close
import numpy as np
try:
    from cftime import (microsec_units, millisec_units, sec_units, min_units,
                        hr_units, day_units)
    from cftime._cftime import _dateparse
    cftime_avail = True
except:
    from netcdftime import (microsec_units, millisec_units, sec_units, min_units,
                            hr_units, day_units)
    cftime_avail = False
    
from time import time

def cfunit_to_datetime64(cube_times):
    cfu_str = cube_times.units.name
    res = cfu_str.split()[0].lower()
    if res in microsec_units:
        tstr = "us"
    elif res in millisec_units:
        tstr = "ms"
    elif res in sec_units:
        tstr = "s"
    elif res in min_units:
        tstr = "m"
    elif res in hr_units:
        tstr = "h"
    elif res in day_units:
        tstr = "D"
    else:
        raise ValueError('unsupported time units')
    if cftime_avail:
        basedate = np.datetime64(_dateparse(cfu_str))
    else:
        basedate = (np.datetime64(cube_times.units.num2date(cube_times.points[0]))
                - cube_times.points[0].astype("timedelta64[%s]" %tstr))
    return (basedate, tstr)
    #return (basedate, tres_str)

if __name__=="__main__":
    
    vals = np.arange(0,5, 1)
    tres_test = ["100ns", "30us", "55ms", "3s", "2h", "3D", "M", "3Y"]
    
    close("all")
    files = get()
    data = GriddedData(files['models']['aatsr_su_v4.3'],
                     var_name="od550aer",
                     name='aatsr_su_v4.3')
    

    for tres in tres_test:
        tstr = "timedelta64[%s]" %tres
        print(np.datetime64("2016") + vals.astype(tstr))
    
    tnums = data.time
    
    t0 = time()
    for k in range(100):
        ts_cubecell = [np.datetime64(t.point) for t in tnums.cells()]
    print("Elapsed time (Cube cell conversion): %.4f s" %(time() - t0))
    
    t0 = time()
    for k in range(100):
        ts_cftime = [np.datetime64(t) for t in tnums.units.num2date(tnums.points)]
    print("Elapsed time (cftime conversion V1): %.4f s" %(time() - t0))
    
    import cf_units
    t0 = time()
    for k in range(100):
        [np.datetime64(t) for t in cf_units.num2date(tnums.points, 
         tnums.units.name, tnums.units.calendar)]
    print("Elapsed time (cftime conversion V2): %.4f s" %(time() - t0))
    
    t0 = time()
    for k in range(100):
        base_date, tres_str = cfunit_to_datetime64(tnums)
        ts_np = base_date + tnums.points.astype("timedelta64[%s]" %tres_str)
    print("Elapsed time (numpy conversion): %.4f s" %(time() - t0))