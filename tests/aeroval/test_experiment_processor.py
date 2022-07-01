from __future__ import annotations

import pytest

from pyaerocom.aeroval.experiment_output import ExperimentOutput
from pyaerocom.aeroval.experiment_processor import ExperimentProcessor
from pyaerocom.aeroval.setupclasses import EvalSetup
from tests.conftest import geojson_unavail


@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_ExperimentProcessor___init__(eval_config: dict):
    cfg = EvalSetup(**eval_config)
    proc = ExperimentProcessor(cfg)
    assert isinstance(proc.cfg, EvalSetup)
    assert isinstance(proc.exp_output, ExperimentOutput)


@pytest.fixture
def processor(eval_config: dict) -> ExperimentProcessor:
    """ExperimentProcessor instance without experiment data"""
    setup = EvalSetup(**eval_config)
    proc = ExperimentProcessor(setup)
    proc.exp_output.delete_experiment_data(also_coldata=True)
    return proc


@geojson_unavail
@pytest.mark.parametrize("cfg", ["cfgexp1", "cfgexp2", "cfgexp3", "cfgexp4", "cfgexp5"])
def test_ExperimentProcessor_run(processor: ExperimentProcessor):
    processor.run()


@geojson_unavail
@pytest.mark.parametrize(
    "cfg,kwargs,error",
    [
        ("cfgexp2", dict(model_name="BLA"), "'No matches could be found that match input BLA'"),
        ("cfgexp2", dict(obs_name="BLUB"), "'No matches could be found that match input BLUB'"),
    ],
)
def test_ExperimentProcessor_run_error(processor: ExperimentProcessor, kwargs: dict, error: str):
    with pytest.raises(KeyError) as e:
        processor.run(**kwargs)
    assert str(e.value) == error
