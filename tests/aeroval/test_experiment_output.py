from __future__ import annotations

from pathlib import Path

import aerovaldb
import pytest

from pyaerocom import const
from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.aeroval.experiment_output import ExperimentOutput, ProjectOutput
from pyaerocom.aeroval.json_utils import read_json, write_json

BASEDIR_DEFAULT = Path(const.OUTPUTDIR) / "aeroval" / "data"


@pytest.fixture()
def dummy_expout(tmp_path: Path) -> ExperimentOutput:
    """ExperimentOutput instance"""
    setup = EvalSetup(proj_id="proj", exp_id="exp", json_basedir=str(tmp_path))
    return ExperimentOutput(setup)


def test_invalid_resource_error():
    with pytest.raises(ValueError):
        ProjectOutput("test", None)


def test_avdb_resource_init(tmp_path):
    with aerovaldb.open(str(tmp_path)) as db:
        val = ProjectOutput("test", db)

        assert val.avdb is db


@pytest.mark.parametrize(
    "proj_id,json_basedir",
    [
        ("bla", "/"),
    ],
)
def test_ProjectOutput(proj_id: str, json_basedir: str):
    val = ProjectOutput(proj_id, json_basedir)
    assert val.proj_id == proj_id
    if json_basedir is not None:
        assert Path(val.json_basedir).exists()


@pytest.mark.parametrize(
    "proj_id,json_basedir,exception,error",
    [
        pytest.param(42, None, ValueError, "need str, got 42", id="ValueError"),
    ],
)
def test_ProjectOutput_error(proj_id, json_basedir, exception: type[Exception], error: str):
    with pytest.raises(exception) as e:
        ProjectOutput(proj_id, json_basedir)
    assert str(e.value) == error


def test_ProjectOutput_proj_dir(tmp_path: Path):
    val = ProjectOutput("test", str(tmp_path))
    path = tmp_path / "test"
    assert val.proj_dir == str(path)
    assert path.exists()


def test_ProjectOutput_experiments_file(tmp_path: Path):
    val = ProjectOutput("test", str(tmp_path))
    path = tmp_path / "test" / "experiments.json"
    assert Path(val.experiments_file) == path


def test_ProjectOutput_available_experiments(tmp_path: Path):
    val = ProjectOutput("test", str(tmp_path))
    assert val.available_experiments == []

    write_json({"exp": 42}, val.experiments_file)
    assert val.available_experiments == ["exp"]


def test_ExperimentOutput__add_entry_experiments_json():
    cfg = EvalSetup(proj_id="proj", exp_id="exp")
    val = ExperimentOutput(cfg)

    val._add_entry_experiments_json("test", 42)
    assert val.available_experiments == ["test"]


def test_ExperimentOutput__del_entry_experiments_json(tmp_path):
    cfg = EvalSetup(proj_id="proj", exp_id="exp")
    val = ExperimentOutput(cfg)

    exp_id = "test"
    assert exp_id in val.available_experiments

    val._del_entry_experiments_json(exp_id)
    assert exp_id not in val.available_experiments


def test_ExperimentOutput():
    cfg = EvalSetup(proj_id="proj", exp_id="exp")
    val = ExperimentOutput(cfg)
    assert isinstance(val.cfg, EvalSetup)
    assert val.proj_id == cfg.proj_info.proj_id

    path = Path(val.json_basedir)
    assert path == BASEDIR_DEFAULT
    assert path.exists()


def test_ExperimentOutput_error():
    with pytest.raises(ValueError):
        ExperimentOutput(None)


def test_ExperimentOutput_exp_id(dummy_expout: ExperimentOutput):
    assert dummy_expout.exp_id == "exp"


def test_ExperimentOutput_exp_dir(dummy_expout: ExperimentOutput, tmp_path: Path):
    assert Path(dummy_expout.exp_dir) == tmp_path / "proj" / "exp"


def test_ExperimentOutput_results_available_False(dummy_expout: ExperimentOutput):
    assert not dummy_expout.results_available


def test_ExperimentOutput_update_menu_EMPTY(dummy_expout: ExperimentOutput):
    dummy_expout.update_menu()

    data = dummy_expout.avdb.get_menu(dummy_expout.proj_id, dummy_expout.exp_id)
    assert data == {}


def test_ExperimentOutput_update_interface_EMPTY(dummy_expout: ExperimentOutput):
    dummy_expout.update_interface()


def test_ExperimentOutput_update_heatmap_json_EMPTY(dummy_expout: ExperimentOutput):
    dummy_expout._sync_heatmaps_with_menu_and_regions()


def test_ExperimentOutput__results_summary_EMPTY(dummy_expout: ExperimentOutput):
    assert dummy_expout._results_summary() == dict(obs=[], ovar=[], vc=[], mod=[], mvar=[], per=[])


def test_ExperimentOutput_clean_json_files_EMPTY(dummy_expout: ExperimentOutput):
    modified = dummy_expout.clean_json_files()
    assert len(modified) == 0


@pytest.mark.parametrize("also_coldata", [True, False])
def test_ExperimentOutput_delete_experiment_data(tmp_path: Path, also_coldata: bool):
    json_path = tmp_path / "json"
    coldata_path = tmp_path / "coldata"
    setup = EvalSetup(
        proj_id="proj",
        exp_id="exp",
        coldata_basedir=coldata_path,
        json_basedir=json_path,
    )
    assert setup.path_manager.coldata_basedir == coldata_path
    assert setup.path_manager.json_basedir == json_path
    assert coldata_path.exists()

    out = ExperimentOutput(setup)
    expdir = json_path / "proj" / "exp"
    coldir = coldata_path / "proj" / "exp"
    assert coldir == Path(out.cfg.path_manager.get_coldata_dir())
    assert expdir == Path(out.exp_dir)
    assert coldir.exists()

    out.delete_experiment_data(also_coldata=also_coldata)
    assert coldata_path.exists()
    assert not expdir.exists()
    assert coldir.exists() == (not also_coldata)


