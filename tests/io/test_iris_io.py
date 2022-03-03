from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Type

import numpy as np
import pytest
from iris import load
from iris.cube import Cube, CubeList
from iris.exceptions import TranslationError

from pyaerocom.exceptions import (
    FileConventionError,
    NetcdfError,
    TemporalResolutionError,
    UnresolvableTimeDefinitionError,
)
from pyaerocom.io import FileConventionRead, iris_io

from .._conftest_helpers import make_dummy_cube_3D_daily
from ..conftest import TESTDATADIR

TM5_DIR = TESTDATADIR / "modeldata/TM5-met2010_CTRL-TEST/renamed"
TM5_FILE1 = TM5_DIR / "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc"
TM5_FILE2 = TM5_DIR / "aerocom3_TM5-met2010_AP3-CTRL2019_od550aer_Column_2010_daily.nc"

EMEP_FILE = TESTDATADIR / "modeldata/EMEP_2017/Base_month.nc"

aod_cube = load(str(TM5_FILE1))[0]

aod_cube_notime = aod_cube.copy()
aod_cube_notime.remove_coord("time")

aod_cube_wrongtime = aod_cube.copy()
tc = aod_cube_wrongtime.coord("time")
pts = list(tc._values_dm._real_array)
pts.append(70000)
tc._values_dm._real_array = np.asarray(pts)

aod_cube_wrongtime2 = aod_cube.copy()
tc = aod_cube_wrongtime2.coord("time")
pts = list(tc._values_dm._real_array)
pts[-1] = 70000
tc._values_dm._real_array = np.asarray(pts)

aod_cube_wrongtime3 = aod_cube.copy()
tc = aod_cube_wrongtime3.coord("time")
aod_cube_wrongtime3.remove_coord("time")


aod_cube_only_longname_dims = aod_cube.copy()
aod_cube_only_longname_dims.coord("longitude").standard_name = None
aod_cube_only_longname_dims.coord("longitude").var_name = None
aod_cube_only_longname_dims.coord("longitude").long_name = "lon"

aod_cube_only_longname_dims.coord("latitude").standard_name = None
aod_cube_only_longname_dims.coord("latitude").var_name = None
aod_cube_only_longname_dims.coord("latitude").long_name = "lat"

aod_cube_only_longname_dims.coord("time").standard_name = None
aod_cube_only_longname_dims.coord("time").var_name = None
aod_cube_only_longname_dims.coord("time").long_name = "time"

aod_cube_nounit = aod_cube.copy()
aod_cube_nounit.units = ""

FAKE_FILE = Path(tempfile.gettempdir()) / "test_iris_io/invalid.nc"
FAKE_FILE.parent.mkdir(exist_ok=True, parents=True)
FAKE_FILE.write_text("")


def test_check_time_coord():
    iris_io.check_time_coord(aod_cube, "monthly", 2010)


@pytest.mark.parametrize(
    "cube,ts_type,year,exception,error",
    [
        pytest.param(
            aod_cube_notime,
            "monthly",
            2010,
            AttributeError,
            "Cube does not contain time dimension",
            id="no time dimension",
        ),
        pytest.param(
            aod_cube,
            "blaa",
            2010,
            TemporalResolutionError,
            "Invalid input for ts_type blaa. Choose from ['minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'native']",
            id="wrong ts_type",
        ),
        pytest.param(
            aod_cube,
            "daily",
            2010,
            UnresolvableTimeDefinitionError,
            "Expected 365 timestamps but data has 12",
            id="daily from monthly",
        ),
        pytest.param(
            aod_cube,
            "daily",
            2012,
            UnresolvableTimeDefinitionError,
            "Expected 366 timestamps but data has 12",
            id="daily from monthly",
        ),
        pytest.param(
            aod_cube,
            "monthly",
            2008,
            ValueError,
            "First timestamp of data 2010-01-15T12:00:00.000000 does not lie in first period: 2008-01",
            id="worng year",
        ),
    ],
)
def test_check_time_coord_error(
    cube: CubeList, ts_type: str, year: int, exception: Type[Exception], error: str
):
    with pytest.raises(exception) as e:
        iris_io.check_time_coord(cube, ts_type, year)
    assert str(e.value) == error


def test_get_dim_names_cube():
    assert iris_io.get_dim_names_cube(aod_cube) == ["time", "latitude", "longitude"]


def test_get_dimnames_cube():
    assert iris_io.get_coord_names_cube(aod_cube) == ["time", "latitude", "longitude"]


