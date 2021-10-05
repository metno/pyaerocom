#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import iris.cube
import os
from datetime import datetime
import numpy as np
import numpy.testing as npt
import pytest
import xarray as xr

from pyaerocom import GriddedData, Variable
from pyaerocom.exceptions import (CoordinateError, DataDimensionError,
                                  DataSearchError, VariableDefinitionError,
                                  VariableNotFoundError)

from pyaerocom.io import ReadGridded

from .conftest import TEST_RTOL, data_unavail, does_not_raise_exception

TESTLATS =  [-10, 20]
TESTLONS =  [-120, 69]

### ----------------------------------------------
# More recent tests (more systematic)
### ----------------------------------------------
@pytest.mark.parametrize('val, raises', [
    (None,pytest.raises(ValueError)),
    ('Blaaa',does_not_raise_exception()),
    ])
def test_GriddedData_var_name(val, raises):
    data = GriddedData()
    assert data.var_name is None
    with raises:
        data.var_name = val
        assert data.var_name == data.grid.var_name == val

@pytest.mark.parametrize('var_name, var_name_aerocom, raises', [
    ('BlBlub', None, does_not_raise_exception()),
    ('od550aer', 'od550aer', does_not_raise_exception()),
    ('scatc550aer', 'sc550aer', does_not_raise_exception()),
    ])
def test_GriddedData_var_name_aerocom(var_name, var_name_aerocom, raises):
    data = GriddedData()
    data.var_name = var_name
    with raises:
        assert data.var_name_aerocom == var_name_aerocom

@pytest.mark.parametrize('var_name, raises', [
    ('manamana',pytest.raises(VariableDefinitionError)),
    ('od550aer',does_not_raise_exception()),
    ])
def test_GriddedData_var_info(var_name, raises):
    data = GriddedData()
    data.var_name = var_name
    with raises:
        var_info = data.var_info
        assert isinstance(var_info, Variable)

def test_GriddedData_long_name():
    data = GriddedData()
    assert data.long_name is None
    data.long_name = 'blaaa'
    assert data.long_name == data.grid.long_name == 'blaaa'

def test_GriddedData_suppl_info():
    assert isinstance(GriddedData().suppl_info, dict)

@data_unavail
def test_basic_properties(data_tm5):

    data =  data_tm5
    from iris.cube import Cube
    assert isinstance(data.cube, Cube)
    assert data.ts_type == 'monthly'
    assert str(data.start) == '2010-01-01T00:00:00.000000'
    assert str(data.stop) == '2010-12-31T23:59:59.999999'
    assert len(data.time.points) == 12
    assert data.data_id == 'TM5_AP3-CTRL2016'
    ff = ['aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc']
    files = [os.path.basename(x) for x in data.from_files]
    print(files)
    assert files == ff
    assert data.shape == (12, 90, 120)
    assert data.lat_res == 2.0
    assert data.lon_res == 3.0

@data_unavail
def test_GriddedData_longitude(data_tm5):
    """Test if longitudes are defined right"""
    assert str(data_tm5.longitude.units) == 'degrees'

    lons = data_tm5.longitude.points
    nominal = [-181.5, 175.5]
    vals = [lons.min(), lons.max()]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)

@data_unavail
def test_GriddedData_latitude(data_tm5):
    """test latitude array"""
    assert str(data_tm5.latitude.units) == 'degrees'
    lats = data_tm5.latitude.points
    nominal = [-89, 89]
    vals = [lats.min(), lats.max()]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)

@data_unavail
def test_GriddedData_time(data_tm5):
    """Test time dimension access and values"""
    time = data_tm5.time

    nominal_eq = ['julian', 'day since 1850-01-01 00:00:00.0000000 UTC', False]
    vals_eq = [time.units.calendar,
               time.units.name,
               isinstance(time.cell(0).point, datetime)]
    assert nominal_eq == vals_eq

@data_unavail
def test_GriddedData_resample_time(data_tm5):
    data = data_tm5

    yearly = data.resample_time('yearly')

    npt.assert_array_equal(yearly.shape, (1, 90, 120))

    # make sure means are preserved (more or less)
    mean_vals = [data.mean(), yearly.mean()]
    npt.assert_allclose(actual=mean_vals,
                        desired=[0.11865, 0.11865], rtol=TEST_RTOL)
@data_unavail
def test_GriddedData_interpolate(data_tm5):
    data = data_tm5

    itp = data.interpolate(latitude=TESTLATS, longitude=TESTLONS)

    assert type(itp) == GriddedData
    assert itp.shape == (12, 2, 2)

    desired = [0.13877, 0.13748]
    actual=[itp.mean(False), itp.mean(True)]
    npt.assert_allclose(actual=actual,
                        desired=desired,
                        rtol=TEST_RTOL)

