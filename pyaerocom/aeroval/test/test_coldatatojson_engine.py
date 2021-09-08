
import pytest
import pyaerocom.aeroval.coldatatojson_engine as mod


def test_get_heatmap_filename():
    assert mod.get_heatmap_filename('daily') ==  'glob_stats_daily.json'

def test_get_stationfile_name():

    val = mod.get_stationfile_name('stat1', 'obs1', 'var1', 'Column')
    assert val == 'stat1_obs1-var1_Column.json'

def test_get_json_mapname():
    """Get name base name of json file"""
    val = mod.get_json_mapname('obs1', 'var1', 'mod1', 'var1', 'Column')
    assert val == 'obs1-var1_Column_mod1-var1.json'

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)
