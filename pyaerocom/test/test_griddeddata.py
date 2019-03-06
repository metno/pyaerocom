#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""

import pytest
import numpy.testing as npt
from datetime import datetime
from pyaerocom.test.settings import TEST_RTOL, lustre_unavail
from pyaerocom import GriddedData

### Helpers that may be used in __main__ for testing
def _load_osuite():
    from pyaerocom.io.testfiles import get
    test_file = get()['models']['ecmwf_osuite']
    return GriddedData(test_file, var_name="od550aer")

def _load_cams_rean():
    from pyaerocom.io import ReadGridded
    r = ReadGridded(data_id="ECMWF_CAMS_REAN")
    return r.read_var('od550aer', ts_type='daily',
                      start=2010, stop=2013)
    
### fixtures
@lustre_unavail
@pytest.fixture(scope='module')
def data_cci():
    '''import example data from Aerosol CCI
    
    The fixture property makes sure that this "variable" is only created once
    for the entire scope of this test session within this module
    '''
    from pyaerocom.io.testfiles import get
    test_file = get()['models']['aatsr_su_v4.3']
    return GriddedData(test_file, var_name="od550aer")

@lustre_unavail
@pytest.fixture(scope='module')
def data_cams_rean():
    return _load_cams_rean()

@lustre_unavail
@pytest.fixture(scope='module')
def data_osuite():
    '''import example data from ECMWF_OSUITE
    
    The fixture property makes sure that this "variable" is only created once
    for the entire scope of this test session within this module
    '''
    return _load_osuite()    

### tests
@lustre_unavail
def test_longitude(data_cci, data_osuite):
    """Test if longitudes are defined right"""
    lons_cci = data_cci.longitude.points
    lons_osuite = data_osuite.longitude.points
    nominal = [-179.5, 179.5, -180.0, 179.6]
    vals = [lons_cci.min(), lons_cci.max(),
            lons_osuite.min(), lons_osuite.max()]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)
    
@lustre_unavail
def test_latitude(data_cci):
    """test latitude array"""
    nominal_eq = ['arc_degree', 0]
    vals_eq = [data_cci.latitude.units.name,
               int(sum(data_cci.latitude.points))]
    npt.assert_array_equal(nominal_eq, vals_eq)

@lustre_unavail    
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


@lustre_unavail
def test_downscale_time(data_cams_rean):
    
    data = data_cams_rean
    print(data)
    
    monthly = data.downscale_time('monthly')
    yearly = data.downscale_time('yearly')
    
    npt.assert_array_equal(data.shape, (1097, 161, 320))
    npt.assert_array_equal(monthly.shape, (37, 161, 320))
    npt.assert_array_equal(yearly.shape, (4, 161, 320))
    
    mean_vals = [data.mean(), monthly.mean(), yearly.mean()]
    npt.assert_allclose(actual=mean_vals,
                        desired=[0.1213392669166126, 
                                 0.12069144475849365, 
                                 0.11591256935171756], rtol=TEST_RTOL)

if __name__=="__main__":
    import warnings
    warnings.filterwarnings('ignore')
    pytest.main()
    
    
    
    