from pyaerocom.units.helpers import (
    get_standard_unit,
)


def test_get_standard_unit():
    assert get_standard_unit("ec550aer") == "1/km"
