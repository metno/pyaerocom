from contextlib import nullcontext as does_not_raise_exception

import pytest

import pyaerocom.aeroval.experiment_processor as mod
from pyaerocom.aeroval.experiment_output import ExperimentOutput
from pyaerocom.aeroval.setupclasses import EvalSetup

from ..conftest import geojson_unavail
from .cfg_test_exp1 import CFG as cfgexp1
from .cfg_test_exp2 import CFG as cfgexp2
from .cfg_test_exp3 import CFG as cfgexp3
from .cfg_test_exp4 import CFG as cfgexp4
from .cfg_test_exp5 import CFG as cfgexp5


@pytest.mark.parametrize("cfgdict", [cfgexp1])
def test_ExperimentProcessor___init__(cfgdict):
    cfg = EvalSetup(**cfgdict)
    proc = mod.ExperimentProcessor(cfg)
    assert isinstance(proc.cfg, EvalSetup)
    assert isinstance(proc.exp_output, ExperimentOutput)


@geojson_unavail
@pytest.mark.parametrize(
    "cfgdict,runkwargs,raises",
    [
        (cfgexp5, {}, does_not_raise_exception()),
        (cfgexp1, {}, does_not_raise_exception()),
        (cfgexp2, {}, does_not_raise_exception()),
        (cfgexp2, dict(model_name="BLA"), pytest.raises(KeyError)),
        (cfgexp2, dict(obs_name="BLUB"), pytest.raises(KeyError)),
        (cfgexp3, {}, does_not_raise_exception()),
        (cfgexp4, {}, does_not_raise_exception()),
    ],
)
def test_ExperimentProcessor_run(cfgdict, runkwargs, raises):
    cfg = EvalSetup(**cfgdict)
    with raises:
        proc = mod.ExperimentProcessor(cfg)
        proc.exp_output.delete_experiment_data(also_coldata=True)
        proc.run(**runkwargs)
