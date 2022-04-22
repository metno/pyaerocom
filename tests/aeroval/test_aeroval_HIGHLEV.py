import glob
import os

import pytest

from pyaerocom.aeroval import ExperimentProcessor
from pyaerocom.aeroval.setupclasses import EvalSetup

from ..conftest import geojson_unavail
from .cfg_test_exp1 import CFG as cfgexp1
from .cfg_test_exp2 import CFG as cfgexp2
from .cfg_test_exp4 import CFG as cfgexp4

CHK_CFG1 = {
    "map": ["AERONET-Sun-od550aer_Column_TM5-AP3-CTRL-od550aer.json"],
    "contour": ["od550aer_TM5-AP3-CTRL.geojson", "od550aer_TM5-AP3-CTRL.json"],
    "hm": ["glob_stats_daily.json", "glob_stats_monthly.json", "glob_stats_yearly.json"],
    "hm/ts": ["stats_ts.json"],
    "scat": ["AERONET-Sun-od550aer_Column_TM5-AP3-CTRL-od550aer.json"],
    "ts": 11,  # number of .json files in subdir
    "ts/diurnal": 0,  # number of .json files in subdir
}

CHK_CFG2 = {
    "map": [
        "AERONET-Sun-od550aer_Column_TM5-AP3-CTRL-od550aer.json",
        "AERONET-SDA-od550aer_Column_TM5-AP3-CTRL-od550aer.json",
    ],
    "contour": 0,
    "hm": ["glob_stats_monthly.json"],
    "hm/ts": ["stats_ts.json"],
    "scat": [
        "AERONET-Sun-od550aer_Column_TM5-AP3-CTRL-od550aer.json",
        "AERONET-SDA-od550aer_Column_TM5-AP3-CTRL-od550aer.json",
    ],
    "ts": 40,  # number of .json files in subdir
    "ts/diurnal": 0,  # number of .json files in subdir
}

CHK_CFG4 = {
    "map": ["SDA-and-Sun-od550aer_Column_TM5-AP3-CTRL-od550aer.json"],
    "contour": 0,
    "hm": ["glob_stats_monthly.json"],
    "hm/ts": ["stats_ts.json"],
    "scat": ["SDA-and-Sun-od550aer_Column_TM5-AP3-CTRL-od550aer.json"],
    "ts": 21,  # number of .json files in subdir
    "ts/diurnal": 0,  # number of .json files in subdir
}


@geojson_unavail
@pytest.mark.parametrize(
    "cfgdict,chk_files",
    [
        (cfgexp1, CHK_CFG1),
        (cfgexp2, CHK_CFG2),
        (cfgexp4, CHK_CFG4),
    ],
)
def test_ExperimentOutput__FILES(cfgdict, chk_files):
    cfg = EvalSetup(**cfgdict)
    fname = f"cfg_{cfg.proj_id}_{cfg.exp_id}.json"
    proc = ExperimentProcessor(cfg)
    proc.exp_output.delete_experiment_data(also_coldata=True)
    proc.run()

    output = proc.exp_output
    assert os.path.exists(output.exp_dir)
    assert os.path.exists(output.experiments_file)
    assert os.path.exists(output.var_ranges_file)
    assert os.path.exists(output.statistics_file)
    assert os.path.exists(output.menu_file)
    assert os.path.exists(os.path.join(output.exp_dir, fname))
    for key, val in cfg.path_manager.get_json_output_dirs().items():
        assert os.path.exists(val)
        files = os.listdir(val)
        if key in chk_files:
            check = chk_files[key]
            if isinstance(check, list):
                for fname in check:
                    assert fname in files
            elif isinstance(check, int):
                numfiles = glob.glob(f"{val}/*.json")
                assert len(numfiles) == check


def test_reanalyse_existing():
    cfg = EvalSetup(**cfgexp4)
    assert cfg.colocation_opts.reanalyse_existing == True
    proc = ExperimentProcessor(cfg)
    proc.exp_output.delete_experiment_data(also_coldata=True)
    proc.run()
    colout = os.path.join(proc.cfg.path_manager.coldata_basedir, proc.cfg.proj_id, proc.cfg.exp_id)
    assert os.path.exists(colout)
    coldata_files = glob.glob(f"{colout}/**/*.nc")
    assert len(coldata_files) > 0
    proc.exp_output.delete_experiment_data(also_coldata=False)
    assert os.path.exists(colout)
    coldata_files = glob.glob(f"{colout}/**/*.nc")
    assert len(coldata_files) > 0
    cfg.colocation_opts.reanalyse_existing = False
    proc = ExperimentProcessor(cfg)
    assert proc.reanalyse_existing == False
    proc.run()
    proc.exp_output.delete_experiment_data(also_coldata=True)
    proc.run()


def test_superobs_different_resolutions():
    cfg = EvalSetup(**cfgexp4)
    cfg.model_cfg["TM5-AP3-CTRL"].model_ts_type_read = None
    cfg.model_cfg["TM5-AP3-CTRL"].flex_ts_type = True

    cfg.obs_cfg["AERONET-Sun"].ts_type = "daily"
    cfg.obs_cfg["AERONET-SDA"].ts_type = "monthly"

    proc = ExperimentProcessor(cfg)
    proc.exp_output.delete_experiment_data(also_coldata=True)
    proc.run()
