#!/usr/bin/env python3
################################################################
# read_aeolus_l2a_data.py
#
# read binary ESA L2B files of the ADM Aeolus mission
#
# this file is part of the pyaerocom package
#
#################################################################
# Created 20180731 by Jan Griesfeller for Met Norway
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
import numpy as np

from pyaerocom import const
import logging
import time
import geopy.distance

from pyaerocom.io.readsatellitel2base import ReadL2DataBase
# from pyaerocom.io.readungriddedbase import ReadUngriddedBase
# import geopy
# import numpy as np
import logging
from pyaerocom import const
from pyaerocom.ungriddeddata import UngriddedData

class ReadL2Data(ReadL2DataBase):
    """Interface for reading ADM AEOLUS L2A data Aerosol product for the AEOLUS PRODEX project

    IMPORTANT:
    This module requires the coda package to be installed in the local python distribution.
    The coda package can be obtained from http://stcorp.nl/coda/
    In addition, it needs a definition file (named AEOLUS-20170913.codadef at the time of
    this writing) that came with the test data from ESA and seems to be available also via the coda
    github page at https://github.com/stcorp/codadef-aeolus/releases/download/20170913/AEOLUS-20170913.codadef.

    A description of the data format can be found here: http://stcorp.nl/coda/codadef/AEOLUS/index.html

    Attributes
    ----------
    data : numpy array of dtype np.float64 initially of shape (10000,8)
        data point array

    Parameters
    ----------

    """

    _FILEMASK = '*.DBL'
    __version__ = "0.11"
    DATA_ID = const.AEOLUS_NAME
    # Flag if the dataset contains all years or not
    DATASET_IS_YEARLY = False

    SUPPORTED_DATASETS = []
    SUPPORTED_DATASETS.append(DATA_ID)

    TS_TYPE = 'undefined'

    _EC355NAME = 'ec355aer'
    _BS355NAME = 'bs355aer'
    _LODNAME = 'lod'
    _SRNAME = 'sr'
    _CASENAME = 'case'

    _QANAME = 'qa_index'
    DEFAULT_VARS = [_EC355NAME]
    PROVIDES_VARIABLES = [_EC355NAME, _BS355NAME, _LODNAME, _SRNAME, _QANAME]

    GLOBAL_ATTRIBUTES = {}
    DATASET_PATH = '/lustre/storeB/project/fou/kl/admaeolus/data.rev.TD01/download/'

    def __init__(self, dataset_to_read=None, index_pointer=0, loglevel=logging.INFO, verbose=False):
        super(ReadL2Data, self).__init__(dataset_to_read)
        self.verbose = verbose
        self.metadata = {}
        self.data = []
        self.index = len(self.metadata)
        self.files = []
        self.index_pointer = index_pointer
        # that's the flag to indicate if the location of a data point in self.data has been
        # stored in rads in self.data already
        # trades RAM for speed
        self.rads_in_array_flag = False

        self.SUPPORTED_RETRIEVALS = []
        self.SUPPORTED_RETRIEVALS.append('sca')
        self.SUPPORTED_RETRIEVALS.append('ica')
        self.SUPPORTED_RETRIEVALS.append('mca')

        self.FILE_MASK = '*AE_OPER_ALD_U_N_2A*'
        self._QANAME = 'qa_index'
        # quality index
        # unfortunately the quality index is coded bit wise:
        # QC information about processing
        # Processing_QC_Flag
        # Bit packed quality field
        # Bit 1: Extinction; data valid 1, otherwise 0
        # Bit 2: Backscatter; data valid 1, otherwise 0
        # Bit 3: Mie SNR; data valid 1, otherwise 0
        # Bit 4: Rayleigh SNR; data valid 1, otherwise 0
        # Bit 5: Extinction error bar; data valid 1, otherwise 0
        # Bit 6: Backscatter error bar; data valid 1, otherwise 0
        # Bit 7: cumulative LOD; data valid 1, otherwise 0
        # Bit 8: Spare
        # or
        # Mid_Processing_QC_Flag
        # QC information about processing
        # Bit packed quality field
        # Bit 1: Extinction; data valid 1, otherwise 0
        # Bit 2: Backscatter; data valid 1, otherwise 0
        # Bit 3: BER; data valid 1, otherwise 0
        # Bit 4: Mie SNR; data valid 1, otherwise 0
        # Bit 5: Rayleigh SNR; data valid 1, otherwise 0
        # Bit 6: Extinction error bar; data valid 1, otherwise 0
        # Bit 7: Backscatter error bar; data valid 1, otherwise 0
        # Bit 8: Cumulative LOD; data valid 1, otherwise 0
        # this is the value against the actual qa_index will be 'anded' bitwise
        # 1 means that we require only the extinction data to be valid
        self._QAINDEX_VAL = np.uint8(1)

        self._LATBOUNDSNAME = 'lat_bnds'
        self._LATBOUNDSSIZE = 4
        self._LONBOUNDSNAME = 'lon_bnds'
        self._LONBOUNDSSIZE = 4

        self._UPPERALTITUDENAME = 'lower_altitude'
        self._ALTBOUNDSNAME = 'alt_bnds'

        self._RAYLEIGHLATNAME = 'rayleigh_lat'
        self._RAYLEIGHLONNAME = 'rayleigh_lon'
        self._RAYLEIGHALTITUDENAME = 'rayleigh_altitude'

        self.COORDINATE_NAMES = [self._LATITUDENAME, self._LONGITUDENAME, self._ALTITUDENAME,
                                 self._LATBOUNDSNAME, self._LONBOUNDSNAME,
                                 self._UPPERALTITUDENAME, self._ALTBOUNDSNAME, self._TIME_NAME]

        self._QAINDEX = UngriddedData._DATAFLAGINDEX
        self._TIME_OFFSET_INDEX = UngriddedData._TRASHINDEX
        self._LATBOUNDINDEX = 13
        self._LONBOUNDINDEX = self._LATBOUNDINDEX + self._LATBOUNDSSIZE + 1

        self._RADLATINDEX = self._LONBOUNDINDEX + 1
        self._RADLONINDEX = self._RADLATINDEX + 1
        self._DISTINDEX = self._RADLATINDEX + 2
        self._LODINDEX =  self._RADLATINDEX + 3
        self._SRINDEX = self._RADLATINDEX + 4
        self._RAYLEIGHLATINDEX = self._SRINDEX + 1
        self._RAYLEIGHLONINDEX = self._RAYLEIGHLATINDEX + 1
        self._RAYLEIGHALTITUDEINDEX = self._RAYLEIGHLONINDEX + 1

        self._UPPERALTITUDEINDEX = self._RAYLEIGHALTITUDEINDEX + 1
        self._COLNO = self._UPPERALTITUDEINDEX + 1

        self._CHUNKSIZE = 100000
        self._HEIGHTSTEPNO = 24

        # variable names for the different retrievals
        self.CODA_READ_PARAMETERS = {}
        self.CODA_READ_PARAMETERS['sca'] = {}
        self.CODA_READ_PARAMETERS['sca']['metadata'] = {}
        self.CODA_READ_PARAMETERS['sca']['vars'] = {}

        # self.RETRIEVAL_READ_PARAMETERS['sca']['metadata'][self._TIME_NAME] = 'sca_optical_properties/starttime'
        self.CODA_READ_PARAMETERS['sca']['metadata'][self._TIME_NAME] = 'sca_pcd/starttime'
        # self.RETRIEVAL_READ_PARAMETERS['sca']['metadata']['test_sca_pcd_starttime'] = 'sca_pcd/starttime'
        # test data to be read
        # self.CODA_READ_PARAMETERS['sca']['metadata']['test_sca_pcd_mid_bins_qc_flag'] = \
        #     'sca_pcd/profile_pcd_mid_bins/processing_qc_flag'
        self.CODA_READ_PARAMETERS['sca']['metadata'][self._RAYLEIGHALTITUDENAME] = \
            'geolocation/measurement_geolocation/rayleigh_geolocation_height_bin/altitude_of_height_bin'
        self.CODA_READ_PARAMETERS['sca']['metadata'][self._RAYLEIGHLATNAME] = \
            'geolocation/measurement_geolocation/rayleigh_geolocation_height_bin/latitude_of_height_bin'
        self.CODA_READ_PARAMETERS['sca']['metadata'][self._RAYLEIGHLONNAME] = \
            'geolocation/measurement_geolocation/rayleigh_geolocation_height_bin/longitude_of_height_bin'

        # /geolocation[?]/measurement_geolocation[?]/rayleigh_geolocation_height_bin[25]/longitude_of_height_bin
        # /geolocation[?]/measurement_geolocation[?]/rayleigh_geolocation_height_bin[25]/latitude_of_height_bin
        # /geolocation[?]/measurement_geolocation[?]/rayleigh_geolocation_height_bin[25]/altitude_of_height_bin

        # self.RETRIEVAL_READ_PARAMETERS['sca']['metadata'][self._QANAME] = 'sca_pcd/qc_flag'
        self.CODA_READ_PARAMETERS['sca']['metadata'][self._QANAME] = 'sca_pcd/profile_pcd_bins/processing_qc_flag'
        self.CODA_READ_PARAMETERS['sca']['metadata'][
            self._LATITUDENAME] = 'sca_optical_properties/geolocation_middle_bins/latitude'
        self.CODA_READ_PARAMETERS['sca']['metadata'][
            self._LONGITUDENAME] = 'sca_optical_properties/geolocation_middle_bins/longitude'
        self.CODA_READ_PARAMETERS['sca']['metadata'][
            self._ALTITUDENAME] = 'sca_optical_properties/geolocation_middle_bins/altitude'
        self.CODA_READ_PARAMETERS['sca']['vars'][
            self._EC355NAME] = 'sca_optical_properties/sca_optical_properties_mid_bins/extinction'
        # self.CODA_READ_PARAMETERS['sca']['vars'][
        #     self._EC355NAME] = 'sca_optical_properties/sca_optical_properties/extinction'
        self.CODA_READ_PARAMETERS['sca']['vars'][
            self._BS355NAME] = 'sca_optical_properties/sca_optical_properties_mid_bins/backscatter'
        # self.CODA_READ_PARAMETERS['sca']['vars'][
        #     self._BS355NAME] = 'sca_optical_properties/sca_optical_properties/backscatter'
        self.CODA_READ_PARAMETERS['sca']['vars'][self._LODNAME] = 'sca_optical_properties/sca_optical_properties/lod'
        self.CODA_READ_PARAMETERS['sca']['vars'][self._SRNAME] = 'sca_optical_properties/sca_optical_properties/sr'

        self.CODA_READ_PARAMETERS['ica'] = {}
        self.CODA_READ_PARAMETERS['ica']['metadata'] = {}
        self.CODA_READ_PARAMETERS['ica']['vars'] = {}
        self.CODA_READ_PARAMETERS['ica']['metadata'][self._TIME_NAME] = 'ica_optical_properties/starttime'

        self.CODA_READ_PARAMETERS['ica']['metadata'][
            self._LATITUDENAME] = 'sca_optical_properties/geolocation_middle_bins/latitude'
        self.CODA_READ_PARAMETERS['ica']['metadata'][
            self._LONGITUDENAME] = 'sca_optical_properties/geolocation_middle_bins/longitude'
        self.CODA_READ_PARAMETERS['ica']['metadata'][
            self._ALTITUDENAME] = 'sca_optical_properties/geolocation_middle_bins/altitude'
        self.CODA_READ_PARAMETERS['ica']['vars'][
            self._EC355NAME] = 'ica_optical_properties/ica_optical_properties/extinction'
        self.CODA_READ_PARAMETERS['ica']['vars'][
            self._BS355NAME] = 'ica_optical_properties/ica_optical_properties/backscatter'
        self.CODA_READ_PARAMETERS['ica']['vars'][self._LODNAME] = 'ica_optical_properties/ica_optical_properties/lod'
        # self.RETRIEVAL_READ_PARAMETERS['ica']['vars'][_CASENAME] = 'ica_optical_properties/ica_optical_properties/case'

        self.CODA_READ_PARAMETERS['mca'] = {}
        self.CODA_READ_PARAMETERS['mca']['metadata'] = {}
        self.CODA_READ_PARAMETERS['mca']['vars'] = {}
        self.CODA_READ_PARAMETERS['mca']['metadata'][self._TIME_NAME] = 'mca_optical_properties/starttime'
        self.CODA_READ_PARAMETERS['mca']['metadata'][
            self._LATITUDENAME] = 'sca_optical_properties/geolocation_middle_bins/latitude'
        self.CODA_READ_PARAMETERS['mca']['metadata'][
            self._LONGITUDENAME] = 'sca_optical_properties/geolocation_middle_bins/longitude'
        self.CODA_READ_PARAMETERS['mca']['metadata'][
            self._ALTITUDENAME] = 'sca_optical_properties/geolocation_middle_bins/altitude'
        self.CODA_READ_PARAMETERS['mca']['vars'][
            self._EC355NAME] = 'mca_optical_properties/mca_optical_properties/extinction'
        self.CODA_READ_PARAMETERS['mca']['vars'][self._LODNAME] = 'mca_optical_properties/mca_optical_properties/lod'
        # DATA_COLNAMES[_MCA_CASENAME] = 'mca_optical_properties/mca_optical_properties/case'

        GROUP_DELIMITER = '/'

        # create a dict with the aerocom variable name as key and the index number in the
        # resulting numpy array as value.

        self.INDEX_DICT.update({self._LATITUDENAME: self._LATINDEX})
        self.INDEX_DICT.update({self._LONGITUDENAME: self._LONINDEX})
        self.INDEX_DICT.update({self._ALTITUDENAME: self._ALTITUDEINDEX})
        self.INDEX_DICT.update({self._UPPERALTITUDENAME: self._UPPERALTITUDEINDEX})
        self.INDEX_DICT.update({self._TIME_NAME: self._TIMEINDEX})
        self.INDEX_DICT.update({self._EC355NAME: self._DATAINDEX01})
        self.INDEX_DICT.update({self._BS355NAME: self._DATAINDEX01})
        self.INDEX_DICT.update({self._QANAME: self._QAINDEX})
        self.INDEX_DICT.update({self._LODNAME: self._LODINDEX})
        self.INDEX_DICT.update({self._SRNAME: self._SRINDEX})
        self.INDEX_DICT.update({self._LATBOUNDSNAME: self._LATBOUNDINDEX})
        self.INDEX_DICT.update({self._LONBOUNDSNAME: self._LONBOUNDINDEX})
        self.INDEX_DICT.update({self._RAYLEIGHLATNAME: self._RAYLEIGHLATINDEX})
        self.INDEX_DICT.update({self._RAYLEIGHLONNAME: self._RAYLEIGHLONINDEX})
        self.INDEX_DICT.update({self._RAYLEIGHALTITUDENAME: self._RAYLEIGHALTITUDEINDEX})

        # dictionary to store array sizes of an element in self.data
        # SIZE_DICT = {}
        self.SIZE_DICT.update({self._LATBOUNDSNAME: self._LATBOUNDSSIZE})
        self.SIZE_DICT.update({self._LONBOUNDSNAME: self._LONBOUNDSSIZE})

        # NaN values are variable specific
        # NAN_DICT = {}
        self.NAN_DICT.update({self._LATITUDENAME: -1.E-6})
        self.NAN_DICT.update({self._LONGITUDENAME: -1.E-6})
        self.NAN_DICT.update({self._ALTITUDENAME: -1.})
        self.NAN_DICT.update({self._UPPERALTITUDENAME: -1.})
        self.NAN_DICT.update({self._RAYLEIGHLATNAME: -1.E-6})
        self.NAN_DICT.update({self._RAYLEIGHLONNAME: -1.E-6})
        self.NAN_DICT.update({self._RAYLEIGHALTITUDENAME: -1.})
        self.NAN_DICT.update({self._EC355NAME: -1.E6})
        self.NAN_DICT.update({self._BS355NAME: -1.E6})
        self.NAN_DICT.update({self._LODNAME: -1.})
        self.NAN_DICT.update({self._SRNAME: -1.})
        self.NAN_DICT.update({self._QANAME: -1.})

        self.PROVIDES_VARIABLES = list(self.CODA_READ_PARAMETERS['sca']['metadata'].keys())
        self.PROVIDES_VARIABLES.extend(self.CODA_READ_PARAMETERS['sca']['vars'].keys())

        # these are the variable specific attributes written into a netcdf file
        self.NETCDF_VAR_ATTRIBUTES[self._BS355NAME] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._BS355NAME]['_FillValue'] = np.nan
        self.NETCDF_VAR_ATTRIBUTES[self._BS355NAME]['long_name'] = 'backscatter @ 355nm'
        # self.NETCDF_VAR_ATTRIBUTES[self._BS355NAME]['standard_name'] = 'volume_extinction_coefficient_in_air_due_to_ambient_aerosol_particles'
        self.NETCDF_VAR_ATTRIBUTES[self._BS355NAME]['units'] = '1'
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME]['_FillValue'] = np.nan
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME]['long_name'] = 'extinction @ 355nm'
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME][
            'standard_name'] = 'volume_extinction_coefficient_in_air_due_to_ambient_aerosol_particles'
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME]['units'] = '1/Mm'

        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME+'_mean'] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME+'_mean']['_FillValue'] = np.nan
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME+'_mean']['long_name'] = 'extinction @ 355nm'
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME+'_mean'][
            'standard_name'] = 'volume_extinction_coefficient_in_air_due_to_ambient_aerosol_particles'
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME+'_mean']['units'] = '1/Mm'

        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME+'_numobs'] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME+'_numobs']['_FillValue'] = np.nan
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME+'_numobs']['long_name'] = 'number of observations of extinction @ 355nm'
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME+'_numobs']['units'] = '1'

        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME+'_stddev'] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME+'_stddev']['_FillValue'] = np.nan
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME+'_stddev']['long_name'] = 'standard deviation of extinction @ 355nm'
        self.NETCDF_VAR_ATTRIBUTES[self._EC355NAME+'_stddev']['units'] = '1/Mm'

        self.NETCDF_VAR_ATTRIBUTES[self._QANAME] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._QANAME]['long_name'] = 'aeolus quality flag'
        self.NETCDF_VAR_ATTRIBUTES[self._QANAME]['units'] = '1'

        self.NETCDF_VAR_ATTRIBUTES[self._UPPERALTITUDENAME] = {}
        self.NETCDF_VAR_ATTRIBUTES[self._UPPERALTITUDENAME]['long_name'] = 'lower altitude'
        self.NETCDF_VAR_ATTRIBUTES[self._UPPERALTITUDENAME]['standard_name'] = 'altitude'
        self.NETCDF_VAR_ATTRIBUTES[self._UPPERALTITUDENAME]['units'] = 'm'

        self.TEX_UNITS = {}
        self.TEX_UNITS[self._EC355NAME] = r'$10^{-6} \cdot m^{-1}$'
        self.TEX_UNITS[self._BS355NAME] = ''

        self.SUPPORTED_SUFFIXES.append('.DBL')
        self.RETRIEVAL_READ = ''

        # number of points found in the files read
        self._point_no_found = 0
        # number of points that passed the quality flag
        self._point_no_with_good_quality = 0

        # minimal number of observations needed for gridding
        self.MIN_VAL_NO_FOR_GRIDDING = 1

        #association of EMEP variable names with aeolus variable names
        self.EMEP_VAR_NAME_DICT = {}
        self.EMEP_VAR_NAME_DICT[self._TIME_NAME] = 'time'
        self.EMEP_VAR_NAME_DICT[self._LONGITUDENAME] = 'lon'
        self.EMEP_VAR_NAME_DICT[self._LATITUDENAME] = 'lat'
        self.EMEP_VAR_NAME_DICT[self._ALTITUDENAME] = 'Z_MID'
        self.EMEP_VAR_NAME_DICT[self._EC355NAME] = 'EXT_350nm'

        # self.EMEP_VAR_NAME_DICT[self._TIME_NAME] = 'EXT_350nm'

        # needed EMEP data variable names for gridding
        self.EMEP_VARS_TO_COPY_FOR_GRIDDING = [self.EMEP_VAR_NAME_DICT[self._LONGITUDENAME],
                                               self.EMEP_VAR_NAME_DICT[self._LATITUDENAME],
                                               self.EMEP_VAR_NAME_DICT[self._ALTITUDENAME],
                                               self.EMEP_VAR_NAME_DICT[self._TIME_NAME],
                                               ]
        # variable name of the topography in the topography file
        self.EMEP_TOPO_FILE_VAR_NAME = 'topography'

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
            # self.logger.debug('init')

    ###################################################################################
    # def ndarr2data(self, file_data):
    #     """small helper routine to put the data read by the read_file method into
    #     the ndarray of self.data"""
    #
    #     # start_read = time.perf_counter()
    #     # return all data points
    #     num_points = len(file_data)
    #     if self.index_pointer == 0:
    #         self.data = file_data
    #         self._ROWNO = num_points
    #         self.index_pointer = num_points
    #
    #     else:
    #         # append to self.data
    #         # add another array chunk to self.data
    #         self.data = np.append(self.data, np.zeros([num_points, self._COLNO], dtype=np.float_),
    #                               axis=0)
    #         self._ROWNO = num_points
    #         # copy the data
    #         self.data[self.index_pointer:, :] = file_data
    #         self.index_pointer = self.index_pointer + num_points
    #
    #         # end_time = time.perf_counter()
    #         # elapsed_sec = end_time - start_read
    #         # temp = 'time for single file read seconds: {:.3f}'.format(elapsed_sec)
    #         # self.logger.warning(temp)
    #
    # ###################################################################################

    def read_file(self, filename, vars_to_retrieve=None, read_retrieval='sca', return_as='dict', loglevel=None,
                  quality_flag=0.0):
        """method to read the file partially

        :param filename:
        :param vars_to_retrieve:
        :param read_retrieval:
        :param return_as:
        :param loglevel:
        :param quality_flag:
        :return:

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : list
            list of str with variable names to read; defaults to ['od355aer']
        verbose : Bool
            set to True to increase verbosity

        Returns
        --------
        Either:
            dictionary (default):
                keys are 'time', 'latitude', 'longitude', 'altitude' and the variable names
                'ec355aer', 'bs355aer', 'sr', 'lod' if the whole file is read
                'time' is a 1d array, while the other dict values are a another dict with the
                time as keys (the same ret['time']) and a numpy array as values. These values represent the profile.
                Note 1: latitude and longitude are height dependent due to the tilt of the measurement.
                Note 2: negative values indicate a NaN

            2d ndarray of type float:
                representing a 'point cloud' with all points
                    column 1: time in seconds since the Unix epoch with ms accuracy (same time for every height
                    in a profile)
                    column 2: latitude
                    column 3: longitude
                    column 4: altitude
                    column 5: extinction
                    column 6: backscatter
                    column 7: sr
                    column 8: lod

                    Note: negative values are put to np.nan already

                    The indexes are noted in read_aeolus_l2a_data.ReadAeolusL2aData.<index_name>
                    e.g. the time index is named read_aeolus_l2a_data.ReadAeolusL2aData._TIMEINDEX
                    have a look at the example to access the values

        This is whats in one DBL file
        codadump list /lustre/storeB/project/fou/kl/admaeolus/data.rev.2A02/AE_OPER_ALD_U_N_2A_20181201T033526026_005423993_001590_0001.DBL

        /mph/product
        /mph/proc_stage
        /mph/ref_doc
        /mph/acquisition_station
        /mph/proc_center
        /mph/proc_time
        /mph/software_ver
        /mph/baseline
        /mph/sensing_start
        /mph/sensing_stop
        /mph/phase
        /mph/cycle
        /mph/rel_orbit
        /mph/abs_orbit
        /mph/state_vector_time
        /mph/delta_ut1
        /mph/x_position
        /mph/y_position
        /mph/z_position
        /mph/x_velocity
        /mph/y_velocity
        /mph/z_velocity
        /mph/vector_source
        /mph/utc_sbt_time
        /mph/sat_binary_time
        /mph/clock_step
        /mph/leap_utc
        /mph/leap_sign
        /mph/leap_err
        /mph/product_err
        /mph/tot_size
        /mph/sph_size
        /mph/num_dsd
        /mph/dsd_size
        /mph/num_data_sets
        /sph/sph_descriptor
        /sph/intersect_start_lat
        /sph/intersect_start_long
        /sph/intersect_stop_lat
        /sph/intersect_stop_long
        /sph/sat_track
        /sph/num_brc
        /sph/num_meas_max_brc
        /sph/num_bins_per_meas
        /sph/num_prof_sca
        /sph/num_prof_ica
        /sph/num_prof_mca
        /sph/num_group_tot
        /dsd[?]/ds_name
        /dsd[?]/ds_type
        /dsd[?]/filename
        /dsd[?]/ds_offset
        /dsd[?]/ds_size
        /dsd[?]/num_dsr
        /dsd[?]/dsr_size
        /dsd[?]/byte_order
        /geolocation[?]/start_of_obs_time
        /geolocation[?]/num_meas_eff
        /geolocation[?]/measurement_geolocation[?]/centroid_time
        /geolocation[?]/measurement_geolocation[?]/mie_geolocation_height_bin[25]/longitude_of_height_bin
        /geolocation[?]/measurement_geolocation[?]/mie_geolocation_height_bin[25]/latitude_of_height_bin
        /geolocation[?]/measurement_geolocation[?]/mie_geolocation_height_bin[25]/altitude_of_height_bin
        /geolocation[?]/measurement_geolocation[?]/rayleigh_geolocation_height_bin[25]/longitude_of_height_bin
        /geolocation[?]/measurement_geolocation[?]/rayleigh_geolocation_height_bin[25]/latitude_of_height_bin
        /geolocation[?]/measurement_geolocation[?]/rayleigh_geolocation_height_bin[25]/altitude_of_height_bin
        /geolocation[?]/measurement_geolocation[?]/longitude_of_dem_intersection
        /geolocation[?]/measurement_geolocation[?]/latitude_of_dem_intersection
        /geolocation[?]/measurement_geolocation[?]/altitude_of_dem_intersection
        /geolocation[?]/geoid_separation
        /meas_pcd[?]/start_of_obs_time
        /meas_pcd[?]/l1b_input_screening/l1b_obs_screening
        /meas_pcd[?]/l1b_input_screening/l1b_obs_screening_flags[40]
        /meas_pcd[?]/l1b_input_screening/l1b_mie_meas_screening[?]/l1b_mie_meas_qc
        /meas_pcd[?]/l1b_input_screening/l1b_mie_meas_screening[?]/l1b_mie_meas_qc_flags[8]
        /meas_pcd[?]/l1b_input_screening/l1b_rayleigh_meas_screening[?]/l1b_rayleigh_meas_qc
        /meas_pcd[?]/l1b_input_screening/l1b_rayleigh_meas_screening[?]/l1b_rayleigh_meas_qc_flags[8]
        /meas_pcd[?]/l1b_cal_screening/cal_valid
        /meas_pcd[?]/l2a_processing_qc/sca_applied
        /meas_pcd[?]/l2a_processing_qc/ica_applied
        /meas_pcd[?]/l2a_processing_qc/mca_applied
        /meas_pcd[?]/l2a_processing_qc/feature_finder_indicators/layer_information[24]/bin_loaded
        /meas_pcd[?]/l2a_processing_qc/feature_finder_indicators/layer_information[24]/seed[30]
        /meas_pcd[?]/l2a_processing_qc/feature_finder_indicators/lowest_computable_bin[30]
        /sca_pcd[?]/starttime
        /sca_pcd[?]/firstmatchingbin
        /sca_pcd[?]/qc_flag
        /sca_pcd[?]/profile_pcd_bins[24]/extinction_variance
        /sca_pcd[?]/profile_pcd_bins[24]/backscatter_variance
        /sca_pcd[?]/profile_pcd_bins[24]/lod_variance
        /sca_pcd[?]/profile_pcd_bins[24]/processing_qc_flag
        /sca_pcd[?]/profile_pcd_mid_bins[23]/extinction_variance
        /sca_pcd[?]/profile_pcd_mid_bins[23]/backscatter_variance
        /sca_pcd[?]/profile_pcd_mid_bins[23]/lod_variance
        /sca_pcd[?]/profile_pcd_mid_bins[23]/ber_variance
        /sca_pcd[?]/profile_pcd_mid_bins[23]/processing_qc_flag
        /ica_pcd[?]/starttime
        /ica_pcd[?]/first_matching_bin
        /ica_pcd[?]/qc_flag
        /ica_pcd[?]/ica_processing_qc_flag_bin[24]
        /mca_pcd[?]/starttime
        /mca_pcd[?]/processing_qc_flag_bin[24]
        /amd_pcd[?]/starttime
        /amd_pcd[?]/l2b_amd_screening_qc
        /amd_pcd[?]/l2b_amd_screening_qc_flags
        /amd_pcd[?]/l2b_amd_collocations[?]/l2b_amd_collocation_qc
        /amd_pcd[?]/l2b_amd_collocations[?]/l2b_amd_collocation_qc_flags
        /group_pcd[?]/starttime
        /group_pcd[?]/brc_start
        /group_pcd[?]/measurement_start
        /group_pcd[?]/brc_end
        /group_pcd[?]/measurement_end
        /group_pcd[?]/height_bin_index
        /group_pcd[?]/upper_problem_flag
        /group_pcd[?]/particle_extinction_variance
        /group_pcd[?]/particle_backscatter_variance
        /group_pcd[?]/particle_lod_variance
        /group_pcd[?]/qc_flag
        /group_pcd[?]/mid_particle_extinction_variance_top
        /group_pcd[?]/mid_particle_backscatter_variance_top
        /group_pcd[?]/mid_particle_lod_variance_top
        /group_pcd[?]/mid_particle_ber_variance_top
        /group_pcd[?]/mid_particle_extinction_variance_bot
        /group_pcd[?]/mid_particle_backscatter_variance_bot
        /group_pcd[?]/mid_particle_lod_variance_bot
        /group_pcd[?]/mid_particle_ber_variance_bot
        /sca_optical_properties[?]/starttime
        /sca_optical_properties[?]/sca_optical_properties[24]/extinction
        /sca_optical_properties[?]/sca_optical_properties[24]/backscatter
        /sca_optical_properties[?]/sca_optical_properties[24]/lod
        /sca_optical_properties[?]/sca_optical_properties[24]/sr
        /sca_optical_properties[?]/geolocation_middle_bins[24]/longitude
        /sca_optical_properties[?]/geolocation_middle_bins[24]/latitude
        /sca_optical_properties[?]/geolocation_middle_bins[24]/altitude
        /sca_optical_properties[?]/sca_optical_properties_mid_bins[23]/extinction
        /sca_optical_properties[?]/sca_optical_properties_mid_bins[23]/backscatter
        /sca_optical_properties[?]/sca_optical_properties_mid_bins[23]/lod
        /sca_optical_properties[?]/sca_optical_properties_mid_bins[23]/ber
        /ica_optical_properties[?]/starttime
        /ica_optical_properties[?]/ica_optical_properties[24]/case
        /ica_optical_properties[?]/ica_optical_properties[24]/extinction
        /ica_optical_properties[?]/ica_optical_properties[24]/backscatter
        /ica_optical_properties[?]/ica_optical_properties[24]/lod
        /mca_optical_properties[?]/starttime
        /mca_optical_properties[?]/mca_optical_properties[24]/climber
        /mca_optical_properties[?]/mca_optical_properties[24]/extinction
        /mca_optical_properties[?]/mca_optical_properties[24]/lod
        /amd[?]/starttime
        /amd[?]/amd_properties[24]/pressure_fp
        /amd[?]/amd_properties[24]/temperature_fp
        /amd[?]/amd_properties[24]/frequencyshift_fp
        /amd[?]/amd_properties[24]/relativehumidity_fp
        /amd[?]/amd_properties[24]/molecularlod_fp
        /amd[?]/amd_properties[24]/molecularbackscatter_fp
        /amd[?]/amd_properties[24]/pressure_fiz
        /amd[?]/amd_properties[24]/temperature_fiz
        /amd[?]/amd_properties[24]/frequencyshift_fiz
        /amd[?]/amd_properties[24]/relativehumidity_fiz
        /amd[?]/amd_properties[24]/molecularlod_fiz
        /amd[?]/amd_properties[24]/molecularbackscatter_fiz
        /group_optical_properties[?]/starttime
        /group_optical_properties[?]/height_bin_index
        /group_optical_properties[?]/group_optical_property/group_extinction
        /group_optical_properties[?]/group_optical_property/group_backscatter
        /group_optical_properties[?]/group_optical_property/group_lod
        /group_optical_properties[?]/group_optical_property/group_sr
        /group_optical_properties[?]/group_geolocation_middle_bins/start_longitude
        /group_optical_properties[?]/group_geolocation_middle_bins/start_latitude
        /group_optical_properties[?]/group_geolocation_middle_bins/start_altitude
        /group_optical_properties[?]/group_geolocation_middle_bins/mid_longitude
        /group_optical_properties[?]/group_geolocation_middle_bins/mid_latitude
        /group_optical_properties[?]/group_geolocation_middle_bins/mid_altitude
        /group_optical_properties[?]/group_geolocation_middle_bins/stop_longitude
        /group_optical_properties[?]/group_geolocation_middle_bins/stop_latitude
        /group_optical_properties[?]/group_geolocation_middle_bins/stop_altitude
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_extinction_top
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_backscatter_top
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_lod_top
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_ber_top
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_extinction_bot
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_backscatter_bot
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_lod_bot
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_ber_bot
        /scene_classification[?]/starttime
        /scene_classification[?]/height_bin_index
        /scene_classification[?]/aladin_cloud_flag/clrh
        /scene_classification[?]/aladin_cloud_flag/clsr
        /scene_classification[?]/aladin_cloud_flag/downclber
        /scene_classification[?]/aladin_cloud_flag/topclber
        /scene_classification[?]/nwp_cloud_flag
        /scene_classification[?]/l2a_group_class_reliability

        The question mark indicates a variable size array

        It is not entirely clear what we actually have to look at.
        For simplicity the data of the group 'sca_optical_properties' is returned at this point

        Example
        -------
        >>> import pyaerocom as pya
        >>> obj = pya.io.read_aeolus_l2a_data.ReadL2Data(verbose=True)
        >>> import numpy as np
        # >>> filename = '/lustre/storeB/project/fou/kl/admaeolus/data.rev.TD01/download/AE_TD01_ALD_U_N_2A_20190526T124829029_005400003_004387_0001/AE_TD01_ALD_U_N_2A_20190526T124829029_005400003_004387_0001.DBL'
        >>> filename = '/lustre/storeB/project/fou/kl/admaeolus/data.rev.TD01/download/AE_TD01_ALD_U_N_2A_20190719T152159021_005472012_005245_0001/AE_TD01_ALD_U_N_2A_20190719T152159021_005472012_005245_0001.DBL'
        >>> # read returning a ndarray
        >>> filedata_numpy = obj.read_file(filename, vars_to_retrieve=['ec355aer'], return_as='numpy')
        >>> test=((data_numpy[:,obj._QAINDEX].astype(np.int)))
        >>> time_as_numpy_datetime64 = data_numpy[0,obj._TIMEINDEX].astype('datetime64[s]')

        >>> print('time: {}'.format(time_as_numpy_datetime64))
        >>> print('latitude: {}'.format(data_numpy[1,obj._LATINDEX]))
        >>> # read returning a dictionary
        >>> filedata = obj.read_file(filename, vars_to_retrieve=['ec355aer'])
        >>> print('time: {}'.format(filedata['time'][0].astype('datetime64[s]')))
        >>> print('all latitudes of 1st time step: {}'.format(filedata['latitude'][filedata['time'][0]]))

        """

        import time
        import coda

        # coda for Aeolus uses 2000-01-01T00:00:00 as epoch unfortunately.
        # so calculate the difference in seconds to the Unix epoch
        seconds_to_add = np.datetime64('2000-01-01T00:00:00') - np.datetime64('1970-01-01T00:00:00')
        seconds_to_add = seconds_to_add.astype(np.float_)

        # the same can be achieved using pandas, but we stick to numpy here
        # base_time = pd.DatetimeIndex(['2000-01-01'])
        # seconds_to_add = (base_time.view('int64') // pd.Timedelta(1, unit='s'))[0]

        start = time.perf_counter()
        file_data = {}

        self.logger.info('reading file {}'.format(filename))
        # read file
        product = coda.open(filename)
        if isinstance(read_retrieval, str):
            read_retrieval = [read_retrieval]
        for retrieval in self.SUPPORTED_RETRIEVALS:
            if retrieval not in read_retrieval:
                continue

            vars_to_read_in = None
            vars_to_read_in = vars_to_retrieve.copy()
            if vars_to_retrieve is None:
                # read all variables
                vars_to_read_in = list(self.CODA_READ_PARAMETERS[retrieval]['vars'].keys())
            vars_to_read_in.extend(list(self.CODA_READ_PARAMETERS[retrieval]['metadata'].keys()))
            vars_to_read_in.append(self._UPPERALTITUDENAME)
            #get rid of duplicates
            vars_to_read_in = list(set(vars_to_read_in))

            # read data time
            # do that differently since its only store once per profile
            coda_groups_to_read = (
                self.CODA_READ_PARAMETERS[retrieval]['metadata'][self._TIME_NAME].split(self.GROUP_DELIMITER))

            file_data[self._TIME_NAME] = coda.fetch(product,
                                                coda_groups_to_read[0],
                                                -1,
                                                coda_groups_to_read[1])
            # epoch is 1 January 2000 at ESA
            # so add offset to move that to 1 January 1970
            # and save it into a np.datetime64[ms] object

            file_data[self._TIME_NAME] = \
                ((file_data[self._TIME_NAME] + seconds_to_add) * 1.E3).astype(np.int).astype('datetime64[ms]')

            # list to store times to skip
            # used in conjunction with the qa_level filtering; completely unvalid profiles will be skipped
            times_to_skip = []
            # read data in a simple dictionary
            for var in vars_to_read_in:
                # time has been read already
                if var in [self._TIME_NAME, 'test_sca_pcd_starttime', self._UPPERALTITUDENAME]:
                    continue

                self.logger.info('reading var: {}'.format(var))
                try:
                    groups = self.CODA_READ_PARAMETERS[retrieval]['vars'][var].split(self.GROUP_DELIMITER)
                except KeyError:
                    groups = self.CODA_READ_PARAMETERS[retrieval]['metadata'][var].split(self.GROUP_DELIMITER)

                file_data[var] = {}
                group_depth = len(groups)

                print("group length {}:".format(group_depth))
                if group_depth == 3:
                    for idx, key in enumerate(file_data[self._TIME_NAME]):
                        file_data[var][key] = coda.fetch(product,
                                                     groups[0],
                                                     idx,
                                                      groups[1],
                                                     -1,
                                                     groups[2])

                elif group_depth == 4:
                    for idx, key in enumerate(file_data[self._TIME_NAME]):
                        file_data[var][key] = coda.fetch(product,
                                                     groups[0],
                                                     idx,
                                                      groups[1],
                                                         0,
                                                      groups[2],
                                                     -1,
                                                     groups[3])

                elif group_depth == 2:
                    for idx, key in enumerate(file_data[self._TIME_NAME]):
                        file_data[var][key] = coda.fetch(product,
                                                         groups[0],
                                                         -1,
                                                         groups[1])
                elif group_depth == 1:
                    for idx, key in enumerate(file_data[self._TIME_NAME]):
                        file_data[var][key] = coda.fetch(product,
                                                         groups[0])

                else:
                    pass

                if var == self._QANAME:
                    file_data[var+'_anded'] = {}
                    for idx, key in enumerate(file_data[self._TIME_NAME]):
                        file_data[var][key] = np.uint8(file_data[var][key])
                        file_data[var+'_anded'][key] = np.bitwise_and(file_data[var][key], self._QAINDEX_VAL)
                        # if there's no valid extinction in the profile, add the profile's time
                        # to the ones that are skipped during the conversion to a numpy array
                        if np.sum(file_data[var+'_anded'][key]) == 0:
                            # print(file_data[var][key])
                            times_to_skip.append(key)

            # add upper_altitude to data...
            var = self._UPPERALTITUDENAME
            file_data[var] = {}
            for idx, key in enumerate(file_data[self._TIME_NAME]):
                file_data[var][key] = file_data[self._ALTITUDENAME][key][1:]

            coda.close(product)

            if return_as == 'numpy':
                # return as one multidimensional numpy array that can be put into self.data directly
                # (column wise because the column numbers do not match)
                index_pointer = 0
                data = np.empty([self._ROWNO, self._COLNO], dtype=np.float_)

                for idx, _time in enumerate(file_data['time'].astype(np.float_)):
                    # skip times of profiles without a single valid extinction
                    # the following is deprecated in current nympy
                    # if _time in times_to_skip:
                    if np.sum(np.isin(times_to_skip,file_data['time'][idx])) > 0:
                        self.logger.info('skipped time {} due to no valid measurement'.format(_time.astype('datetime64[ms]')))
                        self._point_no_found += len(file_data[self._QANAME][file_data[self._TIME_NAME][idx]])
                        continue
                    else:
                        pass
                    # file_data['time'].astype(np.float_) is milliseconds after the (Unix) epoch
                    # but we want to save the time as seconds since the epoch
                    _time = _time / 1000.
                    for _index in range(len(file_data[self._QANAME][file_data[self._TIME_NAME][idx]])):
                        # this works because all variables have to have the same size
                        # (aka same number of height levels)

                        #check the quality flags
                        if file_data[self._QANAME+'_anded'][file_data[self._TIME_NAME][idx]][_index] == 0:
                            #set value to NaN
                            continue

                        # This loop could be avoided using numpy index slicing
                        # do that in case we need more optimisations
                        # maybe only when the general logic has been working

                        data[index_pointer, self._TIMEINDEX] = _time
                        data_nan_flag = False
                        for var in vars_to_read_in:
                            # time is the index, so skip it here
                            if var == self._TIME_NAME or \
                                var == 'test_sca_pcd_mid_bins_qc_flag':
                                continue
                                # var == self._QANAME or \
                            # longitudes are 0 based for Aeolus, but -180 based for model data
                            # adjust Aeolus to model data
                            if var == self._LONGITUDENAME:
                                data[index_pointer, self.INDEX_DICT[var]] = \
                                    file_data[var][file_data[self._TIME_NAME][idx]][_index]
                                if file_data[var][file_data[self._TIME_NAME][idx]][_index] > 180.:
                                    data[index_pointer, self.INDEX_DICT[var]] = \
                                        file_data[var][file_data[self._TIME_NAME][idx]][_index] - 360.
                            else:
                                try:
                                    data[index_pointer, self.INDEX_DICT[var]] = \
                                        file_data[var][file_data['time'][idx]][_index]
                                except KeyError:
                                    # the data has not been forseen to be used
                                    continue
                                    # pass

                            # put negative values to np.nan if the variable is not a metadata variable
                            if data[index_pointer, self.INDEX_DICT[var]] == self.NAN_DICT[var]:
                                data[index_pointer, self.INDEX_DICT[var]] = np.nan
                                data_nan_flag = True

                        if not data_nan_flag:
                            index_pointer += 1
                            data_nan_flag = False

                        if index_pointer >= self._ROWNO:
                            # add another array chunk to self.data
                            chunk = np.empty([self._CHUNKSIZE, self._COLNO],
                                             dtype=np.float_)
                            data = np.append(data, chunk, axis=0)

                # return only the needed elements...
                if np.isnan(data[index_pointer, self.INDEX_DICT[var]]):
                    index_pointer -= 1
                file_data = data[0:index_pointer]

        self._point_no_with_good_quality += index_pointer
        end_time = time.perf_counter()
        elapsed_sec = end_time - start
        temp = 'time for single file read [s]: {:.3f}'.format(elapsed_sec)
        self.logger.info(temp)
        self.logger.info('{} points read; {} were valid'.format(self._point_no_found,self._point_no_with_good_quality))
        self.RETRIEVAL_READ = read_retrieval
        self.files_read.append(filename)
        return file_data

    ###################################################################################

    def get_file_list(self, basedir=None, pattern=None):
        """
        search for files to read

        :param basedir: parameter to limit the search to a certain directory
        :type basedir: str
        :param pattern: change the default pattern
        :type pattern: str
        :return:
            list with fully qualified file names

        Example
        -------
        >>> import pyaerocom as pya
        >>> obj = pya.io.read_aeolus_l2a_data.ReadL2Data(verbose=True)
        >>> basedir='/lustre/storeB/project/fou/kl/admaeolus/data.rev.TD01/download/AE_TD01_ALD_U_N_2A_20190526T124829029_005400003_004387_0001/'
        >>> files = obj.get_file_list(basedir=basedir)

        >>> import pyaerocom as pya
        >>> obj = pya.io.read_aeolus_l2a_data.ReadL2Data(verbose=True)
        >>> basedir='/lustre/storeB/project/fou/kl/admaeolus/data.rev.TD01/download/'
        >>> files = obj.get_file_list(basedir=basedir)
        """

        if pattern is None:
            pattern = self._FILEMASK

        if basedir is None:
            basedir = self.DATASET_PATH

        self.logger.info('searching for data files at {}. This might take a while...'.format(basedir))
        files = glob.glob(os.path.join(basedir, '**',
                                       pattern),
                          recursive=True)

        return files

    ###################################################################################

    def calc_dist_in_data(self, ungridded_data_obj, location=(49.093, 8.428, 0.), backend='pyaerocom'):
        """calculate the distance between a given coordinate and all points in data using numpy and
        put that in data[*,self._DISTINDEX].
        The data array needs to be big enough for this!

        This method will likely never be used by a user, but serves as helper method for the colocate method

        Because the average earth radius in geopy.distance.EARTH_RADIUS is given in km, the result is also given in km

        The algorithm used to calculate the distance is needs the coordinates in rads. In order to not calculate that
        for for all the data points for every station, this is done only at the first call and the stored in
        data[:, self._RADLATINDEX] and self.data[:, self._RADLONINDEX]

        Using the pyaerocom backend of this method returns the same values as geopy.distance.great_circle
        but is roughly 2 magnitudes faster due to much less overhead and usage of the numpy vector functions for the
        calculation

        :param data:
        :param location:
        :param backend:

        Example
        -------
        >>> import logging
        >>> import read_aeolus_l2a_data
        >>> obj = read_aeolus_l2a_data.ReadAeolusL2aData(loglevel=logging.DEBUG)
        >>> obj.read(vars_to_retrieve=['ec355aer'])
        >>> location = (49.093,8.428,0.)
        >>> obj.calc_dist_in_data(location)
        >>> import numpy as np
        >>> print('min distance: {:.3f} km'.format(np.nanmin(obj.data[:, obj._DISTINDEX])))
        >>> print('max distance: {:.3f} km'.format(np.nanmax(obj.data[:, obj._DISTINDEX])))
        """

        start = time.perf_counter()
        data=ungridded_data_obj._data

        if backend == 'pyaerocom':
            if self.rads_in_array_flag:
                # lat1 = self.data[:, self._LATINDEX]
                # lon1 = self.data[:, self._LONINDEX]
                pass
            else:
                # put the lats and lons in rad in self.data
                np.deg2rad(ungridded_data_obj._data[:, self._LATINDEX], out=ungridded_data_obj._data[:, self._RADLATINDEX])
                np.deg2rad(ungridded_data_obj._data[:, self._LONINDEX], out=ungridded_data_obj._data[:, self._RADLONINDEX])
                # lat1 = np.deg2rad(self.data[:, self._LATINDEX], out=self.data[:, self._RADLATINDEX])
                # lon1 = np.deg2rad(self.data[:, self._LONINDEX], out=self.data[:, self._RADLONINDEX])
                self.rads_in_array_flag = True

            lat2 = np.deg2rad(location[0])
            lon2 = np.deg2rad(location[1])

            # code from IDL to match:
            # d =!const.R_Earth * 2 * asin(
            # sqrt((sin((lat1 - lat2) / 2)) ^ 2 + cos(lat1) * cos(lat2) * (sin((lon1 - lon2) / 2)) ^ 2))

            data[:, self._DISTINDEX] = (self.EARTH_RADIUS * 2. * np.arcsin(
                np.sqrt(
                    np.power(np.sin((data[:, self._RADLATINDEX] - lat2) / 2.), 2) + np.cos(
                        ungridded_data_obj._data[:, self._RADLATINDEX]) * np.cos(lat2) * np.power(
                        np.sin((data[:, self._RADLONINDEX] - lon2) / 2),
                        2))))

            end_time = time.perf_counter()
            elapsed_sec = end_time - start
            temp = 'time for single station distance calc [s]: {:.3f}'.format(elapsed_sec)
            self.logger.info(temp)

        elif backend == 'geopy':
            # use geopy to calculate distance
            # two magnitudes slower than the pyaerocom backend
            # but told us that we did the calculation right and opens a possibility to use
            # a geopy supported geoid for the calculation. Although that will then be another
            # magnitude slower than geopy.distance.great_circle
            start = time.perf_counter()
            for idx in range(len(data[:, self._TIMEINDEX])):
                # blend out NaNs in lat and long
                if np.isnan(ungridded_data_obj._data[idx, self._LATINDEX] + ungridded_data_obj._data[idx, self._LONINDEX]):
                    ungridded_data_obj._data[idx, self._DISTINDEX] = np.nan
                    continue

                # one magnitude slower than geopy.distance.great_circle
                # distance = geopy.distance.distance(locs[0],(file_data['latitude']['data'][idx], file_data['longitude']['data'][idx])).m
                # exclude wrong coordinates
                ungridded_data_obj._data[idx, self._DISTINDEX] = geopy.distance.great_circle(location,
                                                                              (ungridded_data_obj._data[idx, self._LATINDEX],
                                                                               ungridded_data_obj._data[idx, self._LONINDEX])).km

            end_time = time.perf_counter()
            elapsed_sec = end_time - start
            temp = 'time for single station distance calc using geopy [s]: {:.3f}'.format(elapsed_sec)
            self.logger.info(temp)
        else:
            pass

        # return self.data

    ###################################################################################
    def colocate(self, ungridded_data_obj, location=None, max_dist=50., bbox=None, resample_to_grid=None):
        """return a point cloud of points that fall within a given distance in km around a given location

        Because the average earth radius in geopy.distance.EARTH_RADIUS is given in km, the result is also given in km

        This method returns the same values as geopy.distance.great_circle

        :param ungridded_data_obj:
        :param location:
        :param max_dist:
        :param bbox:
        :param resample_to_grid:
        :return:

        Example
        -------
        >>> import logging
        >>> import pyaerocom as pya
        >>> obj = pya.io.read_aeolus_l2a_data.ReadL2Data(loglevel=logging.DEBUG)
        >>> testfiles = []
        >>> testfiles.append('/lustre/storeB/project/fou/kl/admaeolus/data.rev.2A02/download/2018-12/01/AE_OPER_ALD_U_N_2A_20181201T033526026_005423993_001590_0001.TGZ')
        >>> data=obj.read(files=testfiles)
        >>> # return the data points within a radius of a certain station
        >>> location = [(49.093,8.428,0.)]
        >>> max_dist = 300
        >>> result = obj.colocate(ungridded_data_obj=data,location=location, max_dist=max_dist)
        >>> import numpy as np
        >>> print('min distance: {:.3f} km'.format(np.nanmin(obj.data[:, obj._DISTINDEX])))
        >>> print('max distance: {:.3f} km'.format(np.nanmax(obj.data[:, obj._DISTINDEX])))
        >>> # return the data belonging to a certain area (here: EUROPE)
        >>> bbox = [(30., 80., -20., 70.)]
        >>> result = obj.colocate(bbox = bbox)
        >>> # return the data for regridding (selects the data for every grid point using the bboxes)
        >>> result = obj.colocate(resample_to_grid=True)
        >>> # find non empty bboxes
        >>> length=[len(result[x]['data']) for x in range(len(result))]
        >>> indexes=np.where(np.asarray(length) > 0.)[0].tolist()
        >>> result[indexes[0]]['bbox']
        >>> result[indexes[0]]['data'].shape
        """

        start = time.perf_counter()

        data = ungridded_data_obj._data
        ret_data = np.empty([self._ROWNO, self._COLNO], dtype=np.float_)
        index_counter = 0
        cut_flag = True
        matching_indexes = []
        if location is not None:
            if isinstance(location, list):
                # parameter is a list
                # iterate
                for idx_lat, loc in enumerate(location):
                    # calculate distance
                    self.calc_dist_in_data(ungridded_data_obj, loc)
                    matching_indexes = np.where(ungridded_data_obj._data[:, self._DISTINDEX] < max_dist)
                    matching_length = len(matching_indexes[0])
                    if matching_length > 0:
                        # check if the data fits into ret_data
                        end_index = index_counter + matching_length
                        if end_index > len(ret_data):
                            # append the needed elements
                            logging.info('adding {} elements to ret_data'.format(end_index - len(ret_data)))
                            ret_data = np.append(ret_data,
                                                 np.zeros([end_index - len(ret_data),
                                                           self._COLNO], dtype=np.float_, axis=0))
                            cut_flag = False

                        ret_data[index_counter:index_counter + matching_length, :] = \
                            ungridded_data_obj._data[matching_indexes, :]
                        index_counter += matching_length

            elif isinstance(location, tuple):
                logging.error('passing one location as tuple not supported at this point')
                pass
            else:
                logging.error('locations have to be passed as a list of tuples with (lat, lon)')
                pass
            # return only the part of the array containing some values
            if cut_flag:
                ret_data = ret_data[:index_counter, :]
            end_time = time.perf_counter()
            elapsed_sec = end_time - start
            temp = 'time for single station distance calc [s]: {:.3f}'.format(elapsed_sec)
            self.logger.info(temp)
            # log the found times
            unique_times = np.unique(ungridded_data_obj._data[matching_indexes, self._TIMEINDEX]).astype('datetime64[s]')
            self.logger.info('matching times:')
            self.logger.info(unique_times)

        elif bbox is not None:
            # return points in the bounding box given in bbox
            if isinstance(bbox, list):
                # parameter is a list
                # iterate
                ret_data = {}
                for idx, _bbox in enumerate(bbox):
                    ret_data[idx] = {}
                    ret_data[idx]['data'] = self.select_bbox(_bbox)
                    ret_data[idx]['bbox'] = _bbox
            else:
                pass
            end_time = time.perf_counter()
            elapsed_sec = end_time - start
            temp = 'time for bbox calc [s]: {:.3f}'.format(elapsed_sec)
            self.logger.info(temp)
        elif resample_to_grid:
            # resample to 1x1 degree grid at this point
            # create a list of tuple with the bounding boxes for a 1x1 degree grid
            # there's more efficient ways of doing that
            start_lat = -90.
            end_lat = 90.
            lat_spacing = 1.
            start_lon = -180.
            end_lon = 180.
            lon_spacing = 1.
            grid_lats_start = list(np.arange(start_lat, end_lat, lat_spacing))
            grid_lats_end = list(np.arange(start_lat + lat_spacing, end_lat + lat_spacing, lat_spacing))
            grid_lons_start = list(np.arange(start_lon, end_lon, lon_spacing))
            grid_lons_end = list(np.arange(start_lon + lon_spacing, end_lon + lon_spacing, lon_spacing))

            bbox_temp = []
            for idx_lat in range(len(grid_lats_start)):
                for idx_lon in range(len(grid_lons_start)):
                    bbox_temp.append((grid_lats_start[idx_lat], grid_lats_end[idx_lat],
                                      grid_lons_start[idx_lon], grid_lons_end[idx_lon]))
            ret_data = {}
            for idx, _bbox in enumerate(bbox_temp):
                # select the values
                ret_data[idx] = {}
                ret_data[idx]['data'] = self.select_bbox(_bbox)
                ret_data[idx]['bbox'] = _bbox
                if idx > 0 and idx % 1000 == 0:
                    self.logger.warning('{} boxes co-located'.format(idx))

            end_time = time.perf_counter()
            elapsed_sec = end_time - start
            temp = 'time for gridding calc [s]: {:.3f}'.format(elapsed_sec)
            self.logger.info(temp)
        else:
            pass

        return ret_data

    ###################################################################################

    def select_bbox(self, data=None, bbox=None):
        """method to return all points of self.data laying within a certain latitude and longitude range

        This method will likely never be used by a user, but serves as helper method for the colocate method

        EXAMPLE
        =======

        """
        start = time.perf_counter()

        lat_min = -90.
        lat_max = 90.
        lon_min = -180.
        lon_max = 360.

        if bbox is not None:
            logging.info(bbox)
            lat_min = bbox[0]
            lat_max = bbox[1]
            lon_min = bbox[2]
            lon_max = bbox[3]

        if data is None:
            _data = self.data
        else:
            try:
                _data = data._data
            except AttributeError:
                _data = data

            # remove NaNs at this point
            matching_indexes = np.where(np.isfinite(_data[:, self._LATINDEX]))
            ret_data = _data[matching_indexes[0], :]

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

            # end_time = time.perf_counter()
            # elapsed_sec = end_time - start
            # temp = 'time for single station bbox calc [s]: {:.3f}'.format(elapsed_sec)
            # self.logger.info(temp)
            # log the found times
            # unique_times = np.unique(self.data[matching_indexes,self._TIMEINDEX]).astype('datetime64[s]')
            # self.logger.info('matching times:')
            # self.logger.info(unique_times)
            # if len(ret_data) == 0:
            #     data_lat_min = np.nanmin(self.data[:,self._LATINDEX])
            #     data_lat_max = np.nanmax(self.data[:,self._LATINDEX])
            #     data_lon_min = np.nanmin(self.data[:,self._LONINDEX])
            #     data_lon_max = np.nanmax(self.data[:,self._LONINDEX])
            #     logging.info('[lat_min, lat_max, lon_min, lon_max in data]: '.format([data_lat_min, data_lat_max, data_lon_min, data_lon_max]))
            return ret_data

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

        bounds_dim_name = 'bounds'
        point_dim_name = 'point'
        lev_dim_name = self._LEVELSNAME
        lev_dim_bnds_name = self._ALTBOUNDSNAME
        time_dim_name = self._TIME_NAME
        lat_dim_name = self._LATITUDENAME
        lat_dim_bnds_name = self._LATBOUNDSNAME
        lon_dim_name = self._LONGITUDENAME
        lon_dim_bnds_name = self._LONBOUNDSNAME

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
            vars_to_write_out.extend(list(self.CODA_READ_PARAMETERS[self.RETRIEVAL_READ[0]]['metadata'].keys()))
            vars_to_write_out.append(self._UPPERALTITUDENAME)

            datetimedata = pd.to_datetime(_data[:, self._TIMEINDEX].astype('datetime64[s]'))
            # datetimedata = pd.to_datetime(_data[:, self._TIMEINDEX].astype('datetime64[ms]'))
            # pointnumber = np.arange(0, len(datetimedata))
            ds = xr.Dataset()

            # time and potentially levels are special variables that needs special treatment
            ds[time_dim_name] = (point_dim_name), datetimedata
            skip_vars = [time_dim_name, 'test_sca_pcd_mid_bins_qc_flag',]
            if lev_dim_name in vars_to_write_out:
                ds[lev_dim_name] = np.arange(self._LEVELSSIZE)
                skip_vars.extend([lev_dim_name])

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
            # write gridded 3d data to netcdf
            if netcdf_filename is None:
                netcdf_filename = '/tmp/to_netcdf_simple_gridded.nc'
            if data_to_write is None:
                _data = self.gridded_data
            else:
                _data = data_to_write

                # gridded
                pass
                time_dim_name = self._TIME_NAME
                lat_dim_name = self._LATITUDENAME
                lon_dim_name = self._LONGITUDENAME
                alt_dim_name = self._ALTITUDENAME
                lev_dim_name = self._LEVELSNAME
                altbnds_dim_name = 'bnds_2'

                ds = xr.Dataset()

                # ds[time_dim_name] = np.array(np.mean(_data[time_dim_name]).astype('datetime64[s]'))
                ds[time_dim_name] = (time_dim_name), _data[time_dim_name]
                ds[lat_dim_name] = (lat_dim_name), _data[lat_dim_name],
                ds[lon_dim_name] = (lon_dim_name), _data[lon_dim_name]
                ds[lev_dim_name] = (lev_dim_name), np.arange(_data[alt_dim_name].shape[1])
                ds[alt_dim_name] = (time_dim_name, lev_dim_name, lat_dim_name, lon_dim_name), _data[alt_dim_name]
                # ds[self._ALTBOUNDSNAME] = (alt_dim_name, altbnds_dim_name), _data[self._ALTBOUNDSNAME]

                # for var in vars_to_write_out:
                vars_to_write_out = data_to_write.keys()
                for var in vars_to_write_out:
                    if var in self.COORDINATE_NAMES:
                        # if var == self._TIME_NAME:
                        continue
                    # 3D data
                    ds[var + '_mean'] = (time_dim_name, lev_dim_name, lat_dim_name, lon_dim_name), _data[var]['mean']
                    ds[var + '_numobs'] = (time_dim_name, lev_dim_name, lat_dim_name, lon_dim_name), _data[var]['numobs']
                    ds[var + '_stddev'] = (time_dim_name, lev_dim_name, lat_dim_name, lon_dim_name), _data[var]['stddev']

            # add attributes to variables
            for var in ds.variables:
                # add predifined attributes
                # print('var {}'.format(var))
                try:
                    for attrib in self.NETCDF_VAR_ATTRIBUTES[var]:
                        ds[var].attrs[attrib] = self.NETCDF_VAR_ATTRIBUTES[var][attrib]
                except KeyError:
                    pass

            # remove _FillValue attribute from coordinate variables since that
            # is forbidden by CF convention
            # unfortunately this does not work for level 3 data where the var name == dim name for some reason
            for var in self.COORDINATE_NAMES:
                try:
                    del ds[var].encoding['_FillValue']
                except KeyError:
                    pass

        # add potential global attributes
        try:
            for name in global_attributes:
                ds.attrs[name] = global_attributes[name]
        except:
            pass

        # temp = 'writing file: {}'.format(netcdf_filename)
        # self.logger.info(temp)
        ds.to_netcdf(netcdf_filename)

        end_time = time.perf_counter()
        elapsed_sec = end_time - start_time
        temp = 'time for netcdf write [s]: {:.3f}'.format(elapsed_sec)
        self.logger.info(temp)
        temp = 'file written: {}'.format(netcdf_filename)
        self.logger.info(temp)

    ###################################################################################
    # def to_netcdf_simple(self, netcdf_filename='/home/jang/tmp/to_netcdf_simple.nc',
    #                      global_attributes=None, vars_to_read=['ec355aer'],
    #                      data_to_write=None):
    #
    #     """method to store the file contents in a very basic netcdf file
    #     >>> import read_aeolus_l2a_data
    #     >>> obj = read_aeolus_l2a_data.ReadAeolusL2aData(verbose=True)
    #     >>> import os
    #     >>> os.environ['CODA_DEFINITION']='/lustre/storeA/project/aerocom/aerocom1/ADM_CALIPSO_TEST/'
    #     >>> filename = '/lustre/storeB/project/fou/kl/admaeolus/data.rev.2A02/AE_OPER_ALD_U_N_2A_20181201T033526026_005423993_001590_0001.DBL'
    #     >>> # read returning a ndarray
    #     >>> filedata_numpy = obj.read_file(filename, vars_to_retrieve=['ec355aer'], return_as='numpy')
    #     >>> obj.ndarr2data(data_numpy)
    #     >>> obj.to_netcdf_simple()
    #
    #     Parameters:
    #     ----------
    #         global_attributes : dict
    #         dictionary with things to put into the global attributes of a netcdf file
    #
    #     """
    #
    #     start_time = time.perf_counter()
    #     import xarray as xr
    #     import pandas as pd
    #     import numpy as np
    #
    #     vars_to_read_in = vars_to_read.copy()
    #     if isinstance(vars_to_read_in, str):
    #         vars_to_read_in = [vars_to_read_in]
    #
    #     if data_to_write is None:
    #         _data = self.data
    #     else:
    #         _data = data_to_write
    #
    #     vars_to_read_in.extend(list(self.RETRIEVAL_READ_PARAMETERS[self.RETRIEVAL_READ[0]]['metadata'].keys()))
    #
    #     datetimedata = pd.to_datetime(_data[:, self._TIMEINDEX].astype('datetime64[s]'))
    #     pointnumber = np.arange(0, len(datetimedata))
    #     ds = xr.Dataset()
    #     ds.coords['point'] = pointnumber
    #     # time is a special variable that needs special treatment
    #     ds['time'] = ('point'), datetimedata
    #     for var in vars_to_read_in:
    #         if var == self._TIME_NAME:
    #             continue
    #         ds[var] = ('point'), _data[:, self.INDEX_DICT[var]]
    #         try:
    #             for attrib in self.NETCDF_VAR_ATTRIBUTES[var]:
    #                 ds[var].attrs[attrib] = self.NETCDF_VAR_ATTRIBUTES[var][attrib]
    #
    #         except KeyError:
    #             pass
    #
    #     try:
    #         for name in global_attributes:
    #             ds.attrs[name] = global_attributes[name]
    #     except:
    #         pass
    #
    #     ds.to_netcdf(netcdf_filename)
    #
    #     end_time = time.perf_counter()
    #     elapsed_sec = end_time - start_time
    #     temp = 'time for netcdf write [s]: {:.3f}'.format(elapsed_sec)
    #     self.logger.info(temp)
    #     temp = 'file written: {}'.format(netcdf_filename)
    #     self.logger.info(temp)

    ###################################################################################

    def read_data_fields(self, filename, coda_handle=None,
                         fields_to_read=['mph','sca_optical_properties'], loglevel=None):
        """method to read certain fields of an ESA binary data file

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_read : list
            list of str with variable names to read; defaults to ['od355aer']
        verbose : Bool
            set to True to increase verbosity

        Returns
        --------
        Either:
            dictionary (default):
                keys are 'time', 'latitude', 'longitude', 'altitude' and the variable names
                'ec355aer', 'bs355aer', 'sr', 'lod' if the whole file is read
                'time' is a 1d array, while the other dict values are a another dict with the
                time as keys (the same ret['time']) and a numpy array as values. These values represent the profile.
                Note 1: latitude and longitude are height dependent due to the tilt of the measurement.
                Note 2: negative values indicate a NaN

            2d ndarray of type float:
                representing a 'point cloud' with all points
                    column 1: time in seconds since the Unix epoch with ms accuracy (same time for every height
                    in a profile)
                    column 2: latitude
                    column 3: longitude
                    column 4: altitude
                    column 5: extinction
                    column 6: backscatter
                    column 7: sr
                    column 8: lod

                    Note: negative values are put to np.nan already

                    The indexes are noted in read_aeolus_l2a_data.ReadAeolusL2aData.<index_name>
                    e.g. the time index is named read_aeolus_l2a_data.ReadAeolusL2aData._TIMEINDEX
                    have a look at the example to access the values

        This is whats in one DBL file
        codadump list /lustre/storeB/project/fou/kl/admaeolus/data.rev.2A02/AE_OPER_ALD_U_N_2A_20181201T033526026_005423993_001590_0001.DBL

        /mph/product
        /mph/proc_stage
        /mph/ref_doc
        /mph/acquisition_station
        /mph/proc_center
        /mph/proc_time
        /mph/software_ver
        /mph/baseline
        /mph/sensing_start
        /mph/sensing_stop
        /mph/phase
        /mph/cycle
        /mph/rel_orbit
        /mph/abs_orbit
        /mph/state_vector_time
        /mph/delta_ut1
        /mph/x_position
        /mph/y_position
        /mph/z_position
        /mph/x_velocity
        /mph/y_velocity
        /mph/z_velocity
        /mph/vector_source
        /mph/utc_sbt_time
        /mph/sat_binary_time
        /mph/clock_step
        /mph/leap_utc
        /mph/leap_sign
        /mph/leap_err
        /mph/product_err
        /mph/tot_size
        /mph/sph_size
        /mph/num_dsd
        /mph/dsd_size
        /mph/num_data_sets
        /sph/sph_descriptor
        /sph/intersect_start_lat
        /sph/intersect_start_long
        /sph/intersect_stop_lat
        /sph/intersect_stop_long
        /sph/sat_track
        /sph/num_brc
        /sph/num_meas_max_brc
        /sph/num_bins_per_meas
        /sph/num_prof_sca
        /sph/num_prof_ica
        /sph/num_prof_mca
        /sph/num_group_tot
        /dsd[?]/ds_name
        /dsd[?]/ds_type
        /dsd[?]/filename
        /dsd[?]/ds_offset
        /dsd[?]/ds_size
        /dsd[?]/num_dsr
        /dsd[?]/dsr_size
        /dsd[?]/byte_order
        /geolocation[?]/start_of_obs_time
        /geolocation[?]/num_meas_eff
        /geolocation[?]/measurement_geolocation[?]/centroid_time
        /geolocation[?]/measurement_geolocation[?]/mie_geolocation_height_bin[25]/longitude_of_height_bin
        /geolocation[?]/measurement_geolocation[?]/mie_geolocation_height_bin[25]/latitude_of_height_bin
        /geolocation[?]/measurement_geolocation[?]/mie_geolocation_height_bin[25]/altitude_of_height_bin
        /geolocation[?]/measurement_geolocation[?]/rayleigh_geolocation_height_bin[25]/longitude_of_height_bin
        /geolocation[?]/measurement_geolocation[?]/rayleigh_geolocation_height_bin[25]/latitude_of_height_bin
        /geolocation[?]/measurement_geolocation[?]/rayleigh_geolocation_height_bin[25]/altitude_of_height_bin
        /geolocation[?]/measurement_geolocation[?]/longitude_of_dem_intersection
        /geolocation[?]/measurement_geolocation[?]/latitude_of_dem_intersection
        /geolocation[?]/measurement_geolocation[?]/altitude_of_dem_intersection
        /geolocation[?]/geoid_separation
        /meas_pcd[?]/start_of_obs_time
        /meas_pcd[?]/l1b_input_screening/l1b_obs_screening
        /meas_pcd[?]/l1b_input_screening/l1b_obs_screening_flags[40]
        /meas_pcd[?]/l1b_input_screening/l1b_mie_meas_screening[?]/l1b_mie_meas_qc
        /meas_pcd[?]/l1b_input_screening/l1b_mie_meas_screening[?]/l1b_mie_meas_qc_flags[8]
        /meas_pcd[?]/l1b_input_screening/l1b_rayleigh_meas_screening[?]/l1b_rayleigh_meas_qc
        /meas_pcd[?]/l1b_input_screening/l1b_rayleigh_meas_screening[?]/l1b_rayleigh_meas_qc_flags[8]
        /meas_pcd[?]/l1b_cal_screening/cal_valid
        /meas_pcd[?]/l2a_processing_qc/sca_applied
        /meas_pcd[?]/l2a_processing_qc/ica_applied
        /meas_pcd[?]/l2a_processing_qc/mca_applied
        /meas_pcd[?]/l2a_processing_qc/feature_finder_indicators/layer_information[24]/bin_loaded
        /meas_pcd[?]/l2a_processing_qc/feature_finder_indicators/layer_information[24]/seed[30]
        /meas_pcd[?]/l2a_processing_qc/feature_finder_indicators/lowest_computable_bin[30]
        /sca_pcd[?]/starttime
        /sca_pcd[?]/firstmatchingbin
        /sca_pcd[?]/qc_flag
        /sca_pcd[?]/profile_pcd_bins[24]/extinction_variance
        /sca_pcd[?]/profile_pcd_bins[24]/backscatter_variance
        /sca_pcd[?]/profile_pcd_bins[24]/lod_variance
        /sca_pcd[?]/profile_pcd_bins[24]/processing_qc_flag
        /sca_pcd[?]/profile_pcd_mid_bins[23]/extinction_variance
        /sca_pcd[?]/profile_pcd_mid_bins[23]/backscatter_variance
        /sca_pcd[?]/profile_pcd_mid_bins[23]/lod_variance
        /sca_pcd[?]/profile_pcd_mid_bins[23]/ber_variance
        /sca_pcd[?]/profile_pcd_mid_bins[23]/processing_qc_flag
        /ica_pcd[?]/starttime
        /ica_pcd[?]/first_matching_bin
        /ica_pcd[?]/qc_flag
        /ica_pcd[?]/ica_processing_qc_flag_bin[24]
        /mca_pcd[?]/starttime
        /mca_pcd[?]/processing_qc_flag_bin[24]
        /amd_pcd[?]/starttime
        /amd_pcd[?]/l2b_amd_screening_qc
        /amd_pcd[?]/l2b_amd_screening_qc_flags
        /amd_pcd[?]/l2b_amd_collocations[?]/l2b_amd_collocation_qc
        /amd_pcd[?]/l2b_amd_collocations[?]/l2b_amd_collocation_qc_flags
        /group_pcd[?]/starttime
        /group_pcd[?]/brc_start
        /group_pcd[?]/measurement_start
        /group_pcd[?]/brc_end
        /group_pcd[?]/measurement_end
        /group_pcd[?]/height_bin_index
        /group_pcd[?]/upper_problem_flag
        /group_pcd[?]/particle_extinction_variance
        /group_pcd[?]/particle_backscatter_variance
        /group_pcd[?]/particle_lod_variance
        /group_pcd[?]/qc_flag
        /group_pcd[?]/mid_particle_extinction_variance_top
        /group_pcd[?]/mid_particle_backscatter_variance_top
        /group_pcd[?]/mid_particle_lod_variance_top
        /group_pcd[?]/mid_particle_ber_variance_top
        /group_pcd[?]/mid_particle_extinction_variance_bot
        /group_pcd[?]/mid_particle_backscatter_variance_bot
        /group_pcd[?]/mid_particle_lod_variance_bot
        /group_pcd[?]/mid_particle_ber_variance_bot
        /sca_optical_properties[?]/starttime
        /sca_optical_properties[?]/sca_optical_properties[24]/extinction
        /sca_optical_properties[?]/sca_optical_properties[24]/backscatter
        /sca_optical_properties[?]/sca_optical_properties[24]/lod
        /sca_optical_properties[?]/sca_optical_properties[24]/sr
        /sca_optical_properties[?]/geolocation_middle_bins[24]/longitude
        /sca_optical_properties[?]/geolocation_middle_bins[24]/latitude
        /sca_optical_properties[?]/geolocation_middle_bins[24]/altitude
        /sca_optical_properties[?]/sca_optical_properties_mid_bins[23]/extinction
        /sca_optical_properties[?]/sca_optical_properties_mid_bins[23]/backscatter
        /sca_optical_properties[?]/sca_optical_properties_mid_bins[23]/lod
        /sca_optical_properties[?]/sca_optical_properties_mid_bins[23]/ber
        /ica_optical_properties[?]/starttime
        /ica_optical_properties[?]/ica_optical_properties[24]/case
        /ica_optical_properties[?]/ica_optical_properties[24]/extinction
        /ica_optical_properties[?]/ica_optical_properties[24]/backscatter
        /ica_optical_properties[?]/ica_optical_properties[24]/lod
        /mca_optical_properties[?]/starttime
        /mca_optical_properties[?]/mca_optical_properties[24]/climber
        /mca_optical_properties[?]/mca_optical_properties[24]/extinction
        /mca_optical_properties[?]/mca_optical_properties[24]/lod
        /amd[?]/starttime
        /amd[?]/amd_properties[24]/pressure_fp
        /amd[?]/amd_properties[24]/temperature_fp
        /amd[?]/amd_properties[24]/frequencyshift_fp
        /amd[?]/amd_properties[24]/relativehumidity_fp
        /amd[?]/amd_properties[24]/molecularlod_fp
        /amd[?]/amd_properties[24]/molecularbackscatter_fp
        /amd[?]/amd_properties[24]/pressure_fiz
        /amd[?]/amd_properties[24]/temperature_fiz
        /amd[?]/amd_properties[24]/frequencyshift_fiz
        /amd[?]/amd_properties[24]/relativehumidity_fiz
        /amd[?]/amd_properties[24]/molecularlod_fiz
        /amd[?]/amd_properties[24]/molecularbackscatter_fiz
        /group_optical_properties[?]/starttime
        /group_optical_properties[?]/height_bin_index
        /group_optical_properties[?]/group_optical_property/group_extinction
        /group_optical_properties[?]/group_optical_property/group_backscatter
        /group_optical_properties[?]/group_optical_property/group_lod
        /group_optical_properties[?]/group_optical_property/group_sr
        /group_optical_properties[?]/group_geolocation_middle_bins/start_longitude
        /group_optical_properties[?]/group_geolocation_middle_bins/start_latitude
        /group_optical_properties[?]/group_geolocation_middle_bins/start_altitude
        /group_optical_properties[?]/group_geolocation_middle_bins/mid_longitude
        /group_optical_properties[?]/group_geolocation_middle_bins/mid_latitude
        /group_optical_properties[?]/group_geolocation_middle_bins/mid_altitude
        /group_optical_properties[?]/group_geolocation_middle_bins/stop_longitude
        /group_optical_properties[?]/group_geolocation_middle_bins/stop_latitude
        /group_optical_properties[?]/group_geolocation_middle_bins/stop_altitude
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_extinction_top
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_backscatter_top
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_lod_top
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_ber_top
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_extinction_bot
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_backscatter_bot
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_lod_bot
        /group_optical_properties[?]/group_optical_property_middle_bins/mid_ber_bot
        /scene_classification[?]/starttime
        /scene_classification[?]/height_bin_index
        /scene_classification[?]/aladin_cloud_flag/clrh
        /scene_classification[?]/aladin_cloud_flag/clsr
        /scene_classification[?]/aladin_cloud_flag/downclber
        /scene_classification[?]/aladin_cloud_flag/topclber
        /scene_classification[?]/nwp_cloud_flag
        /scene_classification[?]/l2a_group_class_reliability

        The question mark indicates a variable size array

        It is not entirely clear what we actually have to look at.
        For simplicity the data of the group 'sca_optical_properties' is returned at this point

        Example
        -------
        >>> import read_aeolus_l2a_data
        >>> obj = read_aeolus_l2a_data.ReadAeolusL2aData(verbose=True)
        >>> import os
        >>> os.environ['CODA_DEFINITION']='/lustre/storeA/project/aerocom/aerocom1/ADM_CALIPSO_TEST/'
        >>> filename = '/lustre/storeB/project/fou/kl/admaeolus/data.rev.2A02/AE_OPER_ALD_U_N_2A_20181201T033526026_005423993_001590_0001.DBL'
        >>> # read returning a ndarray
        >>> coda_data = obj.read_data_fields(filename)
        """

        import time
        import coda

        # coda uses 2000-01-01T00:00:00 as epoch unfortunately.
        # so calculate the difference in seconds to the Unix epoch
        seconds_to_add = np.datetime64('2000-01-01T00:00:00') - np.datetime64('1970-01-01T00:00:00')
        seconds_to_add = seconds_to_add.astype(np.float_)

        # the same can be achieved using pandas, but we stick to numpy here
        # base_time = pd.DatetimeIndex(['2000-01-01'])
        # seconds_to_add = (base_time.view('int64') // pd.Timedelta(1, unit='s'))[0]

        start = time.perf_counter()
        file_data = {}

        self.logger.info('reading file {}'.format(filename))
        # read file
        if coda_handle is None:
            coda_handle = coda.open(filename)
        root_field_names = coda.get_field_names(coda_handle)
        coda_data = {}
        ret_data = {}
        mph_fieldnames = coda.get_field_names(coda_handle, 'mph')

        for root_field_name in root_field_names:
            if root_field_name in fields_to_read:
                if root_field_name == 'mph':
                    # the were cases were coda.fetch(coda_handle, root_field_name) did not work.
                    # read field by field and handle coda.CodacError on that basis
                    ret_data[root_field_name] = {}
                    for fieldname in mph_fieldnames:
                        print(fieldname)
                        try:
                            ret_data[root_field_name][fieldname] = coda.fetch(coda_handle, root_field_name, fieldname)
                        except coda.CodacError:
                            continue
                else:
                    coda_data[root_field_name] = coda.fetch(coda_handle, root_field_name)
                    if isinstance(coda_data[root_field_name],coda.codapython.Record):
                        ret_data[root_field_name] = self.codarecord2pythonstruct(coda_data[root_field_name])
                    else:
                        ret_data[root_field_name] = []
                        for index, name in enumerate(coda_data[root_field_name]):
                            dummy = self.codarecord2pythonstruct(name)
                            ret_data[root_field_name].append(dummy)
                            # ret_data[root_field_name].append(self.codarecord2pythonstruct(name))

        end_time = time.perf_counter()
        elapsed_sec = end_time - start
        temp = 'time for single file read [s]: {:.3f}'.format(elapsed_sec)
        self.logger.info(temp)

        return ret_data

    ###################################################################################

    def codarecord2pythonstruct(self, codaRec):
        """small helper routine to turn a coda record struct into a python struct

        calls itself recursively if codaRec is of type numpy.ndarray
        """

        out_struct = {}
        import numpy as np
        for idx in range(len(codaRec)):
            if isinstance(codaRec[idx],np.ndarray):
                rec_length = len(codaRec[idx])
                for idx2 in range(rec_length):
                    # example dummy:
                    #  {'extinction': -1000000.0,
                    # 'backscatter': -1000000.0,
                    # 'lod': -1.0,
                    # 'sr': -1.0},
                    dummy = self.codarecord2pythonstruct(codaRec[idx][idx2])
                    if idx2 == 0:
                        # define the returned struct
                        out_struct[codaRec._registeredFields[idx]] = {}
                        for str_name in dummy:
                            out_struct[codaRec._registeredFields[idx]][str_name] = np.empty(rec_length, dtype=np.float_)

                    for str_name in dummy:
                        out_struct[codaRec._registeredFields[idx]][str_name][idx2] = dummy[str_name]
            else:
                # print(type(codaRec[idx]))
                # the the dict keys exists: reform to array
                if codaRec._registeredFields[idx] in out_struct:
                    # this code is not called due to the way the data is organised in the
                    # ESA binary file right now
                    if isinstance(codaRec._registeredFields[idx],dict):
                        #reform to array
                        ref_dummy = codaRec._registeredFields[idx]
                        codaRec._registeredFields[idx] = []
                        codaRec._registeredFields[idx].append(ref_dummy)
                        codaRec._registeredFields[idx].append(codaRec[idx])
                    elif isinstance(codaRec._registeredFields[idx],list):
                        codaRec._registeredFields[idx].append(codaRec[idx])
                    else:
                        # might be needed later
                        pass
                else:
                    out_struct[codaRec._registeredFields[idx]] = codaRec[idx]

        return out_struct

    ###################################################################################
    def to_netcdf_data(self,filename, coda_data, grouping='names', verbose=False):
        """method to write coda data into a netcdf file

        Since coda data is has a hierarchy, the user may choose if the data is written into
        netcdf file using groups (netcdf4), or a flat (netcdf4 classic model) netcdf file
        where the hierarchy is retained in the variable names

        Example
        -------

        DONOTUSE!

        >>> import read_aeolus_l2a_data
        >>> obj = read_aeolus_l2a_data.ReadAeolusL2aData(verbose=True)
        >>> import os
        >>> os.environ['CODA_DEFINITION']='/lustre/storeA/project/aerocom/aerocom1/ADM_CALIPSO_TEST/'
        >>> filename = '/lustre/storeB/project/fou/kl/admaeolus/data.rev.2A02/AE_OPER_ALD_U_N_2A_20181201T033526026_005423993_001590_0001.DBL'
        >>> # read returning a ndarray
        >>> coda_data = obj.read_data_fields(filename)
        >>> import xarray as xr
        >>> ds = xr.Dataset()
        """

        import time
        start_time = time.perf_counter()
        import xarray as xr
        import pandas as pd
        import numpy as np

        if grouping == 'names':
            ds = xr.Dataset()
            # group the data by putting the names with double underscores together
            # (single underscores are used by coda in its field names already)
            pass
            for lev1_name in coda_data:
                # lev1 is alsways a dict
                if isinstance(coda_data[lev1_name],dict):
                    for lev2_name in coda_data[lev1_name]:
                        if isinstance(coda_data[lev1_name][lev2_name],dict):
                            for lev3_name in coda_data[lev1_name][lev2_name]:
                                if isinstance(coda_data[lev1_name][lev2_name][lev3_name],dict):
                                    pass
                                pass
                        elif isinstance(coda_data[lev1_name][lev2_name],list):
                            # assume a list of identical dicts here
                            for idx, dummy in enumerate(coda_data[lev1_name]):
                                if idx == 0:
                                    # create dict containing the data lists
                                    group_dummy = {}
                                    for _key in coda_data[lev1_name][idx]:
                                        group_dummy[_key] = []
                                # now fill the data list
                                # do that with python lists for now

                                #starttime is special because we need that several times
                                try:
                                    time = coda_data[lev1_name][idx]['starttime']
                                except KeyError:
                                    time = -1.E6

                                for _key in coda_data[lev1_name][idx]:
                                    if isinstance(coda_data[lev1_name][idx][_key],list):
                                        pass

                        else:
                            var_name = '__'.join([lev1_name,lev2_name])
                            ds[var_name] = coda_data[lev1_name][lev2_name]

                else:
                    # coda_data[lev1_name} is a scalar
                    pass
                    var_name = lev1_name
                    ds[var_name] = coda_data[lev1_name]

                    for lev3_name in coda_data[lev1_name][lev2_name]:
                        pass
        else:
            pass
            # use netcdf4 groups to build the hierarchy

        # datetimedata = pd.to_datetime(self.data[:, self._TIMEINDEX].astype('datetime64[s]'))
        # pointnumber = np.arange(0, len(datetimedata))
        # ds = xr.Dataset()
        # ds['time'] = ('point'), datetimedata
        # ds['latitude'] = ('point'), self.data[:, self._LATINDEX]
        # ds['longitude'] = ('point'), self.data[:, self._LONINDEX]
        # ds['height'] = ('point'), self.data[:, self._ALTITUDEINDEX]
        # ds['ec355aer'] = ('point'), self.data[:, self._EC355INDEX]
        # ds.coords['point'] = pointnumber
        # ds.to_netcdf(netcdf_filename)

        end_time = time.perf_counter()
        elapsed_sec = end_time - start_time
        temp = 'time for netcdf write [s]: {:.3f}'.format(elapsed_sec)
        self.logger.info(temp)
        temp = 'file written: {}'.format(netcdf_filename)
        self.logger.info(temp)

    ###################################################################################

    def plot_location_map(self, plotfilename, data=None, bbox=None, himalaya_flag=None, title=None,
                          plot_time = True, arcgis_background=False):
        """small routine to plot the satellite track on a map

        """

        import matplotlib.pyplot as plt
        from mpl_toolkits.basemap import Basemap
        import numpy as np

        if data is None:
            _data = self.data
        else:
            try:
                _data = data._data
            except AttributeError:
                _data = data

        lats = _data[:,self._LATINDEX]
        lons = _data[:,self._LONINDEX]
        max_index=len(lats)
        min_index=0
        if max_index == 0:
            self.logger.info('plotmap: no points to plot! Returning.')
            return

        if bbox:
            pass

            lat_low = bbox[0]
            lat_high = bbox[1]
            lon_low = bbox[2]
            lon_high = bbox[3]
            himalaya_flag = True
        else:
            lat_low = -90.
            lat_high = 90.
            lon_low = -180.
            lon_high = 180.
            himalaya_flag = True

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
        himalaya_data['Everest']=(27.988056, 86.925278)
        himalaya_data['K2']=(35.8825, 76.513333)
        himalaya_data['Kangchenjunga']=(27.7025, 88.146667)
        himalaya_data['Lhotse']=(27.961667, 86.933333)
        himalaya_data['Makalu']=(27.889167, 87.088611)
        himalaya_data['Cho Oyu']=(28.094167, 86.660833)
        himalaya_data['Dhaulagiri']=(28.698333, 83.4875)
        himalaya_data['Manaslu']=(28.549444, 84.561944)
        himalaya_data['Nanga Parbat']=(35.2375, 74.589167)
        himalaya_data['Annapurna Massif']=(28.596111, 83.820278)
        himalaya_data['Gasherbrum I']=(35.724444, 76.696389)
        himalaya_data['Broad Peak']=(35.811667, 76.565)
        himalaya_data['Gasherbrum II']=(35.758333, 76.653333)
        himalaya_data['Shishapangma']=(28.352222, 85.779722)

        m = Basemap(projection='cyl', llcrnrlat=lat_low, urcrnrlat=lat_high,
                    llcrnrlon=lon_low, urcrnrlon=lon_high, resolution='c', fix_aspect=False)

        x, y = m(lons, lats)
        # m.drawmapboundary(fill_color='#99ffff')
        # m.fillcontinents(color='#cc9966', lake_color='#99ffff')
        plot = m.scatter(x, y, 4, marker='o', color='r', )
        m.drawmeridians(np.arange(-180, 220, 40), labels=[0, 0, 0, 1], fontsize=10)
        m.drawparallels(np.arange(-90, 120, 30), labels=[1, 1, 0, 0], fontsize=10)
        # axis = plt.axis([LatsToPlot.min(), LatsToPlot.max(), LonsToPlot.min(), LonsToPlot.max()])
        ax = plot.axes
        if arcgis_background:
            # m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)
            m.arcgisimage(service='World_Shaded_Relief', xpixels = 1500, verbose= True)
        else:
            m.drawcoastlines()
            # m.etopo()

        if bbox is not None:
            m.drawcountries()
            # m.drawrivers()

        if himalaya_flag:
            for peak in himalaya_data:
                x,y=m(himalaya_data[peak][1], himalaya_data[peak][0])
                plot=m.plot(x, y, 4, marker='.', color='b')

        if title:
            plt.title(title,fontsize='xx-small')

        if plot_time:
            # plot 2 time stamps next to 2 dots to make the times clear

            min_index = np.int(np.floor_divide(len(lats),10.))
            max_index = np.int(len(lats) - min_index)
            time_str = _data[min_index, self._TIMEINDEX].astype('datetime64[s]')
            x,y = m(_data[min_index, self._LONINDEX], _data[min_index, self._LATINDEX])
            # plt.annotate(time_str, xy=(x, y),  xycoords='data', color='k')
            plt.annotate(time_str, xy=(x, y),
                         xycoords='data',
                         color='k',
                         fontsize='xx-small',
                         ha='center')
            time_str = _data[max_index, self._TIMEINDEX].astype('datetime64[s]')
            x,y = m(_data[max_index, self._LONINDEX], _data[max_index, self._LATINDEX])
            plt.annotate(time_str, xy=(x, y),
                         xycoords='data',
                         color='k',
                         fontsize='xx-small',
                         ha='center')

        plt.savefig(plotfilename, dpi=300)
        plt.close()

    ###################################################################################
    def plot_profile_v2(self, plotfilename, data_to_plot=None, vars_to_plot = ['ec355aer'], retrieval_name=None,
                        title=None,
                        plot_range=(0.,2000.),
                        plot_nbins=20.,
                        linear_time=False):
        """plot sample profile plot

        """
        import matplotlib.pyplot as plt
        import matplotlib
        from matplotlib.colors import BoundaryNorm
        from matplotlib.ticker import MaxNLocator

        from scipy import interpolate

        if data_to_plot is None:
            _data = self.data
        else:
            try:
                _data = data_to_plot._data
            except AttributeError:
                _data = data_to_plot

        # read returning a ndarray
        times = _data[:,obj._TIMEINDEX]
        times_no = len(times)
        plot_data = {}
        plot_data_masks = {}
        unique_times = np.unique(times)
        time_step_no = len(unique_times)
        vars_to_plot_arr = [self._ALTITUDENAME]
        vars_to_plot_arr.extend(vars_to_plot)
        filling_zero_val = 0.
        plotting_zero_val = np.nan

        target_height_no = 2001
        intermediate_height_no = 50
        # height step size in m for plotting
        height_step_size = 10.
        target_heights = np.arange(0,target_height_no)*height_step_size
        #target_heights = np.flip(target_heights)
        target_x = np.arange(0,time_step_no)

        for data_var in vars_to_plot_arr:
            # plot_data[data_var] = \
            #     _data[:, self.INDEX_DICT[data_var]]
            plot_data_masks[data_var] = np.isnan(_data[:, self.INDEX_DICT[data_var]])

        # because of height individual quality flags, there will never be all the height steps
        # of a profile in _data.
        # Therefore the number of height steps per time code is not necessarily equal
        # to self._HEIGHTSTEPNO anymore
        # e.g. due to an area based selection or due to NaNs in the profile
        # we therefore have to go through the times and look for changes

        idx_time = times[0]
        time_cut_start_index = 0
        time_cut_end_index = 0
        time_index_dict = {}

        # reconstruct the aeolus profile to cover all height steps so that the nearest neighbour interpolation
        # used for the plot is correct.
        # unfortunately we don't even know all the height levels in the profile because they
        # might not be retrievable or the lower height might be NaN
        # interpolate the existing time steps to a 250m grid (assuming this 250m as the minimum height)

        for idx, time in enumerate(times):
            if time == idx_time:
                time_cut_end_index = idx
            else:
                time_cut_end_index = idx
                time_index_dict[idx_time] = np.arange(time_cut_start_index, time_cut_end_index )
                time_cut_start_index = idx
                idx_time = time

        time_index_dict[idx_time] = np.arange(time_cut_start_index, time_cut_end_index + 1)

        for var in vars_to_plot:
            # this loop has not been optimised for several variables
            out_arr = np.zeros([time_step_no, target_height_no])
            out_arr[:] = np.nan
            for time_step_idx, unique_time in enumerate(unique_times):
                var_data = _data[time_index_dict[unique_time],self.INDEX_DICT[var]]
                # scipy.interpolate cannot cope with nans in the data
                # work only on profiles with a nansum > 0

                nansum = np.nansum(var_data)

                if nansum > 0 and len(var_data) > 1:
                    height_data = _data[time_index_dict[unique_time], self.INDEX_DICT[self._ALTITUDENAME]]
                    if np.isnan(np.sum(var_data)):
                        # lower_height_data = lower_height_data[~plot_data_masks[var][time_index_dict[unique_time]]]
                        height_data = height_data[~plot_data_masks[var][time_index_dict[unique_time]]]
                        var_data = var_data[~plot_data_masks[var][time_index_dict[unique_time]]]

                    if len(height_data) < 10.:
                        try:
                            lower_height_data = _data[time_index_dict[unique_time], self.INDEX_DICT[self._UPPERALTITUDENAME]]
                        except TypeError:
                            pass

                        if np.isnan(np.sum(var_data)):
                            lower_height_data = lower_height_data[~plot_data_masks[var][time_index_dict[unique_time]]]

                        # make sure that gaps in the input profile are also present in the profile created by
                        # a nearest neighbour interpolation (used for better looking plots)
                        plot_heights_temp = np.zeros(intermediate_height_no)
                        plot_val_temp = np.zeros(intermediate_height_no)
                        temp_height_index = 0
                        zero_filled_flag = False
                        # note that the order of heights is from top to bottom
                        for height_level in range(len(height_data)):
                            # if the former height level has been surrounded by filling_zero_val
                            # we also have to surround the actual height with filling_zero_val
                            # to make the nearest neighbour interpolation right
                            if zero_filled_flag:
                                zero_filled_flag = False
                                plot_heights_temp[temp_height_index] = height_data[height_level] + height_step_size
                                plot_val_temp[temp_height_index] = filling_zero_val
                                temp_height_index += 1

                            plot_heights_temp[temp_height_index] = height_data[height_level]
                            plot_val_temp[temp_height_index] = var_data[height_level]
                            temp_height_index += 1
                            # if the height is not the same as the lower height in the profile
                            # we want to extend the profile before interpolation
                            if lower_height_data[height_level] in height_data:
                                plot_heights_temp[temp_height_index] = lower_height_data[
                                                                           height_level] + height_step_size / 10.
                                plot_val_temp[temp_height_index] = var_data[height_level]
                                temp_height_index += 1
                            else:
                                plot_heights_temp[temp_height_index] = lower_height_data[height_level]
                                plot_val_temp[temp_height_index] = var_data[height_level]
                                temp_height_index += 1
                                if height_level < len(height_data) - 1:
                                    plot_heights_temp[temp_height_index] = lower_height_data[
                                                                               height_level] - height_step_size / 10.
                                    plot_val_temp[temp_height_index] = filling_zero_val
                                    temp_height_index += 1
                                    zero_filled_flag = True

                        plot_heights_temp = plot_heights_temp[0:temp_height_index]
                        plot_val_temp = plot_val_temp[0:temp_height_index]
                        height_data = plot_heights_temp[0:temp_height_index]
                        var_data = plot_val_temp[0:temp_height_index]
                        pass

                    try:
                        # f = interpolate.interp1d(height_data, var_data, kind='nearest', bounds_error=False,
                        #                          fill_value=0.)
                        f = interpolate.interp1d(height_data, var_data, kind='nearest', bounds_error=False,
                                                 fill_value=np.nan)
                        interpolated = f(target_heights)
                        out_arr[time_step_idx, :] = interpolated
                    except ValueError:

                        # this happens when height_data and var_data have only one entry
                        # set out_arr[time_step_idx,:] to NaN in this case for now
                        # breakpoint()
                        out_arr[time_step_idx, :] = np.nan

                # if nansum > 0:
                #     height_data = _data[time_index_dict[unique_time],self.INDEX_DICT[self._ALTITUDENAME]]
                #     lower_height_data = _data[time_index_dict[unique_time],self.INDEX_DICT[self._UPPERALTITUDENAME]]
                #     if np.isnan(np.sum(var_data)):
                #         height_data = height_data[~plot_data_masks[var][time_index_dict[unique_time]]]
                #         lower_height_data = lower_height_data[~plot_data_masks[var][time_index_dict[unique_time]]]
                #         var_data = var_data[~plot_data_masks[var][time_index_dict[unique_time]]]
                #
                #     # add some point around the altitude edges to make the finer nearest neighbour interpolation
                #     plot_heights_temp = np.zeros(intermediate_height_no)
                #     plot_val_temp = np.zeros(intermediate_height_no)
                #     temp_height_index = 0
                #     for height_level in range(len(height_data)):
                #         if np.isnan(lower_height_data[height_level]):
                #             plot_heights_temp[temp_height_index] = height_data[height_level] - 250. - height_step_size
                #             plot_heights_temp[temp_height_index + 1] = height_data[height_level] - 250.
                #         else:
                #             plot_heights_temp[temp_height_index] = lower_height_data[height_level] - height_step_size
                #             plot_heights_temp[temp_height_index + 1] = lower_height_data[height_level]
                #
                #         plot_val_temp[temp_height_index] = filling_zero_val
                #         plot_val_temp[temp_height_index + 1] = var_data[height_level]
                #         temp_height_index += 2
                #
                #         plot_heights_temp[temp_height_index] = height_data[height_level]
                #         plot_val_temp[temp_height_index] = var_data[height_level]
                #         temp_height_index += 1
                #         plot_heights_temp[temp_height_index] = height_data[height_level] + height_step_size
                #         plot_val_temp[temp_height_index] = filling_zero_val
                #
                #         temp_height_index += 1
                #
                #     plot_heights_temp = plot_heights_temp[0:temp_height_index]
                #     plot_val_temp = plot_val_temp[0:temp_height_index]
                #     try:
                #         # f = interpolate.interp1d(height_data, var_data, kind='nearest', bounds_error=False, fill_value=np.nan)
                #         f = interpolate.interp1d(plot_heights_temp, plot_val_temp, kind='nearest', bounds_error=False, fill_value=np.nan)
                #         interpolated = f(target_heights)
                #         out_arr[time_step_idx,:] = interpolated
                #     except ValueError:
                #         #out_arr is np.nan already
                #         pass
                #
                elif nansum == 0:
                    # set all heights of the plotted profile to 0 since nothing was detected
                    out_arr[time_step_idx,:] = 0.

            # enable TeX
            # plt.rc('text', usetex=True)
            # plt.rc('font', family='serif')
            fig, _axs = plt.subplots(nrows=1, ncols=1)
            fig.subplots_adjust(hspace=0.3)
            try:
                axs = _axs.flatten()
            except:
                axs = [_axs]

            # levels = MaxNLocator(nbins=15).tick_values(np.nanmin(out_arr), np.nanmax(out_arr))
            levels = MaxNLocator(nbins=plot_nbins).tick_values(plot_range[0],plot_range[1])
            # cmap = plt.get_cmap('PiYG')
            # cmap = plt.get_cmap('jet')
            # cmap = plt.get_cmap('YlOrRd')
            cmap = plt.get_cmap('autumn_r')
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

            # plot_simple2 = axs[0].pcolormesh(out_arr.transpose(), cmap='jet', vmin=2., vmax=2000.)
            plot_simple2 = axs[0].pcolormesh(out_arr.transpose(), cmap=cmap, norm=norm)
            plot_simple2.axes.set_xlabel('time step number',fontsize='small')

            plot_simple2.axes.set_ylabel('height [km]',fontsize='small')
            yticks = plot_simple2.axes.get_yticks()

            yticklabels = plot_simple2.axes.set_yticklabels(yticks/100.)
            # yticklabels = plot_simple2.axes.set_yticklabels(['0','5', '10', '15', '20'])
            if title:
                plot_simple2.axes.set_title(title, fontsize='xx-small')
            else:
                plot_simple2.axes.set_title('title')
            #plot_simple2.axes.set_aspect(0.05)
            # plt.show()
            clb = plt.colorbar(plot_simple2, ax=axs[0], orientation='horizontal',
                               pad=0.2, aspect=30, anchor=(0.5, 0.8))
            if retrieval_name:
                clb.ax.set_title('{} [{}] {} retrieval'.format(var, self.TEX_UNITS[var], retrieval_name), fontsize='xx-small')
            else:
                clb.ax.set_title('{} [{}]'.format(var, self.TEX_UNITS[var]), fontsize='xx-small')

            fig.tight_layout()
            # put the start and end time as string on the plot
            # plt.text(0.001, 0.02, '{}'.format(unique_times[0].astype('datetime64[s]')), transform=axs[0].transAxes, fontsize=12)
            plt.annotate('start={}'.format(unique_times[0].astype('datetime64[s]')),
                         (0.05, 0.27),
                         xycoords='figure fraction',
                         fontsize=9,
                         horizontalalignment='left')
            plt.annotate('end={}'.format(unique_times[-1].astype('datetime64[s]')),
                         (0.98, 0.27),
                         xycoords='figure fraction',
                         fontsize=9,
                         horizontalalignment='right')
            plt.annotate('max val={0:.2f}'.format(np.nanmax(out_arr)),
                         (0.98, 0.24),
                         xycoords='figure fraction',
                         fontsize=9,
                         horizontalalignment='right')
            plt.annotate('median val={0:.2f}'.format(np.nanmedian(out_arr)),
                         (0.05, 0.24),
                         xycoords='figure fraction',
                         fontsize=9,
                         horizontalalignment='left')

            plt.savefig(plotfilename, dpi=300)
            plt.close()
            # print('test')

    ###################################################################################
    def plot_profile_v3(self, plotfilename, data_to_plot=None, vars_to_plot = ['ec355aer'], retrieval_name=None,
                        title=None,
                        plot_range=(0.,2000.),
                        plot_nbins=20.,
                        colorbar='coolwarm',
                        linear_time=False):
        """plot sample profile plot

        """
        import matplotlib.pyplot as plt
        import matplotlib
        from matplotlib.colors import BoundaryNorm
        from matplotlib.ticker import MaxNLocator

        from scipy import interpolate

        if data_to_plot is None:
            _data = self.data
        else:
            try:
                _data = data_to_plot._data
            except AttributeError:
                _data = data_to_plot

        # read returning a ndarray
        times = _data[:,obj._TIMEINDEX]
        times_no = len(times)
        plot_data = {}
        plot_data_masks = {}
        unique_times = np.unique(times)
        time_step_no = len(unique_times)
        vars_to_plot_arr = [self._ALTITUDENAME]
        vars_to_plot_arr.extend(vars_to_plot)
        filling_zero_val = 0.
        filling_zero_val = -1.E6
        plotting_zero_val = np.nan

        target_height_no = 2001
        intermediate_height_no = 50
        # height step size in m for plotting
        height_step_size = 10.
        target_heights = np.arange(0, target_height_no)*height_step_size
        #target_heights = np.flip(target_heights)
        target_x = np.arange(0,time_step_no)

        for data_var in vars_to_plot_arr:
            # plot_data[data_var] = \
            #     _data[:, self.INDEX_DICT[data_var]]
            plot_data_masks[data_var] = np.isnan(_data[:, self.INDEX_DICT[data_var]])

        # because of height individual quality flags, there will never be all the height steps
        # of a profile in _data.
        # Therefore the number of height steps per time code is not necessarily equal
        # to self._HEIGHTSTEPNO anymore
        # e.g. due to an area based selection or due to NaNs in the profile
        # we therefore have to go through the times and look for changes

        idx_time = times[0]
        time_cut_start_index = 0
        time_cut_end_index = 0
        time_index_dict = {}

        # reconstruct the aeolus profile to cover all height steps so that the nearest neighbour interpolation
        # used for the plot is correct.
        # unfortunately we don't even know all the height levels in the profile because they
        # might not be retrievable or the lower height might be NaN
        # interpolate the existing time steps to a 250m grid (assuming this 250m as the minimum height)

        for idx, time in enumerate(times):
            if time == idx_time:
                time_cut_end_index = idx
            else:
                time_cut_end_index = idx
                time_index_dict[idx_time] = np.arange(time_cut_start_index, time_cut_end_index )
                time_cut_start_index = idx
                idx_time = time

        time_index_dict[idx_time] = np.arange(time_cut_start_index, time_cut_end_index + 1)

        for var in vars_to_plot:
            # this loop has not been optimised for several variables
            out_arr = np.zeros([time_step_no, target_height_no])
            out_arr[:] = np.nan
            for time_step_idx, unique_time in enumerate(unique_times):
                var_data = _data[time_index_dict[unique_time],self.INDEX_DICT[var]]
                # scipy.interpolate cannot cope with nans in the data
                # work only on profiles with a nansum > 0

                nansum = np.nansum(var_data)
                # if np.isnan(nansum):
                #     self.logger.info('time index {} nansum is NaN:'.format(time_step_idx))
                #     # potentially remove profile time...
                # if time_step_idx == 75:
                #     self.logger.info('time index {} nansum is NaN:'.format(time_step_idx))

                # if nansum > 0:
                if np.isfinite(nansum):
                    # if nansum > 0 and len(var_data) > 1:
                    height_data = _data[time_index_dict[unique_time], self.INDEX_DICT[self._ALTITUDENAME]]
                    if np.isnan(np.sum(var_data)):
                        # lower_height_data = lower_height_data[~plot_data_masks[var][time_index_dict[unique_time]]]
                        height_data = height_data[~plot_data_masks[var][time_index_dict[unique_time]]]
                        var_data = var_data[~plot_data_masks[var][time_index_dict[unique_time]]]

                    if len(height_data) < 10.:
                        try:
                            lower_height_data = _data[time_index_dict[unique_time], self.INDEX_DICT[self._UPPERALTITUDENAME]]
                        except TypeError:
                            pass

                        if np.isnan(np.sum(var_data)):
                            lower_height_data = lower_height_data[~plot_data_masks[var][time_index_dict[unique_time]]]

                        # make sure that gaps in the input profile are also present in the profile created by
                        # a nearest neighbour interpolation (used for better looking plots)
                        plot_heights_temp = np.zeros(intermediate_height_no)
                        plot_val_temp = np.zeros(intermediate_height_no)
                        temp_height_index = 0
                        zero_filled_flag = False
                        # note that the order of heights is from top to bottom
                        for height_level in range(len(height_data)):
                            # if the former height level has been surrounded by filling_zero_val
                            # we also have to surround the actual height with filling_zero_val
                            # to make the nearest neighbour interpolation right
                            if zero_filled_flag:
                                zero_filled_flag = False
                                plot_heights_temp[temp_height_index] = height_data[height_level] + height_step_size
                                plot_val_temp[temp_height_index] = filling_zero_val
                                temp_height_index += 1

                            plot_heights_temp[temp_height_index] = height_data[height_level]
                            plot_val_temp[temp_height_index] = var_data[height_level]
                            temp_height_index += 1
                            # if the height is not the same as the lower height in the profile
                            # we want to extend the profile before interpolation
                            if lower_height_data[height_level] in height_data:
                                plot_heights_temp[temp_height_index] = lower_height_data[
                                                                           height_level] + height_step_size / 10.
                                plot_val_temp[temp_height_index] = var_data[height_level]
                                temp_height_index += 1
                            else:
                                plot_heights_temp[temp_height_index] = lower_height_data[height_level]
                                plot_val_temp[temp_height_index] = var_data[height_level]
                                temp_height_index += 1
                                if height_level < len(height_data) - 1:
                                    plot_heights_temp[temp_height_index] = lower_height_data[
                                                                               height_level] - height_step_size / 10.
                                    plot_val_temp[temp_height_index] = filling_zero_val
                                    temp_height_index += 1
                                    zero_filled_flag = True

                        plot_heights_temp = plot_heights_temp[0:temp_height_index]
                        plot_val_temp = plot_val_temp[0:temp_height_index]
                        height_data = plot_heights_temp[0:temp_height_index]
                        var_data = plot_val_temp[0:temp_height_index]
                        pass

                    try:
                        # f = interpolate.interp1d(height_data, var_data, kind='nearest', bounds_error=False,
                        #                          fill_value=0.)
                        f = interpolate.interp1d(height_data, var_data, kind='nearest', bounds_error=False,
                                                 fill_value=np.nan)
                        interpolated = f(target_heights)
                        out_arr[time_step_idx, :] = interpolated
                    except ValueError:

                        # this happens when height_data and var_data have only one entry
                        # set out_arr[time_step_idx,:] to NaN in this case for now
                        # breakpoint()
                        out_arr[time_step_idx, :] = np.nan

                elif nansum == 0:
                    # set all heights of the plotted profile to 0 since nothing was detected
                    out_arr[time_step_idx,:] = 0.

                # elif len(var_data) == 1:
                #     pass

            # now remove the very negative values used to make the interpolation work
            out_arr[np.where(out_arr == filling_zero_val)] = np.nan
            # enable TeX
            # plt.rc('text', usetex=True)
            # plt.rc('font', family='serif')
            fig, _axs = plt.subplots(nrows=1, ncols=1)
            fig.subplots_adjust(hspace=0.3)
            try:
                axs = _axs.flatten()
            except:
                axs = [_axs]

            # levels = MaxNLocator(nbins=15).tick_values(np.nanmin(out_arr), np.nanmax(out_arr))
            levels = MaxNLocator(nbins=plot_nbins).tick_values(plot_range[0],plot_range[1])
            # cmap = plt.get_cmap('PiYG')
            # cmap = plt.get_cmap('jet')
            # cmap = plt.get_cmap('YlOrRd')
            # cmap = plt.get_cmap('coolwarm')
            cmap = plt.get_cmap(colorbar)
            norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

            # plot_simple2 = axs[0].pcolormesh(out_arr.transpose(), cmap='jet', vmin=2., vmax=2000.)
            plot_simple2 = axs[0].pcolormesh(out_arr.transpose(), cmap=cmap, norm=norm)
            clb = plt.colorbar(plot_simple2, ax=axs[0], orientation='horizontal',
                               pad=0.2, aspect=30, anchor=(0.5, 0.8))
            plot_simple2.axes.set_xlabel('time step number',fontsize='small')

            plot_simple2.axes.set_ylabel('height [km]',fontsize='small')
            yticks = plot_simple2.axes.get_yticks()

            yticklabels = plot_simple2.axes.set_yticklabels(yticks/100.)
            # yticklabels = plot_simple2.axes.set_yticklabels(['0','5', '10', '15', '20'])
            if title:
                plot_simple2.axes.set_title(title, fontsize='xx-small')
            else:
                plot_simple2.axes.set_title('title')
            #plot_simple2.axes.set_aspect(0.05)
            # plt.show()
            if retrieval_name:
                clb.ax.set_title('{} [{}] {} retrieval'.format(var, self.TEX_UNITS[var], retrieval_name), fontsize='xx-small')
            else:
                clb.ax.set_title('{} [{}]'.format(var, self.TEX_UNITS[var]), fontsize='xx-small')

            # fig.tight_layout()
            # put the start and end time as string on the plot
            # plt.text(0.001, 0.02, '{}'.format(unique_times[0].astype('datetime64[s]')), transform=axs[0].transAxes, fontsize=12)
            plt.annotate('start={}'.format(unique_times[0].astype('datetime64[s]')),
                         (0.05, 0.27),
                         xycoords='figure fraction',
                         fontsize=9,
                         horizontalalignment='left')
            plt.annotate('end={}'.format(unique_times[-1].astype('datetime64[s]')),
                         (0.98, 0.27),
                         xycoords='figure fraction',
                         fontsize=9,
                         horizontalalignment='right')
            plt.annotate('max val={0:.2f}'.format(np.nanmax(out_arr)),
                         (0.98, 0.24),
                         xycoords='figure fraction',
                         fontsize=9,
                         horizontalalignment='right')
            plt.annotate('median val={0:.2f}'.format(np.nanmedian(out_arr)),
                         (0.05, 0.24),
                         xycoords='figure fraction',
                         fontsize=9,
                         horizontalalignment='left')

            plt.savefig(plotfilename, dpi=300)
            plt.close()
            # print('test')

    ###################################################################################
    def to_grid(self, data=None, vars=None, gridtype='1x1', engine='python', return_data_for_gridding=False,
                grid_heights=None, grid_heights_low=None, grid_heights_high=None, grid_field=None, levelno=20):
        """3d gridding routine that uses the 2d gridding from the super class for level wise 2d gridding

        input data is a 2d numpy array
        """

        if data is None:
            _data = self.data
        else:
            _data = data

        if grid_heights is not None:
            # user defined middle points
            # pass this for now
            pass
        else:
            if grid_heights_low is None:
                grid_heights_low = np.arange(levelno+1) * 1000.
            if grid_heights_high is None:
                grid_heights_high = (np.arange(levelno+1) + 1) * 1000.

        if gridtype not in self.SUPPORTED_GRIDS:
            temp = 'Error: Unknown grid: {}'.format(gridtype)
            self.logger.error(temp)
            return
        lat_verbose_flag = False

        if engine == 'python':
            grid_heights=grid_heights_low[:-1] + (grid_heights_low[1:]-grid_heights_low[:-1])/2
            data_for_gridding, gridded_var_data = \
                self._to_grid_grid_init(gridtype=gridtype, vars=vars ,levels=grid_heights,
                                        init_time=np.mean(_data[:,self._TIMEINDEX]))

            gridded_var_data[self._ALTBOUNDSNAME] = np.transpose(np.array(
                [grid_heights_low[0:len(grid_heights)], grid_heights_high[0:len(grid_heights)]]))
            grid_lats = self.SUPPORTED_GRIDS[gridtype]['grid_lats']
            grid_lons = self.SUPPORTED_GRIDS[gridtype]['grid_lons']
            grid_dist_lat = self.SUPPORTED_GRIDS[gridtype]['grid_dist_lat']
            grid_dist_lon = self.SUPPORTED_GRIDS[gridtype]['grid_dist_lon']

            start_time = time.perf_counter()
            matching_points = 0
            neg_points = 0
            # predefine the output data dict
            # data_for_gridding = {}
            matched_heights = 0
            matched_longitudes = 0
            matched_latitudes = 0
            match_lon_data = []
            match_lat_data = []

            for height_idx, grid_height in enumerate(grid_heights_low):
                diff_height = _data[:,self._ALTITUDEINDEX] - grid_height
                max_allowed_height_dist = grid_heights_high[height_idx] - grid_height
                # height_match_indexes = np.squeeze(np.where(diff_height <= max_allowed_height_dist))
                height_match_indexes = np.where((diff_height <= max_allowed_height_dist) & (diff_height > 0.))[0]
                matched_heights += height_match_indexes.size
                if height_match_indexes.size < self.MIN_VAL_NO_FOR_GRIDDING:
                    continue
                print('height: {}, matched indexes: {}'.format(grid_height, height_match_indexes.size))
                # data_temp = _data[height_match_indexes,:]
                for lat_idx, grid_lat in enumerate(grid_lats):
                    diff_lat = np.absolute((_data[height_match_indexes,self._LATINDEX] - grid_lat))
                    lat_match_indexes = np.where(diff_lat <= (grid_dist_lat/2.))[0]
                    matched_latitudes += lat_match_indexes.size
                    if lat_verbose_flag:
                        print('lat: {}, matched indexes: {}'.format(grid_lat, lat_match_indexes.size))
                    if lat_match_indexes.size < self.MIN_VAL_NO_FOR_GRIDDING:
                        continue
                    # simplify code for readability
                    match_indexes = height_match_indexes[lat_match_indexes]
                    match_lat_data.extend(_data[match_indexes,self._LATINDEX])

                    for lon_idx, grid_lon in enumerate(grid_lons):
                        # diff_lon = np.absolute((_data[match_indexes, self._LONINDEX] - grid_lon))
                        # lon_match_indexes = np.squeeze(np.where(diff_lon <= (grid_dist_lon/2.)))
                        # lon_match_indexes = np.where(diff_lon <= (grid_dist_lon/2.))[0]

                        lon_match_indexes = np.where((_data[match_indexes, self._LONINDEX] > (grid_lon - grid_dist_lon/2.))
                                                      & (_data[match_indexes, self._LONINDEX] <= (grid_lon + grid_dist_lon/2.)))[0]

                        matched_longitudes += lon_match_indexes.size
                        if lon_match_indexes.size < self.MIN_VAL_NO_FOR_GRIDDING:
                            continue
                        match_indexes = match_indexes[lon_match_indexes]
                        # print('lon {}, matched {}'.format(grid_lon, _data[match_indexes, self._LONINDEX]))
                        match_lon_data.extend(_data[match_indexes, self._LONINDEX])

                        for var in vars:
                            less_than_zero_indexes = np.where(_data[match_indexes,self.INDEX_DICT[var]] > 0.)[0]
                            neg_points += (match_indexes.size - less_than_zero_indexes.size)
                            if less_than_zero_indexes.size < self.MIN_VAL_NO_FOR_GRIDDING:
                                continue

                            if return_data_for_gridding:
                                data_for_gridding[var][grid_lat][grid_lon][height_idx] = \
                                    np.array(_data[self._LONGITUDENAME].data[match_indexes[less_than_zero_indexes]])

                            if less_than_zero_indexes.size == 1:
                                try:
                                    gridded_var_data[var]['mean'][lat_idx, lon_idx, height_idx] = \
                                        _data[match_indexes[less_than_zero_indexes], self.INDEX_DICT[var]]
                                    gridded_var_data[var]['stddev'][lat_idx, lon_idx, height_idx] = 0.
                                    gridded_var_data[var]['numobs'][lat_idx, lon_idx, height_idx] = 1.
                                    matching_points += 1
                                except ValueError:
                                    pass
                            else:
                                try:
                                    gridded_var_data[var]['mean'][lat_idx, lon_idx, height_idx] = \
                                        np.nanmean(_data[match_indexes[less_than_zero_indexes], self.INDEX_DICT[var]])
                                    gridded_var_data[var]['stddev'][lat_idx, lon_idx, height_idx] = \
                                        np.nanstd(_data[match_indexes[less_than_zero_indexes], self.INDEX_DICT[var]])
                                    gridded_var_data[var]['numobs'][lat_idx, lon_idx, height_idx] = \
                                        _data[match_indexes[less_than_zero_indexes], self.INDEX_DICT[var]].size
                                    matching_points = matching_points + \
                                                      _data[match_indexes[less_than_zero_indexes], self.INDEX_DICT[var]].size
                                except IndexError:
                                    continue

            end_time = time.perf_counter()
            elapsed_sec = end_time - start_time
            temp = 'time for global {} gridding with python data types [s]: {:.3f}'.format(gridtype, elapsed_sec)
            self.logger.info(temp)
            temp = 'matched {} points out of {} existing points to grid'.format(matching_points, _data.shape[0])
            self.logger.info(temp)
            temp = '{} points were negative'.format(neg_points)

            self.logger.info(temp)
            temp = 'matched heights: {}; matched latitudes {}; matched longitude {}'.format(
                matched_heights, matched_latitudes, matched_longitudes)
            self.logger.info(temp)
            if return_data_for_gridding:
                self.logger.info('returning also data_for_gridding...')
                return gridded_var_data, data_for_gridding
            else:
                return gridded_var_data

        else:
            pass

    ###################################################################################

    def _to_grid_grid_init(self,gridtype=None,vars=None,init_time=None,
                           levelno=None, levels=None,
                           latitudes=None, latno=None,
                           longitudes=None, lonno=None,
                           times=None, timeno=None,
                           return_gridding_data_struct=False):
        """small helper routine to init the 3d grid data struct"""

        import numpy as np
        grid_data_prot = {}
        gridded_var_data = {}
        data_for_gridding = {}

        try:
            dummy = levels.any()
            if dummy:
                levelno = len(levels)
            else:
                levels = np.arange(levelno)
        except AttributeError:
            levels = np.arange(levelno)

        if latitudes.any():
            latno = len(latitudes)

        if longitudes.any():
            lonno = len(longitudes)

        try:
            timeno = len(times)
        except:
            pass

        if levelno is None or levelno == 1 or levelno == 0:
            super()._to_grid_grid_init(gridtype=gridtype,vars=vars,init_time=init_time)
        else:

            import time

            start_time = time.perf_counter()

            # predifined static grid, one time step
            if gridtype in self.SUPPORTED_GRIDS:
                temp = 'starting simple gridding for {} grid...'.format(gridtype)
                self.logger.info(temp)

                latitudes = self.SUPPORTED_GRIDS[gridtype]['grid_lats']
                longitudes = self.SUPPORTED_GRIDS[gridtype]['grid_lons']
                grid_array_prot = np.full((self.SUPPORTED_GRIDS[gridtype]['grid_lats'].size,
                                           self.SUPPORTED_GRIDS[gridtype]['grid_lons'].size,
                                           levelno), np.nan)
                # organise the data in a nested python dict like dict_data[level][grid_lat][grid_lon]=np.ndarray
                for grid_lat in self.SUPPORTED_GRIDS[gridtype]['grid_lats']:
                    grid_data_prot[grid_lat] = {}
                    for grid_lon in self.SUPPORTED_GRIDS[gridtype]['grid_lons']:
                        grid_data_prot[grid_lat][grid_lon] = {}

                pass
            else:
                # model grid; just dimensions
                temp = 'starting simple gridding for given grid with dims ({},{},{})...'.format(levelno, latno, lonno)
                self.logger.info(temp)

                grid_array_prot = np.full((timeno, levelno, latno, lonno,), np.nan)
                # organise the data in a nested python dict like dict_data[level][grid_lat][grid_lon]=np.ndarray
                if return_gridding_data_struct:
                    for time in times:
                        grid_data_prot[time] = {}
                        for grid_lat in latitudes:
                            grid_data_prot[time][grid_lat] = {}
                            for grid_lon in longitudes:
                                grid_data_prot[time][grid_lat][grid_lon] = {}
                                for level in levels:
                                    grid_data_prot[time][grid_lat][grid_lon][level] = {}

            end_time = time.perf_counter()
            elapsed_sec = end_time - start_time
            temp = 'time for global {} gridding with python data types [s] init: {:.3f}'.format(gridtype, elapsed_sec)
            self.logger.info(temp)

            # predefine the output data dict
            if latitudes.any():
                gridded_var_data[self._LATITUDENAME] = latitudes
            if longitudes.any():
                gridded_var_data[self._LONGITUDENAME] = longitudes
            # th exact levels are not known at this point, just the number
            if levels.any():
                gridded_var_data[self._ALTITUDENAME] = levels
            try:
                gridded_var_data[self._TIME_NAME] = times
            except:
                gridded_var_data[self._TIME_NAME] = init_time
            for var in vars:
                data_for_gridding[var] = grid_data_prot.copy()
                gridded_var_data[var] = {}
                gridded_var_data[var]['mean'] = grid_array_prot.copy()
                gridded_var_data[var]['stddev'] = grid_array_prot.copy()
                gridded_var_data[var]['numobs'] = grid_array_prot.copy()

        if return_gridding_data_struct:
            return data_for_gridding, \
                   gridded_var_data,
        else:
            return gridded_var_data

    ###################################################################################
    def read_model_file(self, file_name, topofile=None, vars_to_keep=None):
        """method to read a EMEP model file for colocation using xarray

        :param filename:
        file to read
        :param topofile:
        topography file; heights will be added to altitudes if provided
        """
        pass
        import xarray as xr

        if topofile is not None:
            # read topography since that needs to be added to the ground following height of the model
            self.logger.info('reading topography file {}'.format(options['topofile']))
            topo_data = xr.open_dataset(options['topofile'])
            topo_altitudes = np.squeeze(topo_data[self.EMEP_TOPO_FILE_VAR_NAME])
            topo_data.close()

        if not os.path.exists(file_name):
            obj.logger.info('file does not exist: {}. skipping colocation ...'.format(file_name))
            return False
        # read netcdf file if it has not yet been loaded
        obj.logger.info('reading model file {}'.format(file_name))
        nc_data = xr.open_dataset(file_name)
        nc_data[self._LATITUDENAME] = nc_data[self.EMEP_VAR_NAME_DICT[self._LATITUDENAME]]
        nc_data[self._LONGITUDENAME] = nc_data[self.EMEP_VAR_NAME_DICT[self._LONGITUDENAME]]
        nc_data[self._TIME_NAME] = nc_data[self.EMEP_VAR_NAME_DICT[self._TIME_NAME]]
        nc_data[self._ALTITUDENAME] = nc_data[self.EMEP_VAR_NAME_DICT[self._ALTITUDENAME]]

        if topofile is not None:
            # topography needs to be added to all the heighlevels and time steps
            for time_idx, _time in enumerate(nc_data[self.EMEP_VAR_NAME_DICT[self._TIME_NAME]]):
                for level_idx, level in enumerate(nc_data['lev']):
                    nc_data[self._ALTITUDENAME][time_idx,level_idx,:,:] += topo_altitudes
        # nc_times = nc_data.time.data.astype('datetime64[h]')
        # nc_latitudes = nc_data['lat'].data
        # nc_longitudes = nc_data['lon'].data
        # nc_lev_no = len(nc_data['lev'])
        return nc_data

    ###################################################################################
    def to_model_grid(self, data=None, vars=None, engine='python', return_data_for_gridding=False,
                model_data=None):
        """3d gridding routine according to a model level, lat, lon grid (one time step)

        input data is a 2d numpy array with the aeolus data
        model_data is a xarray.Dataset object containing the model data

        """

        if data is None:
            _data = self.data
        else:
            _data = data

        if engine == 'python':
            import time
            lat_verbose_flag = False

            model_levelno = model_data[self._ALTITUDENAME].shape[1]
            ts_no = len(model_data[self.EMEP_VAR_NAME_DICT[self._TIME_NAME]])
            lat_no = len(model_data[self.EMEP_VAR_NAME_DICT[self._LATITUDENAME]])
            lon_no = len(model_data[self.EMEP_VAR_NAME_DICT[self._LONGITUDENAME]])
            grid_lats = model_data[self.EMEP_VAR_NAME_DICT[self._LATITUDENAME]].data
            grid_lons = model_data[self.EMEP_VAR_NAME_DICT[self._LONGITUDENAME]].data
            grid_dist_lat_arr = model_data[self.EMEP_VAR_NAME_DICT[self._LATITUDENAME]].data[1:] - \
                                model_data[self.EMEP_VAR_NAME_DICT[self._LATITUDENAME]].data[:-1]
            grid_dist_lon_arr = model_data[self.EMEP_VAR_NAME_DICT[self._LONGITUDENAME]].data[1:] - \
                                model_data[self.EMEP_VAR_NAME_DICT[self._LONGITUDENAME]].data[:-1]
            grid_dist_lat = grid_dist_lat_arr[0]
            grid_dist_lon = grid_dist_lon_arr[0]
            model_times = model_data[self.EMEP_VAR_NAME_DICT[self._TIME_NAME]].data

            # data_for_gridding_temp, gridded_var_data_temp = \
            if return_data_for_gridding:
                gridded_var_data_temp, gridded_var_data_temp = \
                    self._to_grid_grid_init(vars=vars ,levelno=model_levelno,
                                            latitudes=grid_lats, longitudes=grid_lons,
                                            times=model_times, return_gridding_data_struct=True)
            else:
                gridded_var_data_temp = \
                    self._to_grid_grid_init(vars=vars ,levelno=model_levelno,
                                            latitudes=grid_lats, longitudes=grid_lons,
                                            times=model_times, return_gridding_data_struct=False)

            gridded_var_data = gridded_var_data_temp
            gridded_var_data[self._ALTITUDENAME] = model_data[self._ALTITUDENAME].data.copy()

            data_for_gridding = {}

            start_time = time.perf_counter()
            obs_times = _data[:,self._TIMEINDEX].astype('datetime64[s]').astype('datetime64[h]')
            max_time_diff = np.timedelta64(1,'h')

            matching_points = 0
            neg_points = 0
            matched_times = 0
            matched_heights = 0
            matched_longitudes = 0
            matched_latitudes = 0
            for time_idx, _time in enumerate(model_times):
                match_lon_data = []
                match_lat_data = []
                match_time_data = []
                match_height_data = []
                diff_time = obs_times - _time.astype('datetime64[h]')
                # time_match_indexes = np.where(np.absolute(diff_time <= max_time_diff/2.))[0]
                # time_match_indexes = np.where((diff_time > max_time_diff/-2.) & (diff_time <= max_time_diff/2.))[0]
                # the following works due to the earlier rounding to an hour of obs_times
                time_match_indexes = np.where(diff_time == np.timedelta64(0,'h'))[0]
                if lat_verbose_flag:
                    print('model time: {}, matched indexes: {}'.format(_time.astype('datetime64[h]'), time_match_indexes.size))
                diff_time = None
                if time_match_indexes.size < self.MIN_VAL_NO_FOR_GRIDDING:
                    continue
                matched_times += time_match_indexes.size
                match_indexes = time_match_indexes
                match_time_data.extend(_data[match_indexes, self._TIMEINDEX])

                for lat_idx, grid_lat in enumerate(grid_lats):
                    # diff_lat = np.absolute((_data[match_indexes, self._LATINDEX] - grid_lat))
                    # lat_match_indexes = np.where(diff_lat <= (grid_dist_lat / 2.))[0]
                    lat_min = grid_lat - grid_dist_lat / 2.
                    lat_max = grid_lat + grid_dist_lat / 2.
                    lat_match_indexes = np.where((_data[time_match_indexes, self._LATINDEX] > lat_min) &
                                                 (_data[time_match_indexes, self._LATINDEX] <= lat_max))[0]
                    # diff_lat = None
                    if lat_verbose_flag:
                        print('lat: {}, matched indexes: {}'.format(grid_lat, lat_match_indexes.size))
                    if lat_match_indexes.size < self.MIN_VAL_NO_FOR_GRIDDING:
                        continue
                    matched_latitudes += lat_match_indexes.size
                    # simplify code for readability
                    lat_match_indexes = time_match_indexes[lat_match_indexes]
                    match_lat_data.extend(_data[lat_match_indexes, self._LATINDEX])

                    for lon_idx, grid_lon in enumerate(grid_lons):
                        # diff_lon = np.absolute((_data[match_indexes, self._LONINDEX] - grid_lon))
                        # lon_match_indexes = np.where(diff_lon <= (grid_dist_lon / 2.))[0]
                        lon_min = grid_lon - grid_dist_lon / 2.
                        lon_max = grid_lon + grid_dist_lon / 2.
                        lon_match_indexes = np.where((_data[lat_match_indexes, self._LONINDEX] > lon_min) &
                                                     (_data[lat_match_indexes, self._LONINDEX] <= lon_max))[0]
                        # diff_lon = None

                        if lon_match_indexes.size < self.MIN_VAL_NO_FOR_GRIDDING:
                            continue
                        matched_longitudes += lon_match_indexes.size
                        lon_match_indexes = lat_match_indexes[lon_match_indexes]
                        match_lon_data.extend(_data[lon_match_indexes, self._LONINDEX])

                        if lat_verbose_flag:
                            print('lon {}, matched {}'.format(grid_lon, _data[lon_match_indexes, self._LONINDEX]))
                            print('lat {}, lon {}, heights {}'.format(
                                _data[lon_match_indexes, self._LATINDEX], _data[lon_match_indexes, self._LONINDEX],
                                _data[lon_match_indexes,self._ALTITUDEINDEX]))

                        model_height = model_data[self.EMEP_VAR_NAME_DICT[self._ALTITUDENAME]].data[time_idx,:, lat_idx, lon_idx]
                        mean_idx = {}

                        for match_idx, _height in enumerate(_data[lon_match_indexes,self._ALTITUDEINDEX]):
                            diff_height_to_model = np.absolute(model_height - _height)
                            lowest_idx = np.where(diff_height_to_model == np.amin(diff_height_to_model))[0]
                            if lat_verbose_flag:
                                print("lowest height distance: {} m".format(diff_height_to_model[lowest_idx]))
                            # lowest_idx = height index of model
                            # height_idx = index of satellite data
                            try:
                                mean_idx[lowest_idx[0]].append(lon_match_indexes[match_idx])
                            except:
                                mean_idx[lowest_idx[0]] = [lon_match_indexes[match_idx]]

                        # now apply the height index array to the variables and calculate the height means
                        for idx in mean_idx:
                            data_indexes = np.array(mean_idx[idx])
                            for var in vars:
                                greater_than_zero_indexes = np.where(_data[data_indexes,self.INDEX_DICT[var]] > 0.)[0]
                                neg_points += (data_indexes.size - greater_than_zero_indexes.size)
                                if greater_than_zero_indexes.size < self.MIN_VAL_NO_FOR_GRIDDING:
                                    continue
                                greater_than_zero_indexes = lon_match_indexes[greater_than_zero_indexes]
                                # if return_data_for_gridding:
                                #     if not isinstance(data_for_gridding[var], dict):
                                #         data_for_gridding[var] = data_for_gridding_temp.copy()
                                #         data_for_gridding[var][_time][grid_lat][grid_lon][height_idx] = \
                                #             _data[data_indexes[greater_than_zero_indexes], self.INDEX_DICT[var]]

                                if greater_than_zero_indexes.size == 1:
                                    try:
                                        gridded_var_data[var]['mean'][time_idx, idx, lat_idx, lon_idx] = \
                                            _data[greater_than_zero_indexes, self.INDEX_DICT[var]]
                                        gridded_var_data[var]['stddev'][time_idx, idx, lat_idx, lon_idx] = np.nan
                                        gridded_var_data[var]['numobs'][time_idx, idx, lat_idx, lon_idx] = 1.
                                        matching_points += 1
                                        if lat_verbose_flag:
                                            print('val: {}'.format(_data[greater_than_zero_indexes, self.INDEX_DICT[var]]))
                                    except ValueError:
                                        pass
                                else:
                                    try:
                                        gridded_var_data[var]['mean'][time_idx, idx, lat_idx, lon_idx] = \
                                            np.nanmean(_data[greater_than_zero_indexes, self.INDEX_DICT[var]])
                                        gridded_var_data[var]['stddev'][time_idx, idx, lat_idx, lon_idx] = \
                                            np.nanstd(_data[greater_than_zero_indexes, self.INDEX_DICT[var]])
                                        gridded_var_data[var]['numobs'][time_idx, idx, lat_idx, lon_idx] = \
                                            greater_than_zero_indexes.size
                                        matching_points = matching_points + greater_than_zero_indexes.size
                                        if lat_verbose_flag:
                                            print('val: {}'.format(
                                                _data[greater_than_zero_indexes, self.INDEX_DICT[var]]))

                                    except IndexError:
                                        continue

            end_time = time.perf_counter()
            elapsed_sec = end_time - start_time
            temp = 'time for gridding to model grid with python data types [s]: {:.3f}'.format(elapsed_sec)
            self.logger.info(temp)
            temp = 'matched {} points out of {} existing points to grid'.format(matching_points, _data.shape[0])
            self.logger.info(temp)
            temp = '{} points were negative'.format(neg_points)
            self.logger.info(temp)
            # temp = 'matched heights: {}; matched latitudes {}; matched longitude {}'.format(
            #     matched_heights, matched_latitudes, matched_longitudes)
            # self.logger.info(temp)
            if return_data_for_gridding:
                self.logger.info('returning also data_for_gridding...')
                return gridded_var_data, data_for_gridding
            else:
                return gridded_var_data

        else:
            pass

    ###################################################################################
    # def

