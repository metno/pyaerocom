from __future__ import annotations

from pathlib import Path

import pytest

from pyaerocom import const
from pyaerocom._lowlevel_helpers import read_json, write_json
from pyaerocom.aeroval import ExperimentProcessor
from pyaerocom.aeroval.experiment_output import ExperimentOutput, ProjectOutput
from pyaerocom.aeroval.setupclasses import EvalSetup
from tests.conftest import geojson_unavail

BASEDIR_DEFAULT = Path(const.OUTPUTDIR) / "aeroval" / "data"


@pytest.fixture()
def dummy_expout(tmp_path: Path) -> ExperimentOutput:
    """ExperimentOutput instance"""
    setup = EvalSetup(proj_id="proj", exp_id="exp", json_basedir=str(tmp_path))
    return ExperimentOutput(setup)


@pytest.mark.parametrize(
    "proj_id,json_basedir",
    [
        ("bla", None),
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
        pytest.param(
            "bla", "/blablub/blaaaa", FileNotFoundError, "/blablub/blaaaa", id="FileNotFoundError"
        ),
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
    assert path.exists()


def test_ProjectOutput_available_experiments(tmp_path: Path):
    val = ProjectOutput("test", str(tmp_path))
    assert val.available_experiments == []

    write_json({"exp": 42}, val.experiments_file)
    assert val.available_experiments == ["exp"]


def test_ProjectOutput__add_entry_experiments_json(tmp_path: Path):
    val = ProjectOutput("test", str(tmp_path))
    assert val.available_experiments == []

    val._add_entry_experiments_json("test", 42)
    assert val.available_experiments == ["test"]


def test_ProjectOutput__del_entry_experiments_json(tmp_path: Path):
    val = ProjectOutput("test", str(tmp_path))

    exp_id = "test"
    assert exp_id not in val.available_experiments

    val._add_entry_experiments_json(exp_id, {})
    assert exp_id in val.available_experiments

    val._del_entry_experiments_json(exp_id)
    assert exp_id not in val.available_experiments

    # to catch KeyError and make sure it passes
    val._del_entry_experiments_json(exp_id)
    assert exp_id not in val.available_experiments


def test_ExperimentOutput():
    cfg = EvalSetup(proj_id="proj", exp_id="exp")
    val = ExperimentOutput(cfg)
    assert isinstance(val.cfg, EvalSetup)
    assert val.proj_id == cfg["proj_info"]["proj_id"]

    path = Path(val.json_basedir)
    assert path == BASEDIR_DEFAULT
    assert path.exists()


def test_ExperimentOutput_error():
    with pytest.raises(ValueError) as e:
        ExperimentOutput(None)
    assert str(e.value) == "need instance of <class 'pyaerocom.aeroval.setupclasses.EvalSetup'>"


def test_ExperimentOutput_exp_id(dummy_expout: ExperimentOutput):
    assert dummy_expout.exp_id == "exp"


def test_ExperimentOutput_exp_dir(dummy_expout: ExperimentOutput, tmp_path: Path):
    assert Path(dummy_expout.exp_dir) == tmp_path / "proj" / "exp"


def test_ExperimentOutput_regions_file(dummy_expout: ExperimentOutput):
    path = Path(dummy_expout.regions_file)
    assert str(path.parent) == dummy_expout.exp_dir
    assert path.name == "regions.json"


def test_ExperimentOutput_statistics_file(dummy_expout: ExperimentOutput):
    path = Path(dummy_expout.statistics_file)
    assert str(path.parent) == dummy_expout.exp_dir
    assert path.name == "statistics.json"


def test_ExperimentOutput_var_ranges_file(dummy_expout: ExperimentOutput):
    path = Path(dummy_expout.var_ranges_file)
    assert str(path.parent) == dummy_expout.exp_dir
    assert path.name == "ranges.json"


def test_ExperimentOutput_menu_file(dummy_expout: ExperimentOutput):
    path = Path(dummy_expout.menu_file)
    assert str(path.parent) == dummy_expout.exp_dir
    assert path.name == "menu.json"


def test_ExperimentOutput_results_available_False(dummy_expout: ExperimentOutput):
    assert not dummy_expout.results_available


def test_ExperimentOutput_update_menu_EMPTY(dummy_expout: ExperimentOutput):
    dummy_expout.update_menu()
    assert Path(dummy_expout.menu_file).exists()
    assert read_json(dummy_expout.menu_file) == {}


def test_ExperimentOutput_update_interface_EMPTY(dummy_expout: ExperimentOutput):
    dummy_expout.update_interface()


def test_ExperimentOutput_update_heatmap_json_EMPTY(dummy_expout: ExperimentOutput):
    dummy_expout._sync_heatmaps_with_menu_and_regions()


def test_ExperimentOutput__info_from_map_file():
    output = ExperimentOutput._info_from_map_file(
        "EBAS-2010-ac550aer_Surface_ECHAM-HAM-ac550dryaer_2010.json"
    )

    assert output == ("EBAS-2010", "ac550aer", "Surface", "ECHAM-HAM", "ac550dryaer", "2010")


@pytest.mark.parametrize(
    "filename",
    [
        "blaaaa",
        "EBAS-2010-ac550aer_Surface_ECHAM-HAM_ac550dryaer_2010.json",  # has four underscores
    ],
)
def test_ExperimentOutput__info_from_map_file_error(filename: str):
    with pytest.raises(ValueError) as e:
        ExperimentOutput._info_from_map_file(filename)
    assert str(e.value) == (
        f"invalid map filename: {filename}. "
        "Must contain exactly 3 underscores _ to separate obsinfo, vertical, model info, and periods"
    )


def test_ExperimentOutput__results_summary_EMPTY(dummy_expout: ExperimentOutput):
    assert dummy_expout._results_summary() == dict(obs=[], ovar=[], vc=[], mod=[], mvar=[], per=[])


def test_ExperimentOutput_clean_json_files_EMPTY(dummy_expout: ExperimentOutput):
    modified = dummy_expout.clean_json_files()
    assert len(modified) == 0


@pytest.mark.skip(reason="needs revision")
def test_ExperimentOutput__clean_modelmap_files(dummy_expout: ExperimentOutput):
    dummy_expout._clean_modelmap_files()


@pytest.mark.parametrize("also_coldata", [True, False])
def test_ExperimentOutput_delete_experiment_data(tmp_path: Path, also_coldata: bool):
    json_path = tmp_path / "json"
    coldata_path = tmp_path / "coldata"
    setup = EvalSetup(
        proj_id="proj",
        exp_id="exp",
        coldata_basedir=str(coldata_path),
        json_basedir=str(json_path),
    )
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
                "scale": [
                    -0.2,
                    -0.1,
                    0.0,
                    0.1,
                    0.2,
                    0.3,
                    0.4,
                    0.5,
                    0.6,
                    0.7,
                    0.8,
                    0.9,
                    1.0,
                    1.1,
                    1.2,
                    1.3,
                    1.4,
                    1.5,
                    1.6,
                    1.7,
                    1.8,
                    1.9,
                    2.0,
                ],
                "colmap": "coolwarm",
            },
        ),
        (
            "concprcpso4",
            {"colmap": "coolwarm", "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10]},
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


@geojson_unavail
@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_Experiment_Output_clean_json_files_CFG1(eval_config: dict):
    cfg = EvalSetup(**eval_config)
    proc = ExperimentProcessor(cfg)
    proc.run()
    modified = proc.exp_output.clean_json_files()
    assert len(modified) == 0


@geojson_unavail
@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_Experiment_Output_clean_json_files_CFG1_INVALIDMOD(eval_config: dict):
    cfg = EvalSetup(**eval_config)
    cfg.model_cfg["mod1"] = cfg.model_cfg["TM5-AP3-CTRL"]
    proc = ExperimentProcessor(cfg)
    proc.run()
    del cfg.model_cfg["mod1"]
    modified = proc.exp_output.clean_json_files()
    assert len(modified) == 15


@geojson_unavail
@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_Experiment_Output_clean_json_files_CFG1_INVALIDOBS(eval_config: dict):
    cfg = EvalSetup(**eval_config)
    cfg.obs_cfg["obs1"] = cfg.obs_cfg["AERONET-Sun"]
    proc = ExperimentProcessor(cfg)
    proc.run()
    del cfg.obs_cfg["obs1"]
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
