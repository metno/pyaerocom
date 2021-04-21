#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import pytest
from matplotlib.axes import Axes
import numpy as np
import numpy.testing as npt
import os
import pandas as pd
import xarray as xr
from pyaerocom import ColocatedData
from pyaerocom.exceptions import DataCoverageError, DataDimensionError
from pyaerocom.conftest import TESTDATADIR, CHECK_PATHS, does_not_raise_exception

EXAMPLE_FILE = TESTDATADIR.joinpath(CHECK_PATHS['coldata_tm5_aeronet'])
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

@pytest.mark.parametrize('which,raises', [
    ('fake_nodims', pytest.raises(AttributeError)),
    ('tm5_aeronet', does_not_raise_exception())
    ])
def test_ColocatedData_data_source(coldata, which, raises):
    cd = coldata[which]
    with raises:
        ds = cd.data_source
        assert isinstance(ds, xr.DataArray)
        assert len(ds) == 2

@pytest.mark.parametrize('which,raises', [
    ('fake_nodims', pytest.raises(AttributeError)),
    ('tm5_aeronet', does_not_raise_exception())
    ])
def test_ColocatedData_var_name(coldata, which, raises):
    cd = coldata[which]
    with raises:
        val = cd.var_name
        assert isinstance(val, list)

@pytest.mark.parametrize('which,raises', [
    ('fake_nodims', pytest.raises(AttributeError)),
    ('tm5_aeronet', does_not_raise_exception())
    ])
def test_ColocatedData_latitude(coldata, which, raises):
    cd = coldata[which]
    with raises:
        val = cd.latitude
        assert isinstance(val, xr.DataArray)

@pytest.mark.parametrize('which,raises', [
    ('fake_nodims', pytest.raises(AttributeError)),
    ('tm5_aeronet', does_not_raise_exception())
    ])
def test_ColocatedData_longitude(coldata, which, raises):
    cd = coldata[which]
    with raises:
        val = cd.longitude
        assert isinstance(val, xr.DataArray)

@pytest.mark.parametrize('which,raises', [
    ('fake_nodims', pytest.raises(AttributeError)),
    ('tm5_aeronet', does_not_raise_exception())
    ])
def test_ColocatedData_time(coldata,which,raises):
    cd = coldata[which]
    with raises:
        val = cd.time
        assert isinstance(val, xr.DataArray)

@pytest.mark.parametrize('which,raises,value', [
    ('fake_nodims', pytest.raises(AttributeError), None),
    ('tm5_aeronet', does_not_raise_exception(), (-43.2, 43.9)),
    ('fake_4d', does_not_raise_exception(), (30, 50)),
    ])
def test_ColocatedData_lat_range(coldata,which,raises,value):
    cd = coldata[which]
    with raises:
        val = cd.lat_range
        assert len(val) == 2
        npt.assert_allclose(val, value, rtol=1e-1)

@pytest.mark.parametrize('which,raises,value', [
    ('fake_nodims', pytest.raises(AttributeError), None),
    ('tm5_aeronet', does_not_raise_exception(), (-65.3, 121.5)),
    ('fake_4d', does_not_raise_exception(), (10, 20)),
    ])
def test_ColocatedData_lon_range(coldata,which,raises,value):
    cd = coldata[which]
    with raises:
        val = cd.lon_range
        assert len(val) == 2
        npt.assert_allclose(val, value, rtol=1e-1)

@pytest.mark.parametrize('which,raises', [
    ('fake_nodims', pytest.raises(ValueError)),
    ('tm5_aeronet', does_not_raise_exception())
    ])
def test_ColocatedData_ts_type(coldata,which,raises):
    cd = coldata[which]
    with raises:
        val = cd.ts_type
        assert isinstance(val, str)

@pytest.mark.parametrize('which,raises', [
    ('fake_nodims', pytest.raises(KeyError)),
    ('tm5_aeronet', does_not_raise_exception())
    ])
def test_ColocatedData_units(coldata,which,raises):
    cd = coldata[which]
    with raises:
        val = cd.units
        assert isinstance(val, list)
        assert [isinstance(x, str) for x in val]

@pytest.mark.parametrize('which,raises,result', [
    ('fake_4d', does_not_raise_exception(), 6),
    ('fake_5d', pytest.raises(DataDimensionError), None),
    ('tm5_aeronet', does_not_raise_exception(),8),
    ('fake_nodims', pytest.raises(DataDimensionError), None),
    ('fake_3d', does_not_raise_exception(), 4),


    ])
def test_ColocatedData_num_coords(coldata,which,raises,result):
    cd = coldata[which]
    with raises:
        output = cd.num_coords
        assert output == result

