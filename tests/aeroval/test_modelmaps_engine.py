from pyaerocom.aeroval.modelmaps_engine import ModelMapsEngine
from pyaerocom.aeroval.setupclasses import EvalSetup
from pyaerocom.exceptions import ModelVarNotAvailable
from tests.fixtures.aeroval.cfg_test_exp1 import CFG


def test__process_map_var():
    stp = EvalSetup(**CFG)
    engine = ModelMapsEngine(stp)
    try:
        engine._process_map_var("LOTOS", "concco", False)
    except ModelVarNotAvailable as e:
        # print(e)
        assert "no such entry LOTOS" in str(e)
    else:
        assert False


def test__run(caplog):
    stp = EvalSetup(**CFG)
    engine = ModelMapsEngine(stp)
    engine.run(model_list=["TM5-AP3-CTRL"], var_list=["conco"])
    assert "no data for model TM5-AP3-CTRL, skipping" in caplog.text
