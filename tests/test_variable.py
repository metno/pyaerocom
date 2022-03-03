from __future__ import annotations

import pytest

from pyaerocom.variable import Variable


@pytest.mark.parametrize(
    "var_name,init,kwargs",
    [
        (None, True, {}),
        ("od550aer", None, {"bla": 42}),
        ("od550aer", None, {"map_vmin": 0, "map_vmax": 1}),
        ("concpm10", None, {}),
        ("concpm103d", None, {}),
        ("concpm103D", None, {}),
    ],
)
def test_Variable(var_name: str | None, init: bool, kwargs: dict):
    var = Variable(var_name, init, **kwargs)
    for key, val in kwargs.items():
        assert getattr(var, key) == val


@pytest.mark.parametrize(
    "var_name,cfg,error",
    [
        pytest.param(
            None,
            "bla",
            "invalid input for cfg, need config parser got <class 'str'>",
            id="not a config parser",
        ),
        pytest.param(
            "bla_blub",
            None,
            "invalid variable name bla_blub. Must not contain underscore",
            id="variable name with underscore",
        ),
    ],
)
def test_Variable_error(var_name: str | None, cfg, error: str):
    with pytest.raises(ValueError) as e:
        Variable(var_name, True, cfg)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "var_name,var_name_aerocom",
    [
        ("od550aer3D", "od550aer"),
        ("od550aer", "od550aer"),
        ("od550du", "od550dust"),
        ("od550csaer", "od550aer"),
        ("latitude", "lat"),
        ("abs550oc", "abs550oa"),
        ("sconcss", "concss"),
    ],
)
def test_Variable_var_name_aerocom(var_name: str, var_name_aerocom: str):
    assert Variable(var_name).var_name_aerocom == var_name_aerocom


def test_Variable_alias_var():
    assert "od550csaer" == Variable("od550aer")


def test_Variable_alias_families():
    var = Variable("sconcso4")

    assert var.var_name_input == "sconcso4"
    assert var.var_name == "sconcso4"
    assert var.var_name_aerocom == "concso4"
    assert var.units == "ug m-3"


@pytest.mark.parametrize(
    "var_name,result",
    [
        ("od550aer", False),
        ("emiso4", True),
        ("depso4", False),
        ("pr", False),
        ("prmm", False),
        ("dryso4", False),
        ("wetso4", False),
    ],
)
def test_Variable_is_emission(var_name: str, result: bool):
    assert Variable(var_name).is_emission == result


@pytest.mark.parametrize(
    "var_name,result",
    [
        ("od550aer", False),
        ("emiso4", False),
        ("depso4", True),
        ("pr", False),
        ("prmm", False),
        ("dryso4", True),
        ("wetso4", True),
    ],
)
def test_Variable_is_deposition(var_name: str, result: bool):
    assert Variable(var_name).is_deposition == result


@pytest.mark.parametrize(
    "var_name,result",
    [
        ("od550aer", False),
        ("emiso4", True),
        ("depso4", True),
        ("pr", True),
        ("prmm", True),
        ("dryso4", True),
        ("wetso4", True),
    ],
)
def test_Variable_is_rate(var_name: str, result: bool):
    assert Variable(var_name).is_rate == result


def test_Variable___str__():
    var = Variable("od550aer")
    s = str(var)
    assert s.startswith("\nPyaerocom Variable")
    assert "var_name: od550aer" in s
