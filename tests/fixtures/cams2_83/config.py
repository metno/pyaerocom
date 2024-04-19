from __future__ import annotations

from pathlib import Path

import pytest

from . import cfg_test


@pytest.fixture()
def fake_cache_path(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(
        "pyaerocom.io.cachehandler_ungridded.CacheHandlerUngridded.cache_dir", tmp_path
    )
    cache_file = tmp_path / "tmp.pkl"
    cache_file.write_bytes(b"")
    assert cache_file.exists()
    return tmp_path


@pytest.fixture
def patched_config():
    cfg = cfg_test.CFG
    assert cfg["proj_id"] == "cams2-83"
    return cfg
