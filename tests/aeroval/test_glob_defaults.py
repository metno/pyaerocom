from pyaerocom.aeroval.glob_defaults import var_web_info


def test_var_web_info():
    unique_entries = list(set(var_web_info))
    assert len(unique_entries) == len(var_web_info.keys())
