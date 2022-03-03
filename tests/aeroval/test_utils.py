from __future__ import annotations

from copy import deepcopy

import pytest

from pyaerocom import GriddedData
from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.aeroval.utils import compute_model_average_and_diversity, make_config_template

from .._conftest_helpers import add_dummy_model_data
from ._outbase import ADD_MODELS_DIR
from .cfg_test_exp1 import CFG as cfg1
from .cfg_test_exp2 import CFG as cfg2

# create some fake AOD model data
MODEL_DIR = add_dummy_model_data(
    "od550aer",
    "1",
    "daily",
    "Surface",
    year=2010,
    lat_range=(-90, 90),
    lon_range=(-180, 180),
    tmpdir=ADD_MODELS_DIR,
)

# need more than one model
CFG1 = deepcopy(cfg1)
CFG1["model_cfg"]["DUMMY-MODEL"] = dict(model_id="DUMMY-MODEL", model_data_dir=MODEL_DIR)

# need more than one model
CFG2 = deepcopy(cfg2)
CFG2["model_cfg"]["DUMMY-MODEL"] = dict(model_id="DUMMY-MODEL", model_data_dir=MODEL_DIR)


def test_make_config_template():
    val = make_config_template("bla", "blub")
    assert isinstance(val, EvalSetup)


@pytest.fixture
def processor(cfg) -> ExperimentProcessor | None:
    if cfg is None:
        return None
    setup = EvalSetup(**cfg)
    return ExperimentProcessor(setup)


@pytest.mark.parametrize("cfg", [CFG2])
@pytest.mark.parametrize("avg_how", ["median", "mean"])
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
    "cfg,avg_how,error",
    [
        (None, None, "invalid input, need ExperimentProcessor"),
        (cfg1, None, "Need more than one model to compute average..."),
        (CFG1, "bla", "Invalid input for avg_how bla"),
    ],
)
def test_compute_model_average_and_diversity_error(
    processor: ExperimentProcessor | None, avg_how: str | None, error: str
):
    with pytest.raises(ValueError) as e:
        compute_model_average_and_diversity(processor, "od550aer", avg_how=avg_how)
    assert str(e.value) == error
