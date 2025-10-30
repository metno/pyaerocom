from pyaerocom.io.cmip_ctm.model_variables import cmip_variables


def test_emep_variables():
    variables = cmip_variables()
    assert isinstance(variables, dict)
    assert variables["conco3"] == "SURF_ug_O3"
