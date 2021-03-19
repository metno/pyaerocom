#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""

import pytest
import os
import numpy.testing as npt
from datetime import datetime
from pyaerocom.conftest import TEST_RTOL, testdata_unavail, does_not_raise_exception
from pyaerocom.exceptions import VariableDefinitionError
from pyaerocom import GriddedData, Variable

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
    ('od550aer',does_not_raise_exception()),
    ('manamana',pytest.raises(VariableDefinitionError)),
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

### ----------------------------------------------
# Initial set of tests (not very systematic)
### ----------------------------------------------

@testdata_unavail
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

@testdata_unavail
def test_longitude(data_tm5):
    """Test if longitudes are defined right"""
    assert str(data_tm5.longitude.units) == 'degrees'

    lons = data_tm5.longitude.points
    nominal = [-181.5, 175.5]
    vals = [lons.min(), lons.max()]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)

@testdata_unavail
def test_latitude(data_tm5):
    """test latitude array"""
    assert str(data_tm5.latitude.units) == 'degrees'
    lats = data_tm5.latitude.points
    nominal = [-89, 89]
    vals = [lats.min(), lats.max()]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)

@testdata_unavail
def test_time(data_tm5):
    """Test time dimension access and values"""
    time = data_tm5.time

    nominal_eq = ['julian', 'day since 1850-01-01 00:00:00.0000000 UTC', False]
    vals_eq = [time.units.calendar,
               time.units.name,
               isinstance(time.cell(0).point, datetime)]
    assert nominal_eq == vals_eq

@testdata_unavail
def test_resample_time(data_tm5):
    data = data_tm5

    yearly = data.resample_time('yearly')

    npt.assert_array_equal(yearly.shape, (1, 90, 120))

    # make sure means are preserved (more or less)
    mean_vals = [data.mean(), yearly.mean()]
    npt.assert_allclose(actual=mean_vals,
                        desired=[0.11865, 0.11865], rtol=TEST_RTOL)
@testdata_unavail
def test_interpolate(data_tm5):
    data = data_tm5

    itp = data.interpolate(latitude=TESTLATS, longitude=TESTLONS)

    assert type(itp) == GriddedData
    assert itp.shape == (12, 2, 2)

    desired = [0.13877, 0.13748]
    actual=[itp.mean(False), itp.mean(True)]
    npt.assert_allclose(actual=actual,
                        desired=desired,
                        rtol=TEST_RTOL)

@testdata_unavail
def test_to_time_series(data_tm5):

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

@testdata_unavail
def test_change_baseyear(data_tm5):
    cp = data_tm5.copy()
    cp.change_base_year(901)

    assert str(cp.time.units) == 'days since 901-01-01 00:00:00'

@testdata_unavail
@pytest.mark.parametrize('kwargs,result', [
    (dict(), 0.11864813532841474),
    (dict(areaweighted=False), 0.09825691),
    ])
def test_mean(data_tm5,kwargs,result):
    npt.assert_allclose(data_tm5.mean(**kwargs), result)

if __name__=="__main__":
    import sys
    pytest.main(sys.argv)
