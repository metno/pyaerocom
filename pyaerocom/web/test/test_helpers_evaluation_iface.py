import pytest
import simplejson
import os
from pyaerocom.conftest import (coldata_tm5_aeronet,
                                does_not_raise_exception,
                                tempdir)

from pyaerocom.web import helpers_evaluation_iface as h
@pytest.mark.parametrize('base_dir, proj_id, exp_id', [
    ('/blaaa', 'blub', '42'), ('tmpdir', 'blub', '42'),
    ])
def test_delete_experiment_data_evaluation_iface(base_dir, proj_id, exp_id,
                                                 tmpdir):
    if base_dir == 'tmpdir':
        base_dir = tmpdir
        dp = os.path.join(str(tmpdir), proj_id, exp_id)
        os.makedirs(dp)
        assert os.path.exists(dp)
    h.delete_experiment_data_evaluation_iface(base_dir, proj_id, exp_id)

@pytest.mark.parametrize('cfgdir, mkfiles, raises', [
    ('/blaaa', None, does_not_raise_exception()),
    ('tmpdir', None, does_not_raise_exception()),
    ('tmpdir', [('bla', 'blub')], does_not_raise_exception()),
    ('tmpdir', [('bla', 'blub_blablub')], does_not_raise_exception()),
    ('tmpdir', [('bla', 'blub'), ('bla', 'blub1'), ('blub', 'blub')], does_not_raise_exception()),
    ])
def test_get_all_config_files_evaluation_iface(cfgdir, mkfiles, raises,
                                               tmpdir):
    res = {}
    if cfgdir == 'tmpdir':
        cfgdir = str(tmpdir)
        if isinstance(mkfiles, list):
            for pr, ex in mkfiles:

                fname = f'cfg_{pr}_{ex}.json'
                fp = os.path.join(tmpdir, fname)
                with open(fp, 'w'):
                    print(fp)
                if '_' in pr or '_' in ex:
                    continue
                if not pr in res:
                    res[pr] = {}
                res[pr][ex] = fp
    result = h.get_all_config_files_evaluation_iface(cfgdir)
    assert result == res

@pytest.mark.parametrize('exp_order, raises', [
    (['42', 'invalid'], does_not_raise_exception()),
    ('42', does_not_raise_exception()),
    ('43', does_not_raise_exception()),
    (None, does_not_raise_exception()),
    ({}, pytest.raises(ValueError))
    ])
def test_reorder_experiments_menu_evaluation_iface(exp_order, raises,
                                                   tmpdir):
    menu = {'bla' : {}, 'blub': {}, '42': {}}
    fp = tmpdir.join('menu.json')
    with open(fp, 'w') as f:
        simplejson.dump(menu, f)
    with raises:
        h.reorder_experiments_menu_evaluation_iface(fp, exp_order)

        with open(fp, 'r') as f:
            new = simplejson.load(f)
        if isinstance(exp_order, str):
            exp_order = [exp_order]
        elif exp_order is None:
            exp_order = []
        new_order = []
        for exp in exp_order:
            if exp in menu:
                new_order.append(exp)
        for exp in sorted(menu):
            if not exp in new_order:
                new_order.append(exp)
        assert list(new.keys()) == new_order


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