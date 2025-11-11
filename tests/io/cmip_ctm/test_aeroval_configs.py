from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.aeroval.config.ciconfigs.cmip_config import get_CFG


def test_cmip_config():
    """short test if the example configuration for pm ratios is still in the code"""

    # start_time = "2013-06-01"
    # stop_time = "2014-06-01"
    CFG = get_CFG()
    assert not CFG["raise_exceptions"]
    stp = EvalSetup(**CFG)

    # stp = EvalSetup(proj_id='BLA', exp_id='blub',obs_cfg=OBS)

    ana = ExperimentProcessor(stp)
    ana.run()
