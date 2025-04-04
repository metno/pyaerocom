from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import xarray as xr
from numpy.typing import ArrayLike
from pydantic import ValidationError

from pyaerocom import ColocatedData
from pyaerocom.config import ALL_REGION_NAME
from pyaerocom.exceptions import DataCoverageError, DataDimensionError
from tests.fixtures.collocated_data import EXAMPLE_FILE


@pytest.mark.parametrize("data", [EXAMPLE_FILE, str(EXAMPLE_FILE), np.ones((2, 3, 4))])
def test_ColocatedData_initialization(data: Path | str | ArrayLike):
    cd = ColocatedData(data=data)
    assert isinstance(cd.data, xr.DataArray)


@pytest.mark.parametrize(
    "data,exception",
    [
        ("Blaaaaa", ValueError),
        (np.ones(3), ValidationError),
        ({}, ValueError),
        (xr.DataArray(np.ones((2, 2, 2, 2, 1))), ValidationError),
    ],
)
def test_ColocatedData_initialization_error(data, exception: type[Exception]):
    with pytest.raises(exception):
        ColocatedData(data=data).data


def test_ColocatedData__init__():
    # test that ColocatedData can be given positional arguments
    data = np.ones((2, 2, 1))
    col_data = ColocatedData(data)
    assert col_data


def test_ColocatedData_data():
    data = xr.DataArray(np.ones((2, 2, 1)))
    col = ColocatedData(data=data)
    assert col.data is data


def test_ColocatedData_data_error():
    col = ColocatedData()
    with pytest.raises(ValueError):
        col.data = "Blaaa"


@pytest.mark.parametrize("coldataset", ["tm5_aeronet"])
def test_ColocatedData_data_source(coldata: ColocatedData):
    ds = coldata.data_source
    assert isinstance(ds, xr.DataArray)
    assert len(ds) == 2


@pytest.mark.parametrize("coldataset", ["fake_nodims"])
def test_ColocatedData_data_source_error(coldata: ColocatedData):
    with pytest.raises(AttributeError) as e:
        coldata.data_source
    assert str(e.value).endswith("has no attribute 'data_source'")


@pytest.mark.parametrize("coldataset", ["tm5_aeronet"])
def test_ColocatedData_var_name(coldata: ColocatedData):
    assert isinstance(coldata.var_name, list)


@pytest.mark.parametrize("coldataset", ["fake_nodims"])
def test_ColocatedData_var_name_error(coldata: ColocatedData):
    with pytest.raises(AttributeError) as e:
        coldata.var_name
    assert str(e.value).endswith("has no attribute 'var_name'")


@pytest.mark.parametrize("coldataset", ["tm5_aeronet"])
def test_ColocatedData_latitude(coldata: ColocatedData):
    assert isinstance(coldata.latitude, xr.DataArray)


@pytest.mark.parametrize("coldataset", ["fake_nodims"])
def test_ColocatedData_latitude_error(coldata: ColocatedData):
    with pytest.raises(AttributeError) as e:
        coldata.latitude
    assert str(e.value).endswith("object has no attribute 'latitude'")


@pytest.mark.parametrize("coldataset", ["tm5_aeronet"])
def test_ColocatedData_longitude(coldata: ColocatedData):
    assert isinstance(coldata.longitude, xr.DataArray)


@pytest.mark.parametrize("coldataset", ["fake_nodims"])
def test_ColocatedData_longitude_error(coldata: ColocatedData):
    with pytest.raises(AttributeError) as e:
        coldata.longitude
    assert str(e.value).endswith("object has no attribute 'longitude'")


@pytest.mark.parametrize("coldataset", ["tm5_aeronet"])
def test_ColocatedData_time(coldata: ColocatedData):
    assert isinstance(coldata.time, xr.DataArray)


@pytest.mark.parametrize("coldataset", ["fake_nodims"])
def test_ColocatedData_time_error(coldata: ColocatedData):
    with pytest.raises(AttributeError) as e:
        coldata.time
    assert str(e.value).endswith("object has no attribute 'time'")


@pytest.mark.parametrize(
    "coldataset,lat_range",
    [
        ("tm5_aeronet", (-43.2, 43.9)),
        ("fake_4d", (30, 50)),
    ],
)
def test_ColocatedData_lat_range(coldata: ColocatedData, lat_range: tuple[float, float]):
    assert coldata.lat_range == pytest.approx(lat_range, rel=1e-1)


@pytest.mark.parametrize("coldataset", ["fake_nodims"])
def test_ColocatedData_lat_range_error(coldata: ColocatedData):
    with pytest.raises(AttributeError) as e:
        coldata.lat_range
    assert "object has no attribute" in str(e.value)


