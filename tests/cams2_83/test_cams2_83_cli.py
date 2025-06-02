from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from typer.testing import CliRunner

from pyaerocom.io.cams2_83.models import ModelName, RunType
from pyaerocom.scripts.cams2_83.cli import app, make_config
from pyaerocom.scripts.cams2_83.evaluation import EvalType

runner = CliRunner()


@pytest.mark.usefixtures("fake_ExperimentProcessor", "reset_cachedir")
def test_clearcache(
    monkeypatch,
    fake_cache_path: Path,
    tmp_path: Path,
    caplog,
):
    assert list(fake_cache_path.glob("*.pkl"))

    options = f"forecast week 2024-03-16 2024-03-23 --model-path {tmp_path} --obs-path {tmp_path} --data-path {tmp_path} --coldata-path {tmp_path} --cache {fake_cache_path} --name 'Test'"
    result = runner.invoke(app, options.split())
    assert "Running Statistics" in caplog.text
    assert result.exit_code == 0
    # Check that the cache is cleared
    assert not list(fake_cache_path.glob("*.pkl"))


@pytest.mark.usefixtures("fake_CAMS2_83_Processer", "reset_cachedir")
def test_not_cleared_cache(
    monkeypatch,
    fake_cache_path: Path,
    tmp_path: Path,
    caplog,
):
    assert list(fake_cache_path.glob("*.pkl"))

    options = f"forecast long 2024-03-16 2024-03-23 --model-path {tmp_path} --obs-path {tmp_path} --data-path {tmp_path} --coldata-path {tmp_path} --name 'Test' --medianscores"
    result = runner.invoke(app, options.split())
    assert "Running CAMS2_83 Specific Statistics, cache is not cleared" in caplog.text
    assert result.exit_code == 0
    # Check that the cache is not cleared
    assert list(fake_cache_path.glob("*.pkl"))


def test_eval_dummy(
    tmp_path: Path,
    caplog,
):
    options = f"forecast day 2024-03-16 2024-03-16 --model-path {tmp_path} --obs-path {tmp_path} --data-path {tmp_path} --coldata-path {tmp_path} --name 'Test'"
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0
    assert "Failed to read model variable" in caplog.text


def test_eval_medianscores_dummy(
    tmp_path: Path,
    caplog,
):
    options = f"analysis long 2023-03-01 2024-02-28 --model-path {tmp_path} --obs-path {tmp_path} --data-path {tmp_path} --coldata-path {tmp_path} --name 'Test' --medianscores"
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0
    assert "Running CAMS2_83 Specific Statistics, cache is not cleared" in caplog.text
    assert "Failed to read model variable" in caplog.text


def test_config_options(
    tmp_path: Path,
    caplog,
):
    options = f"forecast week 2024-03-16 2024-03-23 --model-path {tmp_path} --obs-path {tmp_path} --data-path {tmp_path} --coldata-path {tmp_path} --id test_config --fairmode --addmap --addseasons"
    runner.invoke(app, options.split())
    assert "'add_model_maps': True," in caplog.text
    assert "'add_seasons': True," in caplog.text
    assert "'exp_id': 'test_config'," in caplog.text
    assert "'use_fairmode': True," in caplog.text
    assert "'periods': ['20240316-20240323']," in caplog.text


@pytest.mark.parametrize(
    "evaltype,use_fairmode_flag,use_cams2_83_fairmode_flag",
    [
        pytest.param(
            "week",
            True,
            False,
            id="week",
        ),
        pytest.param(
            "season",
            False,
            True,
            id="season",
        ),
        pytest.param(
            "long",
            False,
            True,
            id="long",
        ),
    ],
)
def test_make_config(
    tmp_path: Path,
    evaltype: str,
    use_fairmode_flag: bool,
    use_cams2_83_fairmode_flag: bool,
):
    start_date = date(2025, 3, 1)
    end_date = date(2025, 3, 8)
    leap = 2
    models = [ModelName("emep"), ModelName("chimere")]
    id = "test"
    name = "test"
    description = "test"
    eval_type = EvalType(evaltype)
    run_type = RunType("forecast")

    cfg = make_config(
        start_date=start_date,
        end_date=end_date,
        leap=leap,
        model_path=tmp_path,
        obs_path=tmp_path,
        data_path=tmp_path,
        coldata_path=tmp_path,
        id=id,
        name=name,
        description=description,
        eval_type=eval_type,
        run_type=run_type,
        models=models,
        add_map=True,
        only_map=True,
        add_seasons=True,
        fairmode=True,
        medianscores=True,
    )
    assert cfg["periods"] == ["20250301-20250308"]
    assert cfg["add_model_maps"]
    assert cfg["only_model_maps"]
    assert cfg["use_cams2_83_fairmode"] == use_cams2_83_fairmode_flag
    assert cfg["use_fairmode"] == use_fairmode_flag
