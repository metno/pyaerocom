from pyaerocom.io.cmip_ctm.model_variables import cmip_variables


def test_cmip_variables():
    variables = cmip_variables()
    assert isinstance(variables, dict)
    assert variables["od550aer"] == "od550aer"
