from typing import Callable, Mapping, Optional

import numpy as np
from scipy.stats import kendalltau, spearmanr

from .mathutils import corr, sum

# Type definition for a callable which filters (ie. excludes) data before calculating stats.
DataFilter = Callable[
    [np.array, np.array, Optional[np.array]], tuple[np.array, np.array, Optional[np.array]]
]

# Type definition for a callable which calculates a statistic.
StatisticsCalculator = Callable[[np.array, np.array, Optional[np.array]], np.float64]

# Type definition for a callable which filters out statistics from the resulting stats dictionary.
StatisticsFilter = Callable[[dict[str, np.float64]], dict[str, np.float64]]

# Type definition for a stats dictionary.
StatsDict = dict[str, np.float64]


class FilterNaN:
    """
    Excludes data for which either data or ref_data is NaN.
    """

    def __call__(
        self, data: np.array, ref_data: np.array, weights: Optional[np.array]
    ) -> tuple[np.array, np.array, Optional[np.array]]:
        mask = ~np.isnan(ref_data) * ~np.isnan(data)

        if weights is not None:
            return (data[mask], ref_data[mask], weights[mask])

        return (data[mask], ref_data[mask], None)


## Statistics
def stat_R(data: np.array, ref_data: np.array, weights: Optional[np.array]) -> np.float64:
    """
    Pearson correlation coefficient implementation.
    """
    return corr(data, ref_data, weights)


def stat_rms(data: np.array, ref_data: np.array, weights: Optional[np.array]) -> np.float64:
    """
    Root mean square implementation.
    """
    difference = data - ref_data
    return np.sqrt(np.average(difference**2, weights=weights))


def stat_mb(data: np.array, ref_data: np.array, weights: Optional[np.array]) -> np.float64:
    """
    Mean bias implementation.
    """
    difference = data - ref_data
    return sum(difference, weights=weights) / len(data)


def stat_nmb(data: np.array, ref_data: np.array, weights: Optional[np.array]) -> np.float64:
    """
    Normalised mean bias implementation.
    """
    sum_ref_data = sum(ref_data, weights=weights)
    if sum_ref_data == 0:
        return 0
    return sum(data - ref_data, weights) / sum_ref_data


def stat_mab(data: np.array, ref_data: np.array, weights: Optional[np.array]) -> np.float64:
    """
    Mean absolute bias implementation.
    """
    difference = data - ref_data
    return sum(np.abs(difference)) / len(data)


def stat_mnmb(data: np.array, ref_data: np.array, weights: Optional[np.array]) -> np.float64:
    """
    Modified normalised mean bias implementation.
    """
    difference = data - ref_data
    if np.all(np.isnan(difference)):
        return np.nan

    return 2 / len(data) * sum(difference / (data + ref_data))


def stat_fge(data: np.array, ref_data: np.array, weights: Optional[np.array]) -> np.float64:
    """
    Fractional gross error implementation.
    """
    difference = data - ref_data
    if np.all(np.isnan(difference)):
        return np.nan

    return 2 / len(data) * sum(np.abs(difference / (data + ref_data)), weights=weights)


def stat_R_spearman(data: np.array, ref_data: np.array, weights: Optional[np.array]) -> np.float64:
    """
    Spearman corr. coefficient implementation.
    """
    return spearmanr(data, ref_data)[0]


def stat_R_kendall(data: np.array, ref_data: np.array, weights: Optional[np.array]) -> np.float64:
    """
    Kendall's tau implementation.
    """
    return kendalltau(data, ref_data)[0]


def filter_data(
    data: np.array,
    ref_data: np.array,
    weights: Optional[np.array],
    filters=Optional[list[DataFilter]],
) -> tuple[np.array, np.array, np.array]:
    """Filter data arrays using provided filter functions.

    Parameters
    ----------
    data : np.array
    ref_data : np.array
    weights : np.array | None
    filters : list[DataFilter] | None

    Returns
    -------
    Tuple
        tuple consisting of the modified data, ref_data and weights array.
    """
    if filters is not None:
        for f in filters:
            data, ref_data, weights = f(data, ref_data, weights)

    return (data, ref_data, weights)


