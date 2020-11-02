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
                                   PANDAS_RESAMPLE_OFFSETS)
from pyaerocom.exceptions import TemporalResolutionError

class TsType(object):
    VALID = const.GRID_IO.TS_TYPES
    FROM_PANDAS = PANDAS_FREQ_TO_TS_TYPE
    TO_PANDAS = TS_TYPE_TO_PANDAS_FREQ
    TO_NUMPY =  TS_TYPE_TO_NUMPY_FREQ
    RS_OFFSETS = PANDAS_RESAMPLE_OFFSETS

    TS_MAX_VALS = {'hourly' : 24,
                   'daily'  : 7,
                   'weekly' : 4,
                   'monthly': 12}

    TSTR_TO_CF = {"hourly"  :  "hours",
                  "daily"   :  "days",
                  "monthly" :  "days"}

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
            self._mulfac = int(value)
        except Exception:
            raise ValueError('mulfac needs to be int or convertible to int')

    @property
    def base(self):
        """Base string (without multiplication factor, cf :attr:`mulfac`)"""
        return self._val

    @property
    def name(self):
        """Name of ts_type (Wrapper for :attr:`val`)"""
        return self.val

    @property
    def val(self):
        """Value of frequency (string type), e.g. 3daily"""
        if self._mulfac != 1:
            return '{}{}'.format(self._mulfac, self._val)
        return self._val

    @val.setter
    def val(self, val):
        ival=1
        if val[-1].isdigit():
            raise TemporalResolutionError('Invalid input for TsType: {}'
                                          .format(val))
        elif val[0].isdigit():
            ivalstr = re.findall('\d+', val)[0]
            val = val.split(ivalstr)[-1]
            ival = int(ivalstr)
        if not val in self.VALID:
            try:
                val = self._from_pandas(val)
            except TemporalResolutionError:
                raise TemporalResolutionError('Invalid input. Need any valid '
                                              'ts_type: {}'
                                              .format(self.VALID))
        if val in self.TS_MAX_VALS and ival != 1:
            if ival > self.TS_MAX_VALS[val]:
                raise TemporalResolutionError('Invalid input for ts_type {}{}. '
                                              'Interval factor {} exceeds '
                                              'maximum allowed for {}, which '
                                              'is: {}'
                                              .format(ival, val, ival, val,
                                                      self.TS_MAX_VALS[val]))
        self._val = val
        self._mulfac = ival

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
    def next_lower(self):
        """Next lower resolution code"""
        idx = self.VALID.index(self._val)
        if idx == len(self.VALID) - 1:
            raise IndexError('No lower resolution available than {}'.format(self))
        return TsType(self.VALID[idx+1])

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

        idx = self.VALID.index(self._val)
        if idx == 0:
            raise IndexError('No lower resolution available than {}'.format(self))
        return TsType(self.VALID[idx-1])

    @staticmethod
    def infer(self, datetime_index):
        """Infer resolution based on input datateime_index

        Uses :func:`pandas.infer_freq` to infer frequency
        """
        raise NotImplementedError

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

    def _from_pandas(self, val):
        if not val in self.FROM_PANDAS:
            raise TemporalResolutionError('Invalid input: {}, need pandas '
                                          'frequency string'
                                          .format(val))
        return self.FROM_PANDAS[val]

    def __lt__(self, other):
        if self.val == other.val:
            return False

        idx_this = self.VALID.index(self._val)
        idx_other = self.VALID.index(other._val)
        if not idx_this == idx_other: #they have a different freq string
            return idx_this > idx_other
        #they have the same frequency string but different _mulfac attributes
        return self._mulfac > other._mulfac

    def __le__(self, other):
        return True if (self.__eq__(other) or self.__lt__(other)) else False

    def __eq__(self, other):
        return other.val == self.val

    def __call__(self):
        return self.val

    def __str__(self):
        return self.val

    def __repr__(self):
        return self.val

if __name__=="__main__":

    from pyaerocom.helpers import sort_ts_types

    daily = TsType('daily')
    monthly = TsType('monthly')

    print('Monthly < daily:', monthly < daily)
    print('Monthly == daily:', monthly == daily)
    print('Daily == daily:', daily==daily)
    print('Monthly <= daily:', monthly <= daily)
    print('daily >= monthly:', daily   >= monthly)
    print('daily > monthly:', daily > monthly)
    print('Monthly >= daily:', monthly >= daily)

    hourly = TsType('hourly')
    hourly5 = TsType('5hourly')

    print(hourly)
    print(hourly5)

    print('hourly == 5hourly:', hourly==hourly5)
    print('hourly > 5hourly:', hourly>hourly5)

    print(TsType('yearly').next_higher)

    hourly = TsType('hourly')

    daily = hourly.next_lower

    print(hourly.next_lower)

    unsorted = ['monthly', 'hourly', '5minutely', '3daily', 'daily']

    sort = sort_ts_types(unsorted)

    print(sort)

    print(TsType('16hourly').datetime64_str)
    print(TsType('16hourly').timedelta64_str)
    print(TsType('16hourly').cf_base_unit)
# =============================================================================
#
#     class Num(object):
#         def __init__(self, val):
#             self.val = val
#
#         def __lt__(self, other):
#             print('Other is smaller than this')
#             return self.val < other.val
#
#     print(Num(3) < Num(5))
# =============================================================================
