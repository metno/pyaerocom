#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Molecular masses and units (for conversion of species)

Created on Mon Sep  2 08:47:56 2019

@author: jonasg
"""
import pandas as pd
import cf_units
from pyaerocom.helpers import TS_TYPE_SECS

# 1. DEFINITION OF MOLAR MASSES


# Atoms
M_O = 15.999 # g/mol
M_S = 32.065 # g/mol

# Molecules

M_SO4 = M_S + 4*M_O
M_SO2 = M_S + 2*M_O

# 2. DEFINITION OF CONVERSION FACTORS FOR CERTAIN SPECIES
UCONV_FAC_S_SO4 = M_SO4 / M_S
UCONV_FAC_S_SO2 = M_SO2 / M_S

# 2.1 Other conversion factors
HA_TO_SQM = 10000   # hectar to square metre.

# 3. LOOKUP TABLE FOR CONVERSION FACTORS

# logic of hierarchy is: variable -> from unit -> to_unit -> conversion factor
UCONV_MUL_FACS = pd.DataFrame([
        
  ['concso4', 'ug S/m3', 'ug m-3',  UCONV_FAC_S_SO4],
  ['concso2', 'ug S/m3', 'ug m-3',  UCONV_FAC_S_SO2],
  
  ['concbc', 'ug C/m3', 'ug m-3', 1.0],
  ['concoa', 'ug C/m3', 'ug m-3', 1.0],
  ['concoc', 'ug C/m3', 'ug m-3', 1.0],
  ['conctc', 'ug C/m3', 'ug m-3', 1.0],
  
  ['wetso4', 'kg S/ha', 'kg m-2',  UCONV_FAC_S_SO4 / HA_TO_SQM],
  ['concso4pr', 'mg S/L', 'g m-3',  UCONV_FAC_S_SO4] # 1mg/L = 1g/m3

], columns=['var_name', 'from', 'to', 'fac']).set_index(['var_name', 'from'])

# may be used to specify alternative names for custom units  defined 
# in UCONV_MUL_FACS
UALIASES = {'ug S m-3' : 'ug S/m3',
            'ug C m-3' : 'ug C/m3'}
# =============================================================================
#     
# if sum(CONV_MUL_FACS.index.duplicated()) > 0:
#     raise ValueError('Each unit can only be defined once')
# =============================================================================

def unit_conversion_fac_custom(var_name, from_unit):
    """Get custom conversion factor for a certain unit"""
    if from_unit in UALIASES:
        from_unit = UALIASES[from_unit]
    try:
        info = UCONV_MUL_FACS.loc[(var_name, from_unit), :]
        if not isinstance(info, pd.Series):
            raise Exception('Could not find unique conversion factor in table '
                            'UCONV_MUL_FACS in units_helpers.py. Please check '
                            'for dulplicate entries')
    except KeyError:
        from pyaerocom.exceptions import UnitConversionError
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
        from_unit = cf_units.Unit(from_unit)
    try:
        return from_unit.convert(1, to_unit)    
    except ValueError:
        from pyaerocom.exceptions import UnitConversionError
        raise UnitConversionError('Failed to convert unit from {} to {}'
                                  .format(from_unit, to_unit))

# keep 
def get_tot_number_of_seconds(ts_type, dtime = None):
    from pyaerocom.tstype import TsType
    ts_tpe = TsType(ts_type)
    
    if ts_tpe >= TsType('montly'):
        if dtime is None:
            raise AttributeError('For frequncies larger than or eq. monthly you'+
                                 'need to provide dtime in order to compute the number of second.  ')
        else:
            # find seconds from dtime 
            return None
    else:
        return TS_TYPE_SECS[ts_type]

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
    if var_name in UCONV_MUL_FACS.index:
        from_unit, pre_conv_fac = unit_conversion_fac_custom(var_name, 
                                                             from_unit)
        data *= pre_conv_fac
    
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

if __name__ == '__main__':
    df = UCONV_MUL_FACS
    print(df)
    import numpy as np
    
    print(convert_unit(np.ones(3), 'ug S/m3', 'ug m-3', 'concso4'))
    
    data = np.ones(10)

    unit = 'kg S/ha'
    var_name = 'wetso4'
    print(unit_conversion_fac_custom(var_name, unit))

    print(convert_unit(data, unit, 'kg m-2', var_name))