import pytest

from pyaerocom.mathutils import estimate_value_range, exponent, is_strictly_monotonic, make_binlist


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