@pytest.mark.parametrize(
    "coldataset,lon_range",
    [
        ("tm5_aeronet", (-65.3, 121.5)),
        ("fake_4d", (10, 20)),
    ],
)
def test_ColocatedData_lon_range(coldata: ColocatedData, lon_range: tuple[float, float]):
    assert coldata.lon_range == pytest.approx(lon_range, rel=1e-1)


@pytest.mark.parametrize("coldataset", ["fake_nodims"])
def test_ColocatedData_lon_range_error(coldata: ColocatedData):
    with pytest.raises(AttributeError) as e:
        coldata.lon_range
    assert "object has no attribute" in str(e.value)


@pytest.mark.parametrize("coldataset", ["tm5_aeronet"])
def test_ColocatedData_ts_type(coldata: ColocatedData):
    assert isinstance(coldata.ts_type, str)


@pytest.mark.parametrize("coldataset", ["fake_nodims"])
def test_ColocatedData_ts_type_error(coldata: ColocatedData):
    with pytest.raises(ValueError) as e:
        coldata.ts_type
    assert str(e.value).endswith("does not contain information about temporal resolution")


@pytest.mark.parametrize("coldataset", ["tm5_aeronet"])
def test_ColocatedData_units(coldata: ColocatedData):
    units = coldata.units
    assert isinstance(units, list)
    assert bool(units) and all(isinstance(x, str) for x in units)


@pytest.mark.parametrize("coldataset", ["fake_nodims"])
def test_ColocatedData_units_error(coldata: ColocatedData):
    with pytest.raises(KeyError) as e:
        coldata.units
    assert "units" in str(e.value)


@pytest.mark.parametrize(
    "coldataset,num_coords",
    [
        ("fake_4d", 6),
        ("tm5_aeronet", 8),
        ("fake_3d", 4),
    ],
)
def test_ColocatedData_num_coords(coldata: ColocatedData, num_coords: int):
    assert coldata.num_coords == num_coords


@pytest.mark.parametrize("coldataset", ["fake_nodims"])
def test_ColocatedData_num_coords_error(coldata: ColocatedData):
    with pytest.raises(DataDimensionError) as e:
        coldata.num_coords
    assert str(e.value).startswith("Need dimension")


@pytest.mark.parametrize(
    "coldataset,num_coords_with_data",
    [
        ("tm5_aeronet", 8),
        ("fake_3d", 4),
        ("fake_4d", 5),
    ],
)
def test_ColocatedData_num_coords_with_data(coldata: ColocatedData, num_coords_with_data: int):
    assert coldata.num_coords_with_data == num_coords_with_data


@pytest.mark.parametrize(
    "coldataset,error",
    [
        ("fake_nodims", "Need dimension"),
    ],
)
def test_ColocatedData_num_coords_with_data_error(coldata: ColocatedData, error: str):
    with pytest.raises(DataDimensionError) as e:
        coldata.num_coords_with_data
    assert error in str(e.value)


@pytest.mark.parametrize(
    "coldataset,num_coords",
    [
        ("tm5_aeronet", 8),
        ("fake_4d", 5),
    ],
)
def test_ColocatedData_get_coords_valid_obs(coldata: ColocatedData, num_coords: int):
    coords_valid_obs = coldata.get_coords_valid_obs()
    assert isinstance(coords_valid_obs, list)
    assert len(coords_valid_obs) == 2
    assert all(len(coord) == num_coords for coord in coords_valid_obs)


@pytest.mark.parametrize("coldataset", ["fake_nodims"])
def test_ColocatedData_get_coords_valid_obs_error(coldata: ColocatedData):
    with pytest.raises(ValueError) as e:
        coldata.get_coords_valid_obs()
    assert str(e.value).startswith("'time' not found in array dimensions")


@pytest.mark.parametrize(
    "coldataset,use_area_weights,chk",
    [
        ("tm5_aeronet", False, {"nmb": -0.129, "R": 0.853}),
        # has random numbers in it so nmb, R check is risky with rtol=1e-2
        ("fake_3d", False, {"num_coords_with_data": 4}),
        ("fake_4d", False, {"nmb": 0}),
        ("fake_4d", True, {"nmb": 0}),
    ],
)
def test_ColocatedData_calc_statistics(coldata: ColocatedData, use_area_weights: bool, chk: dict):
    output = coldata.calc_statistics(use_area_weights=use_area_weights)
    assert isinstance(output, dict)
    for key, val in chk.items():
        assert output[key] == pytest.approx(val, rel=1e-2, nan_ok=True)


@pytest.mark.parametrize("coldataset", ["fake_nodims"])
def test_ColocatedData_calc_statistics_error(coldata: ColocatedData):
    with pytest.raises(DataDimensionError) as e:
        coldata.calc_statistics()
    assert str(e.value).startswith("Need dimension")


