#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""

import pytest

from pyaerocom import units_helpers as helpers
from pyaerocom.conftest import lustre_unavail, testdata_unavail
from pyaerocom.griddeddata import GriddedData
from pyaerocom.exceptions import UnitConversionError

def test_unit_conversion_fac():
    assert helpers.unit_conversion_fac('m-1', '1/Mm') == 1e6

@testdata_unavail
@pytest.mark.parametrize('units', [
    's-1','1/s'
    ])
def test_implicit_to_explicit_rates_already_rate(data_tm5, units):
    # Function should not convert data that is already a rate
    data = data_tm5
    data.units = units
    new_data = helpers.implicit_to_explicit_rates(data, 'monthly')
    new_data_values = new_data.to_xarray().values
    data_values = data.to_xarray().values
    assert (new_data_values == data_values).all()


@testdata_unavail
def test_implicit_to_explicit_rates_convert_data(data_tm5):
    data = data_tm5
    data.units = 'kg m-2'
    new_data = helpers.implicit_to_explicit_rates(data, 'monthly')
    assert isinstance(new_data, GriddedData)
    assert new_data.units == 'kg m-2 s-1'
    new_data_values = new_data.to_xarray().values
    data_values = data.to_xarray().values
    assert (new_data_values != data_values).all()

if __name__=='__main__':
    import sys
    pytest.main(sys.argv)
