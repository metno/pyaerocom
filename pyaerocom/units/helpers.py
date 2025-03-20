import numpy as np
from pyaerocom.exceptions import TemporalResolutionError
from pyaerocom.units.datetime import TsType

from pyaerocom.units.datetime.utils import to_pandas_timestamp
from .constants import SECONDS_IN_DAY
from pyaerocom import const

import calendar


def seconds_in_periods(timestamps, ts_type):
    """
    Calculates the number of seconds for each period in timestamps.

    Parameters
    ----------
    timestamps : numpy.datetime64 or numpy.ndarray
        Either a single datetime or an array of datetimes.
    ts_type : str
        Frequency of timestamps.

    Returns
    -------
    np.array :
        Array with same length as timestamps containing number of seconds for
        each period.
    """

    ts_type = TsType(ts_type)
    if isinstance(timestamps, np.datetime64):
        timestamps = np.array([timestamps])
    if isinstance(timestamps, np.ndarray):
        timestamps = [to_pandas_timestamp(timestamp) for timestamp in timestamps]
    # From here on timestamps should be a numpy array containing pandas Timestamps
    if ts_type >= TsType("monthly"):
        if ts_type == TsType("monthly"):
            days_in_months = np.array([timestamp.days_in_month for timestamp in timestamps])
            seconds = days_in_months * SECONDS_IN_DAY
            return seconds
        if ts_type == TsType("daily"):
            return SECONDS_IN_DAY * np.ones_like(timestamps)
        raise NotImplementedError("Only yearly, monthly and daily frequencies implemented.")

    if ts_type == TsType("yearly"):
        days_in_year = [365 + calendar.isleap(ts.year) for ts in timestamps]
        seconds = np.array(days_in_year) * SECONDS_IN_DAY
        return seconds

    raise TemporalResolutionError(f"Unknown TsType: {ts_type}")


def get_standard_unit(var_name: str) -> str:
    """Gets standard unit of AeroCom variable

    Also handles alias names for variables, etc. or strings corresponding to
    older conventions (e.g. names containing 3D).

    Parameters
    ----------
    var_name : str
        AeroCom variable name

    Returns
    -------
    str
        corresponding standard unit
    """
    return const.VARS[var_name].units
