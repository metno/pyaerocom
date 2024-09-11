from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from pyaerocom import GriddedData
from pyaerocom.exceptions import VarNotAvailableError
from pyaerocom.io.readgridded import ReadGridded
from tests.conftest import TEST_RTOL, lustre_unavail
from tests.fixtures.tm5 import TM5_DATA_PATH

path_tm5 = str(TM5_DATA_PATH)


def init_reader():
    return ReadGridded(data_id="ECMWF_CAMS_REAN")


@pytest.fixture(scope="session")
def reader_reanalysis():
    return init_reader()


@pytest.fixture(scope="module")
def reader_tm5():
    return ReadGridded("TM5-met2010_CTRL-TEST")


@pytest.mark.parametrize(
    "input_args,mean_val",
    [
        (dict(var_name="od550aer", ts_type="monthly"), 0.0983),
        (
            dict(
                var_name="od550aer",
                ts_type="monthly",
                constraints={
                    "var_name": "od550aer",
                    "operator": "<",
                    "filter_val": 0.1,
                },
            ),
            0.2054,
        ),
        (
            dict(
                var_name="od550aer",
                ts_type="monthly",
                constraints={
                    "var_name": "od550aer",
                    "operator": ">",
                    "filter_val": 1000,
                },
            ),
            0.0983,
        ),
        (
            dict(
                var_name="od550aer",
                ts_type="monthly",
                constraints=[
                    {"var_name": "od550aer", "operator": "<", "filter_val": 0.1},
                    {"var_name": "od550aer", "operator": ">", "filter_val": 0.11},
                ],
            ),
            0.1047,
        ),
    ],
)
def test_read_var(reader_tm5: ReadGridded, input_args: dict, mean_val: float):
    data = reader_tm5.read_var(**input_args)
    assert data.cube.data.mean() == pytest.approx(mean_val, rel=1e-3)


def test_ReadGridded_class_empty():
    r = ReadGridded()
    assert r.data_id is None
    assert r.data_dir is None
    from pyaerocom.io.aerocom_browser import AerocomBrowser

    assert isinstance(r.browser, AerocomBrowser)
    with pytest.raises(AttributeError):
        r.years_avail
    assert r.vars_filename == []


def test_ReadGridded_data_dir(reader_tm5: ReadGridded):
    assert reader_tm5.data_dir == path_tm5
    assert reader_tm5._vars_2d == ["abs550aer", "od550aer"]
    assert reader_tm5._vars_3d == []


def test_ReadGridded_ts_types():
    r = ReadGridded(data_dir=path_tm5)
    assert sorted(r.ts_types) == ["daily", "monthly"]


def test_ReadGridded_read_var(reader_tm5: ReadGridded):
    r = reader_tm5
    data = r.read_var("od550aer")
    assert data.mean() == pytest.approx(0.0960723)
    with pytest.raises(VarNotAvailableError):
        r.read_var("wetso4")
    from pyaerocom.io.aux_read_cubes import add_cubes

    gridded = r.read_var("new_var", aux_vars=["abs550aer", "od550aer"], aux_fun=add_cubes)
    assert gridded.var_name == "new_var"
    assert isinstance(gridded, GriddedData)

    gridded_single_point = gridded.sel(
        latitude=0.0,
        longitude=0.0,
    )
    with pytest.raises(ValueError):
        gridded_single_point.latitude.guess_bounds()
    with pytest.raises(ValueError):
        gridded_single_point.longitude.guess_bounds()


@pytest.mark.parametrize(
    "experiments",
    [
        (["exp1"]),
        (["exp1", "exp2"]),
    ],
)
def test_ReadGridded_experiments(tmp_path: Path, experiments: list[str]):
    for exp in experiments:
        path = tmp_path / f"aerocom3_TM5-met2010_{exp}-CTRL2019_abs550aer_Column_2010_daily.nc"
        path.write_text("")

    reader = ReadGridded(data_dir=str(tmp_path))
    assert reader.experiments == experiments


@pytest.mark.parametrize(
    "vars,expected",
    [
        (["mmro3", "rho"], ["conco3", "mmro3", "rho"]),
        (["od440aer", "od870aer"], ["ang4487aer", "od440aer", "od870aer"]),
    ],
)
def test_ReadGridded_aux(tmp_path: Path, vars, expected):
    for var in vars:
        path = tmp_path / f"aerocom3_TM5-met2010_AP3-CTRL2019_{var}_Column_2010_daily.nc"
        path.write_text("")

    reader = ReadGridded(data_dir=str(tmp_path))
    for var in expected:
        assert reader.has_var(var)  # calling has_var
    assert sorted(reader.vars_provided) == sorted(expected)
    # assert r.has_var('conco3')


