from __future__ import annotations

import pytest

from pyaerocom.access_testdata import AccessTestData

TESTDATADIR = AccessTestData().testdatadir

CHECK_PATH = "modeldata/EMEP_2017"


@pytest.fixture(scope="session")
def path_emep() -> dict[str, str]:
    """dictionary contining EMEP test data"""
    emep_path = TESTDATADIR / CHECK_PATH
    paths = dict(
        daily=emep_path / "Base_day.nc",
        monthly=emep_path / "Base_month.nc",
        yearly=emep_path / "Base_fullrun.nc",
        data_dir=emep_path,
    )

    return {key: str(path) for key, path in paths.items()}
