from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from . import cfg_test_exp1, cfg_test_exp2, cfg_test_exp3, cfg_test_exp4, cfg_test_exp5

CFG_EXP: dict[str, dict] = dict(
    cfgexp1=cfg_test_exp1.CFG,
    cfgexp2=cfg_test_exp2.CFG,
    cfgexp3=cfg_test_exp3.CFG,
    cfgexp4=cfg_test_exp4.CFG,
    cfgexp5=cfg_test_exp5.CFG,
)


@pytest.fixture
def aeroval_out_path(tmp_path_factory) -> Path:
    """temporary path for aeroval outputs"""
    return tmp_path_factory.mktemp("aeroval")


@pytest.fixture(scope="session")
def aeroval_model_path(tmp_path_factory) -> Path:
    """temporary path for aeroval inputs"""
    return tmp_path_factory.mktemp("modeldata")


@pytest.fixture
def eval_config(cfg: str | None, aeroval_out_path: Path, aeroval_model_path: Path) -> dict:
    """aeroval configuration dispatcher"""
    if cfg is None:
        return {}
    if cfg not in CFG_EXP:
        raise ValueError(f"Unknown {cfg=}")
    config = deepcopy(CFG_EXP[cfg])
    config.update(
        json_basedir=f"{aeroval_out_path}/data",
        coldata_basedir=f"{aeroval_out_path}/coldata",
    )
    if cfg == "cfgexp3":
        config.update(
            model_cfg=cfg_test_exp3.fake_model_data(aeroval_model_path),
        )
    if cfg == "cfgexp5":
        config.update(
            model_cfg=cfg_test_exp5.fake_model_data(aeroval_model_path),
            obs_cfg=cfg_test_exp5.fake_obs_data(aeroval_model_path),
        )
    return config
