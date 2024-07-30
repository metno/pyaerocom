import numpy as np
import pytest

from pyaerocom.stats.data_filters import FilterByLimit, FilterNaN


@pytest.mark.parametrize(
    "data,ref_data,expected_mask",
    (
        pytest.param(
            np.asarray([1, 2, 3, 4]), np.asarray([1, 2, 3, 4]), np.repeat([True], 4), id="no-nan"
        ),
        pytest.param(
            np.repeat([np.nan], 10), np.repeat([np.nan], 10), np.repeat(False, 10), id="only-nan"
        ),
        pytest.param(
            np.asarray([np.nan, 5] * 6),
            np.asarray([np.nan, 5, 3] * 4),
            np.asarray([False, True, False, False, False, True] * 2),
            id="mixed-nan",
        ),
    ),
)
def test_filter_nan(data, ref_data, expected_mask):
    filternan = FilterNaN()

    mask = filternan(data, ref_data, None)

    assert len(mask) == len(data)
    assert np.array_equal(mask, expected_mask, equal_nan=True)


@pytest.mark.parametrize(
    "data,ref_data,lowlim,highlim,expected_mask",
    (
        pytest.param(
            np.asarray([1, 2, 3, 4] * 5),
            np.asarray([5, 4] * 10),
            None,
            None,
            np.asarray([True] * 20),
            id="no-limit",
        ),
        pytest.param(
            np.asarray([1, 2, 3, 4] * 5),
            np.asarray([1, 2, 3, 4] * 5),
            3,
            None,
            np.asarray([False, False, False, True] * 5),
            id="low-limit",
        ),
        pytest.param(
            np.asarray([1, 2, 3, 4] * 5),
            np.asarray([1, 2, 3, 4] * 5),
            None,
            2,
            np.asarray([True, False, False, False] * 5),
            id="high-limit",
        ),
        pytest.param(
            np.asarray([1, 2, 3, 4] * 5),
            np.asarray([1, 2, 3, 4] * 5),
            1,
            4,
            np.asarray([False, True, True, False] * 5),
            id="both-limits",
        ),
    ),
)
def test_filterbylimit(data, ref_data, lowlim, highlim, expected_mask):
    filterbylimit = FilterByLimit(lowlim=lowlim, highlim=highlim)

    mask = filterbylimit(data, ref_data, None)

    assert len(mask) == len(data)
    assert np.array_equal(mask, expected_mask, equal_nan=True)
