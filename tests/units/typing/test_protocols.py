from pyaerocom.units import UnitProtocol
from cf_units import Unit


def test_Unit_is_instance_of_UnitLike():
    u = Unit("meter")
    assert isinstance(u, UnitProtocol)


def test_Object_is_instance_of_UnitLike():
    obj = object()
    assert not isinstance(obj, UnitProtocol)
