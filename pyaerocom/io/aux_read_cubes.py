#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Config file for AeroCom PhaseIII test project
"""


import iris
import numpy as np

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
    except:
        from pyaerocom.exceptions import UnitConversionError
        raise UnitConversionError('Failed to harmonise units')

def add_cubes(gridded1, gridded2):
    """Method to add cubes from 2 gridded data objects
    """
    cube1, cube2 = _check_input_iscube(gridded1, gridded2)
    cube1, cube2 = _check_same_units(cube1, cube2)    
    return  cube1 + cube2

def subtract_cubes(gridded1, gridded2):
    """Method to subtract 1 cube from another"""
    cube1, cube2 = _check_input_iscube(gridded1, gridded2)
    cube1, cube2 = _check_same_units(cube1, cube2)    
    return  cube1 - cube2

def compute_angstrom_coeff_cubes(od1, od2, lambda1=None, lambda2=None):
    """Compute Angstrom coefficient cube based on 2 optical densitiy cubes
    
    Parameters
    ----------
    od1 : iris.cube.Cube
        AOD at wavelength 1
    od2 : iris.cube.Cube
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
    from pyaerocom import GriddedData
    from pyaerocom.variable import VarNameInfo
    from cf_units import Unit
    if isinstance(od1, GriddedData):
        od1 = od1.grid
    if isinstance(od2, GriddedData):
        od2 = od2.grid
    if lambda1 is None:
        lambda1 = VarNameInfo(od1.var_name).wavelength_nm
    if lambda2 is None:
        lambda2 = VarNameInfo(od2.var_name).wavelength_nm
    
    if not od1.shape == od2.shape:
        raise ValueError('Input grids do not have the same shape')
    
    logr = iris.analysis.maths.log(od1 / od2)
    
    wvl_r = np.log(lambda1 / lambda2)
    ang = -1*iris.analysis.maths.divide(logr, wvl_r)
    ang.units = Unit(1)
    return ang