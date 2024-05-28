from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from pyaerocom.scripts.cams2_83.cli_mos import app

runner = CliRunner()


@pytest.fixture()
def fake_config(monkeypatch, patched_config):
    def fake_make_config(*args, **kwargs):
        return patched_config

    monkeypatch.setattr("pyaerocom.scripts.cams2_83.cli_mos.make_config_mos", fake_make_config)


def test_eval_mos_dummy(
    fake_cache_path: Path,
    tmp_path: Path,
    caplog,
):
    assert list(fake_cache_path.glob("*.pkl"))

    options = f"season 2024-03-01 2024-05-12 --data-path {tmp_path} --coldata-path {tmp_path} --name 'Test'"
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0
    assert "no output available" in caplog.text
