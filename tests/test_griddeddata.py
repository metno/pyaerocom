from __future__ import annotations

from datetime import datetime
from pathlib import Path

import iris
import iris.cube
import numpy as np
import pytest
import xarray as xr
from iris.cube import Cube
from numpy.testing import assert_allclose

from pyaerocom import GriddedData, Variable, const
from pyaerocom.exceptions import (
    CoordinateError,
    DataDimensionError,
    DataSearchError,
    VariableDefinitionError,
    VariableNotFoundError,
)
from pyaerocom.io import ReadGridded
from tests.conftest import TEST_RTOL, need_iris_32

TESTLATS = [-10, 20]
TESTLONS = [-120, 69]


def test_GriddedData_var_name():
    data = GriddedData()
    assert data.var_name is None
    data.var_name = "Blaaa"
    assert data.var_name == data.grid.var_name == "Blaaa"


def test_GriddedData_var_name_error():
    not_a_str = None
    with pytest.raises(TypeError) as e:
        GriddedData().var_name = not_a_str
    assert "Invalid input for var_name, need str, got " in str(e.value)


@pytest.mark.parametrize(
    "var_name, var_name_aerocom",
    [
        ("BlBlub", None),
        ("od550aer", "od550aer"),
        ("scatc550aer", "sc550aer"),
    ],
)
def test_GriddedData_var_name_aerocom(var_name, var_name_aerocom):
    data = GriddedData()
    data.var_name = var_name
    assert data.var_name_aerocom == var_name_aerocom


def test_GriddedData_var_info():
    data = GriddedData()
    data.var_name = "od550aer"
    assert isinstance(data.var_info, Variable)


def test_GriddedData_var_info_error():
    data = GriddedData()
    data.var_name = "manamana"
    with pytest.raises(VariableDefinitionError) as e:
        data.var_info
    assert str(e.value) == f"No default access available for variable {data.var_name}"


def test_GriddedData_long_name():
    data = GriddedData()
    assert data.long_name is None
    data.long_name = "blaaa"
    assert data.long_name == data.grid.long_name == "blaaa"


def test_GriddedData_suppl_info():
    assert isinstance(GriddedData().metadata, iris.cube.CubeAttrsDict)


def test_basic_properties(data_tm5: GriddedData):
    assert isinstance(data_tm5.cube, Cube)
    assert data_tm5.ts_type == "monthly"
    assert str(data_tm5.start) == "2010-01-01T00:00:00.000000"
    assert str(data_tm5.stop) == "2010-12-31T23:59:59.999999"
    assert len(data_tm5.time.points) == 12
    assert data_tm5.data_id == "TM5_AP3-CTRL2016"
    assert [Path(file).name for file in data_tm5.from_files] == [
        "aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc"
    ]
    assert data_tm5.shape == (12, 90, 120)
    assert data_tm5.lat_res == 2.0
    assert data_tm5.lon_res == 3.0


@need_iris_32
def test_GriddedData_longitude(data_tm5: GriddedData):
    """Test if longitudes are defined right"""
    assert str(data_tm5.longitude.units) == "degrees"

    lons = data_tm5.longitude.points
    assert (lons.min(), lons.max()) == (-178.5, 178.5)


def test_GriddedData_latitude(data_tm5: GriddedData):
    """test latitude array"""
    assert str(data_tm5.latitude.units) == "degrees"
    lats = data_tm5.latitude.points
    assert (lats.min(), lats.max()) == (-89, 89)


def test_GriddedData_time(data_tm5: GriddedData):
    """Test time dimension access and values"""
    time = data_tm5.time

    nominal_eq = ["julian", "day since 1850-01-01 00:00:00.0000000 UTC", False]
    vals_eq = [time.units.calendar, time.units.name, isinstance(time.cell(0).point, datetime)]
    assert nominal_eq == vals_eq


def test_GriddedData_resample_time(data_tm5: GriddedData):
    yearly = data_tm5.resample_time("yearly")
    assert yearly.shape == (1, 90, 120)

    assert_allclose(data_tm5.mean(), 0.11865, rtol=TEST_RTOL)
    assert_allclose(yearly.mean(), 0.11865, rtol=TEST_RTOL)


