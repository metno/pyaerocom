import os
import pickle
from unittest import mock

import numpy as np
from typer.testing import CliRunner

import pyaerocom
from pyaerocom.io.cachehandler_ungridded import CacheHandlerUngridded
from pyaerocom.scripts.cli import app

runner = CliRunner()


def test_mock_version():
    with mock.patch.object(
        pyaerocom, "__version__", "0.0.0"
    ):  # adding dummy version here as mocking object
        result = runner.invoke(app, ["version"])
        assert (
            result.stdout.rstrip() == "0.0.0"
        )  # When version() method is called by CLI code, the __version__ attribute isn't the original string, it's the string we replaced with patch.object()


def test_clearcache(tmp_path):
    # Create a temp pickle file
    tmp_file = tmp_path / "tmp.pkl"
    tmp_array = np.zeros(10)
    with open(tmp_file, "wb") as f:
        pickle.dump(tmp_array, f)

    # Check pytest's tmp_path is non-empty
    assert os.listdir(tmp_path)

    with mock.patch.object(CacheHandlerUngridded, "cache_dir", tmp_path):
        result = runner.invoke(app, ["clearcache"], input="y")
        # Check the clearcahce exited correctly
        assert result.exit_code == 0
        # Check that clearcache actually cleared the cache
        assert not os.listdir(tmp_path)


def test_browse():
    result = runner.invoke(
        app, ["browse", "EARLINET"]
    )  # EARLINET is an arbitrary choice, but it works. Could think of better choice.
    print(result.stdout)
    assert result.exit_code == 0


def test_ppiaccess():
    result = runner.invoke(app, ["ppiaccess"])
    assert result.exit_code == 0
