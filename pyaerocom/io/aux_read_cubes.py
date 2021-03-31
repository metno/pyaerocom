#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import iris
import numpy as np
from traceback import format_exc
from pyaerocom import print_log
from pyaerocom._lowlevel_helpers import merge_dicts
from pyaerocom.helpers import copy_coords_cube
from pyaerocom.molmasses import get_molmass
from pyaerocom.units_helpers import get_unit_conversion_fac
from pyaerocom.molmasses import get_mmr_to_vmr_fac


CUBE_MATHS = {'add'         :   iris.analysis.maths.add,
              'subtract'    :   iris.analysis.maths.subtract,
              'divide'      :   iris.analysis.maths.divide,
              'multiply'    :   iris.analysis.maths.multiply}

def _apply_operator_cubes(cube1, cube2, operator_name,
                          allow_coord_merge=True):
    if not operator_name in CUBE_MATHS:
        raise NotImplementedError('No such arithmetic cube operator '
                                  'implemented: {}'.format(operator_name))
    fun = CUBE_MATHS[operator_name]
    try:
        return fun(cube1, cube2)
    except ValueError as e:
        print_log.warning('Could not {} cubes straight out of the box. Trying '
                          'to correct for dimension definition errors'
                          .format(operator_name))
        if 'differing coordinates (time)' in repr(e):
            iris.util.unify_time_units([cube1, cube2])
            attrs = {}
            attrs.update(cube1.coord('time').attributes)
            attrs.update(cube2.coord('time').attributes)
            cube2.coord('time').attributes = attrs
            cube1.coord('time').attributes = attrs

        elif allow_coord_merge:
            copy_coords_cube(to_cube=cube2,
                             from_cube=cube1,
                             inplace=True)
    return fun(cube1, cube2)

def _check_input_iscube(*data_objs):
    from pyaerocom.griddeddata import GriddedData
    checked = []
    for obj in data_objs:
        if isinstance(obj, GriddedData):
            checked.append(obj.cube)
        elif isinstance(obj, iris.cube.Cube):
            checked.append(obj)
        else:
            raise ValueError('Invalid input: require GriddedData or Cube, got '
                             '{}'.format(type(obj)))
    return checked

def _check_same_units(cube1, cube2):
    if cube1.units == cube2.units:
        return (cube1, cube2)
    from pyaerocom import const
    var1 = cube1.var_name
    u1 = cube1.units

    var2 = cube2.var_name
    u2 = cube2.units

    if var1 in const.VARS and u1 == const.VARS[var1]['units'] :
        cube2.convert_units(u1)
        return (cube1, cube2)
    elif var2 in const.VARS and u2 == const.VARS[var2]['units'] :
        cube1.convert_units(u2)
        return (cube1, cube2)

    try:
        cube2.convert_units(u1)
        return (cube1, cube2)
    except Exception:
        from pyaerocom.exceptions import UnitConversionError
        raise UnitConversionError('Failed to harmonise units')

def merge_meta_cubes(cube1, cube2):
    try:
        return merge_dicts(cube1.attributes,
                           cube2.attributes)
    except Exception:
        print_log.warning('WARNING: Failed to merge Cube metadata. Reason:\n{}'
                          .format(format_exc()))
        ts_type = None
        try:
            if cube1.attributes['ts_type']==cube2.attributes['ts_type']:
                ts_type = cube1.attributes['ts_type']
        except:
            pass

        return {'NOTE'      : 'METADATA_MERGE_FAILED',
                'meta1'     : cube1.attributes,
                'meta2'     : cube2.attributes,
                'ts_type'   : ts_type}

def apply_rh_thresh_cubes(cube, rh_cube, rh_max=None):
    """Method that applies a low RH filter to input cube"""
    cube, rh_cube =  _check_input_iscube(cube, rh_cube)
    if rh_max is None:
        from pyaerocom import const
        rh_max = const.VARS[cube.var_name]['dry_rh_max']
    if not cube.shape == rh_cube.shape:
        raise ValueError
    mask = rh_cube.data > rh_max
    cube_out = cube.copy()
    cube_out.data[mask] = np.nan
    cube_out.attributes.update(cube.attributes)
    cube_out.attributes['rh_max'] = rh_max
    return cube_out

def add_cubes(cube1, cube2):
    """Method to add cubes from 2 gridded data objects
    """
    cube1, cube2 = _check_input_iscube(cube1, cube2)
    cube1, cube2 = _check_same_units(cube1, cube2)

    cube_out = _apply_operator_cubes(cube1, cube2, 'add',
                                     allow_coord_merge=True)

    cube_out.attributes.update(merge_meta_cubes(cube1, cube2))
    return cube_out

def subtract_cubes(cube1, cube2):
    """Method to subtract 1 cube from another"""
    cube1, cube2 = _check_input_iscube(cube1, cube2)
    cube1, cube2 = _check_same_units(cube1, cube2)

    cube_out = _apply_operator_cubes(cube1, cube2, 'subtract',
                                     allow_coord_merge=True)

    cube_out.attributes.update(merge_meta_cubes(cube1, cube2))
    return cube_out

