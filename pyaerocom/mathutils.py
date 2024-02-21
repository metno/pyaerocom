"""
Mathematical low level utility methods of pyaerocom
"""
import numpy as np
from scipy.stats import kendalltau, pearsonr, spearmanr

from pyaerocom._warnings import ignore_warnings

### LAMBDA FUNCTIONS
in_range = lambda x, low, high: low <= x <= high

### OTHER FUNCTIONS


def is_strictly_monotonic(iter1d) -> bool:
    """
    Check if 1D iterble is strictly monotonic

    Parameters
    ----------
    iter1d
        1D iterable object to be tested

    Returns
    -------
    bool

    """
    return True if np.all(np.diff(iter1d) > 0) else False


def make_binlist(vmin: float, vmax: float, num: int = None) -> list:
    """"""
    if num is None:
        num = 8
    return list(np.linspace(vmin, vmax, num + 1))


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


@ignore_warnings(
    RuntimeWarning, "invalid value encountered in double_scalars", "An input array is constant"
)
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
        return (np.nan, np.nan)
    return (np.nanmean(data), np.nanstd(data))


@ignore_warnings(
    RuntimeWarning, "An input array is constant", "invalid value encountered in .*divide"
)
def calc_statistics(data, ref_data, lowlim=None, highlim=None, min_num_valid=1, weights=None):
    """Calc statistical properties from two data arrays

    Calculates the following statistical properties based on the two provided
    1-dimensional data arrays and returns them in a dictionary (keys are
    provided after the arrows):

        - Mean value of both arrays -> refdata_mean, data_mean
        - Standard deviation of both arrays -> refdata_std, data_std
        - RMS (Root mean square) -> rms
        - NMB (Normalised mean bias) -> nmb
        - MNMB (Modified normalised mean bias) -> mnmb
        - MB (Mean Bias) -> mb
        - MAB (Mean Absolute Bias) -> mab
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
        raise ValueError("Invalid input. Data arrays must be one dimensional")

    result = {}

    mask = ~np.isnan(ref_data) * ~np.isnan(data)
    num_points = mask.sum()

    data, ref_data = data[mask], ref_data[mask]

    weighted = False if weights is None else True

    result["totnum"] = float(len(mask))
    result["num_valid"] = float(num_points)
    ref_mean, ref_std = _nanmean_and_std(ref_data)
    data_mean, data_std = _nanmean_and_std(data)
    result["refdata_mean"] = ref_mean
    result["refdata_std"] = ref_std
    result["data_mean"] = data_mean
    result["data_std"] = data_std
    result["weighted"] = weighted

    if not num_points >= min_num_valid:
        if lowlim is not None:
            valid = np.logical_and(data > lowlim, ref_data > lowlim)
            data = data[valid]
            ref_data = ref_data[valid]
        if highlim is not None:
            valid = np.logical_and(data < highlim, ref_data < highlim)
            data = data[valid]
            ref_data = ref_data[valid]

        result["rms"] = np.nan
        result["nmb"] = np.nan
        result["mnmb"] = np.nan
        result["fge"] = np.nan
        result["R"] = np.nan
        result["R_spearman"] = np.nan

        return result

    if lowlim is not None:
        valid = np.logical_and(data > lowlim, ref_data > lowlim)
        data = data[valid]
        ref_data = ref_data[valid]
    if highlim is not None:
        valid = np.logical_and(data < highlim, ref_data < highlim)
        data = data[valid]
        ref_data = ref_data[valid]

    difference = data - ref_data

    diffsquare = difference**2

    if weights is not None:
        weights = weights[mask]
        weights = weights / weights.max()
        result[
            "NOTE"
        ] = "Weights were not applied to FGE and kendall and spearman corr (not implemented)"

    result["rms"] = np.sqrt(np.average(diffsquare, weights=weights))

    # NO implementation to apply weights yet ...
    if num_points > 1:
        result["R"] = corr(data, ref_data, weights)
        result["R_spearman"] = spearmanr(data, ref_data)[0]
        result["R_kendall"] = kendalltau(data, ref_data)[0]
    else:
        result["R"] = np.nan
        result["R_spearman"] = np.nan
        result["R_kendall"] = np.nan

    sum_diff = sum(difference, weights=weights)
    sum_refdata = sum(ref_data, weights=weights)

    if sum_refdata == 0:
        if sum_diff == 0:
            nmb = 0
            mb = 0
        else:
            nmb = np.nan
            mb = np.nan
    else:
        nmb = sum_diff / sum_refdata
        mb = sum_diff

    sum_data_refdata = data + ref_data
    # for MNMB, and FGE: don't divide by 0 ...
    mask = ~np.isnan(sum_data_refdata)
    num_points = mask.sum()
    if num_points == 0:
        mnmb = np.nan
        fge = np.nan
        mb = np.nan
        mab = np.nan
    else:
        tmp = difference[mask] / sum_data_refdata[mask]
        if weights is not None:
            weights = weights[mask]
        mnmb = 2.0 / num_points * sum(tmp, weights=weights)
        fge = 2.0 / num_points * sum(np.abs(tmp), weights=weights)
        mb = sum(difference[mask]) / num_points
        mab = sum(np.abs(difference[mask])) / num_points

    result["nmb"] = nmb
    result["mnmb"] = mnmb
    result["fge"] = fge
    result["mb"] = mb
    result["mab"] = mab

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
    IN_NUM = False
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
            IN_NUM = False
    if IN_NUM:
        numbers.append(c_num)
    return numbers


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


def estimate_value_range(vmin, vmax, extend_percent=0):
    """
    Round and extend input range to estimate lower and upper bounds of range

    Parameters
    ----------
    vmin : float
        lower value of range
    vmax : float
        upper value of range
    extend_percent : int
        percentage specifying to which extent the input range is supposed to be
        extended.

    Returns
    -------
    float
        estimated lower end of range
    float
        estimated upper end of range


    """
    if not vmax > vmin:
        raise ValueError("vmax needs to exceed vmin")
    # extent value range by +/- 5%
    offs = (vmax - vmin) * extend_percent * 0.01
    vmin, vmax = vmin - offs, vmax + offs

    if vmin != 0:
        exp = float(exponent(vmin))
    else:
        exp = float(exponent(vmax))
    # round values
    vmin = np.floor(vmin * 10 ** (-exp)) * 10.0 ** (exp)
    vmax = np.ceil(vmax * 10 ** (-exp)) * 10.0 ** (exp)
    return vmin, vmax


def _init_stats_dummy():
    # dummy for statistics dictionary for locations without data
    stats_dummy = {}
    for k in calc_statistics([1], [1]):
        stats_dummy[k] = np.nan

    # Test to make sure these variables are defined even when yearly and season != all
    stats_dummy["R_spatial_mean"] = np.nan
    stats_dummy["R_spatial_median"] = np.nan
    stats_dummy["R_temporal_mean"] = np.nan
    stats_dummy["R_temporal_median"] = np.nan

    return stats_dummy
