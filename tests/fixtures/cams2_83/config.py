from __future__ import annotations

import os
from pathlib import Path

import pytest

from pyaerocom import const

from . import cfg_test, cfg_test_mos


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
def reset_cachedir():
    cache = const.CACHEDIR
    yield
    const.CACHEDIR = cache


@pytest.fixture
def patched_config():
    cfg = cfg_test.CFG
    assert cfg["proj_id"] == "cams2-83"
    return cfg


@pytest.fixture
def patched_config_mos():
    cfg = cfg_test_mos.CFG
    assert cfg["exp_id"] == "mos-colocated-data"
    return cfg


@pytest.fixture(scope="session")
def dataDir():
    """Path to the folder with test data, intended to be used as the --coldata-path argument in the mos evaluation tests.
    This means it has to contain the expected colocated data at the subpath /cams2_83/{exp-id}"""
    testDir = os.path.dirname(__file__)
    theDir = os.path.join(testDir, "data")
    return theDir


@pytest.fixture
def fake_CAMS2_83_Processer(monkeypatch):
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

    monkeypatch.setattr("pyaerocom.scripts.cams2_83.evaluation.CAMS2_83_Processer.run", do_not_run)


@pytest.fixture
def fake_ExperimentProcessor(monkeypatch):
    def do_not_run(self, model_name=None, obs_name=None, var_list=None, update_interface=True):
        assert model_name is None
        assert obs_name is None
        assert var_list is None
        assert update_interface is True

    monkeypatch.setattr(
        "pyaerocom.scripts.cams2_83.evaluation.ExperimentProcessor.run", do_not_run
    )
