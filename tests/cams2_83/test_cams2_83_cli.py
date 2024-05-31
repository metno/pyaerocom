from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from pyaerocom.scripts.cams2_83.cli import app

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
