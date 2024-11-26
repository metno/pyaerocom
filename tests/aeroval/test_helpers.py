from __future__ import annotations

import pytest
from pandas import Timestamp

from pyaerocom.aeroval.helpers import (
    _check_statistics_periods,
    _get_min_max_year_periods,
    _period_str_to_timeslice,
    check_if_year,
    make_dummy_model,
)
from pyaerocom.aeroval import EvalSetup


@pytest.mark.parametrize(
    "period,result",
    [
        (["2010-2010", "2005"], ["2010-2010", "2005"]),
        (["20100221-20100912", "20230209"], ["2010/02/21-2010/09/12", "2023/02/09"]),
    ],
)
def test__check_statistics_periods(period: list[str], result: list[str]):
    assert _check_statistics_periods(period) == result


@pytest.mark.parametrize(
    "periods,error",
    [
        pytest.param(
            42,
            "statistics_periods needs to be a list",
            id="not list",
        ),
        pytest.param(
            [42],
            "All periods need to be strings",
            id="not list[str]",
        ),
        pytest.param(
            ["2010-2010-20"],
            "Invalid value for period (2010-2010-20), can be either single years/dates or range of years/dates (e.g. 2000-2010).",
            id="wrong period",
        ),
    ],
)
def test__check_statistics_periods_error(periods: list[str], error: str):
    with pytest.raises(ValueError) as e:
        _check_statistics_periods(periods)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "period,result",
    [
        ("2005", slice("2005", "2005")),
        ("2005-2019", slice("2005", "2019")),
    ],
)
def test__period_str_to_timeslice(period: str, result: slice):
    assert _period_str_to_timeslice(period) == result


def test__period_str_to_timeslice_error():
    with pytest.raises(ValueError) as e:
        _period_str_to_timeslice("2005-2019-2000")
    assert str(e.value) == "2005-2019-2000"


@pytest.mark.parametrize(
    "periods,result",
    [
        (
            ["2005", "2000"],
            (Timestamp("2000-03-16 00:00:00"), Timestamp("2005-03-23 00:00:00")),
        ),
        (
            ["20240316-20240323"],
            (Timestamp("2021-03-16 00:00:00"), Timestamp("2024-03-23 00:00:00")),
        ),
        (
            ["20240316-20240316"],
            (Timestamp("2021-03-16 00:00:00"), Timestamp("2024-03-16 00:00:00")),
        ),
        (
            ["2021-2024", "2021", "2022", "2023", "2024"],
            (Timestamp("2021-01-01 00:00:00"), Timestamp("2024-01-01 00:00:00")),
        ),
        (
            ["2005", "2000", "1999-2021"],
            (Timestamp("1999-01-01 00:00:00"), Timestamp("2021-01-01 00:00:00")),
        ),
    ],
)
def test__get_min_max_year_periods(periods: list[str], result: tuple[int, int]):
    _get_min_max_year_periods(periods) == result


@pytest.mark.parametrize(
    "periods,result",
    [
        (["2005", "2000"], True),
        (["20240316-20240323"], False),
        (["2021-2024", "2021"], True),
    ],
)
def test__check_if_year(periods: list[str], result: bool):
    assert check_if_year(periods) == result


@pytest.mark.parametrize(
    "periods,error",
    [
        (["2005-20000112"], "2005 not on the same format as 20000112"),
        (
            ["1999-2000-2009"],
            "Invalid value for period (1999-2000-2009), can be either single years/dates or range of years/dates (e.g. 2000-2010).",
        ),
        (
            ["2021-2024", "2021", "20231201-20240312"],
            "Found mix of years and dates in ['2021-2024', '2021', '20231201-20240312']",
        ),
    ],
)
def test__check_if_year_error(periods: list[str], error: str):
    with pytest.raises(ValueError) as e:
        check_if_year(periods)
    assert str(e.value) == error


def test__get_min_max_year_periods_error():
    with pytest.raises(ValueError) as e:
        _get_min_max_year_periods(["2005-2004-23", "2000", "1999-2021"])
    assert str(e.value) == "2005-2004-23"


@pytest.mark.parametrize("cfg", ["cfgexp1"])
def test_make_dummy_model(eval_config: dict):
    cfg = EvalSetup(**eval_config)
    assert cfg.obs_cfg.get_entry("AERONET-Sun")
    model_id = make_dummy_model(["AERONET-Sun"], cfg)
    assert model_id == "dummy_model"
