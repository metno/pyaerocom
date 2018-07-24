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

"""
Note
----
    This module has not yet been translated / shipped to the pyaerocom 
    library
"""
import os
import glob
import sys

import numpy as np

import pandas as pd
import re

from pyaerocom import const


class ReadAeronetSunV2:
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
    __version__ = "0.07"
    DATASET_NAME = const.AERONET_SUN_V2L2_AOD_DAILY_NAME
    DATASET_PATH = const.OBSCONFIG[const.AERONET_SUN_V2L2_AOD_DAILY_NAME]['PATH']
    # Flag if the dataset contains all years or not
    DATASET_IS_YEARLY = False

    _METADATAKEYINDEX = 0
    _TIMEINDEX = 1
    _LATINDEX = 2
    _LONINDEX = 3
    _ALTITUDEINDEX = 4
    _VARINDEX = 5
    _DATAINDEX = 6

    _COLNO = 11
    _ROWNO = 10000
    _CHUNKSIZE = 1000
    PROVIDES_VARIABLES = ['od500aer', 'od440aer', 'od870aer', 'ang4487aer', 'od550aer']

    def __init__(self, index_pointer=0, verbose=False):
        self.verbose = verbose
        self.metadata = {}
        self.data = []
        self.index = len(self.metadata)
        self.files = []
        #set the revision to the one from Revision.txt if that file exist
        self.revision = self.get_data_revision()

        # pointer to 1st free row in self.data
        # can be externally set so that in case the super class wants to read more than one data set
        # no data modification is needed to bring several data sets together
        self.index_pointer = index_pointer

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.metadata[float(self.index)]

    def __str__(self):
        stat_names = []
        for key in self.metadata:
            stat_names.append(self.metadata[key]['station_name'])

        return ','.join(stat_names)

    ###################################################################################

    def read_file(self, filename, vars_to_retrieve=['od550aer'], verbose=False):
        """method to read an Aeronet Sun V2 level 2 file and return it in a dictionary
        with the data variables as pandas time series

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : list
            list of str with variable names to read; defaults to ['od550aer']
        verbose : Bool
            set to True to increase verbosity

        Example
        -------
        >>> import pyaerocom.io.read_aeronet_sunv2
        >>> obj = pyaerocom.io.read_aeronet_sunv2.ReadAeronetSunV2()
        >>> filedata = obj.read_file('/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetRaw2.0/renamed/920801_170401_Zambezi.lev20')
        >>> print(filedata)
{'latitude': -13.533, 'longitude': 23.107, 'altitude': 1040.0, 'station_name': 'Zambezi', 'PI': 'Brent Holben', 'od550aer': 1996-08-10    0.801845
1996-08-11    1.062833
1996-08-12    0.850586
1996-08-13    0.839460
                ...
2000-09-22    1.304724
2000-09-23    1.197722
2000-09-24    1.035123
Length: 223, dtype: float64}
        """

        # Level 2.0. Quality Assured Data.<p>The following data are pre and post field calibrated, automatically cloud cleared and manually inspected.
        # Version 2 Direct Sun Algorithm
        # Location=Zvenigorod,long=36.775,lat=55.695,elev=200,Nmeas=11,PI=Brent_Holben,Email=Brent.N.Holben@nasa.gov
        # AOD Level 2.0,Daily Averages,UNITS can be found at,,, http://aeronet.gsfc.nasa.gov/data_menu.html
        # Date(dd-mm-yy),Time(hh:mm:ss),Julian_Day,AOT_1640,AOT_1020,AOT_870,AOT_675,AOT_667,AOT_555,AOT_551,AOT_532,AOT_531,AOT_500,AOT_490,AOT_443,AOT_440,AOT_412,AOT_380,AOT_340,Water(cm),%TripletVar_1640,%TripletVar_1020,%TripletVar_870,%TripletVar_675,%TripletVar_667,%TripletVar_555,%TripletVar_551,%TripletVar_532,%TripletVar_531,%TripletVar_500,%TripletVar_490,%TripletVar_443,%TripletVar_440,%TripletVar_412,%TripletVar_380,%TripletVar_340,%WaterError,440-870Angstrom,380-500Angstrom,440-675Angstrom,500-870Angstrom,340-440Angstrom,440-675Angstrom(Polar),N[AOT_1640],N[AOT_1020],N[AOT_870],N[AOT_675],N[AOT_667],N[AOT_555],N[AOT_551],N[AOT_532],N[AOT_531],N[AOT_500],N[AOT_490],N[AOT_443],N[AOT_440],N[AOT_412],N[AOT_380],N[AOT_340],N[Water(cm)],N[440-870Angstrom],N[380-500Angstrom],N[440-675Angstrom],N[500-870Angstrom],N[340-440Angstrom],N[440-675Angstrom(Polar)]
        # 16:09:2006,00:00:00,259.000000,-9999.,0.036045,0.036734,0.039337,-9999.,-9999.,-9999.,-9999.,-9999.,0.064670,-9999.,-9999.,0.069614,-9999.,0.083549,0.092204,0.973909,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,1.126095,0.973741,1.474242,1.135232,1.114550,-9999.,-9999.,11,11,11,-9999.,-9999.,-9999.,-9999.,-9999.,11,-9999.,-9999.,11,-9999.,11,11,11,11,11,11,11,11,-9999.

        # define some row numbers. not all of them are used at this point
        date_index = 0
        time_index = 1
        julien_day_index = 2
        od1640_index = 3
        od1020index = 4
        od870_index = 5
        od675index = 6
        od667index = 7
        od555index = 8
        od551index = 9
        od532index = 10
        od531index = 11
        od500_index = 12
        od440_index = 15
        od380index = 17
        od340index = 18

        # This value is later put to a np.nan
        nan_val = np.float_(-9999.)

        data_out = {}
        # Iterate over the lines of the file
        if verbose:
            sys.stderr.write(filename + '\n')
        with open(filename, 'rt') as in_file:
            c_head_line = in_file.readline()
            c_algorithm = in_file.readline()
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
            c_Header = in_file.readline()

            #
            #DataArr = {}
            dtime = []
            for var in self.PROVIDES_VARIABLES:
                data_out[var] = []

            for line in in_file:
                # process line
                dummy_arr = line.split(',')
                # the following uses the standatd python datetime functions
                day, month, year = dummy_arr[date_index].split(':')
                hour, minute, second = dummy_arr[time_index].split(':')

                # This uses the numpy datestring64 functions that e.g. also support Months as a time step for timedelta
                # Build a proper ISO 8601 UTC date string
                day, month, year = dummy_arr[date_index].split(':')
                # pdb.set_trace()
                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, dummy_arr[time_index]])
                datestring = '+'.join([datestring, '00:00'])
                dtime.append(np.datetime64(datestring))

                data_out['od500aer'].append(np.float_(dummy_arr[od500_index]))
                if data_out['od500aer'][-1] == nan_val: data_out['od500aer'][-1] = np.nan
                data_out['od440aer'].append(np.float_(dummy_arr[od440_index]))
                if data_out['od440aer'][-1] == nan_val: data_out['od440aer'][-1] = np.nan
                data_out['od870aer'].append(np.float_(dummy_arr[od870_index]))
                if data_out['od870aer'][-1] == nan_val: data_out['od870aer'][-1] = np.nan

                data_out['ang4487aer'].append(
                    -1.0 * np.log(data_out['od440aer'][-1] / data_out['od870aer'][-1]) / np.log(0.44 / .870))
                data_out['od550aer'].append(
                    data_out['od500aer'][-1] * (0.55 / 0.50) ** (np.float_(-1.) * data_out['ang4487aer'][-1]))
                # ;fill up time steps of the now calculated od550_aer that are nans with values calculated from the
                # ;440nm wavelength to minimise gaps in the time series
                if np.isnan(data_out['od550aer'][-1]):
                    temp = data_out['od440aer'][-1] * (0.55 / 0.44) ** (np.float_(-1.) * data_out['ang4487aer'][-1])
                    if not np.isnan(temp) and temp > 0.:
                        data_out['od550aer'][-1] = temp #data_out['od440aer'][-1] * (0.55 / 0.44) ** (np.float_(-1.) * data_out['ang4487aer'][-1])
                if data_out['od550aer'][-1] < const.VAR_PARAM['od550aer']['lower_limit']:
                   data_out['od550aer'][-1] = np.nan

        # convert  the vars in vars_to_retrieve to pandas time series
        # and delete the other ones
        for var in self.PROVIDES_VARIABLES:
            if var in vars_to_retrieve:
                data_out[var] = pd.Series(data_out[var], index=dtime)
            else:
                del data_out[var]

        return data_out

    ###################################################################################

    def read(self, vars_to_retrieve=['od550aer'], verbose=False):
        """method to read all files in self.files into self.data and self.metadata

        Example
        -------
        >>> import pyaerocom.io.read_aeronet_sunv2
        >>> obj = pyaerocom.io.read_aeronet_sunv2.ReadAeronetSunV2()
        >>> obj.read(verbose=True)
        """

        # Metadata key is float because the numpy array holding it is float

        meta_key = 0.
        self.files = self.get_file_list()
        self.data = np.empty([self._ROWNO, self._COLNO], dtype=np.float64)

        for _file in sorted(self.files):
            if self.verbose:
                sys.stdout.write(_file+"\n")
            stat_obs_data = self.read_file(_file, vars_to_retrieve = vars_to_retrieve)
            # Fill the metatdata dict
            self.metadata[meta_key] = {}
            self.metadata[meta_key]['station_name'] = stat_obs_data['station_name']
            self.metadata[meta_key]['latitude'] = stat_obs_data['latitude']
            self.metadata[meta_key]['longitude'] = stat_obs_data['longitude']
            self.metadata[meta_key]['altitude'] = stat_obs_data['altitude']
            self.metadata[meta_key]['PI'] = stat_obs_data['PI']
            self.metadata[meta_key]['dataset_name'] = self.DATASET_NAME

            # this is a list with indices of this station for each variable
            # not sure yet, if we really need that or if it speeds up things
            self.metadata[meta_key]['idx'] = {}
            start_index = self.index_pointer
            # variable index
            obs_var_index = 0
            for var in sorted(vars_to_retrieve):
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
                # print(','.join([stat_obs_data['station_name'], str(start_index), str(end_index), str(end_index - start_index)]))
                self.metadata[meta_key]['idx'][var] = np.arange(start_index, end_index)
                self.data[start_index:end_index, self._VARINDEX] = obs_var_index
                self.data[start_index:end_index, self._LATINDEX] = stat_obs_data['latitude']
                self.data[start_index:end_index, self._LONINDEX] = stat_obs_data['longitude']
                self.data[start_index:end_index, self._ALTITUDEINDEX] = stat_obs_data['altitude']
                self.data[start_index:end_index, self._METADATAKEYINDEX] = meta_key
                start_index = self.index_pointer
                obs_var_index += 1
            meta_key = meta_key + 1.
    
        # shorten self.data to the right number of points
        self.data = self.data[0:end_index]


    ###################################################################################

    def get_file_list(self):
        """search for files to read """

        if self.verbose:
            print('searching for data files. This might take a while...')
        files = glob.glob(os.path.join(self.DATASET_PATH,
                                       self._FILEMASK))
        return files

    ###################################################################################

    def get_data_revision(self):
        """method to read the revision string from the file Revision.txt in the main data directory"""

        revision_file = os.path.join(self.DATASET_PATH, const.REVISION_FILE)
        revision = 'unset'
        if os.path.isfile(revision_file):
            with open(revision_file, 'rt') as in_file:
                revision = in_file.readline().strip()
                in_file.close()

            self.revision = revision

