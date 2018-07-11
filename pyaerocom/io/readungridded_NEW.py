#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################
# readoddata.py
#
# observational data reading class
#
# this file is part of the aerocom_pt package
#
#################################################################
# Created 20171024 by Jan Griesfeller for Met Norway
#
# Last changed: See git log
#################################################################

# Copyright (C) 2017 met.no
# Contact information:
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# E-mail: jan.griesfeller@met.no, jonas.gliss@met.no
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


import os
import glob
# import pdb
import numpy as np
import sys
from collections import OrderedDict as od
#from pyaerocom.io.read_aeronet_sdav2 import ReadAeronetSDAV2
from pyaerocom.io.read_aeronet_sdav3 import ReadAeronetSdaV3
from pyaerocom.io.read_aeronet_invv2 import ReadAeronetInvV2
from pyaerocom.io.read_aeronet_sunv2 import ReadAeronetSunV2
from pyaerocom.io.read_aeronet_sunv3 import ReadAeronetSunV3
from pyaerocom.io.read_earlinet import ReadEarlinet

from pyaerocom.utils import _BrowserDict
from pyaerocom import const

class QueryUngridded(_BrowserDict):
    """Query class for specifying obsdata requests"""
    def __init__(self, dataset_to_read, vars_to_read=None):
        self.dataset_to_read = dataset_to_read
        self.vars_to_read = vars_to_read
        
    def __str__(self):
        s=""
        for k, v in self.items():
            s += "{}: {}\n".format(k, v)
        return s 
        
