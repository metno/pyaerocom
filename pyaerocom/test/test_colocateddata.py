#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import pytest
import numpy as np
from pandas import Timestamp
from pyaerocom import ColocatedData
from pyaerocom.conftest import TESTDATADIR, CHECK_PATHS

EXAMPLE_FILE = TESTDATADIR.joinpath(CHECK_PATHS['coldata_tm5_aeronet'])

def test_meta_access_filename():
    name = 'absc550aer_REF-EBAS-Lev3_MOD-CAM5-ATRAS_20100101_20101231_daily_WORLD-noMOUNTAINS.nc'

    meta = {'var_name': 'absc550aer',
            'ts_type': 'daily',
            'filter_name': 'WORLD-noMOUNTAINS',
            'start': Timestamp('2010-01-01 00:00:00'),
            'stop': Timestamp('2010-12-31 00:00:00'),
            'data_source': ['EBAS-Lev3', 'CAM5-ATRAS']}
    for k, v in ColocatedData.get_meta_from_filename(name).items():
        assert meta[k] == v

def test_read_colocated_data(coldata_tm5_aeronet):
    loaded = ColocatedData(str(EXAMPLE_FILE))
    mean_loaded = np.nanmean(loaded.data)
    mean_fixture = np.nanmean(coldata_tm5_aeronet.data.data)
    assert mean_fixture == mean_loaded

@pytest.mark.parametrize('input_args,latrange,lonrange,numst', [
({'region_id': 'WORLD'}, (-90,90), (-180, 180),8),
({'region_id': 'NHEMISPHERE'}, (0,90), (-180, 180),5),
({'region_id': 'EUROPE'}, (40,72), (-10, 40),2),
({'region_id': 'OCN'}, (-59.95,66.25), (-132.55,119.95),6),
])
def test_apply_latlon_filter(coldata_tm5_aeronet, input_args,
                             latrange, lonrange,numst):

    filtered = coldata_tm5_aeronet.apply_latlon_filter(**input_args)

    lats, lons = filtered.data.latitude.data, filtered.data.longitude.data
    assert lats.min() > latrange[0]
    assert lats.max() < latrange[1]
    assert lons.min() > lonrange[0]
    assert lons.max() < lonrange[1]
    assert len(filtered.data.station_name.data) == numst

@pytest.mark.parametrize('input_args,latrange,lonrange,numst', [

({'region_id': 'NHEMISPHERE'}, (0,90), (-180, 180),5),
({'region_id': 'EUROPE'}, (40,72), (-10, 40),2),
({'region_id': 'OCN'}, (-59.95,66.25), (-132.55,119.95),1),
])
def test_filter_region(coldata_tm5_aeronet,input_args, latrange, lonrange,
                       numst):
    filtered = coldata_tm5_aeronet.filter_region(**input_args)

    lats, lons = filtered.data.latitude.data, filtered.data.longitude.data
    assert lats.min() > latrange[0]
    assert lats.max() < latrange[1]
    assert lons.min() > lonrange[0]
    assert lons.max() < lonrange[1]
    assert len(filtered.data.station_name.data) == numst

if __name__=="__main__":

    import sys
    pytest.main(sys.argv)
