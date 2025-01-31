import pathlib

import pyaro

from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.aeroval.config.ciconfigs.base_config import get_CFG

reportyear = year = 2018
CFG = get_CFG(
    reportyear=reportyear,
    year=year,
)

TEST_FILE = "mep-rd-Birkenes-2018-001.nc"


def test_harp_reader_available():
    """quick test to make sure pyaro_readers is working"""
    engine = "harp"
    assert engine in pyaro.list_timeseries_engines()


def test_harp_test_data_available():
    obs_config = CFG["obs_cfg"]
    conf_name = list(obs_config.keys())[0]
    data_path = dict(CFG["obs_cfg"][conf_name]["obs_config"])["filename_or_obj_or_url"]
    tmp = data_path.glob("*.nc")
    data_files = [x.name for x in tmp if x.is_file()]
    assert len(data_files) > 0
    assert TEST_FILE in data_files


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

    ana.run()
    diurnal_path = (
        # pathlib.Path(CFG["json_basedir"]) / CFG["proj_id"] / CFG["exp_id"] / "ts" / "diurnal"
            pathlib.Path(CFG["json_basedir"]) / CFG["proj_id"] / CFG["exp_id"]
    )
    assert diurnal_path.exists()
    tmp = diurnal_path.glob("*.json")
    diurnal_files = [x for x in tmp if x.is_file()]
    assert len(diurnal_files) > 1
