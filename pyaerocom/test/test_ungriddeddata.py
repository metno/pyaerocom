#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import numpy as np
import numpy.testing as npt
import pytest
from pyaerocom import UngriddedData
from pyaerocom.conftest import testdata_unavail, rg_unavail
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
    
@testdata_unavail
def test_check_index_aeronet_subset(aeronetsunv3lev2_subset):
    aeronetsunv3lev2_subset._check_index()

@testdata_unavail    
@rg_unavail
def test_check_set_country(aeronetsunv3lev2_subset):
    idx, countries = aeronetsunv3lev2_subset.check_set_country()
    assert len(idx) == len(aeronetsunv3lev2_subset.metadata)
    assert len(countries) == len(idx)
    assert countries == ['Italy', 'Japan', 'Burkina Faso', 'Brazil', 
                         'American Samoa', 'French Southern Territories', 
                         'Korea, Republic of', 'France', 'Portugal', 
                         'France', 'Barbados', 'United Kingdom', 'Bolivia', 
                         'United States', 'French Polynesia', 'China', 
                         'Taiwan', 'Algeria', 'Netherlands', 'Greece', 
                         'Belgium', 'Argentina']
    idx, countries = aeronetsunv3lev2_subset.check_set_country()
    assert idx == []
    assert countries == []
 
@pytest.mark.dependency(depends=["test_check_set_country"])
def test_countries_available(aeronetsunv3lev2_subset):
    assert aeronetsunv3lev2_subset.countries_available == ['Algeria', 
        'American Samoa', 'Argentina', 'Barbados', 'Belgium', 'Bolivia', 
        'Brazil', 'Burkina Faso', 'China', 'France', 'French Polynesia', 
        'French Southern Territories', 'Greece', 'Italy', 'Japan', 
        'Korea, Republic of', 'Netherlands', 'Portugal', 'Taiwan', 
        'United Kingdom', 'United States']
    
if __name__=="__main__":
    import sys
    pytest.main(sys.argv)