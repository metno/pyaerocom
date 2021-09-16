import os

import pyaerocom
import pyaerocom.exceptions as exc
import pytest
import xarray as xr

from pyaerocom.griddeddata import GriddedData
from pyaerocom.io.read_mscw_ctm import (
    ReadEMEP,
    ReadMscwCtm,
    calc_concNhno3,
    calc_concNnh3,
    calc_concNnh4,
    calc_concNno3pm10,
    calc_concNno3pm25,
    calc_concNtnh,
    calc_conNtno3,
    update_EC_units,
)

from .._conftest_helpers import _create_fake_MSCWCtm_data
from ..conftest import EMEP_DIR, does_not_raise_exception, lustre_unavail, testdata_unavail


if pyaerocom.const._check_access(f'/home/{pyaerocom.const.user}/lustre/'):
    PREFACE = f'/home/{pyaerocom.const.user}/lustre/'
else:
    PREFACE = '/lustre'
TESTPATH_LUSTRE = f'{PREFACE}/storeB/project/fou/kl/emep/ModelRuns/2021_REPORTING/TRENDS/2019/'

VAR_MAP = {'abs550aer': 'AAOD_550nm', 'abs550bc': 'AAOD_EC_550nm', 
           'absc550aer': 'AbsCoeff', 'absc550dryaer': 'AbsCoeff', 
           'ac550aer': 'AbsCoef_surf', 'drybc': 'DDEP_EC_m2Grid', 
           'drydust': 'DDEP_DUST_m2Grid', 'drynh4': 'DDEP_NH4_f_m2Grid', 
           'dryno3': 'DDEP_TNO3_m2Grid', 'dryoa': 'DDEP_OM25_m2Grid', 
           'dryso2': 'DDEP_SO2_m2Grid', 'dryso4': 'DDEP_SO4_m2Grid', 
           'dryss': 'DDEP_SS_m2Grid', 'ec550aer': 'EXT_550nm', 
           'ec550dryaer': 'EXTdry_550nm', 'emidust': 'DUST_flux', 
           'emisnox': 'Emis_mgm2_nox', 'emisox': 'Emis_mgm2_sox', 
           'loadbc': 'COLUMN_EC_kmax', 'loaddust': 'COLUMN_DUST_kmax', 
           'loadnh4': 'COLUMN_NH4_F_kmax', 'loadno3': 'COLUMN_TNO3_kmax', 
           'loadoa': 'COLUMN_OM25_kmax', 'loadso2': 'COLUMN_SO2_kmax', 
           'loadso4': 'COLUMN_SO4_kmax', 'loadss': 'COLUMN_SS_kmax', 
           'mmrbc': 'D3_mmr_EC', 'mmrdust': 'D3_mmr_DUST', 
           'mmrnh4': 'D3_mmr_NH4_F', 'mmrno3': 'D3_mmr_TNO3', 
           'mmroa': 'D3_mmr_OM25', 'mmrso2': 'D3_mmr_SO2', 
           'mmrso4': 'D3_mmr_SO4', 'mmrss': 'D3_mmr_SS', 
           'od350aer': 'AOD_350nm', 'od440aer': 'AOD_440nm', 
           'od550aer': 'AOD_550nm', 'od550bc': 'AOD_EC_550nm', 
           'od550dust': 'AOD_DUST_550nm', 'od550lt1aer': 'AOD_PMFINE_550nm', 
           'od550nh4': 'AOD_NH4_F_550nm', 'od550no3': 'AOD_TNO3_550nm', 
           'od550oa': 'AOD_OC_550nm', 'od550so4': 'AOD_SO4_550nm', 
           'od550ss': 'AOD_SS_550nm', 'od870aer': 'AOD_870nm', 
           'concaeroh2o': 'SURF_PM25water', 'concbcc': 'SURF_ug_ECCOARSE', 
           'concbcf': 'SURF_ug_ECFINE', 'concdust': 'SURF_ug_DUST', 
           'conchno3': 'SURF_ug_HNO3', 'concnh3': 'SURF_ug_NH3', 
           'concnh4': 'SURF_ug_NH4_F', 'concno2': 'SURF_ug_NO2', 
           'concno3c': 'SURF_ug_NO3_C', 'concno3f': 'SURF_ug_NO3_F', 
           'concno': 'SURF_ug_NO', 'conco3': 'SURF_ug_O3', 
           'concoac': 'SURF_ug_PM_OMCOARSE', 'concoaf': 'SURF_ug_PM_OM25', 
           'concpm10': 'SURF_ug_PM10_rh50', 'concpm25': 'SURF_ug_PM25_rh50', 
           'concrdn': 'SURF_ugN_RDN', 'concso2': 'SURF_ug_SO2', 
           'concso4': 'SURF_ug_SO4', 'concss': 'SURF_ug_SS', 
           'concsspm25': 'SURF_ug_SEASALT_F', 
           'concCocpm25': 'SURF_ugC_PM_OM25', 'vmro32m': 'SURF_2MO3', 
           'vmro3max': 'SURF_MAXO3', 'vmro3': 'SURF_ppb_O3', 
           'vmrco': 'SURF_ppb_CO', 'vmrc2h6': 'SURF_ppb_C2H6', 
           'vmrc2h4': 'SURF_ppb_C2H4', 'vmrhcho': 'SURF_ppb_HCHO', 
           'vmrglyoxal': 'SURF_ppb_GLYOX', 'vmrisop': 'SURF_ppb_C5H8', 
           'wetbc': 'WDEP_EC', 'wetdust': 'WDEP_DUST', 'wetnh4': 'WDEP_NH4_f', 
           'wetno3': 'WDEP_TNO3', 'wetoa': 'WDEP_OM25', 'wetoxn': 'WDEP_OXN', 
           'wetrdn': 'WDEP_RDN', 'wetso2': 'WDEP_SO2', 'wetso4': 'WDEP_SO4', 
           'wetoxs': 'WDEP_SOX', 'wetss': 'WDEP_SS', 'z3d': 'Z_MID', 
           'pr': 'WDEP_PREC', 'concecpm25':'SURF_ug_ECFINE',
           'concssc': 'SURF_ug_SEASALT_C','dryoxn': 'DDEP_OXN_m2Grid',
           'dryoxs': 'DDEP_SOX_m2Grid','dryrdn': 'DDEP_RDN_m2Grid'}


