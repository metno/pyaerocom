from datetime import date

import numpy as np
import pytest

from pyaerocom.trends_helpers import (
    _end_season,
    _find_area,
    _get_season_from_months,
    _init_trends_result_dict,
    _mid_season,
    _start_season,
    _start_stop_period,
    _years_from_periodstr,
)


def test__init_trends_result_dict():
    result = _init_trends_result_dict(2022)
    assert isinstance(result, dict)
    assert len(result.keys()) == 14


def test__get_season_from_months_error():
    with pytest.raises(ValueError):
        _get_season_from_months(months="cat")


@pytest.mark.parametrize(
    "season, year",
    [
        ("spring", 2022),
        ("summer", 2022),
        ("autumn", 2022),
        ("winter", 2022),
        ("all", 2022),
    ],
)
def test__mid_season(season, year):
    res = _mid_season(season, year)
    assert isinstance(res, np.datetime64)
    assert "15" in str(res)


def test__mid_season_error():
    with pytest.raises(ValueError):
        _mid_season(seas="cat", yr=2022)


@pytest.mark.parametrize(
    "season, year",
    [
        ("spring", 2022),
        ("summer", 2022),
        ("autumn", 2022),
        ("winter", 2022),
        ("all", 2022),
    ],
)
def test__start_season(season, year):
    res = _start_season(season, year)
    assert isinstance(res, str)
    assert "01" in res


def test__start_season_error():
    with pytest.raises(ValueError):
        _start_season("cat", 2022)


@pytest.mark.parametrize(
    "season, year",
    [
        ("spring", 2022),
        ("summer", 2022),
        ("autumn", 2022),
        ("winter", 2022),
        ("all", 2022),
    ],
)
def test__end_season(season, year):
    res = _end_season(season, year)
    assert isinstance(res, str)
    assert "01" in res


def test__end_season_error():
    with pytest.raises(ValueError):
        _end_season(seas="cat", yr=2022)


@pytest.mark.parametrize(
    "lat, lon, area",
    [
        (30.033333, 31.233334, "NAFRICA"),
        (48.8566, 2.35, "EUROPE"),
        (22.572645, 88.363892, "INDIA"),
    ],
)
def test__find_area(lat, lon, area):
    res = _find_area(lat, lon)
    assert area == res


def test__years_from_periodstr():
    period = "1990-2010"
    res = _years_from_periodstr(period)
    assert len(res) == 2
    assert all(isinstance(item, int) for item in res)


def test__start_stop_period():
    period = "1990-2010"
    res = _start_stop_period(period)
    assert len(res) == 2
    assert all(isinstance(item, date) for item in res)
