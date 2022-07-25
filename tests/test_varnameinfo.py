import pytest

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


@pytest.mark.parametrize(
    "var_name, vert_code",
    [("concpm10", None), ("wetoxn", "Surface"), ("od550aer", "Column")],
)
def test_get_default_vert_code(var_name, vert_code):
    var_name_info = VarNameInfo(var_name)
    try:
        assert var_name_info.get_default_vert_code() == vert_code
    except:
        with pytest.raises(ValueError) as e:
            var_name_info.get_default_vert_code()
        assert e.type is ValueError


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
