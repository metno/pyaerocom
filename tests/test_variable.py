#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from pyaerocom import const
from pyaerocom.variable import Variable
from pyaerocom.variable import get_emep_variables

@pytest.mark.parametrize('var_name,var_name_aerocom', [
    ('od550aer', 'od550aer'),
    ('od550du', 'od550dust'),
    ('od550csaer', 'od550aer'),
    ('latitude', 'lat'),
    ('abs550oc', 'abs550oa'),
    ('sconcss', 'concss'),

    ])
def test_var_name_aerocom(var_name, var_name_aerocom):
    assert Variable(var_name).var_name_aerocom == var_name_aerocom

def test_alias_var():
    assert 'od550csaer' == Variable('od550aer')


def test_alias_families():
    var = Variable('sconcso4')

    assert var.var_name_input == 'sconcso4'
    assert var.var_name == 'sconcso4'
    assert var.var_name_aerocom == 'concso4'
    assert var.units == 'ug m-3'

def test_get_emep_variables():
    variables = get_emep_variables()
    assert isinstance(variables, dict)
    assert variables['conco3'] == 'SURF_ug_O3'

def test_VarCollection_add_var():
    var = Variable(var_name='concpmgt10',
                   units='ug m-3',
                   long_name='PM mass greater than 10 um')

    const.VARS.add_var(var)
    assert 'concpmgt10' in const.VARS
    var1 = const.VARS['concpmgt10']
    assert var1.var_name == var.var_name
    assert var1.var_name_aerocom == var.var_name_aerocom
    assert var1.units == var.units
    assert var1.long_name == var.long_name



if __name__=='__main__':
    import sys
    pytest.main(sys.argv)
