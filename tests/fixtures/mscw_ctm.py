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
    """dictionary contining EMEP test data"""
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

    tbase = TsType(tst).cf_base_unit

    _lats_fake = np.linspace(30, 82, 10)
    _lons_fake = np.linspace(-25, 90, 15)

    start = datetime.strptime(f"{year}-01-01", "%Y-%m-%d")
    stop = datetime.strptime(f"{year}-12-31", "%Y-%m-%d")
    _time_fake = pd.date_range(start, stop, freq=TsType(tst).to_pandas_freq())
    # _time_fake = np.arange(10)
    timeattrs = {"units": f"{tbase} since 2000-01-01", "calendar": "gregorian"}
    sh = (len(_time_fake), len(_lats_fake), len(_lons_fake))
    _data_fake = numval * np.ones(sh)

    # coords = {"time": ("time", _time_fake, timeattrs), "lat": _lats_fake, "lon": _lons_fake}
    coords = {"time": _time_fake, "lat": _lats_fake, "lon": _lons_fake}

    dims = ["time", "lat", "lon"]

    arr = xr.DataArray(data=_data_fake, coords=coords, dims=dims)
    arr.time.encoding["units"] = "hours since 1900-01-01 00:00:00"
    arr.time.encoding["calendar"] = "gregorian"
    arr.time.encoding["standard_name"] = "time"

    return arr
