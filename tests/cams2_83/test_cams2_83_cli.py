from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from pyaerocom.scripts.cams2_83.cli import app

runner = CliRunner()


@pytest.fixture()
def fake_config(monkeypatch, patched_config):
    def fake_make_config(*args, **kwargs):
        return patched_config

    monkeypatch.setattr("pyaerocom.scripts.cams2_83.cli.make_config", fake_make_config)


def test_clearcache(
    monkeypatch,
    fake_cache_path: Path,
    tmp_path: Path,
    caplog,
):
    assert list(fake_cache_path.glob("*.pkl"))

    def do_not_run(self, model_name=None, obs_name=None, var_list=None, update_interface=True):
        assert model_name is None
        assert obs_name is None
        assert var_list is None
        assert update_interface is True

    monkeypatch.setattr("pyaerocom.scripts.cams2_83.cli.ExperimentProcessor.run", do_not_run)
    options = f"main forecast week 2024-03-16 2024-03-23 --model-path {tmp_path} --obs-path {tmp_path} --data-path {tmp_path} --coldata-path {tmp_path} --name 'Test'"
    result = runner.invoke(app, options.split())
    assert "Running Statistics" in caplog.text
    assert result.exit_code == 0
    # Check that the cache is cleared
    assert not list(fake_cache_path.glob("*.pkl"))


def test_not_cleared_cache(
    monkeypatch,
    fake_cache_path: Path,
    tmp_path: Path,
    caplog,
):
    assert list(fake_cache_path.glob("*.pkl"))

    def do_not_run(
        self,
        model_name=None,
        obs_name=None,
        var_list=None,
        update_interface=True,
        analysis=False,
    ):
        assert model_name is None
        assert obs_name is None
        assert var_list is None
        assert analysis is False
        assert update_interface is True

    monkeypatch.setattr("pyaerocom.scripts.cams2_83.cli.CAMS2_83_Processer.run", do_not_run)
    options = f"main forecast long 2024-03-16 2024-03-23 --model-path {tmp_path} --obs-path {tmp_path} --data-path {tmp_path} --coldata-path {tmp_path} --name 'Test' --medianscores"
    result = runner.invoke(app, options.split())
    assert "Running CAMS2_83 Specific Statistics, cache is not cleared" in caplog.text
    assert result.exit_code == 0
    # Check that the cache is not cleared
    assert list(fake_cache_path.glob("*.pkl"))


def test_eval_dummy(
    fake_cache_path: Path,
    tmp_path: Path,
    caplog,
):
    assert list(fake_cache_path.glob("*.pkl"))

    options = f"main forecast day 2024-03-16 2024-03-16 --model-path {tmp_path} --obs-path {tmp_path} --data-path {tmp_path} --coldata-path {tmp_path} --name 'Test'"
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0
    assert "Failed to read model variable" in caplog.text


def test_eval_medianscores_dummy(
    fake_cache_path: Path,
    tmp_path: Path,
    caplog,
):
    assert list(fake_cache_path.glob("*.pkl"))

    options = f"main analysis long 2023-03-01 2024-02-28 --model-path {tmp_path} --obs-path {tmp_path} --data-path {tmp_path} --coldata-path {tmp_path} --name 'Test' --medianscores"
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0
    assert "Running CAMS2_83 Specific Statistics, cache is not cleared" in caplog.text
    assert "Failed to read model variable" in caplog.text


def test_eval_mos_dummy(
    fake_cache_path: Path,
    tmp_path: Path,
    caplog,
):
    assert list(fake_cache_path.glob("*.pkl"))

    options = f"mos season 2024-03-01 2024-05-12 --data-path {tmp_path} --coldata-path {tmp_path} --name 'Test'"
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0
    assert "no output available" in caplog.text
