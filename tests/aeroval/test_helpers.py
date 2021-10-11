import pytest
from pyaerocom import const
import pyaerocom.aeroval.helpers as mod
from pyaerocom.exceptions import VariableDefinitionError
from pyaerocom.varcollection import VarCollection
from ..conftest import does_not_raise_exception


@pytest.mark.parametrize('dvar,var,raises', [
    ('od550aer', 'od550aer',does_not_raise_exception()),
    ('od550aer', 'od550gt1aer',does_not_raise_exception()),
    ('od550aer', 'bla', pytest.raises(VariableDefinitionError)),
    ('pr', 'prmm', does_not_raise_exception()),
    ('prmm', 'prmm', does_not_raise_exception()),
])
def test_check_var_ranges_avail(data_tm5,dvar,var,raises):
    data = data_tm5.copy()
    data.var_name = dvar
    with raises:
        mod.check_var_ranges_avail(data, var)
    # cleanup
    varcfg = const._var_info_file
    const._var_param = VarCollection(varcfg)

@pytest.mark.parametrize('periods,result,raises', [
    (42, None, pytest.raises(ValueError)),
    ([42], None, pytest.raises(ValueError)),
    (['2010-2010-20'], None, pytest.raises(ValueError)),
    (['2010-2010', '2005'], ['2010-2010', '2005'], does_not_raise_exception()),
])
def test__check_statistics_periods(periods,result,raises):
    with raises:
        val = mod._check_statistics_periods(periods)
        assert val == result

@pytest.mark.parametrize('period,result,raises', [
    ('2005', slice('2005','2005'), does_not_raise_exception()),
    ('2005-2019', slice('2005','2019'), does_not_raise_exception()),
    ('2005-2019-2000', None, pytest.raises(ValueError)),
])
def test__period_str_to_timeslice(period,result,raises):
    with raises:
        val = mod._period_str_to_timeslice(period)
        assert val == result

@pytest.mark.parametrize('statistics_periods,result,raises', [
    (['2005', '2000'], (2000,2005), does_not_raise_exception()),
    (['2005', '2000', '1999-2021'], (1999,2021), does_not_raise_exception()),
    (['2005-2004-23', '2000', '1999-2021'], None,
     pytest.raises(ValueError)),
])
def test__get_min_max_year_periods(statistics_periods,result,raises):
    with raises:
        val = mod._get_min_max_year_periods(statistics_periods)
        assert val == result