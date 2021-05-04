#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 09:31:15 2021

@author: jonasg
"""
import numpy as np
import numpy.testing as npt
import os
import pandas as pd
import pytest
from pyaerocom.conftest import does_not_raise_exception
from pyaerocom.exceptions import DataRetrievalError
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.io.read_airnow import ReadAirNow

@pytest.fixture(scope='module')
def reader():
    return ReadAirNow('AirNowSubset')

class TestReadAirNow(object):

    _FILETYPE = '.dat'

    # to recursively retrieve list of data files
    _FILEMASK = f'/**/*{_FILETYPE}'

    #: version log of this class (for caching)
    __version__ = '0.07'

    #: column delimiter
    FILE_COL_DELIM = '|'

    #: columns in data files
    FILE_COL_NAMES = ['date','time', 'station_id',
                      'station_name', 'time_zone',
                      'variable', 'unit', 'value',
                      'institute']

    #: mapping of columns in station metadata file to pyaerocom standard
    STATION_META_MAP = {
           'aqsid': 'station_id', 'name': 'station_name', 'lat': 'latitude',
           'lon': 'longitude', 'elevation': 'altitude', 'city': 'city',
           'address': 'address', 'timezone': 'timezone',
           'environment': 'area_classification',
           'populationclass': 'station_classification',
           'modificationdate': 'modificationdate', 'comment': 'comment'
            }

    STATION_META_DTYPES = {
            'station_id'            : str,
            'station_name'          : str,
            'latitude'              : float,
            'longitude'             : float,
            'altitude'              : float,
            'city'                  : str,
            'address'               : str,
            'timezone'              : str,
            'area_classification'   : str,
            'modificationdate'      : str,
            'station_classification': str,
            'comment'               : str
            }

    REPLACE_STATNAME = {'&' : 'and',
                        '/' : ' ',
                        ':' : ' ',
                        '.' : ' ',
                        "'" : ''}

    #: Years in timestamps in the files are are 2-digit (e.g. 20 for 2020)
    BASEYEAR = 2000

    #: Name of dataset (OBS_ID)
    DATA_ID = 'AirNow' #'GAWTADsubsetAasEtAl'

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID, 'AirNowSubset']

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
        'concpm10'  : 'PM10',
        'concpm25'  : 'PM2.5',
        'vmrco'    : 'CO',
        'vmrnh3'   : 'NH3',
        'vmrno'    : 'NO',
        'vmrno2'   : 'NO2',
        'vmrnox'   : 'NOX',
        'vmrnoy'   : 'NOY',
        'vmro3'    : 'OZONE',
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

    FILE_NAMES = ['2020010101.dat', '2020010102.dat', '2020010107.dat']

    META_COLNAMES = ['aqsid', 'name', 'lat', 'lon', 'elevation', 'city', 'address',
       'position', 'timezone', 'environment', 'modificationdate',
       'populationclass', 'comment']

    def test__FILETYPE(self, reader):
        assert reader._FILETYPE == self._FILETYPE

    def test__FILEMASK(self, reader):
        assert reader._FILEMASK == self._FILEMASK

    def test__version__(self, reader):
        assert reader.__version__ == self.__version__

    def test_FILE_COL_DELIM(self, reader):
        assert reader.FILE_COL_DELIM == self.FILE_COL_DELIM

    def test_FILE_COL_NAMES(self, reader):
        assert sorted(reader.FILE_COL_NAMES) == sorted(self.FILE_COL_NAMES)

    @staticmethod
    def _test_dict(dic1, dic2):
        assert len(dic1) == len(dic2)
        for key, val in dic1.items():
            assert key in dic2
            assert dic2[key] == val

    def test_STATION_META_MAP(self, reader):
        self._test_dict(self.STATION_META_MAP, reader.STATION_META_MAP)

    def test_STATION_META_DTYPES(self, reader):
        self._test_dict(self.STATION_META_DTYPES, reader.STATION_META_DTYPES)

    def test_REPLACE_STATNAME(self, reader):
        self._test_dict(self.REPLACE_STATNAME, reader.REPLACE_STATNAME)

    def test_BASEYEAR(self, reader):
        assert reader.BASEYEAR == self.BASEYEAR

    def test_DATA_ID(self, reader):
        assert reader.DATA_ID == self.DATA_ID

    def test_SUPPORTED_DATASETS(self, reader):
        assert reader.SUPPORTED_DATASETS == self.SUPPORTED_DATASETS

    def test_UNIT_MAP(self, reader):
        self._test_dict(self.UNIT_MAP, reader.UNIT_MAP)

    def test_VAR_MAP(self, reader):
        self._test_dict(self.VAR_MAP, reader.VAR_MAP)

    def test_PROVIDES_VARIABLES(self, reader):
        assert reader.PROVIDES_VARIABLES == self.PROVIDES_VARIABLES

    def test_DEFAULT_VARS(self, reader):
        assert reader.DEFAULT_VARS == self.DEFAULT_VARS

    def test_TSTYPE(self, reader):
        assert reader.TS_TYPE == self.TS_TYPE

    def test_STAT_META_FILENAME(self, reader):
        assert self.STAT_METADATA_FILENAME == reader.STAT_METADATA_FILENAME

    def test__date_time_str_to_datetime64(self, reader):
        dt = reader._date_time_str_to_datetime64('10/23/20', '13:55')

        assert isinstance(dt, np.datetime64)
        assert dt.dtype == 'datetime64[s]'
        assert str(dt) == '2020-10-23T13:55:00'

    def test__datetime64_from_filename(self, reader):
        fname = self.FILE_NAMES[0]
        dt = reader._datetime64_from_filename(fname)
        assert isinstance(dt, np.datetime64)
        assert dt.dtype == 'datetime64[s]'
        assert str(dt) == '2020-01-01T01:00:00'

    def test__read_metadata_file(self, reader):
        cfg = reader._read_metadata_file()
        assert isinstance(cfg, pd.DataFrame)
        colnames = list(cfg.columns.values)
        assert colnames == self.META_COLNAMES
        assert cfg.values.shape == (2588, 13)

    def test__correct_station_name(self, reader):
        fakename = "Bla/blub.bla'blub:blaa & blub"
        corr = reader._correct_station_name(fakename)
        assert corr == "Bla blub blablub blaa and blub"

    def _test_station_meta(self, stat, **testargs):
        for key, val in testargs.items():
            assert key in stat, key
            if isinstance(val, float):
                npt.assert_allclose(stat[key], val, rtol=1e-3)
            else:
                assert stat[key] == val, (stat[key], val)

    def test__init_station_metadata(self, reader):
        statlist = reader._init_station_metadata()
        assert(len(statlist)) == 2588
        assert [isinstance(x, StationData) for x in statlist]
        statids = list(statlist.keys())
        assert statids[0] == '000010101'
        assert statids[1000] == '160550006'
        self._test_station_meta(statlist['000010101'],
                                latitude=47.568,
                                longitude=-52.702,
                                altitude=7,
                                station_name='Duckworth and Ordinance',
                                station_id='000010101')

        self._test_station_meta(statlist['160550006'],
                                latitude=47.682,
                                longitude=-116.766,
                                altitude=665.0,
                                station_name='Coeur D Alene - Teom',
                                station_id='160550006')


    def test_DATASET_PATH_EXISTS(self, reader):
        assert os.path.exists(reader.DATASET_PATH)

    def test_get_file_list(self, reader):
        files = reader.get_file_list()
        assert len(files) == 3
        for fp in files:
            assert os.path.basename(fp) in self.FILE_NAMES
        reader.FILE_LIST = files

    def _file_list(self, reader):
        try:
            return reader.FILE_LIST
        except AttributeError:
            reader.FILE_LIST = lst = reader.get_file_list()
            return lst

    def test__read_file(self, reader):
        fp = self._file_list(reader)[0]
        data = reader._read_file(fp)
        assert isinstance(data, pd.DataFrame)
        assert list(data.columns.values) == self.FILE_COL_NAMES
        assert data.values.shape == (14979, 9)

    # This should test all variables available and reads the first 3 data files
    # so for each variable, the StationData objects should contain 3 timestamps
    @pytest.mark.parametrize('vars_to_retrieve,statnum,first_dtime,first_vals,unit,expectation', [

        (['concbc'], 8,
         ['2019-12-31T17:00:00', '2019-12-31T18:00:00', '2019-12-31T23:00:00'],
         [0.92, 1.53, 3.37], 'ug m-3', does_not_raise_exception()),

        (['concpm10'], 196,
         ['2019-12-31T19:00:00', '2019-12-31T20:00:00','2020-01-01T01:00:00'],
         [0.0, 0.0, -1.0], 'ug m-3', does_not_raise_exception()),

        (['concpm25'], 679,
         ['2019-12-31T21:00:00', '2019-12-31T22:00:00', '2020-01-01T03:00:00'],
         [11.0, 12.0, 5.0], 'ug m-3', does_not_raise_exception()),

        (['vmrco'], 115,
         ['2019-12-31T18:00:00', '2019-12-31T19:00:00', '2020-01-01T00:00:00'],
         [0.7, 0.8, 0.6], 'ppm', does_not_raise_exception()),

        #ToDo: revies NH3 (not available in selected 3 test files...)
        (['vmrnh3'], None,None,None, None, pytest.raises(DataRetrievalError)),

        (['vmrno'], 129,
         ['2019-12-31T21:00:00', '2019-12-31T22:00:00', '2020-01-01T03:00:00'],
         [0.0,0.0,0.0], 'ppb', does_not_raise_exception()),

        (['vmrno2'], 187,
         ['2019-12-31T21:00:00', '2019-12-31T22:00:00', '2020-01-01T03:00:00'],
         [0.0,0.0,0.0], 'ppb', does_not_raise_exception()),

        (['vmrnox'], 103,
         ['2019-12-31T17:00:00', '2019-12-31T18:00:00', '2019-12-31T23:00:00'],
         [22.7, 30.9, 31.5], 'ppb', does_not_raise_exception()),

        (['vmrnoy'], 33,
         ['2019-12-31T18:00:00', '2019-12-31T19:00:00', '2020-01-01T00:00:00'],
         [21.6, 28.8, 84.5], 'ppb', does_not_raise_exception()),

        (['vmro3'], 747,
         ['2019-12-31T21:00:00', '2019-12-31T22:00:00', '2020-01-01T03:00:00'],
         [30.0, 25.0, 29.0], 'ppb', does_not_raise_exception()),

        (['vmrso2'], 181,
         ['2019-12-31T21:00:00', '2019-12-31T22:00:00', '2020-01-01T03:00:00'],
         [0.0, 0.0, 0.0], 'ppb', does_not_raise_exception()),

        ])
    def test__read_files_single_var(self, reader, vars_to_retrieve, statnum,
                                    first_dtime, first_vals, unit, expectation):
        if not len(vars_to_retrieve) == 1:
            raise ValueError('invalid input for test, only single variables are supported here')

        lst = self._file_list(reader)

        with expectation:
            data = reader._read_files(lst, vars_to_retrieve)
            assert isinstance(data, list)
            assert len(data) == statnum

            var = vars_to_retrieve[0]
            for stat in data:
                assert isinstance(stat, StationData)
                assert var in stat

            first_stat = data[0]
            first_stat_vals =  first_stat[var]
            # check timeseries data
            assert isinstance(first_stat_vals, np.ndarray)
            assert var in first_stat['var_info']
            assert 'units' in first_stat['var_info'][var]
            assert first_stat['var_info'][var]['units'] == unit

            dtimelist = [str(x) for x in first_stat.dtime]
            assert dtimelist == first_dtime, dtimelist

            assert [x for x in first_stat_vals] == first_vals

    def test_read_file(self, reader):
        with pytest.raises(NotImplementedError):
            reader.read_file()


    @pytest.mark.parametrize('vars_to_retrieve, num_meta_blocks,num_stats', [
        ('concpm10', 196, 196),
        (['concbc', 'concpm10', 'concpm25', 'vmrco', 'vmrno',
          'vmrno2', 'vmrnox', 'vmrnoy', 'vmro3', 'vmrso2'], 2378, 1139)
        ])
    def test_read(self, reader, vars_to_retrieve, num_meta_blocks,
                  num_stats):
        data = reader.read(vars_to_retrieve)
        if isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        assert isinstance(data, UngriddedData)
        assert len(data.metadata) == num_meta_blocks
        assert len(data.unique_station_names) == num_stats
        assert sorted(data.contains_vars) == sorted(vars_to_retrieve)

if __name__ == '__main__':

    import sys
    print(list(ReadAirNow().VAR_MAP.keys()))
    pytest.main(sys.argv)