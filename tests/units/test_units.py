import pytest

from pyaerocom.units import Unit
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
    u1 = Unit(unit, aerocom_var=aerocom_var)
    u2 = Unit(to_unit, aerocom_var=aerocom_var)

    assert u1.convert(1, other=u2) == pytest.approx(exp_mul)
    assert u1.convert(1, other=u2, inplace=True) == pytest.approx(exp_mul)


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


def test_origin():
    assert Unit("ug S/m3").origin == "ug S/m3"


@pytest.mark.parametrize(
    "from_unit,to_unit,is_convertible",
    (
        ("m", "km", True),
        ("m", "kg", False),
        (Unit("mg S"), Unit("mg"), False),
        (Unit("mg S", species="SO4"), Unit("mg", species="SO4"), True),
        (Unit("mg S", aerocom_var="concso2"), Unit("mg", aerocom_var="concso2"), True),
        (Unit("mg", species="SO4"), Unit("mg S", species="SO4"), True),
        (Unit("mg", aerocom_var="concso2"), Unit("mg S", aerocom_var="concso2"), True),
        (Unit("mg S", species="SO2"), Unit("mg N", species="SO2"), False),
        (Unit("ug S/m3", aerocom_var="concso4t"), Unit("ug m-3", aerocom_var="concso4t"), False),
    ),
)
def test_is_convertible(from_unit: str | Unit, to_unit: str | Unit, is_convertible: bool):
    if isinstance(from_unit, str):
        from_unit = Unit(from_unit)
    if isinstance(to_unit, str):
        to_unit = Unit(to_unit)

    assert from_unit.is_convertible(to_unit) == is_convertible


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
    "unit,nominator,denominator",
    (("mg", "mg", ""), ("mg N / m2 d", "mg N", "m2 d"), ("mg N m-2 d-1", "mg N", "m-2 d-1")),
)
def test_nominator_denominator(unit: str, nominator: str, denominator: str):
    u = Unit(unit)
    assert u._origin_nominator == nominator
    assert u._origin_denominator == denominator


@pytest.mark.parametrize(
    "unit,species,var,exp_element,exp_species",
    (
        ("mg", None, None, None, None),
        ("mg N", None, None, None, None),
        ("mg N", "NH3", None, "N", "NH3"),
        ("mg N", None, "drynh3", "N", "NH3"),
    ),
)
def test_species_and_element_detection(
    unit: str,
    species: str | None,
    var: str | None,
    exp_element: str | None,
    exp_species: str | None,
):
    u = Unit(unit, species=species, aerocom_var=var)
    assert u._element == exp_element
    assert u._species == exp_species


@pytest.mark.parametrize(
    "from_unit,to_unit,species,conversion_fac",
    (
        (
            "kg N",
            "kg",
            "NH3",
            17.03052 / 14.0067,  # Molecular mass ratio of NH3/N
        ),
        ("mg N", "kg", "NH3", (17.03052 / 14.0067) / 1_000_000),
        ("mg N s-1", "kg s-1", "NH3", (17.03052 / 14.0067) / 1_000_000),
        ("mg N s-1", "kg h-1", "NH3", 3_600 * (17.03052 / 14.0067) / (1_000_000)),
    ),
)
def test_unit_conversion(from_unit: str, to_unit: str, species: str, conversion_fac: float):
    u = Unit(from_unit, species=species)
    fac = u.convert(1, to_unit, species=species)
    assert fac == pytest.approx(conversion_fac)


@pytest.mark.parametrize(
    "from_unit,to_unit,aerocom_var,conversion_fac",
    (("g N", "mg N", "blah", 1000), ("mg S l-1", "kg S m-3", "blah", 10**-3)),
)
def test_unit_conversion2(from_unit: str, to_unit: str, aerocom_var: str, conversion_fac: float):
    u = Unit(from_unit, aerocom_var=aerocom_var)
    fac = u.convert(1, to_unit, aerocom_var=aerocom_var)
    assert fac == pytest.approx(conversion_fac)


@pytest.mark.parametrize(
    "from_unit,to_unit",
    (
        (  # No known reference species to do conversion.
            Unit("kg S"),
            Unit("kg"),
        ),
        (  # Element don't match
            Unit(
                "kg N",
            ),
            Unit("kg S"),
        ),
    ),
)
def test_unit_conversion_fails(from_unit: Unit, to_unit: Unit):
    with pytest.raises(Exception):
        from_unit.convert(1, to_unit)


def test_units_species_concso4c():
    u = Unit("mg S / m3", aerocom_var="concso4c")

    assert u._species == "SO4"
    assert u.convert(1, Unit("mg m-3", aerocom_var="concso4c")) == pytest.approx(2.99, abs=0.01)
