from __future__ import annotations

import pandas as pd
import pytest

from pyaerocom.exceptions import UnitConversionError
from pyaerocom.units_helpers import (
    _check_unit_endswith_freq,
    _unit_conversion_fac_custom,
    _unit_conversion_fac_si,
    convert_unit,
    get_unit_conversion_fac,
)


@pytest.mark.parametrize(
    "unit,result",
    [
        ("ug min-1", True),
        ("ug/min", True),
        ("ug", False),
        ("ug m-1", False),
        ("ug m-2", False),
        ("kg m-2/yr", True),
        ("kg m-2/month", True),
        ("kg m-2/week", True),
        ("kg m-2 month-1", True),
        ("mm", False),
        ("mg d-1", True),
    ],
)
def test__check_unit_endswith_freq(unit: str, result: bool):
    assert _check_unit_endswith_freq(unit) == result


@pytest.mark.parametrize(
    "from_unit,to_unit,result",
    [
        ("m-1", "1/Mm", 1e6),
        ("ug m-3", "ug/m3", 1),
    ],
)
def test__unit_conversion_fac_si(from_unit: str, to_unit: str, result: float):
    assert _unit_conversion_fac_si(from_unit, to_unit) == result


@pytest.mark.parametrize(
    "var_name,from_unit,to_unit,result,",
    [
        # ("SO4ugSm3", "ug/m3", "ug S m-3", 0.333798316),
        # ("concno3", "ug N m-3", "ug m-3", 4.426717),
        ("concso2", "ug S/m3", "ug m-3", 1.9979),
        # ("concso4", "ug S/m3", "ug m-3", 2.9958),
        ("concbc", "ug C/m3", "ug m-3", 1),
        ("concoa", "ug C/m3", "ug m-3", 1),
        ("concoc", "ug C/m3", "ug m-3", 1),
        ("concpm25", "ug m-3", "1", 1),
        ("concpm10", "ug m-3", "1", 1),
        ("wetso4", "kg S/ha", "kg m-2", 0.0003),
        ("concso4pr", "mg S/L", "g m-3", 2.995821),
    ],
)
def test__unit_conversion_fac_custom(var_name: str, from_unit: str, to_unit: str, result: float):
    converted_unit, conversion_fac = _unit_conversion_fac_custom(var_name, from_unit)
    assert converted_unit == to_unit
    assert conversion_fac == pytest.approx(result, rel=1e-2)


def test__unit_conversion_fac_custom_error():
    with pytest.raises(UnitConversionError) as e:
        _unit_conversion_fac_custom("concNno3", "ug N m-3")
    assert str(e.value).startswith("Failed to convert unit ug N/m3 (variable concNno3).")


def test__unit_conversion_fac_custom_FAIL(monkeypatch):
    MOCK_UCONV_MUL_FACS = pd.DataFrame(
        [
            ["concso4", "ug S/m3", "ug m-3", 1],
            ["concso4", "ug S/m3", "ug m-3", 2],
        ],
        columns=["var_name", "from", "to", "fac"],
    ).set_index(["var_name", "from"])
    monkeypatch.setattr("pyaerocom.units_helpers.UCONV_MUL_FACS", MOCK_UCONV_MUL_FACS)

    with pytest.raises(UnitConversionError) as e:
        _unit_conversion_fac_custom("concso4", "ug S/m3")
    assert "Could not find unique conversion factor in table" in str(e.value)


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
