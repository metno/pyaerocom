"""
General helper methods for the pyaerocom library.
"""

# Mypy errors because it doesn't understand the total_ordering
# decorator used for TsType. This suppresses that error:
# mypy: disable-error-code=operator
from __future__ import annotations

import logging
import re
from typing import SupportsInt

import numpy as np

from pyaerocom.exceptions import TemporalResolutionError
from .time_config import (
    PANDAS_FREQ_TO_TS_TYPE,
    TS_TYPE_TO_NUMPY_FREQ,
    TS_TYPE_TO_PANDAS_FREQ,
    TS_TYPE_TO_SI,
    TS_TYPES,
)

from functools import total_ordering
from cf_units import Unit

logger = logging.getLogger(__name__)


@total_ordering
class TsType:
    VALID = TS_TYPES
    VALID_ITER = VALID[:-2]
    FROM_PANDAS = PANDAS_FREQ_TO_TS_TYPE
    TO_PANDAS = TS_TYPE_TO_PANDAS_FREQ
    TO_NUMPY = TS_TYPE_TO_NUMPY_FREQ
    TO_SI = TS_TYPE_TO_SI

    TS_MAX_VALS = {
        "minutely": 360,  # up to 6hourly
        "hourly": 168,  # up to weekly
        "daily": 180,  # up to 6 monthly
        "weekly": 104,  # up to ~2yearly
        "monthly": 120,
    }  # up to 10yearly

    # "monthly": "days" below is because each month does not have the same number of days
    # netcdf does time calculation for you given starting day and days past (CF convention)
    TSTR_TO_CF = {"hourly": "hours", "daily": "days", "monthly": "days"}

    TOL_SECS_PERCENT = 5

    def __init__(self, val) -> None:
        self._mulfac: int = 1
        self._val: str

        self.val = str(val)

    @property
    def mulfac(self) -> int:
        """Multiplication factor of frequency"""
        return self._mulfac

    @mulfac.setter
    def mulfac(self, value: SupportsInt):
        try:
            value = int(value)
        except Exception:
            raise ValueError("mulfac needs to be int or convertible to int")
        if self.base in self.TS_MAX_VALS and value > self.TS_MAX_VALS[self.base]:
            raise ValueError(
                f"Multiplication factor exceeds maximum allowed, which is "
                f"{self.TS_MAX_VALS[self.base]}"
            )
        self._mulfac = value

    @property
    def base(self) -> str:
        """Base string (without multiplication factor, cf :attr:`mulfac`)"""
        return self._val

    @property
    def val(self) -> str:
        """Value of frequency (string type), e.g. 3daily"""
        if self._mulfac != 1:
            return f"{self._mulfac}{self._val}"
        return self._val

    @val.setter
    def val(self, val: str):
        if val is None:
            raise TemporalResolutionError(
                "Invalid input, please provide valid frequency string..."
            )
        mulfac = 1
        if val[0].isdigit():
            ivalstr = re.findall(r"\d+", val)[0]
            val = val.split(ivalstr)[-1]
            mulfac = int(ivalstr)
        if val not in self.VALID:
            try:
                val = self._from_pandas(val)
            except TemporalResolutionError:
                raise TemporalResolutionError(
                    f"Invalid input for ts_type {val}. Choose from {self.VALID}"
                )
        if val in self.TS_MAX_VALS and mulfac != 1:
            if mulfac > self.TS_MAX_VALS[val]:
                raise TemporalResolutionError(
                    f"Invalid input for ts_type {val}. Multiplication factor "
                    f"{mulfac} exceeds maximum allowed for {val}, which is "
                    f"{self.TS_MAX_VALS[val]}"
                )
        self._val = val
        self._mulfac = mulfac

    @property
    def datetime64_str(self) -> str:
        """Convert ts_type str to datetime64 unit string"""
        return f"datetime64[{self.to_numpy_freq()}]"

    @property
    def timedelta64_str(self) -> str:
        """Convert ts_type str to datetime64 unit string"""
        return f"timedelta64[{self.to_numpy_freq()}]"

    @property
    def cf_base_unit(self) -> str:
        """Convert ts_type str to CF convention time unit"""
        if self.base not in self.TSTR_TO_CF:
            raise NotImplementedError(f"Cannot convert {self.base} to CF str")
        return self.TSTR_TO_CF[self.base]

    @property
    def num_secs(self) -> float:
        """Number of seconds in one period

        Note
        ----
        Be aware that for monthly frequency the number of seconds is not well
        defined!
        """
        cf = self.to_si()
        total_secs = 1 / Unit("s").convert(1, cf)
        return total_secs

    @property
    def tol_secs(self) -> int:
        """Tolerance in seconds for current TsType"""
        total_secs = self.num_secs
        frac = self.TOL_SECS_PERCENT / 100
        return int(np.ceil(frac * total_secs))

    def to_timedelta64(self) -> np.timedelta64:
        """
        Convert frequency to timedelta64 object

        Can be used, e.g. as tolerance when reindexing pandas Series

        Returns
        -------
        timedelta64

        """
        return np.timedelta64(1, self.to_numpy_freq())  # type: ignore

    @property
    def next_higher(self) -> TsType:
        """Next higher resolution code"""
        if self.mulfac > 1:
            return TsType(self._val)

        idx = self.VALID_ITER.index(self._val)
        if idx == 0:
            raise IndexError(f"No higher resolution available than {self}")
        return TsType(self.VALID_ITER[idx - 1])

    @property
    def next_lower(self) -> TsType:
        """Next lower resolution code

        This will go to the next lower base resolution, that is if current is
        3daily, it will return weekly, however, if current exceeds next lower
        base, it will iterate that base, that is, if current is 8daily, next
        lower will be 2weekly (and not 9daily).
        """
        idx = self.VALID_ITER.index(self._val)
        if idx == len(self.VALID_ITER) - 1:
            tst = TsType(self.base)
            tst.mulfac = self.mulfac + 1
            return tst
        tst = TsType(self.VALID_ITER[idx + 1])
        if self.mulfac == 1 or self.num_secs < tst.num_secs:
            return tst
        try:
            maxmul = self.TS_MAX_VALS[tst.base]
        except Exception:
            maxmul = 10
        numsecs = self.num_secs
        for mulfac in range(1, maxmul + 1):
            tst.mulfac = mulfac
            if numsecs < tst.num_secs:
                return tst
        raise TemporalResolutionError(f"Failed to determine next lower resolution for {self}")

    @staticmethod
    def valid(val) -> bool:
        try:
            TsType(val)
            return True
        except TemporalResolutionError:
            return False

    def to_numpy_freq(self) -> str:
        if self._val not in self.TO_NUMPY:
            raise TemporalResolutionError(f"numpy frequency not available for {self._val}")
        freq = self.TO_NUMPY[self._val]
        return f"{self.mulfac}{freq}"

    def to_pandas_freq(self) -> str:
        """Convert ts_type to pandas frequency string"""
        if self._val not in self.TO_PANDAS:
            raise TemporalResolutionError(f"pandas frequency not available for {self._val}")
        freq = self.TO_PANDAS[self._val]
        if self._mulfac == 1:
            return freq
        return f"{self._mulfac}{freq}"

    def to_si(self) -> str:
        """Convert to SI conform string (e.g. used for unit conversion)"""
        base = self.base
        if base not in self.TO_SI:
            raise ValueError(f"Cannot convert ts_type={self} to SI unit string...")
        si = self.TO_SI[base]
        return si if self.mulfac == 1 else f"({self.mulfac}{si})"

    def get_min_num_obs(self, to_ts_type: TsType, min_num_obs: dict) -> int:
        selfstr = self.val
        if to_ts_type >= self:  # should occur rarely
            if to_ts_type == self:
                return 0
            raise TemporalResolutionError(
                f"input ts_type {to_ts_type} is lower resolution than current {self}"
            )

        elif str(to_ts_type) in min_num_obs:
            # output frequency is specified in min_num_obs (note: this may
            # also be 3daily, etc, i.e., not restricted to base frequencies)
            mno = min_num_obs[str(to_ts_type)]
            if selfstr in mno:
                return int(mno[selfstr])
            elif self.mulfac != 1 and self.base in mno:
                min_num_base = mno[self.base]
                return int(np.round(min_num_base / self.mulfac))

        elif to_ts_type.base in min_num_obs:
            mno = min_num_obs[to_ts_type.base]
            if selfstr in mno:
                val = mno[selfstr]
                return int(np.round(to_ts_type.mulfac * val))

            elif self.mulfac != 1 and self.base in mno:
                min_num_base = mno[self.base]
                val = min_num_base / self.mulfac * to_ts_type.mulfac
                val = int(np.round(val))
                return val
        raise ValueError(
            f"could not infer min_num_obs value from input dict {min_num_obs} "
            f"for conversion from {self} to {to_ts_type}"
        )

    def check_match_total_seconds(self, total_seconds: int | float) -> bool:
        """
        Check if this object matches with input interval length in seconds

        Parameters
        ----------
        total_seconds : int or float
            interval length in units of seconds (e.g. 86400 for daily)

        Returns
        -------
        bool

        """
        try:
            numsecs = self.num_secs
            tolsecs = self.tol_secs
        except ValueError:  # native / undefined
            return False
        low, high = numsecs - tolsecs, numsecs + tolsecs
        if np.logical_and(total_seconds >= low, total_seconds <= high):
            return True
        return False

    @staticmethod
    def _try_infer_from_total_seconds(base: str, total_seconds: int | float) -> TsType:
        """
        Infer multiplication factor required to match input interval length

        Not to be used directly, is used in :func:`from_total_seconds`.

        Parameters
        ----------
        base : str
            base frequency
        total_seconds : int or float
            interval length

        Raises
        ------
        TemporalResolutionError
            if TsType cannot be inferred

        Returns
        -------
        TsType
            inferred frequency

        """

        if base in TsType.TS_MAX_VALS:
            maxnum = TsType.TS_MAX_VALS[base]
        else:
            maxnum = 2
        candidates = []
        dts = []
        tstype = TsType(base)
        for mulfac in range(1, maxnum):
            tstype.mulfac = mulfac
            if tstype.check_match_total_seconds(total_seconds):
                dt = total_seconds - tstype.num_secs
                dts.append(dt)
                candidates.append(TsType(f"{mulfac}{base}"))
                if dt == 0 or dt < 0:  # current candidate has larger number of seconds than input
                    break

        if len(candidates) > 0:
            return candidates[np.argmin(np.abs(dts))]

        raise TemporalResolutionError(
            f"Period {total_seconds}s could not be associated with any "
            f"allowed multiplication factor of base frequency {base}"
        )

    @staticmethod
    def from_total_seconds(total_seconds: int | float) -> TsType:
        """
        Try to infer TsType based on interval length

        Parameters
        ----------
        total_seconds : int or float
            total number of seconds

        Raises
        ------
        TemporalResolutionError
            If no TsType can be inferred for input number of seconds

        Returns
        -------
        TsType

        """
        candidates = []
        candidates_diff = []
        for tst in TsType.VALID_ITER:
            tstype = TsType(tst)
            if tstype.check_match_total_seconds(total_seconds):
                return tstype
            diff = total_seconds - tstype.num_secs
            if diff > 0:
                candidates.append(tst)
                candidates_diff.append(diff)
        if len(candidates) > 0:
            # sort by the candidate that has the lowest dt
            candidates_sorted = [c for _, c in sorted(zip(candidates_diff, candidates))]
            for base_tst in candidates_sorted:
                try:
                    return TsType._try_infer_from_total_seconds(base_tst, total_seconds)
                except TemporalResolutionError as e:
                    logger.info(e)
                    continue

        raise TemporalResolutionError(
            f"failed to infer ts_type based on input dt={total_seconds} s"
        )

    def _from_pandas(self, val):
        if val not in self.FROM_PANDAS:
            raise TemporalResolutionError(f"Invalid input: {val}, need pandas frequency string")
        return self.FROM_PANDAS[val]

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            other = TsType(other)
        return other.val == self.val

    def __hash__(self):
        return self.val.__hash__()

    def __lt__(self, other) -> bool:
        if isinstance(other, str):
            other = TsType(other)
        # inverted comparison, i.e. if other has less seconds if has higher
        # resolution
        return self.num_secs > other.num_secs

    def __call__(self) -> str:
        return self.val

    def __str__(self) -> str:
        return str(self.val)

    def __repr__(self) -> str:
        return str(self.val)


