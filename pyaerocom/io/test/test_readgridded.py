#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""

# TODO: Docstrings
import pytest
import os
from collections import OrderedDict
import numpy.testing as npt
from pandas import Timestamp, DataFrame
from pyaerocom.conftest import TEST_RTOL, does_not_raise_exception, lustre_unavail, testdata_unavail, TEST_PATHS, TESTDATADIR
from pyaerocom.io.readgridded import ReadGridded
from pyaerocom import GriddedData
from pyaerocom.exceptions import VarNotAvailableError, VariableDefinitionError


def test_ReadGridded_class_empty():
    r = ReadGridded()
    assert r.data_id == None
    assert r.data_dir == None
    from pyaerocom.io.aerocom_browser import AerocomBrowser
    assert isinstance(r.browser, AerocomBrowser)

    failed = False
    try:
        r.years_avail
    except AttributeError:
        failed = True
    assert failed
    assert r.vars_filename == []


path_tm5 = str(TESTDATADIR.joinpath(TEST_PATHS['tm5']))

# @pytest.fixture(scope='function')
# def tm5_reader():
#     return ReadGridded(data_dir=path_tm5)


@testdata_unavail
def test_ReadGridded_data_dir():
    r = ReadGridded(data_dir=path_tm5)
    assert r.data_dir == path_tm5
    assert r._vars_2d == ['abs550aer', 'od550aer']
    assert r._vars_3d == []


def test_ReadGridded_ts_types():
    r = ReadGridded(data_dir=path_tm5)
    assert sorted(r.ts_types) == ['daily', 'monthly']

@testdata_unavail
def test_ReadGridded_read_var():
    r = ReadGridded(data_dir=path_tm5)
    data = r.read_var('od550aer')
    assert isinstance(data, GriddedData)
    ds = data.to_xarray().load()
    mean = float(ds.mean(dim='time').mean(dim='lat').mean(dim='lon'))
    npt.assert_almost_equal(mean, 0.09631748)
    with pytest.raises(VarNotAvailableError):
        r.read_var('wetso4')
    from pyaerocom.io.aux_read_cubes import add_cubes
    gridded = r.read_var('new_var', aux_vars=[
        'abs550aer', 'od550aer'], aux_fun=add_cubes)
    assert gridded.var_name == 'new_var'
    assert isinstance(gridded, GriddedData)


@pytest.mark.parametrize('experiments', [
    (['exp1']),
    (['exp1', 'exp2']),
])
def test_ReadGridded_experiments(tmpdir, experiments):
    for exp in experiments:
        filename = 'aerocom3_TM5-met2010_{}-CTRL2019_abs550aer_Column_2010_daily.nc'.format(exp)
        open(os.path.join(tmpdir, filename), 'a').close()
    r = ReadGridded(data_dir = str(tmpdir))
    assert r.experiments == experiments

@pytest.mark.parametrize('vars,expected', [
    (['mmro3', 'rho'], ['conco3', 'mmro3', 'rho']),
    (['od440aer', 'od870aer'], ['ang4487aer', 'od440aer', 'od870aer']),

])
def test_ReadGridded_aux(tmpdir, vars, expected):
    for var in vars:
        filename = 'aerocom3_TM5-met2010_AP3-CTRL2019_{}_Column_2010_daily.nc'.format(
            var)
        open(os.path.join(tmpdir, filename), 'a').close()
    r = ReadGridded(data_dir=str(tmpdir))
    # assert r._check_var_match_pattern('conco3')
    for var in expected:
        assert r.has_var(var)  # calling has_var
    assert sorted(r.vars_provided) == sorted(expected)
    # assert r.has_var('conco3')


# def test_ReadGridded__check_ts_types():
#     r = ReadGridded()
#     with pytest.raises(IndexError):  # Should throw ValueError
#         r._check_ts_type('nonexisting_ts_type')
#     with pytest.raises(AttributeError):
#         r._check_ts_type(None)
#     assert r._check_ts_type('monthly') == 'monthly'


