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
