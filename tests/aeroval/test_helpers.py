import pytest
import pyaerocom.aeroval.helpers as mod
from pyaerocom.exceptions import VariableDefinitionError
from ..conftest import does_not_raise_exception


@pytest.mark.parametrize('dvar,var,raises', [
    ('od550aer', 'od550aer',does_not_raise_exception()),
    ('od550aer', 'od550gt1aer',does_not_raise_exception()),
    ('od550aer', 'bla', pytest.raises(VariableDefinitionError)),
    ('pr', 'prmm', pytest.raises(ValueError)),
    ('prmm', 'prmm', does_not_raise_exception()),
])
def test_check_var_ranges_avail(data_tm5,dvar,var,raises):
    data = data_tm5.copy()
    data.var_name = dvar
    with raises:
        mod.check_var_ranges_avail(data, var)
