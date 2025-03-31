from __future__ import annotations

import pytest

from pyaerocom.units import UnitConversionError
from pyaerocom.units.units_helpers import (
    convert_unit,
    get_unit_conversion_fac,
)


@pytest.mark.parametrize(
    "from_unit,to_unit,var_name,result",
    [
        ("ug m-3", "ug/m3", None, 1),
        ("ug m-3", "ug/m3", "concso2", 1),
        ("mg m-3", "ug m-3", "concso2", 1e3),
        ("ug S/m3", "mg m-3", "concso2", 1.9979e-3),
    ],
)
def test_convert_unit(from_unit: str, to_unit: str, var_name: str, result: float):
    converted = convert_unit(1, from_unit, to_unit, var_name)
    assert converted == pytest.approx(result, rel=1e-2)


@pytest.mark.parametrize(
    "from_unit,to_unit,var_name,ts_type,result",
    [
        ("kg (2m)-2", "kg/m2", None, None, 0.25),
        ("mm", "mm d-1", "prmm", "daily", 1),
        ("mm", "mm d-1", "prmm", "hourly", 24),
        ("mg m-2", "ug m-2 d-1", "wetoxs", "hourly", 24e3),
        ("mg m-2", "mg m-2 d-1", "wetoxs", "hourly", 24),
        ("mg m-2", "mg m-2/d", "wetoxs", "daily", 1),
        ("mg m-2", "mg m-2 d-1", "wetoxs", "daily", 1),
        ("mg m-2", "ug mm-2", None, None, 1e-3),
        ("mg", "ug", None, None, 1000),
        ("1", "1", None, None, 1),
    ],
)
def test_get_unit_conversion_fac(
    from_unit: str, to_unit: str, var_name: str | None, ts_type: str | None, result: float
):
    conversion_fac = get_unit_conversion_fac(from_unit, to_unit, var_name, ts_type)
    assert conversion_fac == pytest.approx(result, rel=1e-3)


@pytest.mark.parametrize(
    "from_unit,to_unit,var_name",
    [
        ("kg m-2", "mm", "pr"),
        ("kg m-2", "mm", "od550aer"),
        ("1", "ug", None),
    ],
)
def test_get_unit_conversion_fac_error(from_unit: str, to_unit: str, var_name: str | None):
    with pytest.raises(UnitConversionError) as e:
        get_unit_conversion_fac(from_unit, to_unit, var_name)
    assert str(e.value) == f"failed to convert unit from {from_unit} to {to_unit}"