def test_GriddedData_interpolate(data_tm5: GriddedData):
    data = data_tm5.interpolate(latitude=TESTLATS, longitude=TESTLONS)

    assert type(data) is GriddedData
    assert data.shape == (12, 2, 2)

    assert_allclose(data.mean(False), 0.13877, rtol=TEST_RTOL)
    assert_allclose(data.mean(True), 0.13748, rtol=TEST_RTOL)


def test_GriddedData_to_time_series(data_tm5: GriddedData):
    stats = data_tm5.to_time_series(latitude=TESTLATS, longitude=TESTLONS)
    assert [stat.latitude for stat in stats] == [-9, 21]
    assert [stat.longitude for stat in stats] == [-118.5, 70.5]
    assert_allclose([stat.od550aer.mean() for stat in stats], [0.101353, 0.270886], rtol=TEST_RTOL)


def test_GriddedData_change_baseyear(data_tm5: GriddedData):
    data = data_tm5.copy()
    data.change_base_year(1901)
    assert str(data.time.units) == "days since 1901-01-01 00:00:00"


def test_GriddedData_min(data_tm5: GriddedData):
    assert_allclose(data_tm5.min(), 0.004629, atol=0.0001)


def test_GriddedData_nanmin(data_tm5: GriddedData):
    assert_allclose(data_tm5.nanmin(), 0.004629, atol=0.0001)


def test_GriddedData_max(data_tm5: GriddedData):
    assert_allclose(data_tm5.max(), 2.495539, atol=0.0001)


def test_GriddedData_nanmax(data_tm5: GriddedData):
    assert_allclose(data_tm5.nanmax(), 2.495539, atol=0.0001)


@pytest.mark.parametrize(
    "extend_percent,expected",
    [
        (0, (0.004, 2.496)),
        (15, (-0.4, 2.9)),
    ],
)
def test_GriddedData_estimate_value_range_from_data(
    data_tm5: GriddedData, extend_percent: int, expected: tuple[float]
):
    result = data_tm5.estimate_value_range_from_data(extend_percent)
    assert_allclose(result, expected, rtol=1e-2)


def test_GriddedData_area_weighted_mean(data_tm5: GriddedData):
    mean = data_tm5.area_weighted_mean()
    assert len(mean) == 12
    assert_allclose(mean.mean(), 0.118648, atol=0.001)


def test_GriddedData_mean(data_tm5: GriddedData):
    assert_allclose(data_tm5.mean(areaweighted=True), 0.11864813532841474)
    assert_allclose(data_tm5.mean(areaweighted=False), 0.09825691)


def test_GriddedData_std(data_tm5: GriddedData):
    assert_allclose(data_tm5.std(), 0.106527, atol=0.0001)


def test_GriddedData_short_str(data_tm5: GriddedData):
    assert data_tm5.short_str() == "od550aer (TM5_AP3-CTRL2016, freq=monthly, unit=1)"


def test_GriddedData_copy(data_tm5: GriddedData):
    data = data_tm5.copy()
    assert isinstance(data, GriddedData)
    assert data.cube is not data_tm5.cube


def test_GriddedData__check_lonlat_bounds(data_tm5: GriddedData):
    data = data_tm5.copy()
    data.latitude.bounds = None
    data.longitude.bounds = None
    data._check_lonlat_bounds()
    lonb = data.longitude.bounds
    latb = data.latitude.bounds
    assert isinstance(latb, np.ndarray)
    assert isinstance(lonb, np.ndarray)
    assert lonb.shape == (120, 2)
    assert latb.shape == (90, 2)


@pytest.mark.parametrize(
    "val,expected",
    [
        ("lon", {"var_name": "lon"}),
        ("longitude", {"standard_name": "longitude"}),
        ("Center coordinates for longitudes", {"long_name": "Center coordinates for longitudes"}),
        ("lat", {"var_name": "lat"}),
        ("latitude", {"standard_name": "latitude"}),
        ("Center coordinates for latitudes", {"long_name": "Center coordinates for latitudes"}),
        ("time", {"standard_name": "time"}),
        ("Time", {"long_name": "Time"}),
    ],
)
def test_GriddedData__check_coordinate_access(data_tm5: GriddedData, val: str, expected: dict):
    assert data_tm5._check_coordinate_access(val) == expected


