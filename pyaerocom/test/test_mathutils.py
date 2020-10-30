#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for _lowlevel_helpers.py module of pyaerocom
"""
import pytest
import numpy.testing as npt
import pyaerocom.mathutils as mu

@pytest.mark.parametrize('inputval, desired', [
    (0.01, -2), (4, 0), (234, 2)
    ])
def test_exponent(inputval, desired):
    """Test method :func:`exponent` of :mod:`pyaerocom.utils`"""
    assert mu.exponent(inputval) == desired

@pytest.mark.parametrize('inputval, p, T, vmr_unit, mmol_var, mmol_air, to_unit, desired', [
    (1, 101300,293,'nmol mol-1',48,None,'ug m-3', 1.9959),
    (1, 101300,273,'nmol mol-1',48,None,'ug m-3', 2.1421),
    (1, 101300,273,'nmol mol-1',48,None,'kg m-3', 2.1421e-9),
    (1, 101300,273,'mol mol-1',48,None,'kg m-3', 2.1421),
    (1, 98000,273,'mol mol-1',48,None,'kg m-3', 2.0724),
    ])
def test_vmrx_to_concx(inputval, p, T, vmr_unit, mmol_var,
                       mmol_air, to_unit, desired):
    val = mu.vmrx_to_concx(inputval, p, T, vmr_unit, mmol_var, mmol_air,
                           to_unit)
    npt.assert_allclose(val, desired, rtol=1e-4)

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
