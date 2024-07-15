from pyaerocom.io.mscw_ctm.model_variables import emep_variables


def test_emep_variables():
    variables = emep_variables()
    assert isinstance(variables, dict)
    assert variables["conco3"] == "SURF_ug_O3"
