from __future__ import annotations

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
from tests.fixtures.aeroval import make_dummy_cube_3D_daily
from tests.fixtures.data_access import DataForTests
from tests.fixtures.tm5 import CHECK_PATHS

TM5_FILE = DataForTests(CHECK_PATHS.tm5aod).path


@pytest.fixture()
def cube(defect: Cube | str | None) -> Cube:
    """TM5 AOD cube, with optional deffects"""
    cube: Cube = load(str(TM5_FILE))[0]

    if defect == "notime":
        cube.remove_coord("time")

    if defect == "wrongtime":
        time = cube.coord("time")
        pts = list(time._values_dm._real_array)
        pts.append(70000)
        time._values_dm._real_array = np.asarray(pts)

    if defect == "wrongtime2":
        time = cube.coord("time")
        pts = list(time._values_dm._real_array)
        pts[-1] = 70000
        time._values_dm._real_array = np.asarray(pts)

    if defect == "wrongtime3":
        cube.remove_coord("time")

    if defect == "only_longname_dims":
        cube.coord("longitude").standard_name = None
        cube.coord("longitude").var_name = None
        cube.coord("longitude").long_name = "lon"

        cube.coord("latitude").standard_name = None
        cube.coord("latitude").var_name = None
        cube.coord("latitude").long_name = "lat"

        cube.coord("time").standard_name = None
        cube.coord("time").var_name = None
        cube.coord("time").long_name = "time"

    if defect == "nounit":
        cube.units = ""

    return cube


@pytest.fixture(scope="session")
def fake_file(tmp_path_factory) -> Path:
    """empty/invalid NetCDF file"""
    path: Path = tmp_path_factory.mktemp("test_iris_io") / "invalid.nc"
    path.write_bytes(b"")
    return path


@pytest.fixture()
def file_path(file: str, path_emep: dict[str, Path], fake_file: Path) -> Path:
    """dispatch TM5/EMEP/Empty file path"""
    files = dict(tm5=TM5_FILE, emep=path_emep["monthly"], empty=fake_file)
    try:
        return files[file.casefold()]
    except KeyError:
        raise ValueError(f"Unknown {file=}") from None


@pytest.fixture()
def file_paths(file_path: Path) -> list[Path]:
    """dispatch TM5/EMEP/Empty file path"""
    return [file_path]


@pytest.mark.parametrize("defect", [None])
def test_check_time_coord(cube: Cube):
    iris_io.check_time_coord(cube, "monthly", 2010)


@pytest.mark.parametrize(
    "defect,ts_type,year,exception,error",
    [
        pytest.param(
            "notime",
            "monthly",
            2010,
            AttributeError,
            "Cube does not contain time dimension",
            id="no time dimension",
        ),
        pytest.param(
            None,
            "blaa",
            2010,
            TemporalResolutionError,
            "Invalid input for ts_type blaa. Choose from ('minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'native', 'coarsest')",
            id="wrong ts_type",
        ),
        pytest.param(
            None,
            "daily",
            2010,
            UnresolvableTimeDefinitionError,
            "Expected 365 timestamps but data has 12",
            id="daily from monthly",
        ),
        pytest.param(
            None,
            "daily",
            2012,
            UnresolvableTimeDefinitionError,
            "Expected 366 timestamps but data has 12",
            id="daily from monthly",
        ),
        pytest.param(
            None,
            "monthly",
            2008,
            ValueError,
            "First timestamp of data 2010-01-15T12:00:00.000000 does not lie in first period: 2008-01",
            id="wrong year",
        ),
    ],
)
def test_check_time_coord_error(
    cube: Cube, ts_type: str, year: int, exception: type[Exception], error: str
):
    with pytest.raises(exception) as e:
        iris_io.check_time_coord(cube, ts_type, year)
    assert str(e.value) == error


@pytest.mark.parametrize("defect", [None])
def test_get_dim_names_cube(cube: Cube):
    assert iris_io.get_dim_names_cube(cube) == ["time", "latitude", "longitude"]


@pytest.mark.parametrize("defect", [None])
def test_get_dimnames_cube(cube: Cube):
    assert iris_io.get_coord_names_cube(cube) == ["time", "latitude", "longitude"]


