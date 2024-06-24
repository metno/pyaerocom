import numpy as np
import pytest
import xarray as xr

from pyaerocom.mda8.mda8 import calc_mda8


@pytest.mark.parametrize(
    "time,values,exp_length,exp_mda8",
    (
        pytest.param(
            xr.date_range(start="2024-01-01", periods=49, freq="1h"),
            [0] * 49,
            3,
            [0, 0, np.nan],
            id="zeros",
        ),
        pytest.param(
            xr.date_range(start="2024-01-01", periods=49, freq="1h"),
            np.linspace(start=1, stop=49, num=49),
            3,
            [20.5, 44.5, np.nan],
            id="incrementing-by-1",
        ),
        pytest.param(
            xr.date_range(start="2024-01-01 12:00:00", periods=49, freq="1h"),
            np.concatenate(  # Sequence 1-7, 3x nan, 11-14, 3x nan, 28-49
                (
                    np.arange(start=1, stop=8),
                    [np.nan] * 3,
                    np.arange(start=11, stop=25),
                    [np.nan] * 3,
                    np.arange(start=28, stop=50),
                )
            ),
            3,
            [np.nan] * 3,
        ),
    ),
)
def test_calc_mda8(time, values, exp_length, exp_mda8):
    arr = xr.DataArray(
        [[[x] for x in values]],
        dims=["data_source", "time", "station_name"],
        coords={"time": time},
    )

    mda8 = calc_mda8(arr)

    assert mda8.shape[1] == exp_length

    np.testing.assert_array_equal(mda8[0, :, 0], exp_mda8)
