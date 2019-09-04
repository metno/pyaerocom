#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
General helper methods for the pyaerocom library.
"""
from pyaerocom import const
from pyaerocom.helpers import PANDAS_FREQ_TO_TS_TYPE

class TsType(object):
    VALID = const.GRID_IO.TS_TYPES
    FROM_PANDAS = PANDAS_FREQ_TO_TS_TYPE
    
    def __init__(self, val):
        self._val = None
        
        self.val = val
        
    @property
    def val(self):
        """String name of frequency"""
        return self._val
    
    @val.setter
    def val(self, val):
        if not val in self.VALID:
            try:
                val = self._from_pandas(val)
            except ValueError:
                raise ValueError('Invalid input. Need any valid ts_type: {}'
                                 .format(self.VALID))
        self._val = val
        
    @staticmethod
    def infer(self, datetime_index):
        """Infer resolution based on input datateime_index
        
        Uses :func:`pandas.infer_freq` to infer frequency
        """
        raise NotImplementedError
        
    def _from_pandas(self, val):
        if not val in self.FROM_PANDAS:
            raise ValueError('Invalid input: {}, need pandas frequency string'
                             .format(val))
        return self.FROM_PANDAS[val]
    
    def _get_str(self, val=None):
        if val is None:
            val = self._val
        elif isinstance(val, TsType):
            val = val.val
        if not isinstance(val, str):
            raise ValueError('Invalid input, need TsType or str')
        if not val in self.VALID:
            val = self._from_pandas(val)
        return val
    
    def __lt__(self, other):
        idx_this = self.VALID.index(self._get_str())
        idx_other = self.VALID.index(self._get_str(other))
        return idx_this > idx_other
    
    def __le__(self, other):
        return True if (self.__eq__(other) or self.__lt__(other)) else False
        
    def __call__(self):
        return self.val
    
    def __str__(self):
        return self._val
    
    def __repr__(self):
        return self.val
    
    def __eq__(self, other):
        return self._get_str(other) == self._get_str()
    
    
    
if __name__=="__main__":


    daily = TsType('daily')
    monthly = TsType('monthly')
    
    print('Monthly < daily:', monthly < daily)
    print('Monthly == daily:', monthly == daily)
    print('Daily == daily:', daily==daily)
    print('Monthly <= daily:', monthly <= daily)
    print('daily >= monthly:', daily   >= monthly)
    print('Monthly >= daily:', monthly >= daily)
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
