import math
from math import nan

import numpy as np
import pytest
import xarray as xr

from pyaerocom.mda8.mda8 import calc_mda8


@pytest.fixture
def example_data() -> xr.DataArray:
    arr = xr.DataArray(
        [
            [
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
                [0],
            ],
        ],
        dims=["data_source", "time", "station_name"],
        coords={"time": xr.date_range(start="2024-01-01", end="2024-01-02", freq="1h")},
    )
    arr.attrs["ts_type"] = "hourly"
    return arr


def test_calc_mda8(example_data):
    mda8 = calc_mda8(example_data)

    assert mda8.shape == (1, 2, 1)
    assert mda8.values[0][0][0] == 0
    assert math.isnan(mda8.values[0][1][0])
