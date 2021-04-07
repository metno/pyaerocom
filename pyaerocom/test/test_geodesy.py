#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 10:36:15 2019

@author: jonasg
"""
from pyaerocom import geodesy
from pyaerocom.conftest import geonum_unavail, etopo1_unavail, rg_unavail
import numpy.testing as npt
import pytest

TEST_LAT = 50.8
TEST_LON = 9

@rg_unavail
@pytest.mark.parametrize('coords,countries', [
    ((52, 12), ['Germany']),
    ([(46.1956, 6.21125), (55.398, 10.3669)], ['France', 'Denmark'])
    ])
def test_get_country_info_coords(coords, countries):
    for i, res in enumerate(geodesy.get_country_info_coords(coords)):
        assert isinstance(res, dict)
        assert 'country' in res
        assert res['country'] == countries[i]

def test_haversine():
    npt.assert_allclose(geodesy.haversine(0, 15, 0, 16), 111.2, atol=0.1)

def test_is_within_radius_km():
    assert geodesy.is_within_radius_km(0, 15, 0, 16, 1000, 111.2)

@geonum_unavail
@pytest.mark.skip(reason='https://github.com/tkrajina/srtm.py/issues/51')
def test_srtm_altitude():
    npt.assert_almost_equal(geodesy.get_topo_altitude(TEST_LAT, TEST_LON), 207)

@geonum_unavail
@etopo1_unavail
def test_etopo_altitude():
    npt.assert_almost_equal(geodesy.get_topo_altitude(TEST_LAT, TEST_LON,
                                                      topo_dataset='etopo1'), 217)

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
