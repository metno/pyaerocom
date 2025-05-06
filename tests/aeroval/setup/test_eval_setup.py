import os
from copy import deepcopy
from typing import Literal

import pytest

from pyaerocom.aeroval import EvalSetup
from tests.fixtures.aeroval.cfg_test_exp1 import CFG
from pyaerocom.aeroval.modelmaps_helpers import CONTOUR


@pytest.fixture
def cfg_exp1(update: dict | None) -> dict:
    cfg = deepcopy(CFG)
    if update:
        cfg.update(update)

    return cfg


@pytest.fixture
def eval_setup(cfg_exp1: dict) -> EvalSetup:
    return EvalSetup.model_validate(cfg_exp1)


default_config = pytest.mark.parametrize("update", (pytest.param(None, id="default"),))


@default_config
def test_EvalSetup(cfg_exp1: dict):
    assert EvalSetup(**cfg_exp1) == EvalSetup.model_validate(cfg_exp1)


@pytest.mark.parametrize(
    "update",
    (
        pytest.param(None, id="defaults"),
        pytest.param(dict(proj_id="blah"), id="custom"),
    ),
)
def test_EvalSetup_ProjectInfo(eval_setup: EvalSetup, cfg_exp1: dict):
    assert eval_setup.proj_info.proj_id == cfg_exp1["proj_id"]


@pytest.mark.parametrize(
    "update",
    (
        pytest.param(None, id="defaults"),
        pytest.param(
            dict(
                exp_id="exp42",
                exp_descr="Hello world!",
                exp_name="Lorem Ipsum...",
                public=True,
            ),
            id="custom1",
        ),
        pytest.param(
            dict(
                exp_id="exp54",
                exp_descr="Hello world!",
                exp_name="Lorem Ipsum...",
                public=False,
            ),
            id="custom2",
        ),
    ),
)
def test_EvalSetup_ExperimentInfo(eval_setup: EvalSetup, cfg_exp1: dict):
    exp_info = eval_setup.exp_info
    assert exp_info.exp_id == cfg_exp1["exp_id"]
    assert exp_info.exp_descr == cfg_exp1["exp_descr"]
    assert exp_info.exp_name == cfg_exp1["exp_name"]
    assert exp_info.public == cfg_exp1["public"]


@pytest.mark.parametrize(
    "update",
    (
        pytest.param(None, id="defaults"),
        pytest.param(
            dict(freqs=["yearly", "monthly"], main_freq="yearly", periods=[]),
            id="custom1",
        ),
        pytest.param(
            dict(freqs=["monthly"], main_freq="monthly", periods=["2010", "2011", "2016"]),
            id="custom2",
        ),
    ),
)
def test_EvalSetup_TimeSetup(eval_setup: EvalSetup, cfg_exp1: dict):
    time_cfg = eval_setup.time_cfg
    assert time_cfg.freqs == cfg_exp1["freqs"]
    assert time_cfg.main_freq == cfg_exp1["main_freq"]
    assert time_cfg.periods == cfg_exp1["periods"]


@pytest.mark.parametrize(
    "update,start,stop",
    (
        pytest.param(
            dict(periods=["2022"]),
            "2022",
            "2023",
            id="custom1",
        ),
        pytest.param(
            dict(periods=["20220112"]),
            "2022/01/12 00:00:00",
            "2022/01/12 23:00:00",
            id="custom2",
        ),
    ),
)
def test_EvalSetup__check_time_config(
    eval_setup: EvalSetup,
    start: Literal["2022", "2022/01/12 00:00:00"],
    stop: Literal["2023", "2022/01/12 23:00:00"],
):
    eval_setup._check_time_config()
    assert str(eval_setup.colocation_opts.start) == start
    assert str(eval_setup.colocation_opts.stop) == stop


@pytest.mark.parametrize(
    "update",
    (
        pytest.param(None, id="defaults"),
        pytest.param(dict(maps_freq="yearly"), id="custom"),
    ),
)
def test_EvalSetup_ModelMapsSetup(eval_setup: EvalSetup, cfg_exp1: dict, update: dict):
    modelmaps_opts = eval_setup.modelmaps_opts
    if update:
        assert modelmaps_opts.maps_freq == cfg_exp1["maps_freq"] == update["maps_freq"]
    else:  # defaults
        assert "maps_freq" not in cfg_exp1
        assert modelmaps_opts.maps_freq == "coarsest"
        assert "maps_res_deg" not in cfg_exp1
        assert modelmaps_opts.plot_types == {CONTOUR}
        assert modelmaps_opts.overlay_save_format == "webp"


@pytest.mark.parametrize(
    "update",
    (
        pytest.param(None, id="defaults"),
        pytest.param(dict(obs_only=True, only_colocation=True), id="custom"),
    ),
)
def test_EvalSetup_EvalRunOptions(eval_setup: EvalSetup, cfg_exp1: dict, update: dict):
    processing_opts = eval_setup.processing_opts
    assert processing_opts.clear_existing_json == cfg_exp1["clear_existing_json"]
    assert processing_opts.only_json == cfg_exp1["only_json"]
    assert processing_opts.only_model_maps == cfg_exp1["only_model_maps"]
    if update:
        assert processing_opts.obs_only == cfg_exp1["obs_only"] == update["obs_only"]
        assert (
            processing_opts.only_colocation
            == cfg_exp1["only_colocation"]
            == update["only_colocation"]
        )
    else:  # defaults
        assert "obs_only" not in cfg_exp1
        assert processing_opts.obs_only is False
        assert "only_colocation" not in cfg_exp1
        assert processing_opts.only_colocation is False


