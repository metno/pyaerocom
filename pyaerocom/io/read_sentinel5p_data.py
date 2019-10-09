################################################################
# read_sentinel5p_data.py
#
# read Sentinel5P L2 data
#
# this file is part of the pyaerocom package
#
#################################################################
# Created 20180626 by Jan Griesfeller for Met Norway
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

from pyaerocom.io.readsatellitel2base import ReadL2DataBase
# from pyaerocom.io.readungriddedbase import ReadUngriddedBase
# import geopy
import numpy as np
import logging
from pyaerocom import const
from pyaerocom.ungriddeddata import UngriddedData


class ReadL2Data(ReadL2DataBase):
    """Interface for reading various Sentinel5P L2 data

    at this point only N2O and Ozone data is (will be) supported

    .. seealso::

        Base class :class:`ReadUngriddedBase`

    """

    _FILEMASK = '*.nc'
    __version__ = "0.01"
    DATA_ID = const.SENTINEL5P_NAME

    DATASET_PATH = '/lustre/storeB/project/fou/kl/vals5p/download'
    # Flag if the dataset contains all years or not
    DATASET_IS_YEARLY = False

    _NO2NAME = 'tcolno2'
    _O3NAME = 'tcolo3'
    _QANAME = 'qa_index'
    DEFAULT_VARS = [_O3NAME]
    PROVIDES_VARIABLES = [_NO2NAME, _O3NAME]


    SUPPORTED_DATASETS = []
    SUPPORTED_DATASETS.append(DATA_ID)

    TS_TYPE = 'undefined'

    def __init__(self, dataset_to_read=None, index_pointer=0, loglevel=logging.INFO, verbose=False, 
                 read_averaging_kernel=True):
        super(ReadL2Data, self).__init__(dataset_to_read)
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
        # these are the variable specific attributes written into a netcdf file
        self._TIME_OFFSET_NAME = 'delta_time'
        self._NO2NAME = 'tcolno2'
        self._O3NAME = 'tcolo3'
        self._QANAME = 'qa_index'

        self._LATBOUNDSNAME = 'lat_bnds'
        self._LATBOUNDSSIZE = 4
        self._LONBOUNDSNAME = 'lon_bnds'
        self._LONBOUNDSSIZE = 4
        self.COORDINATE_NAMES = [self._LATITUDENAME, self._LONGITUDENAME, self._ALTITUDENAME,
                                 self._LATBOUNDSNAME, self._LONBOUNDSNAME, self._LEVELSNAME]

        self._QAINDEX = UngriddedData._DATAFLAGINDEX
        self._TIME_OFFSET_INDEX = UngriddedData._TRASHINDEX
        self._LATBOUNDINDEX = 13
        self._LONBOUNDINDEX = self._LATBOUNDINDEX + self._LATBOUNDSSIZE + 1
        self._COLNO = self._LATBOUNDINDEX + self._LATBOUNDSSIZE + self._LONBOUNDSSIZE + 2
        self._HEIGHTSTEPNO = 24
        self.SUPPORTED_SUFFIXES.append('.nc')




        # create a dict with the aerocom variable name as key and the index number in the
        # resulting numpy array as value.
        # INDEX_DICT = {}
        self.INDEX_DICT.update({self._LATITUDENAME: self._LATINDEX})
        self.INDEX_DICT.update({self._LONGITUDENAME: self._LONINDEX})
        self.INDEX_DICT.update({self._ALTITUDENAME: self._ALTITUDEINDEX})
        self.INDEX_DICT.update({self._TIME_NAME: self._TIMEINDEX})
        self.INDEX_DICT.update({self._TIME_OFFSET_NAME: self._TIME_OFFSET_INDEX})
        self.INDEX_DICT.update({self._NO2NAME: self._DATAINDEX01})
        self.INDEX_DICT.update({self._O3NAME: self._DATAINDEX01})
        self.INDEX_DICT.update({self._QANAME: self._QAINDEX})
        self.INDEX_DICT.update({self._LATBOUNDSNAME: self._LATBOUNDINDEX})
        self.INDEX_DICT.update({self._LONBOUNDSNAME: self._LONBOUNDINDEX})

        # dictionary to store array sizes of an element in self.data
        # SIZE_DICT = {}
        self.SIZE_DICT.update({self._LATBOUNDSNAME: self._LATBOUNDSSIZE})
        self.SIZE_DICT.update({self._LONBOUNDSNAME: self._LONBOUNDSSIZE})

        # NaN values are variable specific
        # NAN_DICT = {}
        self.NAN_DICT.update({self._LATITUDENAME: -1.E-6})
        self.NAN_DICT.update({self._LONGITUDENAME: -1.E-6})
        self.NAN_DICT.update({self._ALTITUDENAME: -1.})

        # the following defines necessary quality flags for a value to make it into the used data set
        # the flag needs to have a HIGHER or EQUAL value than the one listed here
        # The valuse are taken form the product readme file
        # QUALITY_FLAGS = {}
        self.QUALITY_FLAGS.update({self._NO2NAME: 0.75})
        # QUALITY_FLAGS.update({_NO2NAME: 0.5}) #cloudy
        self.QUALITY_FLAGS.update({self._O3NAME: 0.7})


        self.CODA_READ_PARAMETERS[self._NO2NAME] = {}
        self.CODA_READ_PARAMETERS[self._NO2NAME]['metadata'] = {}
        self.CODA_READ_PARAMETERS[self._NO2NAME]['vars'] = {}
        self.CODA_READ_PARAMETERS[self._NO2NAME]['time_offset'] = np.float_(24. * 60. * 60.)
        self.CODA_READ_PARAMETERS[self._O3NAME] = {}
        self.CODA_READ_PARAMETERS[self._O3NAME]['metadata'] = {}
        self.CODA_READ_PARAMETERS[self._O3NAME]['vars'] = {}
        self.CODA_READ_PARAMETERS[self._O3NAME]['time_offset'] = np.float_(24. * 60. * 60.)


        # self.CODA_READ_PARAMETERS[DATASET_NAME]['metadata'][_TIME_NAME] = 'PRODUCT/time_utc'
        self.CODA_READ_PARAMETERS[self._NO2NAME]['metadata'][self._TIME_NAME] = 'PRODUCT/time'
        self.CODA_READ_PARAMETERS[self._NO2NAME]['metadata'][self._TIME_OFFSET_NAME] = 'PRODUCT/delta_time'
        self.CODA_READ_PARAMETERS[self._NO2NAME]['metadata'][self._LATITUDENAME] = 'PRODUCT/latitude'
        self.CODA_READ_PARAMETERS[self._NO2NAME]['metadata'][self._LONGITUDENAME] = 'PRODUCT/longitude'
        self.CODA_READ_PARAMETERS[self._NO2NAME]['metadata'][
            self._LONBOUNDSNAME] = 'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/longitude_bounds'
        self.CODA_READ_PARAMETERS[self._NO2NAME]['metadata'][self._LATBOUNDSNAME] = 'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/latitude_bounds'
        self.CODA_READ_PARAMETERS[self._NO2NAME]['metadata'][self._QANAME] = 'PRODUCT/qa_value'
        self.CODA_READ_PARAMETERS[self._NO2NAME]['vars'][self._NO2NAME] = 'PRODUCT/nitrogendioxide_tropospheric_column'

        self.CODA_READ_PARAMETERS[self._O3NAME]['metadata'][self._TIME_NAME] = 'PRODUCT/time'
        self.CODA_READ_PARAMETERS[self._O3NAME]['metadata'][self._TIME_OFFSET_NAME] = 'PRODUCT/delta_time'
        self.CODA_READ_PARAMETERS[self._O3NAME]['metadata'][self._LATITUDENAME] = 'PRODUCT/latitude'
        self.CODA_READ_PARAMETERS[self._O3NAME]['metadata'][self._LONGITUDENAME] = 'PRODUCT/longitude'
        self.CODA_READ_PARAMETERS[self._O3NAME]['metadata'][self._LONBOUNDSNAME] = 'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/longitude_bounds'
        self.CODA_READ_PARAMETERS[self._O3NAME]['metadata'][self._LATBOUNDSNAME] = 'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/latitude_bounds'
        self.CODA_READ_PARAMETERS[self._O3NAME]['metadata'][self._QANAME] = 'PRODUCT/qa_value'
        self.CODA_READ_PARAMETERS[self._O3NAME]['vars'][self._O3NAME] = 'PRODUCT/ozone_total_vertical_column'

        ####################################
        self.NETCDF_VAR_ATTRIBUTES[self._NO2NAME] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._NO2NAME]['_FillValue'] = np.nan
        self.NETCDF_VAR_ATTRIBUTES[self._NO2NAME]['long_name'] = \
            'Tropospheric vertical column of nitrogen dioxide'
        self.NETCDF_VAR_ATTRIBUTES[self._NO2NAME][
            'standard_name'] = 'troposphere_mole_content_of_nitrogen_dioxide'
        self.NETCDF_VAR_ATTRIBUTES[self._NO2NAME]['units'] = 'mol m-2'
        self.NETCDF_VAR_ATTRIBUTES[self._NO2NAME]['coordinates'] = 'longitude latitude'

        self.NETCDF_VAR_ATTRIBUTES[self._NO2NAME + '_mean'] = \
            self.NETCDF_VAR_ATTRIBUTES[self._NO2NAME]

        self.NETCDF_VAR_ATTRIBUTES[self._NO2NAME + '_numobs'] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._NO2NAME + '_numobs']['_FillValue'] = np.nan
        self.NETCDF_VAR_ATTRIBUTES[self._NO2NAME + '_numobs']['long_name'] = \
            'number of observations'
        # self.NETCDF_VAR_ATTRIBUTES[_NO2NAME+'_numobs'][
        #     'standard_name'] = 'troposphere_mole_content_of_nitrogen_dioxide'
        self.NETCDF_VAR_ATTRIBUTES[self._NO2NAME + '_numobs']['units'] = '1'
        self.NETCDF_VAR_ATTRIBUTES[self._NO2NAME + '_numobs']['coordinates'] = 'longitude latitude'

        self.NETCDF_VAR_ATTRIBUTES[self._O3NAME + '_mean'] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._O3NAME + '_mean']['_FillValue'] = np.nan
        self.NETCDF_VAR_ATTRIBUTES[self._O3NAME + '_mean']['long_name'] = \
            'total vertical ozone column'
        self.NETCDF_VAR_ATTRIBUTES[self._O3NAME + '_mean'][
            'standard_name'] = 'atmosphere_mole_content_of_ozone'
        self.NETCDF_VAR_ATTRIBUTES[self._O3NAME + '_mean']['units'] = 'mol m-2'
        self.NETCDF_VAR_ATTRIBUTES[self._O3NAME + '_mean']['coordinates'] = 'longitude latitude'

        # used for L2 writing
        self.NETCDF_VAR_ATTRIBUTES[self._O3NAME] = self.NETCDF_VAR_ATTRIBUTES[self._O3NAME + '_mean']

        self.NETCDF_VAR_ATTRIBUTES[self._O3NAME + '_numobs'] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._O3NAME + '_numobs']['_FillValue'] = np.nan
        self.NETCDF_VAR_ATTRIBUTES[self._O3NAME + '_numobs']['long_name'] = \
            'number of observations'
        # self.NETCDF_VAR_ATTRIBUTES[_O3NAME+'_numobs'][
        #     'standard_name'] = 'troposphere_mole_content_of_nitrogen_dioxide'
        self.NETCDF_VAR_ATTRIBUTES[self._O3NAME + '_numobs']['units'] = '1'
        self.NETCDF_VAR_ATTRIBUTES[self._O3NAME + '_numobs']['coordinates'] = 'longitude latitude'

        self.NETCDF_VAR_ATTRIBUTES[self._QANAME] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._QANAME]['_FillValue'] = np.nan
        self.NETCDF_VAR_ATTRIBUTES[self._QANAME]['long_name'] = 'data quality value'
        self.NETCDF_VAR_ATTRIBUTES[self._QANAME]['comment'] = \
            'A continuous quality descriptor, varying between 0(no data) and 1 (full quality data). Recommend to ignore data with qa_value < 0.5'
        self.NETCDF_VAR_ATTRIBUTES[self._QANAME]['units'] = '1'
        self.NETCDF_VAR_ATTRIBUTES[self._QANAME]['coordinates'] = 'longitude latitude'

        if read_averaging_kernel:
            # reading the averaging kernel needs some more data fields
            self._AVERAGINGKERNELNAME = 'avg_kernel'
            self._AVERAGINGKERNELSIZE = 34
            self._AVERAGINGKERNELINDEX = self._LONBOUNDINDEX + self._LONBOUNDSSIZE + 1
            self._GROUNDPRESSURENAME = 'p0'
            self._GROUNDPRESSUREINDEX = self._AVERAGINGKERNELINDEX + self._AVERAGINGKERNELSIZE
            self._LEVELSNAME = 'levels'
            self._LEVELSSIZE = self._AVERAGINGKERNELSIZE
            self._LEVELSINDEX = self._GROUNDPRESSUREINDEX + 1
            self._TM5_TROPOPAUSE_LAYER_INDEX_NAME = 'tm5_tropopause_layer_index'
            self._TM5_TROPOPAUSE_LAYER_INDEX_INDEX = self._LEVELSINDEX + self._LEVELSSIZE + 1
            self._TM5_CONSTANT_A_NAME = 'tm5_constant_a'
            self._TM5_CONSTANT_A_INDEX = self._TM5_TROPOPAUSE_LAYER_INDEX_INDEX + 1
            self._TM5_CONSTANT_B_NAME = 'tm5_constant_b'
            self._TM5_CONSTANT_B_INDEX = self._TM5_CONSTANT_A_INDEX + 1


            self._COLNO = self._TM5_CONSTANT_B_INDEX + 1
            self.INDEX_DICT.update({self._AVERAGINGKERNELNAME: self._AVERAGINGKERNELINDEX})
            self.INDEX_DICT.update({self._LEVELSNAME: self._LEVELSINDEX})
            self.INDEX_DICT.update({self._GROUNDPRESSURENAME: self._GROUNDPRESSUREINDEX})
            self.INDEX_DICT.update({self._TM5_TROPOPAUSE_LAYER_INDEX_NAME: self._TM5_TROPOPAUSE_LAYER_INDEX_INDEX})
            self.INDEX_DICT.update({self._TM5_CONSTANT_A_NAME: self._TM5_CONSTANT_A_INDEX})
            self.INDEX_DICT.update({self._TM5_CONSTANT_B_NAME: self._TM5_CONSTANT_B_INDEX})

            self.SIZE_DICT.update({self._AVERAGINGKERNELNAME: self._AVERAGINGKERNELSIZE})
            self.SIZE_DICT.update({self._LEVELSNAME: self._LEVELSSIZE})

            self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME] = {}
            self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME]['metadata'] = {}
            self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME]['vars'] = {}
            self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME]['time_offset'] = np.float_(24. * 60. * 60.)
            self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME]['metadata'][self._TIME_NAME] = 'PRODUCT/time'
            self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME]['metadata'][self._TIME_OFFSET_NAME] = 'PRODUCT/delta_time'
            self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME]['metadata'][self._LATITUDENAME] = 'PRODUCT/latitude'
            self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME]['metadata'][self._LONGITUDENAME] = 'PRODUCT/longitude'
            self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME]['metadata'][self._LONBOUNDSNAME] = 'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/longitude_bounds'
            self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME]['metadata'][self._LATBOUNDSNAME] = 'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/latitude_bounds'
            self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME]['metadata'][self._QANAME] = 'PRODUCT/qa_value'
            self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME]['vars'][self._AVERAGINGKERNELNAME] = 'PRODUCT/averaging_kernel'

            self.CODA_READ_PARAMETERS[self._LEVELSNAME] = {}
            self.CODA_READ_PARAMETERS[self._LEVELSNAME]['metadata'] = {}
            self.CODA_READ_PARAMETERS[self._LEVELSNAME]['vars'] = {}
            self.CODA_READ_PARAMETERS[self._LEVELSNAME]['time_offset'] = np.float_(24. * 60. * 60.)
            self.CODA_READ_PARAMETERS[self._LEVELSNAME]['vars'][self._LEVELSNAME] = 'PRODUCT/layer'

            self.CODA_READ_PARAMETERS[self._GROUNDPRESSURENAME] = {}
            self.CODA_READ_PARAMETERS[self._GROUNDPRESSURENAME]['metadata'] = {}
            self.CODA_READ_PARAMETERS[self._GROUNDPRESSURENAME]['vars'] = {}
            self.CODA_READ_PARAMETERS[self._GROUNDPRESSURENAME]['time_offset'] = np.float_(24. * 60. * 60.)
            self.CODA_READ_PARAMETERS[self._GROUNDPRESSURENAME]['vars'][self._GROUNDPRESSURENAME] = \
                'PRODUCT/SUPPORT_DATA/INPUT_DATA/surface_pressure'

            self.CODA_READ_PARAMETERS[self._TM5_TROPOPAUSE_LAYER_INDEX_NAME] = {}
            self.CODA_READ_PARAMETERS[self._TM5_TROPOPAUSE_LAYER_INDEX_NAME]['metadata'] = {}
            self.CODA_READ_PARAMETERS[self._TM5_TROPOPAUSE_LAYER_INDEX_NAME]['vars'] = {}
            self.CODA_READ_PARAMETERS[self._TM5_TROPOPAUSE_LAYER_INDEX_NAME]['time_offset'] = np.float_(24. * 60. * 60.)
            self.CODA_READ_PARAMETERS[self._TM5_TROPOPAUSE_LAYER_INDEX_NAME]['vars'][self._TM5_TROPOPAUSE_LAYER_INDEX_NAME] = \
                'PRODUCT/tm5_tropopause_layer_index'

            self.CODA_READ_PARAMETERS[self._TM5_CONSTANT_A_NAME] = {}
            self.CODA_READ_PARAMETERS[self._TM5_CONSTANT_A_NAME]['metadata'] = {}
            self.CODA_READ_PARAMETERS[self._TM5_CONSTANT_A_NAME]['vars'] = {}
            self.CODA_READ_PARAMETERS[self._TM5_CONSTANT_A_NAME]['time_offset'] = np.float_(24. * 60. * 60.)
            self.CODA_READ_PARAMETERS[self._TM5_CONSTANT_A_NAME]['vars'][self._TM5_CONSTANT_A_NAME] = \
                'PRODUCT/tm5_constant_a'
            self.CODA_READ_PARAMETERS[self._TM5_CONSTANT_B_NAME] = {}
            self.CODA_READ_PARAMETERS[self._TM5_CONSTANT_B_NAME]['metadata'] = {}
            self.CODA_READ_PARAMETERS[self._TM5_CONSTANT_B_NAME]['vars'] = {}
            self.CODA_READ_PARAMETERS[self._TM5_CONSTANT_B_NAME]['time_offset'] = np.float_(24. * 60. * 60.)
            self.CODA_READ_PARAMETERS[self._TM5_CONSTANT_B_NAME]['vars'][self._TM5_CONSTANT_B_NAME] = \
                'PRODUCT/tm5_constant_b'

            self.NETCDF_VAR_ATTRIBUTES[self._AVERAGINGKERNELNAME] = {}
            self.NETCDF_VAR_ATTRIBUTES[self._AVERAGINGKERNELNAME]['_FillValue'] = np.nan
            self.NETCDF_VAR_ATTRIBUTES[self._AVERAGINGKERNELNAME]['long_name'] = 'averaging kernel'
            # self.NETCDF_VAR_ATTRIBUTES[self._AVERAGINGKERNELNAME]['standard_name'] = 'averaging_kernel'
            self.NETCDF_VAR_ATTRIBUTES[self._AVERAGINGKERNELNAME]['units'] = '1'
            self.NETCDF_VAR_ATTRIBUTES[self._AVERAGINGKERNELNAME]['coordinates'] = \
                'longitude latitude {}'.format(self._LEVELSNAME)

            self.CODA_READ_PARAMETERS[self._NO2NAME]['vars'][self._LEVELSNAME] = \
                self.CODA_READ_PARAMETERS[self._LEVELSNAME]['vars'][self._LEVELSNAME]
            self.CODA_READ_PARAMETERS[self._NO2NAME]['vars'][self._GROUNDPRESSURENAME] = \
                self.CODA_READ_PARAMETERS[self._GROUNDPRESSURENAME]['vars'][self._GROUNDPRESSURENAME]
            self.CODA_READ_PARAMETERS[self._NO2NAME]['vars'][self._TM5_TROPOPAUSE_LAYER_INDEX_NAME] = \
                self.CODA_READ_PARAMETERS[self._TM5_TROPOPAUSE_LAYER_INDEX_NAME]['vars'][self._TM5_TROPOPAUSE_LAYER_INDEX_NAME]
            self.CODA_READ_PARAMETERS[self._NO2NAME]['vars'][self._TM5_CONSTANT_A_NAME] = \
                self.CODA_READ_PARAMETERS[self._TM5_CONSTANT_A_NAME]['vars'][self._TM5_CONSTANT_A_NAME]
            self.CODA_READ_PARAMETERS[self._NO2NAME]['vars'][self._TM5_CONSTANT_B_NAME] = \
                self.CODA_READ_PARAMETERS[self._TM5_CONSTANT_B_NAME]['vars'][self._TM5_CONSTANT_B_NAME]
            self.CODA_READ_PARAMETERS[self._NO2NAME]['vars'][self._AVERAGINGKERNELNAME] = \
                self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME]['vars'][self._AVERAGINGKERNELNAME]


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
    def read_file(self, filename, vars_to_retrieve=['tcolno2'], return_as='dict',
                  loglevel=None, apply_quality_flag=True, colno=None, read_avg_kernel=True):
        """method to read the file a Sentinel 5P data file

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : str
            str with variable name to read; defaults to ['tcolno2']
        return_as:
            either 'dict' or 'numpy'; defaults to 'dict'
        loglevel:
            loglevel as for the logging module.
            Since the reading can take some time logging.INFO is recommended
        apply_quality_flag:
            apply the quality flag from the data product; True or False; defaults to True
        colno : int
            # of columns to return in case the return_as parameter is 'numpy'
            In it's extended form this object can also return the lat and lon bounds of the location.
            Unfortunately that adds another 8 rows to the entire data array which might be too memory heavy
            and is onluy needed if the data ins converted to netcdf at this point. So we keep this optional for now
            since the netcdf export is nor yet implemented in pyaerocom.
            if colno < _COLNO the bounds will not be returned in the numpy array
        read_avg_kernel : bool
            also read the averaging kernel
            default: True

        Returns
        --------
        Either:
            dictionary (default):
                keys are 'time', 'latitude', 'longitude', 'altitude' and the variable name
                ('tcolno2' or 'tcolo3' at this point if the whole file is read

            2d ndarray of type float:
                representing a 'point cloud' with all points
                    column 1: time in seconds since the Unix epoch with ms accuracy (same time for every point in the
                              swath)
                    column 2: latitude
                    column 3: longitude
                    column 4: altitude

                    Note: negative values are put to np.nan already



        """

        if colno is None:
            colno = self._COLNO

        import time
        import coda

        start = time.perf_counter()
        file_data = {}

        self.logger.info('reading file {}'.format(filename))
        # read file
        product = coda.open(filename)

        if isinstance(vars_to_retrieve, str):
            read_dataset = [vars_to_retrieve]
        vars_to_read_in = None
        vars_to_read_in = vars_to_retrieve.copy()

        # This is for Sentinel 5p netcdf files read via coda to avoid dealing with all the groups in there
        # coda for S5P uses 2010-01-01T00:00:00 as epoch unfortunately.
        # so calculate the difference in seconds to the Unix epoch
        seconds_to_add = np.datetime64('2010-01-01T00:00:00') - np.datetime64('1970-01-01T00:00:00')
        seconds_to_add = seconds_to_add.astype(np.float_)

        # the same can be achieved using pandas, but we stick to numpy here
        # base_time = pd.DatetimeIndex(['2000-01-01'])
        # seconds_to_add = (base_time.view('int64') // pd.Timedelta(1, unit='s'))[0]

        # if vars_to_retrieve[0] is None:
        #     # read all variables
        #     vars_to_read_in = list(self.CODA_READ_PARAMETERS[vars_to_retrieve[0]]['vars'].keys())
        for _vars in vars_to_retrieve:
            vars_to_read_in.extend(list(self.CODA_READ_PARAMETERS[_vars]['vars'].keys()))
            vars_to_read_in.extend(list(self.CODA_READ_PARAMETERS[_vars]['metadata'].keys()))
        # get rid of duplicates
        vars_to_read_in = list(set(vars_to_read_in))

        # read data time
        # it consists of the base time of the orbit and an offset per scanline

        coda_groups_to_read = (
            self.CODA_READ_PARAMETERS[vars_to_retrieve[0]]['metadata'][self._TIME_NAME].split(self.GROUP_DELIMITER))

        # seconds since 1 Jan 2010
        time_data_temp = coda.fetch(product,
                                    coda_groups_to_read[0],
                                    coda_groups_to_read[1])
        file_data[self._TIME_NAME] = \
            ((time_data_temp + seconds_to_add) * 1.E3).astype(np.int).astype('datetime64[ms]')

        # read the offset per scanline
        coda_groups_to_read = (
            self.CODA_READ_PARAMETERS[vars_to_retrieve[0]]['metadata'][self._TIME_OFFSET_NAME].split(self.GROUP_DELIMITER))

        # the result in in milli seconds an can therefore just added to the base time
        time_data_temp = coda.fetch(product,
                                    coda_groups_to_read[0],
                                    coda_groups_to_read[1])
        file_data[self._TIME_OFFSET_NAME] = \
            file_data[self._TIME_NAME] + np.squeeze(time_data_temp)

        # read data in a simple dictionary
        for var in vars_to_read_in:
            # time has been read already
            if var == self._TIME_NAME or var == self._TIME_OFFSET_NAME:
                continue
            self.logger.info('reading var: {}'.format(var))

            try:
                groups = \
                    self.CODA_READ_PARAMETERS[vars_to_retrieve[0]]['metadata'][var].split(self.GROUP_DELIMITER)
            except KeyError:
                groups = \
                    self.CODA_READ_PARAMETERS[vars_to_retrieve[0]]['vars'][var].split(self.GROUP_DELIMITER)

            # the data comes as record and not as array as at aeolus
            file_data[var] = {}

            if len(groups) == 3:
                file_data[var] = np.squeeze(coda.fetch(product,
                                                       groups[0],
                                                       groups[1],
                                                       groups[2]))

            elif len(groups) == 2:
                file_data[var] = np.squeeze(coda.fetch(product,
                                                       groups[0],
                                                       groups[1]))
            elif len(groups) == 4:

                file_data[var] = np.squeeze(coda.fetch(product,
                                                       groups[0],
                                                       groups[1],
                                                       groups[2],
                                                       groups[3]))
            else:
                file_data[var] = np.squeeze(coda.fetch(product,
                                                       groups[0]))
        coda.close(product)

        if return_as == 'numpy':
            # return as one multidimensional numpy array that can be put into self.data directly
            # (column wise because the column numbers do not match)
            index_pointer = 0
            data = np.empty([self._ROWNO, colno], dtype=np.float_)
            #loop over the times
            for idx, _time in enumerate(file_data[self._TIME_OFFSET_NAME]):
                # loop over the number of ground pixels
                for _index in range(file_data[self._LATITUDENAME].shape[1]):
                    # check first if the quality flag requirement is met

                    if apply_quality_flag and \
                            file_data[self._QANAME][idx, _index] < self.QUALITY_FLAGS[vars_to_retrieve[0]]:
                        # potential debugging...
                        # if _index < 100:
                        #     print(file_data[self._QANAME][idx,_index])
                        continue

                    # time can be a scalar...
                    try:
                        data[index_pointer, self._TIMEINDEX] = _time.astype(np.float_)
                    except:
                        data[index_pointer, self._TIMEINDEX] = _time[_index].astype(np.float_)

                    # loop over the variables
                    for var in vars_to_read_in:
                        # time is the index, so skip it here
                        if var == self._TIME_NAME or var == self._TIME_OFFSET_NAME:
                            continue
                        # the bounds need to be treated special

                        elif colno == self._COLNO and var in self.SIZE_DICT:
                            data[index_pointer,
                            self.INDEX_DICT[var]:self.INDEX_DICT[var] + self.SIZE_DICT[var]] = \
                                file_data[var][idx, _index]
                        else:
                            data[index_pointer, self.INDEX_DICT[var]] = file_data[var][idx, _index]

                    index_pointer += 1
                    if index_pointer >= self._ROWNO:
                        # add another array chunk to self.data
                        data = np.append(data, np.empty([self._CHUNKSIZE, self._COLNO], dtype=np.float_),
                                         axis=0)
                        self._ROWNO += self._CHUNKSIZE

            # return only the needed elements...
            file_data = data[0:index_pointer]

        end_time = time.perf_counter()
        elapsed_sec = end_time - start
        temp = 'time for single file read [s]: {:.3f}'.format(elapsed_sec)
        self.logger.info(temp)
        # self.logger.info('{} points read'.format(index_pointer))
        self.files_read.append(filename)
        return file_data

    ###################################################################################

    # def read(self, vars_to_retrieve=None, files=[], first_file=None,
    #          last_file=None, file_pattern=None, list_coda_paths=False,
    #          local_temp_dir=None):
    #     """Method that reads list of files as instance of :class:`UngriddedData`
    #
    #     Parameters
    #     ----------
    #     vars_to_retrieve : :obj:`list` or similar, optional,
    #         list containing variable IDs that are supposed to be read. If None,
    #         all variables in :attr:`PROVIDES_VARIABLES` are loaded
    #     files : :obj:`list`, optional
    #         list of files to be read. If None, then the file list is used that
    #         is returned on :func:`get_file_list`.
    #     first_file : :obj:`int`, optional
    #         index of first file in file list to read. If None, the very first
    #         file in the list is used. Note: is ignored if input parameter
    #         `file_pattern` is specified.
    #     last_file : :obj:`int`, optional
    #         index of last file in list to read. If None, the very last file
    #         in the list is used. Note: is ignored if input parameter
    #         `file_pattern` is specified.
    #     file_pattern : str, optional
    #         string pattern for file search (cf :func:`get_file_list`)
    #     :param local_temp_dir:
    #
    #     Returns
    #     -------
    #     UngriddedData
    #         data object
    #
    #     Example:
    #     >>> import pyaerocom as pya
    #     >>> obj = pya.io.read_sentinel5p_data.ReadL2Data()
    #     >>> testfiles = []
    #     >>> testfiles.append('/lustre/storeB/project/fou/kl/vals5p/download/O3/S5P_OFFL_L2__O3_____20190531T165100_20190531T183230_08446_01_010107_20190606T185838.nc')
    #     >>> testfiles.append('/lustre/storeB/project/fou/kl/vals5p/download/O3/S5P_OFFL_L2__O3_____20190530T051930_20190530T070100_08425_01_010107_20190605T070532.nc')
    #     >>> data=obj.read(files=testfiles)
    #     or with a tar file:
    #     >>> import pyaerocom as pya
    #     >>> obj = pya.io.read_sentinel5p_data.ReadL2Data()
    #     >>> testfiles = []
    #     >>> testfiles.append('/lustre/storeB/project/fou/kl/vals5p/download/tar/2019/01/tropomi_no2_20190115.tar')
    #     >>> data=obj.read(files=testfiles, vars_to_retrieve='tcolno2')
    #
    #     """
    #
    #     import pathlib
    #     import tarfile
    #     import os
    #
    #     if local_temp_dir is None:
    #         local_temp_dir = self.LOCAL_TMP_DIR
    #
    #     if vars_to_retrieve is None:
    #         vars_to_retrieve = self.DEFAULT_VARS
    #     elif isinstance(vars_to_retrieve, str):
    #         vars_to_retrieve = [vars_to_retrieve]
    #
    #     if files is None:
    #         if len(self.files) == 0:
    #             self.get_file_list(pattern=file_pattern)
    #         files = self.files
    #
    #     if file_pattern is None:
    #         if first_file is None:
    #             first_file = 0
    #         if last_file is None:
    #             last_file = len(files)
    #
    #         files = files[first_file:last_file]
    #
    #     self.read_failed = []
    #     temp_files = {}
    #
    #     data_obj = UngriddedData(num_points=self._COLNO, chunksize=self._CHUNKSIZE)
    #     meta_key = 0.0
    #     idx = 0
    #
    #     # check if the supplied file is a supported archive file (tar in this case)
    #     # and extract the files with supported suffixes to const._cachedir
    #     non_archive_files = []
    #     for idx, _file in enumerate(sorted(files)):
    #         # temp = 'reading file: {}'.format(_file)
    #
    #         self.logger.info('file: {}'.format(_file))
    #         suffix = pathlib.Path(_file).suffix
    #         if suffix in self.SUPPORTED_ARCHIVE_SUFFIXES:
    #             temp = 'opening archive file; using {} as temp dir.'.format(local_temp_dir)
    #             self.logger.info(temp)
    #             # untar archive files first
    #             tarhandle = tarfile.open(_file)
    #             files_in_tar = tarhandle.getnames()
    #             for file_in_tar in files_in_tar:
    #                 if pathlib.Path(file_in_tar).suffix in self.SUPPORTED_SUFFIXES:
    #                     # extract file to tmp path
    #                     member = tarhandle.getmember(file_in_tar)
    #                     temp = 'extracting file {}...'.format(member.name)
    #                     self.logger.info(temp)
    #                     tarhandle.extract(member, path=local_temp_dir, set_attrs=False)
    #                     extract_file = os.path.join(local_temp_dir, member.name)
    #                     non_archive_files.append(extract_file)
    #                     temp_files[extract_file] = True
    #             tarhandle.close()
    #         else:
    #             non_archive_files.append(_file)
    #
    #
    #     for idx, _file in enumerate(sorted(non_archive_files)):
    #         # list coda data paths in the 1st file in case the user asked for that
    #         if idx == 0 and list_coda_paths:
    #             pass
    #             coda_handle = coda.open(_file)
    #             root_field_names = coda.get_field_names(coda_handle)
    #             for field in root_field_names:
    #                 print(field)
    #             coda.close(coda_handle)
    #             data_obj = None
    #             return data_obj
    #
    #         file_data = self.read_file(_file, vars_to_retrieve=vars_to_retrieve,
    #                                    loglevel=logging.INFO, return_as='numpy')
    #         self.logger.info('{} points read'.format(file_data.shape[0]))
    #         # the metadata dict is left empty for L2 data
    #         # the location in the data set is time step dependant!
    #         if idx == 0:
    #             data_obj._data = file_data
    #
    #         else:
    #             data_obj._data = np.append(data_obj._data, file_data, axis=0)
    #
    #         data_obj._idx = data_obj._data.shape[0] + 1
    #         file_data = None
    #         # remove file if it was temporary one
    #         if _file in temp_files:
    #             os.remove(_file)
    #         #     pass
    #         # tmp_obj = UngriddedData()
    #         # tmp_obj._data = file_data
    #         # tmp_obj._idx = data_obj._data.shape[0] + 1
    #         # data_obj.append(tmp_obj)
    #
    #     self.logger.info('size of data object: {}'.format(data_obj._idx - 1))
    #     return data_obj

    ###################################################################################
    

