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
import os, logging

from pyaerocom.exceptions import (DataRetrievalError,
                                  NetworkNotImplemented, NetworkNotSupported)
from pyaerocom.io.read_aeronet_sdav2 import ReadAeronetSdaV2
from pyaerocom.io.read_aeronet_sdav3 import ReadAeronetSdaV3
from pyaerocom.io.read_aeronet_invv2 import ReadAeronetInvV2
from pyaerocom.io.read_aeronet_invv3 import ReadAeronetInvV3
from pyaerocom.io.read_aeronet_sunv2 import ReadAeronetSunV2
from pyaerocom.io.read_aeronet_sunv3 import ReadAeronetSunV3
from pyaerocom.io.read_earlinet import ReadEarlinet
from pyaerocom.io.read_ebas import ReadEbas
from pyaerocom.io.read_aasetal import ReadAasEtal
from pyaerocom.io.read_gaw import ReadGAW
from pyaerocom.io.read_ghost import ReadGhost

from pyaerocom.io.cachehandler_ungridded import CacheHandlerUngridded
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.helpers import varlist_aerocom

from pyaerocom import const, print_log

# TODO Note: Removed infiles (list of files from which datasets were read, since it
# was not used anywhere so far)
class ReadUngridded(object):
    """Factory class for reading of ungridded data based on obsnetwork ID"""
    SUPPORTED = [ReadAeronetInvV3,
                 ReadAeronetInvV2,
                 ReadAeronetSdaV2,
                 ReadAeronetSdaV3,
                 ReadAeronetSunV2,
                 ReadAeronetSunV3,
                 ReadEarlinet,
                 ReadEbas,
                 ReadGAW,
                 ReadAasEtal,
                 ReadGhost]

    # when this file exists, an existing cache file is not read
    _DONOTCACHEFILE = None
    if isinstance(const._cachedir, str) and os.path.exists(const._cachedir):
        _DONOTCACHEFILE = os.path.join(const._cachedir, 'DONOTCACHE')

    def __init__(self, datasets_to_read=None, vars_to_retrieve=None,
                 ignore_cache=False, data_dir=None):
        if datasets_to_read is None:
            datasets_to_read = const.AERONET_SUN_V3L2_AOD_DAILY_NAME
        #will be assigned in setter method of dataset_to_read
        self._datasets_to_read = []
        #: dictionary containing reading classes for each dataset to read (will
        #: be filled in setter of datasets_to_read)
        self._readers = {}

        self.datasets_to_read = datasets_to_read

        # optional: list of variables that are supposed to be imported, if
        # None, all variables provided by the corresponding network are loaded
        self.vars_to_retrieve = vars_to_retrieve

        # initiate a logger for this class
        self.logger = logging.getLogger(__name__)

        if data_dir is not None and len(self.datasets_to_read) > 1:
            raise ValueError('Invalid input combination for ReadUngridded. '
                             'Input data_dir can only be specified if a '
                             'single dataset is supposed to be read')

        self.data_dir=data_dir

        if ignore_cache:
            self.logger.info('Deactivating caching')
            const.CACHING = False

    @property
    def DATASET_PATH(self):
        """Data directory of dataset to read

        Raises exception if more than one dataset to read is specified
        """
        if not len(self._datasets_to_read) == 1:
            raise ValueError('Conflict: multiple datasets are assigned to be '
                             'read, but dataset path can only be retrieved for '
                             'single dataset retrievals')
        return self.get_reader(self._datasets_to_read[0]).DATASET_PATH

    @property
    def ignore_cache(self):
        if os.path.exists(self._DONOTCACHEFILE) or not const.CACHING:
            return True
        return False

    @property
    def dataset_to_read(self):
        """Helper that returns the dataset to be read

        Note
        ----
        Only works if a single dataset is assigned in :attr:`datasets_to_read`,
        else throws an ValueError.

        Raises
        ------
        ValueError
            if :attr:`datasets_to_read` contains no or more than one entry.
        """
        dsr = self.datasets_to_read
        if len(dsr) == 0:
            raise ValueError('Could not fetch reader class. No dataset '
                             'assigned in attr. datasets_to_read')
        elif len(dsr) > 1:
            raise ValueError('Could not fetch reader class. More than one '
                             'dataset is assigned in attr. '
                             'datasets_to_read')
        return dsr[0]

    @property
    def datasets_to_read(self):
        """List of datasets supposed to be read"""
        return self._datasets_to_read

    @datasets_to_read.setter
    def datasets_to_read(self, datasets):
        if isinstance(datasets, str):
            datasets = [datasets]
        elif not isinstance(datasets, (tuple, list)):
            raise IOError('Invalid input for parameter datasets_to_read')
        avail = []
        for ds in datasets:
            try:
                self.find_read_class(ds)
                avail.append(ds)
            except NetworkNotSupported:
                print_log.warning('Removing {} from list of datasets to read '
                                  'in ReadUngridded class. Reason: network '
                                  'not supported or data is not available'
                                  .format(ds))
        self._datasets_to_read = avail

    def dataset_provides_variables(self, dataset_to_read=None):
        """List of variables provided by a certain dataset"""
        if dataset_to_read is None:
            dataset_to_read = self.dataset_to_read
        if dataset_to_read in self._readers:
            return self._readers[dataset_to_read].PROVIDES_VARIABLES
        return self.find_read_class(dataset_to_read).PROVIDES_VARIABLES

    def get_reader(self, dataset_to_read=None):
        """Helper method that returns loaded reader class

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
        if dataset_to_read is None:
            dataset_to_read = self.dataset_to_read
        elif not dataset_to_read in self.supported_datasets:
            raise NetworkNotSupported('Could not fetch reader class: Input '
                                      'network {} is not supported by '
                                      'ReadUngridded'.format(dataset_to_read))
        if not dataset_to_read in self._readers:
            self.find_read_class(dataset_to_read)
        return self._readers[dataset_to_read]

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
        if dataset_to_read in self._readers:
            return self._readers[dataset_to_read]
# =============================================================================
#         if not dataset_to_read in const.OBS_IDS_UNGRIDDED:
#             raise NetworkNotSupported("Network {} is not supported or data is "
#                                       "not available on this machine"
#                                       .format(dataset_to_read))
# =============================================================================
        for _cls in self.SUPPORTED:
            if dataset_to_read in _cls.SUPPORTED_DATASETS:
                self._readers[dataset_to_read] = _cls(dataset_to_read)
                return self._readers[dataset_to_read]
        raise NetworkNotImplemented("No reading class available yet for dataset "
                                    "{}".format(dataset_to_read))

    def read_dataset(self, dataset_to_read, vars_to_retrieve=None,
                     only_cached=False, **kwargs):
        """Read dataset into an instance of :class:`ReadUngridded`

        Note
        ----
        This method does not assign loaded data obj to class attribute
        :attr:`data` (only :func:`read` does)

        Parameters
        ----------
        dataset_to_read : str
            name of dataset
        vars_to_retrieve : str or list
            variable or list of variables to be imported
        only_cached : bool
            if True, then nothing is reloaded but only data is loaded that is
            available as cached objects (not recommended to use but may be
            used if working offline without connection to database)

        Returns
        --------
        UngriddedData
            data object
        """
        _caching = None
        if len(kwargs) > 0:
            _caching = const.CACHING
            const.CACHING = False

            print_log.info('Received additional reading constraints, '
                           'ignoring caching')
        if vars_to_retrieve is None:
            # Note: self.vars_to_retrieve may be None as well, then
            # default variables of each network are read
            vars_to_retrieve = self.vars_to_retrieve
        vars_to_retrieve = varlist_aerocom(vars_to_retrieve)

        reader = self.get_reader(dataset_to_read)

        # data_dir will be None in most cases, but can be specified when
        # creating the instance, by default, data_dir is inferred automatically
        # in the reading class, using database location
        data_dir = self.data_dir
        if self.data_dir is not None:

            if not os.path.exists(self.data_dir):
                raise FileNotFoundError(
                    'Trying to read {} from specified data_dir {} failed. '
                    'Directory does not exist'.format(dataset_to_read, data_dir)
                    )
            reader._dataset_path = data_dir
            const.print_log.info('Reading {} from specified data loaction: {}'
                                 .format(dataset_to_read, data_dir))
        if vars_to_retrieve is None:
            vars_to_retrieve = reader.PROVIDES_VARIABLES
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]

        # Since this interface enables to load multiple datasets, each of
        # which support a number of variables, here, only the variables are
        # considered that are supported by the dataset
        vars_available = [var for var in vars_to_retrieve if
                          reader.var_supported(var)]
        if len(vars_available) == 0:
            raise DataRetrievalError('None of the input variables ({}) is '
                                     'supported by {} interface'
                                     .format(vars_to_retrieve, dataset_to_read))
        cache = CacheHandlerUngridded(reader)
        if not self.ignore_cache:
            # initate cache handler
            for var in vars_available:
                try:
                    cache.check_and_load(var,
                                         force_use_outdated=only_cached)
                except Exception:
                    self.logger.exception('Fatal: compatibility error between '
                                          'old cache file {} and current version '
                                          'of code ')

        if not only_cached:
            vars_to_read = [v for v in vars_available if not v in cache.loaded_data]
        else:
            vars_to_read = []

        data_read = None
        if len(vars_to_read) > 0:

            _loglevel = print_log.level
            print_log.setLevel(logging.INFO)
            data_read = reader.read(vars_to_read, **kwargs)
            print_log.setLevel(_loglevel)

            for var in vars_to_read:
                # write the cache file
                if not self.ignore_cache:
                    try:
                        cache.write(data_read, var)
                    except Exception as e:
                        _caching = False
                        print_log.warning('Failed to write to cache directory. '
                                          'Error: {}. Deactivating caching in '
                                          'pyaerocom'.format(repr(e)))

        if len(vars_to_read) == len(vars_available):
            data_out = data_read
        else:
            data_out = UngriddedData()
            for var in vars_available:
                if var in cache.loaded_data:
                    data_out.append(cache.loaded_data[var])
            if data_read is not None:
                data_out.append(data_read)

        if _caching is not None:
            const.CACHING = _caching
        return data_out

    def read(self, datasets_to_read=None, vars_to_retrieve=None,
             only_cached=False, **kwargs):
        """Read observations

        Iter over all datasets in :attr:`datasets_to_read`, call
        :func:`read_dataset` and append to data object

        Parameters
        ----------
        datasets_to_read : str or list
            data ID or list of all datasets to be imported
        vars_to_retrieve : str or list
            variable or list of variables to be imported
        only_cached : bool
            if True, then nothing is reloaded but only data is loaded that is
            available as cached objects (not recommended to use but may be
            used if working offline without connection to database)

        Example
        -------
        >>> import pyaerocom.io.readungridded as pio
        >>> from pyaerocom import const
        >>> obj = pio.ReadUngridded(dataset_to_read=const.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME)
        >>> obj.read()
        >>> print(obj)
        >>> print(obj.metadata[0.]['latitude'])

        """
        if datasets_to_read is not None:
            self.datasets_to_read = datasets_to_read
        if vars_to_retrieve is not None:
            self.vars_to_retrieve = vars_to_retrieve

        data = UngriddedData()
        for ds in self.datasets_to_read:
            self.logger.info('Reading {} data'.format(ds))
            try:
                data.append(self.read_dataset(ds, vars_to_retrieve,
                                              only_cached=only_cached,
                                              **kwargs))
            except DataRetrievalError as e:
                print_log.exception('Failed to read {}. Reason: {}'
                                    .format(ds, repr(e)))

            self.logger.info('Successfully imported {} data'.format(ds))
        return data

    @property
    def SUPPORTED_DATASETS(self):
        """Returns list of strings containing all supported dataset names"""
        l = []
        for r in self.SUPPORTED:
            l.extend(r.SUPPORTED_DATASETS)
        return l

    @property
    def supported_datasets(self):
        return self.SUPPORTED_DATASETS

    def __str__(self):
        #raise NotImplementedError("Requires review after API changes")
        s=''
        for ds in self.datasets_to_read:
            s += '\n{}'.format(self.get_reader(ds))
        return s

    # OUTSOURCED
    def read_datasetOLD(self, dataset_to_read, vars_to_retrieve=None,
                     **kwargs):
        """Read single dataset into instance of :class:`ReadUngridded`

        Note
        ----
        This method does not write class attribute :attr:`data` (only
        :func:`read` does)

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
        _caching = None
        if len(kwargs) > 0:
            _caching = const.CACHING
            const.CACHING = False

            print_log.info('Received additional reading constraints, '
                           'ignoring caching')
        if vars_to_retrieve is None:
            # Note: self.vars_to_retrieve may be None as well, then
            # default variables of each network are read
            vars_to_retrieve = self.vars_to_retrieve

        reader = self.get_reader(dataset_to_read)

        if vars_to_retrieve is None:
            vars_to_retrieve = reader.PROVIDES_VARIABLES
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]

        # Since this interface enables to load multiple datasets, each of
        # which support a number of variables, here, only the variables are
        # considered that are supported by the dataset
        vars_available = [var for var in vars_to_retrieve if var in
                          reader.PROVIDES_VARIABLES]

        # read the data sets
        cache_hit_flag = False

        if not self.ignore_cache:
            # initate cache handler
            try:
                cache = CacheHandlerUngridded(reader, vars_available, **kwargs)
                if cache.check_and_load():
                    all_avail = True
                    for var in vars_available:
                        if not var in cache.loaded_data:
                            all_avail = False
                            break
                    if all_avail:
                        print_log.info('Found Cache match for {}'
                                       .format(dataset_to_read))
                        cache_hit_flag = True
                        data = cache.loaded_data
            except Exception:
                self.logger.exception('Fatal: compatibility error between old '
                                      'cache file and current version of code ')
                cache_hit_flag = False

        if not cache_hit_flag:
            print_log.info('No Cache match found for {} in {}. '
                           'Reading from files (this '
                           'may take a while)'.format(dataset_to_read,
                                                      const.CACHEDIR))
            _loglevel = print_log.level
            print_log.setLevel(logging.INFO)
            data = reader.read(vars_available, **kwargs)
            print_log.setLevel(_loglevel)

        self.revision[dataset_to_read] = reader.data_revision
        self.data_version[dataset_to_read] = reader.__version__

        # write the cache file
        if not cache_hit_flag and not self.ignore_cache:
            try:
                cache.write(data)
            except Exception as e:
                _caching = False
                print_log.warning('Failed to write to cache directory:\n{}.\n'
                               'Deactivating caching in pyaerocom'.format(repr(e)))

        if _caching is not None:
            const.CACHING = _caching
        return data
if __name__=="__main__":

    obs_dir = '/home/jonasg/MyPyaerocom/data/obsdata/AeronetSunV3Lev2.0.daily/renamed'
    reader = ReadUngridded(data_dir=obs_dir)

    data = reader.read('AeronetSunV3Lev2.daily', 'od550aer')

    ch = CacheHandlerUngridded()

    filename = 'test_custom_cache.pkl'
    ch.write(data, filename)

    if ch.check_and_load(filename):
        data1 = ch.loaded_data[filename]
