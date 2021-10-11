import pytest
import pyaerocom.aeroval.utils as mod
from pyaerocom import GriddedData
from pyaerocom.aeroval import EvalSetup, ExperimentProcessor

from .cfg_test_exp1 import CFG as cfg1
from .cfg_test_exp2 import CFG as cfg2

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

from copy import deepcopy
CFG1 = deepcopy(cfg1)
# need more than one model
CFG1['model_cfg']['DUMMY-MODEL'] = dict(model_id='DUMMY-MODEL',
                                       model_data_dir=MODEL_DIR)
CFG2 = deepcopy(cfg2)
# need more than one model
CFG2['model_cfg']['DUMMY-MODEL'] = dict(model_id='DUMMY-MODEL',
                                       model_data_dir=MODEL_DIR)

@pytest.mark.parametrize('cfg,addargs,raises', [
    (cfg1, dict(), pytest.raises(ValueError)),
    (cfg1, dict(avg_how='bla'), pytest.raises(ValueError)),
    (CFG1, dict(avg_how='bla'), pytest.raises(ValueError)),
    (CFG2, dict(), does_not_raise_exception()),
    (CFG2, dict(avg_how='mean'), does_not_raise_exception()),
])
def test_compute_model_average_and_diversity(cfg,addargs,raises):
    with pytest.raises(ValueError):
        mod.compute_model_average_and_diversity(42, 'od550aer')

    stp = EvalSetup(**cfg)
    proc = ExperimentProcessor(stp)
    with raises:
        (avg_out, div_out, q1_out, q3_out, std_out) = \
            mod.compute_model_average_and_diversity(proc, 'od550aer',
                                                    **addargs)

        try:
            avghow = addargs['avg_how']
        except KeyError:
            avghow = 'median'

        assert isinstance(avg_out, GriddedData)
        assert isinstance(div_out, GriddedData)
        if avghow == 'median':
            assert isinstance(q1_out, GriddedData)
            assert isinstance(q3_out, GriddedData)
        else:
            assert isinstance(std_out, GriddedData)

