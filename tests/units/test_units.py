import pytest
import pandas as pd

from pyaerocom.units import Unit
from pyaerocom.units.exceptions import UnitConversionError
from pyaerocom.units.units import UnitConversionCallbackInfo


@pytest.mark.parametrize(
    "unit,aerocom_var,to_unit,exp_mul",
    (
        ("meter", None, "km", 0.001),
        ("km", None, "meter", 1000),
        ("ug S/m3", "concso2", "ug m-3", 1.997935),
    ),
)
def test_PyaerocomUnit_custom_scaling(
    unit: str, aerocom_var: str | None, to_unit: str, exp_mul: float
):
    u = Unit(unit, aerocom_var=aerocom_var)

    assert u.convert(1, other=to_unit) == pytest.approx(exp_mul)
    assert u.convert(1, other=to_unit, inplace=True) == pytest.approx(exp_mul)


@pytest.mark.parametrize(
    "unit,tstype,output_cf_unit",
    (
        ("mg m-2", "daily", "mg m-2 d-1"),
        ("mg m-2", "yearly", "mg m-2 yr-1"),
        ("mg m-2 d-1", "daily", "mg m-2 d-1"),
    ),
)
def test_PyaerocomUnit_implicit_frequency(unit: str, tstype: str | None, output_cf_unit: str):
    u = Unit(unit, aerocom_var="depdust", ts_type=tstype)
    assert str(u) == output_cf_unit


def test_PyaerocomUnit_conversion_callback():
    u = Unit("mg m-2", aerocom_var="depdust", ts_type="daily")

    callback_ran = False

    def callback(info: UnitConversionCallbackInfo):
        nonlocal callback_ran
        callback_ran = True

        assert info.factor == pytest.approx(1 / 24)
        assert info.from_aerocom_var == "depdust"
        assert info.from_ts_type == "daily"
        assert info.from_cf_unit == "mg m-2 d-1"
        assert info.to_cf_unit == "mg m-2 h-1"

    u.convert(1, "mg m-2 h-1", callback=callback)

    assert callback_ran


def test__unit_conversion_fac_custom_FAIL(monkeypatch):
    MOCK_UCONV_MUL_FACS = pd.DataFrame(
        [
            ["concso4", "ug S/m3", "ug m-3", 1],
            ["concso4", "ug S/m3", "ug m-3", 2],
        ],
        columns=["var_name", "from", "to", "fac"],
    ).set_index(["var_name", "from"])
    monkeypatch.setattr("pyaerocom.units.units.Unit._UCONV_MUL_FACS", MOCK_UCONV_MUL_FACS)

    with pytest.raises(UnitConversionError) as e:
        Unit("ug S/m3", aerocom_var="concso4")
    assert "Could not find unique conversion factor in table" in str(e.value)


def test_origin():
    assert Unit("ug S/m3").origin == "ug S/m3"


@pytest.mark.parametrize(
    "from_unit,to_unit,is_convertible", (("m", "km", True), ("m", "kg", False))
)
def test_is_convertible(from_unit: str, to_unit: str, is_convertible: bool):
    assert Unit(from_unit).is_convertible(to_unit) == is_convertible


def test_is_dimensionless():
    assert not Unit("m").is_dimensionless()
    assert Unit("1").is_dimensionless()


@pytest.mark.parametrize(
    "from_unit,to_unit,is_equal,aerocom_var,ts_type",
    (
        ("meter", "meter", True, None, None),
        ("meter", "cm", False, None, None),
        ("ug S/m3", "1.9979354436301264 ug m-3", True, "concso2", None),
        ("g m-2", "g m-2 d-1", True, "depdust", "daily"),
    ),
)
def test_equality(
    from_unit: str, to_unit: str, is_equal: bool, aerocom_var: str | None, ts_type: str | None
):
    assert (Unit(from_unit, aerocom_var=aerocom_var, ts_type=ts_type) == Unit(to_unit)) == is_equal
    assert (Unit(from_unit, aerocom_var=aerocom_var, ts_type=ts_type) != Unit(to_unit)) != is_equal


@pytest.mark.parametrize(
    "unit,var,out_cf_unit", (("kg N ha-1 yr-1", "drynh3", "383441123690.80505 kg m-2 s-1"),)
)
def test_custom_unit_conversion(unit: str, var: str, out_cf_unit: str):
    assert str(Unit(unit, aerocom_var=var)._cfunit) == out_cf_unit
