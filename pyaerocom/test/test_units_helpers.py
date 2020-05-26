#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""

from pyaerocom import units_helpers as helpers
from pyaerocom.conftest import lustre_unavail, testdata_unavail
from pyaerocom.griddeddata import GriddedData
from pyaerocom.exceptions import UnitConversionError

def test_unit_conversion_fac():
    assert helpers.unit_conversion_fac('m-1', '1/Mm') == 1e6


def test_implicit_to_explicit_rates_already_rate():
    g = GriddedData()
    # Function should not convert data that is already a rate
    g.units = 's-1'
    assert g == helpers.implicit_to_explicit_rates(g, 'monthly')
    g.units = '1/s'
    assert g == helpers.implicit_to_explicit_rates(g, 'monthly')


@testdata_unavail
def test_implicit_to_explicit_rates_convert_data(data_tm5):
    # data = data_tm5
    # converted = helpers.implicit_to_explicit_rates(data, 'monthly')
    # assert isinstance(converted, GriddedData)
    # assert (data.to_xarray().values == converted.to_xarray().values).all()
    pass
