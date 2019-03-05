#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import numpy as np
import numpy.testing as npt
from pyaerocom import UngriddedData
from pyaerocom.exceptions import DataCoverageError

def test_init_shape():
    npt.assert_array_equal(UngriddedData().shape, (10000, 12))
    
    d1 = UngriddedData(num_points=2, add_cols=['bla', 'blub'])
    npt.assert_array_equal(d1.shape, (2, 14))
    
    d1.add_chunk(1112)
    
    npt.assert_array_equal(d1.shape, (1114, 14))
    
def test_coordinate_access():
    import string
    d = UngriddedData()
    
    stat_names = list(string.ascii_lowercase)
    lons = np.arange(len(stat_names))
    lats = np.arange(len(stat_names)) - 90
    alts = np.arange(len(stat_names)) * 13
    
    for i, n in enumerate(stat_names):
        d.metadata[i] = dict(data_id = 'testcase',
                             station_name = n, 
                             latitude = lats[i],
                             longitude = lons[i],
                             altitude = alts[i])
        
    print(d)
    
    import numpy.testing as npt
    
    npt.assert_array_equal(d.station_name, stat_names)
    npt.assert_array_equal(d.latitude, lats)
    npt.assert_array_equal(d.longitude, lons)
    npt.assert_array_equal(d.altitude, alts)
    
    case_ok = False
    try:
        d.to_station_data('a')
    except DataCoverageError:
        case_ok = True
        
    assert case_ok
    
    c = d.station_coordinates 
    npt.assert_array_equal(c['station_name'], stat_names)
    npt.assert_array_equal(c['latitude'], lats)
    npt.assert_array_equal(c['longitude'], lons)
    npt.assert_array_equal(c['altitude'], alts)
    
if __name__=="__main__":
    test_init_shape()
    test_coordinate_access()