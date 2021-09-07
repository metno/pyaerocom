from pytest import raises

from pyaerocom.aeroval import EvalSetup


def test_evalsetup():
    conf = EvalSetup("project", "experiment")
    assert conf
    assert conf.proj_id == conf.proj_info.proj_id == "project"
    assert conf.exp_id == conf.exp_info.exp_id == "experiment"


def test_evalsetup_exception():
    with raises((KeyError, ValueError)):
        EvalSetup()

    with raises((KeyError, ValueError)):
        EvalSetup("project")

    with raises((KeyError, ValueError)):
        EvalSetup(proj_id="project")

    with raises((KeyError, ValueError)):
        EvalSetup(exp_id="experiment")
