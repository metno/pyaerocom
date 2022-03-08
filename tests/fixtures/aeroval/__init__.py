from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from .cams84 import CAMS84_CONFIG
from .cfg_test_exp1 import CFG as cfgexp1
from .cfg_test_exp2 import CFG as cfgexp2
from .cfg_test_exp3 import CFG as cfgexp3
from .cfg_test_exp3 import fake_model_data
from .cfg_test_exp4 import CFG as cfgexp4
from .cfg_test_exp5 import CFG as cfgexp5
from .common import (
    add_dummy_model_data,
    aeroval_model_path,
    aeroval_out_path,
    make_dummy_cube_3D_daily,
)


@pytest.fixture
def eval_config(cfg: str | dict | None, aeroval_out_path: Path, aeroval_model_path: Path) -> dict:
    """aeroval configuration dispacher"""
    if cfg is None:
        return {}
    if isinstance(cfg, dict):
        return cfg
    config: dict[str, dict] = dict(
        cfgexp1=cfgexp1,
        cfgexp2=cfgexp2,
        cfgexp3=cfgexp3,
        cfgexp4=cfgexp4,
    )
    if cfg not in config:
        raise ValueError(f"Unknown {cfg=}")
    cfg_name, cfg = cfg, deepcopy(config[cfg])
    cfg.update(
        json_basedir=f"{aeroval_out_path}/data",
        coldata_basedir=f"{aeroval_out_path}/coldata",
    )
    if cfg_name == "cfgexp3":
        cfg.update(model_cfg=fake_model_data(aeroval_model_path))
    return cfg
