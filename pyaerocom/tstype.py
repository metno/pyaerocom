#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General helper methods for the pyaerocom library.
"""
import numpy as np
import re
from pyaerocom import const
from pyaerocom.time_config import (PANDAS_FREQ_TO_TS_TYPE,
                                   TS_TYPE_TO_PANDAS_FREQ,
                                   TS_TYPE_TO_NUMPY_FREQ,
                                   TS_TYPE_TO_SI,
                                   TS_TYPES)

from pyaerocom.exceptions import TemporalResolutionError

class TsType(object):
    VALID = TS_TYPES
    VALID_ITER = VALID[:-1]
    FROM_PANDAS = PANDAS_FREQ_TO_TS_TYPE
    TO_PANDAS = TS_TYPE_TO_PANDAS_FREQ
    TO_NUMPY =  TS_TYPE_TO_NUMPY_FREQ
    TO_SI = TS_TYPE_TO_SI

    TS_MAX_VALS = {'minutely' : 360, # up to 6hourly
                   'hourly' : 168, #up to weekly
                   'daily'  : 180, # up to 6 monthly
                   'weekly' : 104, # up to ~2yearly
                   'monthly': 120} # up to 10yearly

    TSTR_TO_CF = {"hourly"  :  "hours",
                  "daily"   :  "days",
                  "monthly" :  "days"}

    TOL_SECS_PERCENT = 5

    def __init__(self, val):
        self._mulfac = 1
        self._val = None

        self.val = val

    @property
    def mulfac(self):
        """Multiplication factor of frequency"""
        return self._mulfac

    @mulfac.setter
    def mulfac(self, value):
        try:
            value = int(value)
        except Exception:
            raise ValueError('mulfac needs to be int or convertible to int')
        if self.base in self.TS_MAX_VALS and value > self.TS_MAX_VALS[self.base]:
            raise ValueError(
                f'Multiplication factor exceeds maximum allowed, which is '
                f'{self.TS_MAX_VALS[self.base]}')
        self._mulfac = value

    @property
    def base(self):
        """Base string (without multiplication factor, cf :attr:`mulfac`)"""
        return self._val

    @property
    def val(self):
        """Value of frequency (string type), e.g. 3daily"""
        if self._mulfac != 1:
            return '{}{}'.format(self._mulfac, self._val)
        return self._val

    @val.setter
    def val(self, val):
        if val is None:
            raise TemporalResolutionError(
                'Invalid input, please provide valid frequency string...')
        mulfac = 1
        if val[0].isdigit():
            ivalstr = re.findall('\d+', val)[0]
            val = val.split(ivalstr)[-1]
            mulfac = int(ivalstr)
        if not val in self.VALID:
            try:
                val = self._from_pandas(val)
            except TemporalResolutionError:
                raise TemporalResolutionError(
                    f'Invalid input for ts_type {val}. Choose from {self.VALID}'
                    )
        if val in self.TS_MAX_VALS and mulfac != 1:
            if mulfac > self.TS_MAX_VALS[val]:
                raise TemporalResolutionError(
                    f'Invalid input for ts_type {val}. Multiplication factor '
                    f'{mulfac} exceeds maximum allowed for {val}, which is '
                    f'{self.TS_MAX_VALS[val]}')
        self._val = val
        self._mulfac = mulfac

    @property
    def datetime64_str(self):
        """Convert ts_type str to datetime64 unit string"""
        return 'datetime64[{}]'.format(self.to_numpy_freq())

    @property
    def timedelta64_str(self):
        """Convert ts_type str to datetime64 unit string"""
        return 'timedelta64[{}]'.format(self.to_numpy_freq())

    @property
    def cf_base_unit(self):
        """Convert ts_type str to CF convention time unit"""
        if not self.base in self.TSTR_TO_CF:
            raise NotImplementedError('Cannot convert {} to CF str'
                                      .format(self.base))
        return self.TSTR_TO_CF[self.base]

    @property
    def num_secs(self):
        """Number of seconds in one period

        Note
        ----
        Be aware that for monthly frequency the number of seconds is not well
        defined!
        """
        from cf_units import Unit
        cf = self.to_si()
        total_secs = 1 / Unit('s').convert(1, cf)
        return total_secs

    @property
    def tol_secs(self):
        """Tolerance in seconds for current TsType"""
        total_secs = self.num_secs
        frac = self.TOL_SECS_PERCENT / 100
        return int(np.ceil(frac*total_secs))

    def to_timedelta64(self):
        """
        Convert frequency to timedelta64 object

        Can be used, e.g. as tolerance when reindexing pandas Series

        Returns
        -------
        timedelta64

        """
        return np.timedelta64(1, self.to_numpy_freq())


    @property
    def next_higher(self):
        """Next lower resolution code"""
        if self.mulfac > 1:
            return TsType(self._val)

        idx = self.VALID_ITER.index(self._val)
        if idx == 0:
            raise IndexError('No higher resolution available than {}'.format(self))
        return TsType(self.VALID_ITER[idx-1])

    @property
    def next_lower(self):
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
        tst = TsType(self.VALID_ITER[idx+1])
        if self.mulfac == 1 or self.num_secs < tst.num_secs:
            return tst
        try:
            maxmul = self.TS_MAX_VALS[tst.base]
        except:
            maxmul = 10
        numsecs = self.num_secs
        for mulfac in range(1,maxmul+1):
            tst.mulfac = mulfac
            if numsecs < tst.num_secs:
                return tst
        raise TemporalResolutionError(
            f'Failed to determine next lower resolution for {self}'
            )

    @staticmethod
    def valid(val):
        try:
            TsType(val)
            return True
        except TemporalResolutionError:
            return False

    def to_numpy_freq(self):
        if not self._val in self.TO_NUMPY:
            raise TemporalResolutionError('numpy frequency not available for {}'
                                          .format(self._val))
        freq = self.TO_NUMPY[self._val]
        return '{}{}'.format(self.mulfac, freq)

    def to_pandas_freq(self):
        """Convert ts_type to pandas frequency string"""
        if not self._val in self.TO_PANDAS:
            raise TemporalResolutionError('pandas frequency not available for {}'
                                          .format(self._val))
        freq = self.TO_PANDAS[self._val]
        if self._mulfac == 1:
            return freq
        return '{}{}'.format(self._mulfac, freq)

    def to_si(self):
        """Convert to SI conform string (e.g. used for unit conversion)"""
        base = self.base
        if not base in self.TO_SI:
            raise ValueError(f'Cannot convert ts_type={self} to SI unit string...')
        si = self.TO_SI[base]
        return si if self.mulfac == 1 else f'{self.mulfac}{si}'

    def check_match_total_seconds(self, total_seconds):
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
        except ValueError: #native / undefined
            return False
        low, high = numsecs-tolsecs, numsecs+tolsecs
        if np.logical_and(total_seconds >= low,
                          total_seconds <= high):
            return True
        return False

    @staticmethod
    def _try_infer_from_total_seconds(base, total_seconds):
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
                candidates.append(TsType(f'{mulfac}{base}'))
                if dt == 0 or dt < 0: #current candidate has larger number of seconds than input
                    break

        if len(candidates) > 0:
            return candidates[np.argmin(np.abs(dts))]

        raise TemporalResolutionError(
            f'Period {total_seconds}s could not be associated with any '
            f'allowed multiplication factor of base frequency {base}')


    @staticmethod
    def from_total_seconds(total_seconds):
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
            candidates_sorted = [c for _,c in sorted(zip(candidates_diff, candidates))]
            for base_tst in candidates_sorted:
                try:
                    return TsType._try_infer_from_total_seconds(base_tst,
                                                                total_seconds)
                except TemporalResolutionError as e:
                    const.logger.info(e)
                    continue

        raise TemporalResolutionError(
            f'failed to infer ts_type based on input dt={total_seconds} s'
            )



    def _from_pandas(self, val):
        if not val in self.FROM_PANDAS:
            raise TemporalResolutionError('Invalid input: {}, need pandas '
                                          'frequency string'
                                          .format(val))
        return self.FROM_PANDAS[val]

    def __eq__(self, other):
        if isinstance(other, str):
            other = TsType(other)
        return other.val == self.val

    def __lt__(self, other):
        if isinstance(other, str):
            other = TsType(other)
        nss, nso = self.num_secs, other.num_secs
        # inverted comparison, i.e. if other has less seconds if has higher
        # resolution
        return nss > nso

    def __le__(self, other):
        return True if (self.__eq__(other) or self.__lt__(other)) else False

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __call__(self):
        return self.val

    def __str__(self):
        return self.val

    def __repr__(self):
        return self.val

if __name__=="__main__":

    from pyaerocom.helpers import sort_ts_types

    print(TsType.from_total_seconds(1200))
    print(TsType.from_total_seconds(31556925*2))
