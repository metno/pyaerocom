#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mathematical low level utility methods of pyaerocom
"""
import cf_units
import numpy as np

from pyaerocom import const, logger
from scipy.stats import pearsonr, spearmanr, kendalltau

### LAMBDA FUNCTIONS
in_range = lambda x, low, high: low <= x <= high

### OTHER FUNCTIONS

def weighted_sum(data, weights):
    """Compute weighted sum using numpy dot product

    Parameters
    ----------
    data : ndarray
        data array that is supposed to be summed up
    weights : ndarray
        array containing weights for each point in `data`

    Returns
    -------
    float
        weighted sum of values in input array
    """
    return np.dot(data, weights)

def sum(data, weights=None):
    """Summing operation with option to perform weighted sum

    Parameters
    ----------
    data : ndarray
        data array that is supposed to be summed up
    weights : ndarray, optional
        array containing weights for each point in `data`

    Returns
    -------
    float or int
        sum of values in input array
    """
    if weights is None:
        return np.sum(data)
    return weighted_sum(data, weights)

def weighted_mean(data, weights):
    """Compute weighted mean

    Parameters
    ----------
    data : ndarray
        data array that is supposed to be averaged
    weights : ndarray
        array containing weights for each point in `data`

    Returns
    -------
    float or int
        weighted mean of data array
    """
    return np.sum(data * weights) / np.sum(weights)

def weighted_cov(ref_data, data, weights):
    """Compute weighted covariance

    Parameters
    ----------
    data_ref : ndarray
        x data
    data : ndarray
        y data
    weights : ndarray
        array containing weights for each point in `data`

    Returns
    -------
    float
        covariance
    """
    avgx = weighted_mean(ref_data, weights)
    avgy = weighted_mean(data, weights)
    return np.sum(weights * (ref_data - avgx) * (data - avgy)) / np.sum(weights)

def weighted_corr(ref_data, data, weights):
    """Compute weighted correlation

    Parameters
    ----------
    data_ref : ndarray
        x data
    data : ndarray
        y data
    weights : ndarray
        array containing weights for each point in `data`

    Returns
    -------
    float
       weighted correlation coefficient
    """
    wcovxy = weighted_cov(ref_data, data, weights)

    wcovxx = weighted_cov(ref_data, ref_data, weights)
    wcovyy = weighted_cov(data, data, weights)
    wsigmaxy = np.sqrt(wcovxx * wcovyy)
    return wcovxy / wsigmaxy

def corr(ref_data, data, weights=None):
    """Compute correlation coefficient

    Parameters
    ----------
    data_ref : ndarray
        x data
    data : ndarray
        y data
    weights : ndarray, optional
        array containing weights for each point in `data`

    Returns
    -------
    float
       correlation coefficient
    """
    if weights is None:
        return pearsonr(ref_data, data)[0]
    return weighted_corr(ref_data, data, weights)

def _nanmean_and_std(data):
    """
    Calculate mean and std for input data (may contain NaN's')

    Parameters
    ----------
    data : list or numpy.ndarray
        input data

    Returns
    -------
    float
        mean value of input data.
    float
        standard deviation of input data.

    """
    if np.all(np.isnan(data)):
        return (np.nan,np.nan)
    return (np.nanmean(data), np.nanstd(data))

def calc_statistics(data, ref_data, lowlim=None, highlim=None,
                    min_num_valid=1, weights=None):
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

    ws = False
    if weights is not None:
        weights = weights[mask]
        weights = weights / weights.max()
        ws = True
        result['NOTE'] = ('Weights were not applied to FGE and kendall and '
                          'spearman corr (not implemented)')

    result['totnum'] = float(len(mask))
    result['num_valid'] = float(num_points)
    ref_mean, ref_std = _nanmean_and_std(ref_data)
    data_mean, data_std = _nanmean_and_std(data)
    result['refdata_mean'] = ref_mean
    result['refdata_std'] = ref_std
    result['data_mean'] = data_mean
    result['data_std'] = data_std
    result['weighted'] = ws

    if not num_points >= min_num_valid:
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

        return result

    if lowlim is not None:
        valid = np.logical_and(data>lowlim, ref_data>lowlim)
        data = data[valid]
        ref_data = ref_data[valid]
    if highlim is not None:
        valid = np.logical_and(data<highlim, ref_data<highlim)
        data = data[valid]
        ref_data = ref_data[valid]

    difference = data - ref_data

    diffsquare = difference**2
    result['rms'] = np.sqrt(np.average(diffsquare, weights=weights))

    # NO implementation to apply weights yet ...
    if num_points > 1:
        result['R'] = corr(data, ref_data, weights)
        result['R_spearman'] = spearmanr(data, ref_data)[0]
        result['R_kendall'] = kendalltau(data, ref_data)[0]
    else:
        result['R'] = np.nan
        result['R_spearman'] = np.nan
        result['R_kendall'] = np.nan

    sum_diff = sum(difference, weights=weights)
    sum_refdata = sum(ref_data, weights=weights)

    if sum_refdata == 0:
        if sum_diff == 0:
            nmb = 0
        else:
            nmb = np.nan
    else:
        nmb = sum_diff / sum_refdata

    sum_data_refdata = (data + ref_data)
    # for MNMB, and FGE: don't divide by 0 ...
    mask = ~np.isnan(sum_data_refdata)
    num_points = mask.sum()
    if num_points == 0:
        mnmb = np.nan
        fge = np.nan
    else:
        tmp = difference[mask] / sum_data_refdata[mask]
        if weights is not None:
            weights = weights[mask]
        mnmb = 2. / num_points * sum(tmp, weights=weights)
        fge = 2. / num_points * sum(np.abs(tmp), weights=weights)

    result['nmb'] = nmb
    result['mnmb'] = mnmb
    result['fge'] = fge

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
        except Exception:
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

    return result

def compute_ang4470dryaer_from_dry_scat(data):
    """Compute angstrom exponent between 440 and 700 nm

    Parameters
    ----------
    StationData or dict
        data containing dry scattering coefficients at 440 and 700 nm
        (i.e. keys sc440dryaer and sc700dryaer)

    Returns
    -------
    StationData or dict
        extended data object containing angstrom exponent
    """
    return compute_angstrom_coeff(data['sc440dryaer'],
                                  data['sc700dryaer'],
                                  440, 700)

def compute_sc550dryaer(data):
    """Compute dry scattering coefficent applying RH threshold

    Cf. :func:`_compute_dry_helper`

    Parameters
    ----------
    dict
        data object containing scattering and RH data

    Returns
    -------
    dict
        modified data object containing new column sc550dryaer

    """
    rh_max= const.VARS['sc550dryaer'].dry_rh_max
    vals, rh_mean = _compute_dry_helper(data, data_colname='sc550aer',
                               rh_colname='scrh',
                               rh_max_percent=rh_max)
    if not 'sc550dryaer' in data.var_info:
        data.var_info['sc550dryaer'] = {}
    data.var_info['sc550dryaer']['rh_mean'] = rh_mean

    return vals

def compute_sc440dryaer(data):
    """Compute dry scattering coefficent applying RH threshold

    Cf. :func:`_compute_dry_helper`

    Parameters
    ----------
    dict
        data object containing scattering and RH data

    Returns
    -------
    dict
        modified data object containing new column sc550dryaer

    """
    rh_max= const.VARS['sc440dryaer'].dry_rh_max
    return _compute_dry_helper(data, data_colname='sc440aer',
                               rh_colname='scrh',
                               rh_max_percent=rh_max)[0]

def compute_sc700dryaer(data):
    """Compute dry scattering coefficent applying RH threshold

    Cf. :func:`_compute_dry_helper`

    Parameters
    ----------
    dict
        data object containing scattering and RH data

    Returns
    -------
    dict
        modified data object containing new column sc550dryaer

    """
    rh_max= const.VARS['sc700dryaer'].dry_rh_max
    return _compute_dry_helper(data, data_colname='sc700aer',
                               rh_colname='scrh',
                               rh_max_percent=rh_max)[0]

def compute_ac550dryaer(data):
    """Compute aerosol dry absorption coefficent applying RH threshold

    Cf. :func:`_compute_dry_helper`

    Parameters
    ----------
    dict
        data object containing scattering and RH data

    Returns
    -------
    dict
        modified data object containing new column sc550dryaer

    """
    rh_max= const.VARS['ac550dryaer'].dry_rh_max
    return _compute_dry_helper(data, data_colname='ac550aer',
                                         rh_colname='acrh',
                                         rh_max_percent=rh_max)[0]


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

    rh_mean = np.nanmean(rh[~high_rh])

    return vals, rh_mean

def _compute_wdep_from_concprcp_helper(data, wdep_var, concprcp_var):

    vars_needed = (concprcp_var, 'pr')

    if not all(x in data.data_flagged for x in vars_needed):
        raise ValueError(f'Need flags for {vars_needed} to compute wet deposition')
    from pyaerocom import TsType
    from pyaerocom.units_helpers import get_unit_conversion_fac, RATES_FREQ_DEFAULT

    tst = TsType(data.get_var_ts_type(concprcp_var))

    ival = tst.to_si()

    conc_unit = data.get_unit(concprcp_var)
    conc_data = data[concprcp_var]
    if not conc_unit.endswith('m-3'):
        raise NotImplementedError('Can only handle concprcp unit ending with m-3')
    concprcp_flags = data.data_flagged[concprcp_var]

    pr_unit = data.get_unit('pr')
    if not pr_unit == 'm':
        data.convert_unit('pr', 'm')
    pr_data = data['pr']
    pr_flags = data.data_flagged['pr']

    pr_zero = pr_data == 0
    if pr_zero.sum() > 0:
        conc_data[pr_zero] = 0
        concprcp_flags[pr_zero] = False
        pr_flags[pr_zero] = False
    wdep = conc_data * pr_data
    wdep_units = conc_unit.replace('m-3', 'm-2')

    if not ival == RATES_FREQ_DEFAULT:
        fac = get_unit_conversion_fac(ival, RATES_FREQ_DEFAULT)
        wdep /= fac
    # in units of ts_type, that is, e.g. kg m-2 d
    freq_str = f' {RATES_FREQ_DEFAULT}-1'
    wdep_units += freq_str
    if not wdep_var in data.var_info:
        data.var_info[wdep_var] = {}
    data.var_info[wdep_var]['units'] = wdep_units

    # set flags for wetso4
    wdep_flags = np.zeros(len(wdep)).astype(bool)
    wdep_flags[concprcp_flags] = True
    wdep_flags[pr_flags] = True
    data.data_flagged[wdep_var] = wdep_flags

    return wdep

def compute_wetoxs_from_concprcpoxs(data):
    """Compute wdep from conc in precip and precip data

    Parameters
    ----------
    StationData
        data object containing concprcp and precip data

    Returns
    -------
    StationData
        modified data object containing wdep data

    """
    return _compute_wdep_from_concprcp_helper(data, 'wetoxs', 'concprcpoxs')

def compute_wetoxn_from_concprcpoxn(data):
    """Compute wdep from conc in precip and precip data

    Parameters
    ----------
    StationData
        data object containing concprcp and precip data

    Returns
    -------
    StationData
        modified data object containing wdep data

    """
    return _compute_wdep_from_concprcp_helper(data, 'wetoxn', 'concprcpoxn')

def compute_wetrdn_from_concprcprdn(data):
    """Compute wdep from conc in precip and precip data

    Parameters
    ----------
    StationData
        data object containing concprcp and precip data

    Returns
    -------
    StationData
        modified data object containing wdep data

    """
    return _compute_wdep_from_concprcp_helper(data, 'wetrdn', 'concprcprdn')


def vmrx_to_concx(data, p_pascal, T_kelvin, vmr_unit, mmol_var, mmol_air=None,
                  to_unit=None):
    """
    Convert volume mixing ratio (vmr) to mass concentration

    Parameters
    ----------
    data : float or ndarray
        array containing vmr values
    p_pascal : float
        pressure in Pa of input data
    T_kelvin : float
        temperature in K of input data
    vmr_unit : str
        unit of input data
    mmol_var : float
        molar mass of variable represented by input data
    mmol_air : float, optional
        Molar mass of air. Uses average density of dry air if None.
        The default is None.
    to_unit : str, optional
        Unit to which output data is converted. If None, output unit is
        kg m-3. The default is None.

    Returns
    -------
    float or ndarray
        input data converted to mass concentration

    """
    if mmol_air is None:
        from pyaerocom.molmasses import get_molmass
        mmol_air = get_molmass('air_dry')

    Rspecific = 287.058 # J kg-1 K-1

    conversion_fac = 1/cf_units.Unit('mol mol-1').convert(1, vmr_unit)

    airdensity = p_pascal/(Rspecific * T_kelvin) # kg m-3
    mulfac = mmol_var / mmol_air * airdensity # kg m-3
    conc = data * mulfac # kg m-3
    if to_unit is not None:
        conversion_fac *= cf_units.Unit('kg m-3').convert(1, to_unit)
    if not np.isclose(conversion_fac, 1, rtol=1e-7):
        conc *= conversion_fac
    return conc

def concx_to_vmrx(data, p_pascal, T_kelvin, conc_unit, mmol_var, mmol_air=None,
                  to_unit=None):
    """
    WORK IN PROGRESS. DO NOT USE!
    Convert mass concentration to volume mixing ratio (vmr)

    Parameters
    ----------
    data : float or ndarray
        array containing vmr values
    p_pascal : float
        pressure in Pa of input data
    T_kelvin : float
        temperature in K of input data
    vmr_unit : str
        unit of input data
    mmol_var : float
        molar mass of variable represented by input data
    mmol_air : float, optional
        Molar mass of air. Uses average density of dry air if None.
        The default is None.
    to_unit : str, optional
        Unit to which output data is converted. If None, output unit is
        kg m-3. The default is None.

    Returns
    -------
    float or ndarray
        input data converted to volume mixing ratio

    """
    if mmol_air is None:
        from pyaerocom.molmasses import get_molmass
        mmol_air = get_molmass('air_dry')

    Rspecific = 287.058 # J kg-1 K-1

    conversion_fac = 1/cf_units.Unit('kg m-3').convert(1, conc_unit)

    airdensity = p_pascal/(Rspecific * T_kelvin) # kg m-3
    mulfac = mmol_var / mmol_air * airdensity # kg m-3
    vmr = data / mulfac # unitless
    if to_unit is not None:
        conversion_fac *= cf_units.Unit('mole mole-1').convert(1, to_unit)
    if not np.isclose(conversion_fac, 1, rtol=1e-7):
        vmr *= conversion_fac
    return vmr

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
    #print(numbers_in_str('Bla42Blub100'))
    #run tests in all docstrings
    #doctest.testmod()

    mod = np.ones(20)
    obs = np.ones(20)
    weights = np.ones(20)

    weights[10] = 100

    mod[10] = 10
    obs[10] = 10

    c1 = calc_statistics(mod, obs)
    c2 = calc_statistics(mod, obs, weights=weights)

    assert c1['nmb'] == 0
    assert c1['mnmb'] == 0
    assert c1['R'] == 1

    assert c2['nmb'] == 0
    assert c2['mnmb'] == 0
    assert c2['R'] == 1

    obs[10] = 9

    c1 = calc_statistics(mod, obs)
    c2 = calc_statistics(mod, obs, weights=weights)

    wm = weighted_mean(mod, weights)

    print(wm)

    wcov = weighted_cov(obs, mod, weights)
    print(wcov)
