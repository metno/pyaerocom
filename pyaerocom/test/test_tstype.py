#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import pytest

import numpy as np

from pyaerocom.tstype import TsType

def test_basic_operators():
    monthly = TsType('monthly')
    yearly = TsType('yearly')
    daily = TsType('daily')

    assert monthly < daily
    assert monthly <= daily
    assert monthly != daily
    assert yearly < daily
    assert not (yearly == daily)
    assert monthly > yearly
    assert monthly >= yearly

def test_basic_operators_pandas():
    monthly = TsType('MS')
    yearly = TsType('AS')
    daily = TsType('D')

    assert monthly < daily
    assert monthly <= daily
    assert monthly != daily
    assert yearly < daily
    assert not (yearly == daily)
    assert monthly > yearly
    assert monthly >= yearly

def test_to_numpy_freq():
    assert TsType('3hourly').to_numpy_freq() == '3h'
    assert TsType('daily').to_numpy_freq() == '1D'

def test_to_pandas_freq():
    assert TsType('3hourly').to_pandas_freq() == '3H'
    assert TsType('daily').to_pandas_freq() == 'D'

def test_cf_base_unit():
    assert TsType('daily').cf_base_unit == 'days'
    assert TsType('monthly').cf_base_unit == 'days'
    assert TsType('hourly').cf_base_unit == 'hours'

def test_next_higher():
    try:
        TsType('minutely').next_higher
    except Exception as e:
        assert type(e) == IndexError

    assert str(TsType('3minutely').next_higher) == 'minutely'
    assert str(TsType('hourly').next_higher) == 'minutely'
    assert str(TsType('monthly').next_higher) == 'weekly'

def test_next_lower():
    try:
        TsType('yearly').next_lower
    except Exception as e:
        assert type(e) == IndexError

    assert str(TsType('3minutely').next_lower) == 'hourly'

@pytest.mark.parametrize('ts_type,ref_time_str,np_dt_str,output_str', [
    ('daily', '2010-10-01', 'D', '2010-10-02'),
    ('2monthly', '2010-10', 'M', '2010-12'),
    ('3hourly', '2010-10-01T15:00:00', 'h', '2010-10-01T18')
    ])
def test_to_timedelta64(ts_type, ref_time_str, np_dt_str, output_str):
    tref = np.datetime64(ref_time_str, np_dt_str)
    assert str(tref + TsType(ts_type).to_timedelta64()) == output_str

if __name__=="__main__":

    import sys
    pytest.main(sys.argv)
