#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 17:07:45 2021

@author: jonasg
"""
import numpy.testing as npt
import pyaerocom as pya
from cf_units import Unit

u = Unit('kg/m2/s')
test_cases = {'kg h-1' : ['kg s-1', 1/3600]}

for unit, (to, val) in test_cases.items():

    cube = pya.helpers.make_dummy_cube_latlon()

    assert (cube.data == 1).all()
    cube.units = unit
    cube.convert_units(to)
    npt.assert_allclose(cube.data.mean(), val, rtol=1e-3)

# =============================================================================
#
# cube = pya.helpers.make_dummy_cube_latlon()
# cube.var_name = 'wetso4'
# cube.units = 'mg S m-2 h-1'
#
# data = pya.GriddedData(cube)
#
# print(data)
# =============================================================================

