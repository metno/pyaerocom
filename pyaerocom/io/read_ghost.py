# -*- coding: utf-8 -*-
# this file is part of the pyaerocom package
# Copyright (C) 2018 met.no
# Contact information:
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# Author: Jonas Gliss
# E-mail: jonasg@met.no
# License: https://github.com/metno/pyaerocom/blob/master/LICENSE
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA
import glob
import os
import numpy as np
import pandas as pd
import xarray as xr

import pyaerocom as pya
from pyaerocom import const
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.io.ghost_meta_keys import GHOST_META_KEYS
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.helpers import varlist_aerocom
from pyaerocom.time_config import TS_TYPES

class ReadGhost(ReadUngriddedBase):
    """Reading interface for GHOST data
    
    First version of GHOST reading class for reading in pyaerocom 
    
    Note
    ----
    This class inherits from the metaclass template `ReadUngriddedBase`. 
    Please have a look at that and make sure you understand the idea behind
    it. 
    
    TODO
    ----
    - Revise after file format is finalised as there may be ways to make it
    more efficient. E.g. if files remain single variable, the read_file 
    method does not need to be able to handle multiple variables. Also the 
    chunk extension check in read could be done then before looping over 
    all sites, etc..
    - Test if evaluation of flags works properly.
    - Translate default metadata names (e.g. measuring_instrument_name ->
    instrument_name, check class StationMetaData in pyaerocom/metastandards.py)  
    - Translate variable names and make sure to read them in the correct unit 
    (e.g. sconco3 [mmol mmol-1] -> conco3 [ug m-3], cf. 
    pyaerocom/data/variables.ini).
    - Check with Dene and agree on, e.g. 10 sites, and compare time series data
    for each variable, both with and without removal of invalid measurements 
    using default qa flags specified in attr. DEFAULT_FLAGS_INVALID.
    - Investigate data from a few sites that is also available in EBAS database
    and compare timeseries.
    - Write a few tests (e.g. mean value at site X, variable Y for a certain
    time interval)
    - We need a strategy how to handle caching of `UngriddedData` instances
    in :class:`ReadUngridded` for different combinations of QA flags (since 
    they are evaluated during reading).
    
    Information about data quality(Email from D. Bowdalo 2.3.2020)
    --------------------------------------------------------------
    Inside is hourly and daily resolution data for O3, NO, NO2, CO, SO2, PM2.5 
    and PM10 for 2018 and 2019.

    The data is a mesh of the EEA E1a (validated)/E2a (UTD) data streams. 
    Almost all of the 2018 data is from the E1a stream and all of the 2019 is 
    from the E2a stream. 
    These can be entirely separated out using the QA code 4 ('Not Maximum 
    Data Quality Level’), for which all data from the E2a stream is flagged 
    with.

    Additionally I put the QA code 5 ('Preliminary Data’) in my list of 
    default QA codes to screen by Jonas, but you may wish to remove this as a 
    lot of the 2019 E2a data is flagged by EEA as preliminary, and therefore 
    flagged by my processing accordingly.
    """
    __version__ = '0.0.2'
    
    _FILEMASK = '*.nc'
    
    DATA_ID = 'GHOST.daily'
    
    SUPPORTED_DATASETS = ['GHOST.hourly',
                          'GHOST.daily']
    
    TS_TYPES = {'GHOST.hourly'   : 'hourly',
                'GHOST.daily'    : 'daily'}
    
    META_KEYS = GHOST_META_KEYS
    
    FLAG_VARS = ['flag', 'qa']
    
    FLAG_DIMNAMES = {'qa'   : 'N_qa_codes',
                     'flag' : 'N_flag_codes'}
    
    #: these need to be output variables in AeroCom convention (cf. file 
    #: pyaerocom/data/variables.ini). See also :attr:`VARNAMES_DATA` for a 
    #: mapping of variable names used in GHOST
    PROVIDES_VARIABLES = ['concpm10', 'concpm25','concco', 'concno',
                          'concno2', 'conco3', 'concso2']
    
    #: dictionary mapping GHOST variable names to AeroCom variable names
    VARNAMES_DATA = {'concpm10' : 'pm10',
                     'concpm25' : 'pm2p5',
                     'concco'   : 'sconcco',
                     'concno'   : 'sconcno',
                     'concno2'  : 'sconcno2',
                     'conco3'   : 'sconco3',
                     'concso2'  : 'sconcso2',
                     }
    
    # This is the default list of flags that mark bad / invalid data, as 
    # provided by Dene: [0, 1, 2, 3, 5, 6, 8, 9, 10, 12, 13, 14, 17, 18, 22, 
    # 25, 30, 40, 41, 42]
    
    #: Default flags used to invalidate data points (these may be either from
    #: provided flag or qa variable, or both, currently only from qa variable)
    DEFAULT_FLAGS_INVALID = {'qa' : np.asarray([0, 1, 2, 3, 6, 8, 9, 10, 12, 
                                                13, 14, 17, 18, 22, 25, 30, 40, 
                                                41, 42]),
                             'flag' : None}
    
    @property
    def DEFAULT_VARS(self):
        return self.PROVIDES_VARIABLES
        
    @property
    def var_names_data_inv(self):
        try:
            return self._var_names_inv
        except AttributeError:
            self._var_names_inv ={v: k for k, v in self.VARNAMES_DATA.items()}
            return self._var_names_inv
    
    def get_file_list(self, vars_to_read=None, pattern=None):
        """
        Retrieve a list of files to read based on input variable names

        Parameters
        ----------
        vars_to_read : str, optional
            list of variables to be imported. If None, use The default is None.
        pattern : TYPE, optional
            DESCRIPTION. The default is None.

        Raises
        ------
        ValueError
            If no files can be found for any of the input variables.

        Returns
        -------
        list
            list with file paths

        """
        if vars_to_read is None:
            vars_to_read =  self.PROVIDES_VARIABLES
        elif isinstance(vars_to_read, str):
            vars_to_read = [vars_to_read]
            
        if pattern is None:
            pattern = self._FILEMASK
         
        files = []
        for var in vars_to_read:
            if var in self.VARNAMES_DATA:
                # make sure to check for right variable, user may use either 
                # AeroCom variable name or GHOST variable name
                var = self.VARNAMES_DATA[var]
    
            _dir = os.path.join(self.DATASET_PATH, var)
            _files = glob.glob('{}/{}'.format(_dir, pattern)) 
            if len(_files) == 0:
                raise ValueError('Could not find any data files for '
                                 'variable {}'.format(var))
            files.extend(_files)
            
        self.files = sorted(files)
        return self.files
            
    def get_meta_filename(self, filename):
        """Extract metadata from data filename

        Parameters
        ----------
        filename : str
            data file path or name.

        Returns
        -------
        dict
            dictionary containing var_name, start and stop, and eventually 
            also frequency (ts_type)
        """
        var, time = os.path.basename(filename).split('.nc')[0].split('_')

        per = pd.Period(freq='M', year=int(time[:4]), month=int(time[-2:]))
        return dict(var_name=var, start=per.start_time, 
                    stop=per.end_time, ts_type=None)
    
    @staticmethod
    def _eval_flags_slice(slc, invalid_flags):
        """
        Compare a flag slice of a data point with input flags marking invalid
        
        Returns
        -------
        bool
            True, if data point is valid, else False
        """
        if len(np.intersect1d(slc, invalid_flags)) == 0:
            return True
        return False
    

    def _ts_type_from_data_id(self):
        if '.' in self.DATA_ID:
            ts_type = self.DATA_ID.split('.')[-1]
            if ts_type in TS_TYPES:
                self.TS_TYPES[self.DATA_ID] = ts_type
                return ts_type
        raise AttributeError('Failed to retrieve ts_type from DATA_ID')
        
    @property
    def TS_TYPE(self):
        """Default implementation of string for temporal resolution"""
        try:
            return self.TS_TYPES[self.DATA_ID]
        except KeyError:
            try:
                return self._ts_type_from_data_id()
            except:
                return 'undefined'
            
    def read_file(self, filename, var_to_read=None, invalidate_flags=None,
                  var_to_write=None):
        """Read GHOST NetCDF data file
        
        Parameters
        ----------
        filename : str
            absolute path to filename to read
        var_name : str, optional
            name of variable to be read, if None, it is inferred from filename
            
        Returns
        -------
        list
            list of loaded `StationData` objects (dict-like data objects)
        
        """
        if invalidate_flags is None:
            invalidate_flags = self.DEFAULT_FLAGS_INVALID
            
        if var_to_read is None:
            var_to_read = self.get_meta_filename(filename)['var_name']
        elif var_to_read in self.VARNAMES_DATA:
            if var_to_write is None:
                var_to_read, var_to_write = self.VARNAMES_DATA[var_to_read], var_to_read
            else:
                var_to_read = self.VARNAMES_DATA[var_to_read]
        
        if var_to_write is None:
            var_to_write = self.var_names_data_inv[var_to_read]
        
        ds = xr.open_dataset(filename)
        
        if not all(x in ds.dims for x in ['station', 'time']):
            raise AttributeError('Missing dimensions')
        if not 'station_name' in ds:
            raise AttributeError('No variable station_name found')
        
        stats = []
        
        # get all station metadata values as numpy arrays, since xarray isel, 
        # __getitem__, __getattr__ are slow... this can probably be solved 
        # more elegantly
        meta_glob = {}
        for meta_key in self.META_KEYS:
            meta_glob[meta_key] = ds[meta_key].values
            
        tvals = ds['time'].values
        
        vardata = ds[var_to_read] #DataArray
        varinfo = vardata.attrs
        # ToDo: it is important that station comes first since we use numpy 
        # indexing below and not xarray.isel or similar, due to performance 
        # issues. This may will need to be updated in case of profile data.
        assert vardata.dims == ('station', 'time')
        data_np = vardata.values
        
        
        # evaluate flags
        valid = np.ones_like(vardata).astype(bool)
        for flagvar in self.FLAG_VARS:
            # check if this flag variable is in input dictionary
            if flagvar in invalidate_flags:
                invalidate = invalidate_flags[flagvar]
                if invalidate is None:
                    continue
                
                flags = ds[flagvar]
                slice_dim = flags.dims.index(self.FLAG_DIMNAMES[flagvar])
                
                valid *= np.apply_along_axis(self._eval_flags_slice, 
                                             slice_dim, flags.values, 
                                             invalidate)
        
        invalid = ~valid
        for idx in ds.station.values:
            
            stat = {}
            meta = pya.metastandards.StationMetaData()
            meta['ts_type'] = self.TS_TYPE
            stat['time'] = tvals
            stat['meta'] = meta
            meta['var_info'] = {}
            
            for meta_key, vals in meta_glob.items():
                meta[meta_key] = vals[idx]
                
            #vardata = subset[var_name]
            stat[var_to_write] = data_np[idx]
            
            meta['var_info'][var_to_write] = {}
            meta['var_info'][var_to_write].update(varinfo)
            
            # import flagdata (2D array with time and flag dimensions)
            #invalid = self._eval_flags(vardata, invalidate_flags)
            stat['data_flagged'] = {}
            stat['data_flagged'][var_to_write] = invalid[idx]
            stats.append(stat)
        
        return stats
    
    def read(self, vars_to_retrieve=None, files=None, first_file=None, 
             last_file=None, pattern=None, check_time=True):
        """Read data files into `UngriddedData` object
        
        Parameters
        ----------
        vars_to_retrieve : :obj:`list` or similar, optional,
            list containing variable IDs that are supposed to be read. If None, 
            all variables in :attr:`PROVIDES_VARIABLES` are loaded
        files : :obj:`list`, optional
            list of files to be read. If None, then the file list is used that
            is returned on :func:`get_file_list`.
        first_file : :obj:`int`, optional
            index of first file in file list to read. If None, the very first
            file in the list is used
        last_file : :obj:`int`, optional
            index of last file in list to read. If None, the very last file 
            in the list is used
         file_pattern : str, optional
            string pattern for file search (cf :func:`get_file_list`)
            
        Returns
        -------
        UngriddedData
            data object
        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        
        # make sure to use AeroCom variable names in output data
        vars_to_retrieve = varlist_aerocom(vars_to_retrieve)
        if files is None:
            files = self.get_file_list(vars_to_retrieve, pattern=pattern)
         
            
        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)
        
        files = files[first_file:last_file]
        
        data_obj = UngriddedData()
        
        meta_key = -1.0
        idx = 0
        
        #assign metadata object
        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx
        var_count_glob = -1
        rename = self.var_names_data_inv
        for i, _file in enumerate(files):
            metafile = self.get_meta_filename(_file)
            var_to_read = metafile['var_name']
            begin = metafile['start']
            end = metafile['stop']
             
            var_to_write = rename[var_to_read]
            stats = self.read_file(_file, var_to_read=var_to_read,
                                   var_to_write=var_to_write)
            
            if len(stats) == 0:
                const.logger.info('File {} does not contain any of the input '
                                  'variables {}'
                                  .format(_file, vars_to_retrieve))
            
            for stat in stats:
                meta_key += 1
                meta_idx[meta_key] = {}
                metadata[meta_key] = meta = stat['meta']
                
                times = stat['time'].astype('datetime64[s]')
                timenums = np.float64(times)
                
                if check_time and (begin > times[0] or end < times[-1]):
                    raise ValueError('Something seems to be off with time '
                                     'dimension...')
                    
                num_times = len(times)
                
                #check if size of data object needs to be extended
                if (idx + num_times) >= data_obj._ROWNO:
                    #if totnum < data_obj._CHUNKSIZE, then the latter is used
                    data_obj.add_chunk(num_times)
                
                values = stat[var_to_write]
                start = idx 
                stop = start + num_times
                
                if not var_to_write in data_obj.var_idx:
                    var_count_glob += 1
                    var_idx = var_count_glob
                    data_obj.var_idx[var_to_write] = var_idx
                else:
                    var_idx = data_obj.var_idx[var_to_write]
                
                
                #write common meta info for this station (data lon, lat and 
                #altitude are set to station locations)
                data_obj._data[start:stop, 
                               data_obj._LATINDEX] = meta['latitude']
                data_obj._data[start:stop, 
                               data_obj._LONINDEX] = meta['longitude']
                data_obj._data[start:stop, 
                               data_obj._ALTITUDEINDEX] = meta['altitude']
                data_obj._data[start:stop, 
                               data_obj._METADATAKEYINDEX] = meta_key
                               
                # write data to data object
                data_obj._data[start:stop, data_obj._TIMEINDEX] = timenums


                data_obj._data[start:stop, data_obj._DATAINDEX] = values
                
                # add invalid measurements
                invalid = stat['data_flagged'][var_to_write]
                data_obj._data[start:stop, data_obj._DATAFLAGINDEX] = invalid

                data_obj._data[start:stop, data_obj._VARINDEX] = var_idx
                
                meta_idx[meta_key][var_to_write] = np.arange(start, stop)
                    
                idx += num_times
                
        data_obj._data = data_obj._data[:idx]           
        data_obj._check_index()
        return data_obj

if __name__ == '__main__':
    
    reader = ReadGhost()
    
    files = reader.get_file_list('conco3')
    
    stats = reader.read_file(files[-1])
    
    data = reader.read('conco3', files=[files[-1]])
    
    