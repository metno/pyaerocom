from pyaerocom.io.cmip_ctm.model_variables import cmip_variables, cmip_aux_info, cmip_aliases


def test_cmip_variables():
    variables = cmip_variables()
    assert isinstance(variables, dict)
    assert variables["od550aer"] == "od550aer"


def test_aux_info():
    aux_info = cmip_aux_info()
    assert isinstance(aux_info, dict)
    assert "concso4" in aux_info
    assert "aux_vars" in aux_info["concso4"]
    assert sorted(aux_info["concso4"]["aux_vars"]) == ["ps", "ts"]


def test_cmip_aliases():
    aliases = cmip_aliases()
    assert isinstance(aliases, dict)
    assert "ts" in aliases
    assert "alias" in aliases["ts"]
    assert aliases["ts"]["alias"][0] == "ta"
