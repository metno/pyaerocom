from __future__ import annotations

from pathlib import Path
from typing import Type

import numpy as np
import pytest
import xarray as xr
from matplotlib.axes import Axes
from numpy.testing import assert_allclose
from numpy.typing import ArrayLike

from pyaerocom import ColocatedData
from pyaerocom.exceptions import DataCoverageError, DataDimensionError, MetaDataError

from .conftest import CHECK_PATHS, TESTDATADIR

EXAMPLE_FILE = TESTDATADIR / CHECK_PATHS["coldata_tm5_aeronet"]


@pytest.mark.parametrize("data", [EXAMPLE_FILE, str(EXAMPLE_FILE), np.ones((2, 3, 4))])
def test_ColocatedData__init__(data: Path | str | ArrayLike):
    cd = ColocatedData(data=data)
    assert isinstance(cd.data, xr.DataArray)


@pytest.mark.parametrize(
    "data,exception",
    [
        (None, AttributeError),
        ("Blaaaaa", IOError),
        (np.ones(3), DataDimensionError),
        ({}, ValueError),
    ],
)
def test_ColocatedData__init___error(data, exception: Type[Exception]):
    with pytest.raises(exception):
        ColocatedData(data=data).data


def test_ColocatedData_data():
    col = ColocatedData()
    col.data = data = xr.DataArray()
    assert col.data is data


def test_ColocatedData_data_error():
    col = ColocatedData()
    with pytest.raises(ValueError):
        col.data = "Blaaa"


def test_ColocatedData_data_source(coldata):
    ds = coldata["tm5_aeronet"].data_source
    assert isinstance(ds, xr.DataArray)
    assert len(ds) == 2


def test_ColocatedData_data_source_error(coldata):
    with pytest.raises(AttributeError) as e:
        coldata["fake_nodims"].data_source
    assert str(e.value).endswith("has no attribute 'data_source'")


def test_ColocatedData_var_name(coldata):
    cd = coldata["tm5_aeronet"]
    assert isinstance(cd.var_name, list)


def test_ColocatedData_var_name_error(coldata):
    with pytest.raises(AttributeError) as e:
        coldata["fake_nodims"].var_name
    assert str(e.value).endswith("has no attribute 'var_name'")


def test_ColocatedData_latitude(coldata):
    cd = coldata["tm5_aeronet"]
    assert isinstance(cd.latitude, xr.DataArray)


def test_ColocatedData_latitude_error(coldata):
    with pytest.raises(AttributeError) as e:
        coldata["fake_nodims"].latitude
    assert str(e.value).endswith("does not include latitude coordinate")


def test_ColocatedData_longitude(coldata):
    cd = coldata["tm5_aeronet"]
    assert isinstance(cd.longitude, xr.DataArray)


def test_ColocatedData_longitude_error(coldata):
    with pytest.raises(AttributeError) as e:
        coldata["fake_nodims"].longitude
    assert str(e.value).endswith("does not include longitude coordinate")


def test_ColocatedData_time(coldata):
    cd = coldata["tm5_aeronet"]
    assert isinstance(cd.time, xr.DataArray)


def test_ColocatedData_time_error(coldata):
    with pytest.raises(AttributeError) as e:
        coldata["fake_nodims"].time
    assert str(e.value).endswith("does not include time coordinate")


@pytest.mark.parametrize(
    "which,lat_range",
    [
        ("tm5_aeronet", (-43.2, 43.9)),
        ("fake_4d", (30, 50)),
    ],
)
def test_ColocatedData_lat_range(coldata, which: str, lat_range: tuple[float, float]):
    cd_lat_range = coldata[which].lat_range
    assert len(cd_lat_range) == len(lat_range) == 2
    assert_allclose(cd_lat_range, lat_range, rtol=1e-1)


def test_ColocatedData_lat_range_error(coldata):
    with pytest.raises(AttributeError) as e:
        coldata["fake_nodims"].lat_range
    assert str(e.value).endswith("does not include latitude coordinate")


@pytest.mark.parametrize(
    "which,lon_range",
    [
        ("tm5_aeronet", (-65.3, 121.5)),
        ("fake_4d", (10, 20)),
    ],
)
def test_ColocatedData_lon_range(coldata, which: str, lon_range: tuple[float, float]):
    cd_lon_range = coldata[which].lon_range
    assert len(cd_lon_range) == len(lon_range) == 2
    assert_allclose(cd_lon_range, lon_range, rtol=1e-1)


def test_ColocatedData_lon_range_error(coldata):
    with pytest.raises(AttributeError) as e:
        coldata["fake_nodims"].lon_range
    assert str(e.value).endswith("does not include longitude coordinate")


