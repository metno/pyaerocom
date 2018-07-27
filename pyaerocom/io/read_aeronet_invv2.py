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

from pyaerocom import const
from pyaerocom.io.readaeronetbase import ReadAeronetBase
from pyaerocom import StationData

class ReadAeronetInvV2(ReadAeronetBase):
    """Interface for reading Aeronet inversion V2 Level 1.5 and 2.0 data

    Parameters
    ----------
    dataset_to_read
        string specifying either of the supported datasets that are defined 
        in ``SUPPORTED_DATASETS``
    """
    #: Mask for identifying datafiles 
    _FILEMASK = '*.dubovikday'
    
    #: version log of this class (for caching)
    __version__ = "0.04"
    
    #: Name of dataset (OBS_ID)
    DATASET_NAME = const.AERONET_INV_V2L2_DAILY_NAME
    
    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.AERONET_INV_V2L2_DAILY_NAME,
                          const.AERONET_INV_V2L15_DAILY_NAME]
    
    #: default variables for read method
    DEFAULT_VARS = ['ssa675aer','ssa440aer']
    
    #: value corresponding to invalid measurement
    NAN_VAL = -9999.
    
    #: dictionary specifying the file column names (values) for each Aerocom 
    #: variable (keys)
    VAR_NAMES_FILE = {}
    VAR_NAMES_FILE['ssa439aer'] = 'SSA439-T'
    VAR_NAMES_FILE['ssa440aer'] = 'SSA440-T'
    VAR_NAMES_FILE['ssa675aer'] = 'SSA675-T'
    VAR_NAMES_FILE['ssa870aer'] = 'SSA870-T'
    VAR_NAMES_FILE['ssa1018aer'] = 'SSA1018-T'

    #: dictionary specifying the file column names (values) for each 
    #: metadata key (cf. attributes of :class:`StationData`, e.g.
    #: 'station_name', 'longitude', 'latitude', 'altitude')
    META_NAMES_FILE = {}
    META_NAMES_FILE['data_quality_level'] = 'DATA_TYPE'
    META_NAMES_FILE['date'] = 'Date(dd-mm-yyyy)'
    META_NAMES_FILE['time'] = 'Time(hh:mm:ss)'
    META_NAMES_FILE['day_of_year'] = 'Julian_Day'
    
    #: List of variables that are provided by this dataset (will be extended 
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    PROVIDES_VARIABLES = list(VAR_NAMES_FILE.keys())

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
        for item in self.META_NAMES_FILE:
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

            data_out['stat_lat'] = float(dict_loc['lat'])
            data_out['stat_lon'] = float(dict_loc['long'])
            data_out['stat_alt'] = float(dict_loc['elev'])
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
                if var in col_index:
                    vars_available[var] = col_index[var]
                else:
                    self.logger.warning("Variable {} not available in file {}"
                                        .format(var, os.path.basename(filename)))
                
            for line in in_file:
                # process line
                dummy_arr = line.strip().split(self.COL_DELIM)

                # This uses the numpy datestring64 functions that i.e. also 
                # support Months as a time step for timedelta
                # Build a proper ISO 8601 UTC date string
                day, month, year = dummy_arr[col_index['date']].split(':')
                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, dummy_arr[col_index['time']]])
                datestring = '+'.join([datestring, '00:00'])
                data_out['dtime'].append(np.datetime64(datestring))
                
                for var in self.META_NAMES_FILE:
                    val = dummy_arr[col_index[var]]
                    try:
                        # e.g. lon, lat, altitude
                        val = float(val)
                    except:
                        pass
                    data_out[var].append(val)

                # copy the data fields that are available (rest will be filled
                # below)
                for var, idx in vars_available.items():
                    val = np.float_(dummy_arr[idx])
                    if val == self.NAN_VAL: 
                        val = np.nan
                    data_out[var].append(val)
        
        # convert all lists to numpy arrays
        data_out['dtime'] = np.asarray(data_out['dtime'])
        
        for item in self.META_NAMES_FILE:
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
            for var in (vars_to_read + vars_to_compute):
                if var in vars_to_retrieve:
                    data_out[var] = pd.Series(data_out[var], 
                                              index=data_out['dtime'])
                else:
                    del data_out[var]
            
        return data_out

if __name__=="__main__":
    read = ReadAeronetInvV2(const.AERONET_INV_V2L15_DAILY_NAME)
    read.verbosity_level = 'debug'
    
    data = read.read(last_file=2)
    
    data_first = read.read_first_file()
    print(data_first)
    print(data.longitude)
    print(data.latitude)
    