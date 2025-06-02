import pytest

from pyaerocom import const
from pyaerocom.data import resources
from pyaerocom.exceptions import VariableDefinitionError
from pyaerocom.varcollection import VarCollection
from pyaerocom.variable import Variable


def test_VARS_is_VarCollection():
    assert isinstance(const.VARS, VarCollection)


@pytest.fixture()
def collection() -> VarCollection:
    with resources.path("pyaerocom.data", "variables.ini") as path:
        assert path.exists()
        return VarCollection(str(path))


def test_invalid_entries(collection: VarCollection):
    invalid = ("_" in var for var in collection.all_vars)
    assert sum(invalid) == 0


@pytest.mark.parametrize(
    "var_ini,exception,error",
    [
        pytest.param(None, ValueError, "Invalid input for var_ini, need str", id="ValueError"),
        pytest.param(
            "/bla/blub",
            FileNotFoundError,
            "File /bla/blub does not exist",
            id="FileNotFoundError",
        ),
    ],
)
def test_VarCollection___init___error(var_ini, exception, error: str):
    with pytest.raises(exception) as e:
        VarCollection(var_ini)
    assert str(e.value) == error


def test_VarCollection_add_var(collection: VarCollection):
    var = Variable(var_name="concpm10gt1", units="ug m-3")
    collection.add_var(var)
    assert var.var_name in collection.all_vars


def test_VarCollection_add_var_error(collection: VarCollection):
    var = Variable(var_name="concpm10", units="ug m-3")
    with pytest.raises(VariableDefinitionError) as e:
        collection.add_var(var)
    assert str(e.value) == f"variable with name {var.var_name} is already defined"


def test_VarCollection_delete_var(collection: VarCollection):
    var = Variable(var_name="concpm10", units="ug m-3")
    collection.delete_variable(var.var_name)
    assert var.var_name not in collection.all_vars


def test_VarCollection_delete_var_error(collection: VarCollection):
    var = Variable(var_name="concpm10gt1", units="ug m-3")
    with pytest.raises(VariableDefinitionError) as e:
        collection.delete_variable(var.var_name)
    assert str(e.value) == f"No such variable {var.var_name} in VarCollection"


@pytest.mark.parametrize("var_name", ["blablub42", "od550aer"])
def test_VarCollection_get_var(collection: VarCollection, var_name: str):
    collection.add_var(Variable(var_name="blablub42"))
    assert isinstance(collection.get_var(var_name), Variable)


def test_VarCollection_get_var_error(collection: VarCollection):
    var_name = "bla"
    with pytest.raises(VariableDefinitionError) as e:
        collection.get_var(var_name)
    assert str(e.value) == f"Error (VarCollection): input variable {var_name} is not supported"


@pytest.mark.parametrize(
    "search_pattern,num",
    [
        ("*blaaaaaaa*", 0),
        ("dep*", 9),
        ("od*", 27),
        ("conc*", 122),
    ],
)
def test_VarCollection_find(collection: VarCollection, search_pattern: str, num: int):
    result = collection.find(search_pattern)
    assert len(result) == num


def test_VarCollection_delete_var_MULTIDEF(collection: VarCollection):
    var_name = "concpm10"
    collection.all_vars.append(var_name)
    with pytest.raises(VariableDefinitionError) as e:
        collection.delete_variable(var_name)
    assert f"found multiple matches for variable {var_name} in VarCollection" in str(e.value)


def test_VarCollection___dir__(collection: VarCollection):
    result = dir(collection)
    all_vars = collection.all_vars

    assert len(result) == len(all_vars)
    assert result == sorted(all_vars)


@pytest.mark.parametrize("var_name,found", [("blablub", False), ("od550aer", True)])
def test_VarCollection___contains__(collection: VarCollection, var_name: str, found: bool):
    assert (var_name in collection) == found


def test_VarCollection___len__(collection: VarCollection):
    assert len(collection) > 0


def test_VarCollection___getitem__(collection: VarCollection):
    assert isinstance(collection["od550aer"], Variable)


def test_VarCollection___getitem___error(collection: VarCollection):
    var_name = "blaaaa"
    assert var_name not in collection
    with pytest.raises(VariableDefinitionError) as e:
        collection[var_name]
    assert str(e.value).endswith(f"input variable {var_name} is not supported")


def test_VarCollection___repr__(collection: VarCollection):
    assert repr(collection).startswith("VarCollection")


def test_VarCollection___str__(collection: VarCollection):
    assert str(collection).startswith("VarCollection")
