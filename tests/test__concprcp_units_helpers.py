import pytest

import pyaerocom._concprcp_units_helpers


@pytest.mark.parametrize(
    "unit,ts_type,result",
    [
        pytest.param("mg m-2/h", "hourly", "mg m-2 h-1", id="mg/m2/h"),
        pytest.param("mg N m-2", "hourly", "mg N m-2 h-1", id="mg(N)/m2/h"),
        pytest.param("mg N m-2", "daily", "mg N m-2 d-1", id="mg(N)/m2/day"),
    ],
)
def test_translate_rate_units_implicit(unit, ts_type, result):
    val = pyaerocom._concprcp_units_helpers.translate_rate_units_implicit(unit, ts_type)
    assert val == result
