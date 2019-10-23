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
        self._SCANLINENAME = 'scanline'
        self._GROUNDPIXELNAME = 'ground_pixel'

        self._LATBOUNDSNAME = 'lat_bnds'
        self._LATBOUNDSSIZE = 4
        self._LONBOUNDSNAME = 'lon_bnds'
        self._LONBOUNDSSIZE = 4
        self.COORDINATE_NAMES = [self._LATITUDENAME, self._LONGITUDENAME, self._ALTITUDENAME,
                                 self._LATBOUNDSNAME, self._LONBOUNDSNAME, self._LEVELSNAME,
                                 self._TIME_NAME]

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
        self.CODA_READ_PARAMETERS[self._NO2NAME]['metadata'][self._SCANLINENAME] = 'PRODUCT/scanline'
        self.CODA_READ_PARAMETERS[self._NO2NAME]['metadata'][self._GROUNDPIXELNAME] = 'PRODUCT/ground_pixel'
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
        self.CODA_READ_PARAMETERS[self._O3NAME]['metadata'][self._SCANLINENAME] = 'PRODUCT/scanline'
        self.CODA_READ_PARAMETERS[self._O3NAME]['metadata'][self._GROUNDPIXELNAME] = 'PRODUCT/ground_pixel'
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
            self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME]['metadata'][self._SCANLINENAME] = 'PRODUCT/scanline'
            self.CODA_READ_PARAMETERS[self._AVERAGINGKERNELNAME]['metadata'][self._GROUNDPIXELNAME] = 'PRODUCT/ground_pixel'
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

    def to_netcdf_simple(self, netcdf_filename='/home/jang/tmp/to_netcdf_simple.nc', global_attributes=None,
                         vars_to_write=None, data_to_write=None, gridded=False):

        if data_to_write is None:
            _data = self.data
        else:
            _data = data_to_write._data

        if isinstance(_data, dict):
            # write out the read data using the dictionary directly
            vars_to_write_out = vars_to_write.copy()
            if isinstance(vars_to_write_out, str):
                vars_to_write_out = [vars_to_write_out]

            ds = self.to_xarray(_data)

            # add potential global attributes
            try:
                for name in global_attributes:
                    ds.attrs[name] = global_attributes[name]
            except:
                pass

            ds.to_netcdf(netcdf_filename)
            obj.logger.info('file {} written'.format(netcdf_filename))
        else:
            #call super class
            super().to_netcdf_simple(netcdf_filename, global_attributes, vars_to_write, data_to_write, gridded)

    ###################################################################################
    def _match_dim_name(self, dim_dict, dim_size=None, data=None):
        """small helper routine to match the dimension size to a dimension name"""

        # try to match the shapes to the dimensions
        ret_data ={}

        if data is not None:
            for var in data:
                ret_data[var] = []
                for _size in data[var].shape:
                    try:
                        ret_data[var].append(dim_dict[_size])
                    except:
                        pass
            return ret_data
        else:
            return dim_dict[dim_size]
    ###################################################################################

    def to_xarray(self,data_to_write=None, gridded=False):
        """helper method to turn a read dictionary into an xarray dataset opbject"""

        if isinstance(data_to_write,dict):
            _data = data_to_write
        else:
            _data = data_to_write._data

        import xarray as xr
        import numpy as np

        if not gridded:
            # vars_to_write_out.extend(list(self.CODA_READ_PARAMETERS[vars_to_write[0]]['metadata'].keys()))
            # var_write_out = _data.keys()

            # datetimedata = pd.to_datetime(_data[:, self._TIMEINDEX].astype('datetime64[s]'))
            # build the datetimedata...
            ts_no = len(_data['scanline'])
            swath_width = len(_data['ground_pixel'])
            point_dim_len = ts_no * swath_width
            datetimedata = np.empty(point_dim_len)
            for idx, _time in enumerate(_data['delta_time']):
                # print('range: {} to {}'.format(idx*swath_width,(idx+1)*swath_width-1))
                datetimedata[idx * swath_width:(idx + 1) * swath_width] = _data['delta_time'][idx]
                # datetimedata[idx*swath_width:(idx+1)*swath_width] = _data['delta_time'].astype('datetime64[ms]')
            # datetimedata = pd.to_datetime(_data[:, self._TIMEINDEX].astype('datetime64[ms]'))
            # pointnumber = np.arange(0, len(datetimedata))
            bounds_dim_name = 'bounds'
            bounds_dim_size = 4
            point_dim_name = 'point'
            point_dim_size = point_dim_len
            swath_dim_name = self._GROUNDPIXELNAME
            swath_dim_size = swath_width
            level_dim_name = self._LEVELSNAME
            level_dim_size = self._LEVELSSIZE
            tm5_constant_dim_name = 'const_dim'
            tm5_constant_dim_size = 2
            scanline_dim_name = self._SCANLINENAME
            scanline_dim_size = ts_no
            ds = xr.Dataset()

            # time and potentially levels are special variables that needs special treatment
            ds[self._TIME_NAME] = (point_dim_name), datetimedata.astype('datetime64[ms]')
            skip_vars = [self._TIME_NAME]
            skip_vars.extend(['delta_time'])
            ds[self._LEVELSNAME] = (level_dim_name), np.arange(self._LEVELSSIZE)
            skip_vars.extend([self._LEVELSNAME])
            ds[self._GROUNDPIXELNAME] = (swath_dim_name), _data['ground_pixel']
            skip_vars.extend([self._GROUNDPIXELNAME])
            ds[point_dim_name] = np.arange(point_dim_len)
            ds[tm5_constant_dim_name] = np.arange(tm5_constant_dim_size)
            ds[bounds_dim_name] = np.arange(4)

            # define a dict with the dimension size as key and the dimensions name as value
            dim_size_dict = {}
            dim_size_dict[point_dim_size] = point_dim_name
            dim_size_dict[bounds_dim_size] = bounds_dim_name
            dim_size_dict[swath_dim_size] = swath_dim_name
            dim_size_dict[level_dim_size] = level_dim_name
            dim_size_dict[tm5_constant_dim_size] = tm5_constant_dim_name
            dim_size_dict[scanline_dim_size] = scanline_dim_name

            dim_name_dict = self._match_dim_name(dim_size_dict, data=_data)
            for var in _data:
                # loop through the variables
                if var in skip_vars:
                    continue
                print('variable: {}'.format(var))
                if len(_data[var].shape) == 1:
                    # var with dimension time (e.g. 3245)
                    # each time needs to be repeated by the swath width
                    try:
                        ds[var] = (point_dim_name), _data[var]
                    except ValueError:
                        ds[var] = (dim_size_dict[_data[var].shape[0]]), _data[var]

                elif len(_data[var].shape) == 2:
                    # var with dimension time and swath (e.g. 3245, 450)
                    try:
                        ds[var] = (point_dim_name), _data[var].reshape(point_dim_len)
                    except ValueError:
                        ds[var] = (dim_name_dict[var]), _data[var]

                elif len(_data[var].shape) == 3:
                    # var with dimension time, swath and levels or bounds
                    # store some vars depending on the points dimension as a 2d variable
                    if var == 'avg_kernel':
                        ds[var] = (point_dim_name, level_dim_name), _data[var].reshape([point_dim_size, level_dim_size])
                    elif var == 'lat_bnds' or var == 'lon_bnds':
                        ds[var] = (point_dim_name, bounds_dim_name), _data[var].reshape(
                            [point_dim_size, bounds_dim_size])
                    else:
                        ds[var] = (dim_name_dict[var]), _data[var]
                        pass

            # add attributes to variables
            for var in ds:
                # add predifined attributes
                try:
                    for attrib in self.NETCDF_VAR_ATTRIBUTES[var]:
                        ds[var].attrs[attrib] = self.NETCDF_VAR_ATTRIBUTES[var][attrib]

                except KeyError:
                    pass

            # remove _FillValue attribute from coordinate variables since that
            # is forbidden by CF convention
            for var in self.COORDINATE_NAMES:
                # if var in self.COORDINATE_NAMES:
                try:
                    del ds[var].encoding['_FillValue']
                except KeyError:
                    pass

                # # add predifined attributes
                # try:
                #     for attrib in self.NETCDF_VAR_ATTRIBUTES[var]:
                #         ds[var].attrs[attrib] = self.NETCDF_VAR_ATTRIBUTES[var][attrib]
                #
                # except KeyError:
                #     pass
            return ds
        else:
            # gridded
            pass

    ###################################################################################

    def to_grid(self, data=None, vars=None, gridtype='1x1', engine='python', return_data_for_gridding=True,
                averaging_kernels=None):
        """to_grid method that takes a xarray.Dataset object as input"""

        import xarray as xr
        import numpy as np

        if isinstance(data,dict):
            _data = self.to_xarray(data_to_write=data)
        else:
            _data = self.to_xarray(data_to_write=data._data)

        if engine == 'python':
            data_for_gridding, gridded_var_data, grid_lats, grid_lons, max_grid_dist_lat, max_grid_dist_lon = \
                self._to_grid_grid_init(gridtype=gridtype, vars=vars ,init_time=_data['time'].mean())


            start_time = time.perf_counter()
            matching_points = 0
            # predefine the output data dict
            # data_for_gridding = {}

            # Loop through the output grid and collect data
            # store that in data_for_gridding[var]
            for lat_idx, grid_lat in enumerate(grid_lats):
                diff_lat = np.absolute((_data[self._LATITUDENAME].data - grid_lat))
                lat_match_indexes = np.squeeze(np.where(diff_lat <= (max_grid_dist_lat/2.)))
                print('lat: {}, matched indexes: {}'.format(grid_lat, lat_match_indexes.size))
                if lat_match_indexes.size == 0:
                    continue

                for lon_idx, grid_lon in enumerate(grid_lons):
                    diff_lon = np.absolute((_data[self._LONGITUDENAME].data[lat_match_indexes] - grid_lon))
                    lon_match_indexes = np.squeeze(np.where(diff_lon <= (max_grid_dist_lon/2.)))
                    if lon_match_indexes.size == 0:
                        continue

                    for var in vars:
                        if return_data_for_gridding:
                            data_for_gridding[var][grid_lat][grid_lon] = \
                                np.array(_data[self._LONGITUDENAME].data[lat_match_indexes[lon_match_indexes]])
                            # np.array(data[lat_match_indexes[lon_match_indexes], self.INDEX_DICT[var]])

                        gridded_var_data[var]['mean'][lat_idx, lon_idx] = \
                            np.nanmean(_data[var].data[lat_match_indexes[lon_match_indexes]])
                        gridded_var_data[var]['stddev'][lat_idx, lon_idx] = \
                            np.nanstd(_data[var].data[lat_match_indexes[lon_match_indexes]])
                        gridded_var_data[var]['numobs'][lat_idx, lon_idx] = \
                            _data[var].data[lat_match_indexes[lon_match_indexes]].size
                        matching_points = matching_points + _data[var].data[lat_match_indexes[lon_match_indexes]].size

            end_time = time.perf_counter()
            elapsed_sec = end_time - start_time
            temp = 'time for global 1x1 gridding with python data types [s]: {:.3f}'.format(elapsed_sec)
            self.logger.info(temp)
            temp = 'matched {} points out of {} existing points to grid'.format(matching_points, _data['time'].size)
            self.logger.info(temp)

            if return_data_for_gridding:
                self.logger.info('returning also data_for_gridding...')
                return gridded_var_data, data_for_gridding
            else:
                return gridded_var_data

        elif gridtype == '1x1_emep':
            # 1 by on degree grid on emep domain
            pass


        pass






        if isinstance(data, xr.Dataset):

            pass
        else:
            super().to_grid(data=None, vars=None, gridtype='1x1', engine='python', return_data_for_gridding=False)
    ###################################################################################

    def _to_grid_grid_init(self,gridtype='1x1',vars=None,init_time=None):
        """small helper routine to init the grid data struct"""

        import numpy as np

        start_time = time.perf_counter()
        grid_data_prot = {}

        grid_lats = []
        grid_lons = []
        gridded_var_data = {}
        max_grid_dist_lon = 0.
        max_grid_dist_lat = 0.
        data_for_gridding = {}

        if gridtype == '1x1':
            # global 1x1 degree grid
            # pass
            temp = 'starting simple gridding for 1x1 degree grid...'
            self.logger.info(temp)
            max_grid_dist_lon = 1.
            max_grid_dist_lat = 1.
            grid_lats = np.arange(-89.5, 90.5, max_grid_dist_lat)
            grid_lons = np.arange(-179.5, 180.5, max_grid_dist_lon)

            grid_array_prot = np.full((grid_lats.size, grid_lons.size), np.nan)
            # organise the data in a nested python dict like dict_data[grid_lat][grid_lon]=np.ndarray
            for grid_lat in grid_lats:
                grid_data_prot[grid_lat] = {}
                for grid_lon in grid_lons:
                    grid_data_prot[grid_lat][grid_lon] = {}

            end_time = time.perf_counter()
            elapsed_sec = end_time - start_time
            temp = 'time for global 1x1 gridding with python data types [s] init: {:.3f}'.format(elapsed_sec)
            self.logger.info(temp)

            # predefine the output data dict
            for var in vars:
                data_for_gridding[var] = grid_data_prot.copy()
                gridded_var_data['latitude'] = grid_lats
                gridded_var_data['longitude'] = grid_lons
                gridded_var_data['time'] = init_time

                gridded_var_data[var] = {}
                gridded_var_data[var]['mean'] = grid_array_prot.copy()
                gridded_var_data[var]['stddev'] = grid_array_prot.copy()
                gridded_var_data[var]['numobs'] = grid_array_prot.copy()
        else:
            pass


        return data_for_gridding, gridded_var_data, grid_lats, grid_lons, max_grid_dist_lat, max_grid_dist_lon


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
                          local_temp_dir=default_local_temp_dir, return_as='dict')

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
