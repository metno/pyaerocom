import pytest
import os
import pickle
from unittest import mock
from importlib import metadata

import numpy as np
from typer.testing import CliRunner

# import pyaerocom
from pyaerocom.io.cachehandler_ungridded import CacheHandlerUngridded
from pyaerocom.scripts.cli import main

runner = CliRunner()


@pytest.mark.parametrize("command", ("--version", "-V"))
def test_version(command: str):
    result = runner.invoke(main, command.split())
    assert result.exit_code == 0
    assert "pyaerocom" in result.stdout
    assert metadata.version("pyaerocom") in result.stdout


def test_clearcache(tmp_path):
    # Create a temp pickle file
    tmp_file = tmp_path / "tmp.pkl"
    tmp_array = np.zeros(10)
    with open(tmp_file, "wb") as f:
        pickle.dump(tmp_array, f)

    # Check pytest's tmp_path is non-empty
    assert os.listdir(tmp_path)

    with mock.patch.object(CacheHandlerUngridded, "cache_dir", tmp_path):
        result = runner.invoke(main, ["clearcache"], input="y")
        # Check the clearcahce exited correctly
        assert result.exit_code == 0
        # Check that clearcache actually cleared the cache
        assert not os.listdir(tmp_path)


def test_browse():
    result = runner.invoke(
        main, ["browse", "EARLINET"]
    )  # EARLINET is an arbitrary choice, but it works. Could think of better choice.
    print(result.stdout)
    assert result.exit_code == 0


def test_ppiaccess():
    result = runner.invoke(main, ["ppiaccess"])
    assert result.exit_code == 0
