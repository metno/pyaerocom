import numpy as np

StatisticsConstraint = callable[[np.array, np.array], tuple[np.array, np.array]]

StatisticsCalculator = callable[[np.array, np.array], np.float64]


## Constraints
class LimitConstraint:
    """
    Excludes data that lies outside of a lower and/or upper limit.
    """

    def __init__(self, lowlim: int = None, highlim: int = None):
        self.lowlim = lowlim
        self.highlim = highlim

    def __call__(self, data: np.array, ref_data: np.array) -> tuple[np.array, np.array]:
        if self.lowlim is not None:
            valid = np.logical_and(data > self.lowlim, ref_data > self.lowlim)
            data = data[valid]
            ref_data = ref_data[valid]
        if self.highlim is not None:
            valid = np.logical_and(data < self.highlim, ref_data < self.highlim)
            data = data[valid]
            ref_data = ref_data[valid]

        return (data, ref_data)


class NaNConstraint:
    """
    Excludes data for which either data or ref_data is NaN.
    """

    def __call__(self, data: np.array, ref_data: np.array) -> tuple[np.array, np.array]:
        mask = ~np.isnan(ref_data) * ~np.isnan(data)

        return (data[mask], ref_data[mask])


def calc_statistics(
    data,
    ref_data,
    data_constraints: list[StatisticsConstraint] | None = None,
    min_num_valid=1,
    weights: list | None = None,
    drop_stats=None,
):
    data = np.asarray(data)
    ref_data = np.asarray(ref_data)

    if not data.ndim == 1 or not ref_data.ndim == 1:
        raise ValueError("Invalid input. Data arrays must be one dimensional")

    if len(data) != len(ref_data) != len(weights):
        raise ValueError("Length mismatch between data and ref_data.")

    result = dict()

    result["totnum"] = float(len(data))

    # Apply constraints to the data.
    if data_constraints is not None:
        for c in data_constraints:
            data, ref_data = c(data, ref_data)

    result["num_valid"] = float(len(data))

    result["refdata_mean"] = np.nanmean(ref_data)
    result["refdata_std"] = np.nanstd(ref_data)
    result["data_mean"] = np.nanmean(data)
    result["data_std"] = np.nanstd(data)