@pytest.mark.parametrize('which,raises,result', [
    ('tm5_aeronet', does_not_raise_exception(),8),
    ('fake_nodims', pytest.raises(DataDimensionError), None),
    ('fake_3d', does_not_raise_exception(), 4),
    ('fake_4d', does_not_raise_exception(), 5)
    ])
def test_ColocatedData_num_coords_with_data(coldata,which,raises,result):
    cd = coldata[which]
    with raises:
        output = cd.num_coords_with_data
        assert output == result

@pytest.mark.parametrize('which,num_coords,raises', [
    ('fake_nodims', 0, pytest.raises(ValueError)),
    ('tm5_aeronet', 8, does_not_raise_exception()),
    ('fake_4d', 5, does_not_raise_exception())
    ])
def test_ColocatedData_get_coords_valid_obs(coldata,which,num_coords,raises):
    cd = coldata[which]
    with raises:
        val = cd.get_coords_valid_obs()
        assert isinstance(val, list)
        assert len(val) == 2
        assert len(val[0]) == len(val[1]) == num_coords

@pytest.mark.parametrize('which,args,raises,chk', [
    ('tm5_aeronet', {}, does_not_raise_exception(),{'nmb':-0.129,
                                                    'R':0.853}),
    ('fake_nodims', {}, pytest.raises(DataDimensionError),{}),
    ('fake_3d', {}, does_not_raise_exception(),{'num_coords_with_data': 4}), # has random numbers in it so nmb, R check is risky with rtol=1e-2
    ('fake_4d', {}, does_not_raise_exception(),{'nmb':0}),
    ('fake_4d', {'use_area_weights' : True}, does_not_raise_exception(),{'nmb':0}),
    ('fake_5d', {}, pytest.raises(DataDimensionError),{}),
    ])
def test_ColocatedData_calc_statistics(coldata,which,args,raises,chk):
    cd = coldata[which]
    with raises:
        output = cd.calc_statistics(**args)
        assert isinstance(output, dict)
        for key, val in chk.items():
            assert key in output
            res = output[key]
            if isinstance(res, str):
                assert res == val
            else:
                npt.assert_allclose(res, val, rtol=1e-2)

@pytest.mark.parametrize('which,args,raises,chk', [
    ('tm5_aeronet', {}, does_not_raise_exception(),{'nmb':-0.065,
                                                    'R':0.679}),
    ('fake_nodims', {}, pytest.raises(DataDimensionError),{}),
    ('fake_3d', {}, does_not_raise_exception(),{}),
    ('fake_4d', {}, does_not_raise_exception(),{'nmb':0}),
    ('fake_5d', {}, pytest.raises(DataDimensionError),{}),
    ('tm5_aeronet', {'aggr' : 'median'},
     does_not_raise_exception(),{'nmb':-0.0136, 'R':0.851}),
    ('tm5_aeronet', {'aggr' : 'max'},
     pytest.raises(ValueError),None),
    ])
def test_ColocatedData_calc_temporal_statistics(coldata,which,args,raises,chk):
    cd = coldata[which]
    with raises:
        output = cd.calc_temporal_statistics(**args)
        assert isinstance(output, dict)
        for key, val in chk.items():
            assert key in output
            res = output[key]
            if isinstance(res, str):
                assert res == val
            else:
                npt.assert_allclose(res, val, rtol=1e-2)

@pytest.mark.parametrize('which,args,raises,chk', [
    ('tm5_aeronet', {}, does_not_raise_exception(),{'nmb':-0.304,
                                                    'R':0.893}),
    ('fake_nodims', {}, pytest.raises(DataDimensionError),{}),
    ('fake_3d', {}, does_not_raise_exception(),{}),
    ('fake_4d', {}, does_not_raise_exception(),{'nmb':0}),
    ('fake_4d', {'use_area_weights' : True}, does_not_raise_exception(),{'nmb':0}),
    ('fake_5d', {}, pytest.raises(DataDimensionError),{}),
    ('tm5_aeronet', {'aggr' : 'median'},
     does_not_raise_exception(),{'nmb':-0.42, 'R':0.81}),
    ('tm5_aeronet', {'aggr' : 'max'},
     pytest.raises(ValueError),None),
    ])
def test_ColocatedData_calc_spatial_statistics(coldata,which,args,raises,chk):
    cd = coldata[which]
    with raises:
        output = cd.calc_spatial_statistics(**args)
        assert isinstance(output, dict)
        for key, val in chk.items():
            assert key in output
            res = output[key]
            if isinstance(res, str):
                assert res == val
            else:
                npt.assert_allclose(res, val, rtol=1e-2)