@pytest.mark.parametrize(
    "cube,file,file_convention",
    [
        (
            aod_cube_notime,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
            None,
        ),
        (
            aod_cube_wrongtime2,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
            None,
        ),
        (
            aod_cube,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
            None,
        ),
        (
            aod_cube,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
            FileConventionRead("aerocom2"),
        ),
        (
            aod_cube_nounit,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
            None,
        ),
        (
            aod_cube_notime,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
            FileConventionRead("aerocom2"),
        ),
    ],
)
def test__cube_quality_check(cube, file, file_convention):
    cube = iris_io._cube_quality_check(cube, file, file_convention)
    assert [c.name() for c in cube.dim_coords] == ["time", "latitude", "longitude"]


def test__cube_quality_check_error():
    with pytest.raises(UnresolvableTimeDefinitionError) as e:
        iris_io._cube_quality_check(
            aod_cube_wrongtime, "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc"
        )
    error = "UnresolvableTimeDefinitionError('Expected 12 timestamps but data has 13')"
    assert str(e.value) == error


@pytest.mark.parametrize(
    "file,var_name",
    [
        (TM5_FILE1, None),
        (EMEP_FILE, "SURF_ug_NO2"),
    ],
)
def test_load_cube_custom(file, var_name):
    cube = iris_io.load_cube_custom(file, var_name)
    assert isinstance(cube, Cube)


@pytest.mark.parametrize(
    "file,var_name,exception,error",
    [
        pytest.param(
            FAKE_FILE,
            None,
            TranslationError,
            "The file appears empty or incomplete",
            id="enpty file",
        ),
        pytest.param(
            EMEP_FILE,
            None,
            NetcdfError,
            "Could not load single cube from",
            id="no cube",
        ),
        pytest.param(
            EMEP_FILE,
            "od550aer",
            NetcdfError,
            "Variable od550aer not available in file",
            id="no variable",
        ),
    ],
)
def test_load_cube_custom_error(
    file: Path | str, var_name: str | None, exception: Type[Exception], error: str
):
    with pytest.raises(exception) as e:
        iris_io.load_cube_custom(file, var_name)
    assert str(e.value).startswith(error)


@pytest.mark.parametrize(
    "files,num_loaded",
    [
        ([TM5_FILE1], 1),
        ([EMEP_FILE], 0),
    ],
)
def test_load_cubes_custom(files, num_loaded):
    result = iris_io.load_cubes_custom(files)
    assert isinstance(result, tuple) and len(result) == 2
    assert all(isinstance(res, list) for res in result)
    assert all(len(res) == num_loaded for res in result)


def test_check_dim_coord_names_cube():
    iris_io.check_dim_coord_names_cube(aod_cube_only_longname_dims)


@pytest.mark.parametrize(
    "cube,file",
    [
        (
            aod_cube_wrongtime3,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_daily.nc",
        ),
        (
            aod_cube,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
        ),
    ],
)
def test__check_correct_time_dim(cube: CubeList, file: str):
    cube = iris_io._check_correct_time_dim(cube, file)
    assert isinstance(cube, Cube)


@pytest.mark.parametrize(
    "cube,file,error",
    [
        pytest.param(
            aod_cube,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_-1_monthly.nc",
            "Invalid year -1 in filename aerocom3_TM5_AP3-CTRL2016_od550aer_Column_-1_monthly.nc",
            id="year=-1",
        ),
        pytest.param(
            aod_cube,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_20001_monthly.nc",
            "Invalid year 20001 in filename aerocom3_TM5_AP3-CTRL2016_od550aer_Column_20001_monthly.nc",
            id="year=20001",
        ),
    ],
)
def test__check_correct_time_dim_error(cube: CubeList, file: str, error: str):
    with pytest.raises(FileConventionError) as e:
        iris_io._check_correct_time_dim(cube, file)
    assert str(e.value) == error


def make_cubelist(dtype):
    return CubeList(
        [
            make_dummy_cube_3D_daily(2010, dtype=dtype),
            make_dummy_cube_3D_daily(2011, dtype=dtype),
        ]
    )


@pytest.mark.parametrize(
    "cubes,val",
    [
        (CubeList([Cube([1]), Cube([1])]), False),
        (CubeList([make_cubelist(int)[0], make_cubelist(float)[0]]), True),
        (make_cubelist(float), False),
        (make_cubelist(int), False),
    ],
)
def test__check_correct_dtypes_timedim_cube_list(cubes, val):
    result = iris_io._check_correct_dtypes_timedim_cube_list(cubes)
    assert result == val


@pytest.mark.parametrize(
    "cubes,sh",
    [
        (make_cubelist(int), (730, 12, 4)),  # see https://github.com/metno/pyaerocom/issues/432
        (make_cubelist(float), (730, 12, 4)),
    ],
)
def test_concatenate_iris_cubes(cubes, sh):
    result = iris_io.concatenate_iris_cubes(cubes)

    assert isinstance(result, Cube)
    assert result.shape == sh
