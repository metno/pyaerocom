import pytest
import simplejson
import os
from pyaerocom.conftest import (coldata_tm5_aeronet,
                                does_not_raise_exception,
                                tempdir)

from pyaerocom.web import helpers_evaluation_iface as h

@pytest.mark.dependency
def test_get_stationfile_name():
    name = h.get_stationfile_name('bla', 'blub', 'var', 'invalid')
    assert name == 'bla_OBS-blub:var_invalid.json'

def test_get_json_mapname():
    obs_name, obs_var, model_name, model_var, vert_code = ('bla', 'ovar', 'blub', 'var', 'invalid')
    name = h.get_json_mapname(obs_name, obs_var, model_name, model_var, vert_code)
    assert name == 'OBS-bla:ovar_invalid_MOD-blub:var.json'

@pytest.mark.parametrize('ts_data, out_dirs, raises', [
    (None,{},pytest.raises(TypeError)),
    ({},{},pytest.raises(KeyError)),
    (dict(station_name='bla',
          web_iface_name='blub',
          obs_var='ovar',
          vert_code='invalid'),{},pytest.raises(KeyError)),
    (dict(station_name='bla',
          web_iface_name='blub',
          obs_var='ovar',
          vert_code='invalid'),{'ts':'/invalid/42/imagine'},pytest.raises(KeyError)),
    (dict(station_name='bla',
          web_iface_name='blub',
          obs_var='ovar',
          vert_code='invalid',
          model_name='whatever'),{'ts':'/invalid/42/imagine'},pytest.raises(FileNotFoundError)),
    (dict(station_name='bla',
          web_iface_name='blub',
          obs_var='ovar',
          vert_code='invalid',
          model_name='whatever'),{'ts':'tmpdir'}, does_not_raise_exception()),
    # repeat previous to check add entry in existing file
    (dict(station_name='bla',
          web_iface_name='blub',
          obs_var='ovar',
          vert_code='invalid',
          model_name='whatever'),{'ts':'tmpdir'}, does_not_raise_exception()),
    ])
@pytest.mark.dependency(depends=["test_get_stationfile_name"])
def test__write_stationdata_json(ts_data, out_dirs, raises, tempdir):
    with raises:
        if 'ts' in out_dirs and out_dirs['ts'] == 'tmpdir':
            out_dirs['ts'] = tempdir
        h._write_stationdata_json(ts_data, out_dirs)
        fname = h.get_stationfile_name(ts_data['station_name'],
                                       ts_data['web_iface_name'],
                                       ts_data['obs_var'],
                                       ts_data['vert_code'])
        fp = os.path.join(out_dirs['ts'], fname)
        assert os.path.exists(fp)

@pytest.mark.parametrize('heatmap_file, result, obs_name, obs_var, vert_code, model_name, model_var, raises', [
    ('', 42, 'bla', 'ovar', 'invalid', 'blub', 'mvar', pytest.raises(FileNotFoundError)),
    ('tempdir/glob_stats.json', 42, 'bla', 'ovar', 'invalid', 'blub', 'mvar',
     does_not_raise_exception()),
    # repeat previous to check add entry in existing file
    ('tempdir/glob_stats.json', 42, 'bla', 'ovar', 'invalid', 'blub', 'mvar',
     does_not_raise_exception()),
    ('tempdir/glob_stats.json', 43, 'bla', 'ovar', 'Surface', 'blub', 'mvar',
     does_not_raise_exception())
    ])
def test__add_entry_heatmap_json(heatmap_file, result, obs_name, obs_var, vert_code,
                                 model_name, model_var, raises, tempdir):
    with raises:
        if 'tempdir' in heatmap_file:
            heatmap_file = heatmap_file.replace('tempdir', str(tempdir))
        h._add_entry_heatmap_json(heatmap_file, result, obs_name, obs_var,
                                  vert_code, model_name, model_var)
        assert os.path.exists(heatmap_file)
        with open(heatmap_file) as f:
            data = simplejson.load(f)
        assert data[obs_var][obs_name][vert_code][model_name][model_var] == result

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)