def test_GriddedData__check_coordinate_access_error(data_tm5: GriddedData):
    wrong_coord = "not_a_coordinate"
    with pytest.raises(CoordinateError) as e:
        data_tm5._check_coordinate_access(wrong_coord)
    assert (
        str(e.value)
        == f"Could not associate one of the coordinates with input string {wrong_coord}"
    )


@pytest.mark.parametrize("add_aux", [True, False])
def test_GriddedData_delete_aux_vars(data_tm5: GriddedData, add_aux: bool):
    data = data_tm5.copy()

    if add_aux:
        auxc = iris.coords.AuxCoord(data.time.points, var_name="time2")
        data.cube.add_aux_coord(auxc, [0])
        assert len(data.cube.aux_coords) == 1

    data.delete_aux_vars()
    assert len(data.cube.aux_coords) == 0


def test_GriddedData_reader_setter(data_tm5: GriddedData):
    data = data_tm5.copy()
    data.reader = reader = ReadGridded("TM5-met2010_CTRL-TEST")
    assert data._reader is reader
    assert data.reader is reader


def test_GriddedData_reader_setter_error(data_tm5: GriddedData):
    with pytest.raises(ValueError) as e:
        data_tm5.copy().reader = 24
    assert str(e.value).startswith("cannot set reader")


def test_GriddedData_reader_getter(data_tm5: GriddedData):
    data = data_tm5.copy()
    data.metadata["data_id"] = "TM5-met2010_CTRL-TEST"
    assert data._reader is None
    assert isinstance(data.reader, ReadGridded)


def test_GriddedData_reader_getter_error(data_tm5: GriddedData):
    data = data_tm5.copy()
    data.metadata["data_id"] = data_id = "blaaaa"
    with pytest.raises(DataSearchError) as e:
        data.reader
    assert str(e.value) == f"No matches could be found for search pattern {data_id}"


def test_GriddedData_search_other():
    reader = ReadGridded("TM5-met2010_CTRL-TEST")
    variable = "od550aer"
    data = reader.read_var(variable, start=2010, ts_type="monthly")
    assert isinstance(data.search_other(variable), GriddedData)


def test_GriddedData_search_other_error():
    reader = ReadGridded("TM5-met2010_CTRL-TEST")
    data = reader.read_var("od550aer", start=2010, ts_type="monthly")
    wrong_variable = "concso4"
    with pytest.raises(VariableNotFoundError) as e:
        data.search_other(wrong_variable)
    assert str(e.value) == f"Could not find variable {wrong_variable}"


def test_GriddedData_update_meta(data_tm5: GriddedData):
    data = data_tm5.copy()
    data.update_meta(bla=42, blub=43)
    assert data.metadata["bla"] == 42
    assert data.metadata["blub"] == 43


@pytest.mark.parametrize("inplace", [True, False])
def test_GriddedData_delete_all_coords(data_tm5: GriddedData, inplace: bool):
    data = data_tm5.copy()
    new = data.delete_all_coords(inplace)
    assert new.cube.coords() == []
    if inplace:
        assert data is new
    else:
        assert len(data.cube.coords()) == 3


@pytest.mark.parametrize("inplace", [True, False])
def test_GriddedData_copy_coords(inplace: bool):
    reader = ReadGridded("TM5-met2010_CTRL-TEST")
    aod = reader.read_var("od550aer", start=2010, ts_type="monthly")
    abs = reader.read_var("abs550aer", start=2010, ts_type="monthly")
    result = aod.copy_coords(abs, inplace)
    assert (result.cube is aod.cube) == inplace
    for coord in abs.cube.coords():
        assert coord == result.cube.coord(coord.name())


def test_GriddedData_copy_coords_error():
    reader = ReadGridded("TM5-met2010_CTRL-TEST")
    aod = reader.read_var("od550aer", start=2010, ts_type="monthly")
    abs = reader.read_var("abs550aer", start=2010, ts_type="daily")
    with pytest.raises(DataDimensionError) as e:
        aod.copy_coords(abs, False)
    assert str(e.value) == "Cannot copy coordinates: shape mismatch"


