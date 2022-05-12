import pytest

from pyaerocom.aeroval.experiment_output import ExperimentOutput
from pyaerocom.aeroval.experiment_processor import ExperimentProcessor
from pyaerocom.aeroval.setupclasses import EvalSetup

from ..conftest import geojson_unavail
from .cfg_test_exp1 import CFG as cfgexp1
from .cfg_test_exp2 import CFG as cfgexp2
from .cfg_test_exp3 import CFG as cfgexp3
from .cfg_test_exp4 import CFG as cfgexp4
from .cfg_test_exp5 import CFG as cfgexp5


def test_ExperimentProcessor___init__():
    cfg = EvalSetup(**cfgexp1)
    proc = ExperimentProcessor(cfg)
    assert isinstance(proc.cfg, EvalSetup)
    assert isinstance(proc.exp_output, ExperimentOutput)


@pytest.fixture
def processor(cfg: dict) -> ExperimentProcessor:
    setup = EvalSetup(**cfg)
    proc = ExperimentProcessor(setup)
    proc.exp_output.delete_experiment_data(also_coldata=True)
    return proc


@geojson_unavail
@pytest.mark.parametrize("cfg", [cfgexp1, cfgexp2, cfgexp3, cfgexp4, cfgexp5])
def test_ExperimentProcessor_run(processor: ExperimentProcessor):
    processor.run()


@geojson_unavail
@pytest.mark.parametrize(
    "cfg,kwargs,error",
    [
        (cfgexp2, dict(model_name="BLA"), "'No matches could be found that match input BLA'"),
        (cfgexp2, dict(obs_name="BLUB"), "'No matches could be found that match input BLUB'"),
    ],
)
def test_ExperimentProcessor_run_error(processor: ExperimentProcessor, kwargs: dict, error: str):
    with pytest.raises(KeyError) as e:
        processor.run(**kwargs)
    assert str(e.value) == error
