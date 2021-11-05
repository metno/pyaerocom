import os
from contextlib import nullcontext as does_not_raise_exception

import numpy as np
import pytest
import simplejson

from pyaerocom import _lowlevel_helpers as mod


def test_round_floats():
    fl = float(1.12344567890)
    assert mod.round_floats(fl, precision=5) == 1.12345
    fl_list = [np.float_(2.3456789), np.float32(3.456789012)]
    tmp = mod.round_floats(fl_list, precision=3)
    assert tmp == [2.346, pytest.approx(3.457, 1e-3)]
    fl_tuple = (np.float128(4.567890123), np.float_(5.6789012345))
    tmp = mod.round_floats(fl_tuple, precision=5)
    assert isinstance(tmp, list)
    assert tmp == [pytest.approx(4.56789, 1e-5), 5.67890]
    fl_dict = {"bla": np.float128(0.1234455667), "blubb": int(1), "ha": "test"}
    tmp = mod.round_floats(fl_dict, precision=5)
    assert tmp["bla"] == pytest.approx(0.12345, 1e-5)
    assert tmp["blubb"] == 1
    assert isinstance(tmp["blubb"], int)
    assert isinstance(tmp["ha"], str)


class Constrainer(mod.ConstrainedContainer):
    def __init__(self):
        self.bla = 42
        self.blub = "str"
        self.opt = None


class NestedData(mod.NestedContainer):
    def __init__(self):
        self.bla = dict(a=1, b=2)
        self.blub = dict(c=3, d=4)
        self.d = 42


def test_read_json(tmpdir):
    data = {"bla": 42}
    path = os.path.join(tmpdir, "file.json")
    with open(path, "w") as f:
        simplejson.dump(data, f)
    assert os.path.exists(path)
    reload = mod.read_json(path)
    assert reload == data
    os.remove(path)


@pytest.mark.parametrize("data", [{"bla": 42}, {"bla": 42, "blub": np.nan}])
@pytest.mark.parametrize("kwargs", [dict(), dict(ignore_nan=True, indent=5)])
def test_write_json(tmpdir, data, kwargs):
    path = os.path.join(tmpdir, "file.json")
    mod.write_json(data, path, **kwargs)
    assert os.path.exists(path)
    os.remove(path)


@pytest.mark.parametrize("data,kwargs", [({"bla": 42}, dict(bla=42))])
def test_write_json_error(tmpdir, data, kwargs):
    path = os.path.join(tmpdir, "file.json")
    with pytest.raises(TypeError):
        mod.write_json(data, path, **kwargs)


@pytest.mark.parametrize("fname", ["bla.json"])
def test_check_make_json(tmpdir, fname):
    fp = os.path.join(tmpdir, fname)
    val = mod.check_make_json(fp)
    assert os.path.exists(val)


@pytest.mark.parametrize("fname", ["bla.txt"])
def test_check_make_json_error(tmpdir, fname):
    fp = os.path.join(tmpdir, fname)
    with pytest.raises(ValueError):
        val = mod.check_make_json(fp)


def test_invalid_input_err_str():
    st = mod.invalid_input_err_str("bla", "42", (42, 43))
    assert st == "Invalid input for bla (42), choose from (42, 43)"


@pytest.mark.parametrize("dir,val", [(".", True), ("/bla/blub", False), (42, False)])
def test_check_dir_access(dir, val):
    assert mod.check_dir_access(dir) == val


def test_Constrainer():
    cont = Constrainer()
    assert cont.bla == 42
    assert cont.blub == "str"
    assert cont.opt is None


def test_NestedData():
    cont = NestedData()
    assert cont.bla == dict(a=1, b=2)
    assert cont.blub == dict(c=3, d=4)


@pytest.mark.parametrize("kwargs", [dict(), dict(bla=400), dict(bla=45, opt={})])
def test_ConstrainedContainer_update(kwargs):
    cont = Constrainer()
    cont.update(**kwargs)
    for key, val in kwargs.items():
        assert cont[key] == val


@pytest.mark.parametrize("kwargs", [dict(blaaaa=400)])
def test_ConstrainedContainer_update_error(kwargs):
    cont = Constrainer()
    with pytest.raises(ValueError):
        cont.update(**kwargs)


def test_NestedData_keys_unnested():
    cont = NestedData()
    keys = cont.keys_unnested()
    assert sorted(keys) == ["a", "b", "bla", "blub", "c", "d", "d"]


@pytest.mark.parametrize("key,val", [("d", 42)])
def test_NestedData___getitem__(key, val):
    cont = NestedData()
    assert cont[key] == val


@pytest.mark.parametrize("key,val", [("a", 1)])
def test_NestedData___getitem___error(key, val):
    cont = NestedData()
    with pytest.raises(KeyError):
        assert cont[key] == val


@pytest.mark.parametrize("kwargs", [dict(bla=42), dict(a=400), dict(d=400)])
def test_NestedData_update(kwargs):
    cont = NestedData()
    cont.update(**kwargs)
    for key, value in kwargs.items():
        if key in cont.__dict__:  # toplevel entry
            assert cont[key] == value
        for val in cont.values():
            if isinstance(val, dict) and key in val:
                assert val[key] == value


@pytest.mark.parametrize("kwargs", [dict(abc=400)])
def test_NestedData_update_error(kwargs):
    cont = NestedData()
    with pytest.raises(AttributeError):
        cont.update(**kwargs)


@pytest.mark.parametrize(
    "input,pref_list,output_keys",
    [
        ({"b": 1, "a": 2, "kl": 42}, [], ["a", "b", "kl"]),
        ({"b": 1, "a": 2, "kl": 42}, ["blaaa"], ["a", "b", "kl"]),
        ({"b": 1, "a": 2, "kl": 42}, ["kl"], ["kl", "a", "b"]),
        ({"b": 1, "a": 2, "kl": 42}, ["kl", "b"], ["kl", "b", "a"]),
    ],
)
def test_sort_dict_by_name(input, pref_list, output_keys):
    sorted = mod.sort_dict_by_name(input, pref_list)
    assert list(sorted.keys()) == output_keys
