#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Molecular masses and units (for conversion of species)
Created on Mon Sep 2 08:47:56 2019

@author: jonasg
"""
import pandas as pd
import numpy as np

from cf_units import Unit
from pyaerocom import const
from pyaerocom.helpers import seconds_in_periods
from pyaerocom.exceptions import UnitConversionError

VARS = const.VARS

# 1. DEFINITION OF ATOM and MOLECULAR MASSES

# Atoms
M_O = 15.999 # u
M_S = 32.065 # u
M_N = 14.0067 # u
M_H = 1.00784 # u

# Molecules
M_SO2 = M_S + 2 * M_O
M_SO4 = M_S + 4 * M_O

M_NO2 = M_N + 2 * M_O
M_NO3 = M_N + 3 * M_O

M_NH3 = M_N + 3 * M_H
M_NH4 = M_N + 4 * M_H


# 2.1 Other conversion factors
HA_TO_SQM = 10000   # hectar to square metre.

# 3. LOOKUP TABLE FOR CONVERSION FACTORS

# logic of hierarchy is: variable -> from unit -> to_unit -> conversion factor
UCONV_MUL_FACS = pd.DataFrame([

    ['concso4'  , 'ug S/m3'     , 'ug m-3', M_SO4 / M_S],
    ['concso2'  , 'ug S/m3'     , 'ug m-3', M_SO2 / M_S],
    ['concbc'   , 'ug C/m3'     , 'ug m-3', 1.0],
    ['concoa'   , 'ug C/m3'     , 'ug m-3', 1.0],
    ['concoc'   , 'ug C/m3'     , 'ug m-3', 1.0],
    ['conctc'   , 'ug C/m3'     , 'ug m-3', 1.0],
    ['concno3'  , 'ug N/m3'     , 'ug m-3', M_NO3 / M_N],
    ['wetso4'   , 'kg S/ha'     , 'kg m-2', M_SO4 / M_S / HA_TO_SQM],
    ['concso4pr', 'mg S/L'      , 'g m-3' , M_SO4 / M_S] # 1mg/L = 1g/m3

], columns=['var_name', 'from', 'to', 'fac']).set_index(['var_name', 'from'])

# may be used to specify alternative names for custom units  defined
# in UCONV_MUL_FACS
UALIASES = {'ug S m-3'  : 'ug S/m3',
            'ug C m-3'  : 'ug C/m3',
            'ug N m-3'  : 'ug N/m3',
            '/m'        : 'm-1',
            'mgN/m2'    : 'mg N m-2'}

def unit_conversion_fac_custom(var_name, from_unit):
    """Get custom conversion factor for a certain unit"""
    if from_unit in UALIASES:
        from_unit = UALIASES[from_unit]
    try:
        info = UCONV_MUL_FACS.loc[(var_name, str(from_unit)), :]
        if not isinstance(info, pd.Series):
            raise Exception('Could not find unique conversion factor in table '
                            'UCONV_MUL_FACS in units_helpers.py. Please check '
                            'for dulplicate entries')
    except KeyError:
        raise UnitConversionError('Failed to convert unit {} (variable {}). '
                                  'Reason: no custom conversion factor could '
                                  'be inferred from table '
                                  'pyaerocom.units_helpers.UCONV_MUL_FACS'
                                  .format(from_unit, var_name))
    return (info.to, info.fac)

def unit_conversion_fac(from_unit, to_unit):
    """Returns multiplicative unit conversion factor for input units

    Note
    ----
    Input must be either instances of :class:`cf_units.Unit` class or string.

    Parameters
    ----------
    from_unit : :obj:`cf_units.Unit`, or :obj:`str`
        unit to be converted
    to_unit : :obj:`cf_units.Unit`, or :obj:`str`
        final unit

    Returns
    --------
    float
        multiplicative conversion factor

    Raises
    ------
    ValueError
        if units cannot be converted into each other using cf_units package
    """
    if isinstance(from_unit, str):
        from_unit = Unit(from_unit)
    try:
        return from_unit.convert(1, to_unit)
    except ValueError:
        raise UnitConversionError('Failed to convert unit from {} to {}'
                                  .format(from_unit, to_unit))

def convert_unit(data, from_unit, to_unit, var_name=None):
    """Convert unit of data

    Parameters
    ----------
    data : np.ndarray or similar
        input data
    from_unit : cf_units.Unit or str
        current unit of input data
    to_unit : cf_units.Unit or str
        new unit of input data
    var_name : str, optional
        name of variable. If provided, method
        :func:`unit_conversion_fac_custom` is called before the standard unit
        conversion is applied. That requires that `var_name` is specified in
        :attr:`pyaerocom.molmasses.CONV_MUL_FACS`.

    Returns
    -------
    data
        data in new unit
    """
    if isinstance(from_unit, str):
        from_unit = Unit(from_unit)
    if isinstance(to_unit, str):
        to_unit = Unit(to_unit)
    if from_unit == to_unit:
        # nothing to do
        return data
    if var_name in UCONV_MUL_FACS.index:
        try:
            from_unit, pre_conv_fac = unit_conversion_fac_custom(var_name,
                                                                 from_unit)
            data *= pre_conv_fac
        except UnitConversionError:
            # from_unit is likely not custom but standard... and if not
            # call of unit_conversion_fac below will crash
            pass

    conv_fac = unit_conversion_fac(from_unit, to_unit)
    if conv_fac != 1:
        data *= conv_fac
    return data

def convert_unit_back(data, from_unit, to_unit, var_name=None):
    """Convert unit of data

    Parameters
    ----------
    data : np.ndarray or similar
        input data
    from_unit : cf_units.Unit or str
        current unit of input data
    to_unit : cf_units.Unit or str
        new unit of input data
    var_name : str, optional
        name of variable. If provided, method
        :func:`unit_conversion_fac_custom` is called before the standard unit
        conversion is applied. That requires that `var_name` is specified in
        :attr:`pyaerocom.molmasses.CONV_MUL_FACS`.

    Returns
    -------
    data
        data in new unit

    """
    if var_name in UCONV_MUL_FACS.index:
        from_unit, pre_conv_fac = unit_conversion_fac_custom(var_name,
                                                             to_unit)
        data = np.divide(data, pre_conv_fac)

    conv_fac = unit_conversion_fac(to_unit, from_unit)
    if conv_fac != 1:
        data = np.divide(data, conv_fac)
    return data

def implicit_to_explicit_rates(gridded, ts_type):
    """
    Convert implicitly defined daily, monthly or yearly rates to
    per second. Update units and values accordingly.
    Some data should be per second but have units without time information
    information.
    Parameters
    ----------
    gridded : GriddedData
        Data to convert
    ts_type : str
        Temporal resolution of gridded.
    Returns
    -------
    GriddedData
        Modified data, if not already a rate.
    """
    from pyaerocom import GriddedData

    unit = gridded.units
    unit_string = str(unit)
    is_rate = ('/s' in unit_string) or ('s-1' in unit_string)
    if is_rate:
        return gridded
    else:
        seconds_factor = seconds_in_periods(gridded.time_stamps(), ts_type)
        data = gridded.to_xarray()
        mult_fac = np.ones_like(data)
        for i in range(len(seconds_factor)):
            mult_fac[i] *= seconds_factor[i]
        result = data / mult_fac
        cube = result.to_iris()
        new_gridded = GriddedData()
        new_gridded.grid = cube
        new_gridded.units = '{} s-1'.format(gridded.units) # append rate to format
    return new_gridded

if __name__ == '__main__':

    import cf_units as cfu

    unit = cfu.Unit('ug m-3')
