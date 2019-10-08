#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mathematical low level utility methods ofcd pyaerocom
"""

import numpy as np
from pyaerocom import const, logger
from scipy.stats import pearsonr, spearmanr, kendalltau

### LAMBDA FUNCTIONS
in_range = lambda x, low, high: low <= x <= high

### OTHER FUNCTIONS
def calc_statistics(data, ref_data, lowlim=None, highlim=None,
                    min_num_valid=5):
    """Calc statistical properties from two data arrays
    
    Calculates the following statistical properties based on the two provided
    1-dimensional data arrays and returns them in a dictionary (keys are 
    provided after the arrows):
        
        - Mean value of both arrays -> refdata_mean, data_mean
        - Standard deviation of both arrays -> refdata_std, data_std
        - RMS (Root mean square) -> rms
        - NMB (Normalised mean bias) -> nmb
        - MNMB (Modified normalised mean bias) -> mnmb
        - FGE (Fractional gross error) -> fge
        - R (Pearson correlation coefficient) -> R
        - R_spearman (Spearman corr. coeff) -> R_spearman
        
    Note
    ----
    Nans are removed from the input arrays, information about no. of removed
    points can be inferred from keys `totnum` and `num_valid` in return dict.
    
    Parameters
    ----------
    data : ndarray
        array containing data, that is supposed to be compared with reference
        data
    ref_data : ndarray
        array containing data, that is used to compare `data` array with
    lowlim : float
        lower end of considered value range (e.g. if set 0, then all datapoints
        where either ``data`` or ``ref_data`` is smaller than 0 are removed)
    highlim : float
        upper end of considered value range
    min_num_valid : int
        minimum number of valid measurements required to compute statistical
        parameters.
        
    Returns
    -------
    dict
        dictionary containing computed statistics    
    
    Raises
    ------
    ValueError 
        if either of the input arrays has dimension other than 1
        
    """
    data = np.asarray(data)
    ref_data = np.asarray(ref_data)
    
    if not data.ndim == 1 or not ref_data.ndim == 1:
        raise ValueError('Invalid input. Data arrays must be one dimensional')
        
    result = {}
    
    mask = ~np.isnan(ref_data) * ~np.isnan(data)
    num_points = mask.sum()
    
    data, ref_data = data[mask], ref_data[mask]
    
    result['totnum'] = float(len(mask))
    result['num_valid'] = float(num_points)
    result['refdata_mean'] = np.nanmean(ref_data)
    result['refdata_std'] = np.nanstd(ref_data)
    result['data_mean'] = np.nanmean(data)
    result['data_std'] = np.nanstd(data)
    if not num_points > min_num_valid:
        if lowlim is not None:
            valid = np.logical_and(data>lowlim, ref_data>lowlim)
            data = data[valid]
            ref_data = ref_data[valid]
        if highlim is not None:
            valid = np.logical_and(data<highlim, ref_data<highlim)
            data = data[valid]
            ref_data = ref_data[valid]
        
        result['rms'] = np.nan
        result['nmb'] = np.nan
        result['mnmb'] = np.nan
        result['fge'] = np.nan
        result['R'] = np.nan
        result['R_spearman'] = np.nan
    else:
        if lowlim is not None:
            valid = np.logical_and(data>lowlim, ref_data>lowlim)
            data = data[valid]
            ref_data = ref_data[valid]
        if highlim is not None:
            valid = np.logical_and(data<highlim, ref_data<highlim)
            data = data[valid]
            ref_data = ref_data[valid]
        
        difference = data - ref_data
        
        result['rms'] = np.sqrt(np.mean(difference**2))
        
        result['R'] = pearsonr(data, ref_data)[0]
        result['R_spearman'] = spearmanr(data, ref_data)[0]
        result['R_kendall'] = kendalltau(data, ref_data)[0]
        
        # NMB, MNMB and FGE are constrained to positive values, thus negative
        # values need to be removed
        neg_ref = ref_data < 0
        neg_data = data < 0
        
        use_indices = ~(neg_data + neg_ref)
        
        diff_pos = difference[use_indices]
        ref_data_pos = ref_data[use_indices]
        data_pos = data[use_indices]
        
        num_points_pos = len(data_pos)
        
        if num_points_pos == 0:
            result['nmb'] = np.nan
            result['mnmb'] = np.nan
            result['fge'] = np.nan
        else:
            result['nmb'] = np.sum(diff_pos) / np.sum(ref_data_pos) #*100.
            
            tmp = diff_pos / (data_pos + ref_data_pos)
            
            result['mnmb'] = 2. / num_points_pos * np.sum(tmp)# * 100.
            result['fge'] = 2. / num_points_pos * np.sum(np.abs(tmp)) #* 100.
            
        result['num_neg_data'] = np.sum(neg_data)
        result['num_neg_refdata'] = np.sum(neg_ref)
     
    return result

def closest_index(num_array, value):
    """Returns index in number array that is closest to input value"""
    return np.argmin(np.abs(np.asarray(num_array) - value))

def numbers_in_str(input_string):
    """This method finds all numbers in a string
    
    Note
    ----
    - Beta version, please use with care
    - Detects only integer numbers, dots are ignored
    
    Parameters
    ----------
    input_string : str
        string containing numbers
    
    Returns
    -------
    list
        list of strings specifying all numbers detected in string
        
    Example
    -------
    >>> numbers_in_str('Bla42Blub100')
    [42, 100]
    """
    numbers = []
    IN_NUM=False
    c_num = None
    for char in input_string:
        try:
            int(char)
            if not IN_NUM:
                IN_NUM = True
                c_num = char
            elif IN_NUM:
                c_num += char
        except:
            if IN_NUM:
                numbers.append(c_num)
            IN_NUM=False
    if IN_NUM:
        numbers.append(c_num)
    return numbers    
    
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
                           lambda_ref_alt=.44,
                           use_angstrom_coeff='ang4487aer')

def calc_abs550aer(data):
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
                           var_name='abs550aer', 
                           to_lambda=.55, 
                           od_ref='abs500aer', 
                           lambda_ref=.50, 
                           od_ref_alt='abs440aer', 
                           lambda_ref_alt=.44,
                           use_angstrom_coeff='angabs4487aer')
    
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
                           lambda_ref=.50,
                           use_angstrom_coeff='ang4487aer')

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
                           lambda_ref=.50,
                           use_angstrom_coeff='ang4487aer')
        
    
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
                    od_ref_alt=None, lambda_ref_alt=None, 
                    use_angstrom_coeff='ang4487aer'):
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
    use_angstrom_coeff : str
        name of Angstrom coefficient in data, that is used for computation
        
    Returns
    -------
    :obj:`float` or :obj:`ndarray`
        AOD(s) at shifted wavelength
        
    Raises
    ------
    AttributeError
        if neither ``od_ref`` nor ``od_ref_alt`` are available in data, or if
        ``use_angstrom_coeff`` is missing
    """
    if not od_ref in data:
        logger.warning('Reference OD at {} nm is not available in data, '
                       'checking alternative'.format(lambda_ref))
        if od_ref_alt is None or not od_ref_alt in data:
            raise AttributeError('No alternative OD found for computation of '
                                 '{}'.format(var_name))
        return compute_od_from_angstromexp(to_lambda=to_lambda, 
                                           od_ref=data[od_ref_alt],
                                           lambda_ref=lambda_ref_alt, 
                                           angstrom_coeff=data[use_angstrom_coeff])
    elif not use_angstrom_coeff in data:
        raise AttributeError("Angstrom coefficient (440-870 nm) is not "
                             "available in provided data")
    result = compute_od_from_angstromexp(to_lambda=to_lambda, 
                                          od_ref=data[od_ref],
                                          lambda_ref=lambda_ref, 
                                          angstrom_coeff=data[use_angstrom_coeff])
    # optional if available
    if od_ref_alt in data:
        # fill up time steps that are nans with values calculated from the
        # alternative wavelength to minimise gaps in the time series
        mask = np.argwhere(np.isnan(result))
        
        if len(mask) > 0: #there are nans
            ods_alt = data[od_ref_alt][mask]
            ang = data[use_angstrom_coeff][mask]
            replace = compute_od_from_angstromexp(to_lambda=to_lambda, 
                                                    od_ref=ods_alt,
                                                    lambda_ref=lambda_ref_alt, 
                                                    angstrom_coeff=ang)
            result[mask] = replace
    
    try:
        # now replace all values with NaNs that are below the global lower threshold
        below_thresh = result < const.VARS[var_name]['minimum']
        result[below_thresh] = np.nan
    except:
        logger.warning("Could not access lower limit from global settings for "
                       "variable {}".format(var_name))
    
    return result

