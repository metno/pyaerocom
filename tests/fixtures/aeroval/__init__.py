from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from .cams84 import CAMS84_CONFIG
from .cfg_test_exp1 import CFG as cfgexp1
from .cfg_test_exp2 import CFG as cfgexp2
from .cfg_test_exp3 import CFG as cfgexp3
from .cfg_test_exp3 import fake_model_data as fake_model_exp3
from .cfg_test_exp4 import CFG as cfgexp4
from .cfg_test_exp5 import CFG as cfgexp5
from .cfg_test_exp5 import fake_model_data as fake_model_exp5
from .cfg_test_exp5 import fake_obs_data as fake_obs_exp5
from .common import (
    add_dummy_model_data,
    aeroval_model_path,
    aeroval_out_path,
    make_dummy_cube_3D_daily,
)

CFG_EXP: dict[str, dict] = dict(
    cfgexp1=cfgexp1,
    cfgexp2=cfgexp2,
    cfgexp3=cfgexp3,
    cfgexp4=cfgexp4,
    cfgexp5=cfgexp5,
)


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
            model_cfg=fake_model_exp3(aeroval_model_path),
        )
    if cfg == "cfgexp5":
        config.update(
            model_cfg=fake_model_exp5(aeroval_model_path),
            obs_cfg=fake_obs_exp5(aeroval_model_path),
        )
    return config
