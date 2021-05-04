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
from pyaerocom.helpers import (isnumeric,
                               resample_time_dataarray,
                               seconds_in_periods)

from pyaerocom.time_config import SI_TO_TS_TYPE
from pyaerocom.tstype import TsType
from pyaerocom.exceptions import UnitConversionError

VARS = const.VARS

RATES_FREQ_DEFAULT = 'd'

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


# Unit conversion and custom units definitions

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
    ['concno2'  , 'ug N/m3'     , 'ug m-3', M_NO2 / M_N],
    ['concno3'  , 'ug N/m3'     , 'ug m-3', M_NO3 / M_N],
    ['concnh4'  , 'ug N/m3'     , 'ug m-3', M_NH4 / M_N],
    ['wetso4'   , 'kg S/ha'     , 'kg m-2', M_SO4 / M_S / HA_TO_SQM],
    ['concso4pr', 'mg S/L'      , 'g m-3' , M_SO4 / M_S] # 1mg/L = 1g/m3

], columns=['var_name', 'from', 'to', 'fac']).set_index(['var_name', 'from'])


# may be used to specify alternative names for custom units  defined
# in UCONV_MUL_FACS
UALIASES = {
    # mass concentrations
    'ug S m-3'      : 'ug S/m3',
    'ug C m-3'      : 'ug C/m3',
    'ug N m-3'      : 'ug N/m3',
    # deposition rates (implicit)
    ## sulphur species
    'mgS/m2'        : 'mg S m-2',
    'mgSm-2'        : 'mg S m-2',
    ## nitrogen species
    'mgN/m2'        : 'mg N m-2',
    'mgNm-2'        : 'mg N m-2',
    # deposition rates (explicit)
    ## sulphur species
    'mgS/m2/h'      : 'mg S m-2 h-1',
    'mgS/m**2/h'    : 'mg S m-2 h-1',
    'mgSm-2h-1'     : 'mg S m-2 h-1',
    'mgSm**-2h-1'   : 'mg S m-2 h-1',
    'mgS/m2/d'      : 'mg S m-2 d-1',
    ## nitrogen species
    'mgN/m2/h'      : 'mg N m-2 h-1',
    'mgN/m**2/h'    : 'mg N m-2 h-1',
    'mgNm-2h-1'     : 'mg N m-2 h-1',
    'mgNm**-2h-1'   : 'mg N m-2 h-1',
    'mgN/m2/d'      : 'mg N m-2 d-1',
    ## others
    'MM/H'          : 'mm h-1',
    # others
    '/m'            : 'm-1'
    }

DEP_IMPLICIT_UNITS = [Unit('mg N m-2'),
                      Unit('mg S m-2'),
                      Unit('mg m-2')]

PR_IMPLICIT_UNITS = [Unit('mm')]

DEP_TEST_UNIT = 'kg m-2 s-1'
DEP_TEST_NONSI_ATOMS = ['N', 'S']

def _unit_conversion_fac_custom(var_name, from_unit):
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

def _unit_conversion_fac_si(from_unit, to_unit):
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

