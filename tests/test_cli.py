from typer.testing import CliRunner
from pyaerocom.scripts.cli_typer import app
from unittest import mock

# from pyaerocom import __version__

# import pytest

import pyaerocom  # seems extreme. double check example. should be what we are patching


runner = CliRunner()


def test_typer_runner():
    # Test the CLI version arugment
    result = runner.invoke(app, "__version")
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
