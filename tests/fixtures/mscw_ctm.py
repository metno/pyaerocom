from __future__ import annotations

import numpy as np
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


def create_fake_MSCWCtm_data(numval=1, tst=None):
    if tst is None:
        tst = "monthly"
    from pyaerocom import TsType

    tbase = TsType(tst).cf_base_unit

    _lats_fake = np.linspace(30, 82, 10)
    _lons_fake = np.linspace(-25, 90, 15)
    # _time_fake = pd.date_range('2019-01','2019-06', freq=pd_freq)
    _time_fake = np.arange(10)
    timeattrs = {"units": f"{tbase} since 2000-01-01", "calendar": "gregorian"}
    sh = (len(_time_fake), len(_lats_fake), len(_lons_fake))
    _data_fake = numval * np.ones(sh)

    coords = {"time": ("time", _time_fake, timeattrs), "lat": _lats_fake, "lon": _lons_fake}

    dims = ["time", "lat", "lon"]

    arr = xr.DataArray(data=_data_fake, coords=coords, dims=dims)

    return arr
