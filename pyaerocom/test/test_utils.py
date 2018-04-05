#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for utils.py module of pyaerocom
"""

import numpy.testing as npt
import pyaerocom.utils as utils

def test_exponent():
    """Test method :func:`exponent` of :mod:`pyaerocom.utils`"""
    nominal = [-2, 0, 2]
    vals = [utils.exponent(.01),
            utils.exponent(4),
            utils.exponent(234)]
    npt.assert_array_equal(nominal, vals)
    

    
    