from pyaerocom.aeroval.config.ciconfigs.cmip_config import get_CFG


def test_cmip_config():
    """short test if the example configuration for pm ratios is still in the code"""

    year = 2019
    CFG = get_CFG(
        year=year,
    )
    assert not CFG["raise_exceptions"]
