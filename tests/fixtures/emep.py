from __future__ import annotations

import pytest

from .data_access import TESTDATADIR

DATA_PATH = "modeldata/EMEP_2017"
EMEP_DATA_PATH = TESTDATADIR / DATA_PATH


@pytest.fixture(scope="session")
def path_emep() -> dict[str, str]:
    """dictionary contining EMEP test data"""
    paths = dict(
        daily=EMEP_DATA_PATH / "Base_day.nc",
        monthly=EMEP_DATA_PATH / "Base_month.nc",
        yearly=EMEP_DATA_PATH / "Base_fullrun.nc",
        data_dir=EMEP_DATA_PATH,
    )

    return {key: str(path) for key, path in paths.items()}
