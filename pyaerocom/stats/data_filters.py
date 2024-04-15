import numpy as np


class FilterNaN:
    """
    Excludes data for which either data or ref_data is NaN.
    """

    def __call__(
        self, data: np.ndarray, ref_data: np.ndarray, weights: np.ndarray | None
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray | None]:
        mask = ~np.isnan(ref_data) * ~np.isnan(data)

        if weights is not None:
            return (data[mask], ref_data[mask], weights[mask])

        return (data[mask], ref_data[mask], None)


class FilterByLimit:
    """
    Filters out data which is outside of a lower and / or upper limit.
    """

    def __init__(self, lowlim: float | None, highlim: float | None):
        self.lowlim = lowlim
        self.highlim = highlim

    def __call__(
        self, data: np.ndarray, ref_data: np.ndarray, weights: np.ndarray | None
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray | None]:
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