def test_ColocatedData_ts_type(coldata):
    cd = coldata["tm5_aeronet"]
    assert isinstance(cd.ts_type, str)


def test_ColocatedData_ts_type_error(coldata):
    with pytest.raises(ValueError) as e:
        coldata["fake_nodims"].ts_type
    assert str(e.value).endswith("does not contain information about temporal resolution")


def test_ColocatedData_units(coldata):
    units = coldata["tm5_aeronet"].units
    assert isinstance(units, list)
    assert bool(units) and all(isinstance(x, str) for x in units)


def test_ColocatedData_units_error(coldata):
    with pytest.raises(KeyError) as e:
        coldata["fake_nodims"].units
    assert "units" in str(e.value)


@pytest.mark.parametrize(
    "which,num_coords",
    [
        ("fake_4d", 6),
        ("fake_5d", 4),
        ("tm5_aeronet", 8),
        ("fake_3d", 4),
    ],
)
def test_ColocatedData_num_coords(coldata, which: str, num_coords: int):
    assert coldata[which].num_coords == num_coords


def test_ColocatedData_num_coords_error(coldata):
    with pytest.raises(DataDimensionError) as e:
        coldata["fake_nodims"].num_coords
    assert str(e.value).startswith("Need dimension")


@pytest.mark.parametrize(
    "which,num_coords_with_data",
    [
        ("tm5_aeronet", 8),
        ("fake_3d", 4),
        ("fake_4d", 5),
    ],
)
def test_ColocatedData_num_coords_with_data(coldata, which: str, num_coords_with_data: int):
    assert coldata[which].num_coords_with_data == num_coords_with_data


@pytest.mark.parametrize(
    "which,error",
    [
        ("fake_5d", "please reduce dimensionality"),
        ("fake_nodims", "Need dimension"),
    ],
)
def test_ColocatedData_num_coords_with_data_error(coldata, which: str, error: str):
    with pytest.raises(DataDimensionError) as e:
        coldata[which].num_coords_with_data
    assert error in str(e.value)


@pytest.mark.parametrize(
    "which,num_coords",
    [
        ("tm5_aeronet", 8),
        ("fake_4d", 5),
    ],
)
def test_ColocatedData_get_coords_valid_obs(coldata, which: str, num_coords: int):
    coords_valid_obs = coldata[which].get_coords_valid_obs()
    assert isinstance(coords_valid_obs, list)
    assert len(coords_valid_obs) == 2
    assert all(len(coord) == num_coords for coord in coords_valid_obs)


def test_ColocatedData_get_coords_valid_obs_error(coldata):
    with pytest.raises(ValueError) as e:
        coldata["fake_nodims"].get_coords_valid_obs()
    assert str(e.value).startswith("'time' not found in array dimensions")


@pytest.mark.parametrize(
    "which,args,chk",
    [
        ("fake_5d", {}, {"num_coords_with_data": np.nan, "num_coords_tot": 4, "totnum": 36}),
        ("tm5_aeronet", {}, {"nmb": -0.129, "R": 0.853}),
        # has random numbers in it so nmb, R check is risky with rtol=1e-2
        ("fake_3d", {}, {"num_coords_with_data": 4}),
        ("fake_4d", {}, {"nmb": 0}),
        ("fake_4d", {"use_area_weights": True}, {"nmb": 0}),
    ],
)
def test_ColocatedData_calc_statistics(coldata, which: str, args: dict, chk: dict):
    output = coldata[which].calc_statistics(**args)
    assert isinstance(output, dict)
    for key, val in chk.items():
        assert key in output
        assert_allclose(output[key], val, rtol=1e-2)


def test_ColocatedData_calc_statistics_error(coldata):
    with pytest.raises(DataDimensionError) as e:
        coldata["fake_nodims"].calc_statistics()
    assert str(e.value).startswith("Need dimension")


@pytest.mark.parametrize(
    "which,args,statistics",
    [
        ("fake_5d", {}, {}),
        ("tm5_aeronet", {}, {"nmb": -0.065, "R": 0.679}),
        ("fake_3d", {}, {}),
        ("fake_4d", {}, {"nmb": 0}),
        ("tm5_aeronet", {"aggr": "median"}, {"nmb": -0.0136, "R": 0.851}),
    ],
)
def test_ColocatedData_calc_temporal_statistics(
    coldata, which: str, args: dict, statistics: dict[str, float]
):
    temporal_statistics = coldata[which].calc_temporal_statistics(**args)
    assert isinstance(temporal_statistics, dict)
    for key, val in statistics.items():
        assert key in temporal_statistics
        assert_allclose(temporal_statistics[key], val, rtol=1e-2)