@pytest.mark.parametrize(
    "var,val",
    [
        (
            "ang4487aer",
            {
                "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2],
                "colmap": "coolwarm",
            },
        ),
        (
            "concprcpso4",
            {
                "colmap": "coolwarm",
                "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
            },
        ),
    ],
)
def test_ExperimentOutput__get_cmap_info(dummy_expout: ExperimentOutput, var, val):
    assert dummy_expout._get_cmap_info(var) == val


### BELOW ARE TESTS ON ACTUAL OUTPUT THAT DEPEND ON EVALUATION RUNS


@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_ExperimentOutput_delete_experiment_data_CFG1(eval_config: dict):
    cfg = EvalSetup(**eval_config)
    cfg.webdisp_opts.regions_how = "htap"
    cfg.webdisp_opts.add_model_maps = False
    cfg.statistics_opts.add_trends = False
    cfg.time_cfg.add_seasons = False
    proc = ExperimentProcessor(cfg)
    proc.run()
    path = Path(proc.exp_output.exp_dir)
    assert path.exists()
    proc.exp_output.delete_experiment_data()
    assert not path.exists()


@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_Experiment_Output_clean_json_files_CFG1(eval_config: dict):
    cfg = EvalSetup(**eval_config)
    proc = ExperimentProcessor(cfg)
    proc.run()
    modified = proc.exp_output.clean_json_files()
    assert len(modified) == 0


@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_Experiment_Output_clean_json_files_CFG1_INVALIDMOD(eval_config: dict):
    cfg = EvalSetup(**eval_config)
    cfg.model_cfg.add_entry("mod1", cfg.model_cfg.get_entry("TM5-AP3-CTRL"))
    proc = ExperimentProcessor(cfg)
    proc.run()
    cfg.model_cfg.remove_entry("mod1")
    modified = proc.exp_output.clean_json_files()
    assert len(modified) == 13


@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_Experiment_Output_clean_json_files_CFG1_INVALIDOBS(eval_config: dict):
    cfg = EvalSetup(**eval_config)
    cfg.obs_cfg.add_entry("obs1", eval_config["obs_cfg"]["AERONET-Sun"])
    proc = ExperimentProcessor(cfg)
    proc.run()
    cfg.obs_cfg.remove_entry("obs1")
    modified = proc.exp_output.clean_json_files()
    assert len(modified) == 13


@pytest.mark.parametrize(
    "add_names,order,result",
    [
        (["c", "b", "a"], None, ["a", "b", "c"]),
        (["c", "b", "a"], ["c", "b", "a"], ["c", "b", "a"]),
        (["c", "b", "a"], [42], ["a", "b", "c"]),
        (["c", "b", "a"], ["b"], ["b", "a", "c"]),
        (["c", "b", "a"], ["b", "c"], ["b", "c", "a"]),
    ],
)
def test_ExperimentOutput_reorder_experiments(
    dummy_expout: ExperimentOutput, add_names, order, result
):
    path = Path(dummy_expout.experiments_file)

    data = dict().fromkeys(add_names, dict(public=True))
    assert list(data) == add_names

    write_json(data, path, indent=4)
    dummy_expout.reorder_experiments(order)
    new = read_json(path)
    assert list(new) == result
    path.unlink()


def test_ExperimentOutput_reorder_experiments_error(dummy_expout: ExperimentOutput):
    with pytest.raises(ValueError) as e:
        dummy_expout.reorder_experiments("b")
    assert str(e.value) == "need list as input"


@pytest.mark.parametrize("cfg,drop_stats,stats_decimals", [("cfgexp1", ("mab", "R_spearman"), 2)])
def test_Experiment_Output_drop_stats_and_decimals(
    eval_config: dict, drop_stats, stats_decimals: int
):
    eval_config["drop_stats"], eval_config["stats_decimals"] = (
        drop_stats,
        stats_decimals,
    )
    cfg = EvalSetup(**eval_config)
    cfg.model_cfg.add_entry("mod1", cfg.model_cfg.get_entry("TM5-AP3-CTRL"))
    proc = ExperimentProcessor(cfg)
    proc.run()
    path = Path(proc.exp_output.exp_dir)
    files = [f for f in path.iterdir() if f.is_file()]
    assert any(["statistics.json" in f.name for f in files])
    statistics_json = read_json(path / "statistics.json")
    assert all([stat not in statistics_json for stat in drop_stats])
    assert all([statistics_json[stat]["decimals"] == stats_decimals for stat in statistics_json])


@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_Experiment_Output_stats_reorder(eval_config: dict):
    cfg = EvalSetup(**eval_config)
    requested_keys = ("fge", "R_spatial_mean", "mnmb", "nmb")
    cfg.webdisp_opts.stats_order_menu = requested_keys
    proc = ExperimentProcessor(cfg)
    proc.run()
    path = Path(proc.exp_output.exp_dir)
    statistics_json = read_json(path / "statistics.json")

    retrieved_keys = list(statistics_json.keys())

    assert tuple(retrieved_keys[:4]) == requested_keys
