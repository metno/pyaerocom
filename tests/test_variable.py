import pytest
from pyaerocom.variable import Variable
from .conftest import does_not_raise_exception

@pytest.mark.parametrize('var_name,init,cfg,kwargs,raises', [
    (None, True, None, {}, does_not_raise_exception()),
    (None, True, 'bla', {}, pytest.raises(ValueError)),
    ('bla_blub', True, None, {}, pytest.raises(ValueError)),
    ('od550aer', True, None, {'bla': 42}, does_not_raise_exception()),
    ('od550aer', True, None, {'map_vmin': 0, 'map_vmax': 1},
     does_not_raise_exception()),
    ('concpm10', False, None, {}, does_not_raise_exception()),
    ('concpm103d', False, None, {}, does_not_raise_exception()),
    ('concpm103D', False, None, {}, does_not_raise_exception()),

])
def test_Variable___init__(var_name,init,cfg,kwargs,raises):
    with raises:
        var = Variable(var_name=var_name, init=init, cfg=cfg, **kwargs)
        for key, val in kwargs.items():
            assert getattr(var, key) == val


@pytest.mark.parametrize('var_name,var_name_aerocom', [
    ('od550aer3D', 'od550aer'),
    ('od550aer', 'od550aer'),
    ('od550du', 'od550dust'),
    ('od550csaer', 'od550aer'),
    ('latitude', 'lat'),
    ('abs550oc', 'abs550oa'),
    ('sconcss', 'concss'),

    ])
def test_Variable_var_name_aerocom(var_name, var_name_aerocom):
    var = Variable(var_name)
    assert var.var_name_aerocom == var_name_aerocom

def test_Variable_alias_var():
    assert 'od550csaer' == Variable('od550aer')

def test_Variable_alias_families():
    var = Variable('sconcso4')

    assert var.var_name_input == 'sconcso4'
    assert var.var_name == 'sconcso4'
    assert var.var_name_aerocom == 'concso4'
    assert var.units == 'ug m-3'

@pytest.mark.parametrize('var,result', [
    ('od550aer', False), ('emiso4', True), ('depso4', False), ('pr', False),
    ('prmm', False), ('dryso4', False), ('wetso4', False)
])
def test_Variable_is_emission(var,result):
    assert Variable(var).is_emission == result

@pytest.mark.parametrize('var,result', [
    ('od550aer', False), ('emiso4', False), ('depso4', True), ('pr', False),
    ('prmm', False), ('dryso4', True), ('wetso4', True)
])
def test_Variable_is_deposition(var,result):
    assert Variable(var).is_deposition == result

@pytest.mark.parametrize('var,result', [
    ('od550aer', False), ('emiso4', True), ('depso4', True), ('pr', True),
    ('prmm', True), ('dryso4', True), ('wetso4', True)
])
def test_Variable_is_rate(var,result):
    var = Variable(var)
    assert var.is_rate == result

def test_Variable___str__():
    var = Variable('od550aer')
    s = str(var)
    assert isinstance(s, str)