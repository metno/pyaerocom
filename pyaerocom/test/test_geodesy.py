#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 10:36:15 2019

@author: jonasg
"""
from pyaerocom import geodesy
from pyaerocom.test.settings import geonum_unavail, etopo1_unavail
import numpy.testing as npt


TEST_LAT = 50.8
TEST_LON = 9


def test_haversine():
    npt.assert_allclose(geodesy.haversine(0, 15, 0, 16), 111.2, atol=0.1)
    
def test_is_within_radius_km():
    assert geodesy.is_within_radius_km(0, 15, 0, 16, 1000, 111.2)
    
@geonum_unavail
def test_srtm_altitude():
    npt.assert_almost_equal(geodesy.get_topo_altitude(TEST_LAT, TEST_LON), 207)
    
@geonum_unavail
@etopo1_unavail
def test_etopo_altitude():
    npt.assert_almost_equal(geodesy.get_topo_altitude(TEST_LAT, TEST_LON,
                                                      topo_dataset='etopo1'), 
                            217)
    
if __name__ == '__main__':

    test_haversine()
    test_is_within_radius_km()
    
    test_srtm_altitude()
    test_etopo_altitude()