import tempfile
from contextlib import nullcontext as does_not_raise_exception
from pathlib import Path

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


@pytest.mark.parametrize(
    "cube,ts_type,year,raises",
    [
        (aod_cube, "monthly", 2010, does_not_raise_exception()),
        (aod_cube_notime, "monthly", 2010, pytest.raises(AttributeError)),
        (aod_cube, "blaa", 2010, pytest.raises(TemporalResolutionError)),
        (aod_cube, "daily", 2010, pytest.raises(UnresolvableTimeDefinitionError)),
        (aod_cube, "daily", 2012, pytest.raises(UnresolvableTimeDefinitionError)),
        (aod_cube, "monthly", 2008, pytest.raises(ValueError)),
    ],
)
def test_check_time_coord(cube, ts_type, year, raises):
    with raises:
        iris_io.check_time_coord(cube, ts_type, year)


def test_get_dim_names_cube():
    assert iris_io.get_dim_names_cube(aod_cube) == ["time", "latitude", "longitude"]


def test_get_dimnames_cube():
    assert iris_io.get_coord_names_cube(aod_cube) == ["time", "latitude", "longitude"]


@pytest.mark.parametrize(
    "cube,file,file_convention,raises,dimnames",
    [
        (
            aod_cube_notime,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
            None,
            does_not_raise_exception(),
            ["time", "latitude", "longitude"],
        ),
        (
            aod_cube_wrongtime2,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
            None,
            does_not_raise_exception(),
            ["time", "latitude", "longitude"],
        ),
        (
            aod_cube,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
            None,
            does_not_raise_exception(),
            ["time", "latitude", "longitude"],
        ),
        (
            aod_cube,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
            FileConventionRead("aerocom2"),
            does_not_raise_exception(),
            ["time", "latitude", "longitude"],
        ),
        (
            aod_cube_nounit,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
            None,
            does_not_raise_exception(),
            ["time", "latitude", "longitude"],
        ),
        (
            aod_cube_notime,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
            FileConventionRead("aerocom2"),
            does_not_raise_exception(),
            ["time", "latitude", "longitude"],
        ),
        (
            aod_cube_wrongtime,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
            None,
            pytest.raises(UnresolvableTimeDefinitionError),
            None,
        ),
    ],
)
def test__cube_quality_check(cube, file, file_convention, raises, dimnames):
    with raises:
        cube = iris_io._cube_quality_check(cube, file, file_convention)
        _dimnames = [c.name() for c in cube.dim_coords]
        assert _dimnames == dimnames


@pytest.mark.parametrize(
    "file,var_name,file_convention,perform_fmt_checks,raises",
    [
        (FAKE_FILE, None, None, None, pytest.raises(TranslationError)),
        (TM5_FILE1, None, None, None, does_not_raise_exception()),
        (EMEP_FILE, None, None, None, pytest.raises(NetcdfError)),
        (EMEP_FILE, "SURF_ug_NO2", None, None, does_not_raise_exception()),
        (EMEP_FILE, "od550aer", None, None, pytest.raises(NetcdfError)),
    ],
)
def test_load_cube_custom(file, var_name, file_convention, perform_fmt_checks, raises):
    with raises:
        result = iris_io.load_cube_custom(file, var_name, file_convention, perform_fmt_checks)
        assert isinstance(result, Cube)


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


@pytest.mark.parametrize(
    "cube,raises", [(aod_cube_only_longname_dims, does_not_raise_exception())]
)
def test_check_dim_coord_names_cube(cube, raises):
    with raises:
        iris_io.check_dim_coord_names_cube(cube)


@pytest.mark.parametrize(
    "cube,file,raises",
    [
        (
            aod_cube_wrongtime3,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_daily.nc",
            does_not_raise_exception(),
        ),
        (
            aod_cube,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc",
            does_not_raise_exception(),
        ),
        (
            aod_cube,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_-1_monthly.nc",
            pytest.raises(FileConventionError),
        ),
        (
            aod_cube,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_20001_monthly.nc",
            pytest.raises(FileConventionError),
        ),
    ],
)
def test__check_correct_time_dim(cube, file, raises):
    with raises:
        cube = iris_io._check_correct_time_dim(cube, file)
        assert isinstance(cube, Cube)


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
