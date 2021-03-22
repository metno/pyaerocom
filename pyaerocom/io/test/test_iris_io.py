#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 14:53:00 2021

@author: jonasg
"""

import pytest
from iris import load
from iris.cube import Cube
from pyaerocom.conftest import TESTDATADIR, does_not_raise_exception
from pyaerocom.exceptions import (TemporalResolutionError,
                                  UnresolvableTimeDefinitionError)
from pyaerocom.io import iris_io as iio

TM5_DIR = TESTDATADIR.joinpath('modeldata/TM5-met2010_CTRL-TEST/renamed')
TM5_FILE1 = TM5_DIR.joinpath('aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc')
TM5_FILE2 = TM5_DIR.joinpath('aerocom3_TM5-met2010_AP3-CTRL2019_od550aer_Column_2010_daily.nc')

EMEP_FILE = TESTDATADIR.joinpath('modeldata/EMEP_2017/Base_month.nc')

aod_cube = load(str(TM5_FILE1))[0]

@pytest.mark.parametrize('cube,ts_type,year,raises', [
    (aod_cube, 'monthly', 2010, does_not_raise_exception()),
    (aod_cube, 'blaa', 2010, pytest.raises(TemporalResolutionError)),
    (aod_cube, 'daily', 2010, pytest.raises(UnresolvableTimeDefinitionError)),
    (aod_cube, 'daily', 2012, pytest.raises(UnresolvableTimeDefinitionError)),
    (aod_cube, 'monthly', 2008, pytest.raises(ValueError)),

    ])
def test_check_time_coord(cube,ts_type,year,raises):
    with raises:
        iio.check_time_coord(cube, ts_type, year)

def test_get_dim_names_cube():
    assert iio.get_dim_names_cube(aod_cube) == ['time', 'latitude', 'longitude']

def test_get_dimnames_cube():
    assert iio.get_coord_names_cube(aod_cube) == ['time', 'latitude', 'longitude']

@pytest.mark.parametrize('files,var_name,file_convention,perform_fmt_checks,raises,num_loaded', [
    ([TM5_FILE1], None, None, None, does_not_raise_exception(), 1)
    ])
def test_load_cubes_custom(files,var_name,file_convention,perform_fmt_checks,
                           raises,num_loaded):
    with raises:
        result = iio.load_cubes_custom(files,var_name,file_convention,
                                       perform_fmt_checks)
        assert isinstance(result, tuple) and len(result) == 2
        assert isinstance(result[0], list)
        assert isinstance(result[1], list)
        assert len(result[0]) == len(result[1]) == num_loaded


if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)