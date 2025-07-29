from __future__ import annotations

from pathlib import Path

import pytest

from pyaerocom import GriddedData
from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.aeroval.utils import compute_model_average_and_diversity
from tests.fixtures.aeroval import add_dummy_model_data


@pytest.fixture(scope="session")
def model_data_dir(aeroval_model_path: Path) -> str:
    """create some fake AOD model data"""
    return add_dummy_model_data(
        "od550aer",
        "1",
        "daily",
        "Surface",
        year=2010,
        lat_range=(-90, 90),
        lon_range=(-180, 180),
        tmp_path=aeroval_model_path,
    )


@pytest.fixture
def config(
    cfg: str | None,
    eval_config: dict,
    dummy_model: bool,
    model_data_dir: str,
) -> dict | None:
    """experiment configuration"""
    if cfg is None:
        return None
    if dummy_model:
        eval_config["model_cfg"]["DUMMY-MODEL"] = dict(
            model_id="DUMMY-MODEL",
            model_data_dir=model_data_dir,
        )
    return eval_config


@pytest.fixture
def processor(config: dict | None) -> ExperimentProcessor | None:
    """ExperimentProcessor instance, or None"""
    if config is None:
        return None
    setup = EvalSetup(**config)
    return ExperimentProcessor(setup)


@pytest.mark.parametrize(
    "cfg,dummy_model,avg_how",
    [
        ("cfgexp2", True, "median"),
        ("cfgexp2", True, "mean"),
    ],
)
def test_compute_model_average_and_diversity(processor: ExperimentProcessor, avg_how: str):
    avg_out, div_out, q1_out, q3_out, std_out = compute_model_average_and_diversity(
        processor, "od550aer", avg_how=avg_how
    )

    assert isinstance(avg_out, GriddedData)
    assert isinstance(div_out, GriddedData)

    if avg_how == "median":
        assert isinstance(q1_out, GriddedData)
        assert isinstance(q3_out, GriddedData)
    else:
        assert isinstance(std_out, GriddedData)


@pytest.mark.parametrize(
    "cfg,dummy_model,avg_how,error",
    [
        (None, False, None, "invalid input, need ExperimentProcessor"),
        ("cfgexp1", False, None, "Need more than one model to compute average..."),
        ("cfgexp1", True, "bla", "Invalid input for avg_how bla"),
    ],
)
def test_compute_model_average_and_diversity_error(
    processor: ExperimentProcessor | None, avg_how: str | None, error: str
):
    with pytest.raises(ValueError) as e:
        compute_model_average_and_diversity(processor, "od550aer", avg_how=avg_how)
    assert str(e.value) == error
