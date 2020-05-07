#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""


from pyaerocom import units_helpers as helpers
from pyaerocom.conftest import lustre_unavail
from pyaerocom.griddeddata import GriddedData
from iris.cube import Cube
from pyaerocom.exceptions import UnitConversionError

def test_unit_conversion_fac():
    assert helpers.unit_conversion_fac('m-1', '1/Mm') == 1e6


def test_implicit_to_explicit_rates_already_rate():
    g = GriddedData()
    # Function should not convert data that is already a rate
    g.units = 's-1'
    assert helpers.implicit_to_explicit_rates(g, 'monthly') == False
    g.units = '1/s'
    assert helpers.implicit_to_explicit_rates(g, 'monthly') == False


@lustre_unavail
def test_implicit_to_explicit_rates_convert_data():
    # TODO: Add a simple conversion test with a griddeddata object
    pass