def multiply_cubes(cube1, cube2):
    """Method to multiply 2 cubes"""
    cube1, cube2 = _check_input_iscube(cube1, cube2)
    cube_out = _apply_operator_cubes(cube1, cube2, 'multiply',
                                     allow_coord_merge=True)

    cube_out.attributes.update(merge_meta_cubes(cube1, cube2))
    return cube_out

def divide_cubes(cube1, cube2):
    """Method to divide 2 cubes with each other"""
    cube1, cube2 = _check_input_iscube(cube1, cube2)
    cube_out = _apply_operator_cubes(cube1, cube2, 'divide',
                                     allow_coord_merge=True)

    cube_out.attributes.update(merge_meta_cubes(cube1, cube2))
    return cube_out

def lifetime_from_load_and_dep(load, wetdep, drydep):
    """Compute lifetime from load and wet and dry deposition"""
    raise NotImplementedError('Lifetime cannot be computed based on '
                              'grid data')
    load, wetdep, drydep = _check_input_iscube(load, wetdep, drydep)
    deptot = _apply_operator_cubes(wetdep, drydep, 'add',
                                   allow_coord_merge=True)

    deptot.attributes.update(merge_meta_cubes(wetdep, drydep))

    cube_out = _apply_operator_cubes(load, deptot, 'divide',
                                     allow_coord_merge=True)
    cube_out.attributes.update(merge_meta_cubes(load, deptot))
    return cube_out

def compute_angstrom_coeff_cubes(cube1, cube2, lambda1=None, lambda2=None):
    """Compute Angstrom coefficient cube based on 2 optical densitiy cubes

    Parameters
    ----------
    cube1 : iris.cube.Cube
        AOD at wavelength 1
    cube2 : iris.cube.Cube
        AOD at wavelength 2
    lambda1 : float
        wavelength 1
    lambda 2 : float
        wavelength 2

    Returns
    -------
    Cube
        Cube containing Angstrom exponent(s)
    """
    from pyaerocom.variable import VarNameInfo
    from cf_units import Unit
    cube1, cube2 = _check_input_iscube(cube1, cube2)
    if lambda1 is None:
        lambda1 = VarNameInfo(cube1.var_name).wavelength_nm
    if lambda2 is None:
        lambda2 = VarNameInfo(cube2.var_name).wavelength_nm

    ratio = _apply_operator_cubes(cube1, cube2, 'divide')
    logr = iris.analysis.maths.log(ratio)

    wvl_r = np.log(lambda1 / lambda2)
    cube_out = -1*iris.analysis.maths.divide(logr, wvl_r)
    cube_out.units = Unit('1')
    cube_out.attributes.update(merge_meta_cubes(cube1, cube2))
    return cube_out


def rho_from_ts_ps(ts, ps):
    R = 287.058 #R for dry air

    rho = R*divide_cubes(ts,ps)

    rho.attributes.update(merge_meta_cubes(ts, ps))

    return rho

def mmr_from_vmr(cube):
    """
    Convvert gas volume/mole mixing ratios into mass mixing ratios.

    Parameters
    ----------
    cube : iris.cube.Cube
        A cube containing gas vmr data to be converted into mmr.

    Returns
    -------
    cube_out : iris.cube.Cube
        Cube containing mmr data.

    """
    cube = _check_input_iscube(cube)[0]

    var_name = cube.var_name
    M_dry_air = get_molmass('air_dry')
    M_variable = get_molmass(var_name)

    cube_out = (M_variable/M_dry_air)*cube
    return cube_out

def conc_from_vmr(cube, ts, ps):
    cube,ts,ps = _check_input_iscube(cube,ts,ps)

    mmr_cube = mmr_from_vmr(cube)
    rho = rho_from_ts_ps(ts, ps)

    cube_out = multiply_cubes(mmr_cube,rho)

    return cube_out

def conc_from_vmr_STP(cube,):
    cube = _check_input_iscube(cube)[0]

    R = 287.058 #R for dry air

    standard_T = 293
    standard_P = 101300


    mmr_cube = mmr_from_vmr(cube)
    rho = R*standard_T/standard_P

    cube_out = rho*mmr_cube

    return cube_out


def mmr_to_vmr_cube(data):
    """
    Convert cube containing MMR data to VMR

    Parameters
    ----------
    data : iris.Cube or GriddedData
        input data object containing MMR data for a certain variable. Needs
        to have `var_name` attr. assigned and valid MMR AeroCom variable name
        (e.g. mmro3, mmrno2)

    Raises
    ------
    AttributeError
        if attr. `var_name` of input data does not start with mmr

    Returns
    -------
    iris.Cube
        cube containing mixing ratios expressed as VMR in units of nmole mole-1

    """
    from pyaerocom import GriddedData
    var = data.var_name
    if not var.startswith('mmr'):
        raise AttributeError(
            f'MMR to VMR can only be done for MMR variables (which must start '
            f'with mmr, however, the var_name of the input data is {var}')

    # make sure mmr is in correct units (the function will crash if not)
    get_unit_conversion_fac(data.units, 'kg kg-1')
    if isinstance(data, GriddedData):
        data = data.cube

    vmrvar = var.replace('mmr', 'vmr')

    mulfac = get_mmr_to_vmr_fac(var) * 1e9 # 1e9 is to go to nmole mole-1

    cube = data * mulfac
    cube.attributes.update(data.attributes)
    cube.units = 'nmole mole-1'
    cube.var_name = vmrvar
    return cube

