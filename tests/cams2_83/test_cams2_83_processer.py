import pytest

from pyaerocom.aeroval import EvalSetup
from pyaerocom.scripts.cams2_83.processer import CAMS2_83_Processer


@pytest.mark.usefixtures("fake_CAMS2_83_Engine")
def test__run_single_entry(patched_config):
    setup = EvalSetup(**patched_config)
    processer = CAMS2_83_Processer(setup)
    breakpoint()
    result = processer._run_single_entry(
        model_name="ENSEMBLE", obs_name="EEA", var_list=["concno2"], analysis=False
    )
    assert result
