#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Caching class for reading and writing of ungridded data Cache objects
"""
from pyaerocom import const, logger, UngriddedData
from pyaerocom.exceptions import AerocomConnectionError
from pyaerocom.helpers import to_datestring_YYYYMMDD
import glob, os, pickle

# TODO: Write data attribute list contains_vars in header of pickled file and
# check if variables match the request
class CacheHandlerUngridded(object):
    """Interface for reading and writing of cache files
    
    Cache filename mask is 
    
    <dataset_to_read>_<vars_string>_<start>_<stop>.pkl
    
    e.g. EARLINET_DefaultVars_00000101_30000101.pkl
    
    Attributes
    ----------
    reader : ReadUngriddedBase
        reading class for dataset
    vars_to_retrieve : :obj:`list`, optional
        specify variables to be retrieved in dataset, if None, this list 
        corresponds to the default variables of the respective reading class
    start : :obj:`str`, :obj:`datetime`, :obj:`datetime64`, :obj:`Timestamp`, optional
        start time of query, may be string (in format YYYYMMDD), datetime, 
        numpy.datetime64 or pandas.Timestamp. Will be converted to string 
        with format YYYYMMDD
    stop : :obj:`str`, :obj:`datetime`, :obj:`datetime64`, :obj:`Timestamp`, optional
        stop time of query, may be string (in format YYYYMMDD), datetime, 
        numpy.datetime64 or pandas.Timestamp. Will be converted to string 
        with format YYYYMMDD
    """
    __version__ = '0.03'
    #: Directory of cache files
    CACHE_DIR = None
    try:
        CACHE_DIR = const.CACHEDIR
    except:
        logger.exception('Pyaerocom cache directory is not defined')
    #: Length of header of cached pickle files (i.e. no of calls of
    #: pickle.load before actual data object is returned)
    LEN_CACHE_HEAD = 6
    def __init__(self, reader, vars_to_retrieve=None, 
                 start=None, stop=None, **kwargs):
    
        self.reader = reader
       
        self.vars_to_retrieve = vars_to_retrieve
        self._start = start
        self._stop = stop
        
        self.loaded_data = None
        
        #: Flag that is set True if pyaerocom server can be accessed. If this
        #: is the case, potentially pickled files are checked against latest
        #: revision and file available in database, else, pickled match is 
        #: loaded without doublechecking whether the database has changed
        self.connection_established = False
        self.newest_file_in_read_dir = None
        self.newest_file_date_in_read_dir = None
        
        try:# get latest file in data directory of obs network ...
            newest = max(glob.iglob(os.path.join(self.data_dir, '*')), 
                         key=os.path.getctime)
            self.newest_file_in_read_dir = newest
            
            # ... and corresponding file date
            self.newest_file_date_in_read_dir = os.path.getctime(newest)
            self.connection_established = True
        except IOError as e:
            logger.exception('Failed to establish connection with Aerocom '
                             'server. Error: {}'.format(repr(e)))
       
    @property
    def dataset_to_read(self):
        return self.reader.dataset_to_read
    
    @property
    def data_dir(self):
        return self.reader.DATASET_PATH
    
    @property
    def start(self):
        if self._start is None:
            return 'None'
        return self._start
       
    @start.setter
    def start(self, value):
        self._start = to_datestring_YYYYMMDD(value)
        
    @property
    def stop(self):
        if self._stop is None:
            return 'None'
        return self._stop
    
    @stop.setter
    def stop(self, value):
        self._stop = to_datestring_YYYYMMDD(value)
        
    @property
    def vars_to_retrieve_str(self):
        """Variable query list"""
        if self.vars_to_retrieve is None:
            return 'DefaultVars'
        elif len(self.vars_to_retrieve) == 1:
            return str(self.vars_to_retrieve[0])
        else:
            return 'MultipleVars'
        
    @property
    def file_name(self):
        """File name for query"""
        name = '_'.join([self.dataset_to_read, 
                         self.vars_to_retrieve_str,
                         self.start, 
                         self.stop])
        return name + '.pkl'
       
    @property
    def file_path(self):
        """Full file path of cache file for query"""
        if self.CACHE_DIR is None:
            raise IOError('pyaerocom cache directory is not defined')
        return os.path.join(self.CACHE_DIR, self.file_name)
    
# =============================================================================
#     def _check_pkl_head_vs_databaseOLD(self, in_handle):
#         
#         newest_file_in_read_dir_saved = pickle.load(in_handle)
#         newest_file_date_in_read_dir_saved = pickle.load(in_handle)
#         revision_saved = pickle.load(in_handle)
#         reader_version_saved = pickle.load(in_handle)
#         data_version_saved = pickle.load(in_handle)
#         cacher_version_saved = pickle.load(in_handle)
#         if (newest_file_in_read_dir_saved != self.newest_file_in_read_dir
#             or newest_file_date_in_read_dir_saved != self.newest_file_date_in_read_dir
#             or revision_saved != self.reader.data_revision
#             or reader_version_saved != self.reader.__version__
#             or data_version_saved != UngriddedData.__version__
#             or cacher_version_saved != self.__version__):
#             return False
#         return True
# =============================================================================
    
    def _check_pkl_head_vs_database(self, in_handle):
        if not pickle.load(in_handle) == self.newest_file_in_read_dir:
            const.print_log.info('Latest file in cached object is outdated')
            return False
        elif not pickle.load(in_handle) == self.newest_file_date_in_read_dir:
            const.print_log.info('Latest file date in cached object is outdated')
            return False
        elif not pickle.load(in_handle) == self.reader.data_revision:
            const.print_log.info('Data revision in cached object is outdated')
            return False
        elif not pickle.load(in_handle) == self.reader.__version__:
            const.print_log.info('Reader class version in cached object is outdated')
            return False
        elif not pickle.load(in_handle) == UngriddedData.__version__:
            const.print_log.info('UngriddedData class in cached object is outdated')
            return False
        elif not pickle.load(in_handle) == self.__version__:
            const.print_log.info('Cacherloader version in cached object is outdated')
            return False
        return True
    
    def check_and_load(self):
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
            if not os.path.isfile(self.file_path):
                logger.info('No cache file available for query of dataset '
                            '{}'.format(self.dataset_to_read))
                return False
        except IOError as e:
            logger.warning(repr(e))
            return False
        
        delete_existing = const.RM_CACHE_OUTDATED
                
        in_handle = open(self.file_path, 'rb')
        # read meta information about file
        if self.connection_established:
            try:
                use_cache_file = self._check_pkl_head_vs_database(in_handle)
            except Exception as e:
                use_cache_file = False
                delete_existing = True
                logger.exception('File error in cached data file {}. File will '
                                 'be removed and data reloaded'
                                 'Error: {}'.format(self.file_path,
                                         repr(e)))
            if not use_cache_file:
                # TODO: Should we delete the cache file if it is outdated ???
                logger.info('Aborting reading cache file {}. Aerocom database '
                            'or pyaerocom version has changed compared to '
                            'cached version'
                            .format(self.file_name))
                in_handle.close()
                if delete_existing: #something was wrong
                    const.print_log.info('Deleting outdated cache file: {}'
                                         .self.file_path)
                    os.remove(self.file_path)
                return False
        else:
            for k in range(self.LEN_CACHE_HEAD):
                logger.debug(pickle.load(in_handle))
        
        # everything is okay
        data = pickle.load(in_handle)
        if not isinstance(data, UngriddedData):
            raise TypeError('Unexpected data type stored in cache file, need '
                            'instance of UngriddedData, got {}'.format(type(data)))
        self.loaded_data = data
        logger.info('Successfully loaded data for {} from Cache'.format(self.dataset_to_read))
        return True
    
    def write(self, data):
        """Write instance of UngriddedData to cache
        
        Parameters
        ----------
        data : UngriddedData
            object containing the data
        """
        if not self.connection_established:
            # TODO: may be updated in the future
            raise AerocomConnectionError('Cannot write Cache file, connection '
                                         'to Aerocom database could not be '
                                         'established (required for checking '
                                         'revision)')
        if not isinstance(data, UngriddedData):
            raise TypeError('Invalid input, need instance of UngriddedData, '
                            'got {}'.format(type(data)))
        logger.info('Writing cache file: {}'.format(self.file_path))
        success=True
        # OutHandle = gzip.open(c__cache_file, 'wb') # takes too much time
        out_handle = open(self.file_path, 'wb')
        try:
            pickle.dump(self.newest_file_in_read_dir, out_handle, 
                        pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.newest_file_date_in_read_dir, out_handle, 
                        pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.reader.data_revision, out_handle, 
                        pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.reader.__version__, out_handle, 
                        pickle.HIGHEST_PROTOCOL)
            pickle.dump(UngriddedData.__version__, out_handle, 
                        pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.__version__, out_handle, 
                        pickle.HIGHEST_PROTOCOL)
            pickle.dump(data, out_handle, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            from pyaerocom import print_log
            print_log.exception('Failed to write cache'.format(repr(e)))
            success=False
        finally:    
            out_handle.close()
            if not success:
                os.remove(self.file_path)
        
        logger.info('Success!')
        
if __name__ == "__main__":
    from time import time
    import pyaerocom as pya
    
    reader = pya.io.ReadUngridded('AeronetSDAV3Lev2.daily', 
                                  vars_to_retrieve=['od550lt1aer', 
                                                    'od550gt1aer'])
    t0=time()
    data = reader.read()
    t1=time()
    data = reader.read()
    print(t1 - t0)
    print(time()-t1)
    