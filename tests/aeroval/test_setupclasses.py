import pytest
from pyaerocom.aeroval import setupclasses as mod

from .cfg_test_exp1 import CFG as cfgexp1
from ..conftest import does_not_raise_exception

@pytest.mark.parametrize('kwargs,raises', [
    (cfgexp1,does_not_raise_exception())
])
def test_EvalSetup___init__(kwargs,raises):
    with raises:
        stp = mod.EvalSetup(**kwargs)
