import numpy as np
import pytest

# from pyaerocom import ColocatedData, Colocator
from pyaerocom.aeroval import EvalSetup  # , ExperimentProcessor
from pyaerocom.aeroval._processing_base import HasColocator, ProcessingEngine  # , ExperimentOutput
from pyaerocom.aeroval.fairmode_engine import SPECIES, FairmodeEngine

# from tests.fixtures.aeroval.cfg_test_fairmode import CFG, fairmode_cfg
from tests.fixtures.collocated_data import COLDATA


@pytest.mark.parametrize("cfg", ["cfgexp1"])
@pytest.mark.filterwarnings("ignore:divide by zero encountered in .*divide:RuntimeWarning")
def test__fairmode_statistics(eval_config: dict):
    example_coldata = COLDATA["tm5_aeronet"]()

    # add fake station_type
    fake_types = ["bla"] * example_coldata.coords["station_name"].shape[0]

    example_coldata.data = example_coldata.data.assign_coords(
        station_type=("station_name", fake_types)
    )

    # rename variable to pretend it's a fairmode species
    example_coldata.data = example_coldata.data.assign_attrs(var_name=["concno2", "concno2"])

    setup = EvalSetup(**eval_config)
    fairmode_engine = FairmodeEngine(setup)

    assert isinstance(fairmode_engine, ProcessingEngine)
    assert isinstance(fairmode_engine, HasColocator)

    fm_stats = fairmode_engine.fairmode_statistics(example_coldata, "concno2")

    assert not fm_stats["Agoufou"]["persistence_model"]
    assert fm_stats["Agoufou"]["station_type"] == np.str_("bla")
    assert fm_stats["Agoufou"]["freq"] == "hourly"
    assert all(
        fm_stats["Agoufou"][item] == SPECIES["concno2"][item]
        for item in ["freq", "alpha", "percentile", "RV", "UrRV"]
    )
    assert all(
        item in fm_stats["Agoufou"]
        for item in ["RMSU", "sign", "beta_mqi", "Hperc", "crms", "bias", "rms"]
    )


# from tests.fixtures.pyaro import testconfig2


# @pytest.fixture
# def fairmode_coldata(tmp_path) -> tuple[FairmodeEngine, ColocatedData, Colocator]:
#    model_name = "EMEP"
#    obs_name = "testdata-d"
#    cfg = fairmode_cfg(tmp_path)
#    setup = EvalSetup(**cfg)

#    engine = FairmodeEngine(setup)

#    col = engine.get_colocator(model_name, obs_name)
#    data = col.run()
#    # files_to_convert = col.get_available_coldata_files(var_list)

#    return engine, data, col


# def test___init__(tmp_path):
#    cfg = fairmode_cfg(tmp_path)
#    setup = EvalSetup(**cfg)
#    fe = FairmodeEngine(setup)
#    assert isinstance(fe, ProcessingEngine)
#    assert isinstance(fe, HasColocator)


# def test_fairmode_statistics(fairmode_coldata):

#    engine, data, col = fairmode_coldata
#    conc_data = data["concpm10"]["concpm10"]
#    stats = engine.fairmode_statistics(conc_data, "concpm10")
#    assert isinstance(engine, FairmodeEngine)
