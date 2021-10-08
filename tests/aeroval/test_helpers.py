import pytest
import pyaerocom.aeroval.helpers as mod
from pyaerocom.aeroval import EvalSetup
from .cfg_test_exp1 import CFG as cfg1

@pytest.mark.parametrize('cfg,len,raises', [
    (cfg1,None,pytest.raises(NotImplementedError))
])
def test_make_info_str_eval_setup(cfg,len,raises):
    stp = EvalSetup(**cfg)
    with raises:
        st = mod.make_info_str_eval_setup(stp)
        assert len(st) == len