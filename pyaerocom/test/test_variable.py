#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 16:31:13 2020

@author: jonasg
"""

import pytest
from pyaerocom.variable import Variable

def test_od550aer():
    v0 = Variable('od550aer')
    v1 = Variable('OD5503Ddryaer')
    
    assert v0.var_name_aerocom == 'od550aer'
    assert v1.var_name_aerocom != v0.var_name_aerocom
    assert v1.is_3d
    assert v1.is_dry
    assert not v0.is_dry
    assert v0.wavelength_nm == 550
    
def test_alias_var():
    assert 'od550csaer' == Variable('od550aer')
    
def test_alias_families():
    var = Variable('SCONCSO4')
    
    assert var.var_name_input == 'sconcso4'
    assert var.var_name == 'sconcso4'
    assert var.var_name_aerocom == 'concso4'
    assert var.units == 'ug m-3'
    
if __name__=='__main__':
    import sys
    pytest.main(sys.argv)    