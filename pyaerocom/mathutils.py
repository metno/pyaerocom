#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mathematical low level utility methods ofcd pyaerocom
"""

import numpy as np
from pyaerocom import const, logger

def od_wavelength_from_varstr(var_str):
    """Extracts AOD wavelength from Aerocom variable name
    
    Parameters
    ----------
    var_str : str
        Aerocom variable string (must start with od)
       
    Returns
    -------
    int
        wavelength in nm
       
    Raises
    ------
    ValueError
        if input string is invalid
    Example
    -------
    >>> od_wavelength_from_varstr('od500aer')
    500
    """
    raise NotImplementedError('Not sure if we will need this...')
    
    
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
    
    Raises 
    ------
    AttributError
        if either 'od440aer' or 'od870aer' are not available in data object
    """
    if not all([x in data for x in ['od440aer','od870aer']]):
        raise AttributeError("Either of the two (or both) required variables "
                             "(od440aer, od870aer) are not available in data")
    od440aer, od870aer = data['od440aer'], data['od870aer']
    return compute_angstrom_coeff(od440aer, od870aer, .44, .87)

def calc_od550aer(data):
    """Compute AOD at 550 nm using Angstrom coefficient and 500 nm AOD
        
    Parameters
    ----------
    data : dict-like
        data object containing imported results
    
    Returns
    -------
    :obj:`float` or :obj:`ndarray`
        AOD(s) at shifted wavelength
    """
    return _calc_od_helper(data=data, 
                           var_name='od550aer', 
                           to_lambda=.55, 
                           od_ref='od500aer', 
                           lambda_ref=.50, 
                           od_ref_alt='od440aer', 
                           lambda_ref_alt=.44)

def calc_od550gt1aer(data):
    """Compute coarse mode AOD at 550 nm using Angstrom coeff. and 500 nm AOD
        
    Parameters
    ----------
    data : dict-like
        data object containing imported results
    
    Returns
    -------
    :obj:`float` or :obj:`ndarray`
        AOD(s) at shifted wavelength
    """
    return _calc_od_helper(data=data, 
                           var_name='od550gt1aer', 
                           to_lambda=.55, 
                           od_ref='od500gt1aer', 
                           lambda_ref=.50)

def calc_od550lt1aer(data):
    """Compute fine mode AOD at 550 nm using Angstrom coeff. and 500 nm AOD
        
    Parameters
    ----------
    data : dict-like
        data object containing imported results
    
    Returns
    -------
    :obj:`float` or :obj:`ndarray`
        AOD(s) at shifted wavelength
    """
    return _calc_od_helper(data=data, 
                           var_name='od550lt1aer', 
                           to_lambda=.55, 
                           od_ref='od500lt1aer', 
                           lambda_ref=.50)
        
def compute_angstrom_coeff(od1, od2, lambda1, lambda2):
    """Compute Angstrom coefficient based on 2 optical densities
    
    Parameters
    ----------
    od1 : :obj:`float` or :obj:`ndarray`
        AOD at wavelength 1
    od2 : :obj:`float` or :obj:`ndarray`
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
    return -np.log(od1 / od2) / np.log(lambda1 / lambda2)

def compute_od_from_angstromexp(to_lambda, od_ref, lambda_ref, 
                                 angstrom_coeff):
    """Compute AOD at specified wavelength 
    
    Uses Angstrom coefficient and reference AOD to compute the 
    corresponding wavelength shifted AOD
    
    Parameters
    ----------
    to_lambda : :obj:`float` or :obj:`ndarray`
        wavelength for which AOD is calculated
    od_ref : :obj:`float` or :obj:`ndarray`
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
    return od_ref * (lambda_ref / to_lambda) ** angstrom_coeff

def _calc_od_helper(data, var_name, to_lambda, od_ref, lambda_ref, 
                    od_ref_alt=None, lambda_ref_alt=None):
    """Helper method for computing ODs
    
    Parameters
    ----------
    data : dict-like
        data object containing loaded results used to compute the ODs at a new
        wavelength
    var_name : str
        name of variable that is supposed to be computed (is used in order to 
        see whether a global lower threshold is defined for this variable and
        if this is the case, all computed values that are below this threshold
        are replaced with NaNs)
    to_lambda : float
        wavelength of computed AOD
    od_ref : :obj:`float` or :obj:`ndarray`
        reference AOD
    lambda_ref : :obj:`float` or :obj:`ndarray`
        wavelength corresponding to reference AOD
    od_ref_alt : :obj:`float` or :obj:`ndarray`, optional
        alternative reference AOD (is used for datapoints where former is 
        invalid)
    lambda_ref_alt : :obj:`float` or :obj:`ndarray`, optional
        wavelength corresponding to alternative reference AOD
        
    Returns
    -------
    :obj:`float` or :obj:`ndarray`
        AOD(s) at shifted wavelength
        
    Raises
    ------
    AttributeError
        if ``od_ref`` or "ang4487aer" not available in data
    """
    if not od_ref in data:
        raise AttributeError("Reference OD at {} nm data is not available in "
                             "provided data".format(lambda_ref))
    elif not 'ang4487aer' in data:
        raise AttributeError("Angstrom coefficient (440-870 nm) is not "
                             "available in provided data")
    result = compute_od_from_angstromexp(to_lambda=to_lambda, 
                                          od_ref=data[od_ref],
                                          lambda_ref=lambda_ref, 
                                          angstrom_coeff=data['ang4487aer'])
    # optional if available
    if od_ref_alt in data:
        # fill up time steps that are nans with values calculated from the
        # alternative wavelength to minimise gaps in the time series
        mask = np.argwhere(np.isnan(result))
        
        if len(mask) > 0: #there are nans
            ods_alt = data[od_ref_alt][mask]
            ang4487aer = data['ang4487aer'][mask]
            replace = compute_od_from_angstromexp(to_lambda=to_lambda, 
                                                    od_ref=ods_alt,
                                                    lambda_ref=lambda_ref_alt, 
                                                    angstrom_coeff=ang4487aer)
            result[mask] = replace
    
    try:
        # now replace all values with NaNs that are below the global lower threshold
        below_thresh = result < const.VAR_PARAM[var_name]['lower_limit']
        result[below_thresh] = np.nan
    except:
        logger.warn("Could not access lower limit from global settings for "
                    "variable {}".format(var_name))
    
    return result

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
    
    