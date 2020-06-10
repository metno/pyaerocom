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

# @testdata_unavail
# @pytest.mark.parametrize('units', [
#     's-1','1/s'
#     ])
# def test_implicit_to_explicit_rates_already_rate(data_tm5, units):
#     # Function should not convert data that is already a rate
#     data = data_tm5
#     data.units = units
#     assert data == helpers.implicit_to_explicit_rates(data, 'monthly')


@testdata_unavail
def test_implicit_to_explicit_rates_convert_data(data_tm5):
    data = data_tm5
    data.units = 'kg/m2'
    data_values = data.to_xarray().values
    helpers.implicit_to_explicit_rates(data, 'monthly')
#    assert isinstance(converted, GriddedData)
    assert data.units == 'kg/m2 s-1'
    assert (data_values != data.to_xarray().values).all()

if __name__=='__main__':
    import sys
    pytest.main(sys.argv)
