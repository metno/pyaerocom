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

from pyaerocom import const
from pyaerocom.mathutils import (calc_od550aer,
                                 calc_od550gt1aer,
                                 calc_od550lt1aer)
from pyaerocom.io.readaeronetbase import ReadAeronetBase
from pyaerocom import StationData

class ReadAeronetSdaV3(ReadAeronetBase):
    """Interface for reading Aeronet Sun SDA V3 Level 1.5 and 2.0 data
    
    .. seealso::
        
        Base classes :class:`ReadAeronetBase` and :class:`ReadUngriddedBase`
        
    """
    _FILEMASK = '*.lev30'
    __version__ = "0.05"
    
    DATASET_NAME = const.AERONET_SUN_V3L15_SDA_DAILY_NAME
    
    SUPPORTED_DATASETS = [const.AERONET_SUN_V3L15_SDA_DAILY_NAME,
                          const.AERONET_SUN_V3L2_SDA_DAILY_NAME]
    
    DEFAULT_VARS = ['od550aer', 'od550gt1aer','od550lt1aer']
    NAN_VAL = np.float_(-9999.)
    
    REVISION_FILE = const.REVISION_FILE
    
    # column names of supported variables
    DATA_COLNAMES = {}
    DATA_COLNAMES['od500gt1aer'] = 'Coarse_Mode_AOD_500nm[tau_c]'
    DATA_COLNAMES['od500lt1aer'] = 'Fine_Mode_AOD_500nm[tau_f]'
    DATA_COLNAMES['od500aer'] = 'Total_AOD_500nm[tau_a]'
    DATA_COLNAMES['ang4487aer'] = 'Angstrom_Exponent(AE)-Total_500nm[alpha]'

    # meta data vars
    # will be stored as array of strings
    META_COLNAMES = {}
    META_COLNAMES['data_quality_level'] = 'Data_Quality_Level'
    META_COLNAMES['instrument_number'] = 'AERONET_Instrument_Number'
    META_COLNAMES['station_name'] = 'AERONET_Site'
    META_COLNAMES['latitude'] = 'Site_Latitude(Degrees)'
    META_COLNAMES['longitude'] = 'Site_Longitude(Degrees)'
    META_COLNAMES['altitude'] = 'Site_Elevation(m)'
    META_COLNAMES['date'] = 'Date_(dd:mm:yyyy)'
    META_COLNAMES['time'] = 'Time_(hh:mm:ss)'
    META_COLNAMES['day_of_year'] = 'Day_of_Year'
    
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
        StationData 
            dict-like object containing results
        """
        # implemented in base class
        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)
       
        #create empty data object (is dictionary with extended functionality)
        data_out = StationData() 
        
        # create empty arrays for meta information
        for item in self.META_COLNAMES:
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
            self.logger.debug("Data type comment: {}".format(data_type_comment))
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
                if var in col_index:
                    vars_available[var] = col_index[var]
                else:
                    self.logger.warning("Variable {} not available in file {}"
                                        .format(var, os.path.basename(filename)))

            for line in in_file:
                # process line
                dummy_arr = line.split(',')
                
                # copy the meta data (array of type string)
                for var in self.META_COLNAMES:
                    val = dummy_arr[col_index[var]]
                    try:
                        # e.g. lon, lat, altitude
                        val = float(val)
                    except:
                        pass
                    data_out[var].append(val)
                    
                
                # This uses the numpy datestring64 functions that e.g. also support Months as a time step for timedelta
                # Build a proper ISO 8601 UTC date string

                day, month, year = dummy_arr[col_index['date']].split(':')
                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, dummy_arr[col_index['time']]])
                datestring = '+'.join([datestring, '00:00'])
                
                data_out['dtime'].append(np.datetime64(datestring))

                # copy the data fields 
                for var, idx in vars_available.items():
                    val = np.float_(dummy_arr[idx])
                    if val == self.NAN_VAL: 
                        val = np.nan
                    data_out[var].append(val)

        # convert all lists to numpy arrays
        data_out['dtime'] = np.asarray(data_out['dtime'])
        
        for item in self.META_COLNAMES:
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
    
if __name__=="__main__":
    read = ReadAeronetSdaV3()
    read.verbosity_level = 'debug'
    
    first_ten = read.read(last_file=10)
    
    data_first = read.read_first_file()
    print(data_first)
