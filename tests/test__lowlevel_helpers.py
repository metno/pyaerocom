import pytest

from pyaerocom._lowlevel_helpers import (
    check_dir_access,
    invalid_input_err_str,
    sort_dict_by_name,
    str_underline,
    BrowseDict,
)


@pytest.mark.parametrize("title", ["", "Bla", "Hello"])
@pytest.mark.parametrize("indent", [0, 4, 10])
def test_str_underline(title: str, indent: int):
    lines = str_underline(title, indent).split("\n")
    assert len(lines) == 2
    assert len(lines[0]) == len(lines[1]) == len(title) + indent
    assert lines[0].endswith(title)
    assert lines[1].endswith("-" * len(title))
    assert lines[0][:indent] == lines[1][:indent] == " " * indent


def test_invalid_input_err_str():
    st = invalid_input_err_str("bla", "42", (42, 43))
    assert st == "Invalid input for bla (42), choose from (42, 43)"


@pytest.mark.parametrize("dir,val", [(".", True), ("/bla/blub", False), (42, False)])
def test_check_dir_access(dir, val):
    assert check_dir_access(dir) == val


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


def test_BrowseDict():
    bd = BrowseDict(key=42)
    assert bd["key"] == bd.key == 42


def test_BrowseDict_assign():
    bd = BrowseDict()

    bd.key = "test"

    assert bd["key"] == bd.key == "test"


def test_BrowseDict_forbidden_keys():
    bd = BrowseDict()
    bd.FORBIDDEN_KEYS.append("forbidden")

    with pytest.raises(KeyError):
        bd["forbidden"] = "test"
