################################################################
# read_aeronet_sunv2.py
#
# read Aeronet direct sun V2 data
#
# this file is part of the pyaerocom package
#
#################################################################
# Created 20171026 by Jan Griesfeller for Met Norway
#
# Last changed: See git log
#################################################################

# Copyright (C) 2017 met.no
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

import numpy as np
import pandas as pd
from collections import OrderedDict as od
import re

from pyaerocom import const
from pyaerocom.mathutils import (calc_ang4487aer, calc_od550aer)
from pyaerocom.io import ReadUngriddedBase, TimeSeriesFileData
from pyaerocom import UngriddedData

class ReadAeronetSunV2(ReadUngriddedBase):
    """Interface for reading Aeronet direct sun version 2 Level 2.0 data
    
    
    Note
    ----
    Even though this is a reading class, it also includes the option to 
    compute variables during import, that are not contained in the actual 
    data files. These are, for instance, the AOD at 550nm or the Angstrom 
    coefficient (corresponding to 440-870 nm range), where the latter is 
    required to compute the former. These additional computations are 
    specified in the two header dictionaries ``AUX_REQUIRES`` (what
    variables are required to perform the computation) and 
    ``AUX_FUNS`` (functions used to perform the computations).
    
    
    Attributes
    ----------
    col_index : dict
        class containing information about what can be imported from the files
    """
    _FILEMASK = '*.lev20'
    __version__ = "0.09"
    DATASET_NAME = const.AERONET_SUN_V2L2_AOD_DAILY_NAME
    
    # List of all datasets that are supported by this interface
    SUPPORTED_DATASETS = [const.AERONET_SUN_V2L2_AOD_DAILY_NAME]
    
    #value corresponding to invalid measurement
    NAN_VAL = np.float_(-9999)

    #file column information
    COL_INDEX = od(date           = 0,
                   time           = 1,
                   julien_day     = 2,
                   od1640aer      = 3,
                   od1020aer      = 4,
                   od870aer       = 5,
                   od675aer       = 6,
                   od667aer       = 7,
                   od555aer       = 8,
                   od551aer       = 9,
                   od532aer       = 10,
                   od531aer       = 11,
                   od500aer       = 12,
                   od440aer       = 15,
                   od380aer       = 17,
                   od340aer       = 18)
    
    # Variables provided by this interface. Note that some of them are not 
    # contained in the original data files but are computed in this class
    # during data import. For each of the latter, please provide the required 
    # information in attributes ``AUX_REQUIRES`` and ``AUX_FUNS``
    PROVIDES_VARIABLES = ['od500aer', 
                          'od440aer', 
                          'od870aer']

    REVISION_FILE = const.REVISION_FILE
    
    # specify required dependencies for auxiliary variables, i.e. variables 
    # that are NOT in Aeronet files but are computed within this class. 
    # For instance, the computation of the AOD at 550nm requires import of
    # the AODs at 440, 500 and 870 nm. 
    AUX_REQUIRES = {'od550aer'   :   ['od440aer', 
                                      'od500aer',
                                      'ang4487aer'],
                    'ang4487aer' :   ['od440aer',
                                      'od870aer']}
                    
    # Functions that are used to compute additional variables (i.e. one 
    # for each variable defined in AUX_REQUIRES)
    AUX_FUNS = {'od550aer'   :   calc_od550aer,
                'ang4487aer' :   calc_ang4487aer}
    
    # Level 2.0. Quality Assured Data.<p>The following data are pre and post field calibrated, automatically cloud cleared and manually inspected.
    # Version 2 Direct Sun Algorithm
    # Location=Zvenigorod,long=36.775,lat=55.695,elev=200,Nmeas=11,PI=Brent_Holben,Email=Brent.N.Holben@nasa.gov
    # AOD Level 2.0,Daily Averages,UNITS can be found at,,, http://aeronet.gsfc.nasa.gov/data_menu.html
    # Date(dd-mm-yy),Time(hh:mm:ss),Julian_Day,AOT_1640,AOT_1020,AOT_870,AOT_675,AOT_667,AOT_555,AOT_551,AOT_532,AOT_531,AOT_500,AOT_490,AOT_443,AOT_440,AOT_412,AOT_380,AOT_340,Water(cm),%TripletVar_1640,%TripletVar_1020,%TripletVar_870,%TripletVar_675,%TripletVar_667,%TripletVar_555,%TripletVar_551,%TripletVar_532,%TripletVar_531,%TripletVar_500,%TripletVar_490,%TripletVar_443,%TripletVar_440,%TripletVar_412,%TripletVar_380,%TripletVar_340,%WaterError,440-870Angstrom,380-500Angstrom,440-675Angstrom,500-870Angstrom,340-440Angstrom,440-675Angstrom(Polar),N[AOT_1640],N[AOT_1020],N[AOT_870],N[AOT_675],N[AOT_667],N[AOT_555],N[AOT_551],N[AOT_532],N[AOT_531],N[AOT_500],N[AOT_490],N[AOT_443],N[AOT_440],N[AOT_412],N[AOT_380],N[AOT_340],N[Water(cm)],N[440-870Angstrom],N[380-500Angstrom],N[440-675Angstrom],N[500-870Angstrom],N[340-440Angstrom],N[440-675Angstrom(Polar)]
    # 16:09:2006,00:00:00,259.000000,-9999.,0.036045,0.036734,0.039337,-9999.,-9999.,-9999.,-9999.,-9999.,0.064670,-9999.,-9999.,0.069614,-9999.,0.083549,0.092204,0.973909,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,1.126095,0.973741,1.474242,1.135232,1.114550,-9999.,-9999.,11,11,11,-9999.,-9999.,-9999.,-9999.,-9999.,11,-9999.,-9999.,11,-9999.,11,11,11,11,11,11,11,11,-9999.
    
    @property
    def col_index(self):
        return self.COL_INDEX
    
    def read_file(self, filename, vars_to_retrieve=['od550aer'],
                  vars_as_series=False):
        """Read Aeronet Sun V2 level 2 file 

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : list
            list of str with variable names to read; defaults to ['od550aer']
        vars_as_series : bool
            if True, the data columns of all variables in the result dictionary
            are converted into pandas Series objects
        
        Returns
        -------
        TimeSeriesFileData 
            dict-like object containing results
            
        Example
        -------
        >>> import pyaerocom.io.read_aeronet_sunv2
        >>> obj = pyaerocom.io.read_aeronet_sunv2.ReadAeronetSunV2()
        >>> files = obj.get_file_list()
        >>> filedata = obj.read_file(files[0])
        """
        # implemented in base class
        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)
        
        #create empty data object (is dictionary with extended functionality)
        data_out = TimeSeriesFileData() 
        
        #create empty array for all variables that are supposed to be read
        for var in vars_to_read:
            data_out[var] = []
    
        # Iterate over the lines of the file
        self.logger.info("Reading file {}".format(filename))
        with open(filename, 'rt') as in_file:
            #added to output
            data_out.head_line = in_file.readline().strip()
            data_out.algorithm = in_file.readline().strip()
            c_dummy = in_file.readline()
            # re.split(r'=|\,',c_dummy)
            i_dummy = iter(re.split(r'=|\,', c_dummy.rstrip()))
            dict_loc = dict(zip(i_dummy, i_dummy))

            data_out['latitude'] = float(dict_loc['lat'])
            data_out['longitude'] = float(dict_loc['long'])
            data_out['altitude'] = float(dict_loc['elev'])
            data_out['station_name'] = dict_loc['Location']
            data_out['PI'] = dict_loc['PI']
            c_dummy = in_file.readline()
            #added to output
            data_out.data_header = in_file.readline().strip()
            
            for line in in_file:
                # process line
                dummy_arr = line.split(',')
                
                day, month, year = dummy_arr[self.col_index['date']].split(':')
                
                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, dummy_arr[self.col_index['time']]])
                datestring = '+'.join([datestring, '00:00'])
                
                data_out['dtime'].append(np.datetime64(datestring))
                
                for var in vars_to_read:
                    val = float(dummy_arr[self.col_index[var]])
                    if val == self.NAN_VAL:
                        val = np.nan
                    data_out[var].append(val)
        data_out['dtime'] = np.asarray(data_out['dtime'])
        for var in vars_to_read:
            data_out[var] = np.asarray(data_out[var])
        
        data_out = self.compute_additional_vars(data_out, vars_to_compute)
        
        # TODO: reconsider to skip conversion to Series
        # convert  the vars in vars_to_retrieve to pandas time series
        # and delete the other ones
        if vars_as_series:        
            for var in (vars_to_read + vars_to_compute):
                if var in vars_to_retrieve:
                    data_out[var] = pd.Series(data_out[var], 
                                              index=data_out['dtime'])
                else:
                    del data_out[var]
            
        return data_out
    
    def read(self, vars_to_retrieve=['od550aer'], first_file=None, 
             last_file=None):
        """Read all data files into instance of :class:`UngriddedData` object
        
        Parameters
        ----------
        vars_to_retrieve : list
            list of variables that are supposed to be read from the files
            (cf. :class:`_col_index`) or computed during import 
            (cf. class attributes ``AUX_REQUIRES`` and 
            ``AUX_FUNS``)
        first_file : int
            index of first file in file list to read. If None, the very first
            file in the list is used
        last_file : int
            index of last file in list to read. If None, the very last file 
            in the list is used

        
        Example
        -------
        >>> import pyaerocom.io.read_aeronet_sunv2
        >>> obj = pyaerocom.io.read_aeronet_sunv2.ReadAeronetSunV2()
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
        # initialisations
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
                metadata[meta_key] = {}
                metadata[meta_key]['station_name'] = station_data['station_name']
                metadata[meta_key]['latitude'] = station_data['latitude']
                metadata[meta_key]['longitude'] = station_data['longitude']
                metadata[meta_key]['altitude'] = station_data['altitude']
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
                    
                    #assign indices in metadata dictionary
                    metadata[meta_key]['indexes'][var] = np.arange(start, stop)
                                       
                idx += totnum
                meta_key += 1
            except:
                self.read_failed.append(_file)
                self.logger.exception("Failed to read file %s")
        
        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]
        self.data = data_obj
        return data_obj
    
if __name__=="__main__":
    
    read = ReadAeronetSunV2()
    
    read.verbosity_level = 'debug'
    first_ten = read.read(last_file=10)
    
    data = read.read_first_file()
    print(data)