def test_calc_concNhno3():
    
    conchno3 = _create_fake_MSCWCtm_data()
    
    concNhno3_from_func = calc_concNhno3(conchno3)
        
    M_N = 14.006
    M_O = 15.999
    M_H = 1.007
    
    concNhno3 = conchno3*(M_N / (M_H + M_N + M_O * 3))
    concNhno3.attrs['units'] = 'ug N m-3'
    xr.testing.assert_allclose(concNhno3, concNhno3_from_func)

def test_calc_concNno3pm10():
    
    concno3c = _create_fake_MSCWCtm_data()
    concno3f = _create_fake_MSCWCtm_data()
    
    concNno3pm10_from_func = calc_concNno3pm10(concno3f,concno3c)
    
    M_N = 14.006
    M_O = 15.999
    M_H = 1.007
    
    fac = M_N / (M_N + 3*M_O)
    concno3pm10 = concno3f + concno3c
    concNno3pm10 = concno3pm10*fac
    concNno3pm10.attrs['var_name'] = 'concNno3pm10'
    concNno3pm10.attrs['units'] = 'ug N m-3'
    xr.testing.assert_allclose(concNno3pm10,concNno3pm10_from_func)
    
def test_calc_concNno3pm25():
    
    concno3c = _create_fake_MSCWCtm_data()
    concno3f = _create_fake_MSCWCtm_data()
    
    concNno3pm10_from_func = calc_concNno3pm25(concno3f,concno3c)
    
    M_N = 14.006
    M_O = 15.999
    M_H = 1.007
    
    fac = M_N / (M_N + 3*M_O)
    concno3pm10 = concno3f + 0.134*concno3c
    concNno3pm10 = concno3pm10*fac
    concNno3pm10.attrs['var_name'] = 'concNno3pm10'
    concNno3pm10.attrs['units'] = 'ug N m-3'
    xr.testing.assert_allclose(concNno3pm10,concNno3pm10_from_func)
    
def test_calc_conNtno3():
    
    conchno3 = _create_fake_MSCWCtm_data()
    concno3f = _create_fake_MSCWCtm_data()
    concno3c = _create_fake_MSCWCtm_data()
    
    concNtno3_from_func = calc_conNtno3(conchno3,concno3f,concno3c)
    
    concNhno3 = calc_concNhno3(conchno3)
    concNno3pm10 = calc_concNno3pm10(concno3f,concno3c)
    
    concNtno3 = concNhno3 + concNno3pm10
    concNtno3.attrs['units'] = 'ug N m-3'
    xr.testing.assert_allclose(concNtno3,concNtno3_from_func)
    