@pytest.mark.parametrize(
    "defect,file_convention,coords",
    [
        pytest.param(
            None,
            None,
            ["time", "latitude", "longitude"],
            id="TM5",
        ),
        pytest.param(
            None,
            FileConventionRead("aerocom2"),
            ["time", "latitude", "longitude"],
            id="TM5 AeroCom2",
        ),
        pytest.param(
            "notime",
            None,
            ["time", "latitude", "longitude"],
            id="NoTime",
        ),
        pytest.param(
            "notime",
            FileConventionRead("aerocom2"),
            ["latitude", "longitude"],  # no time can be inferred under aerocom2
            id="NoTime AeroCom2",
        ),
        pytest.param(
            "wrongtime2",
            None,
            ["time", "latitude", "longitude"],
            id="WrongTime",
        ),
        pytest.param(
            "nounit",
            None,
            ["time", "latitude", "longitude"],
            id="WrongUnit",
        ),
    ],
)
def test__cube_quality_check(cube: Cube, file_convention, coords: list[str]):
    cube = iris_io._cube_quality_check(cube, TM5_FILE.name, file_convention)
    assert [c.name() for c in cube.dim_coords] == coords


@pytest.mark.parametrize("defect", ["wrongtime"])
def test__cube_quality_check_error(cube: Cube):
    with pytest.raises(UnresolvableTimeDefinitionError) as e:
        iris_io._cube_quality_check(cube, TM5_FILE.name)
    error = "UnresolvableTimeDefinitionError('Expected 12 timestamps but data has 13')"
    assert str(e.value) == error


@pytest.mark.parametrize(
    "file,var_name",
    [
        ("tm5", None),
        ("emep", "SURF_ug_NO2"),
    ],
)
def test_load_cube_custom(file_path: Path, var_name: str | None):
    cube = iris_io.load_cube_custom(file_path, var_name)
    assert isinstance(cube, Cube)


@pytest.mark.parametrize(
    "file,var_name,exception,error",
    [
        pytest.param(
            "empty",
            None,
            TranslationError,
            "The file appears empty or incomplete",
            id="enpty file",
        ),
        pytest.param(
            "EMEP",
            None,
            NetcdfError,
            "Could not load single cube from",
            id="no cube",
        ),
        pytest.param(
            "EMEP",
            "od550aer",
            NetcdfError,
            "Variable od550aer not available in file",
            id="no variable",
        ),
    ],
)
def test_load_cube_custom_error(
    file_path: Path, var_name: str | None, exception: type[Exception], error: str
):
    with pytest.raises(exception) as e:
        iris_io.load_cube_custom(file_path, var_name)
    assert str(e.value).startswith(error)


@pytest.mark.parametrize(
    "file,num_loaded",
    [
        ("tm5", 1),
        ("emep", 0),
    ],
)
def test_load_cubes_custom(file_paths: list[Path], num_loaded: int):
    result = iris_io.load_cubes_custom(file_paths)
    assert isinstance(result, tuple) and len(result) == 2
    assert all(isinstance(res, list) for res in result)
    assert all(len(res) == num_loaded for res in result)


@pytest.mark.parametrize("defect", ["only_longname_dims"])
def test_check_dim_coord_names_cube(cube: Cube):
    iris_io.check_dim_coord_names_cube(cube)


@pytest.mark.parametrize("defect", ["wrongtime3", None])
def test__check_correct_time_dim(cube: Cube):
    cube = iris_io._check_correct_time_dim(cube, TM5_FILE.name)
    assert isinstance(cube, Cube)


@pytest.mark.parametrize(
    "defect,file,error",
    [
        pytest.param(
            None,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_-1_monthly.nc",
            "Invalid year -1 in filename aerocom3_TM5_AP3-CTRL2016_od550aer_Column_-1_monthly.nc",
            id="year=-1",
        ),
        pytest.param(
            None,
            "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_20001_monthly.nc",
            "Invalid year 20001 in filename aerocom3_TM5_AP3-CTRL2016_od550aer_Column_20001_monthly.nc",
            id="year=20001",
        ),
    ],
)
def test__check_correct_time_dim_error(cube: Cube, file: str, error: str):
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
