#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import numpy as np
import numpy.testing as npt
import pytest
import xarray as xr
from pandas import Series, date_range, Timestamp

from pyaerocom import helpers, StationData
from pyaerocom.conftest import does_not_raise_exception
from pyaerocom.exceptions import (DataCoverageError, TemporalResolutionError,
                                  UnitConversionError)

def test_get_standarad_name():
    assert (helpers.get_standard_name('od550aer') ==
            'atmosphere_optical_thickness_due_to_ambient_aerosol_particles')

def test_get_standard_unit():
    assert helpers.get_standard_unit('ec550aer') == '1/Mm'

def test_get_lowest_resolution():
    assert helpers.get_lowest_resolution('3hourly',
                                         'hourly',
                                         'monthly',
                                         'yearly') == 'yearly'
@pytest.mark.parametrize('val', [3, 3.3455, np.complex(1,2)])
def test_isnumeric(val):
    assert helpers.isnumeric(val)

@pytest.mark.parametrize('val,result', [
    ((0, 1), True),
    ([10,20], True),
    ([10,20,30], False),
    ])
def test_isrange(val,result):
    assert helpers.isrange(val) == result

@pytest.mark.parametrize('use,var_name,pref_attr,sort_by_largest,fill_missing_nan,add_meta_keys,raises,num,tst,mean', [
    ('concpm10', 'concpm10',None,True,True,None,does_not_raise_exception(),730,'daily',17.93),
    ('concpm10', 'concpm10','awesomeness',True,True,None,does_not_raise_exception(),730,'daily',17.93),
    ('concpm10', 'concpm10','awesomeness',False,True,None,does_not_raise_exception(),730,'daily',15),
    ('concpm10_X2', 'concpm10',None,True,True,None,pytest.raises(UnitConversionError),None,None,None),
    ('all', 'concpm10',None,True,True,None,pytest.raises(TemporalResolutionError),None,None,None),
    ('concpm10_X', 'concpm10',None,True,True,None,pytest.raises(TemporalResolutionError),None,None,None),
    ('od550aer', 'od550aer',None,True,True,None,does_not_raise_exception(),67,'60daily',0.51),
    ('od550aer', 'od550aer','awesomeness',True,True,None,does_not_raise_exception(),67,'60daily',0.59),
    ('od550aer', 'od550aer','awesomeness',False,True,None,does_not_raise_exception(),67,'60daily',0.51),
    ('od550aer', 'concpm10',None,True,True,None,pytest.raises(DataCoverageError),None,None,None),

    ])
def test_merge_station_data(statlist,use,var_name,pref_attr,sort_by_largest,fill_missing_nan,add_meta_keys,raises,num,tst,mean):
    with raises:
        stats = [x.copy() for x in statlist[use]]
        stat = helpers.merge_station_data(stats,var_name,pref_attr,
                                   sort_by_largest,fill_missing_nan,
                                   add_meta_keys)
        assert isinstance(stat, StationData)
        vardata = stat[var_name]
        assert len(vardata) == num
        assert stat.get_var_ts_type(var_name) == tst
        avg = np.mean(vardata)
        npt.assert_allclose(avg, mean, rtol=1e-2)

def test__get_pandas_freq_and_loffset():
    val = helpers._get_pandas_freq_and_loffset('monthly')
    assert val == ('MS', '14D')

def _make_timeseries_synthetic():

    idx = date_range(start="2000", periods=90, freq='D')

    vals = np.arange(len(idx))
    return  Series(vals, idx)

@pytest.fixture(scope='module')
def timeseries_synthetic():
    return _make_timeseries_synthetic()

def test_resample_timeseries(timeseries_synthetic):
    s1 = helpers.resample_timeseries(timeseries_synthetic,
                                     'monthly')
    assert len(s1) == 3
    for time in s1.index:
        assert time.year == 2000, time.year
        assert time.day == 15, time.day

def test_same_meta_dict():
    d1 = dict(station_name='bla',
              station_id='blub',
              latitude=33,
              longitude=15,
              altitude=400,
              PI='pi1')
    d2 = dict(station_name='bla',
              station_id='blub1',
              latitude=33,
              longitude=15,
              altitude=401,
              PI='pi2')

    assert helpers.same_meta_dict(d1, d2) == False

def test_to_pandas_timestamp():
    pass

def test_to_datetime64():
    pass

def test_is_year():
    assert helpers.is_year(2010)

def test_start_stop():
    pass

def test_datetime2str():
    pass
def test_start_stop_str():
    pass

def test_start_stop_from_year():
    start, stop = helpers.start_stop_from_year(2000)
    assert start == Timestamp('2000')
    assert stop == Timestamp('2000-12-31 23:59:59')

@pytest.mark.parametrize(
    'input,expected', [
        ('20100101', '20100101'),
        (helpers.to_pandas_timestamp('20100101'), '20100101')
    ])
def test_to_datestring_YYYYMMDD(input, expected):
    assert helpers.to_datestring_YYYYMMDD(input) == expected

def test_cftime_to_datetime64():
    pass

def get_constraint():
    pass

def test_get_lat_rng_constraint():
    pass

def test_get_lon_rng_constraint():
    pass

def test_get_time_rng_constraint():
    pass

def test_extract_latlon_dataarray():
    cube = helpers.make_dummy_cube_latlon(lat_res_deg=1, lon_res_deg=1, lat_range=[10, 20], lon_range=[10, 20])
    data = xr.DataArray.from_iris(cube)
    # First coordinate does not exist in the dataarray.
    lat = [15, 15, 18]
    lon = [1, 15, 18]
    subset = helpers.extract_latlon_dataarray(data, lat, lon, check_domain=True)
    assert isinstance(subset, xr.DataArray)
    assert len(subset.lat) == len(lat) - 1 and len(subset.lon) == len(lon) -1

@pytest.mark.parametrize('lat,lon,expectation', [
    ([], [], pytest.raises(DataCoverageError)),
    ([1,2], [-1,2], pytest.raises(DataCoverageError)),
    ([15], [15], does_not_raise_exception())
    ])
def test_extract_latlon_dataarray_no_matches(lat, lon, expectation):
    cube = helpers.make_dummy_cube_latlon(lat_res_deg=1,
                                          lon_res_deg=1,
                                          lat_range=[10, 20],
                                          lon_range=[10, 20])
    data = xr.DataArray.from_iris(cube)
    with expectation:
        helpers.extract_latlon_dataarray(data, lat, lon, check_domain=True)

@pytest.mark.parametrize("date,ts_type,expected", [
    ("2000-02-18", "monthly", 29),  # February leap year
    ("2000-02-18", "yearly", 366),  # Leap year
    ("2001-02-18", "monthly", 28),  # February non leap year
    ("2001-02-18", "daily", 1),     # Daily
    ("2001-02-18", "yearly", 365)]) # Non leap year
def test_seconds_in_periods(date, ts_type, expected):
    seconds_in_day = 24*60*60
    ts = np.datetime64(date)
    seconds = helpers.seconds_in_periods(ts, ts_type)
    assert seconds == expected*seconds_in_day

if __name__ == "__main__":
    import sys
    pytest.main(sys.argv)
