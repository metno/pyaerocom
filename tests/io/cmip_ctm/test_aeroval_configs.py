from pathlib import Path

from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.aeroval.config.ciconfigs.cmip_config import get_CFG

MYPYAEROCOM_DIR = Path.home() / "MyPyaerocom"
JSON_DIR = MYPYAEROCOM_DIR / "tmp" / "data"
COLDATA_DIR = MYPYAEROCOM_DIR / "tmp" / "coldata"

MODELDIR = MYPYAEROCOM_DIR / "testdata-minimal" / "modeldata" / "CMIP6"
PROJECT_ID = "CMIPCI"
EXP_ID = "CMIP-testing-reporting"


def test_cmip_config():
    """run quick CMIP data based aeroval analysis"""

    CFG = get_CFG()
    stp = EvalSetup(**CFG)
    ana = ExperimentProcessor(stp)
    ana.run()
    assert JSON_DIR.exists()
    assert COLDATA_DIR.exists()
    assert JSON_DIR.joinpath("CMIPCI").exists()
    assert JSON_DIR.joinpath("CMIPCI", EXP_ID).exists()
    ts_path = JSON_DIR.joinpath("CMIPCI", EXP_ID, "ts")
    assert ts_path.exists()
    # count the number of json files in there
    # the expected number is 232
    files_found = 0
    for _file in ts_path.rglob("*.json"):
        if _file.is_file():
            files_found += 1
    assert files_found > 230
