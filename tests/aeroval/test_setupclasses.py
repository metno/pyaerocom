import json

import pytest

from pyaerocom.aeroval.setupclasses import EvalSetup
from pyaerocom.exceptions import EvalEntryNameError
from tests.fixtures.aeroval.cfg_test_exp1 import CFG


@pytest.mark.parametrize(
    "cfg,update",
    [
        ("cfgexp1", dict()),
        ("cfgexp1", dict(obs_cfg=dict(OBS=CFG["obs_cfg"]["AERONET-Sun"]))),
    ],
)
def test_EvalSetup___init__(eval_config: dict, update: dict):
    eval_config.update(update)
    EvalSetup(**eval_config)


@pytest.mark.parametrize(
    "cfg,update,error",
    [
        (
            "cfgexp1",
            dict(model_cfg=dict(WRONG_MODEL=CFG["model_cfg"]["TM5-AP3-CTRL"])),
            "Invalid name: WRONG_MODEL",
        ),
        (
            "cfgexp1",
            dict(obs_cfg=dict(WRONG_OBS=CFG["obs_cfg"]["AERONET-Sun"])),
            "Invalid name: WRONG_OBS",
        ),
        (
            "cfgexp1",
            dict(obs_cfg=dict(OBS=dict(web_interface_name="WRONG_OBS"))),
            "Invalid name: WRONG_OBS",
        ),
    ],
)
def test_EvalSetup___init__INVALID_ENTRY_NAMES(eval_config: dict, update: dict, error: str):
    eval_config.update(update)
    with pytest.raises(EvalEntryNameError) as e:
        EvalSetup(**eval_config)
    assert error in str(e.value)


def test_EvalSetup_ProjectInfo():
    eval_setup = EvalSetup.model_validate(CFG)

    for k in ["proj_id"]:
        assert getattr(eval_setup.proj_info, k, None) == CFG[k]


@pytest.mark.parametrize(
    "update",
    [
        ({}),
    ],
)
def test_EvalSetup_ExperimentInfo(update):
    cfg = CFG
    cfg.update(update)

    eval_setup = EvalSetup.model_validate(cfg)

    for k in ["exp_id", "exp_descr", "exp_name", "public"]:
        assert getattr(eval_setup.exp_info, k, None) == cfg[k]


@pytest.mark.parametrize(
    "update",
    [
        ({}),
    ],
)
def test_EvalSetup_TimeSetup(update):
    cfg = CFG
    cfg.update(update)
    eval_setup = EvalSetup.model_validate(cfg)

    assert eval_setup.time_cfg.freqs == cfg["freqs"]
    assert eval_setup.time_cfg.main_freq == cfg["main_freq"]
    assert eval_setup.time_cfg.periods == cfg["periods"]


@pytest.mark.parametrize("update", [({}), ({"maps_freq": "yearly", "maps_res_deg": 10})])
def test_EvalSetup_ModelMapsSetup(update):
    cfg = CFG
    cfg.update(update)
    eval_setup = EvalSetup.model_validate(cfg)

    assert eval_setup.modelmaps_opts.maps_freq == cfg.get("maps_freq", "monthly")
    assert eval_setup.modelmaps_opts.maps_res_deg == cfg.get("maps_res_deg", 5)


@pytest.mark.parametrize("update", [({}), ({"obs_only": True, "only_colocation": True})])
def test_EvalSetup_EvalRunOptions(update):
    cfg = CFG
    if update:
        cfg.update(update)
    cfg.update(update)
    eval_setup = EvalSetup.model_validate(cfg)

    assert eval_setup.processing_opts.clear_existing_json == cfg["clear_existing_json"]
    assert eval_setup.processing_opts.obs_only == cfg.get("obs_only", False)
    assert eval_setup.processing_opts.only_colocation == cfg.get("only_colocation", False)
    assert eval_setup.processing_opts.only_json == cfg["only_json"]
    assert eval_setup.processing_opts.only_model_maps == cfg["only_model_maps"]


@pytest.mark.parametrize(
    "update",
    [
        ({}),
        (
            {
                "trends_min_yrs": 10,
                "use_diurnal": True,
                "use_fairmode": True,
                "weighted_stats": False,
                "model_only_stats": True,
                "obs_only_stats": True,
                "add_trends": True,
                "annual_stats_constrained": True,
            }
        ),
    ],
)
def test_EvalSetup_StatisticsSetup(update):
    cfg = CFG
    cfg.update(update)

    eval_setup = EvalSetup.model_validate(cfg)

    assert eval_setup.statistics_opts.trends_min_yrs == cfg.get("trends_min_yrs", 7)
    assert eval_setup.statistics_opts.use_diurnal == cfg.get("use_diurnal", False)
    assert eval_setup.statistics_opts.use_fairmode == cfg.get("use_fairmode", False)
    assert eval_setup.statistics_opts.weighted_stats == cfg.get("weighted_stats", True)
    assert eval_setup.statistics_opts.model_only_stats == cfg.get("model_only_stats", False)
    assert eval_setup.statistics_opts.obs_only_stats == cfg.get("obs_only_stats", False)
    assert eval_setup.statistics_opts.add_trends == cfg.get("add_trends", False)
    assert eval_setup.statistics_opts.annual_stats_constrained == cfg.get(
        "annual_stats_constrained", True
    )


@pytest.mark.parametrize("update", [({})])
def test_EvalSetup_WebDisplaySetup(update):
    cfg = CFG
    cfg.update(update)

    eval_setup = EvalSetup.model_validate(cfg)

    assert eval_setup.webdisp_opts.add_model_maps == cfg.get("add_model_maps", False)
    assert eval_setup.webdisp_opts.map_zoom == cfg.get("map_zoom", "World")
    assert eval_setup.webdisp_opts.modelorder_from_config == cfg.get(
        "modelorder_from_config", True
    )
    assert eval_setup.webdisp_opts.obsorder_from_config == cfg.get("obsorder_from_config", True)
    assert eval_setup.webdisp_opts.add_model_maps == cfg.get("add_model_maps", False)
