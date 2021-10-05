import pytest
import numpy as np
import numpy.testing as npt
import pyaerocom.aux_var_helpers as mod


def test_calc_ang4487aer():
    data = {}
    with pytest.raises(AttributeError):
        mod.calc_ang4487aer(data)
    data['od440aer'] = 0.2
    with pytest.raises(AttributeError):
        mod.calc_ang4487aer(data)
    data['od870aer'] = 0.1
    vals = mod.calc_ang4487aer(data)
    npt.assert_allclose(vals, 1, atol=0.05)

def test_calc_od550aer():
    ang = 1
    data = dict(
        od500aer = 0.1,
        ang4487aer = ang
    )

    val = mod.calc_od550aer(data)
    npt.assert_allclose(val, 0.09, atol=0.05)

    od440 = mod._calc_od_helper(data,'od440aer', to_lambda=0.44,
                                od_ref='od500aer',
                                lambda_ref=0.5,
                                use_angstrom_coeff='ang4487aer')

    npt.assert_allclose(od440, 0.11, atol=0.05)

    data = dict(
        od440aer=od440,
        ang4487aer=ang
    )
    val = mod.calc_od550aer(data)
    npt.assert_allclose(val, 0.09, atol=0.05)

def test_calc_od550gt1aer():
    ang = 1
    data = dict(
        od500gt1aer = 0.1,
        ang4487aer = ang
    )

    val = mod.calc_od550gt1aer(data)
    npt.assert_allclose(val, 0.09, atol=0.05)

def test_calc_od550lt1aer():
    ang = 1
    data = dict(
        od500lt1aer = 0.1,
        ang4487aer = ang
    )

    val = mod.calc_od550lt1aer(data)
    npt.assert_allclose(val, 0.09, atol=0.05)

@pytest.mark.parametrize('od1,od2,lambda1,lambda2', [
    (0.1,0.2,.6,.3),
    (0.1,0.2,.3,.6),
])
def test_compute_angstrom_coeff(od1,od2,lambda1,lambda2):
    ae = mod.compute_angstrom_coeff(od1,od2,lambda1,lambda2)
    expected = -np.log(od1 / od2) / np.log(lambda1 / lambda2)
    npt.assert_allclose(ae,expected,atol=1e-5)

def test_compute_od_from_angstromexp():
    val = mod.compute_od_from_angstromexp(to_lambda=0.3,
                                          od_ref=0.1,
                                          lambda_ref=0.5,
                                          angstrom_coeff=4
                                          )
    npt.assert_allclose(val, 0.77, atol=.05)

    val = mod.compute_od_from_angstromexp(to_lambda=0.3,
                                          od_ref=0.1,
                                          lambda_ref=0.5,
                                          angstrom_coeff=0
                                          )
    npt.assert_allclose(val, 0.1, atol=.05)

def test__calc_od_helper():
    data = dict(
        od500aer = np.asarray([2, 2, np.nan, 2, np.nan, np.nan]),
        od440aer = np.ones(6)*4,
        ang4487aer = np.zeros(6)
    )
    result = mod._calc_od_helper(data,'od550aer',0.55,'od500aer', 0.5,
                                 'od440aer', 0.44, 'ang4487aer')

    assert len(result) == 6
    assert result.mean() == 3



