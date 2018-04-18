#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""

import pytest
import numpy.testing as npt
from pyaerocom.glob import TEST_RTOL
from pyaerocom import ModelData

@pytest.fixture
def example_data_cci(scope='module'):
    '''import example data from Aerosol CCI
    
    The fixture property makes sure that this "variable" is only created once
    for the entire scope of this test session within this module
    '''
    from pyaerocom.io.testfiles import get
    test_file = get()['models']['aatsr_su_v4.3']
    return ModelData(test_file, var_name="od550aer")

@pytest.fixture
def example_data_osuite(scope='module'):
    '''import example data from ECMWF_OSUITE
    
    The fixture property makes sure that this "variable" is only created once
    for the entire scope of this test session within this module
    '''
    from pyaerocom.io.testfiles import get
    test_file = get()['models']['ecmwf_osuite']
    return ModelData(test_file, var_name="od550aer")

def test_longitudes():
    """Test if longitudes are defined right"""
    data_cci = example_data_cci()
    data_osuite = example_data_osuite()
    lons_cci = data_cci.grid.coord("longitude").points
    lons_osuite = data_osuite.grid.coord("longitude").points
    nominal = [-179.5, 179.5, -180.0, 179.6]
    vals = [lons_cci.min(), lons_cci.max(),
            lons_osuite.min(), lons_osuite.max()]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)
    
if __name__=="__main__":
    test_longitudes()