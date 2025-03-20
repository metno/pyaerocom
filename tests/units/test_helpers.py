from datetime import timedelta
import numpy as np
import pytest
from pyaerocom.units.helpers import (
    get_lowest_resolution,
    seconds_in_periods,
    sort_ts_types,
    get_standard_unit,
)


@pytest.mark.parametrize(
    "input,expected",
    (
        pytest.param(
            ["monthly", "weekly", "daily", "hourly"], ["hourly", "daily", "weekly", "monthly"]
        ),
        pytest.param(
            ["3daily", "4daily", "6daily", "13daily"], ["3daily", "4daily", "6daily", "13daily"]
        ),
    ),
)
def test_sort_tstypes(input, expected):
    assert sort_ts_types(input) == expected


def test_get_standard_unit():
    assert get_standard_unit("ec550aer") == "1/km"


def test_get_lowest_resolution():
    assert get_lowest_resolution("3hourly", "hourly", "monthly", "yearly") == "yearly"


@pytest.mark.parametrize(
    "date,ts_type,days",
    [
        pytest.param("2000-02-18", "yearly", 366, id="leap year"),
        pytest.param("2001-02-18", "yearly", 365, id="lon leap year"),
        pytest.param("2000-02-18", "monthly", 29, id="February leap year"),
        pytest.param("2001-02-18", "monthly", 28, id="February non leap year"),
        pytest.param("2001-02-18", "daily", 1, id="one day"),
    ],
)
def test_seconds_in_periods(date, ts_type, days):
    seconds = timedelta(days=days) / timedelta(seconds=1)
    assert seconds_in_periods(np.datetime64(date), ts_type) == seconds
