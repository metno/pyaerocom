import logging

import numpy as np
import pandas as pd
import xarray as xr

from pyaerocom.colocation.colocated_data import ColocatedData

logger = logging.getLogger(__name__)


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


def _generate_colocated_data(
    calc_func: callable, coldat: ColocatedData, obs_var: str, mod_var: str
) -> ColocatedData:
    """Helper function to generate colocated data for a given calculation function (e.g. mda8 or somo30) and variable names."""
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

    cd = ColocatedData(calc_func(coldat.data))
    cd.data.attrs["var_name"] = [obs_var, mod_var]
    cd.metadata["var_name_input"] = [obs_var, mod_var]

    return cd


def mda8_colocated_data(coldat: ColocatedData, /, obs_var: str, mod_var: str) -> ColocatedData:
    """Applies the mda8 calculation to a colocated data object,
    returning the new colocated data object.

    :param data: The colocated data object.
    :return: Colocated data object containing
    """
    return _generate_colocated_data(calc_mda8, coldat, obs_var, mod_var)


def calc_mda8(data: xr.DataArray) -> xr.DataArray:
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

    Note:
    -----
    Calculated values will only be returned for days which have at least one datapoint
    in the input dataarray to ensure that the ts does not expand.

    See also:
    ---------
    https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32008L0050#ntc3-L_2008152EN.01003001-E0003 (Annex XI)
    """
    mda8 = _daily_max(_rolling_average_8hr(data))

    mda8.attrs["ts_type"] = "daily"

    if "data_source" not in mda8.dims:
        # skip time-shift and filtering, too expensive
        return mda8

    # Ensure time dimension represents the midpoint of the interval.
    mda8.coords.update({"time": mda8.get_index("time") + pd.tseries.frequencies.to_offset("12h")})

    # Keep only values for days that existed in the original time series.
    mda8 = mda8.sel(
        time=np.isin(mda8.coords["time.date"].values, np.unique(data.coords["time.date"].values))
    )

    return mda8


def _rolling_average_8hr(arr: xr.DataArray) -> xr.DataArray:
    # Xarray labels the data right based on the last data point in the period for rolling.
    return arr.rolling(time=8, center=False, min_periods=6).mean()


def _daily_max(arr: xr.DataArray) -> xr.DataArray:
    if "data_source" in arr.dims:
        # colocated data object has time-axis at axis 1
        t_axis = 1
    else:
        # usual data has time-axis at axis 0
        t_axis = 0

    return arr.resample(time="24h", origin="start_day", label="left", offset="1h").reduce(
        lambda x, axis: np.apply_along_axis(min_periods_max, t_axis, x, min_periods=18)
    )


def min_periods_sum_over_threshold(x: np.ndarray, /, threshold: float, min_periods=1) -> float:
    """Calculates the sum of values above a threshold in a 1-dimensional array, returning
    nan if not a minimum count of valid values exist."""
    if x.ndim != 1:
        raise ValueError(f"Unexpected number of dimensions. Got {x.ndim}, expected 1.")

    length = np.sum(~np.isnan(x))
    if length < min_periods:
        return np.nan

    x -= threshold
    x.where(x <= 0, 0, inplace=True)
    return np.nansum(x)


def _yearly_sum_over_threshold(arr: xr.DataArray, threshold: float) -> xr.DataArray:
    if "data_source" in arr.dims:
        # colocated data object has time-axis at axis 1
        t_axis = 1
    else:
        # usual data has time-axis at axis 0
        t_axis = 0
    return arr.resample(time="365D", origin="start_year", label="left").reduce(
        lambda x, axis: np.apply_along_axis(
            min_periods_sum_over_threshold, t_axis, x, threshold=threshold, min_periods=273
        )
    )


def calc_somo30(data: xr.DataArray) -> xr.DataArray:
    """Calculates the yearly SOMO30 value from an hourly array:

    :param data: The DataArray for which to calculate the SOMO30. Input
    should be a DataArray with dimensions ["data_source", "time", "station_name"]
    (ie. the format of ColocatedData.data) representing hourly data.
    :return: Equivalently structured DataArray, resampled along the "time"
    dimension.

    Note:
    -----
    The calculation for SOMO30 is defined as follows:
    > Eight hours values:         75 % of values (i.e. 6 hours)

    > Maximum daily 8-hour mean:  75 % of the hourly running eight hour
                             averages (i.e. 18 eight hour averages per
                             day)

    > Maximum yearly SOMO30:      75 % of the daily max 8-hour means (-30ppb) (i.e. 273 daily values)

    > The maximum daily eight hour mean concentration will be selected by examining
    > eight hour running averages, calculated from hourly data and updated each hour.
    > Each eight hour average so calculated will be assigned to the day on which it
    > ends i.e. the first calculation period for any one day will be the period from
    > 17:00 on the previous day to 01:00 on that day; the last calculation period for
    > any one day will be the period from 16:00 to 24:00 on that day.

    Note:
    -----
    Calculated values will only be returned for days which have at least one datapoint
    in the input dataarray to ensure that the ts does not expand.

    See also:
    ---------
    https://www.emep.int/mscw/definitions.pdf (SOMO35)
    """
    mda8 = calc_mda8(data)

    somo30 = _yearly_sum_over_threshold(mda8, threshold=30)

    somo30.attrs["ts_type"] = "yearly"

    if "data_source" not in somo30.dims:
        # skip time-shift and filtering, too expensive
        return somo30

    # Ensure time dimension represents the midpoint of the interval.
    somo30.coords.update(
        {"time": somo30.get_index("time") + pd.tseries.frequencies.to_offset("182D")}
    )

    # Keep only values for days that existed in the original time series.
    somo30 = somo30.sel(
        time=np.isin(somo30.coords["time.date"].values, np.unique(data.coords["time.date"].values))
    )

    return somo30


def somo30_colocated_data(coldat: ColocatedData, /, obs_var: str, mod_var: str) -> ColocatedData:
    """Applies the SOMO30 calculation to a colocated data object,
    returning the new colocated data object.

    :param data: The colocated data object.
    :return: Colocated data object containing
    """
    return _generate_colocated_data(calc_somo30, coldat, obs_var, mod_var)
