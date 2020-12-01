#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:45:43 2018

@author: jonasg
"""
import pytest
import numpy.testing as npt

from pytest import approx
from pyaerocom import units_helpers as uh
from pyaerocom.conftest import testdata_unavail
from pyaerocom import GriddedData


@pytest.mark.parametrize('from_unit,to_unit,val', [
    ('m-1', '1/Mm', 1e6),
    ('ug m-3', 'ug/m3', 1)
])
def test__unit_conversion_fac_si(from_unit, to_unit, val):
    assert uh._unit_conversion_fac_si(from_unit, to_unit) == val


@pytest.mark.parametrize('var_name,from_unit,to_unit,val', [
    ('concso2', 'ug S/m3', 'ug m-3', 1.9979),
    ('concso4', 'ug S/m3', 'ug m-3', 2.9958),
    ('concbc', 'ug C/m3', 'ug m-3', 1),
    ('concoa', 'ug C/m3', 'ug m-3', 1),
    ('concoc', 'ug C/m3', 'ug m-3', 1),
    ('wetso4', 'kg S/ha', 'kg m-2', 0.0003),
    ('concso4pr', 'mg S/L', 'g m-3', 2.995821)
])
def test__unit_conversion_fac_custom(var_name, from_unit, to_unit, val):
    to, num = uh._unit_conversion_fac_custom(var_name, from_unit)
    assert to == to_unit
    npt.assert_allclose(num,
                        val, rtol=1e-2)


@pytest.mark.parametrize('from_unit,to_unit,var_name,val', [
    ('ug m-3', 'ug/m3', None, 1),
    ('ug m-3', 'ug/m3', 'concso2', 1),
    ('mg m-3', 'ug m-3', 'concso2', 1e3),
    ('ug S/m3', 'mg m-3', 'concso2', 1.9979e-3)
])
def test_convert_unit(from_unit, to_unit, var_name, val):
    result = uh.convert_unit(1, from_unit, to_unit, var_name)
    npt.assert_allclose(result,
                        val, rtol=1e-2)


@testdata_unavail
@pytest.mark.parametrize('units', [
    's-1', '1/s'
])
def test_implicit_to_explicit_rates_already_rate(data_tm5, units):
    # Function should not convert data that is already a rate
    data = data_tm5
    data.units = units
    new_data = uh.implicit_to_explicit_rates(data, 'monthly')
    new_data_values = new_data.to_xarray().values
    data_values = data.to_xarray().values
    assert (new_data_values == data_values).all()


@testdata_unavail
def test_implicit_to_explicit_rates_convert_data(data_tm5):
    data = data_tm5
    data.units = 'kg m-2'
    new_data = uh.implicit_to_explicit_rates(data, 'monthly')
    assert isinstance(new_data, GriddedData)
    assert new_data.units == 'kg m-2 s-1'
    new_data_values = new_data.to_xarray().values
    data_values = data.to_xarray().values
    assert (new_data_values != data_values).all()
    factors = uh.seconds_in_periods(data.time_stamps(), 'monthly')
    ratio = data_values / new_data_values
    for i, factor in enumerate(factors):
        assert (ratio)[i].mean() == factor


if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
