import os.path
import pathlib

import pyaro
import aerovaldb
import aerovaldb.routes

from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.aeroval.config.ciconfigs.base_config import get_CFG
from pyaerocom.io import ReadUngridded
from pyaerocom.io import ReadGridded

import pytest

reportyear = year = 2018
CFG = get_CFG(
    reportyear=reportyear,
    year=year,
)

TEST_FILE = "mep-rd-Birkenes-2018-001.nc"


@pytest.mark.skip(
    reason="This test is skipped because the pyaro reader is not available in the current tox environment for testing on CI."
)
def test_harp_reader_available():
    """quick test to make sure pyaro_readers is working"""
    engine = "harp"
    assert engine in pyaro.list_timeseries_engines()


@pytest.mark.skip(
    reason="This test is skipped because the pyaro reader is not available in the current tox environment for testing on CI."
)
def test_harp_test_data_available():
    obs_config = CFG["obs_cfg"]
    conf_name = list(obs_config.keys())[0]
    data_path = pathlib.Path(
        dict(CFG["obs_cfg"][conf_name]["pyaro_config"])["filename_or_obj_or_url"]
    )
    tmp = data_path.glob("*.nc")
    data_files = [x.name for x in tmp if x.is_file()]
    assert len(data_files) > 0
    assert TEST_FILE in data_files


@pytest.mark.skip(
    reason="This test is skipped because the pyaro reader is not available in the current tox environment for testing on CI."
)
def test_obs_data_readable():
    """test reading obs data using pyaerocom"""

    reportyear = year = 2018
    CFG = get_CFG(
        reportyear=reportyear,
        year=year,
    )
    for aeroval_obs_name in CFG["obs_cfg"]:
        config = CFG["obs_cfg"][aeroval_obs_name]["pyaro_config"]
        reader = ReadUngridded(configs=config)
        data = reader.read()
        assert data


def test_aux_file_available():
    """test if the aux file is available"""

    reportyear = year = 2018
    CFG = get_CFG(
        reportyear=reportyear,
        year=year,
    )
    assert os.path.exists(CFG["io_aux_file"])


def test_model_data_readable():
    """test reading model data using pyaerocom"""

    reportyear = year = 2018
    CFG = get_CFG(
        reportyear=reportyear,
        year=year,
    )
    assert CFG
    for aeroval_model_name in CFG["model_cfg"]:
        #
        data = ReadGridded(data_id=CFG["model_cfg"][aeroval_model_name]["model_id"])
        assert data


@pytest.mark.skip(
    reason="This test is skipped because the pyaro reader is not available in the current tox environment for testing on CI."
)
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

    ana.run()
    diurnals = ana.exp_output.avdb.query(aerovaldb.routes.Route.TIMESERIES_WEEKLY)
    assert len(diurnals) > 0
