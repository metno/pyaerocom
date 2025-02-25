"""
Mathematical low level utility methods of pyaerocom
"""

import numpy as np
from scipy.stats import pearsonr

from pyaerocom._warnings import ignore_warnings


def in_range(x, low, high) -> bool:
    return low <= x <= high


def is_strictly_monotonic(iter1d) -> bool:
    """
    Check if 1D iterable is strictly monotonic

    Parameters
    ----------
    iter1d
        1D iterable object to be tested

    Returns
    -------
    bool

    """
    return True if np.all(np.diff(iter1d) > 0) else False


def make_binlist(vmin: float, vmax: float, num: int = 8) -> list[float]:
    return np.linspace(vmin, vmax, num + 1).tolist()


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


@ignore_warnings(RuntimeWarning, "invalid value encountered in scalar divide")
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
    ['42', '100']
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
    np.int64(3)
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
    np.int64(3)
    >>> range_magnitude(100, 0.1)
    np.int64(-3)
    >>> range_magnitude(1e-3, 1e6)
    np.int64(9)

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
