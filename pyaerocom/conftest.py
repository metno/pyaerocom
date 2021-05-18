#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 15:57:09 2020

@author: jonasg
"""
import matplotlib
matplotlib.use('Agg')
import pytest
import numpy as np

from contextlib import contextmanager

from pyaerocom import const
import pyaerocom._conftest_helpers as cth
import pyaerocom.testdata_access as td
from pyaerocom.griddeddata import GriddedData
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.io import (ReadAasEtal, ReadEbas, ReadAeronetSunV3,
                          ReadAeronetSdaV3)

from pyaerocom.test.synthetic_data import DataAccess
from pyaerocom import __dir__ as PYADIR

INIT_TESTDATA = True
TEST_RTOL = 1e-4

DATA_ACCESS = DataAccess()

# class that provides / ensures access to testdataset
tda = td.TestDataAccess()

TESTDATADIR = tda.testdatadir

# Additional paths that have to exist (for sanity checking)
CHECK_PATHS = {
    'tm5': 'modeldata/TM5-met2010_CTRL-TEST/renamed',
    'tm5aod' : 'modeldata/TM5-met2010_CTRL-TEST/renamed/aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc',
    'emep' : 'modeldata/EMEP_2017',
    'coldata_tm5_aeronet' : 'coldata/od550aer_REF-AeronetSunV3L2Subset.daily_MOD-TM5_AP3-CTRL2016_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc'
    }

TEST_VARS_AERONET = ['od550aer', 'ang4487aer']

EBAS_ISSUE_FILES = {
    # conco3 tower - 3 different measurement heights
    'o3_tower':'CZ0003R.20150101000000.20181107114213.uv_abs.ozone.air.1y.1h..CZ06L_uv_abs.lev2.nas',
    # conco3 - Neg. meas periods
    'o3_neg_dt':'NZ0003G.20090110030000.20181130115605.uv_abs.ozone.air.9h.1h.US06L_Thermo_49C_LAU.US06L_AM.lev2.nas',
    # conco3 - Most common meas period is 150s and does not correspond to any of the supported base frequencies ['minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'native']
    'o3_tstype':'LT0015R.20080101000000.20081231000000.uv_abs.ozone.air.15d.1h.LT01L_uv_abs_15.LT01L_uv_abs..nas',
    # concpm10 - could not resolve unique data column for concpm10 (EBAS varname: ['pm10_mass'])
    'pm10_colsel':'ID1013R.20180101000000.20200102000000.beta_gauge_particulate_sampler.pm10_mass.pm10.1y.1h.ID01L_MetOne_BAM1020..lev2.nas',
    # concpm10 Aliartos - Most common meas period is 172800s and does not correspond to any of the supported base frequencies ['minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'native']
    'pm10_tstype':'GR0001R.20060119000000.20080120000000.b-attenuation.pm10_mass.pm10.11mo.1w.GR01L_b_att_01.GR01L_b-attenuation..nas'
    }



# checks if testdata-minimal is available and if not, tries to download it
# automatically into ~/MyPyaerocom/testdata-minimal

if INIT_TESTDATA:
    TESTDATA_AVAIL = tda.init()
else:
    TESTDATA_AVAIL = False

EBAS_FILES = None
EBAS_FILEDIR = None
if TESTDATA_AVAIL:
    import simplejson
    _ebas_info_file = TESTDATADIR.joinpath('scripts/ebas_files.json')
    assert _ebas_info_file.exists()
    EBAS_FILEDIR = TESTDATADIR.joinpath('obsdata/EBASMultiColumn/data')
    with open(_ebas_info_file, 'r') as f:
        EBAS_FILES = simplejson.load(f)
    for var, sites in EBAS_FILES.items():
        for site, files in sites.items():
            for file in files:
                assert EBAS_FILEDIR.joinpath(file).exists()


# skipif marker that is True if no access to metno PPI is provided
# (some tests are skipped in this case)
lustre_unavail = pytest.mark.skipif(not const.has_access_lustre,
                                    reason='Skipping tests that require access '
                                    'to AEROCOM database on METNo servers')

# custom skipif marker that is used below for test functions that
# require geonum to be installed
geonum_unavail = pytest.mark.skipif(not const.GEONUM_AVAILABLE,
                   reason='Skipping tests that require geonum.')

try:
    import reverse_geocode
    rg_avail = True
except ModuleNotFoundError:
    rg_avail = False

rg_unavail = pytest.mark.skipif(not rg_avail,
                   reason='Skipping tests that require access to reverse_geocode')

etopo1_unavail = pytest.mark.skipif(not const.ETOPO1_AVAILABLE,
                   reason='Skipping tests that require access to ETOPO1 data')

testdata_unavail = pytest.mark.skipif(not TESTDATA_AVAIL,
                    reason='Skipping tests that require testdata-minimal.')

test_not_working = pytest.mark.skip(reason='Method raises Exception')

from pyaerocom import change_verbosity
change_verbosity('critical', const.print_log)
### Fixtures representing data

EMEP_DIR =  str(TESTDATADIR.joinpath(CHECK_PATHS['emep']))

EBAS_SQLite_DB = EBAS_FILEDIR.parent.joinpath('ebas_file_index.sqlite3')

assert EBAS_SQLite_DB.exists()

@pytest.fixture(scope='session')
def path_emep():
    paths = {}
    emep_path= TESTDATADIR.joinpath(CHECK_PATHS['emep'])
    paths['daily'] = str(emep_path.joinpath('Base_day.nc'))
    paths['monthly'] = str(emep_path.joinpath('Base_month.nc'))
    paths['yearly'] = str(emep_path.joinpath('Base_fullrun.nc'))
    paths['data_dir'] = str(emep_path)
    return paths

@pytest.fixture(scope='session')
def data_tm5():
    fpath = tda.testdatadir.joinpath(CHECK_PATHS['tm5aod'])
    if not fpath.exists():
        raise Exception('Unexpected error, please debug')
    data = GriddedData(fpath)
    return data

@pytest.fixture(scope='session')
def coldata_tm5_aeronet():
    fpath = tda.testdatadir.joinpath(CHECK_PATHS['coldata_tm5_aeronet'])
    return cth._load_coldata_tm5_aeronet_from_scratch(fpath)

@pytest.fixture(scope='session')
def coldata_tm5_tm5():
    fpath = tda.testdatadir.joinpath('coldata/od550aer_REF-TM5_AP3-CTRL2016_MOD-TM5_AP3-CTRL2016_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc')
    return cth._load_coldata_tm5_aeronet_from_scratch(fpath)

@pytest.fixture(scope='session')
def aasetal_data():
    reader = ReadAasEtal()
    # that's quite time consuming, so keep it for possible usage in other
    # tests
    return reader.read()  # read all variables

@pytest.fixture(scope='session')
def aeronet_sun_subset_reader():
    reader = ReadAeronetSunV3('AeronetSunV3L2Subset.daily')
    return reader

@pytest.fixture(scope='session')
def aeronet_sda_subset_reader():
    reader = ReadAeronetSdaV3('AeronetSDAV3L2Subset.daily')
    return reader

@pytest.fixture(scope='session')
def aeronetsunv3lev2_subset(aeronet_sun_subset_reader):
    r = aeronet_sun_subset_reader
    #return r.read(vars_to_retrieve=TEST_VARS)
    return r.read(vars_to_retrieve=TEST_VARS_AERONET)

@pytest.fixture(scope='session')
def aeronetsdav3lev2_subset(aeronet_sda_subset_reader):
    r = aeronet_sda_subset_reader
    return r.read(vars_to_retrieve=['od550aer', 'od550lt1aer'])

@pytest.fixture(scope='session')
def data_scat_jungfraujoch():
    r = ReadEbas('EBASSubset')
    return r.read('sc550aer', station_names='Jungfrau*')

@pytest.fixture(scope='session')
def data_scat_jungfraujoch_full():
    r = ReadEbas()
    return r.read('sc550aer', station_names='Jungfrau*')

@pytest.fixture(scope='session')
def loaded_nasa_ames_example():
    if not TESTDATA_AVAIL:
        raise ValueError()
    from pyaerocom.io.ebas_nasa_ames import EbasNasaAmesFile
    fname = EBAS_FILES['sc550dryaer']['Jungfraujoch'][0]
    rpath = f'obsdata/EBASMultiColumn/data/{fname}'
    fp = TESTDATADIR.joinpath(rpath)
    return EbasNasaAmesFile(fp)

@pytest.fixture(scope='session')
def tempdir(tmpdir_factory):
    """Temporary directory for dumping data shared between tests"""
    tmpdir= tmpdir_factory.mktemp('data')
    return tmpdir

@pytest.fixture(scope='session')
def statlist():
    data = {}
    stats = cth.create_fake_stationdata_list()
    data['all'] = stats
    data['od550aer'] = [stat.copy() for stat in stats if stat.has_var('od550aer')]
    pm10sites = [stat.copy() for stat in stats if stat.has_var('concpm10')]
    data['concpm10_X'] = pm10sites
    data['concpm10_X2'] = [stat.copy() for stat in pm10sites[:3]]
    data['concpm10'] = [stat.copy() for stat in pm10sites[:2]]
    return data

@pytest.fixture(scope='session')
def coldata():
    EXAMPLE_FILE = TESTDATADIR.joinpath(CHECK_PATHS['coldata_tm5_aeronet'])
    return {
        'tm5_aeronet'   : ColocatedData(str(EXAMPLE_FILE)),
        'fake_nodims'  : ColocatedData(np.ones((2,1,1))),
        'fake_3d'       : cth._create_fake_coldata_3d(),
        'fake_4d'       : cth._create_fake_coldata_4d(),
        'fake_5d'       : cth._create_fake_coldata_5d(),
        'fake_3d_hr'    : cth._create_fake_coldata_3d_hourly()
        }

@contextmanager
def does_not_raise_exception():
    yield

if __name__=="__main__":
    import sys
    import pyaerocom as pya
