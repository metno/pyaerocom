from typing import Iterable

from pytest import mark, param, raises

from pyaerocom.aeroval import EvalSetup

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
