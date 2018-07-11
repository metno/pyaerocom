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

import sys
import numpy as np
import pandas as pd
import re
import fnmatch

from pyaerocom import const
from pyaerocom.mathutils import compute_angstrom_coeff
from pyaerocom.utils import _BrowserDict
from pyaerocom.io import ReadUngriddedBase, TimeSeriesFileData

# define some row numbers. not all of them are used at this point
class _COL_INFO(_BrowserDict):
    """Header index info for AeronetSunV2 files
    
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
    
class ReadAeronetSunV2(ReadUngriddedBase):
    """Interface for reading Aeronet direct sun version 2 Level 2.0 data

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
    _FILEMASK = '*.lev20'
    __version__ = "0.08"
    DATASET_NAME = const.AERONET_SUN_V2L2_AOD_DAILY_NAME
    
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
    # the AODs at 440, 500 and 870 nm
    ADDITIONAL_REQUIRES = {"od550aer"   :   {vars_req : ['od440aer',
                                                         'od500aer',
                                                         'od870aer']}}
    # Level 2.0. Quality Assured Data.<p>The following data are pre and post field calibrated, automatically cloud cleared and manually inspected.
    # Version 2 Direct Sun Algorithm
    # Location=Zvenigorod,long=36.775,lat=55.695,elev=200,Nmeas=11,PI=Brent_Holben,Email=Brent.N.Holben@nasa.gov
    # AOD Level 2.0,Daily Averages,UNITS can be found at,,, http://aeronet.gsfc.nasa.gov/data_menu.html
    # Date(dd-mm-yy),Time(hh:mm:ss),Julian_Day,AOT_1640,AOT_1020,AOT_870,AOT_675,AOT_667,AOT_555,AOT_551,AOT_532,AOT_531,AOT_500,AOT_490,AOT_443,AOT_440,AOT_412,AOT_380,AOT_340,Water(cm),%TripletVar_1640,%TripletVar_1020,%TripletVar_870,%TripletVar_675,%TripletVar_667,%TripletVar_555,%TripletVar_551,%TripletVar_532,%TripletVar_531,%TripletVar_500,%TripletVar_490,%TripletVar_443,%TripletVar_440,%TripletVar_412,%TripletVar_380,%TripletVar_340,%WaterError,440-870Angstrom,380-500Angstrom,440-675Angstrom,500-870Angstrom,340-440Angstrom,440-675Angstrom(Polar),N[AOT_1640],N[AOT_1020],N[AOT_870],N[AOT_675],N[AOT_667],N[AOT_555],N[AOT_551],N[AOT_532],N[AOT_531],N[AOT_500],N[AOT_490],N[AOT_443],N[AOT_440],N[AOT_412],N[AOT_380],N[AOT_340],N[Water(cm)],N[440-870Angstrom],N[380-500Angstrom],N[440-675Angstrom],N[500-870Angstrom],N[340-440Angstrom],N[440-675Angstrom(Polar)]
    # 16:09:2006,00:00:00,259.000000,-9999.,0.036045,0.036734,0.039337,-9999.,-9999.,-9999.,-9999.,-9999.,0.064670,-9999.,-9999.,0.069614,-9999.,0.083549,0.092204,0.973909,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,1.126095,0.973741,1.474242,1.135232,1.114550,-9999.,-9999.,11,11,11,-9999.,-9999.,-9999.,-9999.,-9999.,11,-9999.,-9999.,11,-9999.,11,11,11,11,11,11,11,11,-9999.
    def __init__(self, **kwargs):
        super(ReadAeronetSunV2, self).__init__(**kwargs)
        #file column information
        self.file_cols = _COL_INFO()
        
    def _compute_additional_vars(self, vars_to_compute, data):
        """Compute additional variables after reading file
        
        Parameters
        ----------
        vars_to_compute : list
            list of additional variables to be computed
        data : dict-like
            data from file
        """
        for var in vars_to_compute:
            if not var in self.ADDITIONAL_REQUIRES:
                raise KeyError("Variable {} not supported")
    
    def _compute_od550aer(self, od440aer, od500aer, od870aer):
        ang4487aer = compute_angstrom_coeff(od440aer, od870aer, .44, .87)
        
        od550aer = od500aer * (0.5 / 0.55) ** ang4487aer
        
        # ;fill up time steps of the now calculated od550_aer that are nans with values calculated from the
        # ;440nm wavelength to minimise gaps in the time series
        if np.isnan(data_out['od550aer'][-1]):
            temp = data_out['od440aer'][-1] * (0.55 / 0.44) ** (np.float_(-1.) * data_out['ang4487aer'][-1])
            if not np.isnan(temp) and temp > 0.:
                data_out['od550aer'][-1] = (data_out['od440aer'][-1] * (0.55 / 0.44) **
                                            (np.float_(-1.) * data_out['ang4487aer'][-1]))
        if data_out['od550aer'][-1] < const.VAR_PARAM['od550aer']['lower_limit']:
           data_out['od550aer'][-1] = np.nan
    def read_file(self, filename, vars_to_read=['od550aer']):
        """Read Aeronet Sun V2 level 2 file 

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_read : list
            list of str with variable names to read; defaults to ['od550aer']
        verbose : Bool
            set to True to increase verbosity

        Example
        -------
        >>> import pyaerocom.io.read_aeronet_sunv2
        >>> obj = pyaerocom.io.read_aeronet_sunv2.ReadAeronetSunV2()
        >>> filedata = obj.read_file('/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetRaw2.0/renamed/920801_170401_Zambezi.lev20')
        >>> print(filedata)
{'latitude': -13.533, 'longitude': 23.107, 'altitude': 1040.0, 'station name': 'Zambezi', 'PI': 'Brent Holben', 'od550aer': 1996-08-10    0.801845
1996-08-11    1.062833
1996-08-12    0.850586
1996-08-13    0.839460
                ...
2000-09-22    1.304724
2000-09-23    1.197722
2000-09-24    1.035123
Length: 223, dtype: float64}
        """
        if vars_to_read is None:
            vars_to_read = self.PROVIDES_VARIABLES
        elif isinstance(vars_to_read, str):
            vars_to_read = [vars_to_read]
            
        # This value is later put to a np.nan
        nan_val = np.float_(-9999.)

        data_out = TimeSeriesFileData()
        
        
        vars_to_compute = []
        for var in vars_to_read:
            data_out[var] = []
            if not var in self.cols: #e.g. od550aer
                
        # Iterate over the lines of the file
        if self.verbose:
            sys.stderr.write(filename + '\n')
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
                
                day, month, year = dummy_arr[self.file_cols.date].split(':')
                
                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, dummy_arr[self.file_cols.time]])
                datestring = '+'.join([datestring, '00:00'])
                
                data_out.time.append(np.datetime64(datestring))
                
                
                data_out['od500aer'].append(np.float_(dummy_arr[self.file_cols.od500aer]))
                if data_out['od500aer'][-1] == nan_val: data_out['od500aer'][-1] = np.nan
                data_out['od440aer'].append(np.float_(dummy_arr[od440_index]))
                if data_out['od440aer'][-1] == nan_val: data_out['od440aer'][-1] = np.nan
                data_out['od870aer'].append(np.float_(dummy_arr[od870_index]))
                if data_out['od870aer'][-1] == nan_val: data_out['od870aer'][-1] = np.nan

                data_out['ang4487aer'].append(
                    -1.0 * np.log(data_out['od440aer'][-1] / data_out['od870aer'][-1]) / np.log(0.44 / .87))
                data_out['od550aer'].append(
                    data_out['od500aer'][-1] * (0.55 / 0.50) ** (np.float_(-1.) * data_out['ang4487aer'][-1]))
                # ;fill up time steps of the now calculated od550_aer that are nans with values calculated from the
                # ;440nm wavelength to minimise gaps in the time series
                if np.isnan(data_out['od550aer'][-1]):
                    temp = data_out['od440aer'][-1] * (0.55 / 0.44) ** (np.float_(-1.) * data_out['ang4487aer'][-1])
                    if not np.isnan(temp) and temp > 0.:
                        data_out['od550aer'][-1] = (data_out['od440aer'][-1] * (0.55 / 0.44) **
                                                    (np.float_(-1.) * data_out['ang4487aer'][-1]))
                if data_out['od550aer'][-1] < const.VAR_PARAM['od550aer']['lower_limit']:
                   data_out['od550aer'][-1] = np.nan

        # convert  the vars in vars_to_read to pandas time series
        # and delete the other ones
        for var in self.PROVIDES_VARIABLES:
            if var in vars_to_read:
                data_out[var] = pd.Series(data_out[var], index=dtime)
            else:
                del data_out[var]

        return data_out

    ###################################################################################

    def read(self, vars_to_read=['od550aer']):
        """method to read all files in self.files into self.data and self.metadata

        Example
        -------
        >>> import pyaerocom.io.read_aeronet_sunv2
        >>> obj = pyaerocom.io.read_aeronet_sunv2.ReadAeronetSunV2()
        >>> obj.read(verbose=True)
        """

        # Metadata key is float because the numpy array holding it is float

        met_data_key = 0.
        self.files = self.get_file_list()
        self.data = np.empty([self._ROWNO, self._COLNO], dtype=np.float64)

        for _file in sorted(self.files):
            if self.verbose:
                sys.stdout.write(_file+"\n")
            stat_obs_data = self.read_file(_file, vars_to_read = vars_to_read)
            # Fill the metatdata dict
            self.metadata[met_data_key] = {}
            self.metadata[met_data_key]['station name'] = stat_obs_data['station name']
            self.metadata[met_data_key]['latitude'] = stat_obs_data['latitude']
            self.metadata[met_data_key]['longitude'] = stat_obs_data['longitude']
            self.metadata[met_data_key]['altitude'] = stat_obs_data['altitude']
            self.metadata[met_data_key]['PI'] = stat_obs_data['PI']
            self.metadata[met_data_key]['dataset_name'] = self.DATASET_NAME

            # this is a list with indexes of this station for each variable
            # not sure yet, if we really need that or if it speeds up things
            self.metadata[met_data_key]['indexes'] = {}
            start_index = self.index_pointer
            # variable index
            obs_var_index = 0
            for var in sorted(vars_to_read):
                for time, val in stat_obs_data[var].iteritems():
                    self.data[self.index_pointer, self._DATAINDEX] = val
                    # pd.TimeStamp.value is nano seconds since the epoch!
                    self.data[self.index_pointer, self._TIMEINDEX] = np.float64(time.value / 1.E9)
                    self.index_pointer += 1
                    if self.index_pointer >= self._ROWNO:
                        # add another array chunk to self.data
                        self.data = np.append(self.data, np.zeros([self._CHUNKSIZE, self._COLNO], dtype=np.float64), axis=0)
                        self._ROWNO += self._CHUNKSIZE
    
                end_index = self.index_pointer
                # print(','.join([stat_obs_data['station name'], str(start_index), str(end_index), str(end_index - start_index)]))
                self.metadata[met_data_key]['indexes'][var] = np.arange(start_index, end_index)
                self.data[start_index:end_index, self._VARINDEX] = obs_var_index
                self.data[start_index:end_index, self._LATINDEX] = stat_obs_data['latitude']
                self.data[start_index:end_index, self._LONINDEX] = stat_obs_data['longitude']
                self.data[start_index:end_index, self._ALTITUDEINDEX] = stat_obs_data['altitude']
                self.data[start_index:end_index, self._METADATAKEYINDEX] = met_data_key
                start_index = self.index_pointer
                obs_var_index += 1
            met_data_key = met_data_key + 1.
    
        # shorten self.data to the right number of points
        self.data = self.data[0:end_index]
        
if __name__=="__main__":
    
    read = ReadAeronetSunV2(verbose=True)
    
    data = read.read_first_file()



