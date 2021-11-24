import pytest

import pyaerocom.aeroval.utils as mod
from pyaerocom import GriddedData
from pyaerocom.aeroval import EvalSetup, ExperimentProcessor

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


def test_make_config_template():
    val = mod.make_config_template("bla", "blub")
    assert isinstance(val, EvalSetup)


from copy import deepcopy

CFG1 = deepcopy(cfg1)
# need more than one model
CFG1["model_cfg"]["DUMMY-MODEL"] = dict(model_id="DUMMY-MODEL", model_data_dir=MODEL_DIR)
CFG2 = deepcopy(cfg2)
# need more than one model
CFG2["model_cfg"]["DUMMY-MODEL"] = dict(model_id="DUMMY-MODEL", model_data_dir=MODEL_DIR)


@pytest.mark.parametrize(
    "cfg,kwargs",
    [
        (CFG2, dict()),
        (CFG2, dict(avg_how="mean")),
    ],
)
def test_compute_model_average_and_diversity(cfg, kwargs):
    stp = EvalSetup(**cfg)
    proc = ExperimentProcessor(stp)
    avg_out, div_out, q1_out, q3_out, std_out = mod.compute_model_average_and_diversity(
        proc, "od550aer", **kwargs
    )

    assert isinstance(avg_out, GriddedData)
    assert isinstance(div_out, GriddedData)

    avg_how = kwargs.get("avg_how", "median")
    if avg_how == "median":
        assert isinstance(q1_out, GriddedData)
        assert isinstance(q3_out, GriddedData)
    else:
        assert isinstance(std_out, GriddedData)


@pytest.mark.parametrize(
    "cfg,kwargs,error",
    [
        (cfg1, dict(), "Need more than one model to compute average..."),
        (cfg1, dict(avg_how="bla"), "Invalid input for avg_how bla"),
        (CFG1, dict(avg_how="bla"), "Invalid input for avg_how bla"),
    ],
)
def test_compute_model_average_and_diversity_error(cfg: dict, kwargs: dict, error: str):
    with pytest.raises(ValueError) as e:
        mod.compute_model_average_and_diversity(42, "od550aer")
    assert str(e.value) == "invalid input, need ExperimentProcessor"

    stp = EvalSetup(**cfg)
    proc = ExperimentProcessor(stp)
    with pytest.raises(ValueError) as e:
        mod.compute_model_average_and_diversity(proc, "od550aer", **kwargs)
    assert str(e.value) == error
