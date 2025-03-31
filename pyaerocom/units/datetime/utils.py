# Mypy errors because it doesn't understand the total_ordering
# decorator used for TsType. This suppresses that error:
# mypy: disable-error-code=operator

import calendar
from collections import Counter

from cf_units import Unit
import iris
from pyaerocom._warnings import ignore_warnings
from pyaerocom.exceptions import TemporalResolutionError
from . import TsType
from ..constants import SECONDS_IN_DAY
from .time_config import (
    GREGORIAN_BASE,
    TS_TYPE_SECS,
    microsec_units,
    millisec_units,
    sec_units,
    min_units,
    hr_units,
    day_units,
    TS_TYPE_DATETIME_CONV,
)
import pandas as pd
import numpy as np
from datetime import datetime, date
from datetime import MINYEAR

import logging


logger = logging.getLogger(__name__)


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


def is_year(val) -> bool:
    """Check if input is / may be year

    Parameters
    ----------
    val
        input that is supposed to be checked

    Returns
    -------
    bool
        True if input is a number between -2000 and 10000, else False
    """
    try:
        if -2000 < int(val) < 10000:
            return True
    except ValueError:
        pass

    return False


def get_tot_number_of_seconds(ts_type: str, dtime: pd.Series | None = None):
    """Get total no. of seconds for a given frequency

    ToDo
    ----
    This method needs revision and can be solved simpler probably

    Parameters
    ----------
    ts_type : str or TsType
        frequency for which number of seconds is supposed to be retrieved
    dtime : TYPE, optional
        DESCRIPTION. The default is None.

    Raises
    ------
    AttributeError
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """

    ts_tpe = TsType(ts_type)

    if ts_tpe >= TsType("monthly"):
        if dtime is None:
            raise AttributeError(
                "For frequencies larger than or eq. monthly you"
                + " need to provide dtime in order to compute the number of second."
            )
        if not ts_type == "monthly":
            raise NotImplementedError("Can only handle monthly so far...")

        # find seconds from dtime
        # TODO generalize this
        days_in_month = dtime.dt.daysinmonth

        return days_in_month * SECONDS_IN_DAY

    return TS_TYPE_SECS[ts_type]


def to_datetime64(value):
    """Convert input value to numpy.datetime64

    Parameters
    ----------
    value
        input value that is supposed to be converted, needs to be either str,
        datetime.datetime, pandas.Timestamp or an integer specifying the
        desired year.

    Returns
    -------
    datetime64
        input timestamp converted to datetime64
    """
    if isinstance(value, np.datetime64):
        return value

    try:
        return to_pandas_timestamp(value).to_datetime64()
    except Exception as e:
        raise ValueError(f"Failed to convert {value} to datetime64 objectError: {repr(e)}")


def cftime_to_datetime64(times, cfunit=None, calendar=None):
    """Convert numerical timestamps with epoch to numpy datetime64

    This method was designed to enhance the performance of datetime conversions
    and is based on the corresponding information provided in the cftime
    package (`see here <https://github.com/Unidata/cftime/blob/master/cftime/
    _cftime.pyx>`__). Particularly, this object does, what the :func:`num2date`
    therein does, but faster, in case the time stamps are not defined on a non
    standard calendar.

    Parameters
    ----------
    times : :obj:`list` or :obj:`ndarray` or :obj:`iris.coords.DimCoord`
        array containing numerical time stamps (relative to basedate of
        ``cfunit``). Can also be a single number.
    cfunit : :obj:`str` or :obj:`Unit`, optional
        CF unit string (e.g. day since 2018-01-01 00:00:00.00000000 UTC) or
        unit. Required if `times` is not an instance of
        :class:`iris.coords.DimCoord`
    calendar : :obj:`str`, optional
        string specifying calendar (only required if ``cfunit`` is of type
        ``str``).

    Returns
    -------
    ndarray
        numpy array containing timestamps as datetime64 objects

    Raises
    ------
    ValueError
        if cfunit is ``str`` and calendar is not provided or invalid, or if
        the cfunit string is invalid

    Example
    -------

    >>> cfunit_str = 'day since 2018-01-01 00:00:00.00000000 UTC'
    >>> cftime_to_datetime64(10, cfunit_str, "gregorian")
    array(['2018-01-11T00:00:00.000000'], dtype='datetime64[us]')
    """
    if isinstance(times, iris.coords.DimCoord):  # special case
        times, cfunit = times.points, times.units
    try:
        len(times)
    except Exception:
        times = [times]
    if isinstance(cfunit, str):
        if calendar is None:
            raise ValueError(
                "Require specification of calendar for conversion into datetime64 objects"
            )
        cfunit = Unit(cfunit, calendar)  # raises Error if calendar is invalid
    if not isinstance(cfunit, Unit):
        raise ValueError(
            "Please provide cfunit either as instance of class cf_units.Unit or as a string"
        )
    calendar = cfunit.calendar
    basedate = cfunit.num2date(0)
    if (calendar == "proleptic_gregorian" and basedate.year >= MINYEAR) or (
        calendar in ["gregorian", "standard"] and basedate > GREGORIAN_BASE
    ):
        cfu_str = cfunit.origin

        res = cfu_str.split()[0].lower()
        if res in microsec_units:
            tstr = "us"
        elif res in millisec_units:
            tstr = "ms"
        elif res in sec_units:
            tstr = "s"
        elif res in min_units:
            tstr = "m"
        elif res in hr_units:
            tstr = "h"
        elif res in day_units:
            tstr = "D"
        else:
            raise ValueError("unsupported time units")

        basedate = np.datetime64(basedate)
        dt = np.asarray(np.asarray(times), dtype=f"timedelta64[{tstr}]")
        return basedate + dt
    else:
        return np.asarray([np.datetime64(t) for t in cfunit.num2date(times)])


