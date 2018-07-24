################################################################
# read_aeronet_earlinet.py
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

"""
import os
import glob
import sys

import numpy as np
import xarray

import pandas as pd

from pyaerocom import const

class ReadEarlinet:
    """class to read EARLINET data

    Attributes
    ----------
    data : numpy array of dtype np.float64 initially of shape (10000,8)
        data point array
    metadata : dict
        meta data dictionary

    Parameters
    ----------
    verboseflag : Bool
        if True some running information is printed
    
    Todo
    ----

        - Review file search routine: iterates currently over all variables \
        thus, iterates over all files N-times if N is the number of req. \
        variables. Should iterate over all files only once and check match \
        of either variable. 
        - Check mask for dust layer height: e.g. first file found when \
        calling :func:`get_file_list` is: /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Earlinet/data/ev/f2010/ev1008192050.e532 \
        and does not contain dust layer height..
        
        
        
    """
    _FILEMASK = '*.e*'
    __version__ = "0.03"
    DATASET_NAME = const.EARLINET_NAME
    DATASET_PATH = const.OBSCONFIG[const.EARLINET_NAME]['PATH']
    _TEST_FILE = "/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Earlinet/data//le/f2013/le1309091830.e355"
    # Flag if the dataset contains all years or not
    DATASET_IS_YEARLY = False

    _METADATAKEYINDEX = 0
    _TIMEINDEX = 1
    _LATINDEX = 2
    _LONINDEX = 3
    _ALTITUDEINDEX = 4  # station height
    _VARINDEX = 5
    _DATAINDEX = 6
    _DATAHEIGHTINDEX = 7    # height of the measurement for profile data

    _COLNO = 11
    _ROWNO = 10000
    _CHUNKSIZE = 1000
    _cC_EarlinetDataTagsToCopy=['ALTITUDE','EXTINCTION', 'ERROREXTINCTION']
    # fC_EARLINETRebinDist = 100.
    # fC_EARLINETRebinHeights = findgen(iC_MaxObsHeightLevels) * fC_EARLINETRebinDist + fC_EARLINETRebinDist / 2.
    # cC_EARLINETRebinVarName = 'Z3D'

    PROVIDES_VARIABLES = ('ec5503daer', 'ec5323daer', 'ec3553daer', 'zdust')
    Z3D_VARNAME = 'Altitude'
    VAR_INFO = {}
    VAR_INFO['ec5503daer'] = {}
    VAR_INFO['ec5503daer']['file_mask'] = '*/f*/*.e5*'
    VAR_INFO['ec5503daer']['netcdf_var_name'] = 'Extinction'
    VAR_INFO['ec5323daer'] = {}
    VAR_INFO['ec5323daer']['file_mask'] = '*/f*/*.e5*'
    VAR_INFO['ec5323daer']['netcdf_var_name'] = 'Extinction'
    VAR_INFO['ec3553daer'] = {}
    VAR_INFO['ec3553daer']['file_mask'] = '*/f*/*.e3*'
    VAR_INFO['ec3553daer']['netcdf_var_name'] = 'Extinction'
    VAR_INFO['zdust'] = {}
    VAR_INFO['zdust']['file_mask'] = '*/f*/*.e*'
    VAR_INFO['zdust']['netcdf_var_name'] = 'DustLayerHeight'
    VAR_INFO['zdust']['min_val'] = 0.
    VAR_INFO['zdust']['max_val'] = 1.E4



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
    # TODO: need review vars_to_retrieve
    def read_file(self, filename, vars_to_retrieve = ['zdust'], verbose = False):
        """method to read an EARLINET file and return it in a dictionary
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
        >>> import pyaerocom.io.read_earlinet
        >>> obj = pyaerocom.io.read_earlinet.ReadEarlinet()
        >>> filedata = obj.read_file('/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Earlinet/data/le/f2013/le1309091830.e355')
        >>> print(filedata)
        <xarray.Dataset>
Dimensions:           (Length: 48)
Dimensions without coordinates: Length
Data variables:
    Altitude          (Length) float64 1.384e+03 1.414e+03 1.443e+03 ...
    Extinction        (Length) float64 7.284e-05 7.685e-05 7.375e-05 ...
    ErrorExtinction   (Length) float64 -5.045e-05 -5.056e-05 -4.974e-05 ...
    Backscatter       (Length) float64 1.675e-06 1.641e-06 1.604e-06 ...
    ErrorBackscatter  (Length) float64 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 ...
    DustLayerHeight   float32 3200.0
