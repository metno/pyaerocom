from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from pyaerocom.scripts.cams2_83.cli import app

runner = CliRunner()


def test_clearcache(monkeypatch, fake_obs: List, fake_cache_path: Path, fake_basedir_path: Path, patched_full_config):
    assert list(fake_cache_path.glob("*.pkl"))

    def fake_make_config(*args, **kwargs):
        return patched_full_config

    monkeypatch.setattr("pyaerocom.scripts.cams2_83.cli.make_config", fake_make_config)

    def do_not_run(self, model_name=None, obs_name=None, var_list=None, update_interface=True):
        assert model_name is None
        assert obs_name is None
        assert var_list is None
        assert update_interface is True

    monkeypatch.setattr("pyaerocom.scripts.cams2_83.cli.ExperimentProcessor.run", do_not_run)
    options = (
        f"2024-03-16 2024-03-23 --data-path {fake_basedir_path} --coldata-path {fake_basedir_path} --name 'Test'"
    )
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0
    # Check that clearcache actually cleared the cache
    assert not list(fake_cache_path.glob("*.pkl"))
