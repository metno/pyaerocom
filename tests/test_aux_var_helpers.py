import pytest
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

