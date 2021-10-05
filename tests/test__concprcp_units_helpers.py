import pytest

import pyaerocom._concprcp_units_helpers
from .conftest import does_not_raise_exception
import pyaerocom._concprcp_units_helpers as mod

@pytest.mark.parametrize('unit,ts_type,result,raises', [
('mg m-2/h', 'hourly', 'mg m-2 h-1', does_not_raise_exception()),
('mg N m-2', 'hourly', 'mg N m-2 h-1', does_not_raise_exception()),
('mg N m-2', 'daily', 'mg N m-2 d-1', does_not_raise_exception()),

])

def test_translate_rate_units_implicit(unit,ts_type,result,raises):
    with raises:
        val = pyaerocom._concprcp_units_helpers.translate_rate_units_implicit(unit, ts_type)
        assert val == result