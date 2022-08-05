from __future__ import annotations

import numpy as np
import pytest

from pyaerocom.aux_var_helpers import (
    _calc_od_helper,
    calc_abs550aer,
    calc_ang4487aer,
    calc_od550aer,
    calc_od550gt1aer,
    calc_od550lt1aer,
    compute_angstrom_coeff,
    compute_od_from_angstromexp,
    vmrx_to_concx,
)


def test_calc_ang4487aer():
    data = dict(od440aer=0.2, od870aer=0.1)

    vals = calc_ang4487aer(data)
    assert vals == pytest.approx(1, abs=0.05)


@pytest.mark.parametrize(
    "data",
    [
        pytest.param(dict(), id="missing both"),
        pytest.param(dict(od440aer=0.2), id="missing od870aer"),
        pytest.param(dict(od870aer=0.1), id="missing od440aer"),
    ],
)
def test_calc_ang4487aer_error(data: dict):
    error = "Either of the two (or both) required variables (od440aer, od870aer) are not available in data"
    with pytest.raises(AttributeError) as e:
        calc_ang4487aer(data)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "data,args,kwargs,result",
    [
        pytest.param(
            dict(od500aer=0.1, ang4487aer=1),
            ("od440aer",),
            dict(
                to_lambda=0.44, od_ref="od500aer", lambda_ref=0.5, use_angstrom_coeff="ang4487aer"
            ),
            0.11,
            id="1 data point",
        ),
        pytest.param(
            dict(
                od500aer=np.asarray([2, 2, np.nan, 2, np.nan, np.nan]),
                od440aer=np.ones(6) * 4,
                ang4487aer=np.zeros(6),
            ),
            ("od550aer", 0.55, "od500aer", 0.5, "od440aer", 0.44, "ang4487aer"),
            {},
            [2, 2, 4, 2, 4, 4],
            id="6 data points",
        ),
    ],
)
def test__calc_od_helper(data: dict, args: tuple, kwargs: dict, result: float | list[float]):
    aod = _calc_od_helper(data, *args, **kwargs)
    assert aod == pytest.approx(result, abs=0.05)


@pytest.mark.parametrize(
    "data,result",
    [
        pytest.param(dict(od500aer=0.1, ang4487aer=1), 0.09, id="simple"),
        pytest.param(
            dict(
                od440aer=_calc_od_helper(
                    dict(od500aer=0.1, ang4487aer=1),
                    "od440aer",
                    to_lambda=0.44,
                    od_ref="od500aer",
                    lambda_ref=0.5,
                    use_angstrom_coeff="ang4487aer",
                ),
                ang4487aer=1,
            ),
            0.09,
            id="complicated",
        ),
    ],
)
def test_calc_od550aer(data: dict, result: float):
    aod = calc_od550aer(data)
    assert aod == pytest.approx(result, abs=0.05)


def test_calc_od550gt1aer():
    data = dict(od500gt1aer=0.1, ang4487aer=1)
    aod = calc_od550gt1aer(data)
    assert aod == pytest.approx(0.09, abs=0.05)


def test_calc_od550lt1aer():
    data = dict(od500lt1aer=0.1, ang4487aer=1)
    aod = calc_od550lt1aer(data)
    assert aod == pytest.approx(0.09, abs=0.05)


@pytest.mark.parametrize(
    "od1,od2,lambda1,lambda2,result",
    [
        (0.1, 0.2, 0.6, 0.3, 1),
        (0.1, 0.2, 0.3, 0.6, -1),
    ],
)
def test_compute_angstrom_coeff(
    od1: float, od2: float, lambda1: float, lambda2: float, result: float
):
    assert compute_angstrom_coeff(od1, od2, lambda1, lambda2) == result


@pytest.mark.parametrize("angs,result", [(4, 0.77), (0, 0.1)])
def test_compute_od_from_angstromexp(angs: float, result: float):
    aod = compute_od_from_angstromexp(
        to_lambda=0.3, od_ref=0.1, lambda_ref=0.5, angstrom_coeff=angs
    )
    aod == result


@pytest.mark.parametrize(
    "inputval,p,T,vmr_unit,mmol_var,mmol_air,to_unit,desired",
    [
        (1, 101300, 293, "nmol mol-1", 48, None, "ug m-3", 1.9959),
        (1, 101300, 273, "nmol mol-1", 48, None, "ug m-3", 2.1421),
        (1, 101300, 273, "nmol mol-1", 48, None, "kg m-3", 2.1421e-9),
        (1, 101300, 273, "mol mol-1", 48, None, "kg m-3", 2.1421),
        (1, 98000, 273, "mol mol-1", 48, None, "kg m-3", 2.0724),
    ],
)
def test_vmrx_to_concx(
    inputval: float,
    p: float,
    T: float,
    vmr_unit: str,
    mmol_var: float,
    mmol_air: float | None,
    to_unit: str,
    desired: float,
):
    val = vmrx_to_concx(inputval, p, T, vmr_unit, mmol_var, mmol_air, to_unit)
    assert val == pytest.approx(desired, rel=1e-4)


@pytest.mark.parametrize(
    "data,expected_result",
    [
        pytest.param(
            dict(od500aer=0.1, ang4487aer=1, abs440aer=1, angabs4487aer=1),
            0.7999999999999999,
        ),
        pytest.param(
            dict(od500aer=0.1, ang4487aer=1, abs440aer=1, angabs4487aer=0),
            1,
        ),
    ],
)
def test_calc_abs550aer(data, expected_result):
    result = calc_abs550aer(data=data)
    assert result == pytest.approx(expected_result, rel=1e-4)


@pytest.mark.parametrize(
    "od_ref, use_angstrom_coeff",
    [
        pytest.param(None, "ang4487aer"),
        pytest.param("od500aer", None),
    ],
)
def test__calc_od_helper_raise_error(od_ref, use_angstrom_coeff):
    data = dict(od500aer=0.1, ang4487aer=1)
    with pytest.raises(AttributeError) as e:
        _calc_od_helper(
            data=data,
            var_name="od550lt1ang",
            to_lambda=0.55,
            od_ref=od_ref,
            lambda_ref=0.50,
            lambda_ref_alt=0.44,
            use_angstrom_coeff=use_angstrom_coeff,
            treshold_angstrom=1.0,
        )
    assert e.type is AttributeError
