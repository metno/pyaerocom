import pytest
import simplejson
import os
from pyaerocom.conftest import (coldata_tm5_aeronet,
                                coldata_tm5_tm5,
                                does_not_raise_exception,
                                tempdir)
from pyaerocom import ColocatedData, Region
from pyaerocom.region_defs import OLD_AEROCOM_REGIONS, HTAP_REGIONS_DEFAULT
from pyaerocom.region import get_all_default_region_ids
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

@pytest.mark.parametrize('ts_data, out_dir, raises', [
    (None,'',pytest.raises(TypeError)),
    ({},'',pytest.raises(KeyError)),
    (dict(station_name='bla',
          web_iface_name='blub',
          obs_var='ovar',
          vert_code='invalid'),'',pytest.raises(KeyError)),
    (dict(station_name='bla',
          web_iface_name='blub',
          obs_var='ovar',
          vert_code='invalid'),'/invalid/42/imagine',pytest.raises(KeyError)),
    (dict(station_name='bla',
          web_iface_name='blub',
          obs_var='ovar',
          vert_code='invalid',
          model_name='whatever'),'/invalid/42/imagine', pytest.raises(FileNotFoundError)),

    # repeat previous to check add entry in existing file
    (dict(station_name='bla',
          web_iface_name='blub',
          obs_var='ovar',
          vert_code='invalid',
          model_name='whatever'),'tmpdir', does_not_raise_exception()),

    ])
@pytest.mark.dependency(depends=["test_get_stationfile_name"])
def test__write_stationdata_json(ts_data, out_dir, raises, tmpdir):
    with raises:
        if out_dir == 'tmpdir':
            out_dir = tmpdir
        h._write_stationdata_json(ts_data, out_dir)
        fname = h.get_stationfile_name(ts_data['station_name'],
                                       ts_data['web_iface_name'],
                                       ts_data['obs_var'],
                                       ts_data['vert_code'])
        fp = os.path.join(out_dir, fname)
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

def test__init_stats_dummy():
    dummy = h._init_stats_dummy()
    keys =  sorted(list(dummy.keys()))
    assert keys == ['R', 'R_kendall', 'R_spearman', 'data_mean', 'data_std',
                    'fge', 'mnmb', 'nmb', 'num_valid', 'refdata_mean',
                    'refdata_std', 'rms', 'totnum', 'weighted']

def test__check_flatten_latlon_dims_3d(coldata_tm5_aeronet):
    cd = h._check_flatten_latlon_dims(coldata_tm5_aeronet)
    assert isinstance(cd, ColocatedData)
    assert 'station_name' in cd.data.dims

def test__check_flatten_latlon_dims_4d(coldata_tm5_tm5):
    cd = h._check_flatten_latlon_dims(coldata_tm5_tm5)
    assert isinstance(cd, ColocatedData)
    assert 'station_name' in cd.data.dims

@pytest.mark.parametrize('region_ids,raises', [
    ('blaaa', pytest.raises(ValueError)),
    (['WORLD'], does_not_raise_exception()),
    (['WORLD', 'EUROPE'], does_not_raise_exception()),
    (['WORLD', 'OCN'], does_not_raise_exception()),
    (['WORLD', 'Italy'], pytest.raises(ValueError)),

    ])
def test__prepare_regions_json_helper(region_ids,raises):
    with raises:
        regborders, regs = h._prepare_regions_json_helper(region_ids)
        assert len(region_ids) == len(regborders) == len(regs)
        for regid in region_ids:
            reg = Region(regid)
            name = reg.name
            assert name in regborders and name in regs
            assert regs[name].region_id == regid
            assert regs[name].name == name
            bd = regborders[name]
            assert reg.lat_range == [bd['minLat'], bd['maxLat']]
            assert reg.lon_range == [bd['minLon'], bd['maxLon']]

def test__prepare_default_regions_json():
    regborders, regs = h._prepare_default_regions_json()
    regids = sorted([reg.region_id for reg in regs.values()])
    default = sorted(get_all_default_region_ids())
    assert default == regids

def test__prepare_aerocom_regions_json():
    regborders, regs = h._prepare_aerocom_regions_json()
    regids = sorted([reg.region_id for reg in regs.values()])
    default = sorted(OLD_AEROCOM_REGIONS)
    assert default == regids

def test__prepare_htap_regions_json():
    regborders, regs = h._prepare_htap_regions_json()
    regids = sorted([reg.region_id for reg in regs.values()])
    default = sorted(HTAP_REGIONS_DEFAULT)
    assert default == regids

def test__prepare_country_regions():
    regids = ['Italy', 'Germany']
    regs = h._prepare_country_regions(regids)
    assert isinstance(regs, dict)
    assert len(regs) == len(regids)
    for name, reg in regs.items():
        assert isinstance(reg, Region)
        assert reg.region_id in regids

@pytest.mark.parametrize('regions_how,raises,regnum', [
    ('bla', pytest.raises(ValueError), 0),
    ('default', does_not_raise_exception(),10),
    ('aerocom', does_not_raise_exception(),10),
    ('htap', does_not_raise_exception(),15),
    ('country', does_not_raise_exception(),9),

    ])
def test_init_regions_web(coldata_tm5_aeronet,regions_how,raises,regnum):
    with raises:
        regborders, regs, regnames = h.init_regions_web(coldata_tm5_aeronet,
                                                        regions_how)
        assert len(regnames) == len(regs) == len(regborders) == regnum
        if regions_how == 'country':
            for reg, brdr in regborders.items():
                if not reg == 'WORLD':
                    assert isinstance(brdr, str) # country code

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)