def calculate_statistics(
    data: np.array,
    ref_data: np.array,
    weights: np.array,
    statistics=dict[str, StatisticsCalculator],
    min_numvalid: int = 1,
) -> StatsDict:
    """Calculates configured statistics for two one-dimensional data arrays.

    Parameters
    ----------
    data : np.array
    ref_data : np.array
    weights : np.array | None
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
            result[name] = stat(data, ref_data, weights)
        else:
            result[name] = np.nan

    return result


def filter_stats(
    stats: StatsDict, filters: Optional[list[StatisticsFilter]]
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


class DropStats:
    def __init__(self, stats_to_drop: list[str]):
        self.stats_to_drop = stats_to_drop

    def __call__(self, stats: StatsDict) -> StatsDict:
        for k in self.stats_to_drop:
            if k in stats.keys():
                del stats[k]

        return stats


class FilterByLimit:
    def __init__(self, lowlim: float | None, highlim: float | None):
        self.lowlim = lowlim
        self.highlim = highlim

    def __call__(
        self, data: np.array, ref_data: np.array, weights: Optional[np.array]
    ) -> tuple[np.array, np.array, Optional[np.array]]:
        if self.lowlim is not None:
            valid = np.logical_and(data > self.lowlim, ref_data > self.lowlim)
            data = data[valid]
            ref_data = ref_data[valid]
            if weights is not None:
                weights = weights[valid]
        if self.highlim is not None:
            valid = np.logical_and(data < self.highlim, ref_data < self.highlim)
            data = data[valid]
            ref_data = ref_data[valid]
            if weights is not None:
                weights = weights[valid]

        return (data, ref_data, weights)


def calc_statistics_helper(
    data,
    ref_data,
    statistics: Mapping[str, StatisticsCalculator] | None = None,
    data_filters: list[DataFilter] | None = None,
    stats_filters: list[StatisticsFilter] | None = None,
    min_num_valid=1,
    weights: list | None = None,
    drop_stats=None,
    lowlim=None,
    highlim=None,
) -> StatsDict:
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
    data_filters : Optional[list[DataFilter]]
        list of filter functions applied to the data arrays before calculating stats.
    statistics : dict[str, StatisticsCalculator]
        mapping between statistics name and functions to calculate that statistics.
    stats_filter : Optional[list[StatisticsFilter]]
        list of filter functions applied to the stats dictionary before returning the dict.
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
        Deprecated. Use stats_filter with instance of DropStats instead.
    Returns
    -------
    StatsDict
        dictionary containing computed statistics. Return mapping is the same as
        provided in `statistics`.

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

    #### ----- BACKWARDS COMPATIBILITY ------
    # TODO: This logic ensures backward compatibility with the old mathutils.calc_stats()
    # version. It should be removed at a later date.

    if statistics is None:
        statistics = {
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

    if data_filters is None:
        data_filters = [FilterNaN()]

    if (stats_filters is None) and (drop_stats is not None):
        stats_filters = [DropStats(drop_stats)]

    if (lowlim is not None) or (highlim is not None):
        data_filters.append(FilterByLimit(lowlim=lowlim, highlim=highlim))
    #### ----- END BACKWARDS COMPATIBILITY

    result = dict()

    result["totnum"] = float(len(data))
    result["weighted"] = False if weights is None else True

    data, ref_data, weights = filter_data(data, ref_data, weights, data_filters)

    result["num_valid"] = float(len(data))

    if weights is None:
        weights = np.repeat([1], len(data))

    if len(weights) > 0:
        weights = weights / np.max(weights)

    additional_stats = calculate_statistics(
        data, ref_data, weights, statistics, min_numvalid=min_num_valid
    )
    result.update(additional_stats)

    result = filter_stats(result, stats_filters)

    return result
