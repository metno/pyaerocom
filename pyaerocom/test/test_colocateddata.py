#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import pytest
import numpy as np
import pandas as pd
import xarray as xr
from pyaerocom import ColocatedData
from pyaerocom.exceptions import DataCoverageError, DataDimensionError
from pyaerocom.conftest import TESTDATADIR, CHECK_PATHS, does_not_raise_exception

def make_fake_4d_coldata():
    _lats_fake = np.arange(30,70,10)
    _lons_fake = np.arange(0,40,10)
    _time_fake = pd.date_range('2010-01', '2010-03', freq='MS')
    _data_fake = np.ones((2, len(_time_fake), len(_lats_fake), len(_lons_fake)))

    coords = {'data_source' : ['obs', 'mod'],
              'time'        : _time_fake,
              'latitude'    : _lats_fake,
              'longitude'   : _lons_fake
              }

    dims = ['data_source', 'time', 'latitude', 'longitude']

    return ColocatedData(data=_data_fake, coords=coords, dims=dims)

EXAMPLE_FILE = TESTDATADIR.joinpath(CHECK_PATHS['coldata_tm5_aeronet'])

COLDATA = ColocatedData(str(EXAMPLE_FILE))
COLDATA_NODIMS = ColocatedData(np.ones((2,1,1)))
COLDATA_4D_FAKE = make_fake_4d_coldata()

@pytest.mark.parametrize('data,kwargs,raises', [
    (None, {}, pytest.raises(AttributeError)),
    (EXAMPLE_FILE, {}, does_not_raise_exception()),
    (str(EXAMPLE_FILE), {}, does_not_raise_exception()),
    ('Blaaaaa', {}, pytest.raises(IOError)),
    (None, dict(bla=42), pytest.raises(AttributeError)),
    (np.ones((3, 2, 3)), {}, pytest.raises(DataDimensionError)),
    (np.ones((3)), {}, pytest.raises(DataDimensionError)),
    (np.ones((2,3,4)), {}, does_not_raise_exception()),
    ({},{},pytest.raises(ValueError))
    ])
def test_ColocatedData__init__(data,kwargs,raises):
    with raises:
        cd = ColocatedData(data=data, **kwargs)
        assert isinstance(cd.data, xr.DataArray)

@pytest.mark.parametrize('data,raises', [
    ('Blaaa', pytest.raises(ValueError)),
    (xr.DataArray(), does_not_raise_exception())
    ])
def test_ColocatedData_data(data, raises):
    col = ColocatedData()
    with raises:
        col.data = data
        assert col.data is data

def test_ColocatedData_name():
    cd = ColocatedData(np.ones((2,1,1)))
    assert cd.name is None
    cd.name = 'bla'
    assert cd.name == cd.data.name == 'bla'

@pytest.mark.parametrize('cd,raises', [
    (COLDATA_NODIMS, pytest.raises(AttributeError)),
    (COLDATA, does_not_raise_exception())
    ])
def test_ColocatedData_data_source(cd,raises):
    with raises:
        ds = cd.data_source
        assert isinstance(ds, xr.DataArray)
        assert len(ds) == 2

@pytest.mark.parametrize('cd,raises', [
    (COLDATA_NODIMS, pytest.raises(AttributeError)),
    (COLDATA, does_not_raise_exception())
    ])
def test_ColocatedData_var_name(cd,raises):
    with raises:
        val = cd.var_name
        assert isinstance(val, list)

@pytest.mark.parametrize('cd,raises', [
    (COLDATA_NODIMS, pytest.raises(AttributeError)),
    (COLDATA, does_not_raise_exception())
    ])
def test_ColocatedData_latitude(cd,raises):
    with raises:
        val = cd.latitude
        assert isinstance(val, xr.DataArray)

@pytest.mark.parametrize('cd,raises', [
    (COLDATA_NODIMS, pytest.raises(AttributeError)),
    (COLDATA, does_not_raise_exception())
    ])
def test_ColocatedData_longitude(cd,raises):
    with raises:
        val = cd.longitude
        assert isinstance(val, xr.DataArray)

@pytest.mark.parametrize('cd,raises', [
    (COLDATA_NODIMS, pytest.raises(AttributeError)),
    (COLDATA, does_not_raise_exception())
    ])