@pytest.mark.parametrize(
    "coldataset,aggr,statistics",
    [
        ("tm5_aeronet", None, {"nmb": -0.065, "R": 0.679}),
        ("fake_3d", None, {}),
        ("fake_4d", None, {"nmb": 0}),
        ("tm5_aeronet", "median", {"nmb": -0.0136, "R": 0.851}),
    ],
)
def test_ColocatedData_calc_temporal_statistics(
    coldata: ColocatedData, aggr: str | None, statistics: dict[str, float]
):
    temporal_statistics = coldata.calc_temporal_statistics(aggr=aggr)
    assert isinstance(temporal_statistics, dict)
    for key, val in statistics.items():
        assert temporal_statistics[key] == pytest.approx(val, rel=1e-2)


@pytest.mark.parametrize(
    "coldataset,aggr,exception,error",
    [
        ("fake_nodims", None, DataDimensionError, "Need dimension"),
        ("tm5_aeronet", "max", ValueError, "So far only mean and median are supported"),
    ],
)
def test_ColocatedData_calc_temporal_statistics_error(
    coldata: ColocatedData, aggr: str | None, exception: type[Exception], error: str
):
    with pytest.raises(exception) as e:
        coldata.calc_temporal_statistics(aggr=aggr)
    assert str(e.value).startswith(error)


@pytest.mark.parametrize(
    "coldataset,args,statistics",
    [
        ("tm5_aeronet", {}, {"nmb": -0.304, "R": 0.893}),
        ("fake_3d", {}, {}),
        ("fake_4d", {}, {"nmb": 0}),
        ("fake_4d", {"use_area_weights": True}, {"nmb": 0}),
        ("tm5_aeronet", {"aggr": "median"}, {"nmb": -0.42, "R": 0.81}),
    ],
)
def test_ColocatedData_calc_spatial_statistics(
    coldata: ColocatedData, args: dict, statistics: dict[str, float]
):
    spatial_statistics = coldata.calc_spatial_statistics(**args)
    assert isinstance(spatial_statistics, dict)
    for key, val in statistics.items():
        assert spatial_statistics[key] == pytest.approx(val, rel=1e-2)


@pytest.mark.parametrize(
    "coldataset,aggr,exception,error",
    [
        ("fake_nodims", None, DataDimensionError, "Need dimension"),
        ("tm5_aeronet", "max", ValueError, "So far only mean and median are supported"),
    ],
)
def test_ColocatedData_calc_spatial_statistics_error(
    coldata: ColocatedData, aggr: str | None, exception: type[Exception], error: str
):
    with pytest.raises(exception) as e:
        coldata.calc_spatial_statistics(aggr=aggr)
    assert str(e.value).startswith(error)


def test_meta_access_filename():
    name = f"od550bc_ang4487aer_MOD-AEROCOM-MEDIAN_REF-42AeronET_20000101_20201231_monthly_{ALL_REGION_NAME}-noMOUNTAINS.nc"

    meta = {
        "model_var": "od550bc",
        "obs_var": "ang4487aer",
        "model_name": "AEROCOM-MEDIAN",
        "obs_name": "42AeronET",
        "start": "20000101",
        "stop": "20201231",
        "ts_type": "monthly",
        "filter_name": f"{ALL_REGION_NAME}-noMOUNTAINS",
    }

    _meta = ColocatedData.get_meta_from_filename(name)
    assert _meta == meta


def test_read_colocated_data(coldata_tm5_aeronet):
    loaded = ColocatedData(data=EXAMPLE_FILE)
    mean_loaded = np.nanmean(loaded.data)
    mean_fixture = np.nanmean(coldata_tm5_aeronet.data.data)
    assert mean_fixture == mean_loaded


