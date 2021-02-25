#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import pytest

import numpy as np
from pyaerocom.conftest import does_not_raise_exception
from pyaerocom.tstype import TsType

def test_VALID():
    assert TsType.VALID == ['minutely', 'hourly', 'daily', 'weekly', 'monthly',
                            'yearly', 'native']

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

@pytest.mark.parametrize('ts_type, value, raises', [
    ('hourly', 'h', does_not_raise_exception()),
    ('3hourly', '3h', does_not_raise_exception()),
    ('daily', 'd', does_not_raise_exception()),
    ('minutely', 'min', does_not_raise_exception()),
    ('weekly', 'week', does_not_raise_exception()),
    ('monthly', 'month',does_not_raise_exception()),
    ('4weekly', '4week', does_not_raise_exception()),
    ])
def test_to_si(ts_type, value, raises):
    with raises:
        assert TsType(ts_type).to_si() == value

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


def test_TOL_SECS_PERCENT():
    assert TsType.TOL_SECS_PERCENT == 5

@pytest.mark.parametrize('ts_type,should_be', [
    ('minutely', 60),
    ('3minutely', 180),
    ('4minutely', 240),
    ('daily', 86400),
    ('weekly', 86400*7),
    ('monthly', 2629743.831225) # not sure how cf_units calculates that
    ])
def test_num_secs(ts_type, should_be):
    val = TsType(ts_type).num_secs
    assert val == should_be

@pytest.mark.parametrize('ts_type,should_be', [
    ('minutely', 3),
    ('3minutely', 9),
    ('4minutely', 12),
    ('daily', 4320),
    ('weekly', 30240),
    ('monthly', 131488)
    ])
def test_tol_secs(ts_type, should_be):
    val = TsType(ts_type).tol_secs
    assert val == should_be

if __name__=="__main__":

    import sys
    pytest.main(sys.argv)
