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

from pyaerocom.io.readungriddedbase import ReadUngriddedBase
import geopy
import numpy as np
import logging
from pyaerocom import const
from pyaerocom.ungriddeddata import UngriddedData


class ReadL2Data(ReadUngriddedBase):
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

    SUPPORTED_SUFFIXES = []
    SUPPORTED_SUFFIXES.append('.nc')

    SUPPORTED_ARCHIVE_SUFFIXES = []
    SUPPORTED_ARCHIVE_SUFFIXES.append('.TGZ')
    SUPPORTED_ARCHIVE_SUFFIXES.append('.tgz')
    SUPPORTED_ARCHIVE_SUFFIXES.append('.tar')
    SUPPORTED_ARCHIVE_SUFFIXES.append('.tar.gz')

    GLOBAL_ATTRIBUTES = {}
    FILE_DIR = ''
    FILE_MASK = '*.nc'

    # variable names
    # dimension data
    _LATITUDENAME = 'latitude'
    _LONGITUDENAME = 'longitude'
    _ALTITUDENAME = 'altitude'

    _TIME_NAME = 'time'
    _TIME_OFFSET_NAME = 'delta_time'
    _NO2NAME = 'tcolno2'
    _O3NAME = 'tcolo3'
    _QANAME = 'qa_index'

    _LATBOUNDSNAME = 'lat_bnds'
    _LATBOUNDSSIZE = 4
    _LONBOUNDSNAME = 'lon_bnds'
    _LONBOUNDSSIZE = 4

    COORDINATE_NAMES = [_LATITUDENAME, _LONGITUDENAME, _ALTITUDENAME, _LATBOUNDSNAME, _LONBOUNDSNAME]


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
    # _DATAINDEX02 = 8
    # _DATAINDEX03 = 9
    # _DATAINDEX04 = 10
    _QAINDEX = UngriddedData._DATAFLAGINDEX
    _TIME_OFFSET_INDEX = UngriddedData._TRASHINDEX
    _LATBOUNDINDEX = 13
    _LONBOUNDINDEX = _LATBOUNDINDEX + _LATBOUNDSSIZE + 1

    _COLNO = _LATBOUNDINDEX + _LATBOUNDSSIZE + _LONBOUNDSSIZE + 2

    _ROWNO = 1000000
    _CHUNKSIZE = 100000
    _HEIGHTSTEPNO = 24

    GROUP_DELIMITER = '/'

    # create a dict with the aerocom variable name as key and the index number in the
    # resulting numpy array as value.
    INDEX_DICT = {}
    INDEX_DICT.update({_LATITUDENAME: _LATINDEX})
    INDEX_DICT.update({_LONGITUDENAME: _LONINDEX})
    INDEX_DICT.update({_ALTITUDENAME: _ALTITUDEINDEX})
    INDEX_DICT.update({_TIME_NAME: _TIMEINDEX})
    INDEX_DICT.update({_TIME_OFFSET_NAME: _TIME_OFFSET_INDEX})
    INDEX_DICT.update({_NO2NAME: _DATAINDEX01})
    INDEX_DICT.update({_O3NAME: _DATAINDEX01})
    INDEX_DICT.update({_QANAME: _QAINDEX})
    INDEX_DICT.update({_LATBOUNDSNAME: _LATBOUNDINDEX})
    INDEX_DICT.update({_LONBOUNDSNAME: _LONBOUNDINDEX})

    # dictionary to store array sizes of an element in self.data
    SIZE_DICT = {}
    SIZE_DICT.update({_LATBOUNDSNAME: _LATBOUNDSSIZE})
    SIZE_DICT.update({_LONBOUNDSNAME: _LONBOUNDSSIZE})

    # NaN values are variable specific
    NAN_DICT = {}
    NAN_DICT.update({_LATITUDENAME: -1.E-6})
    NAN_DICT.update({_LONGITUDENAME: -1.E-6})
    NAN_DICT.update({_ALTITUDENAME: -1.})

    # the following defines necessary quality flags for a value to make it into the used data set
    # the flag needs to have a HIGHER or EQUAL value than the one listed here
    # The valuse are taken form the product readme file
    QUALITY_FLAGS = {}
    QUALITY_FLAGS.update({_NO2NAME: 0.75})
    # QUALITY_FLAGS.update({_NO2NAME: 0.5}) #cloudy
    QUALITY_FLAGS.update({_O3NAME: 0.7})

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
    NETCDF_VAR_ATTRIBUTES['latitude'] = {}
    # NETCDF_VAR_ATTRIBUTES['latitude']['_FillValue'] = {}
    NETCDF_VAR_ATTRIBUTES['latitude']['long_name'] = 'latitude'
    NETCDF_VAR_ATTRIBUTES['latitude']['standard_name'] = 'latitude'
    NETCDF_VAR_ATTRIBUTES['latitude']['units'] = 'degrees north'
    NETCDF_VAR_ATTRIBUTES['latitude']['bounds'] = 'lat_bnds'
    NETCDF_VAR_ATTRIBUTES['latitude']['axis'] = 'Y'
    NETCDF_VAR_ATTRIBUTES['longitude'] = {}
    # NETCDF_VAR_ATTRIBUTES['longitude']['_FillValue'] = {}
    NETCDF_VAR_ATTRIBUTES['longitude']['long_name'] = 'longitude'
    NETCDF_VAR_ATTRIBUTES['longitude']['standard_name'] = 'longitude'
    NETCDF_VAR_ATTRIBUTES['longitude']['units'] = 'degrees_east'
    NETCDF_VAR_ATTRIBUTES['longitude']['bounds'] = 'lon_bnds'
    NETCDF_VAR_ATTRIBUTES['longitude']['axis'] = 'X'
    NETCDF_VAR_ATTRIBUTES['altitude'] = {}
    # NETCDF_VAR_ATTRIBUTES['altitude']['_FillValue'] = {}
    NETCDF_VAR_ATTRIBUTES['altitude']['long_name'] = 'altitude'
    NETCDF_VAR_ATTRIBUTES['altitude']['standard_name'] = 'altitude'
    NETCDF_VAR_ATTRIBUTES['altitude']['units'] = 'm'

    NETCDF_VAR_ATTRIBUTES[_NO2NAME] = {}
    NETCDF_VAR_ATTRIBUTES[_NO2NAME]['_FillValue'] = np.nan
    NETCDF_VAR_ATTRIBUTES[_NO2NAME]['long_name'] = \
        'Tropospheric vertical column of nitrogen dioxide'
    NETCDF_VAR_ATTRIBUTES[_NO2NAME][
        'standard_name'] = 'troposphere_mole_content_of_nitrogen_dioxide'
    NETCDF_VAR_ATTRIBUTES[_NO2NAME]['units'] = 'mol m-2'
    NETCDF_VAR_ATTRIBUTES[_NO2NAME]['coordinates'] = 'longitude latitude'

    NETCDF_VAR_ATTRIBUTES[_NO2NAME+'_mean'] = \
        NETCDF_VAR_ATTRIBUTES[_NO2NAME]

    NETCDF_VAR_ATTRIBUTES[_NO2NAME+'_numobs'] = {}
    NETCDF_VAR_ATTRIBUTES[_NO2NAME+'_numobs']['_FillValue'] = np.nan
    NETCDF_VAR_ATTRIBUTES[_NO2NAME+'_numobs']['long_name'] = \
        'number of observations'
    # NETCDF_VAR_ATTRIBUTES[_NO2NAME+'_numobs'][
    #     'standard_name'] = 'troposphere_mole_content_of_nitrogen_dioxide'
    NETCDF_VAR_ATTRIBUTES[_NO2NAME+'_numobs']['units'] = '1'
    NETCDF_VAR_ATTRIBUTES[_NO2NAME+'_numobs']['coordinates'] = 'longitude latitude'

    NETCDF_VAR_ATTRIBUTES[_O3NAME+'_mean'] = {}
    NETCDF_VAR_ATTRIBUTES[_O3NAME+'_mean']['_FillValue'] = np.nan
    NETCDF_VAR_ATTRIBUTES[_O3NAME+'_mean']['long_name'] = \
        'total vertical ozone column'
    NETCDF_VAR_ATTRIBUTES[_O3NAME+'_mean'][
        'standard_name'] = 'atmosphere_mole_content_of_ozone'
    NETCDF_VAR_ATTRIBUTES[_O3NAME+'_mean']['units'] = 'mol m-2'
    NETCDF_VAR_ATTRIBUTES[_O3NAME+'_mean']['coordinates'] = 'longitude latitude'

    NETCDF_VAR_ATTRIBUTES[_O3NAME+'_numobs'] = {}
    NETCDF_VAR_ATTRIBUTES[_O3NAME+'_numobs']['_FillValue'] = np.nan
    NETCDF_VAR_ATTRIBUTES[_O3NAME+'_numobs']['long_name'] = \
        'number of observations'
    # NETCDF_VAR_ATTRIBUTES[_O3NAME+'_numobs'][
    #     'standard_name'] = 'troposphere_mole_content_of_nitrogen_dioxide'
    NETCDF_VAR_ATTRIBUTES[_O3NAME+'_numobs']['units'] = '1'
    NETCDF_VAR_ATTRIBUTES[_O3NAME+'_numobs']['coordinates'] = 'longitude latitude'

    NETCDF_VAR_ATTRIBUTES[_QANAME] = {}
    NETCDF_VAR_ATTRIBUTES[_QANAME]['_FillValue'] = np.nan
    NETCDF_VAR_ATTRIBUTES[_QANAME]['long_name'] = 'data quality value'
    NETCDF_VAR_ATTRIBUTES[_QANAME]['comment'] = \
        'A continuous quality descriptor, varying between 0(no data) and 1 (full quality data). Recommend to ignore data with qa_value < 0.5'
    NETCDF_VAR_ATTRIBUTES[_QANAME]['units'] = '1'
    NETCDF_VAR_ATTRIBUTES[_QANAME]['coordinates'] = 'longitude latitude'

    CODA_READ_PARAMETERS = {}
    CODA_READ_PARAMETERS[_NO2NAME] = {}
    CODA_READ_PARAMETERS[_NO2NAME]['metadata'] = {}
    CODA_READ_PARAMETERS[_NO2NAME]['vars'] = {}
    CODA_READ_PARAMETERS[_NO2NAME]['time_offset'] = np.float_(24. * 60. * 60.)
    CODA_READ_PARAMETERS[_O3NAME] = {}
    CODA_READ_PARAMETERS[_O3NAME]['metadata'] = {}
    CODA_READ_PARAMETERS[_O3NAME]['vars'] = {}
    CODA_READ_PARAMETERS[_O3NAME]['time_offset'] = np.float_(24. * 60. * 60.)

    # CODA_READ_PARAMETERS[DATASET_NAME]['metadata'][_TIME_NAME] = 'PRODUCT/time_utc'
    CODA_READ_PARAMETERS[_NO2NAME]['metadata'][_TIME_NAME] = 'PRODUCT/time'
    CODA_READ_PARAMETERS[_NO2NAME]['metadata'][_TIME_OFFSET_NAME] = 'PRODUCT/delta_time'
    CODA_READ_PARAMETERS[_NO2NAME]['metadata'][_LATITUDENAME] = 'PRODUCT/latitude'
    CODA_READ_PARAMETERS[_NO2NAME]['metadata'][_LONGITUDENAME] = 'PRODUCT/longitude'
    CODA_READ_PARAMETERS[_NO2NAME]['metadata'][_LONBOUNDSNAME] = 'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/longitude_bounds'
    CODA_READ_PARAMETERS[_NO2NAME]['metadata'][_LATBOUNDSNAME] = 'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/latitude_bounds'
    CODA_READ_PARAMETERS[_NO2NAME]['metadata'][_QANAME] = 'PRODUCT/qa_value'
    CODA_READ_PARAMETERS[_NO2NAME]['vars'][_NO2NAME] = 'PRODUCT/nitrogendioxide_tropospheric_column'

    CODA_READ_PARAMETERS[_O3NAME]['metadata'][_TIME_NAME] = 'PRODUCT/time'
    CODA_READ_PARAMETERS[_O3NAME]['metadata'][_TIME_OFFSET_NAME] = 'PRODUCT/delta_time'
    CODA_READ_PARAMETERS[_O3NAME]['metadata'][_LATITUDENAME] = 'PRODUCT/latitude'
    CODA_READ_PARAMETERS[_O3NAME]['metadata'][_LONGITUDENAME] = 'PRODUCT/longitude'
    CODA_READ_PARAMETERS[_O3NAME]['metadata'][_LONBOUNDSNAME] = 'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/longitude_bounds'
    CODA_READ_PARAMETERS[_O3NAME]['metadata'][_LATBOUNDSNAME] = 'PRODUCT/SUPPORT_DATA/GEOLOCATIONS/latitude_bounds'
    CODA_READ_PARAMETERS[_O3NAME]['metadata'][_QANAME] = 'PRODUCT/qa_value'
    CODA_READ_PARAMETERS[_O3NAME]['vars'][_O3NAME] = 'PRODUCT/ozone_total_vertical_column'

    SUPPORTED_DATASETS = []
    SUPPORTED_DATASETS.append(DATA_ID)

    DEFAULT_VARS = [_O3NAME]
    PROVIDES_VARIABLES = [_NO2NAME, _O3NAME]
    TS_TYPE = 'undefined'

    def __init__(self, dataset_to_read=None, index_pointer=0, loglevel=logging.INFO, verbose=False):
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
    def read_file(self, filename, vars_to_retrieve='tcolno2', return_as='dict',
                  loglevel=None, apply_quality_flag=True, colno=_COLNO):
        """method to read the file partially

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

        import time
        import coda

        start = time.perf_counter()
        file_data = {}

        self.logger.info('reading file {}'.format(filename))
        # read file
        product = coda.open(filename)

        # if isinstance(read_dataset, str):
        #     read_dataset = [read_dataset]
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

        if vars_to_retrieve is None:
            # read all variables
            vars_to_read_in = list(self.CODA_READ_PARAMETERS[vars_to_retrieve[0]]['vars'].keys())
        vars_to_read_in.extend(list(self.CODA_READ_PARAMETERS[vars_to_retrieve[0]]['metadata'].keys()))
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

                    if apply_quality_flag and file_data[self._QANAME][idx, _index] < self.QUALITY_FLAGS[
                        vars_to_retrieve[0]]:
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

        coda.close(product)
        end_time = time.perf_counter()
        elapsed_sec = end_time - start
        temp = 'time for single file read [s]: {:.3f}'.format(elapsed_sec)
        self.logger.info(temp)
        # self.logger.info('{} points read'.format(index_pointer))
        self.files_read.append(filename)
        return file_data

    ###################################################################################

    def read(self, vars_to_retrieve=None, files=[], first_file=None,
             last_file=None, file_pattern=None):
        """Method that reads list of files as instance of :class:`UngriddedData`

        Parameters
        ----------
        vars_to_retrieve : :obj:`list` or similar, optional,
            list containing variable IDs that are supposed to be read. If None,
            all variables in :attr:`PROVIDES_VARIABLES` are loaded
        files : :obj:`list`, optional
            list of files to be read. If None, then the file list is used that
            is returned on :func:`get_file_list`.
        first_file : :obj:`int`, optional
            index of first file in file list to read. If None, the very first
            file in the list is used. Note: is ignored if input parameter
            `file_pattern` is specified.
        last_file : :obj:`int`, optional
            index of last file in list to read. If None, the very last file
            in the list is used. Note: is ignored if input parameter
            `file_pattern` is specified.
        file_pattern : str, optional
            string pattern for file search (cf :func:`get_file_list`)

        Returns
        -------
        UngriddedData
            data object

        Example:
        >>> import pyaerocom as pya
        >>> obj = pya.io.read_sentinel5p_data.ReadL2Data()
        >>> testfiles = []
        >>> testfiles.append('/lustre/storeB/project/fou/kl/vals5p/download/O3/S5P_OFFL_L2__O3_____20190531T165100_20190531T183230_08446_01_010107_20190606T185838.nc')
        >>> testfiles.append('/lustre/storeB/project/fou/kl/vals5p/download/O3/S5P_OFFL_L2__O3_____20190530T051930_20190530T070100_08425_01_010107_20190605T070532.nc')
        >>> data=obj.read(files=testfiles)
        or with a tar file:
        >>> import pyaerocom as pya
        >>> obj = pya.io.read_sentinel5p_data.ReadL2Data()
        >>> testfiles = []
        >>> testfiles.append('/lustre/storeB/project/fou/kl/vals5p/download/tar/2019/01/tropomi_no2_20190115.tar')
        >>> data=obj.read(files=testfiles, vars_to_retrieve='tcolno2')
        """

        import pathlib
        import tarfile
        import os

        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]

        if files is None:
            if len(self.files) == 0:
                self.get_file_list(pattern=file_pattern)
            files = self.files

        if file_pattern is None:
            if first_file is None:
                first_file = 0
            if last_file is None:
                last_file = len(files)

            files = files[first_file:last_file]

        self.read_failed = []
        temp_files = {}

        data_obj = UngriddedData(num_points=self._COLNO, chunksize=self._CHUNKSIZE)
        meta_key = 0.0
        idx = 0

        # check if the supplied file is a supported archive file (tar in this case)
        # and extract the files with supported suffixes to const._cachedir
        non_archive_files = []
        for idx, _file in enumerate(sorted(files)):
            # temp = 'reading file: {}'.format(_file)

            self.logger.info('file: {}'.format(_file))
            suffix = pathlib.Path(_file).suffix
            if suffix in self.SUPPORTED_ARCHIVE_SUFFIXES:
                temp = 'opening archive file; using {} as temp dir.'.format(const._cachedir)
                self.logger.info(temp)
                # untar archive files first
                tarhandle = tarfile.open(_file)
                files_in_tar = tarhandle.getnames()
                for file_in_tar in files_in_tar:
                    if pathlib.Path(file_in_tar).suffix in self.SUPPORTED_SUFFIXES:
                        # extract file to tmp path
                        member = tarhandle.getmember(file_in_tar)
                        temp = 'extracting file {}...'.format(member.name)
                        self.logger.info(temp)
                        tarhandle.extract(member, path=const._cachedir, set_attrs=False)
                        extract_file = os.path.join(const._cachedir, member.name)
                        non_archive_files.append(extract_file)
                        temp_files[extract_file] = True
                tarhandle.close()
            else:
                non_archive_files.append(_file)


        for idx, _file in enumerate(sorted(non_archive_files)):
            file_data = self.read_file(_file, vars_to_retrieve=vars_to_retrieve,
                                       loglevel=logging.INFO, return_as='numpy')
            self.logger.info('{} points read'.format(file_data.shape[0]))
            # the metadata dict is left empty for L2 data
            # the location in the data set is time step dependant!
            if idx == 0:
                data_obj._data = file_data

            else:
                data_obj._data = np.append(data_obj._data, file_data, axis=0)

            data_obj._idx = data_obj._data.shape[0] + 1
            file_data = None
            # remove file if it was temporary one
            if _file in temp_files:
                os.remove(_file)
            #     pass
            # tmp_obj = UngriddedData()
            # tmp_obj._data = file_data
            # tmp_obj._idx = data_obj._data.shape[0] + 1
            # data_obj.append(tmp_obj)

        self.logger.info('size of data object: {}'.format(data_obj._idx - 1))

    ###################################################################################
if __name__=="__main__":
    """small test for the sentinel5p reading...
    """
    import pyaerocom as pya
    obj = pya.io.read_sentinel5p_data.ReadL2Data()
    testfiles = []
    testfiles.append('/lustre/storeB/project/fou/kl/vals5p/download/O3/S5P_OFFL_L2__O3_____20190531T165100_20190531T183230_08446_01_010107_20190606T185838.nc')
    testfiles.append('/lustre/storeB/project/fou/kl/vals5p/download/O3/S5P_OFFL_L2__O3_____20190530T051930_20190530T070100_08425_01_010107_20190605T070532.nc')
    data = obj.read(files=testfiles)
    pass