@pytest.mark.parametrize(
    "which,args,exception,error",
    [
        ("fake_nodims", {}, DataDimensionError, "Need dimension"),
        ("tm5_aeronet", {"aggr": "max"}, ValueError, "So far only mean and median are supported"),
    ],
)
def test_ColocatedData_calc_temporal_statistics_error(
    coldata, which: str, args: dict, exception: Type[Exception], error: str
):
    with pytest.raises(exception) as e:
        coldata[which].calc_temporal_statistics(**args)
    assert str(e.value).startswith(error)


@pytest.mark.parametrize(
    "which,args,statistics",
    [
        ("tm5_aeronet", {}, {"nmb": -0.304, "R": 0.893}),
        ("fake_3d", {}, {}),
        ("fake_4d", {}, {"nmb": 0}),
        ("fake_4d", {"use_area_weights": True}, {"nmb": 0}),
        ("tm5_aeronet", {"aggr": "median"}, {"nmb": -0.42, "R": 0.81}),
    ],
)
def test_ColocatedData_calc_spatial_statistics(
    coldata, which: str, args: dict, statistics: dict[str, float]
):
    spatial_statistics = coldata[which].calc_spatial_statistics(**args)
    assert isinstance(spatial_statistics, dict)
    for key, val in statistics.items():
        assert key in spatial_statistics
        assert_allclose(spatial_statistics[key], val, rtol=1e-2)


@pytest.mark.parametrize(
    "which,args,exception,error",
    [
        ("fake_nodims", {}, DataDimensionError, "Need dimension"),
        ("tm5_aeronet", {"aggr": "max"}, ValueError, "So far only mean and median are supported"),
    ],
)
def test_ColocatedData_calc_spatial_statistics_error(
    coldata, which: str, args: dict, exception: Type[Exception], error: str
):
    with pytest.raises(exception) as e:
        coldata[which].calc_spatial_statistics(**args)
    assert str(e.value).startswith(error)


@pytest.mark.parametrize("which", ["fake_5d", "fake_nodims", "tm5_aeronet", "fake_3d", "fake_4d"])
def test_ColocatedData_plot_scatter(coldata, which):
    plot = coldata[which].plot_scatter()
    assert isinstance(plot, Axes)


def test_meta_access_filename():
    name = "od550bc_ang4487aer_MOD-AEROCOM-MEDIAN_REF-42AeronET_20000101_20201231_monthly_WORLD-noMOUNTAINS.nc"

    meta = {
        "model_var": "od550bc",
        "obs_var": "ang4487aer",
        "model_name": "AEROCOM-MEDIAN",
        "obs_name": "42AeronET",
        "start": "20000101",
        "stop": "20201231",
        "ts_type": "monthly",
        "filter_name": "WORLD-noMOUNTAINS",
    }

    _meta = ColocatedData.get_meta_from_filename(name)
    assert _meta == meta


def test_read_colocated_data(coldata_tm5_aeronet):
    loaded = ColocatedData(EXAMPLE_FILE)
    mean_loaded = np.nanmean(loaded.data)
    mean_fixture = np.nanmean(coldata_tm5_aeronet.data.data)
    assert mean_fixture == mean_loaded


@pytest.mark.parametrize(
    "region_id,latrange,lonrange,numst",
    [
        ("RBU", (29.45, 66.26), (22, -170), 2),  # crosses lon=180 border
        ("WORLD", (-90, 90), (-180, 180), 8),
        ("NHEMISPHERE", (0, 90), (-180, 180), 5),
        ("EUROPE", (40, 72), (-10, 40), 2),
        ("OCN", (-90, 90), (-180, 180), 8),
    ],
)
def test_apply_latlon_filter(
    coldata_tm5_aeronet,
    region_id: str,
    latrange: tuple[float, float],
    lonrange: tuple[float, float],
    numst: int,
):
    filtered = coldata_tm5_aeronet.apply_latlon_filter(region_id=region_id)

    lats, lons = filtered.data.latitude.data, filtered.data.longitude.data
    assert len(filtered.data.station_name.data) == numst
    if numst > 0:
        assert lats.min() > latrange[0]
        assert lats.max() < latrange[1]
        if lonrange[0] < lonrange[1]:
            assert lons.min() > lonrange[0]
            assert lons.max() < lonrange[1]
        else:
            assert -180 < lons.min() < lonrange[1] or lonrange[0] < lons.min() < 180
            assert -180 < lons.max() < lonrange[1] or lonrange[0] < lons.max() < 180


