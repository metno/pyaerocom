import pytest

from pyaerocom.aeroval.experiment_output import ExperimentOutput
from pyaerocom.aeroval.setupclasses import EvalSetup
import pyaerocom.aeroval.experiment_processor as mod

from .cfg_test_exp1 import CFG as cfgexp1
from ..conftest import does_not_raise_exception

@pytest.mark.dependency(name='init-processor')
@pytest.mark.parametrize('cfgdict,raises', [
    (cfgexp1,does_not_raise_exception())
])
def test_ExperimentProcessor___init__(cfgdict,raises):
    cfg = EvalSetup(**cfgdict)
    with raises:
        proc = mod.ExperimentProcessor(cfg)
        assert isinstance(proc.cfg, EvalSetup)
        assert isinstance(proc.exp_output, ExperimentOutput)

@pytest.mark.dependency(name='run-processor', depends=['init-processor'])
@pytest.mark.parametrize('cfgdict,runkwargs,raises', [
    (cfgexp1,{},does_not_raise_exception())
])
def test_ExperimentProcessor_run(cfgdict,runkwargs,raises):
    cfg = EvalSetup(**cfgdict)
    with raises:
        proc = mod.ExperimentProcessor(cfg)
        proc.run(**runkwargs)