@ignore_warnings(UserWarning, r"Parsing .* in DD/MM/YYYY format")
def to_pandas_timestamp(value):
    """Convert input to instance of :class:`pandas.Timestamp`

    Parameters
    ----------
    value
        input value that is supposed to be converted to time stamp

    Returns
    --------
    pandas.Timestamp
    """
    if isinstance(value, np.str_):
        value = str(value)
    if isinstance(value, pd.Timestamp):
        return value
    if isinstance(value, str | np.datetime64 | datetime | date):
        return pd.Timestamp(value)

    try:
        numval = int(value)
        if not 0 <= numval <= 10000:
            raise ValueError("Could not infer valid year from numerical time input")
        return pd.Timestamp(str(numval))
    except Exception as e:
        raise ValueError(f"Failed to convert {value} to Timestamp: {repr(e)}")


def infer_time_resolution(time_stamps, dt_tol_percent=5, minfrac_most_common=0.8) -> TsType:
    """Infer time resolution based on input time-stamps

    Calculates time difference *dt* between consecutive timestamps provided via
    input array or list. Then it counts the most common *dt* (e.g. 86400 s for
    daily). Before inferring the frequency it then checks all other *dts*
    occurring in the input array to see if they are within a certain interval
    around the most common one (e.g. +/- 5% as default, via arg
    `dt_tol_percent`), that is, 86390 would be included if most common dt is
    86400 s but not 80000s. Then it checks if the number of *dts* that
    are within that tolerance level around the most common *dt* exceed a
    certain fraction (arg `minfrac_most_common`) of the total number of *dts*
    that occur in the input array (default is 80%). If that is the case, the
    most common frequency is attempted to be derived using
    :func:`TsType.from_total_seconds` based on the most common *dt* (in this
    example that would be *daily*).


    Parameters
    ----------
    time_stamps : pandas.DatetimeIndex, or similar
        list of time stamps
    dt_tol_percent : int
        tolerance in percent of accepted range of time diffs with respect to
        most common time difference.
    minfrac_most_common : float
        minimum required fraction of time diffs that have to be equal to, or
        within tolerance range, the most common time difference.


    Raises
    ------
    TemporalResolutionError
        if frequency cannot be derived.

    Returns
    -------
    str
        inferred frequency
    """
    if not isinstance(time_stamps, pd.DatetimeIndex):
        time_stamps = pd.DatetimeIndex(time_stamps)
    vals = time_stamps.values

    dts = (vals[1:] - vals[:-1]).astype("timedelta64[s]").astype(int)

    if np.min(dts) < 0:
        raise TemporalResolutionError("Nasa Ames file contains neg. meas periods...")

    counts = Counter(dts).most_common()
    most_common_dt, most_common_num = counts[0]
    num_within_tol = most_common_num
    lower = most_common_dt * (100 - dt_tol_percent) / 100
    upper = most_common_dt * (100 + dt_tol_percent) / 100
    for dt, num in counts[1:]:
        if lower <= dt <= upper:
            num_within_tol += num
    frac_ok = num_within_tol / len(dts)
    if not frac_ok > minfrac_most_common:
        raise TemporalResolutionError("Failed to infer ts_type")
    tst = TsType.from_total_seconds(most_common_dt)
    return tst


def test_cftime_to_datetime64():
    pass


def datetime2str(time, ts_type=None):
    conv = TS_TYPE_DATETIME_CONV[ts_type]
    if is_year(time):
        return str(time)
    try:
        time = to_pandas_timestamp(time).strftime(conv)
    except pd.errors.OutOfBoundsDatetime:
        logger.warning(f"Failed to convert time {time} to string")
    return time
