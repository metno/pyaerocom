################################################################
# read_aeronet_sdav3.py
#
# read Aeronet SDA V3 data
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

"""
Read Aeronet SDA V3 data
"""
import os

import numpy as np
import pandas as pd
from collections import OrderedDict as od

from pyaerocom import const
from pyaerocom.mathutils import (calc_od550aer,
                                 calc_od550gt1aer,
                                 calc_od550lt1aer)
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.io.timeseriesfiledata import TimeSeriesFileData
from pyaerocom import UngriddedData

class ReadAeronetSdaV3(ReadUngriddedBase):
    """Interface for reading Aeronet direct sun version 3 Level 1.5 and 2.0 data

    Attributes
    ----------
    data : numpy array of dtype np.float64 initially of shape (10000,8)
        data point array
    metadata : dict
        meta data dictionary

    Parameters
    ----------
    verbose : Bool
        if True some running information is printed

    """
    _FILEMASK = '*.lev30'
    __version__ = "0.04"
    
    DATASET_NAME = const.AERONET_SUN_V3L15_SDA_DAILY_NAME
    
    SUPPORTED_DATASETS = [const.AERONET_SUN_V3L15_SDA_DAILY_NAME,
                          const.AERONET_SUN_V3L2_SDA_DAILY_NAME]
    
    NAN_VAL = np.float_(-9999.)
    
    REVISION_FILE = const.REVISION_FILE
    # data vars
    # will be stored as pandas time series
    DATA_COLNAMES = {}
    DATA_COLNAMES['od500gt1aer'] = 'Coarse_Mode_AOD_500nm[tau_c]'
    DATA_COLNAMES['od500lt1aer'] = 'Fine_Mode_AOD_500nm[tau_f]'
    DATA_COLNAMES['od500aer'] = 'Total_AOD_500nm[tau_a]'
    DATA_COLNAMES['ang4487aer'] = 'Angstrom_Exponent(AE)-Total_500nm[alpha]'

    # meta data vars
    # will be stored as array of strings
    METADATA_COLNAMES = {}
    METADATA_COLNAMES['data_quality_level'] = 'Data_Quality_Level'
    METADATA_COLNAMES['instrument_number'] = 'AERONET_Instrument_Number'
    METADATA_COLNAMES['station_name'] = 'AERONET_Site'
    METADATA_COLNAMES['latitude'] = 'Site_Latitude(Degrees)'
    METADATA_COLNAMES['longitude'] = 'Site_Longitude(Degrees)'
    METADATA_COLNAMES['altitude'] = 'Site_Elevation(m)'
    METADATA_COLNAMES['date'] = 'Date_(dd:mm:yyyy)'
    METADATA_COLNAMES['time'] = 'Time_(hh:mm:ss)'
    METADATA_COLNAMES['day_of_year'] = 'Day_of_Year'
    
    # specify required dependencies for auxiliary variables, i.e. variables 
    # that are NOT in Aeronet files but are computed within this class. 
    # For instance, the computation of the AOD at 550nm requires import of
    # the AODs at 440, 500 and 870 nm. 
    AUX_REQUIRES = {'od550aer'      :   ['od500aer', 'ang4487aer'],
                    'od550gt1aer'   :   ['od500gt1aer', 'ang4487aer'],
                    'od550lt1aer'   :   ['od500lt1aer', 'ang4487aer']}
                    
    # Functions that are used to compute additional variables (i.e. one 
    # for each variable defined in AUX_REQUIRES)
    AUX_FUNS = {'od550aer'      :   calc_od550aer,
                'od550gt1aer'   :   calc_od550gt1aer,
                'od550lt1aer'   :   calc_od550lt1aer}
    
    # will be extended by auxiliary variables on class init, for details see
    # base class ReadUngriddedBase
    PROVIDES_VARIABLES = list(DATA_COLNAMES.keys())

    def __init__(self, dataset_to_read=None):
        super(ReadAeronetSdaV3, self).__init__(dataset_to_read)
        
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
    
    def read_file(self, filename, 
                  vars_to_retrieve=['od550aer', 'od550gt1aer','od550lt1aer'],
                  vars_as_series=False):
        """Read Aeronet SDA V3 file and return it in a dictionary

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
        TimeSeriesFileData 
            dict-like object containing results
        """
        # implemented in base class
        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)
       
        #create empty data object (is dictionary with extended functionality)
        data_out = TimeSeriesFileData() 
        
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
            in_file.readline()
            in_file.readline()
            in_file.readline()
            in_file.readline()
            
            # PI line
            dummy_arr = in_file.readline().strip().split(';')
            data_out['PI'] = dummy_arr[0].split('=')[1]
            data_out['PI_email'] = dummy_arr[1].split('=')[1]

            data_type_comment = in_file.readline()
            # TODO: delete later
            self.logger.info("Data type comment: {}".format(data_type_comment))
            # line_7 = in_file.readline()
            # put together a dict with the header string as key and the index number as value so that we can access
            # the index number via the header string
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
                dummy_arr = line.split(',')
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
                for var in self.METADATA_COLNAMES:
                    val = dummy_arr[col_index[self.METADATA_COLNAMES[var]]]
                    try:
                        # e.g. lon, lat, altitude
                        val = float(val)
                    except:
                        pass
                    data_out[var].append(val)

                # copy the data fields 
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

    ###################################################################################

    def read(self, vars_to_retrieve=['od550aer', 'od550gt1aer','od550lt1aer'], 
             first_file=None, last_file=None):
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
        >>> from pyaerocom.io import ReadAeronetSdaV3
        >>> obj = ReadAeronetSdaV3()
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
            station_data = self.read_file(_file, vars_to_retrieve=vars_to_retrieve)
            # Fill the metatdata dict
            # the location in the data set is time step dependant!
            # use the lat location here since we have to choose one location
            # in the time series plot
            metadata[meta_key] = {}
            metadata[meta_key]['station_name'] = station_data['station_name'][-1]
            metadata[meta_key]['latitude'] = station_data['latitude'][-1]
            metadata[meta_key]['longitude'] = station_data['longitude'][-1]
            metadata[meta_key]['altitude'] = station_data['altitude'][-1]
            metadata[meta_key]['PI'] = station_data['PI']
            metadata[meta_key]['dataset_name'] = self.DATASET_NAME

            # this is a list with indexes of this station for each variable
            # not sure yet, if we really need that or if it speeds up things
            metadata[meta_key]['indexes'] = {}
            
            num_times = station_data.num_timestamps
            totnum = station_data.len_flat(num_vars)
            
            #check if size of data object needs to be extended
            if (idx + totnum) >= data_obj._ROWNO:
                #if totnum < data_obj._CHUNKSIZE, then the latter is used
                data_obj.add_chunk(totnum)
            
            #access array containing time stamps
            times = np.float64(station_data['dtime'])
            
            for var_idx, var in enumerate(vars_to_retrieve):
                values = station_data[var]
                start = idx + var_idx * num_times
                stop = start + num_times
                
                
                #write common meta info for this station
                data_obj._data[start:stop, 
                               data_obj._LATINDEX] = station_data['latitude']
                data_obj._data[start:stop, 
                               data_obj._LONINDEX] = station_data['longitude']
                data_obj._data[start:stop, 
                               data_obj._ALTITUDEINDEX] = station_data['altitude']
                data_obj._data[start:stop, 
                               data_obj._METADATAKEYINDEX] = meta_key
                               
                # write data to data object
                data_obj._data[start:stop, data_obj._TIMEINDEX] = times
                data_obj._data[start:stop, data_obj._DATAINDEX] = values
                data_obj._data[start:stop, data_obj._VARINDEX] = var_idx
                
                metadata[meta_key]['indexes'][var] = np.arange(start, stop)
            
            idx += totnum  
            meta_key = meta_key + 1.
        
        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]
        self.data = data_obj
        return data_obj
    
if __name__=="__main__":
    read = ReadAeronetSdaV3()
    read.verbosity_level = 'debug'
    
    first_ten = read.read(last_file=10)
    
    data_first = read.read_first_file()
    print(data_first)
