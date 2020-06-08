#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:48:45 2020

@author: jonasg
"""
import os
import xarray as xr
import iris

from pyaerocom import const
import pyaerocom.helpers_landsea_masks as lsm

TEST_REGIONS = const.HTAP_REGIONS[:2]

def test_availabe_region_masks():
    assert lsm.available_htap_masks() == ['PAN', 'EAS', 'NAF', 'MDE', 'LAND',
                                          'SAS', 'SPO', 'OCN', 'SEA', 'RBU',
                                          'EEUROPE', 'NAM', 'WEUROPE', 'SAF',
                                          'USA', 'SAM', 'EUR', 'NPO', 'MCA']

def test_download_htap_masks():

    success = lsm.download_htap_masks(TEST_REGIONS)
    mask_names = []
    for path in success:
        assert os.path.exists(path)
        assert os.path.join('MyPyaerocom', 'filtermasks') in path
        mask_names.append(os.path.basename(path))
    assert mask_names == ['PANhtap.0.1x0.1deg.nc', 'EAShtap.0.1x0.1deg.nc']

def test_get_htap_mask_files():
    mask_names = []
    for file in lsm.get_htap_mask_files(*TEST_REGIONS):
        mask_names.append(os.path.basename(file))
    assert mask_names == ['PANhtap.0.1x0.1deg.nc', 'EAShtap.0.1x0.1deg.nc']

def test_load_region_mask_xr():
    mask = lsm.load_region_mask_xr(*TEST_REGIONS)
    assert isinstance(mask, xr.DataArray)
    pixnum = int(mask.sum())
    assert pixnum == 193355, pixnum

def test_load_region_mask_iris():
    mask = lsm.load_region_mask_iris(*TEST_REGIONS)
    assert isinstance(mask, iris.cube.Cube)
    pixnum = int(mask.data.sum())
    assert pixnum == 193355, pixnum

def test_get_mask_value():
    mask = lsm.load_region_mask_xr('WEUROPE')

    assert lsm.get_mask_value(50, 5, mask)
    assert not lsm.get_mask_value(50, 15, mask)

def test_check_all_htap_available():
    should_be =['EAShtap.0.1x0.1deg.nc', 'EEUROPEhtap.0.1x0.1deg.nc',
                'EURhtap.0.1x0.1deg.nc', 'LANDhtap.0.1x0.1deg.nc',
                'MCAhtap.0.1x0.1deg.nc', 'MDEhtap.0.1x0.1deg.nc',
                'NAFhtap.0.1x0.1deg.nc', 'NAMhtap.0.1x0.1deg.nc',
                'NPOhtap.0.1x0.1deg.nc', 'OCNhtap.0.1x0.1deg.nc',
                'PANhtap.0.1x0.1deg.nc', 'RBUhtap.0.1x0.1deg.nc',
                'SAFhtap.0.1x0.1deg.nc', 'SAMhtap.0.1x0.1deg.nc',
                'SAShtap.0.1x0.1deg.nc', 'SEAhtap.0.1x0.1deg.nc',
                'SPOhtap.0.1x0.1deg.nc', 'USAhtap.0.1x0.1deg.nc',
                'WEUROPEhtap.0.1x0.1deg.nc']

    files = lsm.check_all_htap_available()
    assert sorted([os.path.basename(x) for x in files]) == should_be

if __name__ == '__main__':

    test_availabe_region_masks()
    test_get_mask_value()

    test_download_htap_masks()
    test_get_htap_mask_files()
    test_load_region_mask_xr()
    test_load_region_mask_iris()
    test_check_all_htap_available()
