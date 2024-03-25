from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from pyaerocom.scripts.cams2_83.cli import app
from tests.cams2_83 import cfg_test, cfg_test_full

runner = CliRunner()


@pytest.fixture(scope="session")
def fake_model_path(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp("modeldata")


@pytest.fixture(scope="session")
def fake_obs_path(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp("obsdata")


@pytest.fixture()
def fake_cache(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(
        "pyaerocom.io.cachehandler_ungridded.CacheHandlerUngridded.cache_dir", tmp_path
    )
    cache_file = tmp_path / "tmp.pkl"
    cache_file.write_bytes(b"")
    assert cache_file.exists()
    return tmp_path


@pytest.fixture()
def fake_obs(fake_obs_path: Path):
    file1 = fake_obs_path / "fakeobs1.csv"
    file1.write_bytes(b"")
    assert file1.exists()
    file2 = fake_obs_path / "fakeobs2.csv"
    file2.write_bytes(b"")
    files = [file1, file2]
    return files


def test_clearcache(monkeypatch, fake_obs: List, tmp_path: Path, fake_cache: Path):
    assert list(fake_cache.glob("*.pkl"))

    def patched_config(*args, **kwargs):
        cfg = cfg_test_full.CFG
        cfg["obs_cfg"]["EEA"]["read_opts_ungridded"]["files"] = fake_obs
        cfg["colocation_opts"]["basedir_coldata"] = tmp_path
        cfg["model_cfg"]["EMEP"]["model_data_dir"] = fake_model_path
        return cfg

    monkeypatch.setattr("pyaerocom.scripts.cams2_83.cli.make_config", patched_config)

    def do_not_run(self, model_name=None, obs_name=None, var_list=None, update_interface=True):
        assert model_name is None
        assert obs_name is None
        assert var_list is None
        assert update_interface is True

    monkeypatch.setattr("pyaerocom.scripts.cams2_83.cli.ExperimentProcessor.run", do_not_run)
    options = (
        f"2024-03-16 2024-03-23 --data-path {tmp_path} --coldata-path {tmp_path} --name 'Test'"
    )
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0
    # Check that clearcache actually cleared the cache
    assert not list(fake_cache.glob("*.pkl"))
