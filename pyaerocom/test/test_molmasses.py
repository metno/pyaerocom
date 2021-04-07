#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 09:56:54 2020

@author: jonasg
"""
import pytest
import numpy.testing as npt
from pyaerocom import molmasses as mm

@pytest.mark.parametrize('var_name,species', [
    ('air_dry', 'air_dry'),
    ('concno2', 'no2'),
    ('sconcso2', 'so2'),
    ('vmro3' , 'o3'),
    ('mmro3' , 'o3'),
    ('wetso4', 'so4')
    ])
def test_get_species(var_name, species):
    assert mm.get_species(var_name) == species

@pytest.mark.parametrize('var_name,molmass', [
    ('air_dry', 28.9647),
    ('concno2', 46.0055),
    ('sconcso2', 64.066),
    ('vmro3' , 48),
    ('mmro3' , 48),
    ('wetso4', 96.06)
    ])
def test_get_molmass(var_name, molmass):
    assert mm.get_molmass(var_name) == molmass

@pytest.mark.parametrize('var_name,result', [
    ('mmro3', 0.60343125),
    ('conco3', 0.60343125),
    ])
def test_get_mmr_to_vmr_fac(var_name, result):
    val = mm.get_mmr_to_vmr_fac(var_name)
    npt.assert_allclose(val, result,rtol=1e-3)

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
