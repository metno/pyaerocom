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
read Aeronet SDA V3 data
"""
import os
import glob
import sys

import numpy as np

import pandas as pd
import re

from pyaerocom import const


class ReadAeronetSdaV3:
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
    DATASET_NAME = const.AERONET_SUN_V3L15_SDA_DAILY_NAME
    DATASET_PATH = const.OBSCONFIG[const.AERONET_SUN_V3L15_SDA_DAILY_NAME]['PATH']
    # Flag if the dataset contains all years or not
    DATASET_IS_YEARLY = False

    _METADATAKEYINDEX = 0
    _TIMEINDEX = 1
    _LATINDEX = 2
    _LONINDEX = 3
    _ALTITUDEINDEX = 4
    _VARINDEX = 5
    _DATAINDEX = 6

    _COLNO = 13
    _ROWNO = 10000
    _CHUNKSIZE = 1000

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
    METADATA_COLNAMES['station name'] = 'AERONET_Site'
    METADATA_COLNAMES['latitude'] = 'Site_Latitude(Degrees)'
    METADATA_COLNAMES['longitude'] = 'Site_Longitude(Degrees)'
    METADATA_COLNAMES['altitude'] = 'Site_Elevation(m)'
    METADATA_COLNAMES['date'] = 'Date_(dd:mm:yyyy)'
    METADATA_COLNAMES['time'] = 'Time_(hh:mm:ss)'
    METADATA_COLNAMES['day_of_year'] = 'Day_of_Year'

    # additional vars
    # calculated
    AUX_COLNAMES = []
    AUX_COLNAMES.append('od550gt1aer')
    AUX_COLNAMES.append('od550lt1aer')
    AUX_COLNAMES.append('od550aer')

    PROVIDES_VARIABLES = list(DATA_COLNAMES.keys())
    for col in AUX_COLNAMES:
        PROVIDES_VARIABLES.append(col)

    # COLNAMES_USED = {y:x for x,y in AUX_COLNAMES.items()}

    def __init__(self, index_pointer=0, data_set_to_read = None, verbose=False):
        self.verbose = verbose
        self.metadata = {}
        self.data = []
        self.index = len(self.metadata)
        self.files = []
        # the reading actually works for all V3 SDA data sets
        # so just adjust the name and the path here
        # const.AERONET_SUN_V3L15_SDA_DAILY_NAME is the default
        if data_set_to_read is None:
            pass
            # self.dataset_name = const.AERONET_SUN_V3L15_AOD_DAILY_NAME
            # self.dataset_path = const.OBSCONFIG[const.AERONET_SUN_V3L15_AOD_DAILY_NAME]['PATH']
        elif data_set_to_read == const.AERONET_SUN_V3L2_SDA_DAILY_NAME:
            self.DATASET_NAME = const.AERONET_SUN_V3L2_SDA_DAILY_NAME
            self.DATASET_PATH = const.OBSCONFIG[const.AERONET_SUN_V3L2_SDA_DAILY_NAME]['PATH']

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
            stat_names.append(self.metadata[key]['station name'])

        return ','.join(stat_names)

    ###################################################################################

    def read_file(self, filename, vars_to_read=['od500gt1aer','od550gt1aer'], verbose=False):
        """method to read an Aeronet SDA V3 file and return it in a dictionary
        with the data variables as pandas time series

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
        >>> import pyaerocom.io as pio
        >>> obj = pio.read_aeronet_sdav3.ReadAeronetSdaV3()
        >>> filename = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Aeronet.SDA.V3L1.5.daily/renamed/Karlsruhe.lev30'
        >>> filedata = obj.read_file(filename)
        >>> print(filedata)
        """

        # DAILY DATA:
        # ===========
        # AERONET Version 3; SDA Version 4.1
        # Cuiaba
        # Version 3: SDA Retrieval Level 1.5
        # The following data are cloud cleared and quality controls have been applied but these data may not have final calibration applied.  These data may change.
        # Contact: PI=Brent_Holben; PI Email=Brent.N.Holben@nasa.gov
        # Daily Averages,UNITS can be found at,,, https://aeronet.gsfc.nasa.gov/new_web/units.html
        # AERONET_Site,Date_(dd:mm:yyyy),Time_(hh:mm:ss),Day_of_Year,Total_AOD_500nm[tau_a],Fine_Mode_AOD_500nm[tau_f],Coarse_Mode_AOD_500nm[tau_c],FineModeFraction_500nm[eta],2nd_Order_Reg_Fit_Error-Total_AOD_500nm[regression_dtau_a],RMSE_Fine_Mode_AOD_500nm[Dtau_f],RMSE_Coarse_Mode_AOD_500nm[Dtau_c],RMSE_FineModeFraction_500nm[Deta],Angstrom_Exponent(AE)-Total_500nm[alpha],dAE/dln(wavelength)-Total_500nm[alphap],AE-Fine_Mode_500nm[alpha_f],dAE/dln(wavelength)-Fine_Mode_500nm[alphap_f],N[Total_AOD_500nm[tau_a]],N[Fine_Mode_AOD_500nm[tau_f]],N[Coarse_Mode_AOD_500nm[tau_c]],N[FineModeFraction_500nm[eta]],N[2nd_Order_Reg_Fit_Error-Total_AOD_500nm[regression_dtau_a]],N[RMSE_Fine_Mode_AOD_500nm[Dtau_f]],N[RMSE_Coarse_Mode_AOD_500nm[Dtau_c]],N[RMSE_FineModeFraction_500nm[Deta]],N[Angstrom_Exponent(AE)-Total_500nm[alpha]],N[dAE/dln(wavelength)-Total_500nm[alphap]],N[AE-Fine_Mode_500nm[alpha_f]],N[dAE/dln(wavelength)-Fine_Mode_500nm[alphap_f]],Data_Quality_Level,AERONET_Instrument_Number,AERONET_Site_Name,Site_Latitude(Degrees),Site_Longitude(Degrees),Site_Elevation(m),
        # Karlsruhe,21:03:2005,12:00:00,80,0.242882,0.050086,0.192796,0.206254,0.000435,0.018642,0.019553,0.076899,0.373355,-0.766570,2.387612,1.394079,2,2,2,2,2,2,2,2,2,2,2,2,lev15,325,Karlsruhe,49.093300,8.427900,140.000000


        # ALL POINT DATA
        # ==============


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
            for var in self.METADATA_COLNAMES:
                data_out[var] = []

            for line in in_file:
                # process line
                dummy_arr = line.split(',')
                # the following uses the standard python datetime functions
                # date_index = index_str[COLNAMES['date']]
                # hour, minute, second = dummy_arr[index_str[COLNAMES['time']].split(':')

                # This uses the numpy datestring64 functions that e.g. also support Months as a time step for timedelta
                # Build a proper ISO 8601 UTC date string
                day, month, year = dummy_arr[index_str[self.METADATA_COLNAMES['date']]].split(':')
                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, dummy_arr[index_str[self.METADATA_COLNAMES['time']]]])
                datestring = '+'.join([datestring, '00:00'])
                dtime.append(np.datetime64(datestring))

                # copy the meta data (array of type string)
                for var in self.METADATA_COLNAMES:
                    if len(self.METADATA_COLNAMES[var]) == 0: continue
                    data_out[var].append(dummy_arr[index_str[self.METADATA_COLNAMES[var]]])

                # copy the data fields (array type np.float_; will be converted to pandas.Series later)
                for var in self.DATA_COLNAMES:
                    data_out[var].append(np.float_(dummy_arr[index_str[self.DATA_COLNAMES[var]]]))
                    if data_out[var][-1] == nan_val: data_out[var][-1] = np.nan

                # some stuff needs to be calculated
                data_out['od550aer'].append(
                    data_out['od500aer'][-1] * (0.55 / 0.50) ** (np.float_(-1.) * data_out['ang4487aer'][-1]))
                data_out['od550gt1aer'].append(
                    data_out['od500gt1aer'][-1] * (0.55 / 0.50) ** (np.float_(-1.) * data_out['ang4487aer'][-1]))
                data_out['od550lt1aer'].append(
                    data_out['od500lt1aer'][-1] * (0.55 / 0.50) ** (np.float_(-1.) * data_out['ang4487aer'][-1]))


                # # apply the lower limit for od550aer
                # if data_out['od550aer'][-1] < const.VAR_PARAM['od550aer']['lower_limit']:
                #     data_out['od550aer'][-1] = np.nan
                data_line_no += 1

        # convert the vars in vars_to_read to pandas time series
        # and delete the other ones
        for var in self.PROVIDES_VARIABLES:
            if var in vars_to_read:
                data_out[var] = pd.Series(data_out[var], index=dtime)
            else:
                del data_out[var]

        return data_out

    ###################################################################################

    def read(self, vars_to_read=['od500gt1aer','od550gt1aer'], verbose=False):
        """method to read all files in self.files into self.data and self.metadata

        Example
        -------
        >>> import pyaerocom.io as pio
        >>> obj = pio.read_aeronet_sdav3.ReadAeronetSdaV3(verbose=True)
        >>> obj.read(verbose=True)
        """

        # Metadata key is float because the numpy array holding it is float

        met_data_key = 0.
        self.files = self.get_file_list()
        self.data = np.empty([self._ROWNO, self._COLNO], dtype=np.float_)

        for _file in sorted(self.files):
            if self.verbose:
                sys.stdout.write(_file + "\n")
            stat_obs_data = self.read_file(_file, vars_to_read=vars_to_read)
            # Fill the metatdata dict
            # the location in the data set is time step dependant!
            # use the lat location here since we have to choose one location
            # in the time series plot
            self.metadata[met_data_key] = {}
            self.metadata[met_data_key]['station name'] = stat_obs_data['station name'][-1]
            self.metadata[met_data_key]['latitude'] = stat_obs_data['latitude'][-1]
            self.metadata[met_data_key]['longitude'] = stat_obs_data['longitude'][-1]
            self.metadata[met_data_key]['altitude'] = stat_obs_data['altitude'][-1]
            self.metadata[met_data_key]['PI'] = stat_obs_data['PI']
            self.metadata[met_data_key]['data_set_name'] = self.DATASET_NAME

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
                        self.data = np.append(self.data, np.zeros([self._CHUNKSIZE, self._COLNO], dtype=np.float64),
                                              axis=0)
                        self._ROWNO += self._CHUNKSIZE

                # end_index = self.index_pointer - 1
                # This is right because numpy leaves out the lat index number at array ops
                end_index = self.index_pointer
                # print(','.join([stat_obs_data['station name'], str(start_index), str(end_index), str(end_index - start_index)]))
                # NOTE THAT THE LOCATION KEPT THE TIME STEP DEPENDENCY HERE
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
