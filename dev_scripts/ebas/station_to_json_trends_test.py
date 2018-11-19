#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 10:12:52 2018

@author: jonasg
"""

import pyaerocom as pya
import matplotlib.pyplot as plt

STAT = 'Appalachian State University*'
if __name__ == '__main__':
    
    r = pya.io.ReadEbas()
    
    
    data = r.read(vars_to_retrieve=['scatc550aer', 'absc550aer'], 
                  station_names='Appalachian State University, Boone (NC)', 
                  datalevel=None)
    
    print(data)
    print()
    #stat = data.to_station_data('Appalachian State*')
    

    #fig, ax = plt.subplots(figsize=(16,10))

    VAR = 'scatc550aer'
    FREQ = 'monthly'
    vardata = {}    
    
    stats = data.to_station_data(STAT, VAR, freq=FREQ)
    
    keymap = dict(station_name = 'station',
                  latitude = 'lat',
                  longitude = 'lon',
                  altitude = 'alt',
                  dataset_name = 'dataset',
                  instrument_name = 'instrument')
    

    def _write(outdata, k, v):
        v = str(v)
        if not k in outdata:
            outdata[k] = [v]
        else:
            if not v in outdata[k]:
                outdata[k].append(v)
            
        return outdata
        
    for stat in stats:
        for k, v in keymap.items():
            try:
                val = stat[k]
            except:
                continue
            vardata = _write(vardata, v, val)
        if 'var_info' in stat and VAR in stat['var_info']:
            for k, v in stat['var_info'][VAR].items():
                vardata = _write(vardata, k, v)
    for k, v in vardata.items():
        vardata[k] = ', '.join(list(dict.fromkeys(vardata[k])))
        
    print(vardata)
            
            
            
        
    