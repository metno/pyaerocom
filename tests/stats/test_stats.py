import numpy as np
import pytest

from pyaerocom.stats.implementations import stat_mb, stat_R, stat_R_kendall
from pyaerocom.stats.stats import calculate_statistics


def test_calc_stats_exceptions():
    with pytest.raises(ValueError):
        calculate_statistics(
            np.asarray([[1, 2, 3, 4], [1, 2, 3, 4]]), np.asarray([[1, 2, 3, 4], [1, 2, 3, 4]])
        )

    with pytest.raises(ValueError):
        calculate_statistics([1, 2, 3, 4], [1, 2, 3, 4], weights=[1, 2, 3])

    with pytest.raises(ValueError):
        calculate_statistics([1, 2, 3], [1, 2])

    with pytest.raises(ValueError):
        calculate_statistics([1, 2, 3], [1, 2, 3], weights=[1, 2])


@pytest.mark.parametrize(
    "data,ref_data,statistics,expected_keys",
    (
        pytest.param(
            [1, 2, 3, 4], [1, 2, 3, 4], {}, ["totnum", "weighted", "num_valid"], id="empty"
        ),
        pytest.param(
            [1, 2, 3, 4],
            [1, 2, 3, 4],
            {"R": stat_R, "R_kendall": stat_R_kendall, "mb": stat_mb},
            ["totnum", "weighted", "num_valid", "R", "R_kendall", "mb"],
            id="custom1",
        ),
        pytest.param(
            [1, 2, 3, 4],
            [1, 2, 3, 4],
            None,
            [
                "totnum",
                "weighted",
                "num_valid",
                "R",
                "R_kendall",
                "R_spearman",
                "fge",
                "mab",
                "mab",
                "mb",
                "mnmb",
                "nmb",
                "rms",
                "data_mean",
                "data_std",
                "refdata_mean",
                "refdata_std",
            ],
            id="stats-none",
        ),
    ),
)
def test_calc_stats_keys(data, ref_data, statistics, expected_keys):
    stats = calculate_statistics(data, ref_data, statistics)

    assert isinstance(stats, dict)

    for k in expected_keys:
        assert k in stats.keys()

    for k in stats.keys():
        assert k in expected_keys


def test_custom_stats():
    stats = calculate_statistics(
        [1, 2, 3, 4],
        [1, 2, 3, 4],
        {"test_statistic1": lambda x, y, w: 5, "test_statistic2": lambda x, y, w: 3},
    )

    assert "test_statistic1" in stats.keys()
    assert "test_statistic2" in stats.keys()
    assert stats["test_statistic1"] == 5
    assert stats["test_statistic2"] == 3


perfect_stats_num1_mean1 = {
    "totnum": 1,
    "num_valid": 1,
    "refdata_mean": 1,
    "refdata_std": 0,
    "data_mean": 1,
    "data_std": 0,
    "weighted": False,
    "rms": 0,
    "nmb": 0,
    "mnmb": 0,
    "mb": 0,
    "mab": 0,
    "fge": 0,
    "R": np.nan,
    "R_kendall": np.nan,
    "R_spearman": np.nan,
}
perfect_stats_num2_mean1 = perfect_stats_num1_mean1.copy()
perfect_stats_num2_mean1.update(totnum=2)

num_fakedata = 1000
zero_signal = np.zeros(num_fakedata)
noise = np.random.normal(loc=0, scale=0.01, size=num_fakedata)

idx = np.linspace(0, 2 * np.pi, num_fakedata)
sin_signal = np.sin(idx)


@pytest.mark.parametrize(
    "data,ref_data,expected",
    [
        ([1], [1], perfect_stats_num1_mean1),
        ([1, np.nan], [1, np.nan], perfect_stats_num2_mean1),
        (
            zero_signal,
            zero_signal,
            {
                "totnum": 1000.0,
                "num_valid": 1000.0,
                "refdata_mean": 0.0,
                "refdata_std": 0,
                "data_mean": 0.0,
                "data_std": 0,
                "weighted": False,
                "rms": 0.0,
                "R": np.nan,
                "R_spearman": np.nan,
                "R_kendall": np.nan,
                "nmb": 0,
                "mb": 0,
                "mab": 0,
                "mnmb": np.nan,
                "fge": np.nan,
            },
        ),
        (
            zero_signal,
            noise,
            {
                "totnum": 1000.0,
                "num_valid": 1000.0,
                "refdata_mean": 0.0,
                "refdata_std": 0,
                "data_mean": 0.0,
                "data_std": 0,
                "weighted": False,
                "rms": 0.0,
                "R": np.nan,
                "R_spearman": np.nan,
                "R_kendall": np.nan,
                "nmb": -1,
                "mb": 0,
                "mab": 0,
                "mnmb": -2,
                "fge": 2,
            },
        ),
        (
            sin_signal,
            sin_signal,
            {
                "totnum": 1000.0,
                "num_valid": 1000.0,
                "refdata_mean": 0.0,
                "refdata_std": 0.71,
                "data_mean": 0.0,
                "data_std": 0.71,
                "weighted": False,
                "rms": 0.0,
                "R": 1.0,
                "R_spearman": 1.0,
                "R_kendall": 1.0,
                "nmb": 0,
                "mb": 0,
                "mab": 0,
                "mnmb": np.nan,
                "fge": np.nan,
            },
        ),
    ],
)
def test_calc_statistics(data, ref_data, expected):
    stats = calculate_statistics(data, ref_data)
    assert isinstance(stats, dict)
    assert len(stats) == len(expected)
    for key, val in expected.items():
        assert key in stats
        assert stats[key] == pytest.approx(val, abs=0.02, rel=0.01, nan_ok=True)


@pytest.mark.parametrize(
    "data,ref_data,drop",
    (
        pytest.param(tuple(), tuple(), tuple(), id="empty-data"),
        pytest.param(tuple(), tuple(), ("R", "R_kendall"), id="empty-data-with-drop"),
        pytest.param((1, 2, 3, 4), (1, 2, 3, 4), ("R", "R_kendall"), id="small-data"),
        (
            (1,),
            (2,),
            (
                "nmb",
                "mnmb",
                "mb",
                "mab",
                "R",
                "R_spearman",
                "R_kendall",
                "fge",
                "nrms",
                "rms",
                "data_mean",
                "data_std",
                "weighted",
            ),
        ),
    ),
)
def test_calc_statistics_drop_stats(data, ref_data, drop):
    stats = calculate_statistics(data, ref_data, drop_stats=drop)

    assert all([x not in stats.keys() for x in drop])


def test_fairmode_R_in_expected_range():
    # This test is meant to test for a specific issue where
    # using fairmode=true would result in errors due to the calculated
    # R values being slightly out of range -1<=R<=1. The error is caused
    # because fairmode_stats() expects R values exactly in the range, but
    # values may be outside due to floating point shenanigans.
    # https://xkcd.com/217/
    # As of the time of writing this test, the data used for this test is
    # known to result in a failing test, IF *no* rounding is applied in
    # `stats.stats._prepare_statistics().`
    # https://github.com/metno/pyaerocom/pull/1142
    data1 = np.asarray([17.2073523845202, 15.543783901903302, np.nan])
    data2 = np.asarray([15.046913580246915, 18.462202650290884, np.nan])

    stats = calculate_statistics(data1, data2)

    assert -1 <= stats["R"] <= 1
