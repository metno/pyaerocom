#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mathematical low level utility methods ofcd pyaerocom
"""

import numpy as np

def compute_angstrom_coeff(aod1, aod2, lambda1, lambda2):
    """Compute Angstrom coefficient based on 2 optical densities
    
    Parameters
    ----------
    aod1 : float
        AOD at wavelength 1
    aod2 : float
        AOD at wavelength 2
    lambda1 : float
        wavelength 1
    lambda 2 : float
        wavelength 2
        
    Returns
    -------
    float
        Angstrom exponent
    """
    return -np.log(aod1 / aod2) / np.log(lambda1 / lambda2)

def compute_aod_from_angstromexp(to_lambda, aod_ref, lambda_ref, angstrom_coeff):
    """Compute AOD at specified wavelength 
    
    Uses Angstrom coefficient and reference AOD to compute the 
    corresponding wavelength shifted AOD
    
    Parameters
    ----------
    to_lambda : float
        wavelength for which AOD is calculated
    aod_ref : float
        reference AOD
    lambda_ref : float
        wavelength corresponding to reference AOD
    angstrom_coeff : float
        Angstrom coefficient
        
    Returns
    -------
    float
        AOD at shifted wavelength
    
    """
    return aod_ref * (lambda_ref / to_lambda) ** angstrom_coeff

def exponent(num):
    """Get exponent of input number
        
    Parameters
    ----------
    num : :obj:`float` or iterable
        input number
    
    Returns
    -------
    :obj:`int` or :obj:`ndarray` containing ints
        exponent of input number(s)
        
    Example
    -------
    >>> from pyaerocom.mathutils import exponent
    >>> exponent(2340)
    3
    """
    return np.floor(np.log10(abs(np.asarray(num)))).astype(int)

def range_magnitude(low, high):
    """Returns magnitude of value range
    
    Parameters
    ----------
    low : float
        lower end of range
    high : float
        upper end of range
    
    Returns
    -------
    int
        magnitudes spanned by input numbers
    
    Example
    -------
    
    >>> range_magnitude(0.1, 100)
    3
    >>> range_magnitude(100, 0.1)
    -3
    >>> range_magnitude(1e-3, 1e6)
    9
    
    """
    return exponent(high) - exponent(low)

if __name__ == "__main__":
    import doctest
    exp = exponent(23)
    
    #run tests in all docstrings
    doctest.testmod()
    
    