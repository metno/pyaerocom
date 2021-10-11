import pytest
import os
from pyaerocom import __dir__ as pyadir
from pyaerocom.exceptions import VariableDefinitionError
from pyaerocom.variable import Variable
import pyaerocom.varcollection as mod
from .conftest import does_not_raise_exception

VAR_INI = os.path.join(pyadir, 'data', 'variables.ini')

def test_invalid_entries():
    col = mod.VarCollection(VAR_INI)
    invalid = []
    for var in col.all_vars:
        if '_' in var:
            invalid.append(var)

    assert len(invalid) == 0

def test_VAR_INI_exists():
    assert os.path.exists(VAR_INI)

def test_VARS_is_VarCollection():
    from pyaerocom import const
    assert isinstance(const.VARS, mod.VarCollection)

@pytest.mark.parametrize('var_ini,raises', [
    (None, pytest.raises(ValueError)),
    ('/bla/blub', pytest.raises(FileNotFoundError)),
    (VAR_INI, does_not_raise_exception())
])
def test_VarCollection___init__(var_ini,raises):
    with raises:
        col = mod.VarCollection(var_ini)

@pytest.mark.parametrize('var_name,raises', [
    ('concpm10gt1', does_not_raise_exception()),
    ('concpm10', pytest.raises(VariableDefinitionError)),
])
def test_VarCollection_add_var(var_name,raises):
    var = Variable(var_name=var_name, units='ug m-3')
    col = mod.VarCollection(VAR_INI)
    with raises:
        col.add_var(var)
        all_vars = col.all_vars
        assert var.var_name in all_vars

@pytest.mark.parametrize('var_name,raises', [
    ('concpm10gt1', pytest.raises(VariableDefinitionError)),
    ('concpm10', does_not_raise_exception()),
])
def test_VarCollection_delete_var(var_name,raises):
    var = Variable(var_name=var_name, units='ug m-3')
    col = mod.VarCollection(VAR_INI)
    with raises:
        col.delete_variable(var.var_name)
        assert var.var_name not in col.all_vars

@pytest.mark.parametrize('var,raises', [
    ('bla', pytest.raises(VariableDefinitionError)),
    ('blablub42', does_not_raise_exception()),
    ('od550aer', does_not_raise_exception()),
])
def test_VarCollection_get_var(var,raises):
    col = mod.VarCollection(VAR_INI)
    add = Variable(var_name='blablub42')
    col.add_var(add)
    with raises:
        result = col.get_var(var)
        assert isinstance(result, Variable)

@pytest.mark.parametrize('search_pattern,num,raises', [
    ('*blaaaaaaa*', 0, does_not_raise_exception()),
    ('dep*', 0, does_not_raise_exception()),
    ('od*', 25, does_not_raise_exception()),
    ('conc*', 70, does_not_raise_exception()),
])
def test_VarCollection_find(search_pattern,num,raises):
    col = mod.VarCollection(VAR_INI)
    with raises:
        result = col.find(search_pattern)
        assert len(result) == num

def test_VarCollection_delete_var_MULTIDEF():
    var = Variable(var_name='concpm10', units='ug m-3')
    col = mod.VarCollection(VAR_INI)
    col.all_vars.append('concpm10')
    with pytest.raises(VariableDefinitionError):
        col.delete_variable(var.var_name)

def test_VarCollection___dir__():
    col = mod.VarCollection(VAR_INI)
    result = dir(col)
    all_vars = col.all_vars

    assert len(result) == len(all_vars)
    assert result == sorted(all_vars)

@pytest.mark.parametrize('var,result', [
    ('blablub', False),
    ('od550aer', True)
])
def test_VarCollection___contains__(var,result):
    col = mod.VarCollection(VAR_INI)
    val = var in col
    assert val==result

def test_VarCollection___len__():
    col = mod.VarCollection(VAR_INI)
    assert len(col) > 0

def test_VarCollection___getitem__():
    col = mod.VarCollection(VAR_INI)
    assert isinstance(col['od550aer'], Variable)
    with pytest.raises(VariableDefinitionError):
        col['blaaaa']

def test_VarCollection___repr__():
    assert repr(mod.VarCollection(VAR_INI)).startswith('VarCollection')

def test_VarCollection___str__():
    assert str(mod.VarCollection(VAR_INI)).startswith('VarCollection')