def test_ColocatedData_time(cd,raises):
    with raises:
        val = cd.time
        assert isinstance(val, xr.DataArray)

@pytest.mark.parametrize('cd,raises', [
    (COLDATA_NODIMS, pytest.raises(ValueError)),
    (COLDATA, does_not_raise_exception())
    ])
def test_ColocatedData_ts_type(cd,raises):
    with raises:
        val = cd.ts_type
        assert isinstance(val, str)

@pytest.mark.parametrize('cd,raises', [
    (COLDATA_NODIMS, pytest.raises(KeyError)),
    (COLDATA, does_not_raise_exception())
    ])
def test_ColocatedData_units(cd,raises):
    with raises:
        val = cd.units
        assert isinstance(val, list)
        assert [isinstance(x, str) for x in val]


@pytest.mark.parametrize('cd,num_coords,raises', [
    (COLDATA_NODIMS, 0, pytest.raises(ValueError)),
    (COLDATA, 8, does_not_raise_exception()),
    (COLDATA_4D_FAKE, 16, does_not_raise_exception())
    ])
def test_ColocatedData_get_coords_valid_obs(cd,num_coords,raises):
    with raises:
        val = cd.get_coords_valid_obs()
        assert isinstance(val, list)
        assert len(val) == 2
        assert len(val[0]) == len(val[1]) == num_coords

def test_meta_access_filename():
    name = 'absc550aer_REF-EBAS-Lev3_MOD-CAM5-ATRAS_20100101_20101231_daily_WORLD-noMOUNTAINS.nc'

    meta = {'var_name': 'absc550aer',
            'ts_type': 'daily',
            'filter_name': 'WORLD-noMOUNTAINS',
            'start': pd.Timestamp('2010-01-01 00:00:00'),
            'stop': pd.Timestamp('2010-12-31 00:00:00'),
            'data_source': ['EBAS-Lev3', 'CAM5-ATRAS']}
    _meta = ColocatedData.get_meta_from_filename(name)
    for k, v in _meta.items():
        assert meta[k] == v

def test_read_colocated_data(coldata_tm5_aeronet):
    loaded = ColocatedData(EXAMPLE_FILE)
    mean_loaded = np.nanmean(loaded.data)
    mean_fixture = np.nanmean(coldata_tm5_aeronet.data.data)
    assert mean_fixture == mean_loaded

@pytest.mark.parametrize('input_args,latrange,lonrange,numst,raises', [
    ({'region_id': 'RBU'}, (29.45, 66.26), (22, -170), 2, does_not_raise_exception()), # crosses lon=180 border
    ({'region_id': 'PAN'}, None, None, 0, pytest.raises(DataCoverageError)), # crosses lon=180 border
    ({'region_id': 'NAM'}, None, None, 0, pytest.raises(DataCoverageError)), # crosses lon=180 border
    ({'region_id': 'WORLD'}, (-90,90), (-180, 180),8, does_not_raise_exception()),
    ({'region_id': 'NHEMISPHERE'}, (0, 90), (-180, 180), 5, does_not_raise_exception()),
    ({'region_id': 'EUROPE'}, (40,72), (-10, 40),2, does_not_raise_exception()),
    ({'region_id': 'OCN'}, (-90,90), (-180, 180), 8, does_not_raise_exception()),

])
def test_apply_latlon_filter(coldata_tm5_aeronet, input_args,
                             latrange, lonrange,numst,raises):
    with raises:
        filtered = coldata_tm5_aeronet.apply_latlon_filter(**input_args)

        lats, lons = filtered.data.latitude.data, filtered.data.longitude.data
        assert len(filtered.data.station_name.data) == numst
        if numst > 0:
            assert lats.min() > latrange[0]
            assert lats.max() < latrange[1]
            if lonrange[0] < lonrange[1]:
                assert lons.min() > lonrange[0]
                assert lons.max() < lonrange[1]
            else:
                assert (-180 < lons.min() < lonrange[1] or
                        lonrange[0] < lons.min() <  180)

                assert (-180 < lons.max() < lonrange[1] or
                        lonrange[0] < lons.max() <  180)


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