# def test_ReadGridded_add_aux_compute():
#     r = ReadGridded()


def test_ReadGridded_prefer_longer():
    r = ReadGridded(data_dir=path_tm5)
    daily = r.read_var('abs550aer', ts_type='monthly', flex_ts_type=True,
                       prefer_longer=True)
    assert daily.ts_type == 'daily'


@pytest.mark.parametrize('years, expected', [
    ([2003, 2005], [2003, 2005]),
])
def test_ReadGridded_years_avail(tmpdir, years, expected):
    for year in years:
        filename = 'aerocom3_TM5-met2010_AP3-CTRL2019_od550aer_Column_{}_daily.nc'.format(
            year)
        open(os.path.join(tmpdir, filename), 'a').close()
    r = ReadGridded(data_dir=str(tmpdir))
    assert sorted(r.years_avail) == sorted(years)


def test_ReadGridded_get_var_info_from_files():
    r = ReadGridded(data_dir=path_tm5)
    with pytest.raises(VariableDefinitionError):  # Should not raise error
        od = r.get_var_info_from_files()
    r.AUX_REQUIRES = {}
    od = r.get_var_info_from_files()
    assert isinstance(od, OrderedDict)


# Lustre tests
START = "1-1-2003"
STOP = "31-12-2007"


def init_reader():
    return ReadGridded(data_id="ECMWF_CAMS_REAN")


@lustre_unavail
@pytest.fixture(scope='session')
def reader_reanalysis():
    return init_reader()


@lustre_unavail
def test_file_info(reader_reanalysis):
    assert isinstance(reader_reanalysis.file_info, DataFrame)
    assert len(
        reader_reanalysis.file_info.columns) == 12, 'Mismatch colnum file_info (df)'


@lustre_unavail
def test_years_available(reader_reanalysis):
    years = list(range(2003, 2020)) + [9999]
    npt.assert_array_equal(reader_reanalysis.years_avail, years)


@lustre_unavail
def test_data_dir(reader_reanalysis):
    assert reader_reanalysis.data_dir.endswith(
        'aerocom/aerocom-users-database/ECMWF/ECMWF_CAMS_REAN/renamed')


@lustre_unavail
def test_read_var(reader_reanalysis):
    from numpy import datetime64
    d = reader_reanalysis.read_var(var_name="od550aer", ts_type="daily",
                                   start=START, stop=STOP)

    from pyaerocom import GriddedData
    assert isinstance(d, GriddedData)
    npt.assert_array_equal([d.var_name, sum(d.shape), d.start, d.stop],
                           ["od550aer", 1826 + 161 + 320,
                            datetime64('2003-01-01T00:00:00.000000'),
                            datetime64('2007-12-31T23:59:59.999999')])
    vals = [d.longitude.points[0],
            d.longitude.points[-1],
            d.latitude.points[0],
            d.latitude.points[-1]]
    nominal = [-180.0, 178.875, 90.0, -90.0]
    npt.assert_allclose(actual=vals, desired=nominal, rtol=TEST_RTOL)
    return d


@lustre_unavail
def test_prefer_longer(reader_reanalysis):
    daily = reader_reanalysis.read_var('od550aer', ts_type='monthly',
                                       flex_ts_type=True,
                                       prefer_longer=True)
    assert daily.ts_type == 'daily'


@lustre_unavail
def test_read_vars(reader_reanalysis):
    data = reader_reanalysis.read(['od440aer', 'od550aer', 'od865aer'],
                                  ts_type="daily", start=START, stop=STOP)
    vals = [len(data),
            sum(data[0].shape),
            sum(data[1].shape),
            sum(data[2].shape)]
    nominal = [3, 2307, 2307, 2307]
    npt.assert_array_equal(vals, nominal)


if __name__ == "__main__":
    import sys
    pytest.main(sys.argv)
