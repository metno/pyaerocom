import numpy as np
import pytest

from pyaerocom.mathutils import (
    _nanmean_and_std,
    calc_statistics,
    estimate_value_range,
    exponent,
    is_strictly_monotonic,
    make_binlist,
)


@pytest.mark.parametrize("vmin, vmax, num", [(0, 1, 10), (0.345, 0.346, 100), (-2, -10, 5)])
def test_make_binlist(vmin, vmax, num):
    bins = make_binlist(vmin, vmax, num)
    assert isinstance(bins, list)
    assert bins[0] == vmin
    assert bins[-1] == vmax
    assert len(bins) == num + 1


@pytest.mark.parametrize(
    "inputval,result", [([1, 2], True), ([1], True), ([1, 2, 2], False), ([3, 2], False)]
)
def test_is_strictly_monotonic(inputval, result):
    assert is_strictly_monotonic(inputval) == result


@pytest.mark.parametrize("inputval, desired", [(0.01, -2), (4, 0), (234, 2)])
def test_exponent(inputval, desired):
    assert exponent(inputval) == desired


@pytest.mark.parametrize(
    "data,expected",
    [
        ([1], (1, 0)),
        (np.asarray([1]), (1, 0)),
        ([1, np.nan], (1, 0)),
        ([np.nan, np.nan], (np.nan, np.nan)),
        (np.random.normal(loc=3, scale=0.01, size=100000), (3, 0.01)),
        ([1, np.nan, 0, 2], (1, 0.816497)),
    ],
)
def test__nanmean_and_std(data, expected):
    assert _nanmean_and_std(data) == pytest.approx(expected, abs=0.001, rel=1e-2, nan_ok=True)


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
    stats = calc_statistics(data, ref_data)
    assert isinstance(stats, dict)
    assert len(stats) == len(expected)
    for key, val in expected.items():
        assert key in stats
        assert stats[key] == pytest.approx(val, abs=0.02, rel=0.01, nan_ok=True)


def test_calc_statistics_error():
    with pytest.raises(IndexError) as e:
        calc_statistics([1], [1, np.nan])
    assert str(e.value).startswith("boolean index did not match indexed array")


@pytest.mark.parametrize(
    "vmin,vmax,extend_percent,result",
    [
        (0, 1, 0, (0, 1)),
        (-0.012, 3.12345666, 0, (-0.02, 3.13)),
        (-0.012, 3.12345666, 5, (-0.2, 3.3)),
    ],
)
def test_estimate_value_range(vmin, vmax, extend_percent, result):
    vals = estimate_value_range(vmin, vmax, extend_percent)
    assert vals == pytest.approx(result, rel=1e-3)


def test_estimate_value_range_error():
    with pytest.raises(ValueError) as e:
        estimate_value_range(0, 0)
    assert str(e.value) == "vmax needs to exceed vmin"
