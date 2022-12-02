from pathlib import Path

import pytest

from pyaerocom import const
from pyaerocom.plugins.harp.reader import ReadHARP

LUSTRE_PATH = Path("/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/MEP/download")

STATION_NAMES = ("1478A", "2706A", "3377A")


@pytest.fixture()
def reader() -> ReadHARP:
    if not LUSTRE_PATH.is_dir():  # pragma: no cover
        pytest.fail(f"needs {LUSTRE_PATH}")
    return ReadHARP(data_dir=str(LUSTRE_PATH))


def test_DATASET_NAME(reader: ReadHARP):
    assert reader.DATASET_NAME == "HARP"


def test_DEFAULT_VARS(reader: ReadHARP):
    default = {"concco", "concno2", "conco3", "concpm10", "concpm25", "concso2"}
    assert set(reader.DEFAULT_VARS) >= default


def test_FOUND_FILES(reader: ReadHARP):
    assert reader.FOUND_FILES, "no stations files found"
    assert len(reader.FOUND_FILES) >= 167482, "found less files than expected"


def test_STATIONS(reader: ReadHARP):
    assert reader.STATIONS, f"no stations found"
    assert all(reader.STATIONS.values()), f"stations without files"
    assert reader.STATIONS.keys() >= set(STATION_NAMES), f"missing known station names"


def test_PROVIDES_VARIABLES(reader: ReadHARP):
    default = {"concco", "concno2", "conco3", "concpm10", "concpm25", "concso2"}
    aux = {"vmro3", "vmro3max", "vmrno2"}
    return set(reader.PROVIDES_VARIABLES) >= (default | aux)  # union


@pytest.mark.xfail(not const.has_access_lustre, reason=f"needs access to {LUSTRE_PATH}")
def test_read(reader: ReadHARP):
    data = reader.read(vars_to_retrieve=["vmro3max"])
