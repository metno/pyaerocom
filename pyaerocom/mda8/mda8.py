import numpy as np
import xarray as xr

from pyaerocom.colocation.colocated_data import ColocatedData
from pyaerocom.colocation.colocation_3d import ColocatedDataLists


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


def mda8_colocated_data(
    coldat: ColocatedData | ColocatedDataLists, /, obs_var: str, mod_var: str
) -> ColocatedData | ColocatedDataLists:
    """Applies the mda8 calculation to a colocated data object,
    returning the new colocated data object.

    :param data: The colocated data object.
    :return: Colocated data object containing
    """
    if not isinstance(coldat, ColocatedDataLists | ColocatedData):
        raise ValueError(
            f"Unexpected type {type(coldat)}. Expected ColocatedData or ColocatedDataLists"
        )

    if isinstance(coldat, ColocatedData):
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

    colocateddata_for_statistics = []
    colocateddata_for_profile_viz = []
    for cd in coldat.colocateddata_for_statistics:
        colocateddata_for_statistics.append(
            mda8_colocated_data(cd, obs_var=obs_var, mod_var=mod_var)
        )
    for cd in coldat.colocateddata_for_profile_viz:
        colocateddata_for_profile_viz.append(
            mda8_colocated_data(cd, obs_var=obs_var, mod_var=mod_var)
        )

    return ColocatedDataLists(colocateddata_for_statistics, colocateddata_for_profile_viz)


def _calc_mda8(data: xr.DataArray) -> xr.DataArray:
    """Calculates the daily max 8h average for an array:

    :param data: The DataArray for which to calculate the mda8. Input
    should be a DataArray with dimensions ["data_source", "time", "station_name"]
    (ie. the format of ColocatedData.data) representing hourly data.
    :return: Equivalently structured DataArray, resampled along the "time"
    dimension.
    """
    ravg = data.rolling(time=8, min_periods=6).mean()

    daily_max = ravg.resample(time="1D").reduce(
        lambda x, axis: np.apply_along_axis(min_periods_max, 1, x, min_periods=16)
    )

    daily_max.attrs["ts_type"] = "daily"

    return daily_max
