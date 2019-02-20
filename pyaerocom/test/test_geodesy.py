#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 10:36:15 2019

@author: jonasg
"""
import pytest
import os
from pyaerocom import geodesy, GEONUM_AVAILABLE, const
import numpy.testing as npt
if 'etopo1' in const.SUPPLDIRS and os.path.exists(const.SUPPLDIRS['etopo1']):
    ETOPO1_AVAIL = True
else:
    ETOPO1_AVAIL = False

TEST_LAT = 50.8
TEST_LON = 9

# custom skipif marker that is used below for test functions that 
# require geonum to be installed
geonum_avail = pytest.mark.skipif(not GEONUM_AVAILABLE,
                   reason='Skipping tests that require geonum. srtm.py library is '
                   'not installed')
etopo1_avail = pytest.mark.skipif(not ETOPO1_AVAIL,
                   reason='Skipping tests that require geonum. srtm.py library is '
                   'not installed')

always_skipped = pytest.mark.skipif(True==True, reason='Seek the answer')

def test_haversine():
    npt.assert_allclose(geodesy.haversine(0, 15, 0, 16), 111.2, atol=0.1)
    
def test_is_within_radius_km():
    assert geodesy.is_within_radius_km(0, 15, 0, 16, 1000, 111.2)
    
@always_skipped
def test_that_fails_but_should_be_skipped():
    assert 1==42
    
@geonum_avail
def test_srtm_altitude():
    npt.assert_almost_equal(geodesy.get_topo_altitude(TEST_LAT, TEST_LON), 207)
    
@geonum_avail
@etopo1_avail
def test_etopo_altitude():
    npt.assert_almost_equal(geodesy.get_topo_altitude(TEST_LAT, TEST_LON,
                                                      topo_dataset='etopo1'), 
                            217)
    
if __name__ == '__main__':

    test_haversine()
    test_is_within_radius_km()
    
    test_srtm_altitude()
    test_etopo_altitude()