import pytest

from pyaerocom.exceptions import VariableDefinitionError
from pyaerocom.varnameinfo import VarNameInfo


@pytest.mark.parametrize(
    "var_name, contains_numbers, contains_wavelength_nm, is_wavelength_dependent",
    [
        ("concpm10", True, True, False),
        ("wetoxn", False, False, False),
        ("od550gt1aer", True, True, True),
    ],
)
def test_varnameinfo(var_name, contains_numbers, contains_wavelength_nm, is_wavelength_dependent):
    var_name_info = VarNameInfo(var_name)
    assert isinstance(var_name_info, VarNameInfo)
    assert var_name_info.contains_numbers == contains_numbers
    assert var_name_info.contains_wavelength_nm == contains_wavelength_nm
    assert var_name_info.is_wavelength_dependent == is_wavelength_dependent
    assert isinstance(str(var_name_info), str)


@pytest.mark.parametrize(
    "var_name, vert_code",
    [("wetoxn", "Surface"), ("od550aer", "Column")],
)
def test_get_default_vert_code(var_name, vert_code):
    var_name_info = VarNameInfo(var_name)
    assert var_name_info.get_default_vert_code() == vert_code


def test_get_default_vert_code_error():
    var_name_info = VarNameInfo("concpm10")
    with pytest.raises(ValueError):
        var_name_info.get_default_vert_code()


@pytest.mark.parametrize(
    "var_name, contains_numbers",
    [
        ("concpm10", True),
        ("od550aer", True),
        ("emitolu", False),
    ],
)
def test_contains_numbers(var_name, contains_numbers):
    var_name_info = VarNameInfo(var_name)
    assert var_name_info.contains_numbers == contains_numbers


@pytest.mark.parametrize(
    "var_name, wavelength",
    [
        ("od550aer", 550),
        ("bsc532aer", 532),
    ],
)
def test_wavelength_nm(var_name, wavelength):
    var_name_info = VarNameInfo(var_name)
    assert var_name_info.wavelength_nm == wavelength


@pytest.mark.parametrize(
    "var_name",
    [
        ("concpm10"),
        ("wetoxs"),
    ],
)
def test_wavelength_nm_errors(var_name):
    var_name_info = VarNameInfo(var_name)
    with pytest.raises(VariableDefinitionError):
        var_name_info.wavelength_nm()


@pytest.mark.parametrize(
    "to_wavelength",
    [
        (350),
        (440),
    ],
)
def test_translate_to_wavelength(to_wavelength):
    od = VarNameInfo("od550aer")
    new_od = od.translate_to_wavelength(to_wavelength)
    assert new_od.wavelength_nm == to_wavelength
