from collections.abc import Mapping

import numpy as np

from pyaerocom.stats.data_filters import FilterByLimit, FilterNaN
from pyaerocom.stats.implementations import (
    stat_fge,
    stat_mab,
    stat_mb,
    stat_mnmb,
    stat_nmb,
    stat_R,
    stat_R_kendall,
    stat_R_spearman,
    stat_rms,
)
from pyaerocom.stats.stat_filters import FilterDropStats
from pyaerocom.stats.types import DataFilter, StatisticsCalculator, StatisticsFilter, StatsDict


def _filter_data(
    data: np.ndarray,
    ref_data: np.ndarray,
    weights: np.ndarray,
    filters=list[DataFilter] | None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Filter data arrays using provided filter functions.

    Parameters
    ----------
    data : np.ndarray
    ref_data : np.ndarray
    weights : np.ndarray | None
    filters : list[DataFilter] | None

    Returns
    -------
    Tuple
        tuple consisting of the modified data, ref_data and optional weights array.

    Raises:
    -------
    IndexError:
        If the length of a produced mask does not match the length of the data.
    """
    if filters is not None:
        for f in filters:
            mask = f(data, ref_data, weights)
            if len(mask) != len(data):
                raise IndexError(
                    f"Filter mask length ({len(mask)}) does not match length of data ({len(data)})."
                )
            if weights is None:
                data, ref_data, weights = data[mask], ref_data[mask], None
            else:
                data, ref_data, weights = data[mask], ref_data[mask], weights[mask]

    return (data, ref_data, weights)


def _prepare_statistics(
    data: np.ndarray,
    ref_data: np.ndarray,
    weights: np.ndarray,
    statistics=dict[str, StatisticsCalculator],
    min_numvalid: int = 1,
) -> StatsDict:
    """Calculates configured statistics for two one-dimensional data arrays.

    Parameters
    ----------
    data : np.ndarray
    ref_data : np.ndarray
    weights : np.ndarray | None
        Optional list of weights which will be used for weighted statistics.
    statistics : dict[str, StatisticsCalculator]
        Mapping between names and functions that calculate individual statistics.
    min_numvalid: int
        Minmium number of data points required. If data is lower than this threshold,
        stats will be set to NaN.

    Returns
    -------
    StatsDict
        Dictionary with the calculated statistics. The structure of the return dictionary mirrors
        the statistics parameter.

    Calculates the statistics configured by statistics returning them as a StatsDict.
    """
    result = dict()
    for name, stat in statistics.items():
        if len(data) >= min_numvalid:
            # Rounding to ensure values aren't out of bounds due to floating point
            # arithmetic and to reduce json file size.
            result[name] = np.round(stat(data, ref_data, weights), decimals=6)
        else:
            result[name] = np.nan

    return result


def _filter_stats(
    stats: StatsDict, filters: list[StatisticsFilter] | None
) -> dict[str, np.float64]:
    """Filter a StatsDict

    Filters a StatsDict, dropping values or statistics.

    Parameters
    ----------
    stats : StatsDict
        The StatsDict to be filtered.
    filters
        A list of filter callables which are applied to the dict. The functions
        should take a dict and return the modified dict.

    Returns
    -------
    StatsDict
        The filtered StatsDict.
    """
    if filters is not None:
        for f in filters:
            stats = f(stats)

    return stats


def _get_default_statistic_config() -> dict[str, StatisticsCalculator]:
    """
    Returns a base configuration dictionary to be used with `calculate_statistics`
    which calculates all implemented statistics. Can be used as a starting
    point for adding additional stats using `dict.update()`
    """
    return {
        "refdata_mean": lambda x, y, w: np.nanmean(y),
        "refdata_std": lambda x, y, w: np.nanstd(y),
        "data_mean": lambda x, y, w: np.nanmean(x),
        "data_std": lambda x, y, w: np.nanstd(x),
        "rms": stat_rms,
        "nmb": stat_nmb,
        "mnmb": stat_mnmb,
        "mb": stat_mb,
        "mab": stat_mab,
        "fge": stat_fge,
        "R": stat_R,
        "R_spearman": stat_R_spearman,
        "R_kendall": stat_R_kendall,
    }


def calculate_statistics(
    data,
    ref_data,
    statistics: Mapping[str, StatisticsCalculator] | None = None,
    min_num_valid=1,
    weights: list | None = None,
    drop_stats=None,
    lowlim=None,
    highlim=None,
) -> StatsDict:
    """Calc statistical properties from two data arrays

    Filters data, calculates statistics and filters the resulting dict. If
    `statistics` is None the following statistics will be calculated by
    default.

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
        - R_kendall (Kendall's tau) ->

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
    statistics : dict[str, StatisticsCalculator]
        mapping between statistics name and Callable to calculate that statistics.
    lowlim : float
        lower end of considered value range (e.g. if set 0, then all datapoints
        where either ``data`` or ``ref_data`` is smaller than 0 are removed).
        Deprecated. Use data_filters with FilterByLimit instead.
    highlim : float
        upper end of considered value range
        Deprecated. Use data_filters with FilterByLimit instead.
    min_num_valid : int
        minimum number of valid measurements required to compute statistical
        parameters. Stat will be returned as NaN if length(data) is below this threshold.
    weights: ndarray
        array containing weights if computing weighted statistics.
    drop_stats: tuple
        tuple which drops the provided statistics from computed json files.
        For example, setting drop_stats = ("mb", "mab"), results in json files
        in hm/ts with entries which do not contain the mean bias and mean
        absolute bias, but the other statistics are preserved.
    Returns
    -------
    StatsDict
        dictionary containing computed statistics. Return mapping is the same as
        provided in `statistics`. Additionally a value for `totnum` (the unfiltered
        length of the data) and `weighted` (whether calculations was performed
        weighted or not) will be included.

    Raises
    ------
    ValueError
        if either of the input arrays has dimension other than 1
    ValueError
        if length of data is different to length of ref_data.
    ValueError
        if length of weights is different to length of data (assuming weights != None)
    """
    data = np.asarray(data)
    ref_data = np.asarray(ref_data)

    # Validation
    if not data.ndim == 1 or not ref_data.ndim == 1:
        raise ValueError("Invalid input. Data arrays must be one dimensional")

    if len(data) != len(ref_data):
        raise ValueError("Length mismatch between data and ref_data.")

    if weights is not None:
        if len(weights) != len(data):
            raise ValueError("Invalid input. Length of weights must match length of data.")

    # Set defaults
    if statistics is None:
        statistics = _get_default_statistic_config()

    data_filters = [FilterNaN()]
    if (lowlim is not None) or (highlim is not None):
        data_filters.append(FilterByLimit(lowlim=lowlim, highlim=highlim))

    stats_filters = None
    if drop_stats is not None:
        stats_filters = [FilterDropStats(drop_stats)]

    result = dict()

    result["totnum"] = len(data)
    result["weighted"] = False if weights is None else True

    data, ref_data, weights = _filter_data(data, ref_data, weights, data_filters)

    result["num_valid"] = float(len(data))

    if weights is None:
        weights = np.repeat([1], len(data))

    if len(weights) > 0:
        weights = weights / np.max(weights)

    additional_stats = _prepare_statistics(
        data, ref_data, weights, statistics, min_numvalid=min_num_valid
    )
    result.update(additional_stats)

    result = _filter_stats(result, stats_filters)

    return result


def _init_stats_dummy(drop_stats=None):
    # dummy for statistics dictionary for locations without data
    stats_dummy = {}
    for k in calculate_statistics([1], [1], drop_stats=drop_stats):
        stats_dummy[k] = np.nan

    # Test to make sure these variables are defined even when yearly and season != all
    stats_dummy["R_spatial_mean"] = np.nan
    stats_dummy["R_spatial_median"] = np.nan
    stats_dummy["R_temporal_mean"] = np.nan
    stats_dummy["R_temporal_median"] = np.nan

    return stats_dummy