@data_unavail
def test_GriddedData_to_time_series(data_tm5):

    latsm = [-9, 21]
    lonsm = [-118.5, 70.5]
    stats = data_tm5.to_time_series(latitude=TESTLATS, longitude=TESTLONS)

    lats_actual = []
    lons_actual = []
    means_actual = []

    for stat in stats:
        lats_actual.append(stat.latitude)
        lons_actual.append(stat.longitude)
        means_actual.append(stat.od550aer.mean())
    npt.assert_array_equal(lats_actual, latsm)
    npt.assert_array_equal(lons_actual, lonsm)
    npt.assert_allclose(means_actual, [0.101353, 0.270886], rtol=TEST_RTOL)

@data_unavail
def test_GriddedData_change_baseyear(data_tm5):
    cp = data_tm5.copy()
    cp.change_base_year(1901)

    assert str(cp.time.units) == 'days since 1901-01-01 00:00:00'

def test_GriddedData_min(data_tm5):
    npt.assert_allclose(data_tm5.min(), 0.004629, atol=0.0001)

def test_GriddedData_nanmin(data_tm5):
    npt.assert_allclose(data_tm5.nanmin(), 0.004629, atol=0.0001)

def test_GriddedData_max(data_tm5):
    npt.assert_allclose(data_tm5.max(), 2.495539, atol=0.0001)

def test_GriddedData_nanmax(data_tm5):
    npt.assert_allclose(data_tm5.nanmax(), 2.495539, atol=0.0001)

@pytest.mark.parametrize('extend_percent,expected', [
    (0, (0.004, 2.496)),
    (15, (-0.4, 2.9)),

])
def test_GriddedData_estimate_value_range_from_data(data_tm5,extend_percent,
                                                    expected):
    result = data_tm5.estimate_value_range_from_data(extend_percent)
    npt.assert_allclose(result,expected,rtol=1e-2)

def test_GriddedData_area_weighted_mean(data_tm5):
    val = data_tm5.area_weighted_mean()
    assert len(val) == 12
    npt.assert_allclose(val.mean(), 0.118648, atol=0.001)

@data_unavail
@pytest.mark.parametrize('kwargs,result', [
    (dict(), 0.11864813532841474),
    (dict(areaweighted=False), 0.09825691),
    ])
def test_GriddedData_mean(data_tm5,kwargs,result):
    npt.assert_allclose(data_tm5.mean(**kwargs), result)

def test_GriddedData_std(data_tm5):
    npt.assert_allclose(data_tm5.std(), 0.106527, atol=0.0001)

def test_GriddedData_short_str(data_tm5):
    assert data_tm5.short_str() == 'od550aer (TM5_AP3-CTRL2016, ' \
                                   'freq=monthly, unit=1)'

def test_GriddedData_copy(data_tm5):
    data = data_tm5.copy()
    assert isinstance(data, GriddedData)
    assert data.cube is not data_tm5.cube

def test_GriddedData__check_lonlat_bounds(data_tm5):
    data = data_tm5.copy()
    data.latitude.bounds = None
    data.longitude.bounds = None
    data._check_lonlat_bounds()
    lonb = data.longitude.bounds
    latb = data.latitude.bounds
    assert latb is not None
    assert lonb is not None
    assert isinstance(latb, np.ndarray)
    assert isinstance(lonb, np.ndarray)
    assert lonb.shape == (120, 2)
    assert latb.shape == (90, 2)

@pytest.mark.parametrize('val,expected,raises', [
    ('blaa', None, pytest.raises(CoordinateError)),
    ('lon', {'var_name': 'lon'}, does_not_raise_exception()),
    ('longitude', {'standard_name': 'longitude'}, does_not_raise_exception()),
    ('Center coordinates for longitudes', {'long_name': 'Center coordinates for longitudes'},
     does_not_raise_exception()),
    ('lat', {'var_name': 'lat'}, does_not_raise_exception()),
    ('latitude', {'standard_name': 'latitude'}, does_not_raise_exception()),
    ('Center coordinates for latitudes', {'long_name': 'Center coordinates for latitudes'},
     does_not_raise_exception()),
    ('time', {'standard_name': 'time'}, does_not_raise_exception()),
    ('Time', {'long_name': 'Time'}, does_not_raise_exception()),
])
def test_GriddedData__check_coordinate_access(data_tm5,val,expected,raises):
    with raises:
        output = data_tm5._check_coordinate_access(val)
        assert output==expected

