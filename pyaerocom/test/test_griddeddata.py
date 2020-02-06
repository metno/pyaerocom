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
from pyaerocom.io.test.test_readgridded import reader_reanalysis
from pyaerocom import GriddedData


TESTLATS =  [-10, 20]
TESTLONS =  [-120, 69]

### Helpers that may be used in __main__ for testing    
def _load_tm5_2010_monthly():
    fp = '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/TM5_AP3-CTRL2016/renamed/aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc'
    return GriddedData(fp)
    
### fixtures
@lustre_unavail
@pytest.fixture(scope='session')
def data_tm5():
    return _load_tm5_2010_monthly()

### tests
@lustre_unavail
def test_cams_rean_basic_properties(data_tm5):
    
    data =  data_tm5
    from iris.cube import Cube
    assert isinstance(data.cube, Cube)
    assert data.ts_type == 'monthly'
    assert str(data.start) == '2010-01-01T00:00:00.000000'
    assert str(data.stop) == '2010-12-31T23:59:59.999999'
    assert len(data.time.points) == 12
    assert data.data_id == 'TM5_AP3-CTRL2016'
    ff = ['aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc']
    assert [os.path.basename(x) for x in data.from_files] == ff
    assert data.shape == (12, 90, 120)
    assert data.lat_res == 2.0
    assert data.lon_res == 3.0
    
@lustre_unavail
def test_longitude(data_tm5):
    """Test if longitudes are defined right"""
    assert str(data_tm5.longitude.units) == 'degrees'
    
    lons = data_tm5.longitude.points
    nominal = [-181.5, 175.5]
    vals = [lons.min(), lons.max()]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)
    
@lustre_unavail
def test_latitude(data_tm5):
    """test latitude array"""
    assert str(data_tm5.latitude.units) == 'degrees'
    lats = data_tm5.latitude.points
    nominal = [-89, 89]
    vals = [lats.min(), lats.max()]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)

@lustre_unavail    
def test_time(data_tm5):
    """Test time dimension access and values"""
    time = data_tm5.time

    nominal_eq = ['julian', 'day since 1850-01-01 00:00:00.0000000 UTC', False]
    vals_eq = [time.units.calendar, 
               time.units.name, 
               isinstance(time.cell(0).point, datetime)]
    assert nominal_eq == vals_eq


@lustre_unavail
def test_resample_time(data_tm5):
    data = data_tm5
    
    yearly = data.resample_time('yearly')

    npt.assert_array_equal(yearly.shape, (1, 90, 120))
    
    # make sure means are preserved (more or less)
    mean_vals = [data.mean(), yearly.mean()]
    npt.assert_allclose(actual=mean_vals,
                        desired=[0.11865, 0.11865], rtol=TEST_RTOL)
@lustre_unavail
def test_interpolate(data_tm5):
    data = data_tm5
    
    itp = data.interpolate(latitude=TESTLATS, longitude=TESTLONS)
    
    assert type(itp) == GriddedData
    assert itp.shape == (12, 2, 2)
    
    desired = [0.13877, 0.13748]
    actual=[itp.mean(False), itp.mean(True)]
    npt.assert_allclose(actual=actual, 
                        desired=desired, 
                        rtol=TEST_RTOL)
    
@lustre_unavail
def test_to_time_series(data_tm5):
    
    latsm = [-9, 21]
    lonsm = [-118.5, 70.5]
    stats = data_tm5.to_time_series(latitude=TESTLATS, longitude=TESTLONS)
    
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
    
    pytest.main(['test_griddeddata.py'])
    