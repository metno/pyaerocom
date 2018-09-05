################################################################
# read_aeronet_sunv3.py
#
# read Aeronet direct sun V3 data
#
# this file is part of the pyaerocom package
#
#################################################################
# Created 20180626 by Jan Griesfeller for Met Norway
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
read Aeronet direct sun V3 data
"""
import os
import glob
import sys

import numpy as np

import pandas as pd

from pyaerocom import const

# TODO: flag somehow the values that are postcomputed during read (e.g. AODs
# at 550nm that are missing, using angstrom exponent and values at 440 and 
# 870 nm). The same applied for other Aeronet reading classes. Maybe it is 
# better to do this in post on request and leave the original data as is? 
class ReadAeronetSunV3:
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
    __version__ = "0.01"
    DATASET_NAME = const.AERONET_SUN_V3L15_AOD_DAILY_NAME
    DATASET_PATH = const.OBSCONFIG[const.AERONET_SUN_V3L15_AOD_DAILY_NAME]['PATH']
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

    # data vars
    # will be stored as pandas time series
    VAR_NAMES_FILE = {}
    VAR_NAMES_FILE['od340aer'] = 'AOD_340nm'
    VAR_NAMES_FILE['od440aer'] = 'AOD_440nm'
    VAR_NAMES_FILE['od500aer'] = 'AOD_500nm'
    # VAR_NAMES_FILE['od865aer'] = 'AOD_865nm'
    VAR_NAMES_FILE['od870aer'] = 'AOD_870nm'
    VAR_NAMES_FILE['ang4487aer'] = '440-870_Angstrom_Exponent'

    # meta data vars
    # will be stored as array of strings
    META_NAMES_FILE = {}
    META_NAMES_FILE['data_quality_level'] = 'Data_Quality_Level'
    META_NAMES_FILE['instrument_number'] = 'AERONET_Instrument_Number'
    META_NAMES_FILE['station_name'] = 'AERONET_Site'
    META_NAMES_FILE['latitude'] = 'Site_Latitude(Degrees)'
    META_NAMES_FILE['longitude'] = 'Site_Longitude(Degrees)'
    META_NAMES_FILE['altitude'] = 'Site_Elevation(m)'
    META_NAMES_FILE['date'] = 'Date(dd:mm:yyyy)'
    META_NAMES_FILE['time'] = 'Time(hh:mm:ss)'
    META_NAMES_FILE['day_of_year'] = 'Day_of_Year'

    # additional vars
    # calculated
    AUX_COLNAMES = []
    AUX_COLNAMES.append('ang4487aer_calc')
    AUX_COLNAMES.append('od550aer')

    PROVIDES_VARIABLES = list(VAR_NAMES_FILE.keys())
    for col in AUX_COLNAMES:
        PROVIDES_VARIABLES.append(col)

    # COLNAMES_USED = {y:x for x,y in AUX_COLNAMES.items()}

    def __init__(self, index_pointer=0, dataset_to_read=None, verbose=False):
        self.verbose = verbose
        self.metadata = {}
        self.data = []
        self.index = len(self.metadata)
        self.files = []
        # the reading actually works for all V3 direct sun data sets
        # so just adjust the name and the path here
        # const.AERONET_SUN_V3L15_AOD_DAILY_NAME is the default
        if dataset_to_read is None:
            pass
            # self.dataset_name = const.AERONET_SUN_V3L15_AOD_DAILY_NAME
            # self.dataset_path = const.OBSCONFIG[const.AERONET_SUN_V3L15_AOD_DAILY_NAME]['PATH']
        elif dataset_to_read == const.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME:
            self.DATASET_NAME = const.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME
            self.DATASET_PATH = const.OBSCONFIG[const.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME]['PATH']
        elif dataset_to_read == const.AERONET_SUN_V3L2_AOD_DAILY_NAME:
            self.DATASET_NAME = const.AERONET_SUN_V3L2_AOD_DAILY_NAME
            self.DATASET_PATH = const.OBSCONFIG[const.AERONET_SUN_V3L2_AOD_DAILY_NAME]['PATH']
        elif dataset_to_read == const.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME:
            self.DATASET_NAME = const.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME
            self.DATASET_PATH = const.OBSCONFIG[const.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME]['PATH']


        # set the revision to the one from Revision.txt if that file exist
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
        """method to read an Aeronet Sun V3 level 1.5 file and return it in a dictionary
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
        >>> import pyaerocom.io.read_aeronet_sunv3
        >>> obj = pyaerocom.io.read_aeronet_sunv3.ReadAeronetSunV3()
        >>> filename = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev1.5.daily/renamed/Karlsruhe.lev30'
        >>> filename = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev1.5.AP/renamed/Karlsruhe.lev30'
        >>> filedata = obj.read_file(filename)
        >>> print(filedata)
{'PI': 'Brent_Holben', 'PI_email': 'Brent.N.Holben@nasa.gov\n', 'od550aer': 2005-03-21 12:00:00    0.238024
2005-03-23 12:00:00    0.268991
2005-03-24 12:00:00    0.641364
                         ...
2018-04-28 12:00:00         NaN
2018-04-29 12:00:00    0.161189
2018-04-30 12:00:00    0.058717
2018-05-01 12:00:00    0.083875
2018-05-03 12:00:00    0.326524
2018-05-04 12:00:00    0.277096
2018-05-05 12:00:00    0.272977
2018-05-06 12:00:00    0.083989
2018-05-07 12:00:00    0.084507
2018-05-08 12:00:00    0.078192
2018-05-09 12:00:00    0.172097
2018-05-11 12:00:00    0.326830
2018-05-12 12:00:00    0.311610
Length: 1424, dtype: float64, 'data_quality_level': ['lev15', 'l...
        """

        # DAILY DATA:
        # ===========
        # AERONET Version 3;
        # Cuiaba
        # Version 3: AOD Level 1.5
        # The following data are cloud cleared and quality controls have been applied but these data may not have final calibration applied.  These data may change.
        # Contact: PI=Brent_Holben; PI Email=Brent.N.Holben@nasa.gov
        # Daily Averages,UNITS can be found at,,, https://aeronet.gsfc.nasa.gov/new_web/units.html
        # AERONET_Site,Date(dd:mm:yyyy),Time(hh:mm:ss),Day_of_Year,AOD_1640nm,AOD_1020nm,AOD_870nm,AOD_865nm,AOD_779nm,AOD_675nm,AOD_667nm,AOD_620nm,AOD_560nm,AOD_555nm,AOD_551nm,AOD_532nm,AOD_531nm,AOD_510nm,AOD_500nm,AOD_490nm,AOD_443nm,AOD_440nm,AOD_412nm,AOD_400nm,AOD_380nm,AOD_340nm,Precipitable_Water(cm),AOD_681nm,AOD_709nm,AOD_Empty,AOD_Empty,AOD_Empty,AOD_Empty,AOD_Empty,440-870_Angstrom_Exponent,380-500_Angstrom_Exponent,440-675_Angstrom_Exponent,500-870_Angstrom_Exponent,340-440_Angstrom_Exponent,440-675_Angstrom_Exponent[Polar],N[AOD_1640nm],N[AOD_1020nm],N[AOD_870nm],N[AOD_865nm],N[AOD_779nm],N[AOD_675nm],N[AOD_667nm],N[AOD_620nm],N[AOD_560nm],N[AOD_555nm],N[AOD_551nm],N[AOD_532nm],N[AOD_531nm],N[AOD_510nm],N[AOD_500nm],N[AOD_490nm],N[AOD_443nm],N[AOD_440nm],N[AOD_412nm],N[AOD_400nm],N[AOD_380nm],N[AOD_340nm],N[Precipitable_Water(cm)],N[AOD_681nm],N[AOD_709nm],N[AOD_Empty],N[AOD_Empty],N[AOD_Empty],N[AOD_Empty],N[AOD_Empty],N[440-870_Angstrom_Exponent],N[380-500_Angstrom_Exponent],N[440-675_Angstrom_Exponent],N[500-870_Angstrom_Exponent],N[340-440_Angstrom_Exponent],N[440-675_Angstrom_Exponent[Polar]],
        # Data_Quality_Level,AERONET_Instrument_Number,AERONET_Site_Name,Site_Latitude(Degrees),Site_Longitude(Degrees),Site_Elevation(m)
        # Karlsruhe,21:03:2005,12:00:00,80,-999.,0.222846,0.222462,-999.,-999.,0.224444,-999.,-999.,-999.,-999.,-999.,-999.,-999.,-999.,0.242872,-999.,-999.,0.256999,-999.,-999.,0.276636,0.283760,0.733243,-999.,-999.,-999.,-999.,-999.,-999.,-999.,0.211561,0.473610,0.306976,0.161805,0.391631,-999.,0,2,2,0,0,2,0,0,0,0,0,0,0,0,2,0,0,2,0,0,2,2,2,0,0,0,0,0,0,0,2,2,2,2,2,0,lev15,325,Karlsruhe,49.093300,8.427900,140.000000

        # ALL POINT DATA
        # ==============
        # AERONET Version 3;
        # Cuiaba
        # Version 3: AOD Level 1.5
        # The following data are cloud cleared and quality controls have been applied but these data may not have final calibration applied.  These data may change.
        # Contact: PI=Brent_Holben; PI Email=Brent.N.Holben@nasa.gov
        # All Points,UNITS can be found at,,, https://aeronet.gsfc.nasa.gov/new_web/units.html
        # AERONET_Site,Date(dd:mm:yyyy),Time(hh:mm:ss),Day_of_Year,Day_of_Year(Fraction),AOD_1640nm,AOD_1020nm,AOD_870nm,AOD_865nm,AOD_779nm,AOD_675nm,AOD_667nm,AOD_620nm,AOD_560nm,AOD_555nm,AOD_551nm,AOD_532nm,AOD_531nm,AOD_510nm,AOD_500nm,AOD_490nm,AOD_443nm,AOD_440nm,AOD_412nm,AOD_400nm,AOD_380nm,AOD_340nm,Precipitable_Water(cm),AOD_681nm,AOD_709nm,AOD_Empty,AOD_Empty,AOD_Empty,AOD_Empty,AOD_Empty,Triplet_Variability_1640,Triplet_Variability_1020,Triplet_Variability_870,Triplet_Variability_865,Triplet_Variability_779,Triplet_Variability_675,Triplet_Variability_667,Triplet_Variability_620,Triplet_Variability_560,Triplet_Variability_555,Triplet_Variability_551,Triplet_Variability_532,Triplet_Variability_531,Triplet_Variability_510,Triplet_Variability_500,Triplet_Variability_490,Triplet_Variability_443,Triplet_Variability_440,Triplet_Variability_412,Triplet_Variability_400,Triplet_Variability_380,Triplet_Variability_340,Triplet_Variability_Precipitable_Water(cm),Triplet_Variability_681,Triplet_Variability_709,Triplet_Variability_AOD_Empty,Triplet_Variability_AOD_Empty,Triplet_Variability_AOD_Empty,Triplet_Variability_AOD_Empty,Triplet_Variability_AOD_Empty,440-870_Angstrom_Exponent,380-500_Angstrom_Exponent,440-675_Angstrom_Exponent,500-870_Angstrom_Exponent,340-440_Angstrom_Exponent,440-675_Angstrom_Exponent[Polar],Data_Quality_Level,AERONET_Instrument_Number,AERONET_Site_Name,Site_Latitude(Degrees),Site_Longitude(Degrees),Site_Elevation(m),Solar_Zenith_Angle(Degrees),Optical_Air_Mass,Sensor_Temperature(Degrees_C),Ozone(Dobson),NO2(Dobson),Last_Date_Processed,Number_of_Wavelengths,Exact_Wavelengths_of_AOD(um)_1640nm,Exact_Wavelengths_of_AOD(um)_1020nm,Exact_Wavelengths_of_AOD(um)_870nm,Exact_Wavelengths_of_AOD(um)_865nm,Exact_Wavelengths_of_AOD(um)_779nm,Exact_Wavelengths_of_AOD(um)_675nm,Exact_Wavelengths_of_AOD(um)_667nm,Exact_Wavelengths_of_AOD(um)_620nm,Exact_Wavelengths_of_AOD(um)_560nm,Exact_Wavelengths_of_AOD(um)_555nm,Exact_Wavelengths_of_AOD(um)_551nm,Exact_Wavelengths_of_AOD(um)_532nm,Exact_Wavelengths_of_AOD(um)_531nm,Exact_Wavelengths_of_AOD(um)_510nm,Exact_Wavelengths_of_AOD(um)_500nm,Exact_Wavelengths_of_AOD(um)_490nm,Exact_Wavelengths_of_AOD(um)_443nm,Exact_Wavelengths_of_AOD(um)_440nm,Exact_Wavelengths_of_AOD(um)_412nm,Exact_Wavelengths_of_AOD(um)_400nm,Exact_Wavelengths_of_AOD(um)_380nm,Exact_Wavelengths_of_AOD(um)_340nm,Exact_Wavelengths_of_PW(um)_935nm,Exact_Wavelengths_of_AOD(um)_681nm,Exact_Wavelengths_of_AOD(um)_709nm,Exact_Wavelengths_of_AOD(um)_Empty,Exact_Wavelengths_of_AOD(um)_Empty,Exact_Wavelengths_of_AOD(um)_Empty,Exact_Wavelengths_of_AOD(um)_Empty,Exact_Wavelengths_of_AOD(um)_Empty
        # Karlsruhe,21:03:2005,16:35:13,80,80.691123,-999.000000,0.217930,0.217887,-999.000000,-999.000000,0.220243,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,0.238660,-999.000000,-999.000000,0.252361,-999.000000,-999.000000,0.271864,0.278779,0.733072,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,0.009736,0.009758,-999.000000,-999.000000,0.008882,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,0.008965,-999.000000,-999.000000,0.007377,-999.000000,-999.000000,0.007786,0.005861,0.040874,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,0.215628,0.474049,0.309065,0.167603,0.393740,-999.000000,lev15,325,Karlsruhe,49.093300,8.427900,140.000000,80.094832,5.635644,19.000000,0.368148,0.434568,07:12:2017,8,-999.,1.019300,0.870200,-999.,-999.,0.674800,-999.,-999.,-999.,-999.,-999.,-999.,-999.,-999.,0.500400,-999.,-999.,0.439600,-999.,-999.,0.380000,0.340000,0.941100,-999.,-999.,-999.,-999.,-999.,-999.,-999.


        # This value is later put to a np.nan
        nan_val = np.float_(-9999.)
        
        data_out = {}
        dict_loc={}
        # Iterate over the lines of the file
        if verbose:
            sys.stderr.write(filename + '\n')
        with open(filename, 'rt') as in_file:
            line_1 = in_file.readline()
            line_2 = in_file.readline()
            line_3 = in_file.readline()
            line_4 = in_file.readline()
            # PI line
            dummy_arr = in_file.readline().strip().split(';')
            data_out['PI'] = dummy_arr[0].split('=')[1]
            data_out['PI_email'] = dummy_arr[1].split('=')[1]

            data_type_comment = in_file.readline()
            # line_7 = in_file.readline()
            # put together a dict with the header string as key and the index number as value so that we can access
            # the index number via the header string
            headers = in_file.readline().strip().split(',')
            index_str = {}
            _index = 0
            for header in headers:
                index_str[header] = _index
                _index += 1

            data_line_no = 1
            dtime = []
            for var in self.PROVIDES_VARIABLES:
                data_out[var] = []
            # add time variable location
            for var in self.META_NAMES_FILE:
                data_out[var] = []

            for line in in_file:
                # process line
                dummy_arr = line.split(',')
                # the following uses the standard python datetime functions
                # date_index = index_str[COLNAMES['date']]
                # hour, minute, second = dummy_arr[index_str[COLNAMES['time']].split(':')

                # This uses the numpy datestring64 functions that e.g. also support Months as a time step for timedelta
                # Build a proper ISO 8601 UTC date string
                day, month, year = dummy_arr[index_str[self.META_NAMES_FILE['date']]].split(':')
                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, dummy_arr[index_str[self.META_NAMES_FILE['time']]]])
                datestring = '+'.join([datestring, '00:00'])
                dtime.append(np.datetime64(datestring))

                # copy the meta data (array of type string)
                for var in self.META_NAMES_FILE:
                    if len(self.META_NAMES_FILE[var]) == 0: continue
                    data_out[var].append(dummy_arr[index_str[self.META_NAMES_FILE[var]]])

                # copy the data fields (array type np.float_; will be converted to pandas.Series later)
                for var in self.VAR_NAMES_FILE:
                    data_out[var].append(np.float_(dummy_arr[index_str[self.VAR_NAMES_FILE[var]]]))
                    if data_out[var][-1] == nan_val: data_out[var][-1] = np.nan

                # some stuff needs to be calculated
                data_out['ang4487aer_calc'].append(
                    -1.0 * np.log(data_out['od440aer'][-1] / data_out['od870aer'][-1]) / np.log(0.44 / .870))
                data_out['od550aer'].append(
                    data_out['od500aer'][-1] * (0.55 / 0.50) ** (np.float_(-1.) * data_out['ang4487aer'][-1]))
                # fill up time steps of the now calculated od550aer that are nans with values calculated from the
                # 440nm wavelength to minimise gaps in the time series
                if np.isnan(data_out['od550aer'][-1]):
                    temp = data_out['od440aer'][-1] * (0.55 / 0.44) ** (np.float_(-1.) * data_out['ang4487aer'][-1])
                    if not np.isnan(temp) and temp > 0.:
                        data_out['od550aer'][-1] = (data_out['od440aer'][-1] * (0.55 / 0.44) **
                                                    (np.float_(-1.) * data_out['ang4487aer'][-1]))
                # apply the lower limit for od550aer
                if data_out['od550aer'][-1] < const.VAR_PARAM['od550aer']['minimum']:
                    data_out['od550aer'][-1] = np.nan
                data_line_no += 1

        # convert the vars in vars_to_retrieve to pandas time series
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
        >>> import pyaerocom.io.read_aeronet_sunv3
        >>> obj = pyaerocom.io.read_aeronet_sunv3.ReadAeronetSunV3()
        >>> obj.read(verbose=True)
        """

        # Metadata key is float because the numpy array holding it is float

        meta_key = 0.
        self.files = self.get_file_list()
        self.data = np.empty([self._ROWNO, self._COLNO], dtype=np.float_)

        for _file in sorted(self.files):
            if self.verbose:
                sys.stdout.write(_file + "\n")
            stat_obs_data = self.read_file(_file, vars_to_retrieve=vars_to_retrieve)
            # Fill the metatdata dict
            # the location in the data set is time step dependant!
            # use the lat location here since we have to choose one location
            # in the time series plot
            self.metadata[meta_key] = {}
            self.metadata[meta_key]['station_name'] = stat_obs_data['station_name'][-1]
            self.metadata[meta_key]['latitude'] = stat_obs_data['latitude'][-1]
            self.metadata[meta_key]['longitude'] = stat_obs_data['longitude'][-1]
            self.metadata[meta_key]['altitude'] = stat_obs_data['altitude'][-1]
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
                        self.data = np.append(self.data, np.zeros([self._CHUNKSIZE, self._COLNO], dtype=np.float64),
                                              axis=0)
                        self._ROWNO += self._CHUNKSIZE

                # end_index = self.index_pointer - 1
                # This is right because numpy leaves out the lat index number at array ops
                end_index = self.index_pointer
                # print(','.join([stat_obs_data['station_name'], str(start_index), str(end_index), str(end_index - start_index)]))
                # NOTE THAT THE LOCATION KEPT THE TIME STEP DEPENDENCY HERE
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
###################################################################################
