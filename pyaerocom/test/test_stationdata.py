#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import pytest
import numpy as np
import numpy.testing as npt
from pyaerocom.test import settings
import pyaerocom.exceptions as exc
from cf_units import Unit

RTOL = settings.TEST_RTOL

@pytest.fixture
def stat1():
    return settings.DATA_ACCESS['station_data1']

@pytest.fixture
def stat2():
    return settings.DATA_ACCESS['station_data2']

def test_default_vert_grid(stat1):
    grid = stat1.default_vert_grid
    assert grid.mean() == 7375 #m
    step = np.unique(np.diff(grid))
    assert len(step) == 1
    assert step[0] == 250

def test_has_var(stat1, stat2):
    assert stat1.has_var('od550aer')
    assert stat2.has_var('conco3')
    
def test_get_unit(stat1, stat2):
    
    assert stat1.get_unit('ec550aer') == Unit('m-1')
    assert stat2.get_unit('ec550aer') == Unit('1/Mm')
    
def test_check_var_unit_aerocom(stat1):
    assert stat1.get_unit('ec550aer') == Unit('m-1')
    stat1.check_var_unit_aerocom('ec550aer')
    assert stat1.get_unit('ec550aer') == Unit('1/Mm')
    

    
if __name__=="__main__":
    STAT1 = settings.DATA_ACCESS['station_data1']
    STAT2 = settings.DATA_ACCESS['station_data2']
    
    stat1 = STAT1
    stat2 = STAT2
    
    ec_mean =  np.mean(stat1.ec550aer)
    try:
        stat1.check_unit('ec550aer')
    except exc.DataUnitError:
        from pyaerocom import Variable
        stat1.convert_unit('ec550aer', Variable('ec550aer').units)
    
    from pyaerocom.units_helpers import unit_conversion_fac
    
    fac = unit_conversion_fac('m-1', '1/Mm')
    print(stat1)
    
    npt.assert_allclose(ec_mean * fac,
                        stat1.ec550aer.mean(), 
                        rtol=RTOL)
    
    merged = stat1.merge_other(stat2, 'ec550aer')
    print(merged)
    
    
    