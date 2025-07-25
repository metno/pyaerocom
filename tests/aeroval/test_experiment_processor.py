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


@pytest.mark.parametrize("cfg", ["cfgexp2"])
def test_rerun_by_variable(eval_config: dict):
    # Add new obs network & var to the configuration for test
    eval_config["obs_cfg"]["AERONET-Inv"] = dict(
        obs_id="AeronetInvV3L2Subset.daily",
        obs_vars=("abs550aer",),
        obs_vert_type="Column",
    )
    eval_config["var_order_menu"] = ("od550aer", "abs550aer")
    setup = EvalSetup(**eval_config)
    processor = ExperimentProcessor(setup)
    processor.run()  # Initial full run
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after initial run"
    assert "od550aer" in str(
        processor.exp_output
    ), "od550aer should be present in results after inital run"
    assert "abs550aer" in str(
        processor.exp_output
    ), "abs550aer should be present in results after initial run"
    processor.exp_output.delete_experiment_data(also_coldata=True)  # Clear previous data
    assert not processor.exp_output.results_available, "Experiment data should be cleared"
    # Rerun with the od550aer
    processor.run(var_list="od550aer")
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after rerun of od550aer"
    assert "od550aer" in str(processor.exp_output)
    assert "abs550aer" not in str(
        processor.exp_output
    ), "abs550aer should not be present in results after rerun of just od550aer"
    # Rerun with the abs550aer
    processor.run(var_list="abs550aer")
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after rerun of abs550aer"
    assert "od550aer" in str(
        processor.exp_output
    ), "od550aer should be present in results after rerun with abs550aer"
    assert "abs550aer" in str(
        processor.exp_output
    ), "abs550aer should be present in results after rerun abs550aer"


@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_rerun_by_model(eval_config: dict):
    setup = EvalSetup(**eval_config)
    processor = ExperimentProcessor(setup)
    processor.run()  # Initial full run
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after initial run"
    assert "TM5-AP3-CTRL" in str(
        processor.exp_output
    ), "TM5-AP3-CTRL model should be present in results after initial run"
    processor.exp_output.delete_experiment_data(also_coldata=True)
    assert not processor.exp_output.results_available, "Experiment data should be cleared"
    assert "TM5-AP3-CTRL" not in str(
        processor.exp_output
    ), "TM5-AP3-CTRL model should not be present in results after clearing"
    # Rerun with the TM5-AP3-CTRL model
    processor.run(model_name="TM5-AP3-CTRL")
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after rerun"
    assert "TM5-AP3-CTRL" in str(
        processor.exp_output
    ), "TM5-AP3-CTRL model should be present in results after rerun"
    # Rerun with a non-existing model
    with pytest.raises(KeyError) as e:
        processor.run(model_name="NonExistingModel")
    assert "No matches could be found that match input NonExistingModel" in str(
        e.value
    ), "Should raise KeyError for non-existing model"


@pytest.mark.parametrize("cfg", ["cfgexp4"])
def test_rerun_by_obs_network(eval_config: dict):
    # Ensure that the obs networks are set up correctly - want more than just superobs for this test
    eval_config["obs_cfg"]["AERONET-Sun"]["only_superobs"] = False  # Ensure superobs is not set
    eval_config["obs_cfg"]["AERONET-SDA"]["only_superobs"] = False
    setup = EvalSetup(**eval_config)
    processor = ExperimentProcessor(setup)
    processor.run()  # Initial full run
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after initial run"
    assert "AERONET-Sun" in str(
        processor.exp_output
    ), "AERONET-Sun network should be present in results after initial run"
    assert "AERONET-SDA" in str(
        processor.exp_output
    ), "AERONET-SDA network should be present in results after initial run"
    assert "SDA-and-Sun" in str(
        processor.exp_output
    ), "SDA-and-Sun superobs network should be present in results after initial run"
    processor.exp_output.delete_experiment_data(also_coldata=True)  # Clear previous data
    assert not processor.exp_output.results_available, "Experiment data should be cleared"

    # Test rerun with single observation network
    processor.run(obs_name="AERONET-Sun")
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after rerun of AERONET-Sun"
    assert "AERONET-Sun" in str(
        processor.exp_output
    ), "AERONET-Sun network should be present in results after rerun of AERONET-Sun"
    assert "AERONET-SDA" not in str(
        processor.exp_output
    ), "AERONET-SDA network should not be present in results after rerun of AERONET-Sun"
    assert "SDA-and-Sun" not in str(
        processor.exp_output
    ), "SDA-and-Sun superobs network should not be present in results after rerun of AERONET-Sun"
    processor.run(obs_name="AERONET-SDA")
    # Test that once a network has already been processed, another can be processed without clearing previous results
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after rerun of AERONET-SDA"
    assert "AERONET-Sun" in str(
        processor.exp_output
    ), "AERONET-Sun network should be present in results after rerun of AERONET-SDA"
    assert "AERONET-SDA" in str(
        processor.exp_output
    ), "AERONET-SDA network should be present in results after rerun of AERONET-SDA"
    assert "SDA-and-Sun" not in str(
        processor.exp_output
    ), "SDA-and-Sun superobs network should not be present in results after rerun of AERONET-SDA"
    # Now test that the superobs can be re-added and that all previously processed networks are still present
    processor.run(obs_name="SDA-and-Sun")
    assert (
        processor.exp_output.results_available
    ), "Experiment data should be available after rerun of superobs SDA-and-Sun"
    assert "AERONET-Sun" in str(
        processor.exp_output
    ), "AERONET-Sun network should be present in results after rerun of superobs SDA-and-Sun"
    assert "AERONET-SDA" in str(
        processor.exp_output
    ), "AERONET-SDA network should be present in results after rerun of superobs SDA-and-Sun"
    assert (
        "SDA-and-Sun" in str(processor.exp_output)
    ), "SDA-and-Sun superobs observation network should be present in results after rerun of superobs SDA-and-Sun"
