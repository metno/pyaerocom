import pytest
from pyaerocom import _lowlevel_helpers as mod
from .conftest import does_not_raise_exception

class Constrainer(mod.ConstrainedContainer):
    def __init__(self):
        self.bla=42
        self.blub='str'
        self.opt = None

def test_Constrainer():
    cont = Constrainer()
    assert cont.bla == 42
    assert cont.blub == 'str'
    assert cont.opt is None

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

