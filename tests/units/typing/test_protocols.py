from pyaerocom.units import UnitLike
from cf_units import Unit


def test_Unit_is_instance_of_UnitLike():
    u = Unit("meter")
    assert isinstance(u, UnitLike)


def test_Object_is_instance_of_UnitLike():
    obj = object()
    assert not isinstance(obj, UnitLike)
