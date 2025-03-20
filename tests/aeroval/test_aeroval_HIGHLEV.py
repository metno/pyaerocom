from __future__ import annotations

from pathlib import Path

import pytest

from pyaerocom.aeroval import ExperimentProcessor
from pyaerocom.aeroval.experiment_output import ExperimentOutput
from pyaerocom.aeroval import EvalSetup

CHK_CFG1 = {
    "map": ["AERONET-Sun_od550aer_Column_TM5-AP3-CTRL_od550aer_2010.json"],
    "contour": 0,
    "hm": [
        "glob_stats_daily.json",
        "glob_stats_monthly.json",
        "glob_stats_yearly.json",
    ],
    "hm/ts": 10,  # number of .json files in sub dir
    "scat": ["AERONET-Sun_od550aer_Column_TM5-AP3-CTRL_od550aer_2010.json"],
    "ts": 11,  # number of .json files in subdir
    "ts/diurnal": 0,  # number of .json files in subdir
}

CHK_CFG2 = {
    "map": [
        "AERONET-SDA_od550aer_Column_TM5-AP3-CTRL_od550aer_2010.json",
        "AERONET-Sun_od550aer_Column_TM5-AP3-CTRL_od550aer_2010.json",
    ],
    "contour": 0,
    "hm": ["glob_stats_monthly.json"],
    "hm/ts": 21,
    "scat": [
        "AERONET-SDA_od550aer_Column_TM5-AP3-CTRL_od550aer_2010.json",
        "AERONET-Sun_od550aer_Column_TM5-AP3-CTRL_od550aer_2010.json",
    ],
    "ts": 40,
    "ts/diurnal": 0,  # number of .json files in subdir
}

CHK_CFG4 = {
    "map": ["SDA-and-Sun_od550aer_Column_TM5-AP3-CTRL_od550aer_2010.json"],
    "contour": 0,
    "hm": ["glob_stats_monthly.json"],
    "hm/ts": 10,  # number of .json files in subdir
    "scat": ["SDA-and-Sun_od550aer_Column_TM5-AP3-CTRL_od550aer_2010.json"],
    "ts": 21,  # number of .json files in subdir
    "ts/diurnal": 0,  # number of .json files in subdir
}


@pytest.mark.parametrize(
    "cfg,chk_files",
    [
        ("cfgexp1", CHK_CFG1),
        ("cfgexp2", CHK_CFG2),
        ("cfgexp4", CHK_CFG4),
    ],
)
def test_ExperimentOutput__FILES(eval_config: dict, chk_files: dict):
    cfg = EvalSetup(**eval_config)
    proc = ExperimentProcessor(cfg)
    proc.exp_output.delete_experiment_data(also_coldata=True)
    proc.run()

    output: ExperimentOutput = proc.exp_output
    assert Path(output.exp_dir).is_dir()
    assert Path(output.experiments_file).exists()

    output.avdb.get_statistics(output.proj_id, output.exp_id)
    output.avdb.get_menu(output.proj_id, output.exp_id)
    output.avdb.get_ranges(output.proj_id, output.exp_id)

    output.avdb.get_config(output.proj_id, output.exp_id)

    for key, path in cfg.path_manager.get_json_output_dirs().items():
        path = Path(path)
        assert path.is_dir()
        if key not in chk_files:
            continue

        check = chk_files[key]
        if isinstance(check, list):
            files = [file.name for file in path.iterdir()]
            assert all(file in files for file in check)
        elif isinstance(check, int):
            files = list(path.glob("*.json"))
            assert len(files) == check


@pytest.mark.parametrize("cfg,reanalyse_existing", [("cfgexp4", True), ("cfgexp4", False)])
def test_reanalyse_existing(eval_config: dict, reanalyse_existing: bool):
    eval_config["reanalyse_existing"] = reanalyse_existing
    cfg = EvalSetup(**eval_config)
    assert cfg.colocation_opts.reanalyse_existing == reanalyse_existing
    output = Path(cfg.path_manager.coldata_basedir) / cfg.proj_id / cfg.exp_id

    proc = ExperimentProcessor(cfg)
    proc.exp_output.delete_experiment_data(also_coldata=True)
    assert not output.exists()

    proc.run()
    assert output.is_dir()
    assert list(output.glob("**/*.nc"))

    proc.exp_output.delete_experiment_data(also_coldata=False)
    assert output.is_dir()
    assert list(output.glob("**/*.nc"))


@pytest.mark.parametrize("cfg", ["cfgexp4"])
def test_superobs_different_resolutions(eval_config: dict):
    cfg = EvalSetup(**eval_config)
    cfg.model_cfg.get_entry("TM5-AP3-CTRL").model_ts_type_read = None
    cfg.model_cfg.get_entry("TM5-AP3-CTRL").flex_ts_type = True

    cfg.obs_cfg.get_entry("AERONET-Sun").ts_type = "daily"
    cfg.obs_cfg.get_entry("AERONET-SDA").ts_type = "monthly"

    proc = ExperimentProcessor(cfg)
    proc.exp_output.delete_experiment_data(also_coldata=True)
    proc.run()
