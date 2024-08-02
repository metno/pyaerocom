from __future__ import annotations

import os
from collections.abc import Iterable
from pathlib import Path

import pytest

from pyaerocom.aeroval import EvalSetup
from pyaerocom.aeroval._processing_base import DataImporter, HasColocator, HasConfig
from tests.fixtures.aeroval import CAMS84_CONFIG


@pytest.fixture()
def aeroval_path(tmp_path: Path) -> None:
    """temporary path for aeroval outputs"""
    path: Path = tmp_path / "aeroval/aeroval1"
    path.mkdir(parents=True)
    os.chdir(path)


def test_evalsetup_args():
    setup = EvalSetup(proj_id="project", exp_id="experiment")
    assert setup
    assert setup.proj_id == setup.proj_info.proj_id == "project"
    assert setup.exp_id == setup.exp_info.exp_id == "experiment"


def test_evalsetup_kwargs():
    setup = EvalSetup(proj_id="project", exp_id="experiment")
    assert setup
    assert setup.proj_id == setup.proj_info.proj_id == "project"
    assert setup.exp_id == setup.exp_info.exp_id == "experiment"


@pytest.mark.parametrize(
    "keys",
    [
        pytest.param(("model_cfg",), id="cams84 models"),
        pytest.param(("obs_cfg",), id="cams84 obs"),
        pytest.param(
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
        pytest.param(
            ("json_basedir", "coldata_basedir", "io_aux_file"),
            id="IO paths",
        ),
        pytest.param(("filter_name",), id="regional filter"),
        pytest.param(
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
        pytest.param(
            ("obs_remove_outliers", "model_remove_outliers"),
            id="outlier options",
        ),
        pytest.param(
            (
                "harmonise_units",
                "regions_how",
                "annual_stats_constrained",
                "weighted_stats",
                "var_order_menu",
            ),
            id="other options",
        ),
        pytest.param(
            ("exp_name", "exp_descr", "exp_pi"),
            id="experiment description",
        ),
    ],
)
def test_evalsetup_cams84(keys: Iterable[str], aeroval_path):
    assert all(k in CAMS84_CONFIG for k in keys)

    config = {k: CAMS84_CONFIG[k] for k in keys}
    assert config

    setup = EvalSetup(
        proj_id=CAMS84_CONFIG["proj_id"],  # type:ignore[arg-type]
        exp_id=CAMS84_CONFIG["exp_id"],  # type:ignore[arg-type]
        **config,
    )
    assert setup


def test_HasConfig():
    setup = EvalSetup(**CAMS84_CONFIG)
    config = HasConfig(setup)
    assert config.raise_exceptions == CAMS84_CONFIG["raise_exceptions"]
    assert config.reanalyse_existing == CAMS84_CONFIG["reanalyse_existing"]


@pytest.mark.parametrize(
    "model",
    [
        None,
        pytest.param(
            "IFS-CTRL",
            marks=[
                pytest.mark.xfail(reason="broken test", raises=KeyError),
                pytest.mark.dependency(name="HasColocator::model"),
            ],
        ),
    ],
)
@pytest.mark.parametrize(
    "obs",
    [
        None,
        pytest.param("EEA-NRT-rural", marks=[pytest.mark.dependency(name="HasColocator::obs")]),
    ],
)
def test_HasColocator(model: str | None, obs: str | None):
    setup = EvalSetup(**CAMS84_CONFIG)  # type:ignore[arg-type]
    config = HasColocator(setup)
    assert config.get_colocator(model_name=model, obs_name=obs)


@pytest.mark.parametrize(
    "model",
    [pytest.param("IFS-CTRL", marks=pytest.mark.dependency(depends="HasColocator::model"))],
)
@pytest.mark.parametrize("var", ["vmro3", "vmrno2"])
def test_DataImporter_read_model_data(model: str, var: str):
    setup = EvalSetup(**CAMS84_CONFIG)  # type:ignore[arg-type]
    assert DataImporter(setup).read_model_data(model, var)


@pytest.mark.parametrize(
    "obs",
    [pytest.param("EEA-NRT-rural", marks=pytest.mark.dependency(depends="HasColocator::obs"))],
)
@pytest.mark.parametrize("var", ["vmro3", "vmrno2"])
def test_DataImporter_read_ungridded_obsdata(obs: str, var: str):
    setup = EvalSetup(**CAMS84_CONFIG)  # type:ignore[arg-type]
    assert DataImporter(setup).read_ungridded_obsdata(obs, var)
