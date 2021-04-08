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

def test_TsType_TOL_SECS_PERCENT():
    assert TsType.TOL_SECS_PERCENT == 5

def test_TsType_TSTR_TO_CF():
    assert TsType.TSTR_TO_CF == {"hourly"  :  "hours",
                                  "daily"   :  "days",
                                  "monthly" :  "days"}

def test_TsType_TS_MAX_VALS():
    assert TsType.TS_MAX_VALS == {'minutely': 360,
                                  'hourly' : 168, #up to weekly
                                  'daily'  : 180, # up to 6 monthly
                                  'weekly' : 104, # up to ~2yearly
                                  'monthly': 120} # up to 10yearly

@pytest.mark.parametrize('base,mulfac,raises', [
    ('daily', 10, does_not_raise_exception()),
    ('daily', '10', does_not_raise_exception()),
    ('daily', '10.1', pytest.raises(ValueError)),
    ('daily', 10.1, does_not_raise_exception()),
    ('daily', 200, pytest.raises(ValueError))
    ])
def test_TsType_mulfac(base, mulfac, raises):
    tst = TsType(base)
    with raises:
        tst.mulfac = mulfac
        assert int(mulfac) == tst._mulfac == tst.mulfac

def test_TsType_base():
    tst = TsType('daily')
    assert tst.base == tst._val == 'daily'

@pytest.mark.parametrize('value,raises', [
    ('3daily', does_not_raise_exception()),
    ('blaa', pytest.raises(TemporalResolutionError)),
    ('5000daily', pytest.raises(TemporalResolutionError))
    ])
def test_TsType_val(value, raises):
    tst = TsType('daily')
    with raises:
        tst.val =  value
        assert isinstance(tst.val, str)
        assert tst.val == value

def test_TsType_datetime64_str():
    assert TsType('daily').datetime64_str == 'datetime64[1D]'

def test_TsType_timedelta64_str():
    assert TsType('daily').timedelta64_str == 'timedelta64[1D]'


@pytest.mark.parametrize('base, value, raises', [
    ('native', None, pytest.raises(NotImplementedError)),
    ('minutely', 'minutes', pytest.raises(NotImplementedError)),
    ('hourly', 'hours', does_not_raise_exception()),
    ('daily', 'days', does_not_raise_exception()),
    ('monthly', 'days', does_not_raise_exception()),
    ('yearly', 'days', pytest.raises(NotImplementedError)),
    ])
def test_TsType_cf_base_unit(base, value, raises):
    tst = TsType(base)
    with raises:
        assert tst.cf_base_unit == value

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

@pytest.mark.parametrize('ts_type,ref_time_str,np_dt_str,output_str', [
    ('daily', '2010-10-01', 'D', '2010-10-02'),
    ('2monthly', '2010-10', 'M', '2010-12'),
    ('3hourly', '2010-10-01T15:00:00', 'h', '2010-10-01T18')
    ])
def test_TsType_to_timedelta64(ts_type, ref_time_str, np_dt_str, output_str):
    tref = np.datetime64(ref_time_str, np_dt_str)
    assert str(tref + TsType(ts_type).to_timedelta64()) == output_str

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
    ('yearly', '2yearly', does_not_raise_exception()),
    ('monthly', 'yearly', does_not_raise_exception()),
    ('3monthly', 'yearly',  does_not_raise_exception()),
    ('8daily', '2weekly',  does_not_raise_exception()),
    ('13monthly', '2yearly',  does_not_raise_exception()),
    ('13monthly', '2yearly',  does_not_raise_exception()),
    ('1000yearly', '1001yearly', does_not_raise_exception()),
    ('120monthly', None, pytest.raises(TemporalResolutionError))

    ])
def test_TsType_next_lower(ts_type, value, raises):
    with raises:
        assert TsType(ts_type).next_lower.val == value

@pytest.mark.parametrize('val,valid', [
    ('bla', False), ('60000daily', False), ('daily', True)
    ])
def test_TsType_valid(val, valid):
    assert TsType.valid(val) == valid

@pytest.mark.parametrize('tst,val,raises', [
    ('3hourly','3h',does_not_raise_exception()),
    ('daily','1D',does_not_raise_exception()),
    ('native', None, pytest.raises(TemporalResolutionError))
    ])
def test_TsType_to_numpy_freq(tst, val, raises):
    tst = TsType(tst)
    with raises:
        assert tst.to_numpy_freq() == val

@pytest.mark.parametrize('tst,val,raises', [
    ('3hourly','3H',does_not_raise_exception()),
    ('daily','D',does_not_raise_exception()),
    ('native', None, pytest.raises(TemporalResolutionError))
    ])
def test_TsType_to_pandas_freq(tst, val, raises):
    tst = TsType(tst)
    with raises:
        assert tst.to_pandas_freq() == val

@pytest.mark.parametrize('ts_type, value, raises', [
    ('hourly', 'h', does_not_raise_exception()),
    ('3hourly', '3h', does_not_raise_exception()),
    ('daily', 'd', does_not_raise_exception()),
    ('minutely', 'min', does_not_raise_exception()),
    ('weekly', 'week', does_not_raise_exception()),
    ('monthly', 'month',does_not_raise_exception()),
    ('4weekly', '4week', does_not_raise_exception()),
    ('native', None, pytest.raises(ValueError))
    ])
