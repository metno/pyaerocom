import numpy as np
from scipy.stats import ConstantInputWarning, kendalltau, spearmanr

from pyaerocom.mathutils import corr, sum

from .._warnings import ignore_warnings


def stat_R(data: np.ndarray, ref_data: np.ndarray, weights: np.ndarray | None) -> np.float64:
    """
    Pearson correlation coefficient implementation.
    """
    return corr(data, ref_data, weights)


def stat_rms(data: np.ndarray, ref_data: np.ndarray, weights: np.ndarray | None) -> np.float64:
    """
    Root mean square implementation.
    """
    difference = data - ref_data
    return np.sqrt(np.average(difference**2, weights=weights))


def stat_mb(data: np.ndarray, ref_data: np.ndarray, weights: np.ndarray | None) -> np.float64:
    """
    Mean bias implementation.
    """
    difference = data - ref_data
    return sum(difference, weights=weights) / len(data)


def stat_nmb(data: np.ndarray, ref_data: np.ndarray, weights: np.ndarray | None) -> np.float64:
    """
    Normalised mean bias implementation.
    """
    sum_ref_data = sum(ref_data, weights=weights)
    if sum_ref_data == 0:
        return 0
    return sum(data - ref_data, weights) / sum_ref_data


def stat_mab(data: np.ndarray, ref_data: np.ndarray, weights: np.ndarray | None) -> np.float64:
    """
    Mean absolute bias implementation.
    """
    difference = data - ref_data
    return sum(np.abs(difference)) / len(data)


@ignore_warnings(RuntimeWarning, "invalid value encountered in divide")
def stat_mnmb(data: np.ndarray, ref_data: np.ndarray, weights: np.ndarray | None) -> np.float64:
    """
    Modified normalised mean bias implementation.
    """
    difference = data - ref_data
    if np.all(np.isnan(difference)):
        return np.nan

    return 2 / len(data) * sum(difference / (data + ref_data))


@ignore_warnings(RuntimeWarning, "invalid value encountered in divide")
def stat_fge(data: np.ndarray, ref_data: np.ndarray, weights: np.ndarray | None) -> np.float64:
    """
    Fractional gross error implementation.
    """
    difference = data - ref_data
    if np.all(np.isnan(difference)):
        return np.nan

    return 2 / len(data) * sum(np.abs(difference / (data + ref_data)), weights=weights)


@ignore_warnings(
    ConstantInputWarning, "An input array is constant; the correlation coefficient is not defined."
)
def stat_R_spearman(
    data: np.ndarray, ref_data: np.ndarray, weights: np.ndarray | None
) -> np.float64:
    """
    Spearman corr. coefficient implementation.
    """
    return spearmanr(data, ref_data)[0]


def stat_R_kendall(
    data: np.ndarray, ref_data: np.ndarray, weights: np.ndarray | None
) -> np.float64:
    """
    Kendall's tau implementation.
    """
    return kendalltau(data, ref_data)[0]
