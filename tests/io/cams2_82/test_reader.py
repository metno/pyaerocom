import numpy as np
import pandas as pd
import pytest
import xarray as xr

from pyaerocom.io.cams2_82.reader import (
    AEROCOM_NAMES,
    UNITS,
    drop_vars,
    only_first_day,
    read_dataset,
)

times3h = pd.date_range(start="2025-07-01", freq="3h", periods=12)
levels = np.arange(64, 138)
latitudes = np.arange(90.0, -90.5, -0.5)
longitudes = np.arange(0.0, 360.0, 0.5)


@pytest.fixture()
def dummy_model_data():
    return xr.Dataset(
        {
            "aerext1064": xr.DataArray(
                data=np.ones(shape=(len(times3h), len(levels), len(latitudes), len(longitudes))),
                dims=["time", "level", "latitude", "longitude"],
                coords={
                    "time": times3h,
                    "level": levels,
                    "latitude": latitudes,
                    "longitude": longitudes,
                },
                attrs={"units": "m**-1"},
            ),
            "aerext532": xr.DataArray(
                data=np.ones(shape=(len(times3h), len(levels), len(latitudes), len(longitudes))),
                dims=["time", "level", "latitude", "longitude"],
                coords={
                    "time": times3h,
                    "level": levels,
                    "latitude": latitudes,
                    "longitude": longitudes,
                },
                attrs={"units": "m**-1"},
            ),
        }
    )


def test_drop_vars(dummy_model_data):
    assert "aerext532" in dummy_model_data.data_vars
    ds = drop_vars(dummy_model_data)
    assert "aerext532" not in ds.data_vars


def test_only_first_day(dummy_model_data):
    assert len(dummy_model_data.time) == 12
    ds = only_first_day(dummy_model_data)
    assert len(ds.time) == 8


def test_read_dataset(tmp_path, dummy_model_data):
    path = tmp_path / "dummy_model_data.nc"
    dummy_model_data.to_netcdf(path)
    ds = read_dataset([path])
    assert "altitude" in ds.dims
    assert len(ds.altitude) == len(levels)
    assert set(list(AEROCOM_NAMES.values())) == set(list(ds.keys()))
    for var in ds.data_vars:
        assert (
            ds[var].units
            == UNITS[list(AEROCOM_NAMES.keys())[list(AEROCOM_NAMES.values()).index(var)]]
        )
