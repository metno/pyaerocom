from __future__ import annotations

from pathlib import Path

import pytest

from pyaerocom import const
from pyaerocom.plugins.icos.reader import ReadICOS
from tests.conftest import lustre_unavail

try:
    ICOS_PATH = Path(const.OBSLOCS_UNGRIDDED[const.ICOS_NAME])
except KeyError:
    pytest.mark.skip(reason=f"ICOS path not initialised due to non existence in CI")
    

VARS_DEFAULT = {"vmrco2"}

@lustre_unavail
@pytest.fixture(scope="module")
def reader() -> ReadMEP:
    return ReadMEP(data_dir=str(ICOS_PATH))


@lustre_unavail
@pytest.fixture()
def station_files(station: str) -> list[Path]:
    files = sorted(ICOS_PATH.rglob(f"icos-co2-nrt-{station}-.*-.*-.*.nc"))
    assert files, f"no files for {station}"
    return files
