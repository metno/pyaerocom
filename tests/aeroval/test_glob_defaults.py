from pyaerocom.aeroval.glob_defaults import VarWebInfo


def test_var_web_info():
    var_web_info = VarWebInfo()
    unique_entries = list(set(var_web_info))
    assert len(unique_entries) == len(var_web_info.keys())