def compute_ang4470dryaer_from_dry_scat(data):
    """Compute angstrom exponent between 440 and 700 nm 
    
    Parameters
    ----------
    StationData or dict
        data containing dry scattering coefficients at 440 and 700 nm
        (i.e. keys scatc440dryaer and scatc700dryaer)
    
    Returns
    -------
    StationData or dict
        extended data object containing angstrom exponent
    """
    return compute_angstrom_coeff(data['scatc440dryaer'],
                                  data['scatc700dryaer'],
                                  440, 700)

def compute_scatc550dryaer(data):
    """Compute dry scattering coefficent applying RH threshold
    
    Cf. :func:`_compute_dry_helper`
    
    Parameters
    ----------
    dict
        data object containing scattering and RH data
    
    Returns
    -------
    dict 
        modified data object containing new column scatc550dryaer
    
    """
    rh_max= const.VARS['scatc550dryaer'].dry_rh_max
    return _compute_dry_helper(data, data_colname='scatc550aer', 
                               rh_colname='scatcrh', 
                               rh_max_percent=rh_max)
    
def compute_scatc440dryaer(data):
    """Compute dry scattering coefficent applying RH threshold
    
    Cf. :func:`_compute_dry_helper`
    
    Parameters
    ----------
    dict
        data object containing scattering and RH data
    
    Returns
    -------
    dict 
        modified data object containing new column scatc550dryaer
    
    """
    rh_max= const.VARS['scatc440dryaer'].dry_rh_max
    return _compute_dry_helper(data, data_colname='scatc440aer', 
                               rh_colname='scatcrh', 
                               rh_max_percent=rh_max)

