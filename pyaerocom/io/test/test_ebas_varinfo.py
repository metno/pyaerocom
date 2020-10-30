#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:28:03 2020

@author: jonasg
"""
import pytest
from pyaerocom import const
from pyaerocom.io.ebas_varinfo import EbasVarInfo

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
            ('ang4470dryaer', None, None, None, None, ['sc440dryaer', 'sc700dryaer'], 1),
            ('sc550lt1aer', ['aerosol_light_scattering_coefficient'],
             ['pm25', ' pm1'], None, None, None, 1.0),
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
             ['aerosol', 'pm10', 'pm25', 'pm10_pm25'], None, None, None, 1),
            ('concso2', ['sulphur_dioxide'], ['air'], None, None, None, 1.0),
            ('concpm10', ['pm10_mass'], ['pm10'], None, None, None, 1.0),
            ('concpm25', ['pm25_mass'], ['pm25'], None, None, None, 1.0),
            ('concso4t', ['sulphate_total'], ['aerosol', 'pm25'], None, None,
             None, 1.0),
            ('concso4c', ['sulphate_corrected'], ['aerosol', 'pm25'], None,
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
             ['aerosol', 'pm10', ' pm25', ' pm10_pm25'], None, None, None, 1.0),
            ('concoa', ['organic_carbon'], ['aerosol', 'pm25', 'pm10'],
             None, None, None, 1.4),
            ('concoc', ['organic_carbon'], ['aerosol', 'pm25', 'pm10'],
             None, None, None, 1),
            ('concss', ['sodium'], ['pm10', 'aerosol', 'pm25', 'pm1', 'air'],
             None, None, None, 3.27),
            ('concnh3', ['ammonia'], ['air'], None, None, None, 1.0),
            ('concno3', ['nitrate'], ['aerosol', 'pm10', 'pm25', 'air'],
             None, None, None, 1.0),
            ('concnh4', ['ammonium'], ['aerosol', 'pm10', 'pm25', 'air'],
             None, None, None, 1.0),
            ('conchno3', ['nitric_acid'], ['air'], None, None, None, 1.0),
            ('conctno3', ['sum_nitric_acid_and_nitrate'], ['air+aerosol'],
             None, None, None, 1.0),
            ('concno2', ['nitrogen_dioxide'], ['air'], None, None, None, 1.0),
            ('conco3', ['ozone'], ['air'], None, None, None, 1),
            ('concco', ['carbon_monoxide'], ['air'], None, None, None, 1.0),
            ('concprcpso4', ['sulphate_corrected', 'sulphate_total'],
             ['precip'], None, None, None, 1.0),
            ('concprcpso4t', ['sulphate_total'], ['precip'], None, None, None, 1.0),
            ('concprcpso4c', ['sulphate_corrected'], ['precip'], None, None, None, 1.0),
            ('concprcpno3', ['nitrate'], ['precip'], None, None, None, 1.0),
            ('concprcpso4scavenging', ['sulphate_corrected', 'sulphate_total'],
             ['precip'], None, None, None, 1.0),
            ('concprcpnh4', ['ammonium'], ['precip'], None, None, None, 1.0),
            ('wetso4', None, None, None, None, ['CONCPRCP_SO4', 'METEO_PREC'], 0.27397),
            ('wetconcso4', ['sulphate_corrected'], ['precip'], None, None, None, 1.0),
            ('wetso4t', None, None, None, None, ['METEO_PREC', 'CONCPRCP_SO4T'], 0.27397),
            ('wetso4c', None, None, None, None, ['METEO_PREC', 'CONCPRCP_SO4C'], 0.27397),
            ('wetoxn', None, None, None, None, ['METEO_PREC', 'CONCPRCP_NO3'], 0.27397),
            ('wetrdn', None, None, None, None, ['METEO_PREC', 'CONCPRCP_NH4'], 0.27397),
            ('wetnh4', None, None, None, None, ['METEO_PREC', 'CONCPRCP_NH4'], 0.27397),
            ('precip', ['precipitation_amount_off', 'precipitation_amount'],
             ['precip'], None, None, None, 1.0),
            ('wetconcph', ['pH'], ['precip'], None, None, None, 1.0),
            ('wetno3', None, None, None, None, ['METEO_PREC', 'CONCPRCP_NO3'], 0.27397),
            ('scavratioso4', None, None, None, None, ['SCONC_SO4', 'CONCPRCP_SO4_SCAVENGING'], 1.0),
            ('test', ['aerosol_light_backscattering_coefficient'], ['aerosol'], None, None, None, 1.0)]

def test_init_empty():
    try:
        EbasVarInfo()
    except Exception as e:
        assert type(e)==TypeError

def test_open_config():
    from configparser import ConfigParser
    assert isinstance(EbasVarInfo.open_config(), ConfigParser)

def test_var_names_ini():
    pass

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

# =============================================================================
#     TESTDATA = []
#     for var in EbasVarInfo.open_config():
#         TESTDATA.append(to_tuple(var))
#
#     print(TESTDATA)
# =============================================================================
