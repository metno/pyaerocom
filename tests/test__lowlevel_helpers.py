import pytest
from pyaerocom import _lowlevel_helpers as mod
from .conftest import does_not_raise_exception

class Constrainer(mod.ConstrainedContainer):
    def __init__(self):
        self.bla=42
        self.blub='str'
        self.opt = None

class NestedData(mod.NestedContainer):
    def __init__(self):
        self.bla=dict(a=1, b=2)
        self.blub=dict(c=3, d=4)
        self.d=42

def test_Constrainer():
    cont = Constrainer()
    assert cont.bla == 42
    assert cont.blub == 'str'
    assert cont.opt is None

def test_NestedData():
    cont = NestedData()
    assert cont.bla == dict(a=1, b=2)
    assert cont.blub == dict(c=3, d=4)

@pytest.mark.parametrize('kwargs,raises', [
    (dict(), does_not_raise_exception()),
    (dict(bla=400), does_not_raise_exception()),
    (dict(blaaaa=400), pytest.raises(ValueError)),
    (dict(bla=45, opt={}), does_not_raise_exception()),
])
def test_ConstrainedContainer_update(kwargs,raises):
    cont = Constrainer()
    with raises:
        cont.update(**kwargs)
        for key, val in kwargs.items():
            assert cont[key] == val

def test_NestedData_keys_unnested():
    cont = NestedData()
    keys = cont.keys_unnested()
    assert sorted(keys) == ['a', 'b', 'bla', 'blub', 'c', 'd', 'd']

@pytest.mark.parametrize('key,val,raises', [
    ('a', 1, pytest.raises(KeyError)),
    ('d', 42, does_not_raise_exception()),
])
def test_NestedData___getitem__(key, val, raises):
    cont = NestedData()
    with raises:
        assert cont[key] == val

@pytest.mark.parametrize('kwargs,raises', [
    (dict(bla=42), does_not_raise_exception()),
    (dict(a=400), does_not_raise_exception()),
    (dict(abc=400), pytest.raises(AttributeError)),
    (dict(d=400), does_not_raise_exception()),

])
def test_NestedData_update(kwargs,raises):
    cont = NestedData()
    keys = cont.keys_unnested()
    with raises:
        cont.update(**kwargs)
        for key, value in kwargs.items():
            if key in cont.__dict__.keys(): # toplevel entry
                assert cont[key] == value
            for val in cont.values():
                if isinstance(val, dict) and key in val:
                    assert val[key] == value




