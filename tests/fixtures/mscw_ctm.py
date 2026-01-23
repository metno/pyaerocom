from __future__ import annotations

from datetime import datetime

import numpy as np
import pandas as pd
import pytest
import xarray as xr

from .data_access import TEST_DATA

EMEP_DATA_PATH = TEST_DATA["MODELS"].path / "EMEP_2017"


@pytest.fixture(scope="session")
def path_emep() -> dict[str, str]:
    """dictionary containing EMEP test data"""
    paths = dict(
        daily=EMEP_DATA_PATH / "Base_day.nc",
        monthly=EMEP_DATA_PATH / "Base_month.nc",
        yearly=EMEP_DATA_PATH / "Base_fullrun.nc",
        data_dir=EMEP_DATA_PATH,
    )

    return {key: str(path) for key, path in paths.items()}


def create_fake_MSCWCtm_data(year="2019", numval=1, tst=None):
    if tst is None:
        tst = "monthly"
    from pyaerocom import TsType

    _lats_fake = np.linspace(30, 82, 10)
    _lons_fake = np.linspace(-25, 90, 15)

    start = datetime.strptime(f"{year}-01-01", "%Y-%m-%d")
    stop = datetime.strptime(f"{year}-12-31", "%Y-%m-%d")
    _time_fake = pd.date_range(start, stop, freq=TsType(tst).to_pandas_freq())
    sh = (len(_time_fake), len(_lats_fake), len(_lons_fake))
    _data_fake = numval * np.ones(sh)

    coords = {"time": _time_fake, "latitude": _lats_fake, "longitude": _lons_fake}

    dims = ["time", "latitude", "longitude"]

    arr = xr.DataArray(data=_data_fake, coords=coords, dims=dims)
    arr.time.encoding["units"] = "hours since 1900-01-01 00:00:00"
    arr.time.encoding["calendar"] = "gregorian"
    arr.time.encoding["standard_name"] = "time"

    return arr


@pytest.fixture
def fake_aod_MSCWCtm_data_monthly_2010(tmp_path) -> str:
    path = tmp_path / "EMEP_fake" / "2010"

    if not path.exists():
        path.mkdir(parents=True)
    data = create_fake_MSCWCtm_data(year=2010, numval=1)

    var_name = "AOD_550nm"
    units = "1"
    ds = xr.Dataset()

    ds[var_name] = data
    ds[var_name].attrs.update(units=units, var_name=var_name)

    ds.to_netcdf(path=path / "Base_month.nc")

    return str(path)