@pytest.mark.parametrize(
    "region_id",
    [
        "PAN",  # crosses lon=180 border
        "NAM",  # crosses lon=180 border
    ],
)
def test_apply_latlon_filter_error(coldata_tm5_aeronet, region_id: str):
    with pytest.raises(DataCoverageError):
        coldata_tm5_aeronet.apply_latlon_filter(region_id=region_id)


@pytest.mark.parametrize(
    "which,region_id,check_country_meta,latrange,lonrange,numst",
    [
        ("fake_4d", "EUROPE", False, (40, 72), (-10, 40), 4),
        ("tm5_aeronet", "NHEMISPHERE", False, (0, 90), (-180, 180), 5),
        ("tm5_aeronet", "EUROPE", False, (40, 72), (-10, 40), 2),
        ("tm5_aeronet", "OCN", False, (-59.95, 66.25), (-132.55, 119.95), 1),
        ("tm5_aeronet", "Brazil", True, (-59.95, 66.25), (-132.55, 119.95), 1),
    ],
)
def test_ColocatedData_filter_region(
    coldata,
    which: str,
    region_id: str,
    check_country_meta: bool,
    latrange: tuple[float, float],
    lonrange: tuple[float, float],
    numst: int,
):
    cd = coldata[which]
    if check_country_meta:
        cd = cd.copy()
        cd.check_set_countries()

    filtered = cd.filter_region(region_id=region_id, check_country_meta=check_country_meta)
    lats, lons = filtered.data.latitude.data, filtered.data.longitude.data
    assert lats.min() >= latrange[0]
    assert lats.max() <= latrange[1]
    assert lons.min() >= lonrange[0]
    assert lons.max() <= lonrange[1]
    assert filtered.num_coords == numst


def test_ColocatedData_filter_region_error(coldata):
    cd = coldata["fake_4d"].copy()
    with pytest.raises(DataDimensionError) as e:
        cd.check_set_countries()
    assert str(e.value).startswith("Countries cannot be assigned")

    with pytest.raises(MetaDataError) as e:
        cd.filter_region(region_id="France", check_country_meta=True)
    assert str(e.value).startswith("No country information available")


@pytest.mark.parametrize(
    "which,filename",
    [
        (
            "tm5_aeronet",
            "od550aer_od550aer_MOD-TM5_AP3-CTRL2016_REF-AeronetSunV3L2Subset.daily_20100115_20101215_monthly_WORLD-noMOUNTAINS.nc",
        ),
        (
            "fake_3d_hr",
            "vmro3_vmro3_MOD-fakemod_REF-fakeobs_20180110_20180117_hourly_WORLD-wMOUNTAINS.nc",
        ),
        (
            "fake_3d",
            "concpm10_concpm10_MOD-fakemod_REF-fakeobs_20000115_20191215_monthly_WORLD-wMOUNTAINS.nc",
        ),
    ],
)
def test_ColocatedData_to_netcdf(coldata, tmp_path: Path, which: str, filename: str):
    path = tmp_path / filename
    assert not path.exists()
    file = coldata[which].to_netcdf(tmp_path)
    assert path == Path(file)
    assert path.exists()


@pytest.mark.parametrize("which", ["tm5_aeronet", "fake_3d_hr", "fake_3d"])
def test_ColocatedData_read_netcdf(coldata, tmp_path: Path, which: str):
    file = coldata[which].to_netcdf(tmp_path)
    assert Path(file).exists()
    cd = ColocatedData().read_netcdf(file)
    assert isinstance(cd, ColocatedData)


@pytest.mark.parametrize(
    "which,args,mean",
    [
        ("tm5_aeronet", dict(to_ts_type="yearly"), 0.336),
        ("tm5_aeronet", dict(to_ts_type="yearly", min_num_obs=14), np.nan),
        ("tm5_aeronet", dict(to_ts_type="yearly", settings_from_meta=True), 0.336),
        ("tm5_aeronet", dict(to_ts_type="yearly", colocate_time=True), 0.363),
    ],
)
def test_ColocatedData_resample_time(coldata, which: str, args: dict, mean):
    cd = coldata[which]
    resampled = cd.resample_time(**args)
    if args.get("inplace"):
        assert resampled is cd
    else:
        assert resampled is not cd

    resampled_mean = resampled.data.mean().data
    if np.isnan(mean):
        assert np.isnan(resampled_mean)
    else:
        assert_allclose(resampled_mean, mean, atol=1e-3)