@pytest.mark.parametrize(
    "region_id,latrange,lonrange,numst",
    [
        ("RBU", (29.45, 66.26), (22, -170), 2),  # crosses lon=180 border
        (ALL_REGION_NAME, (-90, 90), (-180, 180), 8),
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
    "coldataset,region_id,check_country_meta,latrange,lonrange,numst",
    [
        ("fake_4d", "EUROPE", False, (40, 72), (-10, 40), 4),
        ("tm5_aeronet", "NHEMISPHERE", False, (0, 90), (-180, 180), 5),
        ("tm5_aeronet", "EUROPE", False, (40, 72), (-10, 40), 2),
        ("tm5_aeronet", "OCN", False, (-59.95, 66.25), (-132.55, 119.95), 1),
        ("tm5_aeronet", "Brazil", True, (-59.95, 66.25), (-132.55, 119.95), 1),
    ],
)
def test_ColocatedData_filter_region(
    coldata: ColocatedData,
    region_id: str,
    check_country_meta: bool,
    latrange: tuple[float, float],
    lonrange: tuple[float, float],
    numst: int,
):
    coldata = coldata
    if check_country_meta:
        coldata.check_set_countries()

    filtered = coldata.filter_region(region_id=region_id, check_country_meta=check_country_meta)
    lats, lons = filtered.data.latitude.data, filtered.data.longitude.data
    assert lats.min() >= latrange[0]
    assert lats.max() <= latrange[1]
    assert lons.min() >= lonrange[0]
    assert lons.max() <= lonrange[1]
    assert filtered.num_coords == numst


@pytest.mark.parametrize("coldataset", ["fake_4d"])
def test_ColocatedData_filter_region_error(coldata: ColocatedData):
    with pytest.raises(DataDimensionError) as e:
        coldata.check_set_countries()
    assert str(e.value).startswith("Countries cannot be assigned")

    with pytest.raises(AttributeError) as e:
        coldata.filter_region(region_id="France", check_country_meta=True)
    assert str(e.value).endswith("'ColocatedData' object has no attribute 'countries_available'")


@pytest.mark.parametrize(
    "coldataset,filename",
    [
        (
            "tm5_aeronet",
            f"od550aer_od550aer_MOD-TM5_AP3-CTRL2016_REF-AeronetSunV3L2Subset.daily_20100115_20101215_monthly_{ALL_REGION_NAME}-noMOUNTAINS.nc",
        ),
        (
            "fake_3d_hr",
            f"vmro3_vmro3_MOD-fakemod_REF-fakeobs_20180110_20180117_hourly_{ALL_REGION_NAME}-wMOUNTAINS.nc",
        ),
        (
            "fake_3d",
            f"concpm10_concpm10_MOD-fakemod_REF-fakeobs_20000115_20191215_monthly_{ALL_REGION_NAME}-wMOUNTAINS.nc",
        ),
    ],
)
def test_ColocatedData_to_netcdf(coldata: ColocatedData, tmp_path: Path, filename: str):
    path = tmp_path / filename
    assert not path.exists()
    file = coldata.to_netcdf(tmp_path)
    assert path == Path(file)
    assert path.exists()


@pytest.mark.parametrize("coldataset", ["tm5_aeronet", "fake_3d_hr", "fake_3d"])
def test_ColocatedData_read_netcdf(coldata: ColocatedData, tmp_path: Path):
    file = coldata.to_netcdf(tmp_path)
    assert Path(file).exists()
    cd = ColocatedData(file)
    assert isinstance(cd, ColocatedData)


@pytest.mark.parametrize(
    "coldataset,args,mean",
    [
        ("tm5_aeronet", dict(to_ts_type="yearly"), 0.336),
        ("tm5_aeronet", dict(to_ts_type="yearly", min_num_obs=14), np.nan),
        ("tm5_aeronet", dict(to_ts_type="yearly", settings_from_meta=True), 0.336),
        ("tm5_aeronet", dict(to_ts_type="yearly", colocate_time=True), 0.363),
    ],
)
def test_ColocatedData_resample_time(coldata: ColocatedData, args: dict, mean):
    resampled = coldata.resample_time(**args)
    assert (resampled is coldata) == args.get("inplace", False)

    resampled_mean = resampled.data.mean().data
    assert resampled_mean == pytest.approx(mean, abs=1e-3, nan_ok=True)


@pytest.mark.parametrize(
    "coldataset",
    (
        pytest.param(
            "tm5_aeronet",
        ),
        pytest.param(
            "fake_3d_hr",
        ),
        pytest.param(
            "fake_3d",
        ),
    ),
)
def test_ColocatedData_to_dataframe(coldata: ColocatedData):
    df = coldata.to_dataframe()

    exp_columns = set(
        [
            "time",
            "station_name",
            "data_source_obs",
            "latitude",
            "longitude",
            "altitude",
            f"{coldata.var_name[0]}_obs",
            "data_source_mod",
            f"{coldata.var_name[1]}_mod",
        ]
    )

    assert df.shape[1] == 9
    assert set(df.columns) == exp_columns
    assert not df["time"].isnull().values.any()
    assert not df["data_source_obs"].isnull().values.any()
    assert not df["data_source_mod"].isnull().values.any()


@pytest.mark.parametrize(
    "coldataset",
    (
        pytest.param(
            "fake_4d",
        ),
    ),
)
def test_ColocatedData_to_dataframe_exception(coldata: ColocatedData):
    with pytest.raises(NotImplementedError):
        coldata.to_dataframe()


@pytest.mark.parametrize(
    "coldataset",
    (
        pytest.param(
            "tm5_aeronet",
        ),
        pytest.param(
            "fake_3d_hr",
        ),
        pytest.param(
            "fake_3d",
        ),
    ),
)
def test_ColocatedData_from_dataframe(coldata: ColocatedData):
    df = coldata.to_dataframe()

    ColocatedData.from_dataframe(df)
