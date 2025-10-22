from datetime import datetime

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from pyaerocom.griddeddata import GriddedData
from pyaerocom.io.cams2_82.reader import (
    AEROCOM_NAMES,
    UNITS,
    ReadCAMS2_82,
    check_files,
    drop_vars,
    model_paths,
    only_first_day,
    read_dataset,
)

times3h = pd.date_range(start="2025-07-01", freq="3h", periods=12)
timesfew = pd.date_range(start="2025-03-01", freq="3h", periods=1)
timesdup = pd.date_range(start="2025-05-01", freq="3h", periods=2).append(
    pd.date_range(start="2025-05-01", freq="3h", periods=2)
)
levels = np.arange(64, 138)
latitudes = np.arange(20.0, -20.5, -0.5)
longitudes = np.arange(0.0, 20.0, 0.5)


def dummy_model_data_create(timeindex):
    return xr.Dataset(
        {
            "aerext1064": xr.DataArray(
                data=np.ones(shape=(len(timeindex), len(levels), len(latitudes), len(longitudes))),
                dims=["time", "level", "latitude", "longitude"],
                coords={
                    "time": timeindex,
                    "level": levels,
                    "latitude": latitudes,
                    "longitude": longitudes,
                },
                attrs={"units": "m**-1"},
            ),
            "aerext532": xr.DataArray(
                data=np.ones(shape=(len(timeindex), len(levels), len(latitudes), len(longitudes))),
                dims=["time", "level", "latitude", "longitude"],
                coords={
                    "time": timeindex,
                    "level": levels,
                    "latitude": latitudes,
                    "longitude": longitudes,
                },
                attrs={"units": "m**-1"},
            ),
        }
    )


@pytest.fixture()
def dummy_model_data():
    return dummy_model_data_create(times3h)


@pytest.fixture()
def dummy_model_data_too_few_times():
    return dummy_model_data_create(timesfew)


@pytest.fixture()
def dummy_model_data_duplicates():
    return dummy_model_data_create(timesdup)


@pytest.fixture()
def dummy_model_path(tmp_path, dummy_model_data):
    path = tmp_path / "2025/20250701_cIFS-00UTC_o-suite_multilev.nc"
    path.parent.mkdir(exist_ok=True, parents=True)
    dummy_model_data.to_netcdf(path)
    return path


@pytest.fixture()
def dummy_model_path_duplicates(tmp_path, dummy_model_data_duplicates):
    path = tmp_path / "2025/20250501_cIFS-00UTC_o-suite_multilev.nc"
    dummy_model_data_duplicates.to_netcdf(path)
    return path


@pytest.fixture()
def dummy_model_path_too_few_times(tmp_path, dummy_model_data_too_few_times):
    path = tmp_path / "2025/20250301_cIFS-00UTC_o-suite_multilev.nc"
    dummy_model_data_too_few_times.to_netcdf(path)
    return path


def test_drop_vars(dummy_model_data):
    assert "aerext532" in dummy_model_data.data_vars
    ds = drop_vars(dummy_model_data)
    assert "aerext532" not in ds.data_vars


def test_only_first_day(dummy_model_data):
    assert len(dummy_model_data.time) == 12
    ds = only_first_day(dummy_model_data)
    assert len(ds.time) == 8


def test_read_dataset(dummy_model_path):
    ds = read_dataset([dummy_model_path])
    assert "altitude" in ds.dims
    assert len(ds.altitude) == len(levels)
    assert set(list(AEROCOM_NAMES.values())) == set(list(ds.keys()))
    for var in ds.data_vars:
        assert (
            ds[var].units
            == UNITS[list(AEROCOM_NAMES.keys())[list(AEROCOM_NAMES.values()).index(var)]]
        )


def test_model_paths(dummy_model_path):
    paths = model_paths("aerext1064", datetime(2025, 7, 1), root_path=dummy_model_path.parent)
    assert list(paths) == [dummy_model_path]


def test_ReadCAMS2_82(dummy_model_path, caplog):
    reader = ReadCAMS2_82(data_dir=dummy_model_path.parent, data_id="IFS")
    reader.daterange = ("2025-07-01", "2025-07-01")
    assert reader.daterange.values[0] == np.datetime64("2025-07-01T00:00:00.000000000")
    assert reader.filepaths == [dummy_model_path]
    data = reader.read_var("ec1064aer", "3hourly")
    assert isinstance(data, GriddedData)
    assert data.altitude.shape[0] == len(levels)
    for species in ["no2", "go3", "aod550", "pm10", "pm2p5"]:
        assert f"Could not find any files for {species}" in caplog.text


def test_ReadCAMS2_82_nodata(tmp_path):
    with pytest.raises(ValueError) as e:
        reader = ReadCAMS2_82(data_dir=tmp_path, data_id="IFS")
        reader.daterange = ("2025-07-01", "2025-07-01")
        reader.read_var("ec1064aer", "3hourly")
        assert e == "No files found"


def test_ReadCAMS2_82_no_data_dir():
    with pytest.raises(AttributeError) as e:
        reader = ReadCAMS2_82(data_id="IFS")
        reader.daterange = ("2025-07-01", "2025-07-01")
        reader.read_var("ec1064aer", "3hourly")
        assert "data_dir needs to be set before accessing" in e


def test_check_files(
    dummy_model_path, dummy_model_path_too_few_times, dummy_model_path_duplicates, caplog
):
    result = check_files(dummy_model_path.parent.glob("*.nc"))
    assert (
        f"Ambiguous time dimension: Duplicate timestamps in {str(dummy_model_path_duplicates)}. Skipping file"
        in caplog.text
    )
    assert (
        f"Too few timestamps in {str(dummy_model_path_too_few_times)}. Skipping file"
        in caplog.text
    )
    assert len(result) == 1
