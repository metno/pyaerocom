from pyaerocom.units import PyaerocomUnit, UnitProtocol


def test_PyaerocomUnit_isinstance_of_UnitLike():
    u = PyaerocomUnit("meter")
    assert isinstance(u, UnitProtocol)
