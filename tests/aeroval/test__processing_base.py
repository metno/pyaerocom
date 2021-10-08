import pytest

from pyaerocom import Colocator
from pyaerocom.aeroval import _processing_base as mod, EvalSetup
from pyaerocom.aeroval.experiment_output import ExperimentOutput
from pyaerocom.exceptions import EntryNotAvailable

from ..conftest import does_not_raise_exception

obs_cfg=dict(
    obs1=dict(obs_id='obs1',obs_vars=['od550aer'], obs_vert_type='Column'),
    obs2=dict(obs_id='obs2',obs_vars=['od550aer'], obs_vert_type='Column',
              diurnal_only=True)
)
dummy_setup = EvalSetup('bla', 'blub', obs_cfg=obs_cfg)

class TestHasConfig:
    def test___init__(self):
        val = mod.HasConfig(dummy_setup)
        assert isinstance(val.cfg, EvalSetup)
        assert isinstance(val.exp_output, ExperimentOutput)


    def test_raise_exceptions(self):
        assert mod.HasConfig(dummy_setup).raise_exceptions == False


    def test_reanalyse_existing(self):
        assert mod.HasConfig(dummy_setup).reanalyse_existing == True

class TestHasColocator:
    def test__get_diurnal_only(self):
        val = mod.HasColocator(dummy_setup)
        assert val._get_diurnal_only('obs1') == False
        assert val._get_diurnal_only('obs2') == True

    @pytest.mark.parametrize('args,raises', [
        (dict(), does_not_raise_exception()),
        (dict(obs_name='obs1'), does_not_raise_exception()),
        (dict(obs_name='obs2'), does_not_raise_exception()),
        (dict(model_name='mod2'), pytest.raises(EntryNotAvailable)),

    ])
    def test_get_colocator(self,args,raises):
        val = mod.HasColocator(dummy_setup)
        with raises:
            col = val.get_colocator(**args)
            assert isinstance(col, Colocator)