def test_GriddedData_register_var_glob():
    arr = np.ones((10, 10, 10))
    arr[2:5] = 4
    var_name = "blablub"
    cube = Cube(arr, var_name=var_name)
    data = GriddedData(input=cube)
    data.register_var_glob()
    vars = const.VARS
    assert vars._all_vars[-1] == var_name
    vars._all_vars.pop(-1)
    del vars._vars_added[var_name]


@pytest.fixture
def fake_dataset_path(tmp_path: Path, var_name: str, units: str) -> Path:
    arr = xr.DataArray(np.ones(10))
    arr.attrs["var_name"] = var_name
    arr.attrs["units"] = units
    ds = arr.to_dataset(name=var_name)

    path = tmp_path / "output.nc"
    ds.to_netcdf(path)
    assert path.exists()
    return path


@pytest.mark.parametrize(
    "var_name,units,data_unit",
    [
        ("od550aer", "1", "1"),
        ("concso4", "ug S m-3", "ug S m-3"),
        ("concco", "ugC/m3", "ug C m-3"),
    ],
)
# iris after 3.7 changed warnings
@pytest.mark.filterwarnings(
    "ignore::iris.fileformats._nc_load_rules.helpers._WarnComboIgnoringCfLoad"
)
def test_GriddedData__check_invalid_unit_alias(
    fake_dataset_path: Path, var_name: str, data_unit: str
):
    data = GriddedData(fake_dataset_path, var_name=var_name, check_unit=False)
    data._check_invalid_unit_alias()
    assert data.units == data_unit


def test_mean_at_coords(data_tm5: GriddedData):
    data = data_tm5.copy()
    mean = data.mean_at_coords(latitude=data.lat.points, longitude=data.lon.points)
    assert isinstance(mean, np.floating)


def test__coords_to_iris_sample_points(data_tm5: GriddedData):
    data = data_tm5.copy()
    assert len(data._coords_to_iris_sample_points()) == 0
    points = data._coords_to_iris_sample_points(coords=(data.lat, data.lon))
    assert isinstance(points, list)
    assert points[0][1][0].shape == data.lat.shape
    assert points[0][1][1].shape == data.lon.shape


def test_extract_surface_level_wrong_dim(
    data_tm5: GriddedData,
):  # can only currently test the exception gets raised b/c don't have a good 4D testing dataset
    data = data_tm5.copy()
    with pytest.raises(DataDimensionError) as e:
        data.extract_surface_level()
    assert e.type is DataDimensionError


def test__infer_index_surface_level_wrong_dim(
    data_tm5: GriddedData,
):  # can only currently test the exception gets raised b/c don't have a good 4D testing dataset
    data = data_tm5.copy()
    with pytest.raises(DataDimensionError) as e:
        data._infer_index_surface_level()
    assert e.type is DataDimensionError


def test_find_closest_index_empty(
    data_tm5: GriddedData,
):  # can't find a place where called in codebase but doesn't seem to be deprecated
    empty = data_tm5.find_closest_index()
    assert len(empty) == 0


def test_remove_outliers(data_tm5: GriddedData):
    data = data_tm5.copy()
    new = data.remove_outliers(inplace=False)
    assert data.shape == new.shape
    assert new.metadata["outliers_removed"]


def test__resample_time_iris(data_tm5: GriddedData):
    data = data_tm5.copy()
    new = data._resample_time_iris("yearly")
    assert new.ts_type == "yearly"


def test_get_area_weighted_timeseries(data_tm5: GriddedData):
    data = data_tm5.copy()
    new = data.get_area_weighted_timeseries("EUROPE")
    assert new.region


def test_extract(data_tm5: GriddedData):
    data = data_tm5.copy()
    sub = data.extract(iris.Constraint(latitude=0.0))
    assert len(sub.shape) < len(data.shape)


def test_intersection(data_tm5: GriddedData):
    data = data_tm5.copy()
    new = data.intersection(longitude=(-70, 35))
    assert new.shape[0:1] == data.shape[0:1]
    assert new.shape[2] < data.shape[2]
