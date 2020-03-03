#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 15:57:09 2020

@author: jonasg
"""
import pytest

from pathlib import Path
import os
import requests
import tarfile

from traceback import format_exc
from pyaerocom import const 
from pyaerocom.griddeddata import GriddedData
from pyaerocom.io import ReadAasEtal
from pyaerocom.io import ReadAeronetSunV3, ReadAeronetSdaV3, ReadAeronetInvV3
from pyaerocom.io import ReadEbas
from pyaerocom.test.synthetic_data import DataAccess

def _download_test_data(basedir=None):
    print("TEMP OUTPUT: DOWNLOADING TESTDATA")
    #raise Exception('Temporarily disabled...')
    if basedir is None:
        basedir = const.OUTPUTDIR
   
    download_loc = Path(basedir).joinpath('{}.tar.gz'.format(const._testdatadirname))
    
    try:
        r = requests.get(_URL_TESTDATA)
        with open(download_loc, 'wb') as f:
            f.write(r.content) 
            
        with tarfile.open(download_loc, 'r:gz') as tar:
            tar.extractall(const.OUTPUTDIR)
            tar.close()
    except Exception:
        const.print_log.warning('Failed to download testdata. Traceback:\n{}'
                                .format(format_exc()))
        return False
    finally:
        if download_loc.exists():
            os.remove(download_loc)
    return True

def _check_access_testdata(basedir, test_paths):
    if isinstance(basedir, str):
        basedir = Path(basedir)
    elif not isinstance(basedir, Path):
        raise ValueError('Invalid input for basedir ({}), need str or Path'
                         .format(type(basedir)))
    if not basedir.exists():
        return False
    
    if not isinstance(test_paths, dict):
        raise ValueError('Invalid input for test_paths, need dict')
    
    for data_id, data_dir in test_paths.items():
        if not basedir.joinpath(data_dir).exists():
            return False
    return True
                
def check_access_testdata(basedir, test_paths):
    if not _check_access_testdata(basedir, test_paths):
        try:
            if _download_test_data(const.OUTPUTDIR):
                if _check_access_testdata(basedir, test_paths):
                    return True
        except Exception:
            pass
        return False
    return True
    
                                  
TEST_RTOL = 1e-4

DATA_ACCESS = DataAccess()

# thats were the testdata can be downloaded from
_URL_TESTDATA = 'https://pyaerocom.met.no/pyaerocom-suppl/testdata-minimal.tar.gz'

# Testdata directory
TESTDATADIR = Path(const._TESTDATADIR)

# Paths to be added to pya.const. All relative to BASEDIR
ADD_PATHS = {
    
    'MODELS'                : 'modeldata/',
    'AeronetSunV3L2Subset'  : 'obsdata/AeronetSunV3Lev2.daily/',
    'AeronetSDAV3L2Subset'  : 'obsdata/AeronetSDAV3Lev2.daily/',
    'AeronetInvV3L2Subset'  : 'obsdata/AeronetInvV3Lev2.daily/',
    'EBASSubset'            : 'obsdata/EBASMultiColumn/'
    
}

# Additional paths that have to exist (for sanity checking)
TEST_PATHS = {
    
    'tm5aod' : 'modeldata/TM5-met2010_CTRL-TEST/renamed/aerocom3_TM5_AP3-CTRL2016_od550aer_Column_2010_monthly.nc'
    
    }
TEST_PATHS.update(ADD_PATHS)



_UNGRIDDED_READERS = {
    'AeronetSunV3L2Subset'  : ReadAeronetSunV3,
    'AeronetSDAV3L2Subset'  : ReadAeronetSdaV3,
    'AeronetInvV3L2Subset'  : ReadAeronetInvV3,
    'EBASSubset'            : ReadEbas
}

def _init_testdata(const):
    for name, relpath in ADD_PATHS.items():
        ddir = str(TESTDATADIR.joinpath(relpath))
        if name in _UNGRIDDED_READERS:
            reader = _UNGRIDDED_READERS[name]
            const.add_ungridded_obs(name, ddir, 
                                    reader=reader,
                                    check_read=True)
        else:
            const.add_data_search_dir(ddir)
    
TEST_VARS_AERONET = ['od550aer', 'ang4487aer']


# checks if testdata-minimal is available and if not, tries to download it 
# automatically into ~/MyPyaerocom/testdata-minimal
TESTDATA_AVAIL = check_access_testdata(TESTDATADIR, TEST_PATHS)

if TESTDATA_AVAIL:
    _init_testdata(const)
    
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

always_skipped = pytest.mark.skipif(True==True, reason='Seek the answer')

testdata_unavail = pytest.mark.skipif(not TESTDATA_AVAIL,
                    reason='Skipping tests that require testdata-minimal.')

test_not_working = pytest.mark.skip(reason='Method raises Exception')

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
def aasetal_data():
    reader = ReadAasEtal()
    # that's quite time consuming, so keep it for possible usage in other 
    # tests
    return reader.read()  # read all variables

@pytest.fixture(scope='session')
def aeronetsunv3lev2_subset():
    r = ReadAeronetSunV3()
    #return r.read(vars_to_retrieve=TEST_VARS)
    return r.read(file_pattern='Tu*', 
                  vars_to_retrieve=TEST_VARS_AERONET)


@pytest.fixture(scope='session')
def data_scat_jungfraujoch():
    r = ReadEbas()
    return r.read('scatc550aer', station_names='Jungfrau*')
    
if __name__=="__main__":
    import sys
    import pyaerocom as pya
    #pytest.main(sys.argv)
    
    
    ddir = '/home/jonasg/MyPyaerocom/testdata-minimal/obsdata/AeronetSunV3Lev2.daily/'
    
    
    const.add_ungridded_obs('AERONETSunSubset', ddir, 
                            reader=pya.io.ReadAeronetSunV3,
                            check_read=True)
    
    data = pya.io.ReadUngridded().read('AERONETSunSubset', 'od550aer')
    data.plot_station_coordinates()