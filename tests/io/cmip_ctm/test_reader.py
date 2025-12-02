from __future__ import annotations

import os.path
from pathlib import Path

import pandas as pd
import pytest

from pyaerocom import GriddedData

# from pyaerocom import config
from pyaerocom.io.cmip_ctm.reader import ReadCmipCtm

TEST_MODEL_NAME = "MPI-ESM-1-2-HAM"
PYAEROCOM_UNIT_TEST_DATA_DIR = (
    "/lustre/storeB/project/aerocom/aerocom-users-database/HYway/NorESM2-LM-C/transient2010s/"
)
PYAEROCOM_UNIT_TEST_DATA_MODEL = "NorESM2-LM-C"
VARS_TO_TEST = ["concso4", "vmro3"]


@pytest.fixture()
def reader() -> ReadCmipCtm:
    """empty CMIP reader"""
    return ReadCmipCtm()


@pytest.fixture()
def data_dir(path_cmip_ci: str) -> str:
    """path to CMIP test data"""
    return path_cmip_ci


@pytest.fixture()
def data_dir_pya(path_cmip_ci: str) -> str:
    """path to CMIP pyaerocom unit testing test data"""
    return PYAEROCOM_UNIT_TEST_DATA_DIR


def test_ReadCmipCtm_read_var_pyaerocom_unit(data_dir_pya: str):
    # testing actual model reading with providing start and stop dates
    # data is in a single multiyear file
    if not os.path.exists(data_dir_pya):
        assert True
    else:
        start_time = pd.Timestamp("2013-01-01")
        stop_time = pd.Timestamp("2014-01-01")
        for var_name in VARS_TO_TEST:
            reader = ReadCmipCtm(data_dir=data_dir_pya, data_id=PYAEROCOM_UNIT_TEST_DATA_MODEL)
            ts_type = "monthly"
            data = reader.read_var(var_name, ts_type, start=start_time, stop=stop_time)
            assert data.shape == (12, 96, 144)


def test_ReadCmipCtm__init__(data_dir: str):
    reader = ReadCmipCtm(data_id=TEST_MODEL_NAME, data_dir=data_dir)
    assert getattr(reader, "data_id") == TEST_MODEL_NAME
    assert getattr(reader, "data_dir") == data_dir


def test_ReadCmipCtm__get_file_list(data_dir: str):
    reader = ReadCmipCtm(TEST_MODEL_NAME, data_dir)
    # files = reader.get_file_list()
    files = reader._files
    assert len(files) > 0


def test_ReadCmipCtm__get_file_info(data_dir: str):
    reader = ReadCmipCtm(TEST_MODEL_NAME, data_dir)
    files = reader._files
    file_info = reader._file_info
    assert len(file_info) > 0
    assert file_info[files[0]]["tstype"] == "monthly"
    assert list(file_info[files[0]]["years"]) == [2012, 2013, 2014]


def test_ReadCmipCtm__init___error():
    data_dir = "not_a_real_path"
    with pytest.raises(FileNotFoundError) as e:
        ReadCmipCtm(None, data_dir)
    assert str(e.value) == data_dir


def test_ReadCmipCtm_data_dir(data_dir: str):
    reader = ReadCmipCtm(data_dir=data_dir, data_id=TEST_MODEL_NAME)
    assert Path(reader.data_dir) == Path(data_dir)


def test_ReadCmipCtm_vars(data_dir: str):
    reader = ReadCmipCtm(data_dir=data_dir, data_id=TEST_MODEL_NAME)
    assert sorted(reader.vars_provided) == ["od550aer", "od550lt1aer"]


def test_ReadCmipCtm_read_var(data_dir: str):
    reader = ReadCmipCtm(data_dir=data_dir, data_id=TEST_MODEL_NAME)
    var_name = "od550aer"
    ts_type = "monthly"
    data = reader.read_var(var_name, ts_type)
    assert isinstance(data, GriddedData)
    if ts_type is not None:
        assert data.ts_type == ts_type
    assert data.ts_type is not None
    assert data.metadata["data_id"] is not None
    assert data.metadata["data_id"] == TEST_MODEL_NAME
    assert data.shape == (25, 96, 192)
    # assert data.ts_type == reader._ts_type


def test_ReadCmipCtm_read_var_start_stop_single_file(data_dir: str):
    # testing actual model reading with providing start and stop dates
    # data is in a single multiyear file
    start_time = pd.Timestamp("2013-01-01")
    stop_time = pd.Timestamp("2014-01-01")
    reader = ReadCmipCtm(data_dir=data_dir, data_id=TEST_MODEL_NAME)
    var_name = "od550aer"
    ts_type = "monthly"
    data = reader.read_var(var_name, ts_type, start=start_time, stop=stop_time)
    assert data.shape == (12, 96, 192)


def test_ReadCmipCtm_read_var_start_stop_multi_file(data_dir: str):
    # testing actual model reading with providing start and stop dates
    # data is in several files
    start_time = "2013-06-01"
    stop_time = "2014-06-01"
    reader = ReadCmipCtm(data_dir=data_dir, data_id=TEST_MODEL_NAME)
    var_name = "od550lt1aer"
    ts_type = "monthly"
    data = reader.read_var(var_name, ts_type, start=start_time, stop=stop_time)
    assert data.shape == (12, 96, 192)