class ReadUngridded:
    """Factory class for reading of ungridded data based on obsnetwork ID
    """

    #SUPPORTED_DATASETS = [const.AERONET_SUN_V2L2_AOD_DAILY_NAME, const.AERONET_SUN_V2L2_SDA_DAILY_NAME]
    SUPPORTED_DATASETS = [const.AERONET_SUN_V2L2_AOD_DAILY_NAME,
                          const.AERONET_INV_V2L2_DAILY_NAME,
                          const.AERONET_SUN_V3L15_AOD_DAILY_NAME,
                          const.AERONET_SUN_V3L15_SDA_DAILY_NAME,
                          const.AERONET_SUN_V3L2_SDA_DAILY_NAME,
                          const.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME,
                          const.EARLINET_NAME]
    # when this file exists, an existing cache file is not read
    _DONOTCACHEFILE = os.path.join(const.OBSDATACACHEDIR, 'DONOTCACHE')

    def __init__(self, dataset_to_read=const.AERONET_SUN_V2L2_AOD_DAILY_NAME,
                 vars_to_read=None, ignore_cache=False,
                 verbose=False):
        
        #will be assigned in setter method of dataset_to_read
        self.data_dir = None
        self._dataset_to_read = None
        
        self.dataset_to_read = dataset_to_read
        
        # optional: list of variables that are supposed to be imported, if 
        # None, all variables provided by the corresponding network are loaded
        self.vars_to_read = vars_to_read
        
        # the data for each dataset_to
        self.data = od()
        
        self.verbose = verbose
        self.infiles = []
        # file caching
        self.writecachefile = True
        # pointer to first unused index of self.data
        
        self.revision = {}
        self.data_version = {}
        
        self.cache_file = {}
    
    @property
    def dataset_to_read(self):
        return self._dataset_to_read
    
    @dataset_to_read.setter
    def dataset_to_read(self, val):
        if not val in const.OBS_IDS:
            raise ValueError("Invalid input for ID of OBS network, please "
                             "choose from {}".format(const.OBS_IDS))
            
        data_dir = const.OBSCONFIG[val]['PATH']
        
        if not os.path.exists(data_dir):
            raise IOError("Specified directory {} for OBS-ID {} does not "
                          "exist".format(data_dir, val))
        
        self._dataset_to_read = val
        self.data_dir = data_dir
        
    def __str__(self):
        raise NotImplementedError("Requires review after API changes")
        stat_names = []
        for key in self.metadata:
            stat_names.append(self.metadata[key]['station name'])
        return ','.join(stat_names)

    def read(self):
        """Read observations

        Example
        -------
        >>> import pyaerocom.io.readungridded as pio
        >>> from pyaerocom import const
        >>> obj = pio.ReadUngridded(dataset_to_read=const.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME)
        >>> obj.read()
        >>> print(obj)
        >>> print(obj.metadata[0.]['latitude'])
        """

        import pickle

        dataset_to_read = self.dataset_to_read
        # read the data sets
        cache_hit_flag = False

        data_dir = const.OBSCONFIG[dataset_to_read]['PATH']
        revision = self.get_data_revision(dataset_to_read)
        newest_file_in_read_dir = max(glob.iglob(os.path.join(data_dir, '*')), 
                                      key=os.path.getctime)
        newest_file_date_in_read_dir = os.path.getctime(newest_file_in_read_dir)

        cache_file = os.path.join(
            const.OBSDATACACHEDIR,
            '_'.join([dataset_to_read, 'AllYears', 'AllVars.plk']))
        # TODO: check for yearly data sets as well and single variables as well
        if os.path.isfile(cache_file):
            # CACHE HIT
            if self.verbose:
                print("Importing from cache file: {}".format(cache_file))
                
            cache_hit_flag = True
            # read cache file
            in_handle = open(cache_file, 'rb')
            newest_file_in_read_dir_saved = pickle.load(in_handle)
            newest_file_date_in_read_dir_saved = pickle.load(in_handle)
            revision_saved = pickle.load(in_handle)
            if (newest_file_in_read_dir_saved != newest_file_in_read_dir
                    or newest_file_date_in_read_dir_saved != newest_file_date_in_read_dir
                    or revision_saved != revision):
                cache_hit_flag = False
                in_handle.close()

            # The rest can only be checked when the reading object is initialised
            object_version_saved = pickle.load(in_handle)

        # self.ReadCacheData(dataset_to_read)
        # CACHE MISS
        # call the different obs data reading classes
        if dataset_to_read == const.AERONET_SUN_V2L2_AOD_DAILY_NAME:
            # read AERONETSUN V2 L2 daily data set
            read_dummy = ReadAeronetSunV2(index_pointer=self.index_pointer, 
                                          verbose=self.verbose)
            if cache_hit_flag and object_version_saved == read_dummy.__version__:
                read_dummy = pickle.load(in_handle)
                if self.verbose:
                    sys.stdout.write('cache file ' + cache_file + ' read\n')
                # TODO we might need to adjust self.index_pointer in case we really work with more than one data set!
                in_handle.close()
            else:
                # re-read data
                read_dummy.read(self.vars_to_read)

        elif dataset_to_read == const.AERONET_SUN_V3L15_SDA_DAILY_NAME or \
                dataset_to_read == const.AERONET_SUN_V3L2_SDA_DAILY_NAME:
            # read AERONET SDA V3 L1.5 daily data set
            read_dummy = ReadAeronetSdaV3(index_pointer=self.index_pointer,
                                          dataset_to_read=dataset_to_read,
                                          verbose=self.verbose)
            if cache_hit_flag and object_version_saved == read_dummy.__version__:
                read_dummy = pickle.load(in_handle)
                if self.verbose:
                    sys.stdout.write('cache file ' + cache_file + ' read\n')
                # TODO we might need to adjust self.index_pointer in case we really work with more than one data set!
                in_handle.close()
            else:
                # re-read data
                read_dummy.read(self.vars_to_read)

        elif dataset_to_read == const.AERONET_INV_V2L2_DAILY_NAME:
            # read AERONET inversions V2 L2.0 daily data set
            read_dummy = ReadAeronetInvV2(index_pointer=self.index_pointer,
                                          dataset_to_read=dataset_to_read,
                                          verbose=self.verbose)
            if cache_hit_flag and object_version_saved == read_dummy.__version__:
                read_dummy = pickle.load(in_handle)
                if self.verbose:
                    sys.stdout.write('cache file ' + cache_file + ' read\n')
                # TODO we might need to adjust self.index_pointer in case we really work with more than one data set!
                in_handle.close()
            else:
                # re-read data
                read_dummy.read(self.vars_to_read)

        elif dataset_to_read == const.AERONET_SUN_V3L15_AOD_DAILY_NAME:
            # read AERONETSUN V3 L1.5 daily data set
            read_dummy = ReadAeronetSunV3(index_pointer=self.index_pointer,
                                          verbose=self.verbose)
            if cache_hit_flag and object_version_saved == read_dummy.__version__:
                read_dummy = pickle.load(in_handle)
                if self.verbose:
                    sys.stdout.write('cache file ' + cache_file + ' read\n')
                # TODO we might need to adjust self.index_pointer in case we really work with more than one data set!
                in_handle.close()
            else:
                # re-read data
                read_dummy.read(self.vars_to_read)

        elif dataset_to_read == const.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME:
            # read AERONETSUN V3 L1.5 all points data set
            read_dummy = ReadAeronetSunV3(index_pointer=self.index_pointer,
                                          dataset_to_read=dataset_to_read,
                                          verbose=self.verbose)
            if cache_hit_flag and object_version_saved == read_dummy.__version__:
                read_dummy = pickle.load(in_handle)
                if self.verbose:
                    sys.stdout.write('cache file ' + cache_file + ' read\n')
                # TODO we might need to adjust self.index_pointer in case we really work with more than one data set!
                in_handle.close()
            else:
                # re-read data
                read_dummy.read(self.vars_to_read)


        elif dataset_to_read == const.AERONET_SUN_V3L20_AOD_DAILY_NAME:
            print("Not implemented at this point.")

        elif dataset_to_read == const.AERONET_SUN_V3L20_AOD_ALL_POINTS_NAME:
            print("Not implemented at this point.")

        elif dataset_to_read == const.EARLINET_NAME:
            read_dummy = ReadEarlinet(index_pointer=self.index_pointer, verbose=self.verbose)
            if cache_hit_flag and object_version_saved == read_dummy.__version__:
                read_dummy = pickle.load(in_handle)
                if self.verbose:
                    sys.stdout.write('cache file ' + cache_file + ' read\n')
                # TODO we might need to adjust self.index_pointer in case we really work with more than one data set!
                in_handle.close()
            else:
                # re-read data
                read_dummy.read(self.vars_to_read)
            
        self.infiles.append(read_dummy.files)
        self.index_pointer = read_dummy.index_pointer
        self.data_dirs[dataset_to_read] = const.OBSCONFIG[dataset_to_read]['PATH']
        self.revision[dataset_to_read] = revision
        self.data_version[dataset_to_read] = read_dummy.__version__
        # TODO do not forget to adjust pointers between metadata and data in case there's more than one data set!!!
        if isinstance(self.data, list):
            # this is the 1st data set
            self.data = read_dummy.data
            # we might want to check for double station names here
            # for the second data set we DO need to update the dict keys of metadata and data!
            # since we do want to keep the point cloud
            # we might want to move the variables to read to a dictionary
        else:
            # extend self.data numpy array
            self.data = np.append(self.data, read_dummy.data, axis=0)
            # also adjust self.index_pointer!
            # sys.stderr.write("ERROR: can only read one obs data network at the time at this point!")
        self.metadata.update(read_dummy.metadata)
        # write the cache file
        if not cache_hit_flag:
            # write cache file in case the data was newly read
            if self.verbose:
                sys.stdout.write('Writing cache file ' + cache_file + '\n')
            # OutHandle = gzip.open(c__cache_file, 'wb') # takes too much time
            out_handle = open(cache_file, 'wb')
            newest_file_in_read_dir_saved = newest_file_in_read_dir
            newest_file_date_in_read_dir_saved = newest_file_date_in_read_dir
            revision_saved = revision
            object_version_saved = read_dummy.__version__
            pickle.dump(newest_file_in_read_dir_saved, out_handle, pickle.HIGHEST_PROTOCOL)
            pickle.dump(newest_file_date_in_read_dir_saved, out_handle, pickle.HIGHEST_PROTOCOL)
            pickle.dump(revision_saved, out_handle, pickle.HIGHEST_PROTOCOL)
            pickle.dump(object_version_saved, out_handle, pickle.HIGHEST_PROTOCOL)
            pickle.dump(read_dummy, out_handle, pickle.HIGHEST_PROTOCOL)
            out_handle.close()
            if self.verbose:
                sys.stdout.write('done\n')

    def get_data_revision(self, dataset_name):
        """method to read the revision string from the file Revision.txt in the main data directory"""

        revision = 'unset'
        try:
            revision_file = os.path.join(const.OBSCONFIG[dataset_name]['PATH'], 
                                         const.REVISION_FILE)
            if os.path.isfile(revision_file):
                with open(revision_file, 'rt') as in_file:
                    revision = in_file.readline().strip()
                    in_file.close()
        except:
            if self.verbose:
                print("Revision file for {} does not exist".format(dataset_name))

        return revision

    def get_data_dir(self, dataset_name):
        """method to return the path of an obs data set"""

        try:
            return const.OBSCONFIG[dataset_name]['PATH']
        except:
            raise AttributeError("data set name " + dataset_name + "not found ")


    def check_obs_network_name(self, obs_network_name):
        """method to quick check if the user supplied obs network string is right"""

        if obs_network_name in self.SUPPORTED_DATASETS:
            return True
        else:
            return False

if __name__=="__main__":
    data = ReadUngridded(const.AERONET_SUN_V2L2_AOD_DAILY_NAME, verbose=True)
    data.read()
