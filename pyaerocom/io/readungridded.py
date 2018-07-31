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

from pyaerocom.exceptions import NetworkNotImplemented, NetworkNotSupported
from pyaerocom.io.read_aeronet_sdav2 import ReadAeronetSdaV2
from pyaerocom.io.read_aeronet_sdav3 import ReadAeronetSdaV3
from pyaerocom.io.read_aeronet_invv2 import ReadAeronetInvV2
from pyaerocom.io.read_aeronet_sunv2 import ReadAeronetSunV2
from pyaerocom.io.read_aeronet_sunv3 import ReadAeronetSunV3
from pyaerocom.io.read_earlinet import ReadEarlinet
from pyaerocom.io.read_ebas import ReadEbas

from pyaerocom.io.cachehandler_ungridded import CacheHandlerUngridded
from pyaerocom.ungriddeddata import UngriddedData

from pyaerocom import const, logger

# TODO Note: Removed infiles (list of files from which datasets were read, since it 
# was not used anywhere so far)
class ReadUngridded:
    """Factory class for reading of ungridded data based on obsnetwork ID
    
    """
    SUPPORTED = [ReadAeronetInvV2,
                 ReadAeronetSdaV2,
                 ReadAeronetSdaV3,
                 ReadAeronetSunV2,
                 ReadAeronetSunV3,
                 ReadEarlinet,
                 ReadEbas]
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

    def __init__(self, datasets_to_read=const.AERONET_SUN_V2L2_AOD_DAILY_NAME,
                 vars_to_retrieve=None, ignore_cache=False):
        
        #will be assigned in setter method of dataset_to_read
        self._datasets_to_read = []
        #: dictionary containing reading classes for each dataset to read (will
        #: be filled in setter of datasets_to_read)
        self._read_objects = {}
        
        self.datasets_to_read = datasets_to_read
    
        # optional: list of variables that are supposed to be imported, if 
        # None, all variables provided by the corresponding network are loaded
        self.vars_to_retrieve = vars_to_retrieve
        
        if os.path.exists(self._DONOTCACHEFILE):
            ignore_cache = True
        self.ignore_cache = ignore_cache
        
        self.revision = {}
        self.data_version = {}
    
        self.cache_files = {}
    
    @property
    def datasets_to_read(self):
        return self._datasets_to_read
    
    @datasets_to_read.setter
    def datasets_to_read(self, datasets):
        if isinstance(datasets, str):
            datasets = [datasets]
        elif not isinstance(datasets, (tuple, list)):
            raise IOError('Invalid input for parameter datasets_to_read')
        
        success = []
        for ds in datasets:
            try:
                reader = self.find_read_class(ds)
                self._read_objects[ds] = reader(ds)
            except (NetworkNotSupported, NetworkNotImplemented) as e:
                logger.warning("Failed to initialise reading of {} data. "
                               "{}".format(ds, repr(e)))
            else:
                success.append(ds)
    
        self._datasets_to_read = success
        
    def find_read_class(self, dataset_to_read):
        """Find reading class for dataset name
        
        Loops over all reading classes available in :attr:`SUPPORTED` and finds
        the first one that matches the input dataset name, by checking the 
        attribute :attr:`SUPPORTED_DATASETS` in each respective reading class
        
        Parameters
        -----------
        dataset_to_read : str
            Name of dataset
        
        Returns
        -------
        ReadUngriddedBase
            instance of reading class (needs to be implementation of base 
            class :class:`ReadUngriddedBase`)
        
        Raises
        ------
        NetworkNotSupported
            if network is not supported by pyaerocom
        NetworkNotImplemented
            if network is supported but no reading routine is implemented yet
        
        """
        if not dataset_to_read in const.OBS_IDS:
            raise NetworkNotSupported("Network {} is not supported and will be "
                                      "ignored".format(dataset_to_read))
        for cls in self.SUPPORTED:
            if dataset_to_read in cls.SUPPORTED_DATASETS:
                return cls
        raise NetworkNotImplemented("No reading class available yet for dataset "
                                    "{}".format(dataset_to_read))
        
    def __str__(self):
        raise NotImplementedError("Requires review after API changes")
        stat_names = []
        for key in self.metadata:
            stat_names.append(self.metadata[key]['station_name'])
        return ','.join(stat_names)
        
    def read_dataset(self, dataset_to_read, vars_to_retrieve=None, **kwargs):
        """Read single dataset into instance of :class:`ReadUngridded`
        
        Parameters
        ----------
        dataset_to_read : str
            name of dataset
        vars_to_retrieve : list
            list of variables to be retrieved. If None (default), the default
            variables of each reading routine are imported
            
        Returns
        --------
        UngriddedData
            data object
        """
        reader = self._read_objects[dataset_to_read]
        
        # read the data sets
        cache_hit_flag = False
        
        # initate cache handler
        cache = CacheHandlerUngridded(reader, vars_to_retrieve, **kwargs)
        
        if cache.check_and_load() and not self.ignore_cache:
            cache_hit_flag = True
            data = cache.loaded_data
        else:
            data = reader.read(vars_to_retrieve)
        
        self.revision[dataset_to_read] = reader.data_revision
        self.data_version[dataset_to_read] = reader.__version__
        self.cache_files[dataset_to_read] = cache.file_path
        
        # write the cache file
        if not cache_hit_flag and not self.ignore_cache:
            cache.write(data)
        
        return data
    
    def read(self):
        """Read observations

        Iter over all datasets in :attr:`datasets_to_read`, call 
        :func:`read_dataset` and append to data object
        
        Example
        -------
        >>> import pyaerocom.io.readungridded as pio
        >>> from pyaerocom import const
        >>> obj = pio.ReadUngridded(dataset_to_read=const.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME)
        >>> obj.read()
        >>> print(obj)
        >>> print(obj.metadata[0.]['latitude'])
        """
        data = UngriddedData()
        for ds in self.datasets_to_read:
            data.append(self.read_dataset(ds))
        self.data = data
        return data
    
if __name__=="__main__":
    test = [const.AERONET_SUN_V3L15_AOD_DAILY_NAME,
            const.EARLINET_NAME]
    read = ReadUngridded(test)
    
    print(read.datasets_to_read)
    
    from time import time
    t0 = time()
    read.read()
    print('Elapsed time first read: {} s'.format(time() - t0))
    
    t0 = time()
    read.read()
    print('Elapsed time 2nd read: {} s'.format(time() - t0))