def test_calc_concNtnh():
    concnh3 = _create_fake_MSCWCtm_data()
    concnh4 = _create_fake_MSCWCtm_data()
    
    concNtnh_from_func = calc_concNtnh(concnh3,concnh4)
    
    concNnh3 = calc_concNnh3(concnh3)
    concNnh4 = calc_concNnh4(concnh4)
    
    concNtnh = concNnh3 + concNnh4
    concNtnh.attrs['units'] = 'ug N m-3'
    xr.testing.assert_allclose(concNtnh, concNtnh_from_func)

def test_calc_concNnh3():
    concnh3 = _create_fake_MSCWCtm_data()
    
    concNnh3_from_func = calc_concNnh3(concnh3)
    
    M_N = 14.006
    M_O = 15.999
    M_H = 1.007
        
    concNnh3 = concnh3*(M_N / (M_H * 3 + M_N))
    concNnh3.attrs['units'] = 'ug N m-3'
    xr.testing.assert_allclose(concNnh3, concNnh3_from_func)
     

def test_calc_concNnh4():
    concnh4 = _create_fake_MSCWCtm_data()
    
    concNnh4_from_func = calc_concNnh4(concnh4)
    
    M_N = 14.006
    M_O = 15.999
    M_H = 1.007
        
    concNnh4 = concnh4*(M_N / (M_H * 4 + M_N))
    concNnh4.attrs['units'] = 'ug N m-3'
    xr.testing.assert_allclose(concNnh4, concNnh4_from_func)

    
def test_update_EC_units():
    
    concecpm25 = _create_fake_MSCWCtm_data()
    
    concCecpm25_from_func = update_EC_units(concecpm25)
    
    concCecpm25 = concecpm25
    concCecpm25.attrs['units'] = 'ug C m-3'
    
    xr.testing.assert_allclose(concCecpm25, concCecpm25_from_func)
    assert concCecpm25.units == concCecpm25_from_func.units

@pytest.fixture(scope='module')
def reader():
    return ReadMscwCtm()

@pytest.mark.parametrize('filepath,data_id,data_dir,check,raises', [

    (EMEP_DIR+'/Base_month.nc',None,None,{
        'data_id'  : 'EMEP_2017',
        'data_dir' : EMEP_DIR},
        does_not_raise_exception()),

    (None,None,None, {'_data_dir' : None,'_filename' : 'Base_day.nc',
                      '_filedata': None, '_file_mask' : None,
                      '_files'    : None},
        does_not_raise_exception()),
    ('blaaa',None,None,{},pytest.raises(FileNotFoundError)),
    (EMEP_DIR,None,None,{},pytest.raises(ValueError)),
    (None,None,'blaaaa',{},pytest.raises(FileNotFoundError) ),
    (None,None,EMEP_DIR+'/Base_month.nc',{},pytest.raises(ValueError)),


    ])
def test_ReadMscwCtm__init__(filepath, data_id, data_dir,check,raises):
    with raises:
        reader = ReadMscwCtm(filepath, data_id, data_dir)
        for key, val in check.items():
            _val = getattr(reader, key)
            assert val == _val

@pytest.mark.parametrize('value, raises', [
    (EMEP_DIR, does_not_raise_exception()),
    (None, pytest.raises(TypeError)),
    ('', pytest.raises(FileNotFoundError))
    ])
def test_ReadMscwCtm_data_dir(value, raises):
    reader = ReadMscwCtm()
    with raises:
        reader.data_dir = value
        assert os.path.samefile(reader.data_dir, value)

@pytest.mark.parametrize('value, raises', [
    ('', does_not_raise_exception()),
    (None, pytest.raises(ValueError)),
    ])
def test_ReadMscwCtm_filename(value, raises):
    reader = ReadMscwCtm()
    with raises:
        reader.filename = value
        assert reader.filename == value

@pytest.mark.parametrize('value, raises, fmask, num_matches', [
    (EMEP_DIR, does_not_raise_exception(), 'Base_*.nc', 3),
    ('/tmp', pytest.raises(FileNotFoundError), '', 0)
    ])
