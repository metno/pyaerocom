#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 15:57:09 2020

@author: jonasg
"""
import pytest

from pathlib import Path
from traceback import format_exc
from contextlib import contextmanager

from pyaerocom import const
import pyaerocom._conftest_helpers as cth
from pyaerocom.griddeddata import GriddedData
from pyaerocom.io import ReadAasEtal
from pyaerocom.io import ReadAeronetSunV3, ReadAeronetSdaV3, ReadAeronetInvV3
from pyaerocom.io import ReadEbas
from pyaerocom.test.synthetic_data import DataAccess

INIT_TESTDATA = True
TEST_RTOL = 1e-4

DATA_ACCESS = DataAccess()

# thats were the testdata can be downloaded from
URL_TESTDATA = 'https://pyaerocom.met.no/pyaerocom-suppl/testdata-minimal.tar.gz'

# Testdata directory
TESTDATADIR = Path(const._TESTDATADIR)

AMES_FILE = 'CH0001G.20180101000000.20190520124723.nephelometer..aerosol.1y.1h.CH02L_TSI_3563_JFJ_dry.CH02L_Neph_3563.lev2.nas'
# Paths to be added to pya.const. All relative to BASEDIR
ADD_PATHS = {

    'MODELS'                : 'modeldata',
    'OBSERVATIONS'          : 'obsdata',
    'CONFIG'                : 'config',
    'AeronetSunV3L2Subset.daily'  : 'obsdata/AeronetSunV3Lev2.daily/renamed',
    'AeronetSDAV3L2Subset.daily'  : 'obsdata/AeronetSDAV3Lev2.daily/renamed',
    'AeronetInvV3L2Subset.daily'  : 'obsdata/AeronetInvV3Lev2.daily/renamed',
    'EBASSubset'            : 'obsdata/EBASMultiColumn'

}

# Additional paths that have to exist (for sanity checking)
TEST_PATHS = {
    'tm5': 'modeldata/TM5-met2010_CTRL-TEST/renamed',
    'tm5aod' : 'modeldata/TM5-met2010_CTRL-TEST/renamed/aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc',
    'nasa_ames_sc550aer' : 'obsdata/EBASMultiColumn/data/{}'.format(AMES_FILE),
    'coldata_tm5_aeronet': 'coldata/od550aer_REF-AeronetSunV3Lev2.daily_MOD-TM5_AP3-CTRL2016_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc'

    }
TEST_PATHS.update(ADD_PATHS)

_UNGRIDDED_READERS = {
    'AeronetSunV3L2Subset.daily'  : ReadAeronetSunV3,
    'AeronetSDAV3L2Subset.daily'  : ReadAeronetSdaV3,
    'AeronetInvV3L2Subset.daily'  : ReadAeronetInvV3,
    'EBASSubset'                  : ReadEbas
}

TEST_VARS_AERONET = ['od550aer', 'ang4487aer']

NASA_AMES_FILEPATHS = {
    'scatc_jfj' :  TESTDATADIR.joinpath(TEST_PATHS['nasa_ames_sc550aer'])
    }

# checks if testdata-minimal is available and if not, tries to download it
# automatically into ~/MyPyaerocom/testdata-minimal
if INIT_TESTDATA:
    TESTDATA_AVAIL = cth.check_access_testdata(TESTDATADIR, TEST_PATHS,
                                               URL_TESTDATA)

    if TESTDATA_AVAIL:
        try:
            cth._init_testdata(const, ADD_PATHS, TESTDATADIR,
                               _UNGRIDDED_READERS)
        except Exception:
            raise ValueError('FATAL: Failed to initiate testdata. Traceback:\n'
                             .format(format_exc()))
            TESTDATA_AVAIL = False
else:
    TESTDATA_AVAIL = False
# skipif marker that is True if no access to metno PPI is provided
# (some tests are skipped in this case)
lustre_unavail = pytest.mark.skipif(not const.has_access_lustre,
                                    reason='Skipping tests that require access '
                                    'to AEROCOM database on METNo servers')

# custom skipif marker that is used below for test functions that
# require geonum to be installed
geonum_unavail = pytest.mark.skipif(not const.GEONUM_AVAILABLE,
                   reason='Skipping tests that require geonum.')
etopo1_unavail = pytest.mark.skipif(not const.ETOPO1_AVAILABLE,
                   reason='Skipping tests that require access to ETOPO1 data')

try:
    import reverse_geocode
    rg_avail = True
except ModuleNotFoundError:
    rg_avail = False

rg_unavail = pytest.mark.skipif(not rg_avail,
                   reason='Skipping tests that require access to reverse_geocode')

etopo1_unavail = pytest.mark.skipif(not const.ETOPO1_AVAILABLE,
                   reason='Skipping tests that require access to ETOPO1 data')
always_skipped = pytest.mark.skipif(True==True, reason='Seek the answer')

testdata_unavail = pytest.mark.skipif(not TESTDATA_AVAIL,
                    reason='Skipping tests that require testdata-minimal.')

test_not_working = pytest.mark.skip(reason='Method raises Exception')

from pyaerocom import change_verbosity
change_verbosity('critical', const.print_log)
### Fixtures representing data

# Example GriddedData object (TM5 model)
@pytest.fixture(scope='session')
def data_tm5():
    fpath = TESTDATADIR.joinpath(TEST_PATHS['tm5aod'])
    if not fpath.exists():
        raise Exception('Unexpected error, please debug')
    data = GriddedData(fpath)
    return data

@pytest.fixture(scope='session')
def coldata_tm5_aeronet():
    fpath = TESTDATADIR.joinpath(TEST_PATHS['coldata_tm5_aeronet'])
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
def loaded_nasa_ames_example():
    from pyaerocom.io.ebas_nasa_ames import EbasNasaAmesFile
    #fp = TESTDATADIR.joinpath(TEST_PATHS['nasa_ames_sc550aer'])
    return EbasNasaAmesFile(NASA_AMES_FILEPATHS['scatc_jfj'])

@pytest.fixture(scope='session')
def tempdir(tmpdir_factory):
    """Temporary directory for dumping data shared between tests"""
    tmpdir= tmpdir_factory.mktemp('data')
    return tmpdir

@contextmanager
def does_not_raise_exception():
    yield

if __name__=="__main__":
    import sys
    import pyaerocom as pya

    reader = pya.io.ReadEbas('EBASSubset')

    db = reader.sqlite_database_file
    print(db)
