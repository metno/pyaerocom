from __future__ import annotations

from pathlib import Path

import pytest

from . import cfg_test, cfg_test_full


@pytest.fixture()
def fake_model_path(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp("modeldata")


@pytest.fixture()
def fake_obs_path(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp("obsdata")


@pytest.fixture()
def fake_basedir_path(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp("basedir")


@pytest.fixture()
def fake_cache_path(monkeypatch, tmp_path: Path):
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


@pytest.fixture
def patched_full_config(fake_obs_path: Path, fake_model_path: Path, fake_basedir_path: Path):
    cfg = cfg_test_full.CFG
    assert cfg["proj_id"] == "cams2-83"
    # cfg["obs_cfg"]["EEA"]["read_opts_ungridded"]["files"] = fake_obs
    # cfg["colocation_opts"]["basedir_coldata"] = fake_basedir_path
    # cfg.model_cfg.EMEP.model_data_dir = fake_model_path
    # cfg.path_manager.coldata_basedir = fake_basedir_path
    # cfg.path_manager.json_basedir = fake_basedir_path
    return cfg
