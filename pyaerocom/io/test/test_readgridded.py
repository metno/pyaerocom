#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""

# TODO: Docstrings
import pytest
import numpy.testing as npt
from pandas import Timestamp, DataFrame
from pyaerocom.test.settings import TEST_RTOL, lustre_unavail
from pyaerocom.io.readgridded import ReadGridded

START = "1-1-2003"
STOP = "31-12-2007"

def make_dataset():
    return ReadGridded(data_id="ECMWF_CAMS_REAN")

@lustre_unavail
@pytest.fixture(scope='session')
def dataset():
    return make_dataset()
    
@lustre_unavail    
def test_file_info(dataset):

    assert isinstance(dataset.file_info, DataFrame)
    assert len(dataset.file_info.columns) == 11, 'Mismatch colnum file_info (df)'

@lustre_unavail    
def test_years_available(dataset):
    years = list(range(2003, 2020)) + [9999]
    npt.assert_array_equal(dataset.years_avail, years)    

@lustre_unavail
def test_data_dir(dataset):
    assert dataset.data_dir == '/lustre/storeA/project/aerocom/aerocom-users-database/ECMWF/ECMWF_CAMS_REAN/renamed'
    
@lustre_unavail    
def test_read_var(dataset):
    from numpy import datetime64
    d = dataset.read_var(var_name="od550aer", ts_type="daily",
                         start=START, stop=STOP)
    npt.assert_array_equal([d.var_name, sum(d.shape), d.start, d.stop],
                           ["od550aer", 1826 + 161 + 320,
                            datetime64('2003-01-01T00:00:00.000000'),
                            datetime64('2007-12-31T23:59:59.999999')])
    vals = [d.longitude.points[0],
            d.longitude.points[-1],
            d.latitude.points[0],
            d.latitude.points[-1],
            d[0].mean()]
    nominal = [-180.0, 178.875, 90.0, -90.0, 0.08924646]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)
    return d

@lustre_unavail
def test_prefer_longer(dataset):
    daily = dataset.read_var('od550aer', ts_type='monthly', 
                             flex_ts_type=True,
                             prefer_longer=True)
    assert daily.ts_type == 'daily'
    
@lustre_unavail
def test_read_vars(dataset):
    d = dataset.read(['od440aer', 'od550aer', 'od865aer'], 
                     ts_type="daily", start=START, stop=STOP)
    vals = [len(d),
            sum(d[0].shape),
            sum(d[1].shape),
            sum(d[2].shape)]
    nominal = [3, 2307, 2307, 2307]
    npt.assert_array_equal(vals, nominal)
    
    vals = [d[0][1825].mean(), d[1][1825].mean(), d[2][1825].mean()]
    nominal = [0.11754113, 0.09734518, 0.06728536]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)
    return d
    
if __name__=="__main__":
    ds = make_dataset()
    test_years_available(ds)
    test_file_info(ds)
    test_read_vars(ds)
    
    