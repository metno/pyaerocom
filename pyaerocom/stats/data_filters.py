import numpy as np


class FilterNaN:
    """
    Excludes data for which either data or ref_data is NaN.
    """

    def __call__(
        self, data: np.ndarray, ref_data: np.ndarray, weights: np.ndarray | None
    ) -> np.ndarray:
        mask = ~np.isnan(ref_data) * ~np.isnan(data)

        return mask


class FilterByLimit:
    """
    Filters out data which is outside of a lower and / or upper limit.
    """

    def __init__(self, lowlim: float | None, highlim: float | None):
        self.lowlim = lowlim
        self.highlim = highlim

    def __call__(
        self, data: np.ndarray, ref_data: np.ndarray, weights: np.ndarray | None
    ) -> np.ndarray:
        valid1 = np.repeat([True], len(data))
        valid2 = np.repeat([True], len(data))

        if self.lowlim is not None:
            valid1 = np.logical_and(data > self.lowlim, ref_data > self.lowlim)
        if self.highlim is not None:
            valid2 = np.logical_and(data < self.highlim, ref_data < self.highlim)

        return valid1 * valid2
