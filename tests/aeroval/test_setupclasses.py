import pytest

from pyaerocom.aeroval.setupclasses import EvalSetup
from pyaerocom.exceptions import EvalEntryNameError

from .cfg_test_exp1 import CFG as cfgexp1


@pytest.mark.parametrize(
    "update", [dict(), dict(obs_cfg=dict(OBS=cfgexp1["obs_cfg"]["AERONET-Sun"]))]
)
def test_EvalSetup___init__(update):
    CFG = cfgexp1.copy()
    CFG.update(update)
    EvalSetup(**CFG)


@pytest.mark.parametrize(
    "update, error",
    [
        (
            dict(model_cfg=dict(WRONG_MODEL=cfgexp1["model_cfg"]["TM5-AP3-CTRL"])),
            "Invalid name: WRONG_MODEL",
        ),
        (
            dict(obs_cfg=dict(WRONG_OBS=cfgexp1["obs_cfg"]["AERONET-Sun"])),
            "Invalid name: WRONG_OBS",
        ),
        (
            dict(obs_cfg=dict(OBS=dict(web_interface_name="WRONG_OBS"))),
            "Invalid name: WRONG_OBS",
        ),
    ],
)
def test_EvalSetup___init__INVALID_ENTRY_NAMES(update, error):
    CFG = cfgexp1.copy()
    CFG.update(update)
    with pytest.raises(EvalEntryNameError) as e:
        EvalSetup(**CFG)
    assert error in str(e.value)
