from pyaerocom.aeroval.config.pmratios.base_config import get_CFG


def test_ratpmconfig():
    """short test if the example configuration for pm ratios is still in the code"""

    reportyear = year = 2019
    CFG = get_CFG(
        reportyear=reportyear,
        year=year,
        model_dir="/lustre/storeB/project/fou/kl/CAMEO/u8_cams0201/",
    )
    assert not CFG["raise_exceptions"]
