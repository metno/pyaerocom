#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import numpy as np
import pytest
from pyaerocom.test.settings import DATA_ACCESS
#import numpy.testing as npt
from pyaerocom import helpers

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
def test_isnumeric():
    assert helpers.isnumeric(3)
    assert helpers.isnumeric(3.3455)
    assert helpers.isnumeric(np.complex(1,2))
    
def test_isrange():
    assert helpers.isrange((0, 1))
    assert helpers.isrange([10, 20])
        
def test_merge_station_data():
    pass

def test__get_pandas_freq_and_loffset():
    val = helpers._get_pandas_freq_and_loffset('monthly')
    assert val == ('MS', '14D')


def _make_timeseries_synthetic():
    from pandas import Series, DatetimeIndex
    idx = DatetimeIndex(freq='D', start='2000', periods=90)
    vals = np.arange(len(idx))
    
    return  Series(vals, idx)

@pytest.fixture(scope='module')
def timeseries_synthetic():
    return _make_timeseries_synthetic()\

def test_resample_timeseries(timeseries_synthetic):
    s1 = helpers.resample_timeseries(timeseries_synthetic, 'monthly')
    
    assert len(s1) == 3
    for time in s1.index:
        assert time.year == 2000, time.year
        assert time.day == 15, time.day
    
def test_same_meta_dict():
    d1 =  dict(station_name = 'bla',
               station_id = 'blub', 
               latitude = 33, 
               longitude = 15, 
               altitude = 400,
               PI='pi1')
    d2 =  dict(station_name = 'bla',
               station_id = 'blub1', 
               latitude = 33, 
               longitude = 15, 
               altitude = 401,
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
    from pandas import Timestamp
    assert start == Timestamp('2000')
    assert stop == Timestamp('2000-12-31 23:59:59')
            
def to_datestring_YYYYMMDD():
    pass

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


if __name__=="__main__":
    
    test_get_standarad_name()
    test_get_standard_unit()
    test_start_stop_from_year()
    test__get_pandas_freq_and_loffset()
    test_resample_timeseries(_make_timeseries_synthetic())
    test_same_meta_dict()
    
    
    stat1 = DATA_ACCESS['station_data1']
    stat2 = DATA_ACCESS['station_data2']
    
    merged_ec = helpers.merge_station_data([stat1, stat2],
                                           var_name='ec550aer')
    
    
    
    
    
    
    
    
    