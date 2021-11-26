import pandas as pd
import pytest
from numpy.testing import assert_allclose

from pyaerocom.exceptions import UnitConversionError
from pyaerocom.units_helpers import (
    _check_unit_endswith_freq,
    _unit_conversion_fac_custom,
    _unit_conversion_fac_si,
    convert_unit,
    get_unit_conversion_fac,
)


@pytest.mark.parametrize(
    "unit,val",
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
def test__check_unit_endswith_freq(unit, val):
    assert _check_unit_endswith_freq(unit) == val


@pytest.mark.parametrize("from_unit,to_unit,val", [("m-1", "1/Mm", 1e6), ("ug m-3", "ug/m3", 1)])
def test__unit_conversion_fac_si(from_unit, to_unit, val):
    assert _unit_conversion_fac_si(from_unit, to_unit) == val


@pytest.mark.parametrize(
    "var_name,from_unit,to_unit,val,",
    [
        ("concno3", "ug N m-3", "ug m-3", 4.426717),
        ("concso2", "ug S/m3", "ug m-3", 1.9979),
        ("concso4", "ug S/m3", "ug m-3", 2.9958),
        ("concbc", "ug C/m3", "ug m-3", 1),
        ("concoa", "ug C/m3", "ug m-3", 1),
        ("concoc", "ug C/m3", "ug m-3", 1),
        ("wetso4", "kg S/ha", "kg m-2", 0.0003),
        ("concso4pr", "mg S/L", "g m-3", 2.995821),
    ],
)
def test__unit_conversion_fac_custom(var_name, from_unit, to_unit, val):
    to, num = _unit_conversion_fac_custom(var_name, from_unit)
    assert to == to_unit
    assert_allclose(num, val, rtol=1e-2)


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

    with pytest.raises(UnitConversionError):
        _unit_conversion_fac_custom("concso4", "ug S/m3")


@pytest.mark.parametrize(
    "from_unit,to_unit,var_name,val",
    [
        ("ug m-3", "ug/m3", None, 1),
        ("ug m-3", "ug/m3", "concso2", 1),
        ("mg m-3", "ug m-3", "concso2", 1e3),
        ("ug S/m3", "mg m-3", "concso2", 1.9979e-3),
    ],
)
def test_convert_unit(from_unit, to_unit, var_name, val):
    result = convert_unit(1, from_unit, to_unit, var_name)
    assert_allclose(result, val, rtol=1e-2)


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
def test_get_unit_conversion_fac(from_unit, to_unit, var_name, ts_type, result):
    val = get_unit_conversion_fac(from_unit, to_unit, var_name, ts_type)
    assert_allclose(val, result, rtol=1e-3)


@pytest.mark.parametrize(
    "from_unit,to_unit,var_name",
    [
        ("kg m-2", "mm", "pr"),
        ("kg m-2", "mm", "od550aer"),
        ("1", "ug", None),
    ],
)
def test_get_unit_conversion_fac_error(from_unit, to_unit, var_name):
    with pytest.raises(UnitConversionError) as e:
        get_unit_conversion_fac(from_unit, to_unit, var_name)
    assert str(e.value) == f"failed to convert unit from {from_unit} to {to_unit}"
