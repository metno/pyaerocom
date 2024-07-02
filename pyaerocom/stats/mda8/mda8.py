import numpy as np
import xarray as xr

from pyaerocom.colocation.colocated_data import ColocatedData


def min_periods_max(x: np.ndarray, /, min_periods=1) -> float:
    """Calculates the max of a 1-dimensional array, returning
    nan if not a minimum count of valid values exist.

    :param x: 1-dimensional ndarray.
    :param min_periods: minimum required non-nan values, defaults to 1
    :return: A single value, which is either nan or a float.
    """
    if x.ndim != 1:
        raise ValueError(f"Unexpected number of dimensions. Got {x.ndim}, expected 1.")

    length = np.sum(~np.isnan(x))
    if length < min_periods:
        return np.nan

    return np.nanmax(x)


def mda8_colocated_data(coldat: ColocatedData, /, obs_var: str, mod_var: str) -> ColocatedData:
    """Applies the mda8 calculation to a colocated data object,
    returning the new colocated data object.

    :param data: The colocated data object.
    :return: Colocated data object containing
    """
    if not isinstance(coldat, ColocatedData):
        raise ValueError(f"Unexpected type {type(coldat)}. Expected ColocatedData")

    if coldat.ts_type != "hourly":
        raise ValueError(f"Expected hourly timeseries. Got {coldat.ts_type}.")

    # TODO: Currently order of dims matter in the implementation, so this check is
    # stricter than it probably should be.
    if coldat.dims != ("data_source", "time", "station_name"):
        raise ValueError(
            f"Unexpected dimensions. Got {coldat.dims}, expected ['data_source', 'time', 'station_name']."
        )

    cd = ColocatedData(_calc_mda8(coldat.data))
    cd.data.attrs["var_name"] = [obs_var, mod_var]
    return cd


def _calc_mda8(data: xr.DataArray) -> xr.DataArray:
    """Calculates the daily max 8h average for an array:

    :param data: The DataArray for which to calculate the mda8. Input
    should be a DataArray with dimensions ["data_source", "time", "station_name"]
    (ie. the format of ColocatedData.data) representing hourly data.
    :return: Equivalently structured DataArray, resampled along the "time"
    dimension.

    Note:
    -----
    The calculation for mda8 is defined as follows:
    > Eight hours values:         75 % of values (i.e. 6 hours)

    > Maximum daily 8-hour mean:  75 % of the hourly running eight hour
                             averages (i.e. 18 eight hour averages per
                             day)

    > The maximum daily eight hour mean concentration will be selected by examining
    > eight hour running averages, calculated from hourly data and updated each hour.
    > Each eight hour average so calculated will be assigned to the day on which it
    > ends i.e. the first calculation period for any one day will be the period from
    > 17:00 on the previous day to 01:00 on that day; the last calculation period for
    > any one day will be the period from 16:00 to 24:00 on that day.
    """
    mda8 = _daily_max(_rolling_average_8hr(data))
    mda8.attrs["ts_type"] = "daily"
    return mda8


def _rolling_average_8hr(arr: xr.DataArray) -> xr.DataArray:
    return arr.rolling(time=8, min_periods=6).mean()


def _daily_max(arr: xr.DataArray) -> xr.DataArray:
    return arr.resample(time="24h", offset="1h").reduce(
        lambda x, axis: np.apply_along_axis(min_periods_max, 1, x, min_periods=18)
    )