if __name__ == '__main__':
    import logging

    import argparse
    options = {}
    default_topo_file = '/lustre/storeB/project/fou/kl/admaeolus/EMEP.topo/MACC14_topo_v1.nc'

    obj = ReadL2Data(verbose=True)
    SUPPORTED_GRIDS = obj.SUPPORTED_GRIDS.keys()
    DEFAULT_GRID = 'MODEL'

    netcdf_indir = '/lustre/storeB/project/fou/kl/admaeolus/EMEPmodel'

    parser = argparse.ArgumentParser(
        description='command line interface to aeolus2netcdf.py\n\n\n')
    parser.add_argument("--file",
                        help="file(s) to read",nargs="+")
    parser.add_argument("-v", "--verbose", help="switch on verbosity",
                        action='store_true')
    # parser.add_argument("--listpaths", help="list the file contents.", action='store_true')
    # parser.add_argument("--readpaths", help="read listed rootpaths of DBL file. Can be comma separated",
    #                     default='mph,sca_optical_properties')
    parser.add_argument("-o", "--outfile", help="output file")
    parser.add_argument("--outdir",
                        help="output directory; the filename will be extended with the string '.nc'; defaults to './'",
                        default='./')
    parser.add_argument("--logfile", help="logfile; defaults to /home/jang/tmp/aeolus2netcdf.log",
                        default="/home/jang/tmp/aeolus2netcdf.log")
    parser.add_argument("-O", "--overwrite", help="overwrite output file", action='store_true')
    parser.add_argument("--emep", help="flag to limit the read data to the cal/val model domain", action='store_true')
    parser.add_argument("--himalayas", help="flag to limit the read data to himalayas", action='store_true')
    parser.add_argument("--codadef", help="set path of CODA_DEFINITION env variable",
                        default='/lustre/storeA/project/aerocom/aerocom1/ADM_CALIPSO_TEST/')
    parser.add_argument("--latmin", help="min latitude to return", default=np.float_(30.))
    parser.add_argument("--latmax", help="max latitude to return", default=np.float_(76.))
    parser.add_argument("--lonmin", help="min longitude to return", default=np.float_(-30.))
    parser.add_argument("--lonmax", help="max longitude to return", default=np.float_(45.))
    parser.add_argument("--dir", help="work on all files below this directory",
                        default='/lustre/storeB/project/fou/kl/admaeolus/data.rev.2A02/download/AE_OPER_ALD_U_N_2A_*')
    # parser.add_argument("--filemask", help="file mask to find data files",
    #                     default='*AE_OPER_ALD_U_N_2A_*')
    parser.add_argument("--tempdir", help="directory for temporary files",
                        default=os.path.join(os.environ['HOME'], 'tmp'))
    parser.add_argument("--plotmap", help="flag to plot a map of the data points; files will be put in outdir",
                        action='store_true')
    parser.add_argument("--plotprofile", help="flag to plot the profiles; files will be put in outdir",
                        action='store_true')
    parser.add_argument("--variables", help="comma separated list of variables to write; default: ec355aer,bs355aer",
                        default='ec355aer')
    parser.add_argument("--retrieval", help="retrieval to read; supported: sca, ica, mca; default: sca", default='sca')
    parser.add_argument("--netcdfcolocate", help="flag to add L2 colocation with a netcdf file",
                        action='store_true')
    parser.add_argument("--gridfile", help="grid data and write it to given output file (L3 in netcdf).")
    parser.add_argument("--gridname",
                        help="name of the grid used for gridding. Supported grids are {}, defaults to {}. "
                             "MODEL means gridding to model altitude field".format(','.join(SUPPORTED_GRIDS),DEFAULT_GRID),
                        default=DEFAULT_GRID)
    parser.add_argument("--modeloutdir", help="directory for colocated model files; will have a similar filename as input file",
                        default=os.path.join(os.environ['HOME'], 'tmp'))
    parser.add_argument("--topofile", help="topography file; defaults to {}.".format(default_topo_file),
                        default=default_topo_file)
    parser.add_argument("--modelindir", help="model directory for reading; defaults to {}.".format(netcdf_indir),
                        default=netcdf_indir)

    parser.add_argument("--aeoluslistfile", help="text file with input files from aeolus.".format(netcdf_indir))

    args = parser.parse_args()

    if args.netcdfcolocate:
        options['netcdfcolocate'] = True
    else:
        options['netcdfcolocate'] = False

    if args.aeoluslistfile:
        options['aeoluslistfile'] = args.aeoluslistfile

    if args.modelindir:
        options['modelindir'] = args.modelindir

    if args.gridfile:
        options['gridfile'] = args.gridfile

    if args.gridname:
        options['gridname'] = args.gridname
        if options['gridname'] == 'MODEL':
            INTERPOL_TO_MODEL_GRID_FLAG = True
        else:
            INTERPOL_TO_MODEL_GRID_FLAG = False

    try:
        if args.retrieval:
            options['retrieval'] = args.retrieval
    except AttributeError:
        options['retrieval'] = 'sca'

    if args.modeloutdir:
        options['modeloutdir'] = args.modeloutdir

    if args.logfile:
        options['logfile'] = args.logfile
        logging.basicConfig(filename=options['logfile'], level=logging.INFO)

    if args.dir:
        options['dir'] = args.dir

    if args.outdir:
        options['outdir'] = args.outdir

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
        options['latmin'] = float(30.)
        options['latmax'] = float(76.)
        options['lonmin'] = float(-30.)
        options['lonmax'] = float(45.)
    else:
        options['emepflag'] = False

    if args.himalayas:
        options['himalayas'] = args.himalayas
        options['latmin'] = float(10.)
        options['latmax'] = float(50.)
        options['lonmin'] = float(60.)
        options['lonmax'] = float(110.)
    else:
        options['himalayas'] = False

    # if args.readpaths:
    #     options['readpaths'] = args.readpaths.split(',')

    if args.variables:
        options['variables'] = args.variables.split(',')

    if args.file:
        options['files'] = args.file

    try:
        if args.listpaths:
            options['listpaths'] = True
        else:
            options['listpaths'] = False
    except AttributeError:
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

    if args.codadef:
        options['codadef'] = args.codadef

    if args.topofile:
        options['topofile'] = args.topofile

    # import read_data_fieldaeolus_l2a_data
    import os
    os.environ['CODA_DEFINITION'] = options['codadef']
    import coda
    import sys
    import glob
    import pathlib
    import tarfile

    bbox = None
    global_attributes = None

    if 'files' not in options:
        if 'aeoluslistfile' not in options:
            options['files'] = glob.glob(options['dir']+'/**/'+options['filemask'], recursive=True)
        else:
            options['files'] = []
            with open(options['aeoluslistfile']) as fh:
                options['files'] = [line.rstrip('\n') for line in fh]

    for file_idx, filename in enumerate(options['files']):
        print(filename)
        suffix = pathlib.Path(filename).suffix
        temp_file_flag = False
        if suffix == '.TGZ':
            # untar *.DBL file first
            tarhandle = tarfile.open(filename)
            files_in_tar = tarhandle.getnames()
            for file_in_tar in files_in_tar:
                if pathlib.Path(file_in_tar).suffix == '.DBL':
                    # extract file to tmp path
                    member = tarhandle.getmember(file_in_tar)
                    tarhandle.extract(member, path=options['tempdir'],set_attrs=False)
                    filename = os.path.join(options['tempdir'],file_in_tar)
                    tarhandle.close()
                    temp_file_flag = True
                    break
        elif suffix != '.DBL':
            print('ignoring file {}'.format(filename))
            continue

        if options['listpaths']:
            coda_handle = coda.open(filename)
            root_field_names = coda.get_field_names(coda_handle)
            for field in root_field_names:
                print(field)
            coda.close(coda_handle)
        else:
            obj = ReadL2Data(verbose=True)
            # read sca retrieval data
            vars_to_read = options['variables'].copy()
            data_numpy_tmp = obj.read_file(filename, vars_to_retrieve=vars_to_read, return_as='numpy',
                                       read_retrieval=options['retrieval'])
            # obj.ndarr2data(filedata_numpy)
            # read additional data
            if file_idx > 0:
                # append data_numpy_tmp to data_numpy
                data_numpy = np.append(data_numpy, data_numpy_tmp, axis=0)
            else:
                data_numpy = data_numpy_tmp

            ancilliary_data = obj.read_data_fields(filename, fields_to_read=['mph'])
            if temp_file_flag:
                obj.logger.info('removing temp file {}'.format(filename))
                os.remove(filename)

    # apply emep options for cal / val
    if options['emepflag']:
        bbox = [options['latmin'], options['latmax'],options['lonmin'],options['lonmax']]
        tmp_data = obj.select_bbox(data=data_numpy, bbox=bbox)
        if len(tmp_data) > 0:
            data_numpy = tmp_data
            obj.logger.info('file {} contains {} points in emep area! '.format(filename, len(tmp_data)))
        else:
            obj.logger.info('file {} contains no data in emep area! '.format(filename))
            data_numpy = None
            # continue

    if options['himalayas']:
        bbox = [options['latmin'], options['latmax'],options['lonmin'],options['lonmax']]
        tmp_data = obj.select_bbox(data=data_numpy, bbox=bbox)
        if len(tmp_data) > 0:
            data_numpy = tmp_data
            obj.logger.info('file {} contains {} points in himalaya area! '.format(filename, len(tmp_data)))
        else:
            obj.logger.info('file {} contains no data in himalaya area! '.format(filename))
            data_numpy = None
            # continue

    if 'outfile' in options or 'gridfile' in options or 'outdir' in options:
        # if not global_attributes:
        #     global_attributes = {}
        global_attributes = ancilliary_data['mph']
        global_attributes['Aeolus_Retrieval'] = obj.RETRIEVAL_READ
        global_attributes['input files'] = ','.join(obj.files_read)
        global_attributes[
            'info'] = 'file created by pyaerocom.io.read_aeolus_l2a_data ' + obj.__version__ + ' (https://github.com/metno/pyaerocom) at ' + \
                      np.datetime64('now').astype('str')
        global_attributes['quality'] = 'quality flags for extinction applied'

    # single outfile
    if 'outfile' in options:
        if len(options['files']) == 1:
            # write netcdf
            if os.path.exists(options['outfile']):
                if options['overwrite']:
                    obj.to_netcdf_simple(netcdf_filename=options['outfile'], data_to_write=data_numpy,
                                         global_attributes=global_attributes, vars_to_write=[vars_to_read[0], obj._UPPERALTITUDENAME])
                else:
                    sys.stderr.write('Error: path {} exists'.format(options['outfile']))
            else:
                obj.to_netcdf_simple(netcdf_filename=options['outfile'], data_to_write=data_numpy,
                                     global_attributes=global_attributes, vars_to_write=[vars_to_read[0], obj._UPPERALTITUDENAME])
        else:
            sys.stderr.write("error: multiple input files, but only on output file given\n"
                             "Please use the --outdir option instead\n")

    # outdir
    # if 'outdir' in options and 'outfile' not in options:
    #     outfile_name = os.path.join(options['outdir'], os.path.basename(filename) + '.nc')
    #     obj.logger.info('writing file {}'.format(outfile_name))
    #     if os.path.exists(outfile_name):
    #         if options['overwrite']:
    #             obj.to_netcdf_simple(netcdf_filename=outfile_name, data_to_write=data_numpy,
    #                                  global_attributes=global_attributes, vars_to_write=vars_to_read)
    #         else:
    #             sys.stderr.write('Error: file {} exists'.format(options['outfile']))
    #     else:
    #         obj.to_netcdf_simple(netcdf_filename=outfile_name, data_to_write=data_numpy,
    #                              global_attributes=global_attributes, vars_to_write=vars_to_read)
    #

    # work with emep data and do some colocation
    if options['netcdfcolocate']:
        start_time = time.perf_counter()

        netcdf_indir = '/lustre/storeB/project/fou/kl/admaeolus/EMEPmodel'
        import xarray as xr
        # read topography since that needs to be added to the ground following height of the model
        obj.logger.info('reading topography file {}'.format(options['topofile']))
        topo_data = xr.open_dataset(options['topofile'])

        #truncate Aeolus times to hour

        aeolus_times_rounded = data_numpy[:,obj._TIMEINDEX].astype('datetime64[s]').astype('datetime64[h]')
        aeolus_times = data_numpy[:,obj._TIMEINDEX].astype('datetime64[s]')
        unique_aeolus_times, unique_aeolus_time_indexes = np.unique(aeolus_times, return_index=True)
        aeolus_profile_no = len(unique_aeolus_times)
        # aeolus_profile_no = int(len(aeolus_times)/obj._HEIGHTSTEPNO)
        last_netcdf_file = ''
        for time_idx in range(len(unique_aeolus_time_indexes)):
            ae_year, ae_month, ae_dummy = \
                aeolus_times[unique_aeolus_time_indexes[time_idx]].astype('str').split('-')
            ae_day, ae_dummy = ae_dummy.split('T')
            file_name = 'CWF_12ST-{}{}{}_hourInst.nc'.format(ae_year, ae_month, ae_day)
            file_name = os.path.join(netcdf_indir, file_name)
            if not os.path.exists(file_name):
                obj.logger.info('file does not exist: {}. skipping colocation ...'.format(file_name))
                continue
            # read netcdf file if it has not yet been loaded
            if file_name != last_netcdf_file:
                obj.logger.info('reading and co-locating on model file {}'.format(file_name))
                last_netcdf_file = file_name
                nc_data = xr.open_dataset(file_name)
                nc_times = nc_data.time.data.astype('datetime64[h]')
                nc_latitudes = nc_data['lat'].data
                nc_longitudes = nc_data['lon'].data
                nc_lev_no = len(nc_data['lev'])
                nc_colocated_data = np.zeros([aeolus_profile_no * nc_lev_no, obj._COLNO], dtype=np.float_)

            # locate current rounded Aeolus time in netcdf file
            nc_ts_no = np.where(nc_times == unique_aeolus_times[time_idx].astype('datetime64[h]'))
            if len(nc_ts_no) != 1:
                # something is wrong here!
                pass

            # locate current profile's location index in lats and lons
            # Has to be done on original aeolus data
            for aeolus_profile_index in range(aeolus_profile_no):
                data_idx = unique_aeolus_time_indexes[aeolus_profile_index]
                try:
                    data_idx_end = unique_aeolus_time_indexes[aeolus_profile_index+1]
                except:
                    data_idx_end = len(aeolus_times)

                data_idx_arr = np.arange(data_idx_end - data_idx) + data_idx

                aeolus_lat = np.nanmean(data_numpy[data_idx_arr, obj._LATINDEX])
                aeolus_lon = np.nanmean(data_numpy[data_idx_arr, obj._LONINDEX])
                aeolus_altitudes = data_numpy[data_idx_arr, obj._ALTITUDEINDEX]
                diff_dummy = nc_latitudes - aeolus_lat
                min_lat_index = np.argmin(np.abs(diff_dummy))
                diff_dummy = nc_longitudes - aeolus_lon
                min_lon_index = np.argmin(np.abs(diff_dummy))

                nc_data_idx = aeolus_profile_index * nc_lev_no
                nc_index_arr = np.arange(nc_lev_no) + nc_data_idx
                nc_colocated_data[nc_index_arr,obj.INDEX_DICT[obj._EC355NAME]] = \
                    nc_data['EXT_350nm'].data[nc_ts_no,:,min_lat_index,min_lon_index]
                # nc_data['EXT_350nm'].data[nc_ts_no,:,min_lat_index,min_lon_index].reshape(nc_lev_no)
                nc_colocated_data[nc_index_arr,obj._ALTITUDEINDEX] = \
                    nc_data['Z_MID'].data[nc_ts_no,:,min_lat_index,min_lon_index] + \
                    topo_data['topography'].data[0,min_lat_index,min_lon_index]
                nc_colocated_data[nc_index_arr,obj._LATINDEX] = \
                    nc_data['lat'].data[min_lat_index]
                nc_colocated_data[nc_index_arr,obj._LONINDEX] = \
                    nc_data['lon'].data[min_lon_index]
                # nc_data['Z_MID'].data[nc_ts_no,:,min_lat_index,min_lon_index].reshape(nc_lev_no)
                nc_colocated_data[nc_index_arr,obj._TIMEINDEX] = \
                    data_numpy[data_idx, obj._TIMEINDEX]

        end_time = time.perf_counter()
        elapsed_sec = end_time - start_time
        temp = 'time for colocation all time steps [s]: {:.3f}'.format(elapsed_sec)
        if 'nc_colocated_data' in locals():
            obj.logger.info(temp)
            obj.logger.info('{} is colocated model output directory'.format(options['modeloutdir']))
            model_file_name = os.path.join(options['modeloutdir'], os.path.basename(filename) + '.colocated.nc')
            # obj.to_netcdf_simple(model_file_name, data_to_write=nc_colocated_data)
            obj.to_netcdf_simple(netcdf_filename=model_file_name, data_to_write=nc_colocated_data,
                                 vars_to_write=vars_to_read)
        pass

    #plot the profile
    if options['plotprofile']:
        plotfilename = os.path.join(options['outdir'], os.path.basename(filename)
                                    + '.'+options['retrieval']+'.profile.png')
        obj.logger.info('profile plot file: {}'.format(plotfilename))
        # title = '{} {}'.format(options['retrieval'], os.path.basename(filename))
        title = '{}'.format(os.path.basename(filename))
        obj.plot_profile_v3(plotfilename, title=title, data_to_plot=data_numpy,
                            retrieval_name=options['retrieval'],
                            plot_range=(-200,200.),
                            plot_nbins=40)
        # obj.plot_profile_v3(plotfilename, title=title, data_to_plot=data_numpy,
        #                                     retrieval_name=options['retrieval'],
        #                                     plot_range=(0.,200.))

    #plot the map
    if options['plotmap']:
        plotmapfilename = os.path.join(options['outdir'], os.path.basename(filename) + '.map.png')
        obj.logger.info('map plot file: {}'.format(plotmapfilename))
        #title = os.path.basename(filename)
        obj.plot_location_map(plotmapfilename, data=data_numpy, bbox=bbox, title=os.path.basename(filename))
        # obj.plot_location_map(plotmapfilename)

    # write L3 gridded data
    if 'gridfile' in options:
        import xarray as xr
        vars_to_copy = [obj._ALTITUDENAME, obj._LONGITUDENAME, obj._LATITUDENAME, '']
        vars_to_read = options['variables'].copy()
        netcdf_indir = options['modelindir']
        aeolus_times_rounded = data_numpy[:, obj._TIMEINDEX].astype('datetime64[s]').astype('datetime64[h]')
        aeolus_times = data_numpy[:, obj._TIMEINDEX].astype('datetime64[s]')
        unique_aeolus_times, unique_aeolus_time_indexes = np.unique(aeolus_times, return_index=True)
        aeolus_profile_no = len(unique_aeolus_times)
        # aeolus_profile_no = int(len(aeolus_times)/obj._HEIGHTSTEPNO)
        last_netcdf_file = ''
        for time_idx in range(len(unique_aeolus_time_indexes)):
            ae_year, ae_month, ae_dummy = \
                aeolus_times[unique_aeolus_time_indexes[time_idx]].astype('str').split('-')
            ae_day, ae_dummy = ae_dummy.split('T')
            file_name = 'CWF_12ST-{}{}{}_hourInst.nc'.format(ae_year, ae_month, ae_day)
            file_name = os.path.join(netcdf_indir, file_name)
            if not os.path.exists(file_name):
                obj.logger.info('file does not exist: {}. skipping colocation ...'.format(file_name))
                continue
            # read netcdf file if it has not yet been loaded
            if file_name != last_netcdf_file:
                obj.logger.info('reading and preparing model data for gridding file {}'.format(file_name))
                # read model file
                if len(last_netcdf_file) == 0:
                    model_data_temp = obj.read_model_file(file_name, topofile=options['topofile'])
                    model_data = model_data_temp
                else:
                    model_data = xr.concat([model_data, model_data_temp], obj._TIME_NAME, data_vars='minimal')
                last_netcdf_file = file_name

        if INTERPOL_TO_MODEL_GRID_FLAG:
            # grid to model grid with altitude being a 4d field
            gridded_var_data = obj.to_model_grid(data=data_numpy, vars=vars_to_read,
                                                 model_data=model_data)
        else:
            # grid to static grid
            gridded_var_data = obj.to_grid(data=data_numpy, vars=vars_to_read,
                                           gridtype=options['gridname'])

        obj.to_netcdf_simple(netcdf_filename=options['gridfile'],
                             vars_to_write=vars_to_read,
                             global_attributes=global_attributes,
                             data_to_write=gridded_var_data,
                             gridded=True)
