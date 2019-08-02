################################################################
# readsatellitel2base.py
#
# base class for satellite level2 data reading conversion
#
# this file is part of the pyaerocom package
#
#################################################################
# Created 20190802 by Jan Griesfeller for Met Norway
#
# Last changed: See git log
#################################################################

# Copyright (C) 2019 met.no
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

from pyaerocom.io.readungriddedbase import ReadUngriddedBase
import geopy
import numpy as np
import logging
from pyaerocom import const
from pyaerocom.ungriddeddata import UngriddedData


class ReadL2DataBase(ReadUngriddedBase):
    """Interface for reading various satellite's L2 data

    at this point Sentinel5 and Aeolus

    .. seealso::

        Base class :class:`ReadUngriddedBase`

    """
    _FILEMASK = '*'
    __version__ = "0.01"
    DATA_ID = ''

    DATASET_PATH = ''
    # Flag if the dataset contains all years or not
    DATASET_IS_YEARLY = False

    SUPPORTED_SUFFIXES = []

    SUPPORTED_ARCHIVE_SUFFIXES = []
    SUPPORTED_ARCHIVE_SUFFIXES.append('.TGZ')
    SUPPORTED_ARCHIVE_SUFFIXES.append('.tgz')
    SUPPORTED_ARCHIVE_SUFFIXES.append('.tar')
    SUPPORTED_ARCHIVE_SUFFIXES.append('.tar.gz')

    GLOBAL_ATTRIBUTES = {}

    # variable names
    # dimension data
    _LATITUDENAME = 'latitude'
    _LONGITUDENAME = 'longitude'
    _ALTITUDENAME = 'altitude'

    _TIME_NAME = 'time'

    # variable names for the different retrievals

    _TIMEINDEX = UngriddedData._TIMEINDEX
    _LATINDEX = UngriddedData._LATINDEX
    _LONINDEX = UngriddedData._LONINDEX
    _ALTITUDEINDEX = UngriddedData._ALTITUDEINDEX
    # for distance calculations we need the location in radians
    # so store these for speed in self.data
    # the following indexes indicate the column where that is stored
    # _RADLATINDEX = 4
    # _RADLONINDEX = 5
    # _DISTINDEX = 6

    _DATAINDEX01 = UngriddedData._DATAINDEX
    _COLNO = 12

    _ROWNO = 1000000
    _CHUNKSIZE = 100000

    GROUP_DELIMITER = '/'

    # create a dict with the aerocom variable name as key and the index number in the
    # resulting numpy array as value.
    INDEX_DICT = {}
    INDEX_DICT.update({_LATITUDENAME: _LATINDEX})
    INDEX_DICT.update({_LONGITUDENAME: _LONINDEX})
    INDEX_DICT.update({_ALTITUDENAME: _ALTITUDEINDEX})
    INDEX_DICT.update({_TIME_NAME: _TIMEINDEX})

    # dictionary to store array sizes of an element in self.data
    SIZE_DICT = {}

    # NaN values are variable specific
    NAN_DICT = {}

    # the following defines necessary quality flags for a value to make it into the used data set
    # the flag needs to have a HIGHER or EQUAL value than the one listed here
    # The valuse are taken form the product readme file
    QUALITY_FLAGS = {}

    # PROVIDES_VARIABLES = list(RETRIEVAL_READ_PARAMETERS['sca']['metadata'].keys())
    # PROVIDES_VARIABLES.extend(RETRIEVAL_READ_PARAMETERS['sca']['vars'].keys())

    # max distance between point on the earth's surface for a match
    # in meters
    MAX_DISTANCE = 50000.
    EARTH_RADIUS = geopy.distance.EARTH_RADIUS
    NANVAL_META = -1.E-6
    NANVAL_DATA = -1.E6

    # these are the variable specific attributes written into a netcdf file
    NETCDF_VAR_ATTRIBUTES = {}
    NETCDF_VAR_ATTRIBUTES[_LATITUDENAME] = {}
    # NETCDF_VAR_ATTRIBUTES[_LATITUDENAME]['_FillValue'] = {}
    NETCDF_VAR_ATTRIBUTES[_LATITUDENAME]['long_name'] = 'latitude'
    NETCDF_VAR_ATTRIBUTES[_LATITUDENAME]['standard_name'] = 'latitude'
    NETCDF_VAR_ATTRIBUTES[_LATITUDENAME]['units'] = 'degrees north'
    NETCDF_VAR_ATTRIBUTES[_LATITUDENAME]['bounds'] = 'lat_bnds'
    NETCDF_VAR_ATTRIBUTES[_LATITUDENAME]['axis'] = 'Y'
    NETCDF_VAR_ATTRIBUTES[_LONGITUDENAME] = {}
    # NETCDF_VAR_ATTRIBUTES[_LONGITUDENAME]['_FillValue'] = {}
    NETCDF_VAR_ATTRIBUTES[_LONGITUDENAME]['long_name'] = 'longitude'
    NETCDF_VAR_ATTRIBUTES[_LONGITUDENAME]['standard_name'] = 'longitude'
    NETCDF_VAR_ATTRIBUTES[_LONGITUDENAME]['units'] = 'degrees_east'
    NETCDF_VAR_ATTRIBUTES[_LONGITUDENAME]['bounds'] = 'lon_bnds'
    NETCDF_VAR_ATTRIBUTES[_LONGITUDENAME]['axis'] = 'X'
    NETCDF_VAR_ATTRIBUTES[_ALTITUDENAME] = {}
    # NETCDF_VAR_ATTRIBUTES[_ALTITUDENAME]['_FillValue'] = {}
    NETCDF_VAR_ATTRIBUTES[_ALTITUDENAME]['long_name'] = 'altitude'
    NETCDF_VAR_ATTRIBUTES[_ALTITUDENAME]['standard_name'] = 'altitude'
    NETCDF_VAR_ATTRIBUTES[_ALTITUDENAME]['units'] = 'm'



    SUPPORTED_DATASETS = []
    SUPPORTED_DATASETS.append(DATA_ID)

    DEFAULT_VARS = []
    PROVIDES_VARIABLES = []
    TS_TYPE = 'undefined'

    __baseversion__ = '0.01_' + ReadUngriddedBase.__baseversion__
    
    def __init__(self, dataset_to_read=None, index_pointer=0, loglevel=logging.INFO, verbose=False):
        super(ReadL2DataBase, self).__init__(dataset_to_read)
        self.verbose = verbose
        self.metadata = {}
        self.data = None
        self.data_for_gridding = {}
        self.gridded_data = {}
        self.global_attributes = {}
        self.index = len(self.metadata)
        self.files = []
        self.files_read = []
        self.index_pointer = index_pointer
        # that's the flag to indicate if the location of a data point in self.data has been
        # stored in rads in self.data already
        # trades RAM for speed
        self.rads_in_array_flag = False

        if loglevel is not None:
            # self.logger = logging.getLogger(__name__)
            # if self.logger.hasHandlers():
            #     # Logger is already configured, remove all handlers
            #     self.logger.handlers = []
            # # self.logger = logging.getLogger('pyaerocom')
            # default_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
            # console_handler = logging.StreamHandler()
            # console_handler.setFormatter(default_formatter)
            # self.logger.addHandler(console_handler)
            self.logger.setLevel(loglevel)


    ###################################################################################
# if __name__=="__main__":
#     """small test for the sentinel5p reading...
#     """
#     import pyaerocom as pya
#     obj = pya.io.read_sentinel5p_data.ReadL2Data()
#     testfiles = []
#     testfiles.append('/lustre/storeB/project/fou/kl/vals5p/download/O3/S5P_OFFL_L2__O3_____20190531T165100_20190531T183230_08446_01_010107_20190606T185838.nc')
#     testfiles.append('/lustre/storeB/project/fou/kl/vals5p/download/O3/S5P_OFFL_L2__O3_____20190530T051930_20190530T070100_08425_01_010107_20190605T070532.nc')
#     data = obj.read(files=testfiles)
#     pass
