import pytest
import numpy as np
from datetime import timedelta
from pyaerocom.units.datetime import seconds_in_periods


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
