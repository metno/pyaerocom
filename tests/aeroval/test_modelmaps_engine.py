import pytest

from pyaerocom.aeroval.modelmaps_engine import ModelMapsEngine
from pyaerocom.aeroval.setupclasses import EvalSetup
from pyaerocom.exceptions import ModelVarNotAvailable
from tests.fixtures.aeroval.cfg_test_exp1 import CFG


def test__process_map_var():
    stp = EvalSetup(**CFG)
    engine = ModelMapsEngine(stp)
    with pytest.raises(ModelVarNotAvailable) as excinfo:
        engine._process_map_var("LOTOS", "concco", False)
    assert "Cannot read data for model LOTOS" in str(excinfo.value)


def test__run(caplog):
    stp = EvalSetup(**CFG)
    engine = ModelMapsEngine(stp)
    engine.run(model_list=["TM5-AP3-CTRL"], var_list=["conco"])
    assert "no data for model TM5-AP3-CTRL, skipping" in caplog.text


@pytest.mark.parametrize(
    "maps_freq, result",
    [("monthly", "monthly"), ("yearly", "yearly"), ("coarsest", "yearly")],
)
def test__get_maps_freq(maps_freq, result):
    CFG2 = CFG.copy()
    CFG2["maps_freq"] = maps_freq
    stp = EvalSetup(**CFG2)
    engine = ModelMapsEngine(stp)
    freq = engine._get_maps_freq()

    assert freq == result


@pytest.mark.parametrize(
    "maps_freq,result,ts_types",
    [
        ("monthly", "monthly", ["daily", "monthly", "yearly"]),
        ("yearly", "yearly", ["daily", "monthly", "yearly"]),
        ("coarsest", "yearly", ["daily", "monthly", "yearly"]),
        ("coarsest", "monthly", ["hourly", "daily", "monthly"]),
        ("coarsest", "daily", ["weekly", "daily"]),
    ],
)
def test__get_read_model_freq(maps_freq, result, ts_types):
    CFG2 = CFG.copy()
    CFG2["maps_freq"] = maps_freq
    stp = EvalSetup(**CFG2)
    engine = ModelMapsEngine(stp)
    freq = engine._get_read_model_freq(ts_types)

    assert freq == result


@pytest.mark.parametrize(
    "maps_freq,ts_types,errormsg",
    [
        (
            "daily",
            ["monthly", "yearly"],
            "Could not find any model data for given maps_freq.*",
        ),
        (
            "coarsest",
            ["hourly", "weekly"],
            "Could not find any TS type to read maps",
        ),
    ],
)
def test__get_read_model_freq_error(maps_freq, ts_types, errormsg):
    CFG2 = CFG.copy()
    CFG2["maps_freq"] = maps_freq
    stp = EvalSetup(**CFG2)
    engine = ModelMapsEngine(stp)

    with pytest.raises(ValueError, match=errormsg):
        freq = engine._get_read_model_freq(ts_types)