@pytest.mark.parametrize('which,args,raises', [
    ('tm5_aeronet', {}, does_not_raise_exception()),
    ('fake_nodims', {}, pytest.raises(DataDimensionError)),
    ('fake_3d', {}, does_not_raise_exception()),
    ('fake_4d', {}, does_not_raise_exception()),
    ('fake_5d', {}, pytest.raises(DataDimensionError)),
    ])
def test_ColocatedData_plot_scatter(coldata,which,args,raises):
    cd = coldata[which]
    with raises:
        output = cd.plot_scatter(**args)
        assert isinstance(output, Axes)

def test_meta_access_filename():
    name = 'absc550aer_REF-EBAS-Lev3_MOD-CAM5-ATRAS_20100101_20101231_daily_WORLD-noMOUNTAINS.nc'

    meta = {'var_name': 'absc550aer',
            'ts_type': 'daily',
            'filter_name': 'WORLD-noMOUNTAINS',
            'start': pd.Timestamp('2010-01-01 00:00:00'),
            'stop': pd.Timestamp('2010-12-31 00:00:00'),
            'data_source': ['EBAS-Lev3', 'CAM5-ATRAS']}
    for k, v in ColocatedData.get_meta_from_filename(name).items():
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

@pytest.mark.parametrize('which,input_args,raises,latrange,lonrange,numst', [
('fake_4d',{'region_id': 'EUROPE'}, does_not_raise_exception(),
 (40,72),(-10, 40),4),
('fake_4d',{'region_id': 'France', 'check_country_meta':True},
 pytest.raises(DataDimensionError),None, None, None),
('tm5_aeronet',{'region_id': 'NHEMISPHERE'}, does_not_raise_exception(),
 (0,90), (-180, 180),5),
('tm5_aeronet',{'region_id': 'EUROPE'}, does_not_raise_exception(),
 (40,72), (-10, 40),2),
('tm5_aeronet',{'region_id': 'OCN'}, does_not_raise_exception(),
 (-59.95,66.25), (-132.55,119.95),1),
('tm5_aeronet',{'region_id': 'Brazil','check_country_meta' : True},
 does_not_raise_exception(),(-59.95,66.25), (-132.55,119.95),1),
])
def test_ColocatedData_filter_region(coldata,which,input_args,raises,latrange,lonrange,numst):
    cd = coldata[which]
    with raises:
        if 'check_country_meta' in input_args:
            cd= cd.copy()
            cd.check_set_countries()

        filtered = cd.filter_region(**input_args)
        lats, lons = filtered.data.latitude.data, filtered.data.longitude.data
        assert lats.min() >= latrange[0]
        assert lats.max() <= latrange[1]
        assert lons.min() >= lonrange[0]
        assert lons.max() <= lonrange[1]
        assert filtered.num_coords == numst

@pytest.mark.parametrize('which,raises,filename', [
    ('tm5_aeronet',does_not_raise_exception(),
     'od550aer_REF-AeronetSunV3L2Subset.daily_MOD-TM5_AP3-CTRL2016_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc'),
    ('fake_3d_hr',does_not_raise_exception(),
     'vmro3_REF-fakeobs_MOD-fakemod_20180110_20180117_hourly_WORLD-wMOUNTAINS.nc'),
    ('fake_3d',does_not_raise_exception(),
     'concpm10_REF-fakeobs_MOD-fakemod_20000115_20191215_monthly_WORLD-wMOUNTAINS.nc')

    ])
def test_ColocatedData_to_netcdf(coldata, tempdir, which, raises, filename):
    cd = coldata[which]
    fp = cd.to_netcdf(tempdir)
    assert os.path.exists(fp)
    assert os.path.basename(fp) == filename

@pytest.mark.parametrize('filename,raises', [
    ('od550aer_REF-AeronetSunV3L2Subset.daily_MOD-TM5_AP3-CTRL2016_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc',
     does_not_raise_exception()),
    ('vmro3_REF-fakeobs_MOD-fakemod_20180110_20180117_hourly_WORLD-wMOUNTAINS.nc',
     does_not_raise_exception()),
    ('concpm10_REF-fakeobs_MOD-fakemod_20000115_20191215_monthly_WORLD-wMOUNTAINS.nc',
     does_not_raise_exception())
    ])
def test_ColocatedData_read_netcdf(tempdir,filename,raises):
    fp = os.path.join(tempdir, filename)
    assert os.path.exists(fp)
    with raises:
        cd = ColocatedData().read_netcdf(fp)
        assert isinstance(cd, ColocatedData)

if __name__=="__main__":
    import sys
    pytest.main(sys.argv)