if __name__ == "__main__":
    """small test for the sentinel5p reading...
    """
    import argparse
    import os

    options = {}
    default_topo_file = '/lustre/storeB/project/fou/kl/admaeolus/EMEP.topo/MACC14_topo_v1.nc'
    # default_gridded_out_file = './gridded.nc'
    default_local_temp_dir = '/home/jang/tmp/'

    parser = argparse.ArgumentParser(
        description='command line interface to pyaerocom.io.readsentinel5p_data.py\n\n\n')
    parser.add_argument("--file",
                        help="file(s) to read", nargs="+")
    parser.add_argument("-v", "--verbose", help="switch on verbosity",
                        action='store_true')
    parser.add_argument("--listpaths", help="list the file contents.", action='store_true')
    parser.add_argument("--readpaths", help="read listed rootpaths of coda supported file. Can be comma separated",
                        default='mph,sca_optical_properties')
    parser.add_argument("-o", "--outfile", help="output file")
    parser.add_argument("--outdir", help="output directory; the filename will be extended with the string '.nc'")
    # parser.add_argument("--plotdir", help="directories where the plots will be put; defaults to './'",
    #                     default='./')
    # parser.add_argument("--logfile", help="logfile; defaults to /home/jang/tmp/aeolus2netcdf.log",
    #                     default="/home/jang/tmp/aeolus2netcdf.log")
    parser.add_argument("-O", "--overwrite", help="overwrite output file", action='store_true')
    parser.add_argument("--emep", help="flag to limit the read data to the cal/val model domain",
                        action='store_true')
    parser.add_argument("--himalayas", help="flag to limit the read data to himalayas", action='store_true')
    # parser.add_argument("--codadef", help="set path of CODA_DEFINITION env variable",
    #                     default='/lustre/storeA/project/aerocom/aerocom1/ADM_CALIPSO_TEST/')
    parser.add_argument("--latmin", help="min latitude to return", default=np.float_(30.))
    parser.add_argument("--latmax", help="max latitude to return", default=np.float_(76.))
    parser.add_argument("--lonmin", help="min longitude to return", default=np.float_(-30.))
    parser.add_argument("--lonmax", help="max longitude to return", default=np.float_(45.))
    parser.add_argument("--dir", help="work on all files below this directory",
                        default='/lustre/storeB/project/fou/kl/admaeolus/data.rev.2A02/download/AE_OPER_ALD_U_N_2A_*')
    parser.add_argument("--filemask", help="file mask to find data files",
                        default='*AE_OPER_ALD_U_N_2A_*')
    parser.add_argument("--tempdir", help="directory for temporary files",
                        default=os.path.join(os.environ['HOME'], 'tmp'))
    parser.add_argument("--plotmap", help="flag to plot a map of the data points; files will be put in outdir",
                        action='store_true')
    parser.add_argument("--plotprofile", help="flag to plot the profiles; files will be put in outdir",
                        action='store_true')
    parser.add_argument("--variables",
                        help="comma separated list of variables to write; default: ec355aer,bs355aer",
                        default='ec355aer')
    parser.add_argument("--retrieval", help="retrieval to read; supported: sca, ica, mca; default: sca",
                        default='sca')
    parser.add_argument("--netcdfcolocate", help="flag to add colocation with a netcdf file",
                        action='store_true')
    parser.add_argument("--modeloutdir",
                        help="directory for colocated model files; will have a similar filename as aeolus input file",
                        default=os.path.join(os.environ['HOME'], 'tmp'))
    parser.add_argument("--topofile", help="topography file; defaults to {}.".format(default_topo_file),
                        default=default_topo_file)
    parser.add_argument("--gridfile", help="grid data and write it to given output file (in netcdf).")

    args = parser.parse_args()

    if args.netcdfcolocate:
        options['netcdfcolocate'] = True
    else:
        options['netcdfcolocate'] = False

    if args.filemask:
        options['filemask'] = args.filemask

    if args.gridfile:
        options['gridfile'] = args.gridfile

    if args.retrieval:
        options['retrieval'] = args.retrieval

    if args.modeloutdir:
        options['modeloutdir'] = args.modeloutdir

    if args.dir:
        options['dir'] = args.dir

    if args.outdir:
        options['outdir'] = args.outdir

    # if args.plotdir:
    #     options['plotdir'] = args.plotdir
    # else:
    #     options['plotdir'] = './'

    if args.plotmap:
        options['plotmap'] = True
    else:
        options['plotmap'] = False

    if args.plotprofile:
        options['plotprofile'] = True
    else:
        options['plotprofile'] = False

    if args.tempdir:
        options['tempdir'] = args.tempdir

    if args.latmin:
        options['latmin'] = np.float_(args.latmin)

    if args.latmax:
        options['latmax'] = np.float_(args.latmax)

    if args.lonmin:
        options['lonmin'] = np.float_(args.lonmin)

    if args.lonmax:
        options['lonmax'] = np.float_(args.lonmax)

    if args.emep:
        options['emepflag'] = args.emep
        options['latmin'] = np.float(30.)
        options['latmax'] = np.float(76.)
        options['lonmin'] = np.float(-30.)
        options['lonmax'] = np.float(45.)
    else:
        options['emepflag'] = False

    if args.himalayas:
        options['himalayas'] = args.himalayas
        options['latmin'] = np.float(10.)
        options['latmax'] = np.float(50.)
        options['lonmin'] = np.float(60.)
        options['lonmax'] = np.float(110.)
    else:
        options['himalayas'] = False

    if args.readpaths:
        options['readpaths'] = args.readpaths.split(',')

    if args.variables:
        options['variables'] = args.variables.split(',')

    if args.file:
        options['files'] = args.file

    if args.listpaths:
        options['listpaths'] = True
    else:
        options['listpaths'] = False

    if args.verbose:
        options['verbose'] = True
    else:
        options['verbose'] = False

    if args.overwrite:
        options['overwrite'] = True
    else:
        options['overwrite'] = False

    if args.outfile:
        options['outfile'] = args.outfile

    # if args.codadef:
    #     options['codadef'] = args.codadef

    if args.topofile:
        options['topofile'] = args.topofile

    import os
    # os.environ['CODA_DEFINITION'] = options['codadef']
    import coda
    import sys
    import glob
    import pathlib
    import tarfile
    import time
    import pyaerocom as pya

    bbox = None
    obj = ReadL2Data(verbose=True)
    non_archive_files = []
    temp_files_dir = {}
    temp_file_flag = False

    if 'files' not in options:
        options['files'] = glob.glob(options['dir'] + '/**/' + options['filemask'], recursive=True)

    vars_to_retrieve = options['variables'].copy()

    data_numpy = obj.read(files=options['files'], vars_to_retrieve=vars_to_retrieve[0],
                          local_temp_dir=default_local_temp_dir)

    # limit data to EMEP CAMS domain
    if options['emepflag']:
        bbox = [options['latmin'], options['latmax'], options['lonmin'], options['lonmax']]
        tmp_data = obj.select_bbox(data_numpy, bbox)
        if len(tmp_data) > 0:
            data_numpy = tmp_data
            obj.logger.info('data object contains {} points in emep area! '.format(len(tmp_data)))
        else:
            obj.logger.info('data object contains no data in emep area! ')
            data_numpy = None
            # continue

    if options['himalayas']:
        bbox = [options['latmin'], options['latmax'], options['lonmin'], options['lonmax']]
        tmp_data = obj.select_bbox(data_numpy, bbox)
        if len(tmp_data) > 0:
            data_numpy = tmp_data
            obj.logger.info('file {} contains {} points in himalaya area! '.format(filename, len(tmp_data)))
        else:
            obj.logger.info('file {} contains no data in himalaya area! '.format(filename))
            data_numpy = None
            # continue

    if 'outfile' in options or 'gridfile' in options or 'outdir' in options:
        global_attributes = {}
        global_attributes['input files']=','.join(obj.files_read)
        global_attributes['info']='file created by pyaerocom.io.read_sentinel5p_data '+obj.__version__+' (https://github.com/metno/pyaerocom) at '+\
                                  np.datetime64('now').astype('str')
        global_attributes['quality']='quality flag of 0.7 applied'

    # obj.to_netcdf_simple(data_to_write=data_numpy, global_attributes=obj.global_attributes, vars_to_write=obj.DEFAULT_VARS,
    #                      netcdf_filename='/home/jang/tmp/to_netcdf_simple.nc')
    # gridded_data = obj.to_grid(data=data, vars=obj.DEFAULT_VARS, )
    # obj.to_netcdf_simple(data_to_write=gridded_data, global_attributes=global_attributes, vars_to_write=obj.DEFAULT_VARS,
    #                      gridded=True,
    #                      netcdf_filename='/home/jang/tmp/to_netcdf_simple_gridded.nc')

    # write L2 ungridded single outfile
    if 'outfile' in options:
        # write netcdf
        if os.path.exists(options['outfile']):
            if options['overwrite']:
                obj.to_netcdf_simple(netcdf_filename=options['outfile'], data_to_write=data_numpy,
                                     global_attributes=global_attributes, vars_to_write=vars_to_retrieve)
            else:
                sys.stderr.write('Error: path {} exists'.format(options['outfile']))
        else:
            # obj.to_netcdf_simple(options['outfile'], global_attributes=ancilliary_data['mph'])
            obj.to_netcdf_simple(netcdf_filename=options['outfile'], data_to_write=data_numpy,
                                 global_attributes=global_attributes, vars_to_write=vars_to_retrieve)

    # write L3 gridded data
    if 'gridfile' in options:
        gridded_var_data = obj.to_grid(data=data_numpy, vars=vars_to_retrieve)

        obj.to_netcdf_simple(netcdf_filename=options['gridfile'],
                             vars_to_write=vars_to_retrieve,
                             global_attributes=global_attributes,
                             data_to_write=gridded_var_data,
                             gridded=True)

    if options['plotmap']:
        if len(obj.gridded_data.keys()) == 0:
            # gridding has not been done yet
            gridded_var_data = obj.to_grid(vars=vars_to_retrieve)

        if len(obj.files_read) == 1:
            # single file read
            plotmapfilename = os.path.join(options['plotdir'], '_'.join([options['variables'][0],
                                                                         os.path.basename(
                                                                             obj.files_read[0])]) + '.map.png')
            title = '\n'.join([options['variables'][0], os.path.basename(obj.files_read[0])])
            obj.plot_map(gridded_var_data, plotmapfilename, bbox=bbox, title=title)
        else:
            # archive file read
            plot_date = np.datetime64(obj.gridded_data['time'], 'D').astype('str')
            for var in options['variables']:
                plotmapfilename = os.path.join(options['plotdir'], '_'.join([var, plot_date]) + '.map.png')
                obj.logger.info('map plot file: {}'.format(plotmapfilename))
                title = '_'.join([var, plot_date])
                # title = os.path.basename(filename)

                obj.plot_map(gridded_var_data, plotmapfilename, bbox=bbox, title=title)
                # obj.plot_location_map(plotmapfilename)

    # obj = pya.io.read_sentinel5p_data.ReadL2Data()
    # testfiles = []
    #
    # testfiles.append('/lustre/storeB/project/fou/kl/vals5p/download/O3/S5P_OFFL_L2__O3_____20190531T165100_20190531T183230_08446_01_010107_20190606T185838.nc')
    # testfiles.append('/lustre/storeB/project/fou/kl/vals5p/download/O3/S5P_OFFL_L2__O3_____20190530T051930_20190530T070100_08425_01_010107_20190605T070532.nc')
    # data = obj.read(files=testfiles)
    # global_attributes = {}
    # global_attributes['input files']=','.join(obj.files_read)
    # global_attributes['info']='file created by pyaerocom.io.read_sentinel5p_data '+obj.__version__+' (https://github.com/metno/pyaerocom) at '+\
    #                           np.datetime64('now').astype('str')
    # global_attributes['quality']='quality flag of 0.7 applied'
    #
    # # print(data._data[0:10, obj._TIMEINDEX].astype('datetime64[ms]'))
    # obj.to_netcdf_simple(data_to_write=data, global_attributes=global_attributes, vars_to_write=obj.DEFAULT_VARS,
    #                      netcdf_filename='/home/jang/tmp/to_netcdf_simple.nc')
    # gridded_data = obj.to_grid(data=data, vars=obj.DEFAULT_VARS, )
    # obj.to_netcdf_simple(data_to_write=gridded_data, global_attributes=global_attributes, vars_to_write=obj.DEFAULT_VARS,
    #                      gridded=True,
    #                      netcdf_filename='/home/jang/tmp/to_netcdf_simple_gridded.nc')
