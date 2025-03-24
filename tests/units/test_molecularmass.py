import pytest


from pyaerocom.units.molecularmass import MolecularMass


@pytest.mark.parametrize(
    "val,label,exp_mass,exp_label",
    (
        ("Be", None, 9.0122, "Be"),
        ("O", None, 15.9994, "O"),
        ("N", None, 14.0067, "N"),
        ("H2O", None, 18.0152, "H2O"),
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
