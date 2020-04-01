#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import pytest
import pandas as pd
import numpy as np
import numpy.testing as npt
from pyaerocom.conftest import DATA_ACCESS, TEST_RTOL
from cf_units import Unit

RTOL = TEST_RTOL

@pytest.fixture
def stat1():
    return DATA_ACCESS['station_data1']

@pytest.fixture
def stat2():
    return DATA_ACCESS['station_data2']

def test_default_vert_grid(stat1):
    grid = stat1.default_vert_grid
    assert grid.mean() == 7375 #m
    step = np.unique(np.diff(grid))
    assert len(step) == 1
    assert step[0] == 250

@pytest.mark.parametrize('var_name', ['od550aer', 'ec550aer'])
def test_has_var(stat1, var_name):
    assert stat1.has_var(var_name)

@pytest.mark.parametrize('var_name,ts_type,how,apply_constraints,min_num_obs,inplace,numts,t0', [
    ('od550aer','yearly','mean',True,None,False,1,pd.Timestamp('30-6-2007')),
    ('od550aer','5daily','mean',False,None,False,56,pd.Timestamp('1-1-2007')),
    ('ec550aer','monthly','mean',False,None,True,10,pd.Timestamp('15-1-2007')),
    ('conco3','3daily','mean',False,None,True,93,pd.Timestamp('1-1-2007')),
    ])
def test_resample_time(stat2,var_name,ts_type,how,
                      apply_constraints, min_num_obs, 
                      inplace,numts,t0):
    result = stat2.resample_time(var_name,ts_type,how,
                                 apply_constraints, min_num_obs, 
                                 inplace)
    assert result['ts_type'] == None
    assert result['var_info'][var_name]['ts_type'] == ts_type
    assert len(result[var_name]) == numts
    assert result[var_name].index[0] == t0
    
    
@pytest.mark.parametrize('var_name,val', [
    ('od550aer', 'daily'), 
    ('ec550aer', 'monthly'),
    ('conco3', '3daily')
    ])    
def test_get_var_ts_type(stat2, var_name, val):
    assert stat2.get_var_ts_type(var_name) == val
    
def test_get_unit(stat1, stat2):
    
    assert stat1.get_unit('ec550aer') == Unit('m-1')
    assert stat2.get_unit('ec550aer') == Unit('1/Mm')
    
def test_check_var_unit_aerocom(stat1):
    stat1.check_var_unit_aerocom('ec550aer')
 
@pytest.mark.parametrize(('var_name,is_ts_type,sort_index,check_overlaps,'
                          'check_coords,tsnum,mean,overlap'), [
    ('ec550aer',None,True,True,True,60,3e7,True)
    
    ])
def test_merge_other(stat1, stat2, var_name, is_ts_type, 
                     sort_index, check_overlaps, check_coords,tsnum,
                     mean,overlap):
    merged = stat1.merge_other(stat2, var_name, is_ts_type, 
                               sort_index, check_overlaps, check_coords)
    data = merged[var_name]
    assert isinstance(data, pd.Series)
    assert len(data) == tsnum
    npt.assert_allclose(mean, np.nanmean(data))
    has_overlap = var_name in merged['overlap']
    assert overlap == has_overlap
    if has_overlap:
        assert isinstance(merged['overlap'][var_name], pd.Series)
    
    
if __name__=="__main__":
    import sys
    pytest.main(sys.argv)