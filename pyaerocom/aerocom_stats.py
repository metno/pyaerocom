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


## Constraints
class LimitConstraint:
    """
    Excludes data that lies outside of a lower and/or upper limit.
    """

    def __init__(self, lowlim: int = None, highlim: int = None):
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


class NaNConstraint:
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
    return sum(difference, weights=weights)


def stat_nmb(data: np.array, ref_data: np.array, weights: Optional[np.array]) -> np.float64:
    """
    Normalised mean bias implementation.
    """
    sum_ref_data = sum(ref_data, weights=weights)
    if sum_ref_data == 0:
        return 0
    return stat_mb(data, ref_data, weights) / sum_ref_data


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
    if filters is not None:
        for f in filters:
            data, ref_data, weights = f(data, ref_data, weights)

    return (data, ref_data, weights)


def filter_stats(
    stats: StatsDict, filters: Optional[list[StatisticsFilter]]
) -> dict[str, np.float64]:
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


def calc_statistics(
    data,
    ref_data,
    statistics: Mapping[str, StatisticsCalculator] | None = None,
    data_filters: list[DataFilter] | None = None,
    stats_filters: list[StatisticsFilter] | None = None,
    min_num_valid=1,
    weights: list | None = None,
    drop_stats=None,
) -> StatsDict:
    data = np.asarray(data)
    ref_data = np.asarray(ref_data)

    # Validation
    if not data.ndim == 1 or not ref_data.ndim == 1:
        raise ValueError("Invalid input. Data arrays must be one dimensional")

    # TODO: Should check length of weights as well if provided.
    # TODO: Currently not testing this because broken backwards compat.
    # if len(data) != len(ref_data):
    #     raise ValueError("Length mismatch between data and ref_data.")

    #### ----- BACKWARDS COMPATIBILITY ------
    # TODO: This logic ensures backwards compatibility with the old mathutils.calc_stats()
    # version. It may be removed at a later date.

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
        data_filters = [NaNConstraint()]

    if (stats_filters is None) and (drop_stats is not None):
        stats_filters = [DropStats(drop_stats)]

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

    for name, stat in statistics.items():
        if result["num_valid"] >= min_num_valid:
            result[name] = stat(data, ref_data, weights)
        else:
            result[name] = np.nan

    result = filter_stats(result, stats_filters)

    return result
