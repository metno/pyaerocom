import pytest
import pyaerocom.aeroval.utils as mod
from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from .cfg_test_exp1 import CFG as cfg1

from ._outbase import ADD_MODELS_DIR
from ..conftest import does_not_raise_exception
from .._conftest_helpers import add_dummy_model_data

# create some fake AOD model data
MODEL_DIR = add_dummy_model_data('od550aer', '1', 'daily',
                                 'Surface', year=2010, lat_range=(-90,90),
                                 lon_range=(-180,180),
                                 tmpdir=ADD_MODELS_DIR)


def test_make_config_template():
    val = mod.make_config_template('bla', 'blub')
    assert isinstance(val, EvalSetup)

@pytest.mark.parametrize('addargs,raises', [
    (dict(), does_not_raise_exception())
])
def test_compute_model_average_and_diversity(addargs,raises):
    with pytest.raises(ValueError):
        mod.compute_model_average_and_diversity(42, 'od550aer')

    CFG = {**cfg1}
    # need more than one model
    CFG['model_cfg']['DUMMY-MODEL'] = dict(model_id='DUMMY-MODEL',
                                           model_data_dir=MODEL_DIR)

    stp = EvalSetup(**CFG)
    proc = ExperimentProcessor(stp)
    with raises:
        mod.compute_model_average_and_diversity(proc, 'od550aer', **addargs)