import pytest

from pyaerocom.helpers import make_dummy_cube_latlon


def test_convert_units():
    cube = make_dummy_cube_latlon()
    assert (cube.data == 1).all()

    cube.units = "kg h-1"
    cube.convert_units("kg s-1")
    assert cube.data.mean() == pytest.approx(1 / 3600)


# =============================================================================
#
# cube = pya.helpers.make_dummy_cube_latlon()
# cube.var_name = 'wetso4'
# cube.units = 'mg S m-2 h-1'
#
# data = pya.GriddedData(cube)
#
# print(data)
# =============================================================================
