#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""

import pytest
import numpy.testing as npt
from datetime import datetime
from pyaerocom.test.settings import TEST_RTOL
from pyaerocom import GriddedData

@pytest.fixture(scope='module')
def data_cci():
    '''import example data from Aerosol CCI
    
    The fixture property makes sure that this "variable" is only created once
    for the entire scope of this test session within this module
    '''
    from pyaerocom.io.testfiles import get
    test_file = get()['models']['aatsr_su_v4.3']
    return GriddedData(test_file, var_name="od550aer")

@pytest.fixture(scope='module')
def data_osuite():
    '''import example data from ECMWF_OSUITE
    
    The fixture property makes sure that this "variable" is only created once
    for the entire scope of this test session within this module
    '''
    from pyaerocom.io.testfiles import get
    test_file = get()['models']['ecmwf_osuite']
    return GriddedData(test_file, var_name="od550aer")


def test_longitude(data_cci, data_osuite):
    """Test if longitudes are defined right"""
    lons_cci = data_cci.longitude.points
    lons_osuite = data_osuite.longitude.points
    nominal = [-179.5, 179.5, -180.0, 179.6]
    vals = [lons_cci.min(), lons_cci.max(),
            lons_osuite.min(), lons_osuite.max()]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)
    
def test_latitude(data_cci):
    """test latitude array"""
    nominal_eq = ['arc_degree', 0]
    vals_eq = [data_cci.latitude.units.name,
               int(sum(data_cci.latitude.points))]
    npt.assert_array_equal(nominal_eq, vals_eq)
    
def test_time(data_cci, data_osuite):
    """Test time dimension access and values"""
    time_cci = data_cci.time
    time_osuite = data_osuite.time
    nominal_eq = ["gregorian", 
                  "julian",
                  'day since 2018-01-01 00:00:00.00000000 UTC',
                  'day since 2008-01-01 00:00:00.00000000 UTC', 
                  True, 
                  False]
    vals_eq = [time_osuite.units.calendar, 
               time_cci.units.calendar,
               time_osuite.units.name, 
               time_cci.units.name,
               isinstance(time_osuite.cell(0).point, datetime),
               isinstance(time_cci.cell(0).point, datetime)]
    npt.assert_array_equal(nominal_eq, vals_eq)


if __name__=="__main__":
    import warnings
    warnings.filterwarnings('ignore')
    pytest.main()
    
    