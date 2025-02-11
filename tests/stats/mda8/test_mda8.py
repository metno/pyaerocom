import numpy as np
import pytest
import xarray as xr

from pyaerocom.colocation.colocated_data import ColocatedData
from pyaerocom.stats.mda8.mda8 import (
    _calc_mda8,
    _daily_max,
    _rolling_average_8hr,
    mda8_colocated_data,
)


@pytest.fixture
def test_data(time, values) -> xr.DataArray:
    return xr.DataArray(
        [[[x] for x in values]],
        dims=["data_source", "time", "station_name"],
        coords={"time": time},
    )


@pytest.mark.parametrize(
    "time,values,exp_mda8",
    (
        pytest.param(
            xr.date_range(start="2024-01-01 01:00", periods=49, freq="1h"),
            [0.0] * 49,
            [0, 0, np.nan],
            id="zeros",
        ),
        pytest.param(
            xr.date_range(start="2024-01-01 01:00", periods=49, freq="1h"),
            np.linspace(start=1, stop=49, num=49),
            [20.5, 44.5, np.nan],
            id="incrementing-by-1",
        ),
        pytest.param(
            xr.date_range(start="2024-01-01 13:00:00", periods=49, freq="1h"),
            np.concatenate(  # Sequence 1-7, 3x nan, 11-14, 3x nan, 28-49
                (
                    np.arange(start=1, stop=8),
                    [np.nan] * 3,
                    np.arange(start=11, stop=25),
                    [np.nan] * 3,
                    np.arange(start=28, stop=50),
                )
            ),
            [np.nan] * 3,
            id="with-nans",
        ),
        # https://github.com/metno/pyaerocom/issues/1323
        pytest.param(
            xr.date_range(start="2024-01-01 06:00:00", periods=30, freq="1h"),
            np.arange(30, dtype=float),
            [np.nan, np.nan],
            id="#1323",
        ),
    ),
)
def test_calc_mda8(test_data, exp_mda8):
    mda8 = _calc_mda8(test_data)

    assert mda8.shape[1] == len(exp_mda8)

    assert all(mda8[0, :, 0] == pytest.approx(exp_mda8, abs=0, nan_ok=True))


def test_calc_mda8_with_gap():
    arr1 = xr.DataArray(
        [[[x] for x in np.linspace(start=1, stop=50, num=50)]],
        dims=["data_source", "time", "station_name"],
        coords={"time": xr.date_range(start="2024-01-01 01:00", periods=50, freq="1h")},
    )

    arr2 = xr.DataArray(
        [[[x] for x in np.linspace(start=1, stop=50, num=50)]],
        dims=["data_source", "time", "station_name"],
        coords={"time": xr.date_range(start="2024-01-04 01:00", periods=50, freq="1h")},
    )

    arr = xr.concat((arr1, arr2), dim="time")

    mda8 = _calc_mda8(arr)

    assert mda8.shape == (1, 6, 1)
    pytest.approx(mda8[0, :, 0], [20.5, 44.5, np.nan, 41.25, 44.5, np.nan], abs=10 * 10**-5)


@pytest.mark.parametrize("coldataset", ("fake_3d_hr",))
def test_coldata_to_mda8(coldata):
    mda8 = mda8_colocated_data(coldata, obs_var="vmro3mda8", mod_var="vmro3mda8")

    assert isinstance(mda8, ColocatedData)
    assert mda8.metadata["ts_type"] == "daily"
    assert mda8.metadata["var_name"] == ["vmro3mda8", "vmro3mda8"]
    assert mda8.shape == (2, 8, 1)

    assert mda8.data.values[0, :, 0] == pytest.approx(
        [np.nan, np.nan, 1.18741556, 1.18777241, 1.18869106, 1.18879322, 1.18807846, 1.18700801],
        abs=10**-5,
        nan_ok=True,
    )

    assert mda8.data.values[1, :, 0] == pytest.approx(
        [
            1.57327333,
            1.28884431,
            1.28741556,
            1.28777241,
            1.28869106,
            1.28879322,
            1.28807846,
            1.28700801,
        ],
        abs=10**-5,
        nan_ok=True,
    )


@pytest.mark.parametrize(
    "time,values,exp_ravg",
    (
        (
            xr.date_range(start="2024-01-01 01:00", periods=48, freq="1h"),
            [0.0, 1, 2, 3, 4, 5, 6, 7] * 6,
            [np.nan] * 5 + [2.5, 3] + [3.5] * 41,
        ),
        (
            xr.date_range(start="2024-01-01 01:00", periods=24, freq="1h"),
            [np.nan, 1, 2, 3, 4, 5, 6, 7] * 3,
            [np.nan] * 6 + [3.5] + [4] * 17,
        ),
        (
            xr.date_range(start="2024-01-01 01:00", periods=24, freq="1h"),
            [np.nan, np.nan, 2, 3, 4, 5, 6, 7] * 3,
            [np.nan] * 7 + [4.5] * 17,
        ),
        (
            xr.date_range(start="2024-01-01 01:00", periods=24, freq="1h"),
            [np.nan, np.nan, np.nan, 3, 4, 5, 6, 7] * 3,
            [np.nan] * 24,
        ),
    ),
)
def test_rollingaverage(test_data, exp_ravg):
    """
    Test of rolling average calculation
    """
    ravg = _rolling_average_8hr(test_data)

    assert all(ravg[0, :, 0] == pytest.approx(exp_ravg, abs=0, nan_ok=True))


def test_rollingaverage_label():
    """
    Checks that the labels of rolling average is correct (we want it to be labeled based
    on the "right-most" interval, ie. latest measurement in the interval). This is currently
    the case in xarray but not greatly documented, so this test checks for that.

    https://github.com/metno/pyaerocom/issues/1323
    """
    data = xr.DataArray(
        [[[float(x)] for x in range(24)]],
        dims=["data_source", "time", "station_name"],
        coords={"time": xr.date_range(start="2024-01-01 00:00", periods=24, freq="1h")},
    )

    ravg = _rolling_average_8hr(data)

    assert ravg["time"].isel(time=0) == np.datetime64("2024-01-01 00:00")
    assert ravg["time"].isel(time=23) == np.datetime64("2024-01-01 23:00")


@pytest.mark.parametrize(
    "time,values,exp_daily_max",
    (
        (
            xr.date_range(start="2024-01-01 01:00", periods=48, freq="1h"),
            np.linspace(1, 48, num=48),
            [24, 48],
        ),
        (
            xr.date_range(start="2024-01-01 01:00", periods=24, freq="1h"),
            [np.nan] * 6 + list(range(7, 25)),
            [24],
        ),
        (
            xr.date_range(start="2024-01-01 01:00", periods=24, freq="1h"),
            [np.nan] * 7 + list(range(8, 25)),
            [np.nan],
        ),
    ),
)
def test_daily_max(test_data, exp_daily_max):
    """
    Tests the daily max calculation. Note that "the first calculation period
    for any one day will be the period from 17:00 on the previous day to 01:00
    on that day; the last calculation period for any one day will be the period
    from 16:00 to 24:00 on that day
    """
    dmax = _daily_max(test_data)

    assert all(dmax[0, :, 0] == pytest.approx(exp_daily_max, abs=0, nan_ok=True))
