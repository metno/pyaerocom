#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 14:53:00 2021

@author: jonasg
"""

import pytest
from iris import load
from iris.cube import Cube
from iris.exceptions import TranslationError
import numpy as np
from pyaerocom.io import FileConventionRead
from pyaerocom.conftest import TESTDATADIR, does_not_raise_exception
from pyaerocom.exceptions import (TemporalResolutionError,
                                  UnresolvableTimeDefinitionError,
                                  NetcdfError,
                                  FileConventionError)
from pyaerocom.io import iris_io as iio

tm5fname1 = 'aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc'
TM5_DIR = TESTDATADIR.joinpath('modeldata/TM5-met2010_CTRL-TEST/renamed')
TM5_FILE1 = TM5_DIR.joinpath(tm5fname1)
TM5_FILE2 = TM5_DIR.joinpath('aerocom3_TM5-met2010_AP3-CTRL2019_od550aer_Column_2010_daily.nc')

EMEP_FILE = TESTDATADIR.joinpath('modeldata/EMEP_2017/Base_month.nc')

aod_cube = load(str(TM5_FILE1))[0]

aod_cube_notime = aod_cube.copy()
aod_cube_notime.remove_coord('time')

aod_cube_wrongtime = aod_cube.copy()
tc = aod_cube_wrongtime.coord('time')
pts = list(tc._values_dm._real_array)
pts.append(70000)
tc._values_dm._real_array = np.asarray(pts)

aod_cube_wrongtime2 = aod_cube.copy()
tc = aod_cube_wrongtime2.coord('time')
pts = list(tc._values_dm._real_array)
pts[-1] = 70000
tc._values_dm._real_array = np.asarray(pts)

aod_cube_wrongtime3 = aod_cube.copy()
tc = aod_cube_wrongtime3.coord('time')
aod_cube_wrongtime3.remove_coord('time')


aod_cube_only_longname_dims = aod_cube.copy()
aod_cube_only_longname_dims.coord('longitude').standard_name = None
aod_cube_only_longname_dims.coord('longitude').var_name = None
aod_cube_only_longname_dims.coord('longitude').long_name = 'lon'

aod_cube_only_longname_dims.coord('latitude').standard_name = None
aod_cube_only_longname_dims.coord('latitude').var_name = None
aod_cube_only_longname_dims.coord('latitude').long_name = 'lat'

aod_cube_only_longname_dims.coord('time').standard_name = None
aod_cube_only_longname_dims.coord('time').var_name = None
aod_cube_only_longname_dims.coord('time').long_name = 'time'

aod_cube_nounit = aod_cube.copy()
aod_cube_nounit.units = ''

import tempfile
from pathlib import Path
tmpdirnc = Path(tempfile.gettempdir()).joinpath('test_iris_io')
if not tmpdirnc.exists():
    tmpdirnc.mkdir()

FAKE_FILE = str(tmpdirnc.joinpath('invalid.nc'))
open(FAKE_FILE, 'w').close()


@pytest.mark.parametrize('cube,ts_type,year,raises', [
    (aod_cube, 'monthly', 2010, does_not_raise_exception()),
    (aod_cube_notime, 'monthly', 2010, pytest.raises(AttributeError)),
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

@pytest.mark.parametrize('cube,file,file_convention,raises,dimnames', [
    (aod_cube_notime,'aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc',
     None, does_not_raise_exception(), ['time', 'latitude', 'longitude']),
    (aod_cube_wrongtime2, 'aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc',
     None, does_not_raise_exception(), ['time', 'latitude', 'longitude']),
    (aod_cube,'aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc',None,
     does_not_raise_exception(),['time', 'latitude', 'longitude']),
    (aod_cube,'aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc',
     FileConventionRead('aerocom2'),does_not_raise_exception(),
     ['time', 'latitude', 'longitude']),
    (aod_cube_nounit,'aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc',
     None,does_not_raise_exception(),['time', 'latitude', 'longitude']),
    (aod_cube_notime,'aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc',
     FileConventionRead('aerocom2'),does_not_raise_exception(),
     ['time', 'latitude', 'longitude']),
    (aod_cube_wrongtime, 'aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc',
     None, pytest.raises(UnresolvableTimeDefinitionError), None),
    ])
def test__cube_quality_check(cube,file,file_convention,raises,dimnames):
    with raises:
        cube = iio._cube_quality_check(cube, file, file_convention)
        _dimnames = [c.name() for c in cube.dim_coords]
        assert _dimnames == dimnames

@pytest.mark.parametrize('file,var_name,file_convention,perform_fmt_checks,raises', [
    (FAKE_FILE, None, None, None, pytest.raises(TranslationError)),
    (TM5_FILE1, None, None, None, does_not_raise_exception()),
    (EMEP_FILE, None, None, None, pytest.raises(NetcdfError)),
    (EMEP_FILE, 'SURF_ug_NO2', None, None, does_not_raise_exception()),
    (EMEP_FILE, 'od550aer', None, None, pytest.raises(NetcdfError)),
    ])
def test_load_cube_custom(file,var_name,file_convention,perform_fmt_checks,
                           raises):
    with raises:
        result = iio.load_cube_custom(file,var_name,file_convention,
                                       perform_fmt_checks)
        assert isinstance(result, Cube)

@pytest.mark.parametrize('files,var_name,file_convention,perform_fmt_checks,raises,num_loaded', [
    ([TM5_FILE1], None, None, None, does_not_raise_exception(), 1),

    ([EMEP_FILE], None, None, None, does_not_raise_exception(), 0)
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

@pytest.mark.parametrize('cube,raises', [
    (aod_cube_only_longname_dims, does_not_raise_exception())
    ])
def test_check_dim_coord_names_cube(cube, raises):
    with raises:
        iio.check_dim_coord_names_cube(cube)

@pytest.mark.parametrize('cube,file,raises', [
    (aod_cube_wrongtime3, 'aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_daily.nc',
     does_not_raise_exception()),
    (aod_cube, 'aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc',
     does_not_raise_exception()),
    (aod_cube, 'aerocom3_TM5_AP3-CTRL2016_od550aer_Column_-1_monthly.nc',
     pytest.raises(FileConventionError)),
    (aod_cube, 'aerocom3_TM5_AP3-CTRL2016_od550aer_Column_20001_monthly.nc',
     pytest.raises(FileConventionError))

    ])
def test__check_correct_time_dim(cube, file, raises):
    with raises:
        cube = iio._check_correct_time_dim(cube, file)
        assert isinstance(cube, Cube)



if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)