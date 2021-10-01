#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:28:03 2020

@author: jonasg
"""
import pytest
from pyaerocom import const
from pyaerocom.conftest import does_not_raise_exception
from pyaerocom.io.ebas_varinfo import EbasVarInfo
from pyaerocom.io.ebas_file_index import EbasSQLRequest

TESTDATA = [('DEFAULT', None, None, None, None, None, 1),
            ('sc550aer', ['aerosol_light_scattering_coefficient'],
             ['aerosol', 'pm10'], None, None, None, 1.0),
            ('sc440aer', ['aerosol_light_scattering_coefficient'],
             ['aerosol', 'pm10'], None, None, None, 1.0),
            ('sc700aer', ['aerosol_light_scattering_coefficient'],
             ['aerosol', 'pm10'], None, None, None, 1.0),
            ('sc550dryaer', None, None, None, None, ['sc550aer', 'scrh'], 1),
            ('sc440dryaer', None, None, None, None, ['sc440aer', 'scrh'], 1),
            ('sc700dryaer', None, None, None, None, ['sc700aer', 'scrh'], 1),
            ('sc550lt1aer', ['aerosol_light_scattering_coefficient'],
             ['pm25', 'pm1'], None, None, None, 1.0),
            ('bsc550aer', ['aerosol_light_backscattering_coefficient'],
             ['aerosol', 'pm10', 'pm25'], None, None, None, 1.0),
            ('ac550aer', ['aerosol_absorption_coefficient'], ['aerosol', 'pm10'],
             ['filter_absorption_photometer'], None, None, 1.0),
            ('ac550dryaer', None, None, ['filter_absorption_photometer'], None,
             ['ac550aer', 'acrh'], 1),
            ('ac550lt1aer', ['aerosol_absorption_coefficient'], ['pm25', 'pm1'],
             ['filter_absorption_photometer'], None, None, 1.0),
            ('bsc550dryaer', ['aerosol_light_backscattering_coefficient'],
             ['pm10', 'pm25', 'pm1', 'aerosol'], ['nephelometer'], None, None, 1.0),
            ('scrh', ['relative_humidity'], ['instrument', 'aerosol', 'met', 'pm10', 'pm25', 'pm1'],
             None, None, None, 1),
            ('acrh', ['relative_humidity'],
             ['instrument', 'aerosol', 'met', 'pm10', 'pm25', 'pm1'],
             None, None, None, 1),
            ('concso4', ['sulphate_corrected', 'sulphate_total'],
             ['aerosol', 'pm10', 'pm25'], None, None, None, 1),
            ('concso2', ['sulphur_dioxide'], ['air'], None, None, None, 1.0),
            ('concpm10', ['pm10_mass'], ['pm10'], None, None, None, 1.0),
            ('concpm25', ['pm25_mass'], ['pm25'], None, None, None, 1.0),
            ('concso4t', ['sulphate_total'], ['aerosol', 'pm10', 'pm25'], None, None,
             None, 1.0),
            ('concso4c', ['sulphate_corrected'], ['aerosol', 'pm10', 'pm25'], None,
             None, None, 1.0),
            ('concbc', ['elemental_carbon'], ['pm25', 'pm10', 'pm1', 'aerosol'],
             ['denuder', 'ecoc_monitor', 'filter_1pack', 'filter_2pack',
              'high_vol_sampler', 'impactor', 'low_vol_sampler',
              'lvs_denuder_single', 'lvs_denuder_tandem',
              'lvs_QBQ', 'lvs_single', 'lvs_single_twin', 'lvs_teflon'],
             None, None, 1.0),
            ('conceqbc', ['equivalent_black_carbon'],
             ['aerosol', 'pm1', 'pm10', 'pm25'],
             ['filter_absorption_photometer'], None, None, 1),
            ('conctc', ['total_carbon'],
             ['pm25', 'pm10','aerosol'], None, None, None, 1.0),
            ('concoa', ['organic_carbon'], ['pm25', 'pm10', 'aerosol', 'pm1'],
             None, None, None, 1.4),
            ('concoc', ['organic_carbon'], ['pm25', 'pm10', 'aerosol', 'pm1'],
             None, None, None, 1),
            ('concss', ['sodium'], ['pm10', 'aerosol', 'pm25', 'pm1', 'air'],
             None, None, None, 3.27),
            ('concnh3', ['ammonia'], ['air'], None, None, None, 1.0),
            ('concno3', ['nitrate'], ['pm10','aerosol','pm25'],
             None, None, None, 1.0),
            ('concnh4', ['ammonium'], ['pm10','aerosol','pm25'],
             None, None, None, 1.0),
            ('concNhno3', ['nitric_acid'], ['air'], None, None, None, 1.0),
            ('concNtno3', ['sum_nitric_acid_and_nitrate'], ['air+aerosol'],
             None, None, None, 1.0),
            ('concno2', ['nitrogen_dioxide'], ['air'], None, None, None, 1.0),
            ('conco3', ['ozone'], ['air'], None, None, None, 1),
            ('concco', ['carbon_monoxide'], ['air'], None, None, None, 1.0),
            ('concprcpoxs', ['sulphate_corrected', 'sulphate_total'],
             ['precip'], None, None, None, 1.0),
            ('concprcpoxn', ['nitrate'], ['precip'], None, None, None, 1.0),
            ('concprcprdn', ['ammonium'], ['precip'], None, None, None, 1.0),
            ('wetoxs', None, None, None, None, ['concprcpoxs'], 1),
            ('wetoxn', None, None, None, None, ['concprcpoxn'], 1),
            ('wetrdn', None, None, None, None, ['concprcprdn'], 1),
            ('pr', ['precipitation_amount_off', 'precipitation_amount'],
             ['precip'], None, None, None, 1.0)
            ]

def test_init_empty():
    try:
        EbasVarInfo()
    except Exception as e:
        assert type(e)==TypeError

def test_open_config():
    from configparser import ConfigParser
    assert isinstance(EbasVarInfo.open_config(), ConfigParser)

def test_var_name_aerocom():
    assert EbasVarInfo('sconcno3').var_name_aerocom == 'concno3'

@pytest.mark.parametrize(('var_name, component, matrix, instrument, '
                          'statistics, requires, scale_factor'), TESTDATA)
def test_varinfo(var_name, component, matrix, instrument, statistics,
                 requires, scale_factor):

    var = EbasVarInfo(var_name)

    assert var.component == component
    assert var.matrix == matrix
    assert var.instrument == instrument
    assert var.statistics == statistics
    assert var.requires == requires
    assert var.scale_factor == scale_factor

def test_to_dict():
    info = EbasVarInfo('concpm10')
    dic = info.to_dict()
    assert isinstance(dic, dict)
    for key, val in dic.items():
        assert getattr(info, key) == val

@pytest.mark.parametrize('var,constraints,raises', [
    (None, {}, pytest.raises(AttributeError)),
    ('sc700dryaer', {}, pytest.raises(ValueError)),
    ('sc550dryaer', {}, pytest.raises(ValueError)),
    ('concpm10', {}, does_not_raise_exception()),
    ('concpm10', {'bla': 42}, does_not_raise_exception()),
    # ToDo: the following example should actually be checked and maybe raise an Exception already here
    # (i.e. start_date is a valid constraint but 42 is not allowed as input)
    ('concpm10', {'start_date': 42}, does_not_raise_exception()),

    ])
def test_make_sql_request(var,constraints,raises):
    if var is None:
        info = EbasVarInfo('concpm10')
        info.component = None
    else:
        info = EbasVarInfo(var)
    with raises:
        req = info.make_sql_request(**constraints)
        from pyaerocom.io import EbasSQLRequest
        assert isinstance(req, EbasSQLRequest)

@pytest.mark.parametrize('var,constraints,raises,num', [
    ('concpm10', {}, does_not_raise_exception(), 1),
    ('sc700dryaer', {}, does_not_raise_exception(), 2),
    ('sc550dryaer', {}, does_not_raise_exception(), 2),
    ('sc440dryaer', {}, does_not_raise_exception(), 2),
    ])
def test_make_sql_requests(var,constraints,raises,num):
    info = EbasVarInfo(var)
    with raises:
        reqs = info.make_sql_requests(**constraints)
        assert isinstance(reqs, dict)
        assert len(reqs) == num
        for key, req in reqs.items():
            assert isinstance(req, EbasSQLRequest)

def test___str__():
    s = EbasVarInfo('concpm10').__str__()
    assert isinstance(s, str)

if __name__=='__main__':

    #info = EbasVarInfo()
    def to_tuple(var_name):
        var = EbasVarInfo(var_name)
        return (var_name, var.component, var.matrix, var.instrument,
                var.statistics, var.requires, var.scale_factor)
    from time import time
    import sys
    t0 =time()
    pytest.main(sys.argv)
    print(time()-t0)

    ok = []
    notok = []
    for var in EbasVarInfo.open_config():
        if var in const.VARS:
            ok.append(var)
        else:
            notok.append(var)

    print('OK')
    print(ok)

    print()
    print('NOT OK')
    print(notok)
