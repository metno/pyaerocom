################################################################
# read_aeronet_invv2.py
#
# read Aeronet inversion V2 data
#
# this file is part of the pyaerocom package
#
#################################################################
# Created 20180629 by Jan Griesfeller for Met Norway
#
# Last changed: See git log
#################################################################

# Copyright (C) 2018 met.no
# Contact information:
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# E-mail: jan.griesfeller@met.no
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

import os, re

import numpy as np
import pandas as pd

from collections import OrderedDict as od

from pyaerocom import const
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom import UngriddedData, StationData

class ReadAeronetInvV2(ReadUngriddedBase):
    """Interface for reading Aeronet inversion version 2 Level 1.5 and 2.0 data

    Parameters
    ----------
    dataset_to_read
        string specifying either of the supported datasets that are defined 
        in ``SUPPORTED_DATASETS``.

    """
    _FILEMASK = '*.dubovikday'
    __version__ = "0.03"
    #
    DATASET_NAME = const.AERONET_INV_V2L2_DAILY_NAME
    
    SUPPORTED_DATASETS = [const.AERONET_INV_V2L2_DAILY_NAME,
                          const.AERONET_INV_V2L15_DAILY_NAME]
    
    NAN_VAL = np.float_(-9999.)
    
    REVISION_FILE = const.REVISION_FILE
    
    # data vars
    # will be stored as pandas time series
    DATA_COLNAMES = {}
    DATA_COLNAMES['ssa439aer'] = 'SSA439-T'
    DATA_COLNAMES['ssa440aer'] = 'SSA440-T'
    DATA_COLNAMES['ssa675aer'] = 'SSA675-T'
    DATA_COLNAMES['ssa870aer'] = 'SSA870-T'
    DATA_COLNAMES['ssa1018aer'] = 'SSA1018-T'

    # meta data vars
    # will be stored as array of strings
    METADATA_COLNAMES = {}
    METADATA_COLNAMES['data_quality_level'] = 'DATA_TYPE'
    METADATA_COLNAMES['date'] = 'Date(dd-mm-yyyy)'
    METADATA_COLNAMES['time'] = 'Time(hh:mm:ss)'
    METADATA_COLNAMES['day_of_year'] = 'Julian_Day'
    
    PROVIDES_VARIABLES = list(DATA_COLNAMES.keys())

    def __init__(self, dataset_to_read=None):
        #init base class
        super(ReadAeronetInvV2, self).__init__(dataset_to_read)
        
        # dictionary that contains information about the file columns
        # is written in method _update_col_index
        self._col_index = od()
        
        # header string referring to the content in attr. col_index. Is 
        # updated whenever the former is updated (i.e. when method
        # _update_col_index is called). Can be used to check if
        # file structure changed between subsequent files so that 
        # col_index is only recomputed when the file structure changes 
        # and not for each file individually
        self._last_col_index_str = None
        
    @property
    def col_index(self):
        """Current column index dictionary"""
        return self._col_index
    
    def _update_col_index(self, col_index_str):
        """Update column information for fast access during read_file"""
        cols = col_index_str.strip().split(',')
        col_index = od()
        for idx, info_str in enumerate(cols):
            col_index[info_str] = idx
        self._col_index = col_index
        self._last_col_index_str = col_index_str
        return col_index
    
    # TODO: currently every file is read, regardless of whether it actually
    # contains the desired variables or not. Do we need that? Slows stuff down..
    # Also: Quick check reading all files in the database showed that only 
    # about 20% of the files contain the default variables..
    def read_file(self, filename, vars_to_retrieve=['ssa675aer','ssa440aer'],
                  vars_as_series=False):
        """Read Aeronet file containing results from v2 inversion algorithm

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : list
            list of str with variable names to read
        vars_as_series : bool
            if True, the data columns of all variables in the result dictionary
            are converted into pandas Series objects
            
        Returns
        -------
        StationData 
            dict-like object containing results
        

        Example
        -------
        >>> import pyaerocom.io as pio
        >>> obj = pio.read_aeronet_invv2.ReadAeronetInvV2()
        >>> files = obj.get_file_list()
        >>> filedata = obj.read_file(files[0])
        """
        # implemented in base class
        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)
       
        #create empty data object (is dictionary with extended functionality)
        data_out = StationData() 
        
        # create empty arrays for meta information
        for item in self.METADATA_COLNAMES:
            data_out[item] = []
            
        # create empty arrays for all variables that are supposed to be read
        # from file
        for var in vars_to_read:
            data_out[var] = []
        
        # Iterate over the lines of the file
        self.logger.info("Reading file {}".format(filename))
    
        with open(filename, 'rt') as in_file:
            #get rid of the first com,a seperated string element...
            c_dummy = ','.join(in_file.readline().strip().split(',')[1:])
            # re.split(r'=|\,',c_dummy)
            i_dummy = iter(re.split(r'=|\,', c_dummy.rstrip()))
            dict_loc = dict(zip(i_dummy, i_dummy))

            data_out['latitude'] = float(dict_loc['lat'])
            data_out['longitude'] = float(dict_loc['long'])
            data_out['altitude'] = float(dict_loc['elev'])
            data_out['station_name'] = dict_loc['Locations']
            data_out['PI'] = dict_loc['PI']
            data_out['PI_email'] = dict_loc['Email']

            #skip next two lines
            in_file.readline()
            in_file.readline()
            
            col_index_str = in_file.readline()
            if col_index_str != self._last_col_index_str:
                self.logger.info("Header has changed, reloading col_index map")
                self._update_col_index(col_index_str)
            col_index = self.col_index
            
            # dependent on the station, some of the required input variables
            # may not be provided in the data file. These will be ignored
            # in the following list that iterates over all data rows and will
            # be filled below, with vectors containing NaNs after the file 
            # reading loop
            vars_available = {}
            for var in vars_to_read:
                var_id = self.DATA_COLNAMES[var]
                if var_id in col_index:
                    vars_available[var] = col_index[var_id]
                else:
                    self.logger.warning("Variable {} not available in file {}"
                                        .format(var, os.path.basename(filename)))
                
            for line in in_file:
                # process line
                dummy_arr = line.strip().split(',')
                # the following uses the standard python datetime functions
                # date_index = col_index[COLNAMES['date']]
                # hour, minute, second = dummy_arr[col_index[COLNAMES['time']].split(':')

                # This uses the numpy datestring64 functions that e.g. also support Months as a time step for timedelta
                # Build a proper ISO 8601 UTC date string
                date = col_index[self.METADATA_COLNAMES['date']]
                time = col_index[self.METADATA_COLNAMES['time']]
                day, month, year = dummy_arr[date].split(':')
                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, dummy_arr[time]])
                datestring = '+'.join([datestring, '00:00'])
                data_out['dtime'].append(np.datetime64(datestring))

                # copy the meta data (array of type string)
                for meta_var in self.METADATA_COLNAMES:
                    meta_val = dummy_arr[col_index[self.METADATA_COLNAMES[meta_var]]]
                    data_out[meta_var].append(meta_val)

                # copy the data fields that are available (rest will be filled
                # below)
                for var, idx in vars_available.items():
                    val = np.float_(dummy_arr[idx])
                    if val == self.NAN_VAL: 
                        val = np.nan
                    data_out[var].append(val)
        
        # convert all lists to numpy arrays
        data_out['dtime'] = np.asarray(data_out['dtime'])
        
        for item in self.METADATA_COLNAMES:
            data_out[item] = np.asarray(data_out[item])
            
        for var in vars_to_read:
            if var in vars_available:
                array = np.asarray(data_out[var])
            else:
                array = np.zeros(len(data_out['dtime'])) * np.nan
            data_out[var] = array
        
        # compute additional variables (if applicable)
        data_out = self.compute_additional_vars(data_out, vars_to_compute)
        
        if vars_as_series:
            # convert the vars in vars_to_retrieve to pandas time series
            # and delete the other ones
            for var in self.PROVIDES_VARIABLES:
                # if var not in data_out: continue
                if var in vars_to_retrieve:
                    data_out[var] = pd.Series(data_out[var], 
                                              index=data_out['time'])
                else:
                    del data_out[var]

        return data_out

    def read(self, vars_to_retrieve=['ssa675aer','ssa440aer'], first_file=None, 
             last_file=None):
        """Read all data files into instance of :class:`UngriddedData` object
        
        Parameters
        ----------
        vars_to_retrieve : list
            list of variables that are supposed to be imported
        first_file : int
            index of first file in file list to read. If None, the very first
            file in the list is used
        last_file : int
            index of last file in list to read. If None, the very last file 
            in the list is used
            
        Example
        -------
        >>> from pyaerocom.io import ReadAeronetInvV2
        >>> obj = ReadAeronetSunV2()
        >>> obj.read()
        """
        if len(self.files) == 0:
            self.get_file_list()
        files = sorted(self.files)
        
        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)
        
        files = files[first_file:last_file]
        
        self.read_failed = []
        
        data_obj = UngriddedData()
        meta_key = 0.0
        idx = 0
        
        #assign metadata object
        metadata = data_obj.metadata
        
        num_vars = len(vars_to_retrieve)

        for _file in files:
            try:
                station_data = self.read_file(_file, vars_to_retrieve)
                
                
                # Fill the metatdata dict
                # the location in the data set is time step dependant!
                # use the lat location here since we have to choose one location
                # in the time series plot
                metadata[meta_key] = {}
                metadata[meta_key].update(station_data.get_meta())
                metadata[meta_key].update(station_data.get_coords())
                
                