def test_TsType_to_si(ts_type, value, raises):
    with raises:
        assert TsType(ts_type).to_si() == value

@pytest.mark.parametrize('ts_type, total_seconds, value, raises', [
    ('hourly', 3600, True, does_not_raise_exception()),
    ('hourly', 3605, True, does_not_raise_exception()),
    ('20minutely', 1200, True, does_not_raise_exception()),
    ('native', 1200, False, does_not_raise_exception())
    ])
def test_TsType_check_match_total_seconds(ts_type, total_seconds, value, raises):
    with raises:
        assert TsType(ts_type).check_match_total_seconds(total_seconds) == value

@pytest.mark.parametrize('base,total_seconds,val,raises', [
    ('daily', 86400*2, '2daily', does_not_raise_exception()),
    ('daily', 86400, 'daily', does_not_raise_exception()),
    ('daily', 86000, 'daily', does_not_raise_exception()), #5% tolerance
    ('yearly', 31556925, 'yearly', does_not_raise_exception()),
    ('yearly', 31556925*2, '2yearly', pytest.raises(TemporalResolutionError)),
    ])
def test_TsType__try_infer_from_total_seconds(base,total_seconds,val,raises):
    with raises:
        tst = TsType._try_infer_from_total_seconds(base, total_seconds)
        assert isinstance(tst, TsType)
        assert str(tst) == val

@pytest.mark.parametrize('total_seconds, value, raises', [
    (86400*2, '2daily', does_not_raise_exception()),
    (30, '2daily', pytest.raises(TemporalResolutionError)),
    (3605, 'hourly', does_not_raise_exception()),
    (1200, '20minutely', does_not_raise_exception()),
    (31556925*2, '24monthly', does_not_raise_exception()),
    (31556925*12, '12yearly', pytest.raises(TemporalResolutionError)),
    ])
def test_TsType_from_total_seconds(total_seconds, value, raises):
    with raises:
        tst = TsType.from_total_seconds(total_seconds)
        assert tst.val == value

@pytest.mark.parametrize('tst1,tst2,value,raises', [
    ('daily', 'daily', True, does_not_raise_exception()),
    (TsType('daily'), 'daily', True, does_not_raise_exception()),
    ('daily', TsType('daily'), True, does_not_raise_exception()),
    (TsType('daily'), TsType('monthly'), False, does_not_raise_exception()),
    (TsType('3daily'), TsType('2daily'), False, does_not_raise_exception()),
    (TsType('3daily'), TsType('daily'), False, does_not_raise_exception()),
    ])
def test_TsType__eq__(tst1, tst2, value, raises):
    with raises:
        same = tst1 == tst2
        assert same == value

@pytest.mark.parametrize('tst1,tst2,value,raises', [
    (TsType('daily'), 'daily', False, does_not_raise_exception()),
    (TsType('2daily'), TsType('monthly'), False, does_not_raise_exception()),
    (TsType('2daily'), TsType('1daily'), True, does_not_raise_exception()),
    ])
def test_TsType__lt__(tst1, tst2, value, raises):
    with raises:
        val = tst1 < tst2
        assert val == value

@pytest.mark.parametrize('tst1,tst2,value,raises', [
    (TsType('daily'), 'daily', True, does_not_raise_exception()),
    (TsType('2daily'), TsType('monthly'), False, does_not_raise_exception()),
    (TsType('2daily'), TsType('1daily'), True, does_not_raise_exception()),
    ])
def test_TsType__le__(tst1, tst2, value, raises):
    with raises:
        val = tst1 <= tst2
        assert val == value

@pytest.mark.parametrize('tst1,tst2,value,raises', [
    (TsType('daily'), 'daily', False, does_not_raise_exception()),
    (TsType('2daily'), TsType('monthly'), True, does_not_raise_exception()),
    (TsType('2daily'), TsType('1daily'), False, does_not_raise_exception()),
    ])
def test_TsType__gt__(tst1, tst2, value, raises):
    with raises:
        val = tst1 > tst2
        assert val == value

@pytest.mark.parametrize('tst1,tst2,value,raises', [
    (TsType('daily'), 'daily', True, does_not_raise_exception()),
    (TsType('2daily'), TsType('monthly'), True, does_not_raise_exception()),
    (TsType('2daily'), TsType('1daily'), False, does_not_raise_exception()),
    (TsType('6daily'), TsType('MS'), True, does_not_raise_exception()),
    (TsType('50daily'), TsType('MS'), False, does_not_raise_exception()),
    ])
def test_TsType__ge__(tst1, tst2, value, raises):
    with raises:
        val = tst1 >= tst2
        assert val == value

def test_TsType__call__():
    assert TsType('daily')() == 'daily'

def test_TsType__str__():
    assert str(TsType('daily')) == 'daily'

def test_TsType__repr__():
    assert repr(TsType('daily')) == 'daily'

if __name__=="__main__":

    import sys
    pytest.main(sys.argv)
