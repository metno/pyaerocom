#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import numpy.testing as npt
import pytest

import pyaerocom._concprcp_units_helpers
import pyaerocom.units_helpers
from pyaerocom.exceptions import UnitConversionError
from pyaerocom.griddeddata import GriddedData
from pyaerocom import units_helpers as mod

from .conftest import data_unavail, does_not_raise_exception

@pytest.mark.parametrize('unit,val', [
    ('ug min-1', True),('ug/min', True),('ug', False),
    ('ug m-1', False), ('ug m-2', False), ('kg m-2/yr', True),
    ('kg m-2/month', True), ('kg m-2/week', True), ('kg m-2 month-1', True),
    ('mm', False), ('mg d-1', True)

])
def test__check_unit_endswith_freq(unit,val):
    assert mod._check_unit_endswith_freq(unit) == val

@pytest.mark.parametrize('from_unit,to_unit,val', [
    ('m-1', '1/Mm', 1e6),
    ('ug m-3', 'ug/m3', 1)
])
def test__unit_conversion_fac_si(from_unit, to_unit, val):
    assert mod._unit_conversion_fac_si(from_unit, to_unit) == val


@pytest.mark.parametrize('var_name,from_unit,to_unit,val,raises', [
    ('concNno3', 'ug N m-3', 'ug m-3', 2.995821, pytest.raises(UnitConversionError)),
    ('concno3', 'ug N m-3', 'ug m-3', 4.426717, does_not_raise_exception()),
    ('concso2', 'ug S/m3', 'ug m-3', 1.9979, does_not_raise_exception()),
    ('concso4', 'ug S/m3', 'ug m-3', 2.9958, does_not_raise_exception()),
    ('concbc', 'ug C/m3', 'ug m-3', 1, does_not_raise_exception()),
    ('concoa', 'ug C/m3', 'ug m-3', 1, does_not_raise_exception()),
    ('concoc', 'ug C/m3', 'ug m-3', 1, does_not_raise_exception()),
    ('wetso4', 'kg S/ha', 'kg m-2', 0.0003, does_not_raise_exception()),
    ('concso4pr', 'mg S/L', 'g m-3', 2.995821, does_not_raise_exception()),
])
def test__unit_conversion_fac_custom(var_name,from_unit,to_unit,val,raises):
    with raises:
        to, num = mod._unit_conversion_fac_custom(var_name, from_unit)
        assert to == to_unit
        npt.assert_allclose(num, val, rtol=1e-2)

def test__unit_conversion_fac_custom_FAIL():
    df = mod.UCONV_MUL_FACS
    import pandas as pd
    UCONV_MUL_FACS = pd.DataFrame([

        ['concso4', 'ug S/m3', 'ug m-3', 1],
        ['concso4', 'ug S/m3', 'ug m-3', 2],

    ], columns=['var_name', 'from', 'to', 'fac']).set_index(
        ['var_name', 'from'])
    mod.UCONV_MUL_FACS = UCONV_MUL_FACS
    with pytest.raises(UnitConversionError):
        mod._unit_conversion_fac_custom('concso4', 'ug S/m3')
    mod.UCONV_MUL_FACS = df

@pytest.mark.parametrize('from_unit,to_unit,var_name,val', [
    ('ug m-3', 'ug/m3', None, 1),
    ('ug m-3', 'ug/m3', 'concso2', 1),
    ('mg m-3', 'ug m-3', 'concso2', 1e3),
    ('ug S/m3', 'mg m-3', 'concso2', 1.9979e-3)
])
def test_convert_unit(from_unit, to_unit, var_name, val):
    result = mod.convert_unit(1, from_unit, to_unit, var_name)
    npt.assert_allclose(result,
                        val, rtol=1e-2)

@pytest.mark.parametrize('from_unit,to_unit,var_name,ts_type,result,raises', [
    ('kg (2m)-2', 'kg/m2', None, None, 0.25, does_not_raise_exception()),
    ('kg m-2', 'mm', 'pr', None, 1, pytest.raises(
        UnitConversionError)),
    ('kg m-2', 'mm', 'od550aer', None,None, pytest.raises(
        UnitConversionError)),
    ('mm', 'mm d-1', 'prmm','daily',1, does_not_raise_exception()),
    ('mm', 'mm d-1', 'prmm','hourly',24, does_not_raise_exception()),
    ('mg m-2', 'ug m-2 d-1', 'wetoxs','hourly',24e3,
     does_not_raise_exception()),
    ('mg m-2', 'mg m-2 d-1', 'wetoxs','hourly',24,does_not_raise_exception()),
    ('mg m-2', 'mg m-2/d', 'wetoxs','daily',1,does_not_raise_exception()),
    ('mg m-2', 'mg m-2 d-1', 'wetoxs','daily',1,does_not_raise_exception()),
    ('mg m-2', 'ug mm-2', None,None,1e-3,does_not_raise_exception()),
    ('mg', 'ug', None,None,1000,does_not_raise_exception()),
    ('1', 'ug', None,None,None,pytest.raises(UnitConversionError)),
    ('1', '1', None,None,1,does_not_raise_exception()),
])
def test_get_unit_conversion_fac(from_unit,to_unit,var_name,ts_type,result,
                                 raises):
    with raises:
        val = mod.get_unit_conversion_fac(from_unit,to_unit,var_name,ts_type)
        npt.assert_allclose(val, result, rtol=1e-3)


