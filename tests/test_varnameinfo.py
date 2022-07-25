import pytest

from pyaerocom.varnameinfo import VarNameInfo


@pytest.mark.parametrize(
    "var_name, contains_numbers, contains_wavelength_nm, is_wavelength_dependent",
    [
        ("concpm10", True, True, False),
        ("wetoxn", False, False, False),
    ],
)
def test_varnameinfo(var_name, contains_numbers, contains_wavelength_nm, is_wavelength_dependent):
    var_name_info = VarNameInfo(var_name)
    assert isinstance(var_name_info, VarNameInfo)
    assert var_name_info.contains_numbers == contains_numbers
    assert var_name_info.contains_wavelength_nm == contains_wavelength_nm
    assert var_name_info.is_wavelength_dependent == is_wavelength_dependent
