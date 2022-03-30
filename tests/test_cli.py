from typer.testing import CliRunner
from pyaerocom.scripts.cli_typer import app
from pyaerocom.io.cachehandler_ungridded import CacheHandlerUngridded
from unittest import mock

from pyaerocom import const
from pyaerocom.config import Config

# from pyaerocom import __version__

import pytest

import glob
import os
import logging
import tempfile
import shutil
import pickle
import numpy as np

# import pytest

import pyaerocom  # seems extreme. double check example. should be what we are patching


logger = logging.getLogger(__name__)
runner = CliRunner()


def test_typer_runner():
    # Test the CLI version arugment
    result = runner.invoke(app, "version")
    print()
    print(f"version: {result.stdout}")

    result = runner.invoke(
        app, ["browse", "ppiaccess"]
    )  # LB: Not sure if I want to check clearcache just yet
    print(f"list:\n{result.stdout}")


def test_mock_version():
    with mock.patch.object(
        pyaerocom, "__version__", "0.0.0"
    ):  # adding dummy version here as mocking object
        result = runner.invoke(app, ["version"])
        assert (
            result.stdout.rstrip() == "0.0.0"
        )  # When version() method is called by CLI code, the __version__ attribute isn't the original string, it's the string we replaced with patch.object()


# @pytest.fixture(scope="session")
# def test_create_file(tmp_path):
#     tmp_dir = tmp_path / "sub"
#     tmp_dir.mkdir()
#     tmp_file = tmp_dir / "tmp.pkl"

#     tmp_array = np.zeros(10)
#     with open(tmp_file, "wb") as f:
#         pickle.dump(tmp_array, f)


def test_clearcache(tmp_path):
    # pyaerocom.const.CACHEDIR

    # if not os.listdir(ch.cache_dir):
    #     print("Cache directory is empty")
    # else:
    # tmp_cache_dir = tempfile.TemporaryDirectory(dir=const.CACHEDIR)
    tmp_dir = tmp_path / "sub"
    tmp_dir.mkdir()
    tmp_file = tmp_dir / "tmp.pkl"

    tmp_array = np.zeros(10)
    with open(tmp_file, "wb") as f:
        pickle.dump(tmp_array, f)

    assert tmp_dir

    # conf = Config()
    ch = CacheHandlerUngridded()
    ch.delete_all_cache_files()

    assert not os.listdir(tmp_dir)

    # copy all cahced files into a temporary sub-dir
    # for fp in glob.glob(f"{ch.cache_dir}/*.pkl"):
    # shutil.copy(fp, tmp_cache_dir)
    #    print(fp)
    # assert this tmp sub-dir is nonempty

    # assert os.listdir(tmp_cache_dir.name)

    # for fp in pyaerocom.const.CACHEDIR
    #    os.remove(fp)
    #    logger.info(f"Deleted {fp}")
