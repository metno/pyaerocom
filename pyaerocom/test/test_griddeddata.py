#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""

import pytest
import os
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
    
def _load_tm5_2010_monthly():
    fp = '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/TM5_AP3-CTRL2016/renamed/aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc'
    return GriddedData(fp)
    
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
def data_tm5():
    return _load_tm5_2010_monthly()

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
def test_cams_rean_basic_properties(data_cams_rean):
    
    data =  data_cams_rean
    assert data.ts_type == 'daily'
    assert str(data.start) == '2010-01-01T00:00:00.000000'
    assert str(data.stop) == '2012-12-31T23:59:59.999999'
    assert len(data.time.points) == 1096
    assert data.data_id == 'ECMWF_CAMS_REAN'
    ff = ['aerocom.ECMWF_CAMS_REAN.daily.od550aer.2010.nc',
          'aerocom.ECMWF_CAMS_REAN.daily.od550aer.2011.nc',
          'aerocom.ECMWF_CAMS_REAN.daily.od550aer.2012.nc']
    assert [os.path.basename(x) for x in data.from_files] == ff
    assert data.shape == (1096, 161, 320)
    
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
def test_resample_time(data_cams_rean):
    data = data_cams_rean
    
    monthly = data.resample_time('monthly')
    yearly = data.resample_time('yearly')
    
    npt.assert_array_equal(data.shape, (1096, 161, 320))
    npt.assert_array_equal(monthly.shape, (36, 161, 320))
    npt.assert_array_equal(yearly.shape, (3, 161, 320))
    
    mean_vals = [data.mean(), monthly.mean(), yearly.mean()]
    npt.assert_allclose(actual=mean_vals,
                        desired=[0.14915, 
                                 0.14906, 
                                 0.14906], rtol=TEST_RTOL)
@lustre_unavail
def test_interpolate(data_tm5):
    data = data_tm5
    #test_resample_time(data)
    
    
    lats = [-10, 20]
    lons = [-120, 69]
    
    itp = data.interpolate(latitude=lats, longitude=lons)
    
    assert type(itp) == GriddedData
    assert itp.shape == (12, 2, 2)
    npt.assert_allclose(actual=[itp.mean(False),
                                itp.mean(True)], 
                        desired=[0.138774,
                                0.137484], 
                                 rtol=TEST_RTOL)
    
@lustre_unavail
def test_to_time_series(data_tm5):
    lats = [-10, 20]
    lons = [-120, 69]
    
    latsm = [-9, 21]
    lonsm = [-118.5, 70.5]
    stats = data_tm5.to_time_series(latitude=lats, longitude=lons)
    
    lats_actual = []
    lons_actual = []
    means_actual = []

    for stat in stats:
        lats_actual.append(stat.latitude)
        lons_actual.append(stat.longitude)
        means_actual.append(stat.od550aer.mean())
    npt.assert_array_equal(lats_actual, latsm)
    npt.assert_array_equal(lons_actual, lonsm)
    npt.assert_allclose(means_actual, [0.101353, 0.270886], rtol=TEST_RTOL)

if __name__=="__main__":
    
    data = _load_tm5_2010_monthly()
    
    test_interpolate(data)
    test_to_time_series(data)
    