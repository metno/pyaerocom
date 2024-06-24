import numpy as np
import xarray as xr


def calc_mda8(data: xr.DataArray) -> xr.DataArray:
    """Calculates the daily max 8h average for an array:

    :param data: The DataArray for which to calculate the mda8. Input
    should be a DataArray with dimensions ["data_source", "time", "station_name"]
    (ie. the format of ColocatedData.data) representing hourly data.
    :return: Equivalently structured DataArray, resampled along the "time"
    dimension.
    """

    def min_periods_max(x: np.ndarray, /, min_periods=1) -> float:
        """Calculates the max of a 1-dimensional array, returning
        nan if not a minimum set of valid values exist.

        :param x: 1-dimensional ndarray.
        :param min_periods: minimum required non-nan values, defaults to 1
        :return: A single value, which is either nan or a float.
        """
        if not x.ndim == 1:
            raise ValueError(f"Unexpected number of dimensions. Got {x.ndim}, expected 1.")

        mask = ~np.isnan(x)
        length = np.sum(mask)
        if length >= min_periods:
            mx = np.nanmax(x)
            return mx

        else:
            return np.nan

    # TODO: This function should check some underlying assumptions such as the dimensions,
    # that the data represents hourly data and so on.

    ravg = data.rolling(time=8, min_periods=6).mean()

    daily_max = ravg.resample(time="1D").reduce(
        lambda x, axis: np.apply_along_axis(min_periods_max, 1, x, min_periods=16)
    )

    return daily_max