@pytest.mark.parametrize(
    "update",
    (
        pytest.param(None, id="default"),
        pytest.param(
            dict(
                stats_min_yrs=10,
                use_diurnal=True,
                use_fairmode=True,
                weighted_stats=False,
                model_only_stats=True,
                obs_only_stats=True,
                add_trends=True,
                annual_stats_constrained=True,
            ),
            id="custom",
        ),
    ),
)
def test_EvalSetup_StatisticsSetup(eval_setup: EvalSetup, cfg_exp1: dict, update: dict):
    statistics_opts = eval_setup.statistics_opts
    if update:
        assert (
            statistics_opts.stats_min_yrs == cfg_exp1["stats_min_yrs"] == update["stats_min_yrs"]
        )
        assert statistics_opts.use_diurnal == cfg_exp1["use_diurnal"] == update["use_diurnal"]
        assert statistics_opts.use_fairmode == cfg_exp1["use_fairmode"] == update["use_fairmode"]
        assert (
            statistics_opts.weighted_stats
            == cfg_exp1["weighted_stats"]
            == update["weighted_stats"]
        )
        assert (
            statistics_opts.model_only_stats
            == cfg_exp1["model_only_stats"]
            == update["model_only_stats"]
        )
        assert (
            statistics_opts.obs_only_stats
            == cfg_exp1["obs_only_stats"]
            == update["obs_only_stats"]
        )
        assert statistics_opts.add_trends == cfg_exp1["add_trends"] == update["add_trends"]
        assert (
            statistics_opts.annual_stats_constrained
            == cfg_exp1["annual_stats_constrained"]
            == update["annual_stats_constrained"]
        )
    else:  # defaults
        assert "stats_min_yrs" not in cfg_exp1
        assert statistics_opts.stats_min_yrs == 0
        assert "use_diurnal" not in cfg_exp1
        assert statistics_opts.use_diurnal is False
        assert "use_fairmode" not in cfg_exp1
        assert statistics_opts.use_fairmode is False
        assert statistics_opts.weighted_stats == cfg_exp1["weighted_stats"] == True  # noqa: E712
        assert "model_only_stats" not in cfg_exp1
        assert statistics_opts.model_only_stats is False
        assert "obs_only_stats" not in cfg_exp1
        assert statistics_opts.obs_only_stats is False
        assert "add_trends" not in cfg_exp1
        assert statistics_opts.add_trends is False
        assert (
            statistics_opts.annual_stats_constrained  # noqa: E712
            == cfg_exp1["annual_stats_constrained"]
            == True
        )


@default_config
def test_EvalSetup_WebDisplaySetup(eval_setup: EvalSetup, cfg_exp1: dict):
    webdisp_opts = eval_setup.webdisp_opts
    # from config
    assert webdisp_opts.add_model_maps == cfg_exp1["add_model_maps"]
    assert webdisp_opts.map_zoom == cfg_exp1["map_zoom"]
    assert webdisp_opts.add_model_maps == cfg_exp1["add_model_maps"]
    # defaults
    assert "modelorder_from_config" not in cfg_exp1
    assert webdisp_opts.modelorder_from_config is True
    assert "obsorder_from_config" not in cfg_exp1
    assert webdisp_opts.obsorder_from_config is True


@default_config
def test_user_var_scale_colmap(cfg_exp1: dict):
    es1 = EvalSetup(**cfg_exp1)
    assert "deprdn" in es1.var_scale_colmap

    cfg = cfg_exp1.copy()
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    cfg["var_scale_colmap_file"] = os.path.join(
        parent_directory, "data", "user_var_scale_colmap.ini"
    )
    esX = EvalSetup(**cfg)
    assert "deprdn" in esX.var_scale_colmap
    assert "newvar" in esX.var_scale_colmap
    assert esX.var_scale_colmap["deprdn"]["colmap"] != es1.var_scale_colmap["deprdn"]["colmap"]
    assert esX.var_scale_colmap["deprdn"]["scale"] != es1.var_scale_colmap["deprdn"]["scale"]

    cfg_fail = cfg_exp1.copy()
    cfg_fail["var_scale_colmap_file"] = os.path.join(
        parent_directory, "data", "buggy_var_scale_colmap.ini"
    )
    esY = EvalSetup(**cfg_fail)
    with pytest.raises(KeyError) as e:
        _ = esY.var_scale_colmap
    assert "buggy_var_scale_colmap.ini" in str(e.value)
    assert "scale" in str(e.value)


@default_config
def test_user_var_web_info(cfg_exp1: dict):
    es1 = EvalSetup(**cfg_exp1)
    assert "deprdn" in es1.var_web_info

    cfg = cfg_exp1.copy()
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    cfg["var_web_info_file"] = os.path.join(parent_directory, "data", "user_var_web_info.ini")
    esX = EvalSetup(**cfg)
    assert "deprdn" in esX.var_web_info
    assert "newvar" in esX.var_web_info
    assert esX.var_web_info["deprdn"][0] != es1.var_web_info["deprdn"][0]

    cfg_fail = cfg_exp1.copy()
    cfg_fail["var_web_info_file"] = os.path.join(
        parent_directory, "data", "buggy_var_web_info.ini"
    )
    esY = EvalSetup(**cfg_fail)
    with pytest.raises(KeyError) as e:
        _ = esY.var_web_info

    assert "buggy_var_web_info.ini" in str(e.value)
    assert "category" in str(e.value)
