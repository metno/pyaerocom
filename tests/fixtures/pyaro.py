from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from pyaerocom.io import PyaroConfig, ReadPyaro


def make_csv_test_file(tmp_path: Path) -> Path:
    d = tmp_path / "pyaro"
    file = d / "test_data.csv"

    if not d.exists():
        d.mkdir()
    if file.exists():
        return file

    start = pd.to_datetime("01.01.2010", dayfirst=True)
    end = pd.to_datetime("31.12.2010", dayfirst=True)
    dates = pd.date_range(start, end, freq="D")
    stations = ["NO0002", "GB0881"]
    countries = ["NO", "GB"]
    coords = [(58, 8), (60, -1)]
    species = ["NOx", "SOx", "AOD", "NO", "PM10"]
    area_type = ["Rural", "Urban"]

    with open(file, "w") as f:
        for s in species:
            for i, station in enumerate(stations):
                for j, date in enumerate(dates):
                    delta_t = ["1h", "3D", "2D", "2h"][
                        j % 4
                    ]  # Rotates over the freqs in a deterministic fashion
                    if s == "AOD":
                        unit = 1
                    else:
                        unit = "Gg m-3" if s != "NO" else "ng m-3"
                    f.write(
                        f"{s}, {station}, {coords[i][1]}, {coords[i][0]}, {np.random.normal(10, 5)}, {unit}, {date}, {date + pd.Timedelta(delta_t)},{countries[i]},{area_type[i]} \n"
                    )

    return file


def testconfig(tmp_path: Path) -> tuple[PyaroConfig, PyaroConfig]:
    reader_id = "csv_timeseries"

    config1 = PyaroConfig(
        name="test",
        reader_id=reader_id,
        filename_or_obj_or_url=str(make_csv_test_file(tmp_path)),
        filters={},
        name_map={"SOx": "concso4", "AOD": "od550aer"},
    )

    config2 = PyaroConfig(
        name="test2",
        reader_id=reader_id,
        filename_or_obj_or_url=str(make_csv_test_file(tmp_path)),
        filters={},
        name_map={"SOx": "concso4", "AOD": "od550aer"},
    )
    return [config1, config2]


def testconfig_kwargs(tmp_path: Path) -> PyaroConfig:
    reader_id = "csv_timeseries"
    columns = {
        "variable": 0,
        "station": 1,
        "longitude": 2,
        "latitude": 3,
        "value": 4,
        "units": 5,
        "start_time": 6,
        "end_time": 7,
        "altitude": "0",
        "country": 8,
        "standard_deviation": "NaN",
        "flag": "0",
        "area_classification": 9,
    }

    config = PyaroConfig(
        name="test",
        reader_id=reader_id,
        filename_or_obj_or_url=str(make_csv_test_file(tmp_path)),
        filters={},
        name_map={"SOx": "concso4"},
        columns=columns,
    )

    return config


@pytest.fixture
def pyaro_kwargs() -> dict:
    columns = {
        "variable": 0,
        "station": 1,
        "longitude": 2,
        "latitude": 3,
        "value": 4,
        "units": 5,
        "start_time": 6,
        "end_time": 7,
        "altitude": "0",
        "country": 8,
        "standard_deviation": "NaN",
        "flag": "0",
        "area_classification": 9,
    }
    return columns


@pytest.fixture
def pyaro_test_data_file(tmp_path) -> Path:
    return make_csv_test_file(tmp_path)


@pytest.fixture
def pyaro_testconfig(tmp_path) -> PyaroConfig:
    return testconfig(tmp_path=tmp_path)


@pytest.fixture
def pyaro_testconfig_kwargs(tmp_path) -> PyaroConfig:
    return testconfig_kwargs(tmp_path=tmp_path)


@pytest.fixture
def pyaro_testdata(tmp_path) -> ReadPyaro:
    config = testconfig(tmp_path=tmp_path)[0]
    rp = ReadPyaro(config=config)

    return rp


@pytest.fixture
def pyaro_testdata_kwargs(tmp_path) -> ReadPyaro:
    config = testconfig_kwargs(tmp_path=tmp_path)
    rp = ReadPyaro(config=config)

    return rp
