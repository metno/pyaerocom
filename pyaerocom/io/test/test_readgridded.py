#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 14:14:29 2018
"""

import pytest
import os
from collections import OrderedDict
import numpy.testing as npt
import numpy as np
from pandas import DataFrame
from pyaerocom.conftest import (TEST_RTOL, lustre_unavail, testdata_unavail,
                                CHECK_PATHS, TESTDATADIR)
from pyaerocom.io.readgridded import ReadGridded
from pyaerocom import GriddedData
from pyaerocom.exceptions import VarNotAvailableError

def init_reader():
    return ReadGridded(data_id="ECMWF_CAMS_REAN")

@pytest.fixture(scope='session')
def reader_reanalysis():
    return init_reader()

@pytest.fixture(scope='module')
def reader_tm5():
    return ReadGridded('TM5-met2010_CTRL-TEST')

path_tm5 = str(TESTDATADIR.joinpath(CHECK_PATHS['tm5']))

@pytest.mark.parametrize('input_args,mean_val', [

    (dict(var_name='od550aer', ts_type='monthly'), 0.0983),
    (dict(var_name='od550aer', ts_type='monthly', constraints={
                                  'var_name'   : 'od550aer',
                                  'operator'   : '<',
                                  'filter_val' : 0.1
                                  }), 0.2054),
    (dict(var_name='od550aer', ts_type='monthly', constraints={
                                  'var_name'   : 'od550aer',
                                  'operator'   : '>',
                                  'filter_val' : 1000
                                  }), 0.0983),

    (dict(var_name='od550aer', ts_type='monthly', constraints=[
        {'var_name'   : 'od550aer',
         'operator'   : '<',
         'filter_val' : 0.1},
        {'var_name'   : 'od550aer',
         'operator'   : '>',
         'filter_val' : 0.11}
        ]), 0.1047)
    ])
def test_read_var(reader_tm5, input_args, mean_val):
    data = reader_tm5.read_var(**input_args)
    # ToDo: .mean() is broken since constrained filtering works lazy now and
    # I did not figure out how to mask grid points in an dask array, thus, data
    # that is invalid is set to NaN in which case GriddedData.mean() fails...
    # Needs to be checked.
    #mean = data.mean()
    mean = np.nanmean(data.cube.data)
    npt.assert_allclose(mean, mean_val, rtol=1e-3)

def test_ReadGridded_class_empty():
    r = ReadGridded()
    assert r.data_id == None
    assert r.data_dir == None
    from pyaerocom.io.aerocom_browser import AerocomBrowser
    assert isinstance(r.browser, AerocomBrowser)
    with pytest.raises(AttributeError):
        r.years_avail
    assert r.vars_filename == []


@testdata_unavail
def test_ReadGridded_data_dir(reader_tm5):
    assert reader_tm5.data_dir == path_tm5
    assert reader_tm5._vars_2d == ['abs550aer', 'od550aer']
    assert reader_tm5._vars_3d == []


def test_ReadGridded_ts_types():
    r = ReadGridded(data_dir=path_tm5)
    assert sorted(r.ts_types) == ['daily', 'monthly']

@testdata_unavail
def test_ReadGridded_read_var(reader_tm5):
    r = reader_tm5
    data = r.read_var('od550aer')
    npt.assert_almost_equal(data.mean(), 0.0960723)
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
    for var in expected:
        assert r.has_var(var)  # calling has_var
    assert sorted(r.vars_provided) == sorted(expected)
    # assert r.has_var('conco3')

@pytest.mark.parametrize('options,expected', [
    (dict(prefer_longer=True, flex_ts_type=True, ts_type='monthly'), 'daily'),
    (dict(prefer_longer=False, flex_ts_type=True, ts_type='monthly'), 'monthly'),
    (dict(prefer_longer=True, flex_ts_type=False, ts_type='monthly'), 'monthly'),
    (dict(prefer_longer=False, flex_ts_type=False, ts_type='monthly'), 'monthly'),
    (dict(prefer_longer=True, flex_ts_type=True), 'daily'),
    (dict(prefer_longer=False, flex_ts_type=True), 'daily')
])
def test_ReadGridded_prefer_longer(options, expected):
    r = ReadGridded(data_dir=path_tm5)
    gridded = r.read_var('abs550aer', **options)
    assert gridded.ts_type == expected


def test_filter_query(reader_tm5):
    reader_tm5.filter_query('abs550aer', ts_type='yearly', flex_ts_type=True)

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


def test_ReadGridded_get_var_info_from_files(reader_tm5):
    od = reader_tm5.get_var_info_from_files()
    assert isinstance(od, OrderedDict)
    assert sorted(od.keys()) == sorted(['abs550aer', 'od550aer'])


# Lustre tests
START = "1-1-2003"
STOP = "31-12-2007"

@lustre_unavail
def test_file_info(reader_reanalysis):
    assert isinstance(reader_reanalysis.file_info, DataFrame)
    assert len(
        reader_reanalysis.file_info.columns) == 12, 'Mismatch colnum file_info (df)'


@lustre_unavail
def test_years_available(reader_reanalysis):
    years = list(range(2003, 2021)) + [9999]
    npt.assert_array_equal(reader_reanalysis.years_avail, years)


@lustre_unavail
def test_data_dir(reader_reanalysis):
    assert reader_reanalysis.data_dir.endswith(
        'aerocom/aerocom-users-database/ECMWF/ECMWF_CAMS_REAN/renamed')


@lustre_unavail
def test_read_var_lustre(reader_reanalysis):
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