def compute_scatc700dryaer(data):
    """Compute dry scattering coefficent applying RH threshold
    
    Cf. :func:`_compute_dry_helper`
    
    Parameters
    ----------
    dict
        data object containing scattering and RH data
    
    Returns
    -------
    dict 
        modified data object containing new column scatc550dryaer
    
    """
    rh_max= const.VARS['scatc700dryaer'].dry_rh_max
    return _compute_dry_helper(data, data_colname='scatc700aer', 
                               rh_colname='scatcrh', 
                               rh_max_percent=rh_max)
    
def compute_absc550dryaer(data):
    """Compute aerosol dry absorption coefficent applying RH threshold
    
    Cf. :func:`_compute_dry_helper`
    
    Parameters
    ----------
    dict
        data object containing scattering and RH data
    
    Returns
    -------
    dict 
        modified data object containing new column scatc550dryaer
    
    """
    rh_max= const.VARS['absc550dryaer'].dry_rh_max
    return _compute_dry_helper(data, data_colname='absc550aer', 
                               rh_colname='abscrh', 
                               rh_max_percent=rh_max)
    
def _compute_dry_helper(data, data_colname, rh_colname, 
                        rh_max_percent=None):
    """Compute new column that contains data where RH is smaller than ...
    
    All values in original data columns are set to NaN, where RH exceeds a 
    certain threshold or where RH is NaN.
    
    Parameters
    ----------
    data : dict-like
        dictionary-like object that contains data
    data_colname : str
        column name of variable data that is supposed to be filtered
    rh_colname : str
        column name of RH data
    rh_max_percent : int
        maximum relative humidity
        
    Returns
    -------
    dict
        modified data dictionary with new dry data column 
    """
    if rh_max_percent is None:
        rh_max_percent = const.RH_MAX_PERCENT_DRY
        
    vals = np.array(data[data_colname], copy=True)

    rh = data[rh_colname]
    
    high_rh = rh > rh_max_percent
    
    vals[high_rh] = np.nan
    vals[np.isnan(rh)] = np.nan
    
    return vals
    
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
    #import doctest
    exp = exponent(23)
    print(numbers_in_str('Bla42Blub100'))
    #run tests in all docstrings
    #doctest.testmod()
    
    