import pytest

from pyaerocom.molmasses import get_mmr_to_vmr_fac, get_molmass, get_species


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
    assert get_species(var_name) == species


@pytest.mark.parametrize(
    "var_name,molmass",
    [
        ("air_dry", 28.9647),
        ("concno2", 46.0055),
        ("sconcso2", 64.066),
        ("vmro3", 48),
        ("mmro3", 48),
        ("wetso4", 96.06),
        ("concNnh4", 18.039),
        ("concNnh3", 17.031),
        ("concNtno3", 62.0045),
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
