from __future__ import annotations

from typing import Iterable

from pytest import mark, param, raises

from pyaerocom.aeroval import EvalSetup
from pyaerocom.aeroval._processing_base import DataImporter, HasColocator, HasConfig

from ..conftest import broken_test
from .cams84 import CAMS84_CONFIG


def test_evalsetup_args():
    setup = EvalSetup("project", "experiment")
    assert setup
    assert setup.proj_id == setup.proj_info.proj_id == "project"
    assert setup.exp_id == setup.exp_info.exp_id == "experiment"


def test_evalsetup_kwargs():
    setup = EvalSetup(proj_id="project", exp_id="experiment")
    assert setup
    assert setup.proj_id == setup.proj_info.proj_id == "project"
    assert setup.exp_id == setup.exp_info.exp_id == "experiment"


def test_evalsetup_missing_arguments():
    with raises((KeyError, ValueError)):
        EvalSetup()

    with raises((KeyError, ValueError)):
        EvalSetup("project")

    with raises((KeyError, ValueError)):
        EvalSetup(proj_id="project")

    with raises((KeyError, ValueError)):
        EvalSetup(exp_id="experiment")


@mark.parametrize(
    "keys",
    [
        param(("model_cfg",), id="cams84 models"),
        param(("obs_cfg",), id="cams84 obs"),
        param(
            (
                "reanalyse_existing",
                "only_json",
                "add_model_maps",
                "only_model_maps",
                "clear_existing_json",
                "raise_exceptions",
            ),
            id="bool options",
        ),
        param(
            ("json_basedir", "coldata_basedir", "io_aux_file"),
            id="IO paths",
        ),
        param(("filter_name",), id="regional filter"),
        param(
            (
                "ts_type",
                "map_zoom",
                "freqs",
                "periods",
                "main_freq",
                "zeros_to_nan",
                "min_num_obs",
                "colocate_time",
            ),
            id="colocation options",
        ),
        param(
            ("obs_remove_outliers", "model_remove_outliers"),
            id="outlier options",
        ),
        param(
            (
                "harmonise_units",
                "regions_how",
                "annual_stats_constrained",
                "weighted_stats",
                "var_order_menu",
            ),
            id="other options",
        ),
        param(
            ("exp_name", "exp_descr", "exp_pi"),
            id="experiment description",
        ),
    ],
)
def test_evalsetup_cams84(keys: Iterable[str]):
    assert all(k in CAMS84_CONFIG for k in keys)

    config = {k: CAMS84_CONFIG[k] for k in keys}
    assert config

    setup = EvalSetup(proj_id=CAMS84_CONFIG["proj_id"], exp_id=CAMS84_CONFIG["exp_id"], **config)  # type: ignore
    assert setup


def test_HasConfig():
    setup = EvalSetup(**CAMS84_CONFIG)
    config = HasConfig(setup)
    assert config.raise_exceptions == CAMS84_CONFIG["raise_exceptions"]
    assert config.reanalyse_existing == CAMS84_CONFIG["reanalyse_existing"]


@mark.parametrize(
    "model",
    [None, param("IFS-CTRL", marks=[broken_test, mark.dependency(name="HasColocator::model")])],
)
@mark.parametrize(
    "obs",
    [None, param("EEA-NRT-rural", marks=[mark.dependency(name="HasColocator::obs")])],
)
def test_HasColocator(model: str | None, obs: str | None):
    setup = EvalSetup(**CAMS84_CONFIG)
    config = HasColocator(setup)
    assert config.get_colocator(model_name=model, obs_name=obs)


@mark.parametrize(
    "model", [param("IFS-CTRL", marks=mark.dependency(depends="HasColocator::model"))]
)
@mark.parametrize("var", ["vmro3", "vmrno2"])
def test_DataImporter_read_model_data(model: str, var: str):
    setup = EvalSetup(**CAMS84_CONFIG)
    assert DataImporter(setup).read_model_data(model, var)


@mark.parametrize(
    "obs", [param("EEA-NRT-rural", marks=mark.dependency(depends="HasColocator::obs"))]
)
@mark.parametrize("var", ["vmro3", "vmrno2"])
def test_DataImporter_read_ungridded_obsdata(obs: str, var: str):
    setup = EvalSetup(**CAMS84_CONFIG)
    assert DataImporter(setup).read_ungridded_obsdata(obs, var)