def get_unit_conversion_fac(from_unit, to_unit, var_name=None):

    pre_conv_fac = 1
    if from_unit == to_unit:
        # nothing to do
        return 1
    elif var_name is not None and var_name in UCONV_MUL_FACS.index:
        try:
            from_unit, pre_conv_fac = _unit_conversion_fac_custom(var_name,
                                                                  from_unit)
        except UnitConversionError:
            # from_unit is likely not custom but standard... and if not
            # call of unit_conversion_fac below will crash
            pass

    return _unit_conversion_fac_si(from_unit, to_unit) * pre_conv_fac

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
        :func:`_unit_conversion_fac_custom` is called before the standard unit
        conversion is applied. That requires that `var_name` is specified in
        :attr:`pyaerocom.molmasses.CONV_MUL_FACS`.

    Returns
    -------
    data
        data in new unit
    """
    conv_fac = get_unit_conversion_fac(from_unit, to_unit, var_name)
    if conv_fac != 1:
        data *= conv_fac
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

def _check_unit_conversion_fac(unit, test_unit, non_si_info=None):
    if non_si_info is None:
        non_si_info = []
    try:
        get_unit_conversion_fac(unit, DEP_TEST_UNIT)
        return True
    except UnitConversionError:
        for substr in non_si_info:
            if substr in unit:
                check = unit.replace(substr, '')
                return _check_unit_conversion_fac(check, test_unit)
    return False

def check_rate_units_implicit(unit, ts_type):

    unit = Unit(unit)

    freq = TsType(ts_type)
    freq_si = freq.to_si()

    # check if unit is implicit and change if possible
    found = False
    for imp_unit in DEP_IMPLICIT_UNITS:
        if unit == imp_unit:
            unit = f'{imp_unit} {freq_si}-1'
            found=True
            break

    if not found and not _check_unit_conversion_fac(unit=str(unit),
                                          test_unit=DEP_TEST_UNIT,
                                          non_si_info=DEP_TEST_NONSI_ATOMS):
            raise ValueError(f'Cannot handle wet deposition unit {unit}')

    # Check if frequency in unit corresponds to sampling frequency (e.g.
    # ug m-2 h-1 for hourly data).
    freq_si_str = f'{freq_si}-1'
    freq_si_str_alt = f'/{freq_si}'
    if freq_si_str_alt in str(unit):

        # make sure frequencey is denoted as e.g. m s-1 instead of m/s
        unit = Unit(str(unit).replace(freq_si_str_alt,
                                      freq_si_str))


    # for now, raise NotImplementedError if wdep unit is, e.g. ug m-2 s-1 but
    # ts_type is hourly (later, use units_helpers.implicit_to_explicit_rates)
    if not freq_si_str in str(unit):
        raise NotImplementedError(f'Cannot yet handle wdep in {unit} but '
                                  f'{freq} sampling frequency')
    return unit

def check_pr_units(gridded):
    #ToDo: harmonise input and output with check_rate_units_implicit
    unit = Unit(gridded.units)
    freq = TsType(gridded.ts_type)
    freq_si = freq.to_si()

    # check if precip unit is implicit
    if any([unit == x for x in PR_IMPLICIT_UNITS]):
        unit = f'{unit} {freq_si}-1'
        gridded.units = unit

    # Check if frequency in unit corresponds to sampling frequency (e.g.
    # ug m-2 h-1 for hourly data).
    freq_si_str = f' {freq_si}-1'
    freq_si_str_alt = f'/{freq_si}'
    if freq_si_str_alt in str(unit):
        # make sure frequencey is denoted as e.g. m s-1 instead of m/s
        unit = str(unit).replace(freq_si_str_alt,
                                 freq_si_str)

        gridded.units = unit

    # for now, raise NotImplementedError if wdep unit is, e.g. ug m-2 s-1 but
    # ts_type is hourly (later, use units_helpers.implicit_to_explicit_rates)
    if not freq_si_str in str(unit):
        raise NotImplementedError(f'Cannot yet handle wdep in {unit} but '
                                  f'{freq} sampling frequency')
    return gridded

def _check_prlim_units(prlim, prlim_units):
    # ToDo: cumbersome for now, make it work first, then make it simpler...
    if not prlim_units.endswith('-1'):
        raise ValueError('Please specify prlim_unit as string ending with '
                         '-1 (e.g. mm h-1) or similar')

    spl = prlim_units.split()
    if not len(spl) == 2:
        raise ValueError('Invalid input for prlim_units (only one whitespace '
                         'is allowed)')
    # make sure to be in the correct length unit
    mulfac = get_unit_conversion_fac(spl[0], 'm')
    prlim *= mulfac

    prlim_units = f'm {spl[1]}'
    prlim_freq = spl[1][:-2] # it endswith -1
    # convert the freque
    if not prlim_freq in SI_TO_TS_TYPE:
        raise ValueError(
            f'frequency in prlim_units must be either of the '
            f'following values: {list(SI_TO_TS_TYPE.keys())}.')

    prlim_tstype = TsType(SI_TO_TS_TYPE[prlim_freq])
    return (prlim, prlim_units, prlim_tstype)

def _apply_prlim_wdep(wdeparr, prarr, prlim, prlim_unit, prlim_set_under):
    if prlim_unit is None:
        raise ValueError(f'Please provide prlim_unit for prlim={prlim}')
    elif prlim_set_under is None:
        raise ValueError(f'Please provide prlim_set_under for prlim={prlim}')
    elif not isnumeric(prlim_set_under):
        raise ValueError(f'Please provide a numerical value or np.nan for '
                         f'prlim_set_under, got {prlim_set_under}')

    prmask = prarr.data < prlim
    wdeparr.data[prmask] = prlim_set_under

    return wdeparr, prmask

def _aggregate_wdep_pr(wdeparr, prarr, wdep_unit, pr_unit, from_tstype,
                       to_tstype):
    to_tstype_pd = to_tstype.to_pandas_freq()
    to_tstype_si = to_tstype.to_si()

    from_tstype_si = from_tstype.to_si()

    wdeparr = resample_time_dataarray(wdeparr,
                                      to_tstype_pd,
                                      how='sum')
    wdep_unit = wdep_unit.replace(f'{from_tstype_si}-1',
                                  f'{to_tstype_si}-1')
    prarr = resample_time_dataarray(prarr,
                                    to_tstype_pd,
                                    how='sum')
    pr_unit = pr_unit.replace(f'{from_tstype_si}-1',
                              f'{to_tstype_si}-1')

    return (wdeparr, prarr, wdep_unit, pr_unit)

def compute_concprcp_from_pr_and_wetdep(wdep, pr, ts_type=None,
                                        prlim=None, prlim_units=None,
                                        prlim_set_under=None):

    if ts_type is None:
        ts_type = wdep.ts_type

    wdep_tstype = TsType(wdep.ts_type)

    # get units from deposition input and precipitation; sometimes, they are
    # defined implicit, e.g. mm for precipitation, which is then already
    # accumulated over the provided time resolution in the data, that is, if
    # the data is hourly and precip is in units of mm, then it means the the
    # unit is mm/h. In addition, wet deposition units may be in mass of main
    # atom (e.g. N, or S) which are not SI and thus, not handled properly by
    # CF units.
    wdep_unit = str(wdep.units)

    wdep = check_rate_units_implicit(wdep_unit,
                                     wdep_tstype)
    pr = check_pr_units(pr)




    # repeat the unit check steps done for wet deposition
    pr_unit = str(pr.units)
    pr_tstype = TsType(pr.ts_type)

    if not wdep_tstype == pr_tstype:
        # ToDo: this can probably fixed via time resampling with how='sum'
        # for the higher resolution dataset, but for this first draft, this
        # is not allowed.
        raise ValueError('Input precipitation and wetdeposition fields '
                         'need to be in the same frequency...')

    # assign input frequency (just for making the code better readable)
    from_tstype = wdep_tstype
    from_tstype_si = from_tstype.to_si()

    # convert data objects to xarray to do modifications and computation of
    # output variable
    prarr = pr.to_xarray()
    wdeparr = wdep.to_xarray()

    # Make sure precip unit is correct for concprcp=wdep/pr
    pr_unit_calc = f'm {from_tstype_si}-1'

    # unit conversion factor for precip
    mulfac_pr = get_unit_conversion_fac(pr_unit, pr_unit_calc)

    if mulfac_pr != 1:
        prarr *= mulfac_pr
        pr_unit = pr_unit_calc

    # Make sure wdep unit is correct for concprcp=wdep/pr
    wdep_unit_check_calc = wdep_unit.replace('N', '').replace('S', '')
    wdep_unit_calc = f'ug m-2 {from_tstype_si}-1'
    mulfac_wdep = get_unit_conversion_fac(wdep_unit_check_calc, wdep_unit_calc)

    if mulfac_wdep != 1:
        wdeparr *= mulfac_wdep
        if 'N' in wdep_unit:
            wdep_unit_calc = wdep_unit_calc.replace('ug', 'ug N')
        elif 'S' in wdep_unit:
            wdep_unit_calc = wdep_unit_calc.replace('ug', 'ug S')
        wdep_unit = wdep_unit_calc

    # final output frequency (precip limit may be applied in higher resolution)
    to_tstype = TsType(ts_type)
    to_tstype_si = to_tstype.to_si()

    # apply prlim filter if applicable
    apply_prlim, prlim_applied = False, False
    if prlim is not None:
        apply_prlim = True

        prlim, prlim_units, prlim_tstype=_check_prlim_units(prlim, prlim_units)

        if prlim_tstype == from_tstype:
            wdeparr,_ = _apply_prlim_wdep(wdeparr, prarr, prlim, prlim_units,
                                          prlim_set_under)
            prlim_applied = True

    if apply_prlim and not prlim_applied and prlim_tstype > to_tstype:
        # intermediate frequency where precip filter should be applied
        (wdeparr,
         prarr,
         wdep_unit,
         pr_unit) = _aggregate_wdep_pr(wdeparr, prarr, wdep_unit, pr_unit,
                                       from_tstype, prlim_tstype)

        wdeparr,_ = _apply_prlim_wdep(wdeparr, prarr, prlim, prlim_units,
                                      prlim_set_under)
        prlim_applied = True
        from_tstype = prlim_tstype

    if not from_tstype == to_tstype:
        (wdeparr,
         prarr,
         wdep_unit,
         pr_unit) = _aggregate_wdep_pr(wdeparr, prarr, wdep_unit, pr_unit,
                                       from_tstype, to_tstype)

    if apply_prlim and not prlim_applied:
        if not to_tstype == prlim_tstype:
            raise ValueError('... ... .. ')
        wdeparr,_ = _apply_prlim_wdep(wdeparr, prarr,
                                      prlim, prlim_units,
                                      prlim_set_under)

    # set PR=0 to NaN (as we divide py PR)
    prarr.data[prarr.data==0] = np.nan

    concprcparr = wdeparr / prarr

    cube = concprcparr.to_iris()
    # infer output unit of concentration variable (should be ug m-3 or ug N m-3 or ug S m-3)
    conc_unit_out = wdep_unit.replace('m-2', 'm-3').replace(f'{to_tstype_si}-1', '').strip()
    cube.units = conc_unit_out
    cube.attributes['ts_type'] = str(to_tstype)
    return cube

if __name__ == '__main__':

    import cf_units as cfu

    unit = cfu.Unit('ug m-3')
