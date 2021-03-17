#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import pytest

import numpy as np
from pyaerocom.exceptions import TemporalResolutionError
from pyaerocom.conftest import does_not_raise_exception
from pyaerocom.tstype import TsType


def test_TsType_VALID():
    assert TsType.VALID == ['minutely', 'hourly', 'daily', 'weekly', 'monthly',
                            'yearly', 'native']

def test_TsType_VALID_ITER():
    assert TsType.VALID_ITER == ['minutely', 'hourly', 'daily', 'weekly', 'monthly',
                                   'yearly']

def test_TsType_TS_MAX_VALS():
    assert TsType.TS_MAX_VALS == {'minutely': 180,
                                  'hourly' : 168, #up to weekly
                                  'daily'  : 180, # up to 6 monthly
                                  'weekly' : 104, # up to ~2yearly
                                  'monthly': 120} # up to 10yearly

@pytest.mark.parametrize('base,mulfac,raises', [
    ('daily', 10, does_not_raise_exception()),
    ('daily', '10', does_not_raise_exception()),
    ('daily', '10.1', pytest.raises(ValueError)),
    ('daily', 10.1, does_not_raise_exception())
    ])
def test_TsType_mulfac(base, mulfac, raises):
    tst = TsType(base)
    with raises:
        tst.mulfac = mulfac
        assert int(mulfac) == tst._mulfac == tst.mulfac

def test_TsType_basic_operators():
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

def test_TsType_basic_operators_pandas():
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

def test_TsType_to_numpy_freq():
    assert TsType('3hourly').to_numpy_freq() == '3h'
    assert TsType('daily').to_numpy_freq() == '1D'

def test_TsType_to_pandas_freq():
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
def test_TsType_to_si(ts_type, value, raises):
    with raises:
        assert TsType(ts_type).to_si() == value

def test_TsType_cf_base_unit():
    assert TsType('daily').cf_base_unit == 'days'
    assert TsType('monthly').cf_base_unit == 'days'
    assert TsType('hourly').cf_base_unit == 'hours'

@pytest.mark.parametrize('ts_type, value, raises', [
    ('minutely', None, pytest.raises(IndexError)),
    ('3minutely', 'minutely', does_not_raise_exception()),
    ('hourly', 'minutely', does_not_raise_exception()),
    ('3hourly', 'hourly', does_not_raise_exception()),
    ('weekly', 'daily', does_not_raise_exception()),
    ('monthly', 'weekly', does_not_raise_exception()),
    ('yearly', 'monthly', does_not_raise_exception()),
    ])
def test_TsType_next_higher(ts_type, value, raises):
    with raises:
        assert TsType(ts_type).next_higher.val == value

@pytest.mark.parametrize('ts_type, value, raises', [
    ('yearly', None, pytest.raises(IndexError))
    ])
def test_TsType_next_lower(ts_type, value, raises):
    with raises:
        assert TsType(ts_type).next_lower.val == value

@pytest.mark.parametrize('ts_type,ref_time_str,np_dt_str,output_str', [
    ('daily', '2010-10-01', 'D', '2010-10-02'),
    ('2monthly', '2010-10', 'M', '2010-12'),
    ('3hourly', '2010-10-01T15:00:00', 'h', '2010-10-01T18')
    ])
def test_TsType_to_timedelta64(ts_type, ref_time_str, np_dt_str, output_str):
    tref = np.datetime64(ref_time_str, np_dt_str)
    assert str(tref + TsType(ts_type).to_timedelta64()) == output_str


def test_TsType_TOL_SECS_PERCENT():
    assert TsType.TOL_SECS_PERCENT == 5

@pytest.mark.parametrize('ts_type,should_be', [
    ('minutely', 60),
    ('3minutely', 180),
    ('4minutely', 240),
    ('daily', 86400),
    ('weekly', 86400*7),
    ('monthly', 2629743.831225) # not sure how cf_units calculates that
    ])
def test_TsType_num_secs(ts_type, should_be):
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
def test_TsType_tol_secs(ts_type, should_be):
    val = TsType(ts_type).tol_secs
    assert val == should_be

@pytest.mark.parametrize('ts_type, total_seconds, value, raises', [
    ('hourly', 3600, True, does_not_raise_exception()),
    ('hourly', 3605, True, does_not_raise_exception()),
    ('20minutely', 1200, True, does_not_raise_exception())

    ])
def test_TsType_check_match_total_seconds(ts_type, total_seconds, value, raises):
    with raises:
        assert TsType(ts_type).check_match_total_seconds(total_seconds) == value

@pytest.mark.parametrize('total_seconds, value, raises', [
    (86400*2, '2daily', does_not_raise_exception()),
    (30, '2daily', pytest.raises(TemporalResolutionError)),
    (3605, 'hourly', does_not_raise_exception()),
    (1200, '20minutely', does_not_raise_exception())

    ])
def test_TsType_from_total_seconds(total_seconds, value, raises):
    with raises:
        tst = TsType.from_total_seconds(total_seconds)
        assert tst.val == value

if __name__=="__main__":

    import sys
    pytest.main(sys.argv)
