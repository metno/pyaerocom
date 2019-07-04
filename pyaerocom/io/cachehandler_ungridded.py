#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Caching class for reading and writing of ungridded data Cache objects
"""
from pyaerocom import const, logger, UngriddedData
from pyaerocom.exceptions import (AerocomConnectionError, CacheReadError,
                                  CacheWriteError)

import glob, os, pickle

# TODO: Write data attribute list contains_vars in header of pickled file and
# check if variables match the request
class CacheHandlerUngridded(object):
    """Interface for reading and writing of cache files
    
    Cache filename mask is 
    
    <dataset_to_read>_<var>.pkl
    
    e.g. EBASMC_scatc550aer.pkl
    
    Attributes
    ----------
    reader : ReadUngriddedBase
        reading class for dataset
    loaded_data : dict
        dictionary containing successfully loaded instances of single variable
        :class:`UngriddedData` objects (keys are variable names)
    """
    __version__ = '1.00'
    #: Directory of cache files
    try:
        CACHE_DIR = const.CACHEDIR
    except:
        CACHE_DIR = None
        logger.exception('Pyaerocom cache directory is not defined')
    #: Cache file header keys that are checked (and required unchanged) when
    #: reading a cache file
    CACHE_HEAD_KEYS = ['pyaerocom_version',
                       'newest_file_in_read_dir',
                       'newest_file_date_in_read_dir',
                       'data_revision', 
                       'reader_version', 
                       'ungridded_data_version', 
                       'cacher_version']
    
    def __init__(self, reader=None, cache_dir=None, **kwargs):
        self._reader = None
        self.reader = reader
        
        self.loaded_data = {}
        
        self._cache_dir = cache_dir
        
    @property
    def reader(self):
        """Instance of reader class"""
        if self._reader is None:
            raise AttributeError('No reader class assigned to cache object')
        return self._reader
    
    @reader.setter
    def reader(self, val):
        from pyaerocom.io import ReadUngriddedBase
        if not isinstance(val, ReadUngriddedBase):
            try:
                val = val.get_reader()
                if not isinstance(val, ReadUngriddedBase):
                    raise TypeError('Invalid input for reader')
            except:
                raise TypeError('Invalid input for reader')
        self._reader = val
        self.loaded_data = {}
        
    @property
    def cache_dir(self):
        """Directory where cached files are stored"""
        if self._cache_dir is not None:
            return self._cache_dir
        if self.CACHE_DIR is None or not os.path.exists(self.CACHE_DIR):
            raise FileNotFoundError('Cache directory does not exist: {}'
                                    .format(self.CACHE_DIR))
        return self.CACHE_DIR
    
    @cache_dir.setter
    def cache_dir(self, val):
        if not isinstance(val, str) or not os.path.exists(val):
            raise FileNotFoundError('Input directory does not exist: {}'
                                    .format(val))
        self._cache_dir = val
        
    @property
    def dataset_to_read(self):
        """Data ID of the associated dataset"""
        return self.reader.dataset_to_read
    
    @property
    def data_dir(self):
        """Data directory of the associated dataset"""
        return self.reader.DATASET_PATH        
        
    def file_name(self, var_name):
        """File name of cache file"""
        name = '_'.join([self.dataset_to_read, var_name])
        return name + '.pkl'
    
    def file_path(self, var_name):
        """File path of cache file"""
        return os.path.join(self.cache_dir, self.file_name(var_name))
    
    def _check_pkl_head_vs_database(self, in_handle):
        current = self.cache_meta_info()
        head = pickle.load(in_handle)
        if not isinstance(head, dict):
            raise CacheReadError('Invalid cache file')
        for k, v in head.items():
            if not k in current:
                raise CacheReadError('Invalid cache header key: {}'.format(k))
            elif not v == current[k]:
                const.print_log.info('{} is outdated (value: {}). Current '
                                     'value: {}'.format(k, v, current[k]))
                return False
        return True
    
    def cache_meta_info(self):
        """Dictionary containing relevant caching meta-info"""
        try:
            newest = max(glob.iglob(os.path.join(self.data_dir, '*')), 
                         key=os.path.getctime)
            newest_date = os.path.getctime(newest)
        except Exception as e:
            raise AerocomConnectionError('Failed to establish connection to '
                                         'data server. Reason: {}'.repr(e))
        d = dict.fromkeys(self.CACHE_HEAD_KEYS)
        from pyaerocom import __version__
        
        d['pyaerocom_version'] = __version__
        d['newest_file_in_read_dir'] = newest
        d['newest_file_date_in_read_dir'] = newest_date
        d['data_revision'] = self.reader.data_revision
        d['reader_version'] = self.reader.__version__
        d['ungridded_data_version'] = UngriddedData.__version__ 
        d['cacher_version'] = self.__version__
        return d
    
    def check_and_load(self, var_name):
        """Check if cache file exists and load
        
        Note
        ----
        If a cache file exists for this database, but cannot be loaded or is
        outdated against pyaerocom updates, then it will be removed (the latter
        only if :attr:`pyaerocom.const.RM_CACHE_OUTDATED` is True).
        
        Returns
        -------
        bool
            True, if cache file exists and could be successfully loaded, else
            False. Note: if import is successful, the corresponding data object
            (instance of :class:`pyaerocom.UngriddedData` can be accessed via
            :attr:`loaded_data'
            
        Raises
        ------
        TypeError
            if cached file is not an instance of :class:`pyaerocom.UngriddedData` 
            class (which should not happen)
        """
        try:
            fp = self.file_path(var_name)
        except FileNotFoundError as e:
            logger.warning(repr(e))
            return False
        
        if not os.path.isfile(fp):
            logger.info('No cache file available for {}, {}'
                        .format(self.dataset_to_read, var_name))
            return False
    
        
        delete_existing = const.RM_CACHE_OUTDATED
                
        in_handle = open(fp, 'rb')
        
        
        try:
            ok = self._check_pkl_head_vs_database(in_handle)
        except Exception as e:
            ok = False
            delete_existing = True
            logger.exception('File error in cached data file {}. File will '
                             'be removed and data reloaded'
                             'Error: {}'.format(fp, repr(e)))
        if not ok:
            # TODO: Should we delete the cache file if it is outdated ???
            logger.info('Aborting reading cache file {}. Aerocom database '
                        'or pyaerocom version has changed compared to '
                        'cached version'
                        .format(self.file_name(var_name)))
            in_handle.close()
            if delete_existing: #something was wrong
                const.print_log.info('Deleting outdated cache file: {}'
                                     .format(fp))
                os.remove(self.file_path(var_name))
            return False
        
        # everything is okay
        data = pickle.load(in_handle)
        if not isinstance(data, UngriddedData):
            raise TypeError('Unexpected data type stored in cache file, need '
                            'instance of UngriddedData, got {}'
                            .format(type(data)))
            
        self.loaded_data[var_name] = data
        logger.info('Successfully loaded data for {} from Cache'
                    .format(self.dataset_to_read))
        return True
    
    def write(self, data, var_name=None):
        """Write single-variable instance of UngriddedData to cache
        
        Parameters
        ----------
        data : UngriddedData
            object containing the data (possibly containing multiple variables)
        var_name : str, optional
            name of variable that is supposed to be stored (only required if
            input `data` contains more than one variable)
        """
        meta = self.cache_meta_info()
        
        if not isinstance(data, UngriddedData):
            raise TypeError('Invalid input, need instance of UngriddedData, '
                            'got {}'.format(type(data)))
        if len(data.contains_datasets) > 1:
            raise CacheWriteError('Input UngriddedData object contains '
                                  'datasets: {}. Can only write single '
                                  'dataset objects'
                                  .format(data.contains_datasets))
        if var_name is None:
            if len(data.contains_vars) > 1:
                raise CacheWriteError('Input UngriddedData object for {} contains '
                                      'more than one variable: {}. Please '
                                      'specify which variable should be '
                                      'cached'
                                      .format(self.reader.data_id,
                                              data.contains_vars))
            var_name = data.contains_vars[0]
        
        elif not var_name in data.contains_vars:
            raise CacheWriteError('Cannot write cache file: variable {} does '
                                  'not exist in input UngriddedData object'
                                  .format(var_name))
            
        if len(data.contains_vars) > 1:
            data = data.extract_var(var_name)
            
        fp = self.file_path(var_name)
        logger.info('Writing cache file: {}'.format(fp))
        success = True
        # OutHandle = gzip.open(c__cache_file, 'wb') # takes too much time
        out_handle = open(fp, 'wb')
        
        try:
            # write cache header
            pickle.dump(meta, out_handle, pickle.HIGHEST_PROTOCOL)
            # write data
            pickle.dump(data, out_handle, pickle.HIGHEST_PROTOCOL)
    
        except Exception as e:
            from pyaerocom import print_log
            print_log.exception('Failed to write cache'.format(repr(e)))
            success=False
        finally:    
            out_handle.close()
            if not success:
                os.remove(self.file_path)
        logger.info('Successfully wrote {} data ({}) to disk!'
                    .format(var_name, self.reader.data_id))
        
    def __str__(self):
        return 'Cache handler for {}'.format(self.reader.data_id)
    
if __name__ == "__main__":
    import pyaerocom as pya
    
    import matplotlib.pyplot as plt
    plt.close('all')

    r = pya.io.ReadAeronetSunV3()
    
    data = r.read(vars_to_retrieve=['od550aer', 'ang4487aer'],
                  file_pattern='Bo*')
    
    aod = data.extract_var('od550aer')
    
    cache = CacheHandlerUngridded(r)
    
    cache.write(aod)
    
    r = pya.io.ReadUngridded()
    r.read('AeronetSunV3Lev2.daily', 
           vars_to_retrieve=['od550aer', 'ang4487aer'],
           file_pattern='Bo*')
    