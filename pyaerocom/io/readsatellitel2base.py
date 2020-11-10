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

    SUPPORTED_DATASETS = []
    SUPPORTED_DATASETS.append(DATA_ID)

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

        self.SUPPORTED_SUFFIXES = []

        self.SUPPORTED_ARCHIVE_SUFFIXES = []
        self.SUPPORTED_ARCHIVE_SUFFIXES.append('.TGZ')
        self.SUPPORTED_ARCHIVE_SUFFIXES.append('.tgz')
        self.SUPPORTED_ARCHIVE_SUFFIXES.append('.tar')
        self.SUPPORTED_ARCHIVE_SUFFIXES.append('.tar.gz')

        self.GLOBAL_ATTRIBUTES = {}

        # variable names
        # dimension data
        self._LATITUDENAME = 'latitude'
        self._LONGITUDENAME = 'longitude'
        self._ALTITUDENAME = 'altitude'
        self._LEVELSNAME = 'level'
        self._LEVELSSIZE = 34

        self._TIME_NAME = 'time'

        # variable names for the different retrievals

        self._TIMEINDEX = UngriddedData._TIMEINDEX
        self._LATINDEX = UngriddedData._LATINDEX
        self._LONINDEX = UngriddedData._LONINDEX
        self._ALTITUDEINDEX = UngriddedData._ALTITUDEINDEX
        # for distance calculations we need the location in radians
        # so store these for speed in self.data
        # the following indexes indicate the column where that is stored
        # _RADLATINDEX = 4
        # _RADLONINDEX = 5
        # _DISTINDEX = 6

        self._DATAINDEX01 = UngriddedData._DATAINDEX
        self._COLNO = 12

        self._CHUNKSIZE = 100000

        self.GROUP_DELIMITER = '/'

        # create a dict with the aerocom variable name as key and the index number in the
        # resulting numpy array as value.
        self.INDEX_DICT = {}
        self.INDEX_DICT.update({self._LATITUDENAME: self._LATINDEX})
        self.INDEX_DICT.update({self._LONGITUDENAME: self._LONINDEX})
        self.INDEX_DICT.update({self._ALTITUDENAME: self._ALTITUDEINDEX})
        self.INDEX_DICT.update({self._TIME_NAME: self._TIMEINDEX})

        # dictionary to store array sizes of an element in self.data
        self.SIZE_DICT = {}

        # NaN values are variable specific
        self.NAN_DICT = {}

        # the following defines necessary quality flags for a value to make it into the used data set
        # the flag needs to have a HIGHER or EQUAL value than the one listed here
        # The valuse are taken form the product readme file
        self.QUALITY_FLAGS = {}

        # PROVIDES_VARIABLES = list(RETRIEVAL_READ_PARAMETERS['sca']['metadata'].keys())
        # PROVIDES_VARIABLES.extend(RETRIEVAL_READ_PARAMETERS['sca']['vars'].keys())

        # max distance between point on the earth's surface for a match
        # in meters
        self.MAX_DISTANCE = 50000.
        self.EARTH_RADIUS = geopy.distance.EARTH_RADIUS
        self.NANVAL_META = -1.E-6
        self.NANVAL_DATA = -1.E6

        # these are the variable specific attributes written into a netcdf file
        self.NETCDF_VAR_ATTRIBUTES = {}
        self.NETCDF_VAR_ATTRIBUTES[self._LATITUDENAME] = {}
        # NETCDF_VAR_ATTRIBUTES[_LATITUDENAME]['_FillValue'] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._LATITUDENAME]['long_name'] = 'latitude'
        self.NETCDF_VAR_ATTRIBUTES[self._LATITUDENAME]['standard_name'] = 'latitude'
        self.NETCDF_VAR_ATTRIBUTES[self._LATITUDENAME]['units'] = 'degrees_north'
        self.NETCDF_VAR_ATTRIBUTES[self._LATITUDENAME]['bounds'] = 'lat_bnds'
        self.NETCDF_VAR_ATTRIBUTES[self._LATITUDENAME]['axis'] = 'Y'
        self.NETCDF_VAR_ATTRIBUTES[self._LONGITUDENAME] = {}
        # self.NETCDF_VAR_ATTRIBUTES[_LONGITUDENAME]['_FillValue'] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._LONGITUDENAME]['long_name'] = 'longitude'
        self.NETCDF_VAR_ATTRIBUTES[self._LONGITUDENAME]['standard_name'] = 'longitude'
        self.NETCDF_VAR_ATTRIBUTES[self._LONGITUDENAME]['units'] = 'degrees_east'
        self.NETCDF_VAR_ATTRIBUTES[self._LONGITUDENAME]['bounds'] = 'lon_bnds'
        self.NETCDF_VAR_ATTRIBUTES[self._LONGITUDENAME]['axis'] = 'X'
        self.NETCDF_VAR_ATTRIBUTES[self._ALTITUDENAME] = {}
        # self.NETCDF_VAR_ATTRIBUTES[_ALTITUDENAME]['_FillValue'] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._ALTITUDENAME]['long_name'] = 'altitude'
        self.NETCDF_VAR_ATTRIBUTES[self._ALTITUDENAME]['standard_name'] = 'altitude'
        self.NETCDF_VAR_ATTRIBUTES[self._ALTITUDENAME]['units'] = 'm'

        self.CODA_READ_PARAMETERS = {}

        self.DATASET_READ = ''

        self.COORDINATE_NAMES = []

        self.SCALING_FACTORS = {}
        # list with static field names
        self.STATICFIELDNAMES = []
        # field name whose size determines the number of time steps in a product
        self.TSSIZENAME=''

        self._QANAME = ''
        # DEFAULT_VARS = []
        # PROVIDES_VARIABLES = []
        # self.DEFAULT_VARS = []

        # grid definitions for to_grid method
        self.SUPPORTED_GRIDS = {}

        try:
            self.LOCAL_TMP_DIR = const.LOCAL_TMP_DIR
        except:
            self.LOCAL_TMP_DIR = const.CACHEDIR

        # some gridding constants
        self.MIN_LAT = -90.
        self.MAX_LAT = 90.
        self.MIN_LON = -180.
        self.MAX_LON = 180.
        # supported grids
        self.SUPPORTED_GRIDS['MODEL'] = {}
        self.SUPPORTED_GRIDS['MODEL']['grid_dist_lon'] = 0.25
        self.SUPPORTED_GRIDS['MODEL']['grid_dist_lat'] = 0.125
        self.SUPPORTED_GRIDS['CAMS50'] = {}
        self.SUPPORTED_GRIDS['CAMS50']['grid_dist_lon'] = 0.25
        self.SUPPORTED_GRIDS['CAMS50']['grid_dist_lat'] = 0.125
        self.SUPPORTED_GRIDS['1x1'] = {}
        self.SUPPORTED_GRIDS['1x1']['grid_dist_lon'] = 1.
        self.SUPPORTED_GRIDS['1x1']['grid_dist_lat'] = 1.
        self.SUPPORTED_GRIDS['0.5x0.5'] = {}
        self.SUPPORTED_GRIDS['0.5x0.5']['grid_dist_lon'] = 0.5
        self.SUPPORTED_GRIDS['0.5x0.5']['grid_dist_lat'] = 0.5
        self.SUPPORTED_GRIDS['0.1x0.1'] = {}
        self.SUPPORTED_GRIDS['0.1x0.1']['grid_dist_lon'] = 0.1
        self.SUPPORTED_GRIDS['0.1x0.1']['grid_dist_lat'] = 0.1

        for grid_name in self.SUPPORTED_GRIDS:
            self.SUPPORTED_GRIDS[grid_name]['grid_lats'] = \
                np.arange(self.MIN_LAT + self.SUPPORTED_GRIDS[grid_name]['grid_dist_lat'] / 2.,
                          self.MAX_LAT + self.SUPPORTED_GRIDS[grid_name]['grid_dist_lat'] / 2.,
                          self.SUPPORTED_GRIDS[grid_name]['grid_dist_lat'])
            self.SUPPORTED_GRIDS[grid_name]['grid_lons'] = \
                np.arange(self.MIN_LON + self.SUPPORTED_GRIDS[grid_name]['grid_dist_lon'] / 2.,
                          self.MAX_LON + self.SUPPORTED_GRIDS[grid_name]['grid_dist_lon'] / 2.,
                          self.SUPPORTED_GRIDS[grid_name]['grid_dist_lon'])

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

    def read(self, vars_to_retrieve=None, files=[], first_file=None,
             last_file=None, file_pattern=None, list_coda_paths=False,
             local_temp_dir=None, return_as='numpy', apply_quality_flag=0.0):
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
        :param local_temp_dir:

        Returns
        -------
        UngriddedData
            data object

        Example:
        >>> import pyaerocom as pya
        >>> obj = pya.io.read_aeolus_l2a_data.ReadL2Data()
        >>> testfiles = []
        >>> testfiles.append('/lustre/storeB/project/fou/kl/admaeolus/data.rev.2A02/download/2018-12/01/AE_OPER_ALD_U_N_2A_20181201T033526026_005423993_001590_0001.TGZ')
        >>> data=obj.read(files=testfiles)
        >>> data=obj.read(files=testfiles, vars_to_retrieve='ec355aer')

        """

        import pathlib
        import tarfile
        import os
        import coda

        if local_temp_dir is None:
            local_temp_dir = self.LOCAL_TMP_DIR

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

        data_obj = UngriddedData(num_points=self._CHUNKSIZE)
        meta_key = 0.0
        idx = 0

        # check if the supplied file is a supported archive file (tar in this case)
        # and extract the files with supported suffixes to const.CACHEDIR
        non_archive_files = []
        for idx, _file in enumerate(sorted(files)):
            # temp = 'reading file: {}'.format(_file)

            self.logger.info('file: {}'.format(_file))
            suffix = pathlib.Path(_file).suffix
            if suffix in self.SUPPORTED_ARCHIVE_SUFFIXES:
                temp = 'opening archive file; using {} as temp dir.'.format(local_temp_dir)
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
                        tarhandle.extract(member, path=local_temp_dir, set_attrs=False)
                        extract_file = os.path.join(local_temp_dir, member.name)
                        non_archive_files.append(extract_file)
                        temp_files[extract_file] = True
                tarhandle.close()
            else:
                non_archive_files.append(_file)

        for idx, _file in enumerate(sorted(non_archive_files)):
            # list coda data paths in the 1st file in case the user asked for that
            if idx == 0 and list_coda_paths:
                pass
                coda_handle = coda.open(_file)
                root_field_names = coda.get_field_names(coda_handle)
                for field in root_field_names:
                    print(field)
                coda.close(coda_handle)
                data_obj = None
                return data_obj

            file_data = self.read_file(_file, vars_to_retrieve=vars_to_retrieve,
                                       loglevel=logging.INFO, return_as=return_as)
            if return_as == 'numpy':
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
            elif return_as == 'dict':
                if idx == 0:
                    data_obj._data = {}
                    shape_store = {}
                    index_store = {}
                    file_start_index_arr = [0]
                    # apply quality flags
                    if apply_quality_flag > 0.:
                        qflags = file_data[self._QANAME]
                        keep_indexes=np.where(qflags >= apply_quality_flag)
                        elements_to_add = keep_indexes.size
                    else:
                        keep_indexes=np.arange(0,len(file_data[self._QANAME]))
                        elements_to_add = file_data[self._QANAME].shape[0]

                    for _key in file_data:
                        # print('key: {}'.format(_key))
                        shape_store[_key] = file_data[_key].shape
                        index_store[_key] = file_data[_key].shape[0]
                        input_shape = list(file_data[_key].shape)
                        input_shape[0] = self._ROWNO
                        data_obj._data[_key] = np.empty(input_shape, dtype=np.float_)
                        if len(input_shape) == 1:
                            data_obj._data[_key][0:file_data[_key].shape[0]] = file_data[_key]
                        elif len(input_shape) == 2:
                            data_obj._data[_key][0:file_data[_key].shape[0],:] = file_data[_key]
                        elif len(input_shape) == 3:
                            data_obj._data[_key][0:file_data[_key].shape[0],:,:] = file_data[_key]
                        elif len(input_shape) == 4:
                            data_obj._data[_key][0:file_data[_key].shape[0],:,:,:] = file_data[_key]
                        else:
                            pass

                # 2nd + file
                else:
                    if apply_quality_flag > 0.:
                        qflags = file_data[self._QANAME]
                        keep_indexes=np.where(qflags >= apply_quality_flag)
                        elements_to_add = keep_indexes.size

                    file_start_index_arr.append(file_data[self.TSSIZENAME].shape[0])
                    for _key in file_data:
                        if _key in self.STATICFIELDNAMES:
                            print('key: {}'.format(_key))
                            continue
                        # shape_store[_key] = file_data[_key].shape
                        elements_to_add = file_data[_key].shape[0]
                        # extend data_obj._data[_key] if necessary
                        if index_store[_key] + elements_to_add > data_obj._data[_key].shape[0]:
                            current_shape = list(data_obj._data[_key].shape)
                            current_shape[0] = current_shape[0] + self._CHUNKSIZE
                            tmp_data = np.empty(current_shape, dtype=np.float_)
                            if len(current_shape) == 1:
                                tmp_data[0:data_obj._data[_key].shape[0]] = data_obj._data[_key]
                            elif len(current_shape) == 2:
                                tmp_data[0:data_obj._data[_key].shape[0],:] = data_obj._data[_key]
                            elif len(current_shape) == 3:
                                tmp_data[0:data_obj._data[_key].shape[0],:,:] = data_obj._data[_key]
                            elif len(current_shape) == 4:
                                tmp_data[0:data_obj._data[_key].shape[0],:,:,:] = data_obj._data[_key]
                            else:
                                pass

                        input_shape = list(file_data[_key].shape)
                        if len(input_shape) == 1:
                            data_obj._data[_key][index_store[_key]:index_store[_key]+file_data[_key].shape[0]] = file_data[_key]
                        elif len(input_shape) == 2:
                            data_obj._data[_key][index_store[_key]:index_store[_key]+file_data[_key].shape[0],:] = file_data[_key]
                        elif len(input_shape) == 3:
                            data_obj._data[_key][index_store[_key]:index_store[_key]+file_data[_key].shape[0],:,:] = file_data[_key]
                        elif len(input_shape) == 4:
                            data_obj._data[_key][index_store[_key]:index_store[_key]+file_data[_key].shape[0],:,:,:] = file_data[_key]
                        else:
                            pass
                        index_store[_key] += elements_to_add

                file_data = None
                # remove file if it was temporary one
                if _file in temp_files:
                    os.remove(_file)
            else:
                pass

        # now shorten the data dict to the necessary size
        if return_as == 'dict':
            for _key in data_obj._data:
                data_obj._data[_key] = data_obj._data[_key][:index_store[_key]]
            data_obj._data['file_indexes'] = file_start_index_arr

            # apply the quality flags
            if apply_quality_flag > 0.:
                pass

        return data_obj

    ###################################################################################

    def to_netcdf_simple(self, netcdf_filename='/home/jang/tmp/to_netcdf_simple.nc',
                         global_attributes=None, vars_to_write=None,
                         data_to_write=None, gridded=False):

        """method to store the file contents in a very basic netcdf file

        Parameters:
        ----------
            global_attributes : dict
            dictionary with things to put into the global attributes of a netcdf file

        """
        import time
        start_time = time.perf_counter()
        import xarray as xr
        import pandas as pd
        import numpy as np

        vars_to_write_out = vars_to_write.copy()
        if isinstance(vars_to_write_out, str):
            vars_to_write_out = [vars_to_write_out]

        if not gridded:
            if netcdf_filename is None:
                netcdf_filename = '/tmp/to_netcdf_simple.nc'
            if data_to_write is None:
                _data = self.data
            else:
                try:
                    _data = data_to_write._data
                except AttributeError:
                    _data = data_to_write

            # vars_to_read_in.extend(list(self.CODA_READ_PARAMETERS[self.DATASET_READ]['metadata'].keys()))
            vars_to_write_out.extend(list(self.CODA_READ_PARAMETERS[vars_to_write[0]]['metadata'].keys()))

            # datetimedata = pd.to_datetime(_data[:, self._TIMEINDEX].astype('datetime64[s]'))
            datetimedata = pd.to_datetime(_data[:, self._TIMEINDEX].astype('datetime64[ms]'))
            # pointnumber = np.arange(0, len(datetimedata))
            bounds_dim_name = 'bounds'
            point_dim_name = 'point'
            level_dim_name = self._LEVELSNAME
            ds = xr.Dataset()

            # time and potentially levels are special variables that needs special treatment
            ds[self._TIME_NAME] = (point_dim_name), datetimedata
            skip_vars = [self._TIME_NAME]
            if level_dim_name in vars_to_write_out:
                ds[level_dim_name] = np.arange(self._LEVELSSIZE)
                skip_vars.extend([self._LEVELSNAME])

            for var in vars_to_write_out:
                if var in skip_vars:
                    continue
                # 1D data
                if var not in self.SIZE_DICT:
                    ds[var] = (point_dim_name), _data[:, self.INDEX_DICT[var]]
                else:
                    # 2D data: here: bounds
                    ds[var] = ((point_dim_name, bounds_dim_name),
                               _data[:, self.INDEX_DICT[var]:self.INDEX_DICT[var] + self.SIZE_DICT[var]])

                # remove _FillVar attribute for coordinate variables as CF requires it
                if var in self.COORDINATE_NAMES:
                    ds[var].encoding['_FillValue'] = None

                # add predefined attributes
                try:
                    for attrib in self.NETCDF_VAR_ATTRIBUTES[var]:
                        ds[var].attrs[attrib] = self.NETCDF_VAR_ATTRIBUTES[var][attrib]

                except KeyError:
                    pass

        else:
            # write gridded data to netcdf
            if netcdf_filename is None:
                netcdf_filename = '/tmp/to_netcdf_simple_gridded.nc'
            if data_to_write is None:
                _data = self.gridded_data
            else:
                _data = data_to_write

            bounds_dim_name = 'bounds'
            time_dim_name = 'time'
            lat_dim_name = 'latitude'
            lon_dim_name = 'longitude'

            ds = xr.Dataset()

            # coordinate variables need special treatment

            ds[time_dim_name] = (time_dim_name), [np.datetime64(_data[time_dim_name], 'D')]
            ds[lat_dim_name] = (lat_dim_name), _data[lat_dim_name],
            ds[lon_dim_name] = (lon_dim_name), _data[lon_dim_name]

            for var in vars_to_write_out:
                if var == self._TIME_NAME:
                    continue
                # 1D data
                # 3D data
                ds[var + '_mean'] = (time_dim_name, lat_dim_name, lon_dim_name), np.reshape(_data[var]['mean'], (
                len(ds[time_dim_name]), len(_data[lat_dim_name]), len(_data[lon_dim_name])))
                ds[var + '_numobs'] = (time_dim_name, lat_dim_name, lon_dim_name), np.reshape(_data[var]['numobs'], (
                len(ds[time_dim_name]), len(_data[lat_dim_name]), len(_data[lon_dim_name])))

                # remove _FillVar attribute for coordinate variables as CF requires it

            vars_to_write_out.extend([time_dim_name, lat_dim_name, lon_dim_name])

            for var in ds:
                # add predifined attributes
                try:
                    for attrib in self.NETCDF_VAR_ATTRIBUTES[var]:
                        ds[var].attrs[attrib] = self.NETCDF_VAR_ATTRIBUTES[var][attrib]

                except KeyError:
                    pass

            for var in ds.coords:
                if var in self.COORDINATE_NAMES:
                    ds[var].encoding['_FillValue'] = None

                # add predifined attributes
                try:
                    for attrib in self.NETCDF_VAR_ATTRIBUTES[var]:
                        ds[var].attrs[attrib] = self.NETCDF_VAR_ATTRIBUTES[var][attrib]

                except KeyError:
                    pass

        # add potential global attributes
        try:
            for name in global_attributes:
                ds.attrs[name] = global_attributes[name]
        except:
            pass

        ds.to_netcdf(netcdf_filename)

        end_time = time.perf_counter()
        elapsed_sec = end_time - start_time
        temp = 'time for netcdf write [s]: {:.3f}'.format(elapsed_sec)
        self.logger.info(temp)
        temp = 'file written: {}'.format(netcdf_filename)
        self.logger.info(temp)

    ###################################################################################
    def to_grid(self, data=None, vars=None, gridtype='1x1', engine='python', return_data_for_gridding=False):
        """simple gridding algorithm that only takes the pixel middle points into account

        All the data points in data are considered!

        """
        import numpy as np
        import time

        _vars = vars.copy()
        if isinstance(_vars, str):
            _vars = [_vars]

        if data is None:
            data = self.data
        else:
            data = data._data
        # vars_to_retrieve = self.DEFAULT_VARS

        if engine == 'python':
            start_time = time.perf_counter()
            grid_data_prot = {}
            # define ouput grid
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
                        grid_data_prot[grid_lat] = {}

                end_time = time.perf_counter()
                elapsed_sec = end_time - start_time
                temp = 'time for global 1x1 gridding with python data types [s] init: {:.3f}'.format(elapsed_sec)
                self.logger.info(temp)

                # predefine the output data dict
                data_for_gridding = {}
                gridded_var_data = {}
                for var in vars:
                    data_for_gridding[var] = grid_data_prot.copy()
                    gridded_var_data['latitude'] = grid_lats
                    gridded_var_data['longitude'] = grid_lons
                    gridded_var_data['time'] = np.mean(data[:, self._TIMEINDEX]).astype('datetime64[ms]')

                    gridded_var_data[var] = {}
                    gridded_var_data[var]['mean'] = grid_array_prot.copy()
                    gridded_var_data[var]['stddev'] = grid_array_prot.copy()
                    gridded_var_data[var]['numobs'] = grid_array_prot.copy()

                # Loop through the output grid and collect data
                # store that in data_for_gridding[var]
                for lat_idx, grid_lat in enumerate(grid_lats):
                    diff_lat = np.absolute((data[:, self._LATINDEX] - grid_lat))
                    lat_match_indexes = np.squeeze(np.where(diff_lat <= max_grid_dist_lat))
                    if lat_match_indexes.size == 0:
                        continue

                    for lon_idx, grid_lon in enumerate(grid_lons):
                        diff_lon = np.absolute((data[lat_match_indexes, self._LONINDEX] - grid_lon))
                        lon_match_indexes = np.squeeze(np.where(diff_lon <= max_grid_dist_lon))
                        if lon_match_indexes.size == 0:
                            continue

                        for var in vars:
                            data_for_gridding[var][grid_lat][grid_lon] = \
                                np.array(data[lat_match_indexes[lon_match_indexes], self.INDEX_DICT[var]])
                            gridded_var_data[var]['mean'][lat_idx, lon_idx] = \
                                np.nanmean(data[lat_match_indexes[lon_match_indexes], self.INDEX_DICT[var]])
                            gridded_var_data[var]['stddev'][lat_idx, lon_idx] = \
                                np.nanstd(data[lat_match_indexes[lon_match_indexes], self.INDEX_DICT[var]])
                            gridded_var_data[var]['numobs'][lat_idx, lon_idx] = \
                                data[lat_match_indexes[lon_match_indexes], self.INDEX_DICT[var]].size

                # now go through self.data and select the appropriate data points
                # self.data_for_gridding = data_for_gridding
                # self.gridded_data = gridded_var_data
                end_time = time.perf_counter()
                elapsed_sec = end_time - start_time
                temp = 'time for global 1x1 gridding with python data types [s]: {:.3f}'.format(elapsed_sec)
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

        pass

    ###################################################################################
    def _to_grid_grid_init(self,gridtype='1x1',vars=None,init_time=None):
        """small helper routine to init the grid data struct"""

        import numpy as np
        import time

        start_time = time.perf_counter()
        grid_data_prot = {}
        gridded_var_data = {}
        data_for_gridding = {}

        if gridtype in self.SUPPORTED_GRIDS:
            temp = 'starting simple gridding for {} grid...'.format(gridtype)
            self.logger.info(temp)

            grid_array_prot = np.full((self.SUPPORTED_GRIDS[gridtype]['grid_lats'].size,
                                       self.SUPPORTED_GRIDS[gridtype]['grid_lons'].size), np.nan)
            # organise the data in a nested python dict like dict_data[grid_lat][grid_lon]=np.ndarray
            for grid_lat in self.SUPPORTED_GRIDS[gridtype]['grid_lats']:
                grid_data_prot[grid_lat] = {}
                for grid_lon in self.SUPPORTED_GRIDS[gridtype]['grid_lons']:
                    grid_data_prot[grid_lat][grid_lon] = {}

            pass
        else:
            temp = 'Error: Unknown grid: {}'.format(gridtype)
            return

        end_time = time.perf_counter()
        elapsed_sec = end_time - start_time
        temp = 'time for global {} gridding with python data types [s] init: {:.3f}'.format(gridtype, elapsed_sec)
        self.logger.info(temp)

        # predefine the output data dict
        for var in vars:
            data_for_gridding[var] = grid_data_prot.copy()
            gridded_var_data['latitude'] = self.SUPPORTED_GRIDS[gridtype]['grid_lats']
            gridded_var_data['longitude'] = self.SUPPORTED_GRIDS[gridtype]['grid_lons']
            gridded_var_data['time'] = init_time

            gridded_var_data[var] = {}
            gridded_var_data[var]['mean'] = grid_array_prot.copy()
            gridded_var_data[var]['stddev'] = grid_array_prot.copy()
            gridded_var_data[var]['numobs'] = grid_array_prot.copy()

        return data_for_gridding, \
               gridded_var_data,

    ###################################################################################

    def select_bbox(self, _data, bbox=None):
        """method to return all points of data laying within a certain latitude and longitude range

        EXAMPLE
        =======
        """
        import time
        start = time.perf_counter()

        # ret_data = np.empty([self._ROWNO, self._COLNO], dtype=np.float_)
        # index_counter = 0
        # cut_flag = True
        data = _data._data

        if bbox is not None:
            logging.info(bbox)
            lat_min = bbox[0]
            lat_max = bbox[1]
            lon_min = bbox[2]
            lon_max = bbox[3]

            # remove NaNs at this point
            matching_indexes = np.where(np.isfinite(data[:, self._LATINDEX]))
            ret_data = data[matching_indexes[0], :]

            # np.where can unfortunately only work with a single criterion
            matching_indexes = np.where(ret_data[:, self._LATINDEX] <= lat_max)
            ret_data = ret_data[matching_indexes[0], :]
            # logging.warning('len after lat_max: {}'.format(len(ret_data)))
            matching_indexes = np.where(ret_data[:, self._LATINDEX] >= lat_min)
            ret_data = ret_data[matching_indexes[0], :]
            # logging.warning('len after lat_min: {}'.format(len(ret_data)))
            matching_indexes = np.where(ret_data[:, self._LONINDEX] <= lon_max)
            ret_data = ret_data[matching_indexes[0], :]
            # logging.warning('len after lon_max: {}'.format(len(ret_data)))
            matching_indexes = np.where(ret_data[:, self._LONINDEX] >= lon_min)
            ret_data = ret_data[matching_indexes[0], :]
            # logging.warning('len after lon_min: {}'.format(len(ret_data)))
            # matching_length = len(matching_indexes[0])
            _data._data = ret_data
            return _data

    ###################################################################################

    def plot_map(self, gridded_data, plotfilename, bbox=None, himalaya_flag=None, title=None,
                 vars=None):
        """small routine to plot gridded_data for debugging purposes

        This method should not be used by a user as it is not using the gridded data object at this time

        >>> import matplotlib.pyplot as plt
        >>> from mpl_toolkits.basemap import Basemap
        >>> lats=obj.data[:,obj._LATINDEX]
        >>> lons=obj.data[:,obj._LONINDEX]
        >>> m = Basemap(projection='merc',lon_0=0)
        >>> x, y = m(lons,lats)
        >>> m.drawmapboundary(fill_color='#99ffff')
        >>> m.fillcontinents(color='#cc9966',lake_color='#99ffff')
        >>> m.scatter(x,y,3,marker='o',color='k')
        >>> plt.show()

        >>> infile='/lustre/storeB/project/fou/kl/vals5p/aerocom/Sentinel5P/renamed/aerocom.Sentinel5P.daily.sconcno2.2018.nc'
        >>> import xarray as xr
        >>> import cartopy.crs as ccrs
        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> ds=xr.open_dataset(infile)
        >>> ds['sconcno2'].data[ds['sconcno2'] < 0.]=np.nan
        >>> mean_data = ds['sconcno2'].mean(axis=0)

        >>> from matplotlib.colors import LogNorm

        >>> fig = plt.figure(figsize=(10, 6))
        >>> ax = fig.add_subplot(111, projection=ccrs.Robinson(), aspect='auto')
        >>> plot=mean_data.plot.pcolormesh(ax=ax, cmap='jet', transform=ccrs.PlateCarree(), robust=True, levels=16)
        >>> ax.coastlines()
        >>> ax.set_global()

        """

        import matplotlib.pyplot as plt
        from mpl_toolkits.basemap import Basemap
        import numpy as np

        # positions of some peaks:

        # Everest: 27.988056, 86.925278
        # K2: 35.8825, 76.513333
        # Kangchenjunga: 27.7025, 88.146667
        # Lhotse: 27.961667, 86.933333
        # Makalu: 27.889167, 87.088611
        # Cho Oyu: 28.094167, 86.660833
        # Dhaulagiri: 28.698333, 83.4875
        # Manaslu: 28.549444, 84.561944
        # Nanga Parbat: 35.2375, 74.589167
        # Annapurna Massif: 28.596111, 83.820278
        # Gasherbrum I: 35.724444, 76.696389
        # Broad Peak: 35.811667, 76.565
        # Gasherbrum II:35.758333, 76.653333
        # Shishapangma:28.352222, 85.779722
        himalaya_data = {}
        himalaya_data['Everest'] = (27.988056, 86.925278)
        himalaya_data['K2'] = (35.8825, 76.513333)
        himalaya_data['Kangchenjunga'] = (27.7025, 88.146667)
        himalaya_data['Lhotse'] = (27.961667, 86.933333)
        himalaya_data['Makalu'] = (27.889167, 87.088611)
        himalaya_data['Cho Oyu'] = (28.094167, 86.660833)
        himalaya_data['Dhaulagiri'] = (28.698333, 83.4875)
        himalaya_data['Manaslu'] = (28.549444, 84.561944)
        himalaya_data['Nanga Parbat'] = (35.2375, 74.589167)
        himalaya_data['Annapurna Massif'] = (28.596111, 83.820278)
        himalaya_data['Gasherbrum I'] = (35.724444, 76.696389)
        himalaya_data['Broad Peak'] = (35.811667, 76.565)
        himalaya_data['Gasherbrum II'] = (35.758333, 76.653333)
        himalaya_data['Shishapangma'] = (28.352222, 85.779722)
        if bbox:
            lat_low = bbox[0]
            lat_high = bbox[1]
            lon_low = bbox[2]
            lon_high = bbox[3]
        else:
            lat_low = -90.
            lat_high = 90.
            lon_low = -180.
            lon_high = 180.

        for var in vars:
            lats = gridded_data['latitude']
            lons = gridded_data['longitude']

            m = Basemap(projection='cyl', llcrnrlat=lat_low, urcrnrlat=lat_high,
                        llcrnrlon=lon_low, urcrnrlon=lon_high, resolution='c', fix_aspect=False)

            x, y = m(lons, lats)
            # m.drawmapboundary(fill_color='#99ffff')
            # m.fillcontinents(color='#cc9966', lake_color='#99ffff')
            # plot = m.scatter(x, y, 4, marker='o', color='r', )
            # plot = iplt.pcolormesh(time_sub_cube[:, :], cmap = colormap, vmin=0., vmax=max(colorbar_levels))

            my_cmap = plt.get_cmap('rainbow')
            my_cmap.set_under('white')
            cs = m.pcolormesh(x, y, gridded_data[var]['mean'], cmap=my_cmap)
            m.colorbar(cs, extend='min')

            m.drawmeridians(np.arange(-180, 220, 40), labels=[0, 0, 0, 1], fontsize=10)
            m.drawparallels(np.arange(-90, 120, 30), labels=[1, 1, 0, 0], fontsize=10)
            # axis = plt.axis([LatsToPlot.min(), LatsToPlot.max(), LonsToPlot.min(), LonsToPlot.max()])
            # ax = plot.axes
            m.drawcoastlines()
            # m.etopo()
            # m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)
            # m.arcgisimage(service='World_Shaded_Relief', xpixels = 1500, verbose= True)
            if bbox is not None:
                m.drawcountries()
                # m.drawrivers()

            if himalaya_flag:
                for peak in himalaya_data:
                    x, y = m(himalaya_data[peak][1], himalaya_data[peak][0])
                    plot = m.plot(x, y, 4, marker='.', color='b')

            if title:
                plt.title(title, fontsize='small')
            plt.savefig(plotfilename, dpi=300)
            plt.close()

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
