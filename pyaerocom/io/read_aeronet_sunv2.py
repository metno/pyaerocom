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
import re
import fnmatch

from pyaerocom import const
from pyaerocom.mathutils import (compute_angstrom_coeff, 
                                 compute_aod_from_angstromexp)
from pyaerocom.utils import _BrowserDict
from pyaerocom.io import ReadUngriddedBase, TimeSeriesFileData
from pyaerocom import UngriddedData

# define some row numbers. not all of them are used at this point
class _COL_INFO(_BrowserDict):
    """ info for AeronetSunV2 files
    
    Please use keys corresponding to AEROCOM convention
    """
    def __init__(self):
        self.date           = 0
        self.time           = 1
        self.julien_day     = 2
        self.od1640aer      = 3
        self.od1020aer      = 4
        self.od870aer       = 5
        self.od675aer       = 6
        self.od667aer       = 7
        self.od555aer       = 8
        self.od551aer       = 9
        self.od532aer       = 10
        self.od531aer       = 11
        self.od500aer       = 12
        self.od440aer       = 15
        self.od380aer       = 17
        self.od340aer       = 18
        
    @property
    def PROVIDES_VARIABLES(self):
        return [x for x in self.keys() if re.search(fnmatch.translate("od*aer"), x)]
    
def add_ang4487aer(data):
    """Method that computes and adds Angstrom coefficient (440-870nm) to data
    
    Parameters
    ----------
    data : dict-like
        data object containing imported results
    
    Returns
    -------
    dict
        updated data object
    """
    od440aer, od870aer = data['od440aer'], data['od870aer']
    data['ang4487aer'] = compute_angstrom_coeff(od440aer, od870aer, .44, .87)
    return data
    

def add_od550aer(data):
    """Method that computes and adds AOD at 550 nm to data object
        
        Parameters
        ----------
        data : dict-like
            data object containing imported results
        
        Returns
        -------
        dict
            updated data object
    """
    od550aer = compute_aod_from_angstromexp(to_lambda=.55, 
                                            aod_ref=data['od500aer'],
                                            lambda_ref=.50, 
                                            angstrom_coeff=data['ang4487aer'])
    
    # ;fill up time steps of the now calculated od550_aer that are nans with values calculated from the
    # ;440nm wavelength to minimise gaps in the time series
    mask = np.argwhere(np.isnan(od550aer))
    
    if len(mask) > 0: #there are nans
        od440aer = data['od440aer'][mask]
        ang4487aer = data['ang4487aer'][mask]
        replace = compute_aod_from_angstromexp(to_lambda=.55, 
                                                aod_ref=od440aer,
                                                lambda_ref=.44, 
                                                angstrom_coeff=ang4487aer)
        od550aer[mask] = replace
        
    # now replace all v
    below_thresh = od550aer < const.VAR_PARAM['od550aer']['lower_limit']
    od550aer[below_thresh] = np.nan

    data['od550aer'] = od550aer
    return data

