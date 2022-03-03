from pyaerocom.variable_helpers import get_emep_variables


def test_get_emep_variables():
    variables = get_emep_variables()
    assert isinstance(variables, dict)
    assert variables["conco3"] == "SURF_ug_O3"
