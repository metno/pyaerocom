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
