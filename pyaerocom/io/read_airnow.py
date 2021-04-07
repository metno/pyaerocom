#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########################################################################
#
# This python module is part of the pyaerocom software
#
# License: GNU General Public License v3.0
# More information: https://github.com/metno/pyaerocom
# Documentation: https://pyaerocom.readthedocs.io/en/latest/
# Copyright (C) 2017 met.no
# Contact information: Norwegian Meteorological Institute (MET Norway)
#
########################################################################

import os
from glob import glob
import pandas as pd
from tqdm import tqdm
import numpy as np
from pyaerocom import const
from pyaerocom.exceptions import DataRetrievalError
from pyaerocom.io import ReadUngriddedBase
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.stationdata import StationData

class ReadAirNow(ReadUngriddedBase):
    """
    Reading routine for North-American Air Now observations
    """
    # Data type of files
    _FILETYPE = '.dat'

    # File search mask to recursively retrieve list of data files
    _FILEMASK = f'/**/*{_FILETYPE}'

    #: Version log of this class (for caching)
    __version__ = '0.06'

    #: Column delimiter
    FILE_COL_DELIM = '|'

    #: Columns in data files
    FILE_COL_NAMES = ['date','time', 'station_id',
                      'station_name', 'time_zone',
                      'variable', 'unit', 'value',
                      'institute']

    #: Mapping of columns in station metadata file to pyaerocom standard
    STATION_META_MAP = {
            'aqsid'             : 'station_id',
            'name'              : 'station_name',
            'lat'               : 'latitude',
            'lon'               : 'longitude',
            'elevation'         : 'altitude',
            'city'              : 'city',
            'address'           : 'address',
            'timezone'          : 'timezone',
            'environment'       : 'area_classification',
            'populationclass'   : 'station_classification',
            'modificationdate'  : 'modificationdate',
            'comment'           : 'comment'
            }

    #: conversion functions for metadata dtypes
    STATION_META_DTYPES = {
            'station_id'                : str,
            'station_name'              : str,
            'latitude'                  : float,
            'longitude'                 : float,
            'altitude'                  : float,
            'city'                      : str,
            'address'                   : str,
            'timezone'                  : str,
            'area_classification'       : str,
            'station_classification'    : str,
            'modificationdate'          : str,
            'comment'                   : str
            }

    #: strings to be replaced in original station names
    REPLACE_STATNAME = {'&' : 'and',
                        '/' : ' ',
                        ':' : ' ',
                        '.' : ' ',
                        "'" : ''}

    #: Years in timestamps in the files are are 2-digit (e.g. 20 for 2020)
    BASEYEAR = 2000

    #: Name of dataset (OBS_ID)
    DATA_ID = 'AirNow'

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    #: Units found in data files
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

    #: Variable names in data files
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

    def __init__(self, dataset_to_read=None, data_dir=None):
        super(ReadAirNow, self).__init__(dataset_to_read=dataset_to_read,
                                         dataset_path=data_dir)
        self.make_datetime64_array = np.vectorize(self._date_time_str_to_datetime64)

    def _date_time_str_to_datetime64(self, date, time):
        """
        Convert date and time string into datetime64 object

        Parameters
        ----------
        date : str
            date string as mm/dd/yy as in data files
        time : str
            time of the day as HH:MM

        Returns
        -------
        datetime64[s]
        """
        mm, dd, yy = date.split('/')
        HH, MM = time.split(':')
        yr=str(self.BASEYEAR + int(yy))
        # returns as datetime64[s]
        return np.datetime64(f'{yr}-{mm}-{dd}T{HH}:{MM}:00')

    def _datetime64_from_filename(self, filepath):
        """
        Get timestamp from filename

        Note
        ----
        This is not in use at the moment and the timestamps in the file may
        differ within 1h around what the filename suggests. So be careful if
        you want to use this method.

        Parameters
        ----------
        filepath : str
            path of file

        Returns
        -------
        datetime64[s]
        """
        fn = os.path.basename(filepath).split(self._FILETYPE)[0]
        assert len(fn) == 10
        tstr = f'{fn[:4]}-{fn[4:6]}-{fn[6:8]}T{fn[8:10]}:00:00'
        return np.datetime64(tstr)

    def _read_metadata_file(self):
        """
        Read station metadatafile

        Returns
        -------
        cfg : pandas.DataFrame
            metadata dataframe

        """
        fn = os.path.join(self.DATASET_PATH, self.STAT_METADATA_FILENAME)
        cfg = pd.read_csv(fn,sep=',', converters={'aqsid': lambda x: str(x)})
        return cfg

    def _correct_station_name(self, station_name):
        """
        Remove unwanted chars from original station names

        Parameters
        ----------
        station_name : str
            original station name

        Returns
        -------
        str
            station name cleaned of chars defined in :attr:`REPLACE_STATNAME`

        """
        for search, replace in self.REPLACE_STATNAME.items():
            station_name = station_name.replace(search, replace)
        return station_name

    def _init_station_metadata(self):
        """
        Initiate metadata for all stations

        Returns
        -------
        dict
            dictionary with metadata dictionaries for all stations

        """

        cfg = self._read_metadata_file()
        meta_map = self.STATION_META_MAP

        cols = list(cfg.columns.values)
        col_idx = {}
        for from_meta, to_meta in meta_map.items():
            col_idx[to_meta] = cols.index(from_meta)

        arr = cfg.values
        dtypes = self.STATION_META_DTYPES
        stats = {}
        for row in arr:
            stat = {}
            for meta_key, col_num in col_idx.items():
                stat[meta_key] = dtypes[meta_key](row[col_num])
            sid = stat['station_id']

            stat['station_name'] = self._correct_station_name(stat['station_name'])
            stat['data_id'] = self.data_id
            stat['ts_type'] = self.TS_TYPE
            stats[sid] = stat

        return stats

    def get_file_list(self):
        """
        Retrieve list of data files

        Returns
        -------
        list
        """
        basepath = self.DATASET_PATH
        pattern = f'{basepath}{self._FILEMASK}'
        files = sorted(glob(pattern))
        return files

    def _read_file(self, file):
        """
        Read one datafile using :func:`pandas.read_csv`

        Parameters
        ----------
        file : str
            file path

        Returns
        -------
        df : pandas.DataFrame
            DataFrame containing the file data

        """
        df = pd.read_csv(file,sep=self.FILE_COL_DELIM,
                         names=self.FILE_COL_NAMES)
        return df

    def _read_files(self, files, vars_to_retrieve):
        """
        Read input variables from list of files

        Parameters
        ----------
        files : list
            list of data files
        vars_to_retrieve : list
            list of variables to retrieve

        Raises
        ------
        NotImplementedError
            if several timezones are assigned to the same station
        AttributeError
            if data unit is unkown

        Returns
        -------
        stats : list
            list of StationData objects

        """

        stat_meta = self._init_station_metadata()
        stat_ids = list(stat_meta.keys())
        const.print_log.info('Read AirNow data file(s)')
        # initialize empty dataframe

        varcol = self.FILE_COL_NAMES.index('variable')
        statcol = self.FILE_COL_NAMES.index('station_id')
        tzonecol = self.FILE_COL_NAMES.index('time_zone')
        unitcol = self.FILE_COL_NAMES.index('unit')
        valcol = self.FILE_COL_NAMES.index('value')

        arrs = []
        for i in tqdm(range(len(files))):
            fp = files[i]
            filedata = self._read_file(fp)
            arr = filedata.values

            for i, var in enumerate(vars_to_retrieve):
                if i == 0:
                    mask = arr[:, varcol] == self.VAR_MAP[var]
                else:
                    mask = np.logical_or(mask, arr[:, varcol] == self.VAR_MAP[var])
            matches = mask.sum()
            if matches:
                vardata = arr[mask]
                arrs.append(vardata)
        if len(arrs) == 0:
            raise DataRetrievalError(
                'None of the input variables could be found in input list')
        data = np.concatenate(arrs)

        dtime = self.make_datetime64_array(data[:, 0], data[:, 1])
        stats = []
        for var in vars_to_retrieve:
            # extract only variable data (should speed things up)
            var_in_file = self.VAR_MAP[var]
            mask = data[:, varcol] == var_in_file
            subset = data[mask]
            dtime_subset = dtime[mask]
            statlist = np.unique(subset[:, statcol])
            for stat_id in statlist:
                if not stat_id in stat_ids:
                    continue
                statmask = subset[:, statcol] == stat_id
                if statmask.sum() == 0:
                    continue
                statdata = subset[statmask]
                timestamps = dtime_subset[statmask]

                stat = StationData(**stat_meta[stat_id])
                offs = np.unique(statdata[:, tzonecol])


                if not len(offs) == 1:
                    raise NotImplementedError(
                        f'Encountered several timezones for station ID {stat_id}'
                        )
                # account for timezone
                timedelta = np.timedelta64(int(offs[0]), 'h')
                vals = statdata[:, valcol]
                units = np.unique(statdata[:, unitcol])
                if len(units) != 1:
                    raise NotImplementedError(
                        f'Encountered several units for {var}'
                        )
                elif not units[0] in self.UNIT_MAP:
                    raise AttributeError(
                        'Encountered unregistered unit {units[0]} for {var}'
                        )
                stat['dtime'] = timestamps + timedelta
                stat['timezone'] ='UTC'
                stat[var] = vals
                unit = self.UNIT_MAP[units[0]]
                stat['var_info'][var] = dict(units=unit)
                stats.append(stat)
        return stats

    def read_file(self):
        """
        This method is not implemented (but needs to be declared for template)

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError('Not needed for these data since the format '
                                  'is unsuitable...')

    def read(self, vars_to_retrieve=None, first_file=None, last_file=None):
        """
        Read variable data

        Parameters
        ----------
        vars_to_retrieve : str or list, optional
            List of variables to be retrieved. The default is None.
        first_file : int, optional
            Index of first file to be read. The default is None, in which case
            index 0 in file list is used.
        last_file : int, optional
            Index of last file to be read. The default is None, in which case
            last index in file list is used.

        Returns
        -------
        data : UngriddedData
            loaded data object.

        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]

        files = self.get_file_list()
        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)
        files = files[first_file:last_file]

        stats = self._read_files(files, vars_to_retrieve)

        data = UngriddedData.from_station_data(stats,
                                               add_meta_keys=['timezone',
                                                              'area_classification',
                                                              'station_classification']
                                               )

        return data


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.close('all')
    path_data = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/MACC_INSITU_AirNow'
    path_data = '/home/jonasg/MyPyaerocom/data/obsdata/MACC_INSITU_AirNow'

    test_file =  path_data + '/202001/2020010100.dat'
    reader = ReadAirNow(data_dir=path_data)

    #data = reader._read_file(test_file)

    last_file = 10
    varis = None
    data = reader.read('vmrso2', last_file=last_file)

    if last_file == 10 and varis == ['concpm10', 'concpm25']:
        assert len(data.unique_station_names) == 744
    data.plot_station_coordinates()
    #data1 = _read_file_alt(files[0])
