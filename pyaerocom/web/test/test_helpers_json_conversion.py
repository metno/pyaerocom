import glob
import numpy as np
import os
import pytest
import simplejson

from pyaerocom.conftest import does_not_raise_exception
from pyaerocom import ColocatedData, Region
from pyaerocom.exceptions import AeroValConfigError
from pyaerocom.region_defs import OLD_AEROCOM_REGIONS, HTAP_REGIONS_DEFAULT
from pyaerocom.region import get_all_default_region_ids
from pyaerocom.web import AerocomEvaluation
from pyaerocom.web import helpers_json_conversion as h


@pytest.mark.dependency
def test_get_stationfile_name():
    name = h.get_stationfile_name('bla', 'blub', 'var', 'invalid')
    assert name == 'bla_blub-var_invalid.json'

def test_get_json_mapname():
    obs_name, obs_var, model_name, model_var, vert_code = ('bla', 'ovar', 'blub', 'var', 'invalid')
    name = h.get_json_mapname(obs_name, obs_var, model_name, model_var, vert_code)
    assert name == 'bla-ovar_invalid_blub-var.json'

@pytest.mark.parametrize('ts_data, out_dir, raises', [
    (None,'',pytest.raises(TypeError)),
    ({},'',pytest.raises(KeyError)),
    (dict(station_name='bla',
          obs_name='blub',
          obs_var='ovar',
          vert_code='invalid'),'',pytest.raises(KeyError)),
    (dict(station_name='bla',
          obs_name='blub',
          obs_var='ovar',
          vert_code='invalid'),'/invalid/42/imagine',pytest.raises(KeyError)),
    (dict(station_name='bla',
          obs_name='blub',
          obs_var='ovar',
          vert_code='invalid',
          model_name='whatever'),'/invalid/42/imagine', pytest.raises(FileNotFoundError)),

    # repeat previous to check add entry in existing file
    (dict(station_name='bla',
          obs_name='blub',
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
                                       ts_data['obs_name'],
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

@pytest.mark.parametrize('which,raises,ncd,omc,mmc', [
    ('fake_3d', does_not_raise_exception(), 4, False, False)
    ])
def test__apply_annual_constraint_helper(coldata,which,raises,ncd,omc,mmc):
    cd = coldata[which]
    yearly = cd.resample_time('yearly', inplace=False, colocate_time=False)
    with raises:
        result = h._apply_annual_constraint_helper(cd.copy(), yearly)
        assert isinstance(cd, ColocatedData)
        assert not cd is result # make sure fixture has not been modified, the function applied it directly to the input data
        assert result.shape == cd.shape
        assert result.num_coords_with_data == ncd
        omean_before = np.nanmean(cd.data[0].data)
        mmean_before = np.nanmean(cd.data[1].data)

        omean = np.nanmean(result.data[0].data)
        mmean = np.nanmean(result.data[1].data)

        omean_same = np.allclose(omean, omean_before, rtol=1e-5)
        mmean_same = np.allclose(mmean, mmean_before, rtol=1e-5)

        if omc:
            assert omean_same
        else:
            assert not omean_same
        if mmc:
            assert mmean_same
        else:
            assert not mmean_same

@pytest.mark.parametrize('which,obs_name,model_name,use_weights,'
                         'vert_code,diurnal_only,'
                         'statistics_freqs,statistics_periods,'
                         'regions_how,zeros_to_nan,annual_stats_constrained,'
                         'raises,fnumdirs', [
    ('fake_4d', 'bla','blub',True,'Column',False,
     ['daily','monthly','yearly'],['2010'],None,False,True,
     does_not_raise_exception(),{'ts' : 14,'map' : 1}),

    ('fake_4d', 'bla','blub',False,'Column',False,
     ['monthly'],['2010'],None,False,False,
     does_not_raise_exception(),{'ts' : 16,'map' : 1}),

    ('fake_3d', 'bla','blub',False,'Column',False,
     ['monthly'],['2010'],None,False,False,
     does_not_raise_exception(),{'ts' : 14,'map' : 1}),

    ('fake_3d', 'bla','blub',True,'Column',False,
     ['monthly'],['2010'],None,False,True,
     pytest.raises(AeroValConfigError),None),



    ('tm5_aeronet','bla','blub',False,'Column',False,
     ['monthly'],['2010'],None,False,False,
     does_not_raise_exception(),{'ts' : 18,'map' : 1, 'contour' : 0,
                                 'profiles' : 0, 'hm' : 1, 'scat': 1,
                                 'ts/dw' : 0}),

    ('tm5_aeronet','bla','blub',False,'Column',False,
     ['monthly', 'yearly'],['2010'],None,False,True,
     does_not_raise_exception(),{'ts' : 17,'map' : 1}),

    ])
def test_compute_json_files_from_colocateddata(coldata, tmpdir, which, obs_name,
                                          model_name, use_weights,
                                          vert_code, diurnal_only,
                                          statistics_freqs, statistics_periods,
                                          regions_how, zeros_to_nan,
                                          annual_stats_constrained,raises,
                                          fnumdirs):
    outdir = str(tmpdir)
    proj = 'proj'
    exp = 'exp'
    stp = AerocomEvaluation(proj_id=proj, exp_id=exp,out_basedir=outdir)
    stp.init_json_output_dirs()
    cs = stp.colocation_settings
    out_dirs = stp.out_dirs
    regions_json = stp.regions_file
    cd = coldata[which]

    with raises:
        h.compute_json_files_from_colocateddata(cd,obs_name,model_name,
                                                use_weights,cs,vert_code,
                                                out_dirs,regions_json,
                                                diurnal_only,
                                                statistics_freqs,
                                                statistics_periods,
                                                regions_how,
                                                zeros_to_nan,
                                                annual_stats_constrained)
        outbase = os.path.join(outdir, f'{proj}/{exp}')
        assert os.path.isdir(outbase)
        for subdir, num in fnumdirs.items():
            fp = os.path.join(outbase, subdir)
            assert os.path.isdir(fp)
            files = glob.glob(f'{fp}/*.json')
            assert len(files) == num

if __name__ == '__main__':
    import sys
    pytest.main(sys.argv)