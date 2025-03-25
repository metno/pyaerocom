import pytest


from pyaerocom.units.molecular_mass import (
    MolecularMass,
    get_molmass,
    _get_species,
    get_mmr_to_vmr_fac,
)


@pytest.mark.parametrize(
    "val,label,exp_mass,exp_label",
    (
        ("Be", None, 9.0122, "Be"),
        ("O", None, 15.9994, "O"),
        ("N", None, 14.0067, "N"),
        ("H2O", None, 18.01528, "H2O"),
    ),
)
def test_molecular_mass_initialization(
    val: str | float, label: str | float, exp_mass: float, exp_label: str
):
    mass = MolecularMass(val, label=label)

    assert mass.label == exp_label
    assert mass.mass == exp_mass


def test_molecular_mass_error1():
    with pytest.raises(ValueError):
        MolecularMass("C6H12O6")


def test_molecular_mass_error2():
    with pytest.raises(ValueError):
        MolecularMass("Ca(OH)2")


@pytest.mark.parametrize(
    "val,label,exp_repr,exp_str",
    (
        ("H2O", None, "MolecularMass('H2O')", "H2O"),
        (1, None, "MolecularMass('1.0000 u')", "1.0000 u"),
        (1, "test", "MolecularMass('test')", "test"),
    ),
)
def test_molecular_mass___repr___and___str__(
    val: str | float, label: str | None, exp_repr: str, exp_str: str
):
    mass = MolecularMass(val, label=label)
    assert repr(mass) == exp_repr
    assert str(mass) == exp_str


@pytest.mark.parametrize(
    "var_name,species",
    [
        ("air_dry", "air_dry"),
        ("concno2", "no2"),
        ("sconcso2", "so2"),
        ("vmro3", "o3"),
        ("mmro3", "o3"),
        ("wetso4", "so4"),
        ("concNnh4", "nh4"),
        ("concNnh3", "nh3"),
        ("concNtno3", "no3"),
        ("proxydryno2", "no2"),
        ("proxywetno2", "no2"),
    ],
)
def test_get_species(var_name: str, species: str):
    assert _get_species(var_name) == species


@pytest.mark.parametrize(
    "var_name,molmass",
    [
        ("air_dry", 28.9647),
        ("concno2", 46.0055),
        ("sconcso2", 64.0638),
        ("vmro3", 47.9982),
        ("mmro3", 47.9982),
        ("wetso4", 96.0626),
        ("concNnh4", 18.03846),
        ("concNnh3", 17.03052),
        ("concNtno3", 62.0049),
        ("proxydryno2", 46.0055),
    ],
)
def test_get_molmass(var_name: str, molmass: float):
    assert get_molmass(var_name) == molmass


@pytest.mark.parametrize(
    "var_name,result",
    [
        ("mmro3", 0.60343125),
        ("conco3", 0.60343125),
    ],
)
def test_get_mmr_to_vmr_fac(var_name: str, result: float):
    assert get_mmr_to_vmr_fac(var_name) == pytest.approx(result, rel=1e-3)