class ReadAeronetSunV2(ReadUngriddedBase):
    """Interface for reading Aeronet direct sun version 2 Level 2.0 data
    
    
    Note
    ----
    Even though this is a reading class, it also includes the option to 
    compute variables during import, that are not contained in the actual 
    data files. These are, for instance, the AOD at 550nm or the Angstrom 
    coefficient (corresponding to 440-870 nm range), where the latter is 
    required to compute the former. These additional computations are 
    specified in the two header dictionaries ``ADDITIONAL_REQUIRES`` (what
    variables are required to perform the computation) and 
    ``ADDITIONAL_FUNS`` (functions used to perform the computations).
    
    
    Attributes
    ----------
    col_info : _COL_INFO
        class containing information about what can be imported from the files

    Parameters
    ----------
    verbose : Bool
        if True some running information is printed

    """
    _FILEMASK = '*.lev20'
    __version__ = "0.08"
    DATASET_NAME = const.AERONET_SUN_V2L2_AOD_DAILY_NAME
    
    #value corresponding to invalid measurement
    NAN_VAL = float(-9999)
    # Variables provided by this interface. Note that some of them are not 
    # contained in the original data files but are computed in this class
    # during data import
    PROVIDES_VARIABLES = ['od500aer', 
                          'od440aer', 
                          'od870aer', 
                          'ang4487aer', 
                          'od550aer']

    REVISION_FILE = const.REVISION_FILE
    
    # specify required dependencies for variables that are NOT in Aeronet files
    # but are computed within this class. 
    # For instance, the computation of the AOD at 550nm requires import of
    # the AODs at 440, 500 and 870 nm. 
    ADDITIONAL_REQUIRES = {'od550aer'   :   ['od440aer', 
                                             'od500aer',
                                             'ang4487aer'],
                           'ang4487aer' :   ['od440aer',
                                             'od870aer']}
    # Functions that are used to compute additional variables (i.e. one 
    # for each variable defined in ADDITIONAL_REQUIRES)
    ADDITIONAL_FUNS = {'od550aer'   :   add_od550aer,
                      'ang4487aer'  :   add_ang4487aer}
    # Level 2.0. Quality Assured Data.<p>The following data are pre and post field calibrated, automatically cloud cleared and manually inspected.
    # Version 2 Direct Sun Algorithm
    # Location=Zvenigorod,long=36.775,lat=55.695,elev=200,Nmeas=11,PI=Brent_Holben,Email=Brent.N.Holben@nasa.gov
    # AOD Level 2.0,Daily Averages,UNITS can be found at,,, http://aeronet.gsfc.nasa.gov/data_menu.html
    # Date(dd-mm-yy),Time(hh:mm:ss),Julian_Day,AOT_1640,AOT_1020,AOT_870,AOT_675,AOT_667,AOT_555,AOT_551,AOT_532,AOT_531,AOT_500,AOT_490,AOT_443,AOT_440,AOT_412,AOT_380,AOT_340,Water(cm),%TripletVar_1640,%TripletVar_1020,%TripletVar_870,%TripletVar_675,%TripletVar_667,%TripletVar_555,%TripletVar_551,%TripletVar_532,%TripletVar_531,%TripletVar_500,%TripletVar_490,%TripletVar_443,%TripletVar_440,%TripletVar_412,%TripletVar_380,%TripletVar_340,%WaterError,440-870Angstrom,380-500Angstrom,440-675Angstrom,500-870Angstrom,340-440Angstrom,440-675Angstrom(Polar),N[AOT_1640],N[AOT_1020],N[AOT_870],N[AOT_675],N[AOT_667],N[AOT_555],N[AOT_551],N[AOT_532],N[AOT_531],N[AOT_500],N[AOT_490],N[AOT_443],N[AOT_440],N[AOT_412],N[AOT_380],N[AOT_340],N[Water(cm)],N[440-870Angstrom],N[380-500Angstrom],N[440-675Angstrom],N[500-870Angstrom],N[340-440Angstrom],N[440-675Angstrom(Polar)]
    # 16:09:2006,00:00:00,259.000000,-9999.,0.036045,0.036734,0.039337,-9999.,-9999.,-9999.,-9999.,-9999.,0.064670,-9999.,-9999.,0.069614,-9999.,0.083549,0.092204,0.973909,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,1.126095,0.973741,1.474242,1.135232,1.114550,-9999.,-9999.,11,11,11,-9999.,-9999.,-9999.,-9999.,-9999.,11,-9999.,-9999.,11,-9999.,11,11,11,11,11,11,11,11,-9999.
    def __init__(self):
        super(ReadAeronetSunV2, self).__init__()
        #file column information
        self.col_info = _COL_INFO()
    
    def _add_additional_vars(self, vars_to_retrieve):
        added = False
        added_vars = []
        for var in vars_to_retrieve:
            if var in self.ADDITIONAL_REQUIRES:
                add_vars = self.ADDITIONAL_REQUIRES[var]
                for add_var in add_vars:
                    if not add_var in vars_to_retrieve:
                        added_vars.append(add_var)
                        added = True
        return (added, added_vars)
    
    def check_vars_to_retrieve(self, vars_to_retrieve):
        """Separate variables that are in file from those that are computed
        
        Some of the provided variables by this interface are not included in
        the data files but are computed within this class during data import
        (e.g. od550aer, ang4487aer). 
        
        The latter may require additional parameters to be retrieved from the 
        file, which is specified in the class header (cf. attribute
        ``ADDITIONAL_REQUIRES``).
        
        This function checks the input list that specifies all required 
        variables and separates them into two lists, one that includes all
        variables that can be read from the files and a second list that
        specifies all variables that are computed in this class.
        
        Parameters
        ----------
        vars_to_retrieve : list
            all parameter names that are supposed to be loaded
        
        Returns
        -------
        tuple
            2-element tuple, containing
            
            - list: list containing all variables to be read
            - list: list containing all variables to be computed
        
        Raises
        ------
        IOError
            if one of the variables is not supported by this interface
        """
        repeat = True
        while repeat:
            repeat, add_vars = self._add_additional_vars(vars_to_retrieve)
            # it is important to insert the additionally required variables in
            # the beginning, as these need to be computed first later on 
            # Example: if vars_to_retrieve=['od550aer'] then this loop will
            # find out that this requires 'ang4487aer' to be computed as 
            # well. So at the end of this function, ang4487aer needs to be 
            # before od550aer in the list vars_to_compute, since the method
            # @"compute_additional_vars" loops over that list in the specified
            # order
            vars_to_retrieve = add_vars + vars_to_retrieve
        
        # unique list containing all variables that are supposed to be read, 
        # either because they are required to be retrieved, or because they 
        # are supposed to be read because they are required to compute one 
        # of the output variables
        vars_to_retrieve = list(dict.fromkeys(vars_to_retrieve))
        
        # in the following, vars_to_retrieve is separated into two arrays, one 
        # containing all variables that can be read from the files, and the 
        # second containing all variables that are computed
        vars_to_read = []
        vars_to_compute = []
        
        for var in vars_to_retrieve:
            if var in self.col_info:
                vars_to_read.append(var)
            elif var in self.ADDITIONAL_REQUIRES:
                vars_to_compute.append(var)
            else:
                raise IOError("Variable {} not supported".format(var))
        return (vars_to_read, vars_to_compute)
    
    
    def compute_additional_vars(self, data, vars_to_compute):
        """Compute all additional variables
        
        The computations for each additional parameter are done using the 
        specified methods in ``ADDITIONAL_FUNS``.
        
        Parameters
        ----------
        data : dict-like
            data object containing imported results
        
        Returns
        -------
        dict
            updated data object
        """
        for var in vars_to_compute:
            data = self.ADDITIONAL_FUNS[var](data)
        return data
    
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
        if vars_to_retrieve is None:
            vars_to_retrieve = self.PROVIDES_VARIABLES
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
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
            data_out.head_line = in_file.readline()
            data_out.algorithm = in_file.readline()
            c_dummy = in_file.readline()
            # re.split(r'=|\,',c_dummy)
            i_dummy = iter(re.split(r'=|\,', c_dummy.rstrip()))
            dict_loc = dict(zip(i_dummy, i_dummy))

            data_out['latitude'] = float(dict_loc['lat'])
            data_out['longitude'] = float(dict_loc['long'])
            data_out['altitude'] = float(dict_loc['elev'])
            data_out['station name'] = dict_loc['Location']
            data_out['PI'] = dict_loc['PI']
            c_dummy = in_file.readline()
            #added to output
            data_out.data_header = in_file.readline()
            
            for line in in_file:
                # process line
                dummy_arr = line.split(',')
                
                day, month, year = dummy_arr[self.col_info['date']].split(':')
                
                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, dummy_arr[self.col_info['time']]])
                datestring = '+'.join([datestring, '00:00'])
                
                data_out['dtime'].append(np.datetime64(datestring))
                
                for var in vars_to_read:
                    val = float(dummy_arr[self.col_info[var]])
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
            (cf. :class:`_COL_INFO`) or computed during import 
            (cf. class attributes ``ADDITIONAL_REQUIRES`` and 
            ``ADDITIONAL_FUNS``)
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
                metadata[meta_key]['station name'] = station_data['station name']
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
################################################################################
### SORTED OUT
################################################################################
    def readOLD(self, vars_to_retrieve=['od550aer'], first_file=None, 
             last_file=None):
        """Read all data files into instance of :class:`UngriddedData` object
        
        Parameters
        ----------
        vars_to_retrieve : list
            list of variables that are supposed to be read from the files
            (cf. :class:`_COL_INFO`) or computed during import 
            (cf. class attributes ``ADDITIONAL_REQUIRES`` and 
            ``ADDITIONAL_FUNS``)
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
        self.logger.warning(DeprecationWarning("please use read method"))
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
        start_index = idx
        
        #assign metadata object
        metadata = data_obj.metadata
        
        for _file in sorted(files):
            try:
                station_data = self.read_file(_file, vars_to_retrieve,
                                              vars_as_series=True)
            
                # Fill the metatdata dict
                metadata[meta_key] = {}
                metadata[meta_key]['station name'] = station_data['station name']
                metadata[meta_key]['latitude'] = station_data['latitude']
                metadata[meta_key]['longitude'] = station_data['longitude']
                metadata[meta_key]['altitude'] = station_data['altitude']
                metadata[meta_key]['PI'] = station_data['PI']
                metadata[meta_key]['dataset_name'] = self.DATASET_NAME
    
                # this is a list with indexes of this station for each variable
                # not sure yet, if we really need that or if it speeds up things
                metadata[meta_key]['indexes'] = {}
                
                # variable index
                obs_var_index = 0
                
                for var in sorted(vars_to_retrieve):
                    times = np.float64(station_data.dtime)
                    
                    for i, val in enumerate(station_data[var].values):
                        data_obj._data[idx, data_obj._DATAINDEX] = val
                        data_obj._data[idx, data_obj._TIMEINDEX] = times[i]
                        # pd.TimeStamp.value is nano seconds since the epoch!
                        #data_obj._data[idx, data_obj._TIMEINDEX] = np.float64(time.value / 1.E9)
                        idx += 1
                        if idx >= data_obj._ROWNO:
                            # add another array chunk to data_obj._data
                            data_obj.add_chunk()
        
                    end_index = idx
                    # print(','.join([station_data['station name'], str(start_index), str(end_index), str(end_index - start_index)]))
                    metadata[meta_key]['indexes'][var] = np.arange(start_index, end_index)
                    data_obj._data[start_index:end_index, 
                                   data_obj._VARINDEX] = obs_var_index
                    data_obj._data[start_index:end_index, 
                                   data_obj._LATINDEX] = station_data['latitude']
                    data_obj._data[start_index:end_index, 
                                   data_obj._LONINDEX] = station_data['longitude']
                    data_obj._data[start_index:end_index, 
                                   data_obj._ALTITUDEINDEX] = station_data['altitude']
                    data_obj._data[start_index:end_index, 
                                   data_obj._METADATAKEYINDEX] = meta_key
                    start_index = idx
                    obs_var_index += 1
                meta_key += 1
            except:
                self.read_failed.append(_file)
                self.logger.exception("Failed to read file %s")
    
        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[0:end_index]
        self.data = data_obj
        return data_obj
    
if __name__=="__main__":
    
    read = ReadAeronetSunV2()
    
    read.verbosity_level = 'warning'
    
    files = read.get_file_list()

    data = read.readOLD(first_file=7, last_file=9)
    
    data_new = read.read(first_file=7, last_file=9)



