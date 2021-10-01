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
    __version__ = '0.07'

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
        self.make_datetime64_array = np.vectorize(
            self._date_time_str_to_datetime64)
        self._station_metadata = None

    @property
    def station_metadata(self):
        """Dictionary containing global metadata for each site"""
        if self._station_metadata is None:
            self._init_station_metadata()
        return self._station_metadata

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
        self._station_metadata = stats
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
        const.print_log.info('Read AirNow data file(s)')
        # initialize empty dataframe
        varcol = self.FILE_COL_NAMES.index('variable')
        arrs = []
        for i in tqdm(range(len(files))):
            fp = files[i]
            filedata = self._read_file(fp)
            arr = filedata.values

            for i, var in enumerate(vars_to_retrieve):
                cond = arr[:, varcol]==self.VAR_MAP[var]
                if i == 0:
                    mask = cond
                else:
                    mask = np.logical_or(mask, cond)
            matches = mask.sum()
            if matches:
                vardata = arr[mask]
                arrs.append(vardata)
        if len(arrs) == 0:
            raise DataRetrievalError(
                'None of the input variables could be found in input list')
        return self._filedata_to_statlist(arrs, vars_to_retrieve)

    def _filedata_to_statlist(self, arrs, vars_to_retrieve):
        """
        Convert loaded filedata into list of StationData objects

        Parameters
        ----------
        arrs : list
            list of numpy arrays extracted from each file
            (see :func:`_read_files`).
        vars_to_retrieve : list
            list of variables to be retrieved from input data.

        Returns
        -------
        stats : list
            list of :class:`StationData` objects, one for each var and station.

        """
        data = np.concatenate(arrs)

        const.print_log.info('Converting filedata to list os StationData')
        stat_meta = self.station_metadata
        stat_ids = list(stat_meta.keys())
        varcol = self.FILE_COL_NAMES.index('variable')
        statcol = self.FILE_COL_NAMES.index('station_id')
        tzonecol = self.FILE_COL_NAMES.index('time_zone')
        unitcol = self.FILE_COL_NAMES.index('unit')
        valcol = self.FILE_COL_NAMES.index('value')


        dtime = self.make_datetime64_array(data[:, 0], data[:, 1])
        stats = []
        for var in vars_to_retrieve:

            # extract only variable data (should speed things up)
            var_in_file = self.VAR_MAP[var]
            mask = data[:, varcol] == var_in_file
            subset = data[mask]
            dtime_subset = dtime[mask]
            statlist = np.unique(subset[:, statcol])
            for stat_id in tqdm(statlist, desc=var):
                if not stat_id in stat_ids:
                    continue
                statmask = subset[:, statcol] == stat_id
                if statmask.sum() == 0:
                    continue
                statdata = subset[statmask]
                timestamps = dtime_subset[statmask]
                # timezone offsets
                toffs = statdata[:, tzonecol].astype(int)
                stat = StationData(**stat_meta[stat_id])

                vals = statdata[:, valcol]
                units = np.unique(statdata[:, unitcol])
                # errors that did not occur in v0 but that may occur
                assert len(units) == 1
                assert units[0] in self.UNIT_MAP
                toffs = toffs.astype('timedelta64[h]')
                timestamps += toffs
                stat['dtime'] = timestamps
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
        self._init_station_metadata()
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
    loc =  '/home/jonasg/MyPyaerocom/data/obsdata/MACC_INSITU_AirNow'
    reader = ReadAirNow(data_dir=loc)

    reader.read('concpm25',last_file=10)