import pytest

from pyaerocom.aeroval.fairmode_engine import FairmodeEngine
from pyaerocom import ColocatedData, Colocator
from pyaerocom.aeroval import ExperimentProcessor
from pyaerocom.aeroval._processing_base import HasColocator, ProcessingEngine, ExperimentOutput
from pyaerocom.aeroval import EvalSetup

from tests.fixtures.aeroval.cfg_test_fairmode import CFG, fairmode_cfg

# from tests.fixtures.pyaro import testconfig2


@pytest.fixture
def fairmode_coldata(tmp_path) -> tuple[FairmodeEngine, ColocatedData, Colocator]:
    model_name = "EMEP"
    obs_name = "testdata-d"
    cfg = fairmode_cfg(tmp_path)
    setup = EvalSetup(**cfg)
    
    engine = FairmodeEngine(setup)

    col = engine.get_colocator(model_name, obs_name)
    data = col.run()
    # files_to_convert = col.get_available_coldata_files(var_list)

    return engine, data, col



def test___init__(tmp_path):
    cfg = fairmode_cfg(tmp_path)
    setup = EvalSetup(**cfg)
    fe = FairmodeEngine(setup)
    assert isinstance(fe, ProcessingEngine)
    assert isinstance(fe, HasColocator)

def test_fairmode_statistics(fairmode_coldata):
    
    engine, data, col = fairmode_coldata
    conc_data = data["concpm10"]["concpm10"]
    stats = engine.fairmode_statistics(conc_data, "concpm10")
    assert isinstance(engine, FairmodeEngine)
    