Attributes:
    System:                  PollyXT_ift
    Location:                Leipzig, Germany
    Longitude_degrees_east:  12.43
    Latitude_degrees_north:  51.35
    Altitude_meter_asl:      90
    EmissionWavelength_nm:   355
    DetectionWavelength_nm:  387
    DetectionMode:           photon counting
    EvaluationMethod:        Raman
    InputParameters:         Lindenberg_LV_13090918.txt;PollyXT_ift_20131001-...
    ZenithAngle_degrees:     5
    ResolutionRaw_meter:     29.89
    ResolutionEvaluated:     567.83
    StartDate:               20130909
    StartTime_UT:            183000
    StopTime_UT:             192900
    ShotsAveraged:           106200
    Comments:                EARLINET
        """
        data_out = xarray.open_dataset(filename)

        return (data_out)

    ###################################################################################

    def read(self, vars_to_retrieve = ['zdust'], verbose = False):
        """method to read all files in self.files into self.data and self.metadata

        Example
        -------
        >>> import pyaerocom.io.read_earlinet
        >>> obj = pyaerocom.io.read_earlinet.ReadEarlinet()
        >>> obj.read()
        """

        # Metadata key is float because the numpy array holding it is float

        meta_key = -1. # we want to start at key 0.
        files = self.get_file_list()
        # self.data = np.empty([self._ROWNO, self._COLNO], dtype=np.float64)
        self.data = np.zeros([self._ROWNO, self._COLNO], dtype=np.float64)

        last_stat_code = ''
        time = []
        start_index = self.index_pointer
        for _file in sorted(files):
            if self.verbose:
                sys.stdout.write(_file+"\n")

            stat_obs_data = self.read_file(_file, vars_to_retrieve = vars_to_retrieve)
            # Fill the metatdata dict
            stat_code = _file.split('/')[-3]
            if stat_code != last_stat_code:
                # new station
                meta_key += 1.
                self.metadata[meta_key] = {}
                self.metadata[meta_key]['station_name'] = stat_obs_data.attrs['Location']
                self.metadata[meta_key]['latitude'] = stat_obs_data.attrs['Latitude_degrees_north']
                self.metadata[meta_key]['longitude'] = stat_obs_data.attrs['Longitude_degrees_east']
                self.metadata[meta_key]['altitude'] = stat_obs_data.attrs['Altitude_meter_asl']
                self.metadata[meta_key]['PI'] = ''
                self.metadata[meta_key]['dataset_name'] = self.DATASET_NAME
                self.metadata[meta_key]['has_zdust'] = False
                # this is a list with indices of this station for each variable
                # not sure yet, if we really need that or if it speeds up things
                self.metadata[meta_key]['idx'] = {}
                self.metadata[meta_key]['files'] = []
                last_stat_code = stat_code

            str_dummy = str(stat_obs_data.StartDate)
            year = str_dummy[0:4]
            month = str_dummy[4:6]
            day = str_dummy[6:8]

            str_dummy = str(stat_obs_data.StartTime_UT).zfill(6)
            hours = str_dummy[0:2]
            minutes = str_dummy[2:4]
            seconds = str_dummy[4:6]
            datestring = '-'.join([year, month, day])
            datestring = 'T'.join([datestring, ':'.join([hours, minutes, seconds])])
            #datestring = '+'.join([datestring, '00:00'])
            #time = (np.datetime64(datestring))
            # print(datestring)
            # time = pd.DatetimeIndex([datestring])
            time = pd.Timestamp(datestring)

            start_index = self.index_pointer
            # variable index
            obs_var_index = 0


            for var in sorted(vars_to_retrieve):
                netcdf_var_name = self.VAR_INFO[var]['netcdf_var_name']
                # check if the desired variable is in the file
                if netcdf_var_name not in stat_obs_data.variables:
                    sys.stderr.write("Error: variable " + var + " not found in file " + _file + ". Skipping file!\n")
                    continue

                if stat_obs_data.variables[netcdf_var_name].ndim == 0:  #1d var
                    # check if the value provided is non NaN and in an expected range
                    if np.isnan(stat_obs_data.variables[netcdf_var_name]):
                        sys.stderr.write("Error: value of variable " + var + " in file " + _file + " is NaN. Skipping...!\n")
                        continue
                    if stat_obs_data.variables[netcdf_var_name] > self.VAR_INFO[var]['max_val']:
                        sys.stderr.write("Error: value of variable " + var + " in file " + _file + " greater max val. Skipping...!\n")
                        continue
                    if stat_obs_data.variables[netcdf_var_name] < self.VAR_INFO[var]['min_val']:
                        sys.stderr.write("Error: value of variable " + var + " in file " + _file + " less than max val. Skipping...!\n")
                        continue
                    self.metadata[meta_key]['files'].append(_file)
                    self.metadata[meta_key]['has_zdust'] = True
                    self.data[self.index_pointer, self._DATAINDEX] = stat_obs_data.variables[netcdf_var_name]
                    #self.data[self.index_pointer, self._DATAHEIGHTINDEX] = height_data[step]
                    self.index_pointer += 1
                    if self.index_pointer >= self._ROWNO:
                        # add another array chunk to self.data
                        self.data = np.append(self.data, np.zeros([self._CHUNKSIZE, self._COLNO], dtype=np.float64), axis=0)
                        self._ROWNO += self._CHUNKSIZE

                    end_index = self.index_pointer - 1
                    # print(','.join([stat_obs_data['station_name'], str(start_index), str(end_index), str(end_index - start_index)]))
                    try:
                        self.metadata[meta_key]['idx'][var].append(end_index)
                    except KeyError:
                        self.metadata[meta_key]['idx'][var] = []
                        self.metadata[meta_key]['idx'][var].append(end_index)

                    # self.metadata[meta_key]['idx'][var] = np.arange(start_index, end_index)
                    self.data[end_index, self._TIMEINDEX] = np.float64(time.value / 1.E9)
                    self.data[end_index, self._VARINDEX] = obs_var_index
                    self.data[end_index, self._LATINDEX] = stat_obs_data.attrs['Latitude_degrees_north']
                    self.data[end_index, self._LONINDEX] = stat_obs_data.attrs['Longitude_degrees_east']
                    self.data[end_index, self._ALTITUDEINDEX] = stat_obs_data.attrs['Altitude_meter_asl']
                    self.data[end_index, self._METADATAKEYINDEX] = meta_key
                else: #2d variable
                    # TODO test profile code
                    height_steps = len(stat_obs_data.variables[netcdf_var_name])
                    variable_data = np.float64(stat_obs_data.variables[netcdf_var_name])
                    height_data = np.float64(stat_obs_data.variables[self.Z3D_VARNAME])

                    for step in range(height_steps):
                        self.data[self.index_pointer, self._DATAINDEX] = variable_data[step]
                        self.data[self.index_pointer, self._DATAHEIGHTINDEX] = height_data[step]

                        self.index_pointer += 1
                        if self.index_pointer >= self._ROWNO:
                            # add another array chunk to self.data
                            self.data = np.append(self.data, np.zeros([self._CHUNKSIZE, self._COLNO], dtype=np.float64), axis=0)
                            self._ROWNO += self._CHUNKSIZE
                    # self.metadata[meta_key]['idx'][var] = np.arange(start_index, end_index)
                    end_index = self.index_pointer
                    self.data[start_index:end_index, self._TIMEINDEX] = np.float64(time.value / 1.E9)
                    self.data[start_index:end_index, self._VARINDEX] = obs_var_index
                    self.data[start_index:end_index, self._LATINDEX] = stat_obs_data.attrs['Latitude_degrees_north']
                    self.data[start_index:end_index, self._LONINDEX] = stat_obs_data.attrs['Longitude_degrees_east']
                    self.data[start_index:end_index, self._ALTITUDEINDEX] = stat_obs_data.attrs['Altitude_meter_asl']
                    self.data[start_index:end_index, self._METADATAKEYINDEX] = meta_key


                start_index = self.index_pointer
                obs_var_index += 1
            # TODO check self.metadata[meta_key]['idx'] for reference
            # if none is found, remove the last metadata entry again since the station did not provide data

        # shorten self.data to the right number of points
        # self.data = self.data[0:end_index]


    ###################################################################################

    def get_file_list(self, vars_to_retrieve=['zdust']):
        """search for files to read

        Parameters
        ----------
        vars_to_retrieve : list
            list of variables that are supposed to be read
        
        Returns
        -------
        list
            file list
            
        Example
        -------
        >>> import pyaerocom.io.read_earlinet
        >>> obj = pyaerocom.io.read_earlinet.ReadEarlinet()
        >>> obj.get_file_list()
        """


        if self.verbose:
            print('searching for data files. This might take a while...')
        # files = glob.glob(os.path.join(self.DATASET_PATH,
        #                                self._FILEMASK), recursive=True)
        #files = []
        for var in vars_to_retrieve:
            files = (glob.glob(os.path.join(self.DATASET_PATH,
                                            self.VAR_INFO[var]['file_mask']), 
                     recursive=True))
        self.files = files
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

        return revision
###################################################################################
