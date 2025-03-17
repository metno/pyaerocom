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