# =============================================================================
#                 
#                 metadata[meta_key]['station_name'] = station_data['station_name']
#                 metadata[meta_key]['latitude'] = station_data['latitude']
#                 metadata[meta_key]['longitude'] = station_data['longitude']
#                 metadata[meta_key]['altitude'] = station_data['altitude']
#                 metadata[meta_key]['PI'] = station_data['PI']
#                 metadata[meta_key]['dataset_name'] = self.DATASET_NAME
# =============================================================================
    
                # this is a list with indexes of this station for each variable
                # not sure yet, if we really need that or if it speeds up things
                metadata[meta_key]['indexes'] = {}
                
                num_times = station_data.num_timestamps
                totnum = station_data.len_flat(num_vars)
                
                #check if size of data object needs to be extended
                if (idx + totnum) >= data_obj._ROWNO:
                    #if totnum < data_obj._CHUNKSIZE, then the latter is used
                    data_obj.add_chunk(totnum)
                
                #write common meta info for this station
                data_obj._data[idx:(idx+totnum), 
                               data_obj._LATINDEX] = station_data['latitude']
                data_obj._data[idx:(idx+totnum), 
                               data_obj._LONINDEX] = station_data['longitude']
                data_obj._data[idx:(idx+totnum), 
                               data_obj._ALTITUDEINDEX] = station_data['altitude']
                data_obj._data[idx:(idx+totnum), 
                               data_obj._METADATAKEYINDEX] = meta_key
                
                #access array containing time stamps
                times = np.float64(station_data['dtime'])
                
                for var_idx, var in enumerate(vars_to_retrieve):
                    values = station_data[var]
                    start = idx + var_idx * num_times
                    stop = start + num_times
                    
                    # write to data object
                    data_obj._data[start:stop, data_obj._TIMEINDEX] = times
                    data_obj._data[start:stop, data_obj._DATAINDEX] = values
                    data_obj._data[start:stop, data_obj._VARINDEX] = var_idx
                    
                    metadata[meta_key]['indexes'][var] = np.arange(start, stop)
                
                idx += totnum  
                meta_key = meta_key + 1.
            except:
                self.read_failed.append(_file)
                self.logger.exception("Failed to read file %s")

        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]
        self.data = data_obj
        return data_obj

if __name__=="__main__":
    read = ReadAeronetInvV2(const.AERONET_INV_V2L15_DAILY_NAME)
    read.verbosity_level = 'debug'
    
    first_ten = read.read(last_file=10)
    
    data_first = read.read_first_file()
    print(data_first)