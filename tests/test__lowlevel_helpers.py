import json
from pathlib import Path

import numpy as np
import pytest

from pyaerocom._lowlevel_helpers import (
    ConstrainedContainer,
    NestedContainer,
    check_dir_access,
    check_make_json,
    invalid_input_err_str,
    read_json,
    round_floats,
    sort_dict_by_name,
    str_underline,
    write_json,
)


@pytest.mark.parametrize(
    "raw,precision,rounded",
    [
        pytest.param(
            float(1.12344567890),
            5,
            1.12345,
            id="single float",
        ),
        pytest.param(
            [np.float_(2.3456789), np.float32(3.456789012)],
            3,
            [2.346, pytest.approx(3.457, 1e-3)],
            id="np.float list",
        ),
        pytest.param(
            (np.float128(4.567890123), np.float_(5.6789012345)),
            5,
            [pytest.approx(4.56789, 1e-5), 5.67890],
            id="np.float tuple",
        ),
        pytest.param(
            dict(bla=np.float128(0.1234455667), blubb=int(1), ha="test"),
            5,
            dict(bla=pytest.approx(0.12345, 1e-5), blubb=1, ha="test"),
            id="mixed dict",
        ),
    ],
)
def test_round_floats(raw, precision: int, rounded):
    _rounded = round_floats(raw, precision=precision)
    if type(raw) in (list, tuple):
        assert type(_rounded) == list
    if type(raw) == dict:
        assert type(_rounded) == dict
    assert _rounded == rounded


@pytest.mark.parametrize("title", ["", "Bla", "Hello"])
@pytest.mark.parametrize("indent", [0, 4, 10])
def test_str_underline(title: str, indent: int):
    lines = str_underline(title, indent).split("\n")
    assert len(lines) == 2
    assert len(lines[0]) == len(lines[1]) == len(title) + indent
    assert lines[0].endswith(title)
    assert lines[1].endswith("-" * len(title))
    assert lines[0][:indent] == lines[1][:indent] == " " * indent


class Constrainer(ConstrainedContainer):
    def __init__(self):
        self.bla = 42
        self.blub = "str"
        self.opt = None


class NestedData(NestedContainer):
    def __init__(self):
        self.bla = dict(a=1, b=2)
        self.blub = dict(c=3, d=4)
        self.d = 42


@pytest.fixture()
def json_path(tmp_path: Path) -> Path:
    path = tmp_path / "file.json"
    assert not path.exists()
    return path


def test_read_json(json_path: Path):
    data = {"bla": 42}
    json_path.write_text(json.dumps(data))
    assert json_path.exists()
    assert read_json(json_path) == data


@pytest.mark.parametrize("data", [{"bla": 42}, {"bla": 42, "blub": np.nan}])
@pytest.mark.parametrize("kwargs", [dict(), dict(ignore_nan=True, indent=5)])
def test_write_json(json_path: Path, data: dict, kwargs: dict):
    write_json(data, json_path, **kwargs)
    assert json_path.exists()


def test_write_json_error(json_path: Path):
    with pytest.raises(TypeError) as e:
        write_json({"bla": 42}, json_path, bla=42)
    assert str(e.value).endswith("unexpected keyword argument 'bla'")


def test_check_make_json(json_path: Path):
    json = check_make_json(json_path)
    assert Path(json).exists()


def test_check_make_json_error(tmp_path: Path):
    path = tmp_path / "bla.txt"
    assert not path.exists()
    with pytest.raises(ValueError) as e:
        check_make_json(path)
    assert str(e.value) == "Input filepath must end with .json"


def test_invalid_input_err_str():
    st = invalid_input_err_str("bla", "42", (42, 43))
    assert st == "Invalid input for bla (42), choose from (42, 43)"


@pytest.mark.parametrize("dir,val", [(".", True), ("/bla/blub", False), (42, False)])
def test_check_dir_access(dir, val):
    assert check_dir_access(dir) == val


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


def test_NestedData___getitem__():
    cont = NestedData()
    assert cont["d"] == 42


def test_NestedData___getitem___error():
    cont = NestedData()
    with pytest.raises(KeyError):
        cont["a"]


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


def test_NestedData_update_error():
    cont = NestedData()
    with pytest.raises(AttributeError) as e:
        cont.update(abc=400)
    assert str(e.value) == "invalid key abc"


@pytest.mark.parametrize("input", [{"b": 1, "a": 2, "kl": 42}])
@pytest.mark.parametrize(
    "pref_list,output_keys",
    [
        ([], ["a", "b", "kl"]),
        (["blaaa"], ["a", "b", "kl"]),
        (["kl"], ["kl", "a", "b"]),
        (["kl", "b"], ["kl", "b", "a"]),
    ],
)
def test_sort_dict_by_name(input, pref_list, output_keys):
    sorted = sort_dict_by_name(input, pref_list)
    assert list(sorted.keys()) == output_keys
