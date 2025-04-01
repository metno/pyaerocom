import pathlib
from copy import deepcopy

import aerovaldb
import aerovaldb.routes
import pytest

from pyaerocom import GriddedData
from pyaerocom.aeroval import EvalSetup
from pyaerocom.aeroval.modelmaps_engine import ModelMapsEngine
from pyaerocom.exceptions import ModelVarNotAvailable
from tests.fixtures.aeroval.cfg_test_exp1 import CFG


@pytest.fixture(scope="function")
def cfg(tmpdir: pathlib.Path):
    cfg = deepcopy(CFG)
    cfg["json_basedir"] = f"{tmpdir}/data"
    cfg["coldata_basedir"] = f"{tmpdir}/coldata"

    return cfg


def test__process_map_var(cfg: dict):
    stp = EvalSetup(**cfg)
    engine = ModelMapsEngine(stp)
    with pytest.raises(ModelVarNotAvailable) as excinfo:
        engine._process_contour_map_var("LOTOS", "concco", False)

    assert "Cannot read data for model LOTOS" in str(excinfo.value)


def test__run(caplog, cfg: dict):
    stp = EvalSetup(**cfg)
    engine = ModelMapsEngine(stp)
    engine.run(model_list=["TM5-AP3-CTRL"], var_list=["conco"])
    assert "no data for model TM5-AP3-CTRL, skipping" in caplog.text


def test__run_reanalysefalse(tmp_path, caplog, cfg: dict):
    """Test the case reanalyse_existing=False for plot type contour"""

    cfg["reanalyse_existing"] = False
    # modify the config so to have just one output map geojson file, for simplicity
    cfg["ts_type"] = "daily"
    cfg["periods"] = ["20100615"]
    cfg["main_freq"] = "daily"

    json_basedir = tmp_path / "data"
    cfg["json_basedir"] = json_basedir
    # create expected geojson output file (empty file is ok:
    # in the case reanalyse_existing=False content is not checked, only existence)
    with aerovaldb.open(f"json_files:{json_basedir}") as db:
        db.put_contour("", "test", "exp1", "od550aer", "TM5-AP3-CTRL", timestep="1277942400000")

    stp = EvalSetup(**cfg)
    engine = ModelMapsEngine(stp)
    engine.run(model_list=["TM5-AP3-CTRL"], var_list=["od550aer"])
    assert (
        "Skipping contour processing of od550aer_TM5-AP3-CTRL: data already exists" in caplog.text
    )


def test__run_working(cfg: dict):
    cfg["plot_types"] = ("contour", "overlay")
    stp = EvalSetup(**cfg)
    engine = ModelMapsEngine(stp)
    engine.run(model_list=["TM5-AP3-CTRL"], var_list=["od550aer"])
    contours = engine.exp_output.avdb.query(aerovaldb.routes.Route.CONTOUR_TIMESPLIT)
    overlays = engine.exp_output.avdb.query(aerovaldb.routes.Route.MAP_OVERLAY)
    assert len(contours) > 0
    assert len(overlays) > 0
    assert contours[0].meta["obsvar"] == "od550aer"
    assert contours[0].meta["model"] == "TM5-AP3-CTRL"


@pytest.mark.parametrize(
    "maps_freq, result",
    [("monthly", "monthly"), ("yearly", "yearly"), ("coarsest", "yearly")],
)
def test__get_maps_freq(maps_freq, result, cfg: dict):
    cfg["maps_freq"] = maps_freq
    stp = EvalSetup(**cfg)
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
def test__get_read_model_freq(maps_freq, result, ts_types, cfg: dict):
    cfg["maps_freq"] = maps_freq
    stp = EvalSetup(**cfg)
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
    ],
)
def test__get_read_model_freq_error(maps_freq, ts_types, errormsg, cfg: dict):
    cfg["maps_freq"] = maps_freq
    stp = EvalSetup(**cfg)
    engine = ModelMapsEngine(stp)

    with pytest.raises(ValueError, match=errormsg):
        engine._get_read_model_freq(ts_types)


def test__read_model_data(cfg: dict):
    model_name = "TM5-AP3-CTRL"
    var_name = "od550aer"
    stp = EvalSetup(**cfg)
    engine = ModelMapsEngine(stp)

    data = engine._read_model_data(model_name, var_name)

    assert isinstance(data, GriddedData)
