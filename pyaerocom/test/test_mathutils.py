#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for _lowlevel_helpers.py module of pyaerocom
"""

import numpy.testing as npt
import pyaerocom.mathutils as utils

def test_exponent():
    """Test method :func:`exponent` of :mod:`pyaerocom.utils`"""
    nominal = [-2, 0, 2]
    vals = [utils.exponent(.01),
            utils.exponent(4),
            utils.exponent(234)]
    npt.assert_array_equal(nominal, vals)
    
if __name__ == '__main__':
    test_exponent()
    
    