@pytest.mark.parametrize(
    "options,expected",
    [
        (dict(prefer_longer=True, flex_ts_type=True, ts_type="monthly"), "daily"),
        (dict(prefer_longer=False, flex_ts_type=True, ts_type="monthly"), "monthly"),
        (dict(prefer_longer=True, flex_ts_type=False, ts_type="monthly"), "monthly"),
        (dict(prefer_longer=False, flex_ts_type=False, ts_type="monthly"), "monthly"),
        (dict(prefer_longer=True, flex_ts_type=True), "daily"),
        (dict(prefer_longer=False, flex_ts_type=True), "daily"),
    ],
)
def test_ReadGridded_prefer_longer(options, expected):
    r = ReadGridded(data_dir=path_tm5)
    gridded = r.read_var("abs550aer", **options)
    assert gridded.ts_type == expected


def test_filter_query(reader_tm5: ReadGridded):
    reader_tm5.filter_query("abs550aer", ts_type="yearly", flex_ts_type=True)


@pytest.mark.parametrize(
    "years, expected",
    [
        ([2003, 2005], [2003, 2005]),
    ],
)
def test_ReadGridded_years_avail(tmp_path: Path, years, expected):
    for year in years:
        path = tmp_path / f"aerocom3_TM5-met2010_AP3-CTRL2019_od550aer_Column_{year}_daily.nc"
        path.write_text("")

    reader = ReadGridded(data_dir=str(tmp_path))
    assert sorted(reader.years_avail) == expected


def test_ReadGridded_get_var_info_from_files(reader_tm5: ReadGridded):
    info = reader_tm5.get_var_info_from_files()
    assert isinstance(info, dict)
    assert sorted(info) == ["abs550aer", "od550aer"]


# Lustre tests
START = "1-1-2003"
STOP = "31-12-2007"


@lustre_unavail
def test_file_info(reader_reanalysis: ReadGridded):
    assert isinstance(reader_reanalysis.file_info, pd.DataFrame)
    assert len(reader_reanalysis.file_info.columns) == 12


@lustre_unavail
def test_years_available(reader_reanalysis: ReadGridded):
    # reanalysis years in database will increase every year, only checking for some years in tests
    years = set(range(2003, 2024))
    assert set(reader_reanalysis.years_avail) >= years


@lustre_unavail
def test_data_dir(reader_reanalysis: ReadGridded):
    assert reader_reanalysis.data_dir.endswith(
        "aerocom/aerocom-users-database/ECMWF/ECMWF_CAMS_REAN/renamed"
    )


@lustre_unavail
def test_read_var_lustre(reader_reanalysis: ReadGridded):
    d = reader_reanalysis.read_var(var_name="od550aer", ts_type="daily", start=START, stop=STOP)

    assert isinstance(d, GriddedData)
    assert d.var_name == "od550aer"
    assert sum(d.shape) == 1826 + 161 + 320
    assert d.start == np.datetime64("2003-01-01T00:00:00.000000")
    assert d.stop == np.datetime64("2007-12-31T23:59:59.999999")
    assert d.longitude.points[[0, -1]] == pytest.approx([-180.0, 178.875], rel=TEST_RTOL)
    assert d.latitude.points[[0, -1]] == pytest.approx([90.0, -90.0], rel=TEST_RTOL)


@lustre_unavail
def test_prefer_longer(reader_reanalysis: ReadGridded):
    daily = reader_reanalysis.read_var(
        "od550aer", ts_type="monthly", flex_ts_type=True, prefer_longer=True
    )
    assert daily.ts_type == "daily"


@lustre_unavail
def test_read_vars(reader_reanalysis: ReadGridded):
    data = reader_reanalysis.read(
        ["od440aer", "od550aer", "od865aer"], ts_type="daily", start=START, stop=STOP
    )
    assert len(data) == 3
    assert all(d.shape == (1826, 161, 320) for d in data)


def test_read_climatology_file(reader_tm5: ReadGridded):
    data = reader_tm5.read_var("abs550aer", start=9999)
    assert isinstance(data, GriddedData)
