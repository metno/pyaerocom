#!/usr/bin/env python3
# -*- coding: utf-8 -*-

VAR_PREFIXES = ['vmr', 'mmr', 'conc', 'sconc', 'wet', 'dry']

# in g/mol
MOLMASSES = {'air_dry'  : 28.9647,
             'o3'       : 48,
             'so2'      : 64.066,
             'so4'      : 96.06,
             'no'       : 30.01,
             'no2'      : 46.0055,
             'hno3'     : 63.01,
             'nh3'      : 17.031,
             'co'       : 28.010}

class UnkownSpeciesError(ValueError):
    pass

def get_species(var_name):
    """
    Get species name from variable name

    Parameters
    ----------
    var_name : str
        pyaerocom variable name (cf. variables.ini)

    Raises
    ------
    UnkownSpeciesError
        if species cannot be inferred

    Returns
    -------
    str
        name of species

    """
    if var_name in MOLMASSES:
        return var_name
    for prefix in VAR_PREFIXES:
        if var_name.startswith(prefix):
            species = var_name.split(prefix)[-1]
            if species in MOLMASSES:
                return species
    raise UnkownSpeciesError('Could not infer atom / molecule/ species from '
                             'var_name {}'.format(var_name))

def get_molmass(var_name):
    """
    Get molar mass for input variable

    Parameters
    ----------
    var_name : str
        pyaerocom variable name (cf. variables.ini) or name of species

    Returns
    -------
    float
        molar mass of species in units of g/mol

    """
    return MOLMASSES[get_species(var_name)]

def get_mmr_to_vmr_fac(var_name):
    """
    Get conversion factor for MMR -> VMR conversion for input variable

    Note
    ----
    Assumes dry air molar mass

    Parameters
    ----------
    var_name : str
        Name of variable to be converted

    Returns
    -------
    float
        multiplication factor to convert MMR -> VMR

    """
    return get_molmass('air_dry') / get_molmass(var_name)