def test__ReadMscwCtm__check_files_in_data_dir(value, raises, fmask, num_matches):
    reader = ReadMscwCtm()
    with raises:
        mask, matches = reader._check_files_in_data_dir(value)
        assert mask == fmask
        assert len(matches) == num_matches

def test_ReadMscwCtm_ts_type():
    reader = ReadMscwCtm()
    assert reader.ts_type == 'daily'

def test_ReadMscwCtm_var_map():
    var_map = ReadMscwCtm().var_map
    assert isinstance(var_map, dict)
    assert var_map == VAR_MAP

@testdata_unavail
@pytest.mark.parametrize('var_name, ts_type, raises', [
    ('blaaa', 'daily', pytest.raises(exc.VariableDefinitionError)),
    ('od550gt1aer', 'daily', pytest.raises(exc.VarNotAvailableError)),
    ('vmro3', 'daily', does_not_raise_exception()),
    ('vmro3', None, does_not_raise_exception()),
    ('concpmgt25', 'daily', does_not_raise_exception())
    ])
def test_ReadMscwCtm_read_var(path_emep,var_name,ts_type,raises):
    r = ReadMscwCtm(data_dir=path_emep['data_dir'])
    with raises:
        data = r.read_var(var_name, ts_type)
        assert isinstance(data, GriddedData)
        if ts_type is not None:
            assert data.ts_type == ts_type
        assert data.ts_type is not None
        assert data.ts_type == r.ts_type

@testdata_unavail
@pytest.mark.parametrize('var_name, ts_type, raises', [
    ('blaaa', 'daily', pytest.raises(KeyError)),
    ('concpmgt25', 'daily', does_not_raise_exception()),
    ('concpmgt25', 'monthly', does_not_raise_exception()),
    ])
def test_ReadMscwCtm__compute_var(path_emep,var_name,ts_type,raises):
    r = ReadMscwCtm(data_dir=path_emep['data_dir'])
    with raises:
        data = r._compute_var(var_name, ts_type)
        assert isinstance(data, xr.DataArray)
 
@lustre_unavail
@pytest.mark.parametrize('path,var_name, ts_type, raises', [
    (TESTPATH_LUSTRE,'concNhno3', 'monthly', does_not_raise_exception()),
    (TESTPATH_LUSTRE,'concNtno3', 'monthly', does_not_raise_exception()),
    (TESTPATH_LUSTRE,'concNtnh', 'monthly', does_not_raise_exception()),
    (TESTPATH_LUSTRE,'concNnh3', 'monthly', does_not_raise_exception()),
    (TESTPATH_LUSTRE,'concNnh4', 'monthly', does_not_raise_exception()),
    (TESTPATH_LUSTRE,'concNhno3', 'monthly', does_not_raise_exception()),
    (TESTPATH_LUSTRE,'concNno3pm10', 'monthly', does_not_raise_exception()),
    (TESTPATH_LUSTRE,'concNno3pm25', 'monthly', does_not_raise_exception()),
    (TESTPATH_LUSTRE,'concsspm10', 'monthly', does_not_raise_exception()),
    (TESTPATH_LUSTRE,'concCecpm25', 'monthly', does_not_raise_exception()),
    ])        
def test_ReadMscwCtm__compute_var_v2(path,var_name,ts_type,raises):
    r = ReadMscwCtm(filepath=f'{path}/Base_month.nc')
    ts_type  = 'monthly'
    with raises:
        data = r._compute_var(var_name,ts_type)
        assert isinstance(data, xr.DataArray)
        

@testdata_unavail
def test_ReadMscwCtm_data(path_emep):
    path = path_emep['daily']
    r = ReadMscwCtm(filepath=path)

    vars_provided = r.vars_provided
    assert isinstance(vars_provided, list)
    assert 'vmro3' in vars_provided

    data = r.read_var('vmro3', ts_type='daily')
    assert isinstance(data, GriddedData)
    assert data.time.long_name == 'time'
    assert data.time.standard_name == 'time'
    assert data.ts_type=='daily'

    data = r.read_var('vmro3')
    assert isinstance(data, GriddedData)
    assert data.time.long_name == 'time'
    assert data.time.standard_name == 'time'
    assert data.ts_type=='daily'


@testdata_unavail
def test_ReadMscwCtm_directory(path_emep):
    data_dir = path_emep['data_dir']
    r = ReadMscwCtm(data_dir=data_dir)
    assert r.data_dir == data_dir
    vars_provided = r.vars_provided
    assert 'vmro3' in vars_provided
    assert 'concpm10' in vars_provided
    assert 'concno2' in vars_provided
    paths = r._files
    assert len(paths) == 3

