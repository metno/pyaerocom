import numpy as np
import pytest
from numpy.testing import assert_allclose

from pyaerocom.aux_var_helpers import (
    _calc_od_helper,
    calc_ang4487aer,
    calc_od550aer,
    calc_od550gt1aer,
    calc_od550lt1aer,
    compute_angstrom_coeff,
    compute_od_from_angstromexp,
)


def test_calc_ang4487aer():
    data = {}
    with pytest.raises(AttributeError):
        calc_ang4487aer(data)

    data["od440aer"] = 0.2
    with pytest.raises(AttributeError):
        calc_ang4487aer(data)

    data["od870aer"] = 0.1
    vals = calc_ang4487aer(data)
    assert_allclose(vals, 1, atol=0.05)


def test_calc_od550aer():
    data = dict(od500aer=0.1, ang4487aer=1)

    val = calc_od550aer(data)
    assert_allclose(val, 0.09, atol=0.05)

    od440 = _calc_od_helper(
        data,
        "od440aer",
        to_lambda=0.44,
        od_ref="od500aer",
        lambda_ref=0.5,
        use_angstrom_coeff="ang4487aer",
    )
    assert_allclose(od440, 0.11, atol=0.05)

    data = dict(od440aer=od440, ang4487aer=1)
    val = calc_od550aer(data)
    assert_allclose(val, 0.09, atol=0.05)


def test_calc_od550gt1aer():
    data = dict(od500gt1aer=0.1, ang4487aer=1)

    val = calc_od550gt1aer(data)
    assert_allclose(val, 0.09, atol=0.05)


def test_calc_od550lt1aer():
    data = dict(od500lt1aer=0.1, ang4487aer=1)

    val = calc_od550lt1aer(data)
    assert_allclose(val, 0.09, atol=0.05)


@pytest.mark.parametrize(
    "od1,od2,lambda1,lambda2",
    [
        (0.1, 0.2, 0.6, 0.3),
        (0.1, 0.2, 0.3, 0.6),
    ],
)
def test_compute_angstrom_coeff(od1, od2, lambda1, lambda2):
    ae = compute_angstrom_coeff(od1, od2, lambda1, lambda2)
    expected = -np.log(od1 / od2) / np.log(lambda1 / lambda2)
    assert_allclose(ae, expected, atol=1e-5)


def test_compute_od_from_angstromexp():
    val = compute_od_from_angstromexp(to_lambda=0.3, od_ref=0.1, lambda_ref=0.5, angstrom_coeff=4)
    assert_allclose(val, 0.77, atol=0.05)

    val = compute_od_from_angstromexp(to_lambda=0.3, od_ref=0.1, lambda_ref=0.5, angstrom_coeff=0)
    assert_allclose(val, 0.1, atol=0.05)


def test__calc_od_helper():
    data = dict(
        od500aer=np.asarray([2, 2, np.nan, 2, np.nan, np.nan]),
        od440aer=np.ones(6) * 4,
        ang4487aer=np.zeros(6),
    )
    result = _calc_od_helper(
        data, "od550aer", 0.55, "od500aer", 0.5, "od440aer", 0.44, "ang4487aer"
    )

    assert len(result) == 6
    assert result.mean() == 3
