import json
from importlib import metadata
from pathlib import Path

import pytest
from typer.testing import CliRunner

from pyaerocom.scripts.cli import main

runner = CliRunner()


@pytest.mark.parametrize("command", ("--version", "-V"))
def test_version(command: str):
    result = runner.invoke(main, command.split())
    assert result.exit_code == 0
    assert "pyaerocom" in result.stdout
    assert metadata.version("pyaerocom") in result.stdout


@pytest.fixture()
def fake_cache(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(
        "pyaerocom.io.cachehandler_ungridded.CacheHandlerUngridded.cache_dir", tmp_path
    )
    cache_file = tmp_path / "tmp.pkl"
    cache_file.write_bytes(b"")
    assert cache_file.exists()
    return tmp_path


def test_listcache(fake_cache: Path):
    assert list(fake_cache.glob("*.pkl"))
    result = runner.invoke(main, ["listcache"])
    assert result.exit_code == 0


def test_clearcache(fake_cache: Path):
    assert list(fake_cache.glob("*.pkl"))

    result = runner.invoke(main, ["clearcache"], input="y")
    # Check the clearcahce exited correctly
    assert result.exit_code == 0
    # Check that clearcache actually cleared the cache
    assert not list(fake_cache.glob("*.pkl"))


def test_clearcache_nope(fake_cache: Path):
    assert list(fake_cache.glob("*.pkl"))

    result = runner.invoke(main, ["clearcache"], input="n")
    # Check the clearcahce exited correctly
    assert result.exit_code == 0
    # Check that clearcache still there
    assert list(fake_cache.glob("*.pkl"))


def test_browse():
    result = runner.invoke(
        main, ["browse", "EARLINET"]
    )  # EARLINET is an arbitrary choice, but it works. Could think of better choice.
    print(result.stdout)
    assert result.exit_code == 0


def test_ppiaccess():
    result = runner.invoke(main, ["ppiaccess"])
    assert result.exit_code == 0


def test_init():
    result = runner.invoke(main, ["init"])
    assert result.exit_code == 0


@pytest.fixture()
def config_json(monkeypatch, tmp_path: Path, eval_config: dict) -> Path:
    def do_not_run(self, model_name=None, obs_name=None, var_list=None, update_interface=True):
        assert model_name is None
        assert obs_name is None
        assert var_list is None
        assert update_interface is True

    monkeypatch.setattr("pyaerocom.scripts.cli.ExperimentProcessor.run", do_not_run)

    path = tmp_path / "conf.json"
    path.write_text(json.dumps(eval_config))
    return path


@pytest.mark.parametrize("cfg", ("cfgexp1",))
def test_aeroval(config_json: Path):
    assert config_json.is_file()
    result = runner.invoke(main, ["aeroval", str(config_json)])
    assert result.exit_code == 0
