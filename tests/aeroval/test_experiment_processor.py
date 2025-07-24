from __future__ import annotations

import pytest

from pyaerocom.aeroval.experiment_output import ExperimentOutput
from pyaerocom.aeroval.experiment_processor import ExperimentProcessor
from pyaerocom.aeroval import EvalSetup


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


@pytest.mark.parametrize("cfg", ["cfgexp1", "cfgexp2", "cfgexp3", "cfgexp4", "cfgexp5"])
def test_ExperimentProcessor_run(processor: ExperimentProcessor):
    processor.run()


# Temporary until ObsCollection implemented similarly then can run same test
@pytest.mark.parametrize(
    "cfg,kwargs,error",
    [
        (
            "cfgexp2",
            dict(model_name="BLA"),
            "'No matches could be found that match input BLA'",
        ),
        (
            "cfgexp2",
            dict(obs_name="BLUB"),
            "'No matches could be found that match input BLUB'",
        ),
    ],
)
def test_ExperimentProcessor_run_error_obs_name(
    processor: ExperimentProcessor, kwargs: dict, error: str
):
    with pytest.raises(KeyError) as e:
        processor.run(**kwargs)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "cfg,kwargs,error",
    [
        ("cfgexp2", dict(var_list="BLUB"), "var_list %s and obs_vars %s mismatch."),
    ],
)
def test_ExperimentProcessor_catch_wrong_var_list(
    processor: ExperimentProcessor, kwargs: dict, error: str, caplog
):
    processor.run(**kwargs)
    assert any([error in str(record) for record in caplog.records])


@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_rerun_by_variable(eval_config: dict):
    setup = EvalSetup(**eval_config)
    processor = ExperimentProcessor(setup)
    processor.run()  # Initial full run
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after initial run"
    processor.exp_output.delete_experiment_data(also_coldata=True)  # Clear previous data
    assert not processor.exp_output.results_available, "Experiment data should be cleared"
    processor.run(var_list="od550aer")
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after rerun"


@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_rerun_by_model(eval_config: dict):
    setup = EvalSetup(**eval_config)
    processor = ExperimentProcessor(setup)
    processor.run()  # Initial full run
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after initial run"
    processor.exp_output.delete_experiment_data(also_coldata=True)  # Clear previous data
    assert not processor.exp_output.results_available, "Experiment data should be cleared"
    processor.run(model_name="TM5-AP3-CTRL")
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after rerun"


@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_rerun_by_obs_network(eval_config: dict):
    setup = EvalSetup(**eval_config)
    processor = ExperimentProcessor(setup)
    processor.run()  # Initial full run
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after initial run"
    processor.exp_output.delete_experiment_data(also_coldata=True)  # Clear previous data
    assert not processor.exp_output.results_available, "Experiment data should be cleared"
    processor.run(obs_name="AERONET-Sun")
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after rerun"
