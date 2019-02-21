#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High level test methods that check EBAS time series data for selected stations
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import numpy.testing as npt
from pyaerocom.test.settings import lustre_unavail
from pyaerocom.io import ReadEbas

if __name__=="__main__":
    r = ReadEbas()
    data = r.read('scatc550aer', station_names='Jungfrau*')
    
    print(data)
    
    stat = data.to_station_data('Jung*')
    stat.plot_timeseries('scatc550aer')