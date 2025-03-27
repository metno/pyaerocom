import pytest


from pyaerocom.units import PyaerocomUnit


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
    u = PyaerocomUnit(unit, aerocom_var=aerocom_var)

    assert u.convert(1, other=to_unit) == pytest.approx(exp_mul)


@pytest.mark.parametrize(
    "unit,tstype,output_cf_unit",
    (
        ("mg m-2", "daily", "mg m-2 d-1"),
        ("mg m-2", "yearly", "mg m-2 yr-1"),
        ("mg m-2 d-1", "daily", "mg m-2 d-1"),
    ),
)
def test_PyaerocomUnit_implicit_frequency(unit: str, tstype: str | None, output_cf_unit: str):
    u = PyaerocomUnit(unit, aerocom_var="depdust", ts_type=tstype)
    assert str(u) == output_cf_unit