@pytest.mark.parametrize('files, ts_types, raises', [
    ([],[], pytest.raises(AttributeError)),
    (['Base_hour.nc','test.nc','Base_month.nc', 'Base_day.nc', 'Base_fullrun.nc'],
     ['hourly','monthly','daily','yearly'], does_not_raise_exception())
])
def test_ReadMscwCtm_ts_types(files, ts_types, raises, tmpdir):
    ddir = None
    for filename in files:
        open(os.path.join(tmpdir, filename), 'w').close()
        ddir = str(tmpdir)
    with raises:
        r = ReadMscwCtm(data_dir=ddir)
        assert sorted(r.ts_types) == sorted(ts_types)

@pytest.mark.parametrize('filename,ts_type, raises', [
    ('Base_hour.nc', 'hourly', does_not_raise_exception()),
    ('Base_month.nc', 'monthly', does_not_raise_exception()),
    ('Base_day.nc', 'daily', does_not_raise_exception()),
    ('Base_fullrun', 'yearly', does_not_raise_exception()),
    ('blaaa', 'yearly', pytest.raises(ValueError)),
    ])
def test_ReadMscwCtm_ts_type_from_filename(reader, filename, ts_type, raises):
    with raises:
        assert reader.ts_type_from_filename(filename) == ts_type

@pytest.mark.parametrize('filename,ts_type, raises', [
    ('Base_hour.nc', 'hourly', does_not_raise_exception()),
    ('Base_month.nc', 'monthly', does_not_raise_exception()),
    ('Base_day.nc', 'daily', does_not_raise_exception()),
    ('Base_fullrun.nc', 'yearly', does_not_raise_exception()),
    ('', 'blaaa', pytest.raises(ValueError)),
    ])
def test_ReadMscwCtm_filename_from_ts_type(reader, filename, ts_type, raises):
    reader._file_mask = reader.FILE_MASKS[0]
    with raises:
        assert reader.filename_from_ts_type(ts_type) == filename

def test_ReadMscwCtm_years_avail(path_emep):
    data_dir = path_emep['data_dir']
    r = ReadMscwCtm(data_dir=data_dir)
    assert r.years_avail == [2017]

def test_ReadMscwCtm_preprocess_units():
    units = ''
    prefix = 'AOD'
    assert ReadMscwCtm().preprocess_units(units, prefix) == '1'

def test_ReadMscwCtm_open_file(path_emep):
    reader = ReadMscwCtm()
    with pytest.raises(AttributeError):
        reader.open_file()
    reader.data_dir = path_emep['data_dir']
    data = reader.open_file()
    assert isinstance(data, xr.Dataset)
    assert reader._filedata is data

@pytest.mark.parametrize('var_name, value, raises',[
    ('od550gt1aer', False, does_not_raise_exception()),
    ('absc550aer', True, does_not_raise_exception()),
    ('concpm10', True, does_not_raise_exception()),
    ('sconcpm10', True, does_not_raise_exception()),
    ('blaaa', True, pytest.raises(exc.VariableDefinitionError)),
    ])
def test_ReadMscwCtm_has_var(reader, var_name, value, raises):
    with raises:
        assert reader.has_var(var_name) == value

@pytest.mark.parametrize('value, raises',[
    (None, pytest.raises(TypeError)),
    ('', pytest.raises(FileNotFoundError)),
    ('/tmp', pytest.raises(FileNotFoundError)),
    (EMEP_DIR, pytest.raises(FileNotFoundError)),
    (EMEP_DIR + '/Base_month.nc', does_not_raise_exception())

    ])
def test_ReadMscwCtm_filepath(reader, value, raises):
    with raises:
        reader.filepath = value
        assert os.path.samefile(reader.filepath, value)

def test_ReadMscwCtm__str__():
    assert str(ReadMscwCtm()) == 'ReadMscwCtm'

def test_ReadMscwCtm__repr__():
    assert repr(ReadMscwCtm()) == 'ReadMscwCtm'

def test_ReadEMEP__init__():
    assert isinstance(ReadEMEP(), ReadMscwCtm)

if __name__ == '__main__': # pragma: no cover
    import sys
    pytest.main(sys.argv)