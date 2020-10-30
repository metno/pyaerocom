#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import pytest
import numpy as np
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
    import sys
    pytest.main(sys.argv)
