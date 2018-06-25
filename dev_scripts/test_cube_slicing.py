#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 11:34:03 2018

@author: jonasg
"""
from matplotlib.pyplot import close
import numpy as np
import iris
from pyaerocom.io.testfiles import get
from pyaerocom import GriddedData
from pyaerocom.plot.mapping import plot_map

if __name__=="__main__":
    close("all")
    
    files = get()
    data = GriddedData(files['models']['aatsr_su_v4.3'], var_name="od550aer")
    
    cube = data.grid
    
    iris.coord_categorisation.add_month(cube, "time", name='months')
    iris.coord_categorisation.add_year(cube, "time", name='years')
    cube_monthly = cube.aggregated_by(['months', 'years'], iris.analysis.MEAN)
    
    cube_mean = cube_monthly.collapsed
    ts = data.time
    import cf_units
    
    times = cf_units.num2date(ts.points, ts.units.name, ts.units.calendar)
    
    
    
    
    
    