@pytest.mark.parametrize('add_aux', [True, False])
def test_GriddedData_delete_aux_vars(data_tm5, add_aux):

    data = data_tm5.copy()
    if add_aux:
        import iris
        auxc = iris.coords.AuxCoord(data.time.points, var_name='time2')
        data.cube.add_aux_coord(auxc, [0])
        assert len(data.cube.aux_coords) == 1
    data.delete_aux_vars()
    assert len(data.cube.aux_coords) == 0

@pytest.mark.parametrize('val,raises', [
    (42, pytest.raises(ValueError)),
    (ReadGridded('TM5-met2010_CTRL-TEST'), does_not_raise_exception())
])
def test_GriddedData_reader_setter(data_tm5,val,raises):
    data = data_tm5.copy()
    with raises:
        data.reader = val
        assert data._reader is val
        assert data.reader is val

@pytest.mark.parametrize('set_data_id,raises', [
    ('blaaaa', pytest.raises(DataSearchError)),
    ('TM5-met2010_CTRL-TEST', does_not_raise_exception())
])
def test_GriddedData_reader_getter(data_tm5,set_data_id,raises):
    data = data_tm5.copy()
    data.metadata['data_id'] = set_data_id
    assert data._reader is None
    with raises:
        reader = data.reader
        assert isinstance(reader, ReadGridded)

@pytest.mark.parametrize('var,raises', [
    ('abs550aer',does_not_raise_exception()),
    ('concso4',pytest.raises(VariableNotFoundError))
])
def test_GriddedData_search_other(var,raises):
    from pyaerocom.io import ReadGridded
    reader = ReadGridded('TM5-met2010_CTRL-TEST')
    data = reader.read_var('od550aer', start=2010, ts_type='monthly')
    with raises:
        result = data.search_other(var)
        assert isinstance(result, GriddedData)

def test_GriddedData_update_meta(data_tm5):
    data = data_tm5.copy()
    data.update_meta(bla=42, blub=43)
    assert data.metadata['bla'] == 42
    assert data.metadata['blub'] == 43

@pytest.mark.parametrize('inplace', [True, False])
def test_GriddedData_delete_all_coords(data_tm5, inplace):
    data = data_tm5.copy()
    new = data.delete_all_coords(inplace)
    assert new.cube.coords() == []
    if inplace:
        assert data is new
    else:
        assert len(data.cube.coords()) == 3

@pytest.mark.parametrize('inplace,other_tst,raises', [
    (True, 'monthly', does_not_raise_exception()),
    (False, 'monthly', does_not_raise_exception()),
    (False, 'daily', pytest.raises(DataDimensionError)),

    ])
def test_GriddedData_copy_coords(inplace,other_tst,raises):
    from pyaerocom.io import ReadGridded
    reader = ReadGridded('TM5-met2010_CTRL-TEST')
    aod = reader.read_var('od550aer', start=2010, ts_type='monthly')
    abs = reader.read_var('abs550aer', start=2010, ts_type=other_tst)
    with raises:
        result = aod.copy_coords(abs,inplace)
        if inplace:
            assert result.cube is aod.cube
        else:
            assert result.cube is not aod.cube
        for coord in abs.cube.coords():
            _coord = result.cube.coord(coord.name())
            assert coord == _coord

def test_GriddedData_register_var_glob(tmpdir):
    from pyaerocom import const
    arr = np.ones((10,10,10))
    arr[2:5] = 4
    var_name = 'blablub'
    cube = iris.cube.Cube(arr,var_name=var_name)
    data = GriddedData(input=cube)
    data.register_var_glob()
    vars = const.VARS
    assert vars._all_vars[-1] == var_name
    vars._all_vars.pop(-1)
    del vars._vars_added[var_name]


def _make_fake_dataset(var_name, units):
    arr = xr.DataArray(np.ones(10))
    arr.attrs['var_name'] = var_name
    arr.attrs['units'] = units
    ds = arr.to_dataset(name=var_name)
    return ds

@pytest.mark.parametrize('var_name,units,data_unit', [
    ('od550aer', '1', '1'),
    ('od550aer', 'invalid', '1'),
    ('concso4', 'ug S m-3', 'ug S m-3'),
    ('concco', 'ugC/m3', 'ug C m-3'),

])
def test_GriddedData__check_invalid_unit_alias(tmpdir,var_name,units,
                                               data_unit):

    ds = _make_fake_dataset(var_name,units)
    path = os.path.join(tmpdir, 'output.nc')
    ds.to_netcdf(path)
    assert os.path.exists(path)
    data = GriddedData(path, var_name=var_name, check_unit=False)
    data._check_invalid_unit_alias()
    assert data.units == data_unit

