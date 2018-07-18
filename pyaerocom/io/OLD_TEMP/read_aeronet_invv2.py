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


class ReadAeronetInvV2:
    """Interface for reading Aeronet inversion version 2 Level 1.5 and 2.0 data

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
    _FILEMASK = '*.dubovikday'
    __version__ = "0.01"
    DATASET_NAME = const.AERONET_INV_V2L2_DAILY_NAME
    DATASET_PATH = const.OBSCONFIG[const.AERONET_INV_V2L2_DAILY_NAME]['PATH']
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
    DATA_COLNAMES['ssa439aer'] = 'SSA439-T'
    DATA_COLNAMES['ssa440aer'] = 'SSA440-T'
    DATA_COLNAMES['ssa675aer'] = 'SSA675-T'
    DATA_COLNAMES['ssa870aer'] = 'SSA870-T'
    DATA_COLNAMES['ssa1018aer'] = 'SSA1018-T'

    # meta data vars
    # will be stored as array of strings
    META_COLNAMES = {}
    META_COLNAMES['data_quality_level'] = 'DATA_TYPE'
    META_COLNAMES['date'] = 'Date(dd-mm-yyyy)'
    META_COLNAMES['time'] = 'Time(hh:mm:ss)'
    META_COLNAMES['day_of_year'] = 'Julian_Day'

    # additional vars
    # calculated
    AUX_COLNAMES = []
    # AUX_COLNAMES.append('od550gt1aer')
    # AUX_COLNAMES.append('od550lt1aer')
    # AUX_COLNAMES.append('od550aer')

    PROVIDES_VARIABLES = list(DATA_COLNAMES.keys())
    for col in AUX_COLNAMES:
        PROVIDES_VARIABLES.append(col)

    # COLNAMES_USED = {y:x for x,y in AUX_COLNAMES.items()}

    def __init__(self, index_pointer=0, dataset_to_read=None, verbose=False):
        self.verbose = verbose
        self.metadata = {}
        self.data = []
        self.index = len(self.metadata)
        self.files = []
        # the reading actually works for all V2 inversion data sets
        # so just adjust the name and the path here
        # const.AERONET_INV_V2L2_DAILY_NAME is the default
        if dataset_to_read is None:
            pass
            # self.dataset_name = const.AERONET_INV_V2L2_DAILY_NAME
            # self.dataset_path = const.OBSCONFIG[const.AERONET_INV_V2L2_DAILY_NAME]['PATH']
        elif dataset_to_read == const.AERONET_INV_V2L15_DAILY_NAME:
            self.DATASET_NAME = const.AERONET_INV_V2L15_DAILY_NAME
            self.DATASET_PATH = const.OBSCONFIG[const.AERONET_INV_V2L15_DAILY_NAME]['PATH']

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

    def read_file(self, filename, vars_to_retrieve=['ssa675aer','ssa440aer'], verbose=False):
        """method to read an Aeronet SDA V3 file and return it in a dictionary
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
        >>> import pyaerocom.io as pio
        >>> obj = pio.read_aeronet_invv2.ReadAeronetInvV2()
        >>> filename = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Aeronet.Inv.V2L2.0.daily/renamed/920801_171216_Karlsruhe.dubovikday'
        >>> filename = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Aeronet.Inv.V2L2.0.daily/renamed/920801_171216_AOE_Baotou.dubovikday'
        >>> filedata = obj.read_file(filename)
        >>> print(filedata)
        """
        # DAILY DATA:
        # ===========
        # 21:03:2005,Locations=Karlsruhe,long=8.428,lat=49.093,elev=140,Nmeas=2,PI=Bernhard_Vogel,Email=bernhard.vogel@kit.edu
        # Level 2.0 Almucantar Retrievals, Version 2
        # Combined Dubovik Retrievals,DAILY AVERAGES,Inversion Product UNITS can be found at,,, http://aeronet.gsfc.nasa.gov/new_web/units.html
        # Date(dd-mm-yyyy),Time(hh:mm:ss),Julian_Day,AOT_1640,AOT_1020,AOT_870,AOT_675,AOT_667,AOT_555,AOT_551,AOT_532,AOT_531,AOT_500,AOT_490,AOT_443,AOT_440,AOT_412,AOT_380,AOT_340,Water(cm),AOTExt440-T,AOTExt675-T,AOTExt870-T,AOTExt1018-T,AOTExt440-F,AOTExt675-F,AOTExt870-F,AOTExt1018-F,AOTExt440-C,AOTExt675-C,AOTExt870-C,AOTExt1018-C,870-440AngstromParam.[AOTExt]-Total,SSA440-T,SSA675-T,SSA870-T,SSA1018-T,AOTAbsp440-T,AOTAbsp675-T,AOTAbsp870-T,AOTAbsp1018-T,870-440AngstromParam.[AOTAbsp],REFR(440),REFR(675),REFR(870),REFR(1018),REFI(440),REFI(675),REFI(870),REFI(1018),ASYM440-T,ASYM675-T,ASYM870-T,ASYM1018-T,ASYM440-F,ASYM675-F,ASYM870-F,ASYM1018-F,ASYM440-C,ASYM675-C,ASYM870-C,ASYM1018-C,0.050000,0.065604,0.086077,0.112939,0.148184,0.194429,0.255105,0.334716,0.439173,0.576227,0.756052,0.991996,1.301571,1.707757,2.240702,2.939966,3.857452,5.061260,6.640745,8.713145,11.432287,15.000000,Inflection_Point[um],VolCon-T,EffRad-T,VolMedianRad-T,StdDev-T,VolCon-F,EffRad-F,VolMedianRad-F,StdDev-F,VolCon-C,EffRad-C,VolMedianRad-C,StdDev-C,Altitude(BOA)(km),Altitude(TOA)(km),DownwardFlux(BOA),DownwardFlux(TOA),UpwardFlux(BOA),UpwardFlux(TOA),RadiativeForcing(BOA),RadiativeForcing(TOA),ForcingEfficiency(BOA),ForcingEfficiency(TOA),DownwardFlux440-T,DownwardFlux675-T,DownwardFlux870-T,DownwardFlux1018-T,UpwardFlux440-T,UpwardFlux675-T,UpwardFlux870-T,UpwardFlux1018-T,DiffuseFlux440-T,DiffuseFlux675-T,DiffuseFlux870-T,DiffuseFlux1018-T,N[AOT_1640],N[AOT_1020],N[AOT_870],N[AOT_675],N[AOT_667],N[AOT_555],N[AOT_551],N[AOT_532],N[AOT_531],N[AOT_500],N[AOT_490],N[AOT_443],N[AOT_440],N[AOT_412],N[AOT_380],N[AOT_340],N[Water(cm)],N[AOTExt440-T],N[AOTExt675-T],N[AOTExt870-T],N[AOTExt1018-T],N[AOTExt440-F],N[AOTExt675-F],N[AOTExt870-F],N[AOTExt1018-F],N[AOTExt440-C],N[AOTExt675-C],N[AOTExt870-C],N[AOTExt1018-C],N[870-440AngstromParam.[AOTExt]-Total],N[SSA440-T],N[SSA675-T],N[SSA870-T],N[SSA1018-T],N[AOTAbsp440-T],N[AOTAbsp675-T],N[AOTAbsp870-T],N[AOTAbsp1018-T],N[870-440AngstromParam.[AOTAbsp]-Total],N[REFR(440)],N[REFR(675)],N[REFR(870)],N[REFR(1018)],N[REFI(440)],N[REFI(675)],N[REFI(870)],N[REFI(1018)],N[ASYM440-T],N[ASYM675-T],N[ASYM870-T],N[ASYM1018-T],N[ASYM440-F],N[ASYM675-F],N[ASYM870-F],N[ASYM1018-F],N[ASYM440-C],N[ASYM675-C],N[ASYM870-C],N[ASYM1018-C],N[0.050000],N[0.065604],N[0.086077],N[0.112939],N[0.148184],N[0.194429],N[0.255105],N[0.334716],N[0.439173],N[0.576227],N[0.756052],N[0.991996],N[1.301571],N[1.707757],N[2.240702],N[2.939966],N[3.857452],N[5.061260],N[6.640745],N[8.713145],N[11.432287],N[15.000000],N[Inflection_Point[um]],N[VolCon-T],N[EffRad-T],N[VolMedianRad-T],N[StdDev-T],N[VolCon-F],N[EffRad-F],N[VolMedianRad-F],N[StdDev-F],N[VolCon-C],N[EffRad-C],N[VolMedianRad-C],N[StdDev-C],N[Altitude](BOA)(km),N[Altitude](TOA)(km),N[DownwardFlux](BOA),N[DownwardFlux](TOA),N[UpwardFlux](BOA),N[UpwardFlux](TOA),N[RadiativeForcing](BOA),N[RadiativeForcing](TOA),N[ForcingEfficiency](BOA),N[ForcingEfficiency](TOA),N[DownwardFlux440-T],N[DownwardFlux675-T],N[DownwardFlux870-T],N[DownwardFlux1018-T],N[UpwardFlux440-T],N[UpwardFlux675-T],N[UpwardFlux870-T],N[UpwardFlux1018-T],N[DiffuseFlux440-T],N[DiffuseFlux675-T],N[DiffuseFlux870-T],N[DiffuseFlux1018-T],last_processing_date(mm/dd/yyyy),alm_type,DATA_TYPE
        # 23:03:2005,00:00:00,82,-9999.,0.083839,0.107933,0.160749,-9999.,-9999.,-9999.,-9999.,-9999.,0.253814,-9999.,-9999.,0.296464,-9999.,0.344551,-9999.,1.560031,0.298250,0.161350,0.108300,0.083750,0.284250,0.146300,0.091700,0.065950,0.014000,0.015050,0.016600,0.017750,1.478205,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,0.761146,0.694031,0.648542,0.626446,0.757593,0.685709,0.626377,0.584583,0.845645,0.782238,0.776409,0.784517,0.000335,0.001379,0.004453,0.011425,0.023246,0.035244,0.034897,0.022261,0.011832,0.007350,0.006417,0.007526,0.009035,0.008374,0.006213,0.004285,0.003244,0.002710,0.002207,0.001499,0.000757,0.000272,0.756000,0.056000,0.257500,0.386000,1.075500,0.042000,0.203000,0.229000,0.492500,0.013500,1.651500,2.005000,0.681500,0.140000,120.000000,236.537995,397.202700,36.959740,93.263465,-32.737075,-17.849030,-147.851120,-80.637445,489.512910,403.065362,260.545924,192.072825,138.342458,113.911303,73.633531,54.282178,0.840192,0.503973,0.291522,0.196531,-9999.,2,2,2,-9999.,-9999.,-9999.,-9999.,-9999.,2,-9999.,-9999.,2,-9999.,2,-9999.,2,2,2,2,2,2,2,2,2,2,2,2,2,2,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,-9999.,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,07/04/2007,2,Level 2.0


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
            #get rid of the first com,a seperated string element...
            c_dummy = ','.join(in_file.readline().strip().split(',')[1:])
            # re.split(r'=|\,',c_dummy)
            i_dummy = iter(re.split(r'=|\,', c_dummy.rstrip()))
            dict_loc = dict(zip(i_dummy, i_dummy))

            data_out['latitude'] = float(dict_loc['lat'])
            data_out['longitude'] = float(dict_loc['long'])
            data_out['altitude'] = float(dict_loc['elev'])
            data_out['station_name'] = dict_loc['Locations']
            data_out['PI'] = dict_loc['PI']
            data_out['PI_email'] = dict_loc['Email']

            line_2 = in_file.readline()
            line_3 = in_file.readline()

            # put together a dict with the header string as key and the index 
            # number as value so that we can access
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
            for var in self.META_COLNAMES:
                data_out[var] = []

            for line in in_file:
                # process line
                dummy_arr = line.strip().split(',')
                # the following uses the standard python datetime functions
                # date_index = index_str[COLNAMES['date']]
                # hour, minute, second = dummy_arr[index_str[COLNAMES['time']].split(':')

                # This uses the numpy datestring64 functions that e.g. also support Months as a time step for timedelta
                # Build a proper ISO 8601 UTC date string
                day, month, year = dummy_arr[index_str[self.META_COLNAMES['date']]].split(':')
                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, dummy_arr[index_str[self.META_COLNAMES['time']]]])
                datestring = '+'.join([datestring, '00:00'])
                dtime.append(np.datetime64(datestring))

                # copy the meta data (array of type string)
                for var in self.META_COLNAMES:
                    if len(self.META_COLNAMES[var]) == 0: continue
                    data_out[var].append(dummy_arr[index_str[self.META_COLNAMES[var]]])

                # copy the data fields (array type np.float_; will be converted to pandas.Series later)
                for var in self.DATA_COLNAMES:
                    if self.DATA_COLNAMES[var] in index_str:
                        data_out[var].append(np.float_(dummy_arr[index_str[self.DATA_COLNAMES[var]]]))
                        if data_out[var][-1] == nan_val: data_out[var][-1] = np.nan
                    else:
                        pass
                data_line_no += 1

        # convert the vars in vars_to_retrieve to pandas time series
        # and delete the other ones
        for var in self.PROVIDES_VARIABLES:
            # if var not in data_out: continue
            if var in vars_to_retrieve:
                if len(data_out[var]) > 0:
                    data_out[var] = pd.Series(data_out[var], index=dtime)
                else:
                    #create an list of NaNs in case the variable was not in the file
                    data_out[var] = pd.Series(np.full_like(dtime,np.nan,dtype=np.float_), index=dtime)
            else:
                del data_out[var]

        return data_out

    ###################################################################################

    def read(self, vars_to_retrieve=['ssa675aer','ssa440aer'], verbose=False):
        """method to read all files in self.files into self.data and self.metadata

        Example
        -------
        >>> import pyaerocom.io as pio
        >>> obj = pio.read_aeronet_invv2.ReadAeronetInvV2(verbose=True)
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
            self.metadata[meta_key]['station_name'] = stat_obs_data['station_name']
            self.metadata[meta_key]['latitude'] = stat_obs_data['latitude']
            self.metadata[meta_key]['longitude'] = stat_obs_data['longitude']
            self.metadata[meta_key]['altitude'] = stat_obs_data['altitude']
            self.metadata[meta_key]['PI'] = stat_obs_data['PI']
            self.metadata[meta_key]['dataset_name'] = self.DATASET_NAME

            # this is a list with indexes of this station for each variable
            # not sure yet, if we really need that or if it speeds up things
            self.metadata[meta_key]['indexes'] = {}
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
                self.metadata[meta_key]['indexes'][var] = np.arange(start_index, end_index)
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

if __name__=="__main__":
    r = ReadAeronetInvV2()
    r.get_file_list()
    r.read_file(r.files[0])