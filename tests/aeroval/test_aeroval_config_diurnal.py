import pathlib

from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.aeroval.config.ciconfigs.base_config import get_CFG


def test_aeroval_config_diurnal():
    """test to make sure diurnal cycle analysis works
    The data used is entirely fake
    This test just checks if json files below ts/diurnal have been created"""

    reportyear = year = 2018
    CFG = get_CFG(
        reportyear=reportyear,
        year=year,
    )

    stp = EvalSetup(**CFG)
    ana = ExperimentProcessor(stp)
    ana.update_interface()

    res = ana.run()
    diurnal_path = (
        pathlib.Path(CFG["json_basedir"]) / CFG["proj_id"] / CFG["exp_id"] / "ts" / "diurnal"
    )
    assert diurnal_path.exists()
    tmp = diurnal_path.glob("*.json")
    diurnal_files = [x for x in tmp if x.is_file()]
    assert len(diurnal_files) > 1