def sort_ts_types(ts_types: list[str | TsType]) -> list[str]:
    """Sort a list of ts_types in ascending order, returning them as
    strings.

    Parameters
    ----------
    ts_types : list
        list of strings (or instance of :class:`TsType`) to be sorted

    Returns
    -------
    list
        list of strings with sorted frequencies

    Raises
    ------
    TemporalResolutionError
        if one of the input ts_types is not supported
    """
    ls = [TsType(x) for x in ts_types]
    return [str(tstype) for tstype in sorted(ls, reverse=True)]


def get_lowest_resolution(ts_type: str | TsType, *ts_types: str | TsType) -> str:
    """Get the lowest resolution from several ts_type codes

    Parameters
    ----------
    ts_type : str
        first ts_type
    *ts_types
        one or more additional ts_type codes

    Returns
    -------
    str
        the ts_type that corresponds to the lowest resolution

    Raises
    ------
    ValueError
        if one of the input ts_type codes is not supported
    """
    ls = [ts_type]
    ls.extend(ts_types)
    return sort_ts_types(ls)[-1]


def get_highest_resolution(ts_type: str | TsType, *ts_types: str | TsType) -> str:
    """Get the highest resolution from several ts_type codes

    Parameters
    ----------
    ts_type : str
        first ts_type
    *ts_types
        one or more additional ts_type codes

    Returns
    -------
    str
        the ts_type that corresponds to the highest resolution

    Raises
    ------
    ValueError
        if one of the input ts_type codes is not supported
    """
    lst = [ts_type]
    lst.extend(ts_types)
    return sort_ts_types(lst)[0]
