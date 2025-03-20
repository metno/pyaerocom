from collections import Counter
from pyaerocom._warnings import ignore_warnings
from pyaerocom.exceptions import TemporalResolutionError
from . import TsType
from ..constants import SECONDS_IN_DAY
from ._time_config import TS_TYPE_SECS
import pandas as pd
import numpy as np
from datetime import datetime, date


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
                "For frequncies larger than or eq. monthly you"
                + " need to provide dtime in order to compute the number of second."
            )
        if not ts_type == "monthly":
            raise NotImplementedError("Can only handle monthly so far...")

        # find seconds from dtime
        # TODO generalize this
        days_in_month = dtime.dt.daysinmonth

        return days_in_month * SECONDS_IN_DAY
    else:
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


def infer_time_resolution(time_stamps, dt_tol_percent=5, minfrac_most_common=0.8):
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
    from pyaerocom import TsType

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
    return str(tst)
