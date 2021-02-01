#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 09:31:15 2021

@author: jonasg
"""
import pytest
from pyaerocom.io.read_airnow import ReadAirNow

@pytest.fixture(scope='module')
def reader():
    return ReadAirNow('AirNowSubset')

class TestReadAirNow(object):

    _FILETYPE = '.dat'

    # to recursively retrieve list of data files
    _FILEMASK = f'/**/*{_FILETYPE}'

    #: version log of this class (for caching)
    __version__ = '0.2'

    #: column delimiter
    FILE_COL_DELIM = '|'

    #: columns in data files
    FILE_COL_NAMES = ['date','time', 'station_id',
                      'station_name', 'time_zone',
                      'variable', 'unit', 'value',
                      'institute']

    #: mapping of columns in station metadata file to pyaerocom standard
    STATION_META_MAP = {
            'aqsid'             : 'station_id',
            'name'              : 'station_name',
            'lat'               : 'latitude',
            'lon'               : 'longitude',
            'elevation'         : 'altitude',
            'city'              : 'city',
            'address'           : 'address',
            'timezone'          : 'timezone',
            'environment'       : 'environment',
            'modificationdate'  : 'modificationdate',
            'populationclass'   : 'classification',
            'comment'           : 'comment'
            }

    STATION_META_DTYPES = {
            'station_id'        : str,
            'station_name'      : str,
            'latitude'          : float,
            'longitude'         : float,
            'altitude'          : float,
            'city'              : str,
            'address'           : str,
            'timezone'          : str,
            'environment'       : str,
            'modificationdate'  : str,
            'classification'    : str,
            'comment'           : str
            }
    #: Years in timestamps in the files are are 2-digit (e.g. 20 for 2020)
    BASEYEAR = 2000

    #: Name of dataset (OBS_ID)
    DATA_ID = 'AirNow' #'GAWTADsubsetAasEtAl'

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    #: units found in file
    UNIT_MAP = {
        'C' : 'celcius',
        'M/S' : 'm s-1',
        'MILLIBAR' : 'mbar',
        'MM' : 'mm',
        'PERCENT' : '%',
        'PPB' : 'ppb',
        'PPM' : 'ppm',
        'UG/M3' : 'ug m-3',
        'WATTS/M2': 'W m-2'
        }


    VAR_MAP = {
        'concbc'    : 'BC',
        'vmrco'    : 'CO',
        #'concnh3'   : 'NH3',
        #'concno'    : 'NO',
        'vmrno2'   : 'NO2',
        #'concnox'   : 'NOX',
        #'concnoy'   : 'NOY',
        'vmro3'    : 'OZONE',
        'concpm10'  : 'PM10',
        'concpm25'  : 'PM2.5',
        'vmrso2'   : 'SO2',
        }

    #: List of variables that are provided
    PROVIDES_VARIABLES = list(VAR_MAP.keys())

    #: Default variables
    DEFAULT_VARS = PROVIDES_VARIABLES

    #: Frequncy of measurements
    TS_TYPE = 'hourly'

    #: file containing station metadata
    STAT_METADATA_FILENAME = 'allStations_20191224.csv'

if __name__ == '__main__':

    import sys
    pytest.main(sys.argv)