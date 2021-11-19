import os

import pytest

import pyaerocom.varcollection as mod
from pyaerocom import __dir__ as pyadir
from pyaerocom.exceptions import VariableDefinitionError
from pyaerocom.variable import Variable

VAR_INI = os.path.join(pyadir, "data", "variables.ini")


def test_invalid_entries():
    col = mod.VarCollection(VAR_INI)
    invalid = []
    for var in col.all_vars:
        if "_" in var:
            invalid.append(var)

    assert len(invalid) == 0


def test_VAR_INI_exists():
    assert os.path.exists(VAR_INI)


def test_VARS_is_VarCollection():
    from pyaerocom import const

    assert isinstance(const.VARS, mod.VarCollection)


@pytest.mark.parametrize("var_ini", [VAR_INI])
def test_VarCollection___init__(var_ini):
    mod.VarCollection(var_ini)


@pytest.mark.parametrize(
    "var_ini,exception,error",
    [
        pytest.param(None, ValueError, "Invalid input for var_ini, need str", id="ValueError"),
        pytest.param(
            "/bla/blub", FileNotFoundError, "File /bla/blub does not exist", id="FileNotFoundError"
        ),
    ],
)
def test_VarCollection___init___error(var_ini, exception, error: str):
    with pytest.raises(exception) as e:
        mod.VarCollection(var_ini)
    assert str(e.value) == error


def test_VarCollection_add_var():
    var = Variable(var_name="concpm10gt1", units="ug m-3")
    col = mod.VarCollection(VAR_INI)
    col.add_var(var)
    assert var.var_name in col.all_vars


def test_VarCollection_add_var_error():
    var = Variable(var_name="concpm10", units="ug m-3")
    col = mod.VarCollection(VAR_INI)
    with pytest.raises(VariableDefinitionError) as e:
        col.add_var(var)
    assert str(e.value) == f"variable with name {var.var_name} is already defined"


def test_VarCollection_delete_var():
    var = Variable(var_name="concpm10", units="ug m-3")
    col = mod.VarCollection(VAR_INI)
    col.delete_variable(var.var_name)
    assert var.var_name not in col.all_vars


def test_VarCollection_delete_var_error():
    var = Variable(var_name="concpm10gt1", units="ug m-3")
    col = mod.VarCollection(VAR_INI)
    with pytest.raises(VariableDefinitionError) as e:
        col.delete_variable(var.var_name)
    assert str(e.value) == f"No such variable {var.var_name} in VarCollection"


@pytest.mark.parametrize(
    "var_name",
    [
        "blablub42",
        "od550aer",
    ],
)
def test_VarCollection_get_var(var_name):
    col = mod.VarCollection(VAR_INI)
    col.add_var(Variable(var_name="blablub42"))
    assert isinstance(col.get_var(var_name), Variable)


def test_VarCollection_get_var_error():
    col = mod.VarCollection(VAR_INI)
    var_name = "bla"
    with pytest.raises(VariableDefinitionError) as e:
        col.get_var(var_name)
    assert str(e.value) == f"Error (VarCollection): input variable {var_name} is not supported"


@pytest.mark.parametrize(
    "search_pattern,num",
    [
        ("*blaaaaaaa*", 0),
        ("dep*", 0),
        ("od*", 25),
        ("conc*", 71),
    ],
)
def test_VarCollection_find(search_pattern, num):
    col = mod.VarCollection(VAR_INI)
    result = col.find(search_pattern)
    assert len(result) == num


def test_VarCollection_delete_var_MULTIDEF():
    var = Variable(var_name="concpm10", units="ug m-3")
    col = mod.VarCollection(VAR_INI)
    col.all_vars.append("concpm10")
    with pytest.raises(VariableDefinitionError):
        col.delete_variable(var.var_name)


def test_VarCollection___dir__():
    col = mod.VarCollection(VAR_INI)
    result = dir(col)
    all_vars = col.all_vars

    assert len(result) == len(all_vars)
    assert result == sorted(all_vars)


@pytest.mark.parametrize("var,result", [("blablub", False), ("od550aer", True)])
def test_VarCollection___contains__(var, result):
    col = mod.VarCollection(VAR_INI)
    val = var in col
    assert val == result


def test_VarCollection___len__():
    col = mod.VarCollection(VAR_INI)
    assert len(col) > 0


def test_VarCollection___getitem__():
    col = mod.VarCollection(VAR_INI)
    assert isinstance(col["od550aer"], Variable)
    with pytest.raises(VariableDefinitionError):
        col["blaaaa"]


def test_VarCollection___repr__():
    assert repr(mod.VarCollection(VAR_INI)).startswith("VarCollection")


def test_VarCollection___str__():
    assert str(mod.VarCollection(VAR_INI)).startswith("VarCollection")
