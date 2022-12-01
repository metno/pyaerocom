from pathlib import Path

import pytest

from pyaerocom import const
from pyaerocom.plugins.harp.reader import ReadHARP

FILE_DIR = "/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/MEP/download"


@pytest.fixture()
def reader() -> ReadHARP:
    if not Path(FILE_DIR).is_dir():  # pragma: no cover
        pytest.fail(f"needs {FILE_DIR}")
    return ReadHARP(data_dir=FILE_DIR)


@pytest.mark.xfail(not const.has_access_lustre, reason=f"needs access to {FILE_DIR}")
def test_read(reader: ReadHARP):
    data = reader.read(vars_to_retrieve=["vmro3max"])
