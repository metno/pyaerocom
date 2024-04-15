from copy import deepcopy

import pytest

from pyaerocom.aeroval.modelmaps_engine import ModelMapsEngine
from pyaerocom.aeroval.setupclasses import EvalSetup
from tests.fixtures.aeroval.cfg_test_exp1 import CFG


def test__process_map_var(caplog):
    stp = EvalSetup(**CFG)
    engine = ModelMapsEngine(stp)
    engine._process_map_var("LOTOS", "concco", False)
    print(caplog.text)
    assert "no such entry LOTOS" in caplog.text
