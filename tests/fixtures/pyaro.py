from __future__ import annotations

import pytest
from pathlib import Path
import pandas as pd
import numpy as np

from pyaerocom.io import ReadPyaro, PyaroConfig

def make_csv_test_file(tmp_path: Path) -> Path:
    d = tmp_path / "pyaro"
    file = d / "test_data.csv"


    if not d.exists():
        d.mkdir()
    if file.exists():
        return file



    start = pd.to_datetime("01.01.2015", dayfirst=True)
    end = pd.to_datetime("31.12.2015", dayfirst=True)
    dates = pd.date_range(start, end, freq="D")
    stations = ["NO0002", "GB0881"]
    coords = [(58, 8), (60, -1)]
    species = ["NOx", "SOx"]


    with open(file, "w") as f:
        for s in species:
            for i, station in enumerate(stations):
                for date in dates:
                    f.write(f"{s}, {station}, {coords[i][1]}, {coords[i][0]}, {np.random.normal(10, 5)}, Gg, {date}, {date+pd.Timedelta('1D')} \n")

    return file

@pytest.fixture
def pyaro_test_data_file(tmp_path) -> Path:
    return make_csv_test_file(tmp_path)

@pytest.fixture
def pyaro_testdata(tmp_path) -> ReadPyaro:
    data_id = "csv_timeseries"

    config = PyaroConfig(
        data_id=data_id,
        filename_or_obj_or_url=str(make_csv_test_file(tmp_path)),
        filters={},
        name_map={"SOx": "oxidised_sulphur"},
    )
    rp = ReadPyaro(config=config)

    return rp
