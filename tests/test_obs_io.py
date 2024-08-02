from copy import deepcopy

import pytest

from pyaerocom.obs_io import (
    OBS_ALLOW_ALT_WAVELENGTHS,
    OBS_WAVELENGTH_TOL_NM,
    AuxInfoUngridded,
    ObsVarCombi,
)

AUX_EXAMPLE = dict(
    data_id="AERONET",
    vars_supported=["fmf550aer", "od550lt1aer"],
    aux_merge_how={"fmf550aer": "eval", "od550lt1aer": "combine"},
    aux_requires={
        "fmf550aer": {
            "AeronetSDAV3Lev2.daily": "od550lt1aer",
            "AeronetSunV3Lev2.daily": "od550aer",
        },
        "od550lt1aer": {
            "AeronetSDAV3Lev2.daily": "od550lt1aer",
            "AeronetSunV3Lev2.daily": "od550aer",
        },
    },
    aux_funs={
        "fmf550aer": "(AeronetSDAV3Lev2.daily;od550lt1aer/AeronetSunV3Lev2.daily;od550aer)*100"
    },
    aux_units={"fmf550aer": "%"},
)


def test_OBS_WAVELENGTH_TOL_NM():
    assert OBS_WAVELENGTH_TOL_NM == 10.0


def test_OBS_ALLOW_ALT_WAVELENGTHS():
    assert OBS_ALLOW_ALT_WAVELENGTHS is True


def test_ObsVarCombi():
    assert str(ObsVarCombi("bla", "blub")) == "bla;blub"


def test_AuxInfoUngridded_MAX_VARS_PER_METHOD():
    assert AuxInfoUngridded.MAX_VARS_PER_METHOD == 2


EX_WRONG1: dict = deepcopy(AUX_EXAMPLE)
EX_WRONG1.update(aux_funs=None)

EX_WRONG2 = deepcopy(AUX_EXAMPLE)
EX_WRONG2.update(vars_supported={"a": 1})

EX_WRONG3: dict = deepcopy(AUX_EXAMPLE)
EX_WRONG3["vars_supported"].append("blablub")

EX_WRONG4 = deepcopy(EX_WRONG3)
EX_WRONG4["aux_merge_how"].update(blablub="eval")

EX_WRONG5 = deepcopy(EX_WRONG4)
EX_WRONG5["aux_requires"].update(blablub=42)

EX_WRONG6 = deepcopy(EX_WRONG5)
EX_WRONG6["aux_requires"].update(blablub={"abc": "42"})

EX_WRONG7 = deepcopy(EX_WRONG6)
EX_WRONG7["aux_requires"]["blablub"].update({"def": "43"})


@pytest.mark.parametrize(
    "kwargs,error",
    [
        (EX_WRONG1, "Specification of computation function is missing for var fmf550aer"),
        (EX_WRONG2, "Variable a is not defined in attr aux_requires..."),
        (EX_WRONG3, "Variable blablub is not defined in attr aux_requires..."),
        (EX_WRONG4, "Variable blablub is not defined in attr aux_requires..."),
        (EX_WRONG5, "Specification of computation function is missing for var blablub"),
        (EX_WRONG6, "Specification of computation function is missing for var blablub"),
        (EX_WRONG7, "Specification of computation function is missing for var blablub"),
    ],
)
def test_AuxInfoUngridded_error(kwargs, error: str):
    with pytest.raises(ValueError) as e:
        AuxInfoUngridded(**kwargs)
    assert str(e.value) == error


EX_NOTWRONG1 = deepcopy(EX_WRONG7)
EX_NOTWRONG1["aux_funs"]["blablub"] = "abc;42+def;43"

EX_NOTWRONG2 = deepcopy(EX_NOTWRONG1)
EX_NOTWRONG2["aux_units"]["blablub"] = "1"


@pytest.mark.parametrize(
    "kwargs",
    [
        AUX_EXAMPLE,
        EX_NOTWRONG1,
        EX_NOTWRONG2,
    ],
)
def test_AuxInfoUngridded_to_dict(kwargs):
    info = AuxInfoUngridded(**kwargs)
    assert info.to_dict() == kwargs
