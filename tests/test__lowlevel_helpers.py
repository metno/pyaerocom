import numpy as np
import os
import pytest
import simplejson
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

def test_read_json(tmpdir):
    data = {'bla' : 42}
    path = os.path.join(tmpdir, 'file.json')
    with open(path, 'w') as f:
        simplejson.dump(data, f)
    assert os.path.exists(path)
    reload = mod.read_json(path)
    assert reload == data
    os.remove(path)

@pytest.mark.parametrize('data,kwargs,raises', [
    ({'bla': 42}, dict(), does_not_raise_exception()),
    ({'bla': 42, 'blub' : np.nan}, dict(), does_not_raise_exception()),
    ({'bla': 42, 'blub' : np.nan}, dict(ignore_nan=True, indent=5), does_not_raise_exception()),
    ({'bla': 42}, dict(bla=42), pytest.raises(TypeError)),
])
def test_write_json(tmpdir,data,kwargs,raises):
    path = os.path.join(tmpdir, 'file.json')
    with raises:
        mod.write_json(data,path,**kwargs)
        assert os.path.exists(path)
        os.remove(path)

@pytest.mark.parametrize('fname,raises', [
    ('bla.txt', pytest.raises(ValueError)),
    ('bla.json', does_not_raise_exception()),
])
def test_check_make_json(tmpdir,fname,raises):
    fp = os.path.join(tmpdir,fname)
    with raises:
        val = mod.check_make_json(fp)
        assert os.path.exists(val)


def test_invalid_input_err_str():
    st = mod.invalid_input_err_str('bla', '42', (42,43))
    assert st == 'Invalid input for bla (42), choose from (42, 43)'

@pytest.mark.parametrize('dir,val', [
    ('.', True), ('/bla/blub', False), (42, False)
])
def test_check_dir_access(dir,val):
    assert mod.check_dir_access(dir) == val

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

@pytest.mark.parametrize('input,pref_list,output_keys,raises', [
    ({'b':1, 'a':2, 'kl':42}, [], ['a', 'b', 'kl'],does_not_raise_exception()),
    ({'b':1, 'a':2, 'kl':42}, ['blaaa'], ['a', 'b', 'kl'],does_not_raise_exception()),
    ({'b':1, 'a':2, 'kl':42}, ['kl'], ['kl', 'a', 'b'],does_not_raise_exception()),
    ({'b':1, 'a':2, 'kl':42}, ['kl', 'b'], ['kl', 'b', 'a'],does_not_raise_exception()),
])
def test_sort_dict_by_name(input,pref_list,output_keys,raises):
    with raises:
        sorted = mod.sort_dict_by_name(input,pref_list)
        assert list(sorted.keys()) == output_keys






