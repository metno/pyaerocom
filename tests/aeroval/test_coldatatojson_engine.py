import numpy as np

import pytest

import pyaerocom.aeroval.coldatatojson_engine as mod
import pyaerocom.exceptions as exceptions
from pyaerocom import ColocatedData, TsType

from ..conftest import does_not_raise_exception


def test_get_heatmap_filename():
    assert mod.get_heatmap_filename('daily') ==  'glob_stats_daily.json'

def test_get_stationfile_name():

    val = mod.get_stationfile_name('stat1', 'obs1', 'var1', 'Column')
    assert val == 'stat1_obs1-var1_Column.json'

def test_get_json_mapname():
    """Get name base name of json file"""
    val = mod.get_json_mapname('obs1', 'var1', 'mod1', 'var1', 'Column')
    assert val == 'obs1-var1_Column_mod1-var1.json'

@pytest.mark.parametrize('which,to_ts_types,raises', [
    ('tm5_aeronet', ['daily', 'monthly'], does_not_raise_exception()),
    ('tm5_aeronet', ['3yearly'], does_not_raise_exception())
    ])
def test__init_data_default_frequencies(coldata, which, to_ts_types, raises):
    data = coldata[which]
    with raises:
        result = mod._init_data_default_frequencies(data, to_ts_types)
        tst = TsType(data.ts_type)
        assert len(result) == len(to_ts_types)
        for freq, val in result.items():
            if TsType(freq) > tst:
                assert val is None
            else:
                assert isinstance(val, ColocatedData)
                assert val.ts_type == freq

@pytest.fixture(scope='module')
def example_coldata(coldata):
    return mod._init_data_default_frequencies(coldata['tm5_aeronet'],
                                              ['daily', 'monthly', 'yearly'])


def test_get_jsdate(example_coldata):
    vals = mod._get_jsdate(example_coldata['monthly'].data.time.values)
    assert len(vals) == 12

@pytest.mark.parametrize('freq,region_ids,use_weights,use_country,data_freq,nmb_avg,raises', [
    ('yearly', {'EUROPE':'Europe'}, False, False, 'monthly',0.168, does_not_raise_exception()),
    ('yearly', {'EUROPE':'Europe'}, False, False, None, 0.122, does_not_raise_exception()),
    ('monthly', {'EUROPE':'Europe'}, False, False, None, 0.181, does_not_raise_exception()),
    ('monthly', {'EUR':'Europe(HTAP)'}, False, False, None, 0.181, does_not_raise_exception()),

    ('monthly', {'SEA':'SE Asia(HTAP)'}, False, False, None, np.nan, does_not_raise_exception()),
    ('monthly', {'SEA':'SE Asia(HTAP)','EUR':'Europe(HTAP)'}, False, False, None,0.181, does_not_raise_exception()),
    ('monthly', {'bla':'blub'}, False, False, None,np.nan,
     pytest.raises(exceptions.UnknownRegion)),
    ('monthly', {}, False, False, None, np.nan,does_not_raise_exception()),
    ('daily', {}, False, False, 'daily', np.nan,
     pytest.raises(exceptions.TemporalResolutionError)),
    ('daily', {}, False, False, 'monthly', np.nan,
     pytest.raises(exceptions.TemporalResolutionError)),

    ])
def test__process_statistics_timeseries(example_coldata,
                                        freq,region_ids,use_weights,
                                        use_country,data_freq,
                                        nmb_avg, raises):
    with raises:
        result = mod._process_statistics_timeseries(example_coldata,
                                                    freq, region_ids, use_weights,
                                                    use_country, data_freq)
        assert len(result) == len(region_ids)
        biases = [np.nan]
        for region, data in result.items():
            for jsdate, stats in data.items():
                biases.append(stats['nmb'])
        mean_bias = np.nanmean(biases)
        if np.isnan(nmb_avg):
            assert np.isnan(mean_bias)
        else:
            np.testing.assert_allclose(mean_bias, nmb_avg, atol=0.001)


if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
