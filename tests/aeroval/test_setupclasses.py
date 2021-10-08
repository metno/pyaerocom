import pytest
from pyaerocom.aeroval import setupclasses as mod
from pyaerocom.exceptions import EvalEntryNameError

from .cfg_test_exp1 import CFG as cfgexp1
from ..conftest import does_not_raise_exception

@pytest.mark.parametrize('kwargs,raises', [
    (cfgexp1,does_not_raise_exception())
])
def test_EvalSetup___init__(kwargs,raises):
    with raises:
        stp = mod.EvalSetup(**kwargs)


@pytest.mark.parametrize('update,raises',[
    (dict(model_cfg=dict(WRONG_MODEL=cfgexp1['model_cfg']['TM5-AP3-CTRL'])),
     pytest.raises(EvalEntryNameError)),
    (dict(obs_cfg=dict(WRONG_OBS=cfgexp1['obs_cfg']['AERONET-Sun'])),
     pytest.raises(EvalEntryNameError)),
    (dict(obs_cfg=dict(OBS=cfgexp1['obs_cfg']['AERONET-Sun'])),
     does_not_raise_exception()),
    (dict(obs_cfg=dict(OBS=dict(web_interface_name='WRONG_OBS'))),
     pytest.raises(EvalEntryNameError)),
])
def test_EvalSetup___init__INVALID_ENTRY_NAMES(update,raises):
    CFG = {**cfgexp1}
    CFG.update(**update)
    with raises:
        stp = mod.EvalSetup(**CFG)
