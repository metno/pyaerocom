import pytest

from pyaerocom.aeroval.experiment_output import ExperimentOutput
from pyaerocom.aeroval.setupclasses import EvalSetup
import pyaerocom.aeroval.experiment_processor as mod

from .cfg_test_exp1 import CFG as cfgexp1
from ..conftest import does_not_raise_exception

@pytest.mark.parametrize('kwargs,raises', [
    (cfgexp1,does_not_raise_exception())
])
def test_ExperimentProcessor___init__(kwargs,raises):
    stp = EvalSetup(**kwargs)
    with raises:
        proc = mod.ExperimentProcessor(stp)
        assert isinstance(proc.cfg, EvalSetup)
        assert isinstance(proc.exp_output, ExperimentOutput)
