#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mathematical low level utility methods ofcd pyaerocom
"""

import numpy as np
from pyaerocom import const

def calc_ang4487aer(data):
    """Compute Angstrom coefficient (440-870nm) from 440 and 870 nm AODs
    
    Parameters
    ----------
    data : dict-like
        data object containing imported results
    
    Note
    ----
    Requires the following two variables to be available in provided data 
    object:
        
        1. od440aer
        2. od870aer
    
    Returns
    -------
    ndarray
        array containing computed angstrom coefficients
    """
    od440aer, od870aer = data['od440aer'], data['od870aer']
    return compute_angstrom_coeff(od440aer, od870aer, .44, .87)
    

def calc_od550aer(data):
    """Compute AOD at 550 nm using Angstrom coefficients and 
        
        Parameters
        ----------
        data : dict-like
            data object containing imported results
        
        Returns
        -------
        dict
            updated data object
    """
    od550aer = compute_aod_from_angstromexp(to_lambda=.55, 
                                            aod_ref=data['od500aer'],
                                            lambda_ref=.50, 
                                            angstrom_coeff=data['ang4487aer'])
    
    # ;fill up time steps of the now calculated od550_aer that are nans with values calculated from the
    # ;440nm wavelength to minimise gaps in the time series
    mask = np.argwhere(np.isnan(od550aer))
    
    if len(mask) > 0: #there are nans
        od440aer = data['od440aer'][mask]
        ang4487aer = data['ang4487aer'][mask]
        replace = compute_aod_from_angstromexp(to_lambda=.55, 
                                                aod_ref=od440aer,
                                                lambda_ref=.44, 
                                                angstrom_coeff=ang4487aer)
        od550aer[mask] = replace
        
    # now replace all values with NaNs that are below the global lower threshold
    below_thresh = od550aer < const.VAR_PARAM['od550aer']['lower_limit']
    od550aer[below_thresh] = np.nan

    return od550aer

def compute_angstrom_coeff(aod1, aod2, lambda1, lambda2):
    """Compute Angstrom coefficient based on 2 optical densities
    
    Parameters
    ----------
    aod1 : :obj:`float` or :obj:`ndarray`
        AOD at wavelength 1
    aod2 : :obj:`float` or :obj:`ndarray`
        AOD at wavelength 2
    lambda1 : :obj:`float` or :obj:`ndarray`
        wavelength 1
    lambda 2 : :obj:`float` or :obj:`ndarray`
        wavelength 2
        
    Returns
    -------
    :obj:`float` or :obj:`ndarray`
        Angstrom exponent(s)
    """
    return -np.log(aod1 / aod2) / np.log(lambda1 / lambda2)

def compute_aod_from_angstromexp(to_lambda, aod_ref, lambda_ref, 
                                 angstrom_coeff):
    """Compute AOD at specified wavelength 
    
    Uses Angstrom coefficient and reference AOD to compute the 
    corresponding wavelength shifted AOD
    
    Parameters
    ----------
    to_lambda : :obj:`float` or :obj:`ndarray`
        wavelength for which AOD is calculated
    aod_ref : :obj:`float` or :obj:`ndarray`
        reference AOD
    lambda_ref : :obj:`float` or :obj:`ndarray`
        wavelength corresponding to reference AOD
    angstrom_coeff : :obj:`float` or :obj:`ndarray`
        Angstrom coefficient
        
    Returns
    -------
    :obj:`float` or :obj:`ndarray`
        AOD(s) at shifted wavelength
    
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
    
    