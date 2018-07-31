#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Caching class for reading and writing of ungridded data Cache objects
"""
from pyaerocom import const, logger, UngriddedData
from pyaerocom.helpers import to_datestring_YYYYMMDD
import glob, os, pickle

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
    CACHE_DIR = const.OBSDATACACHEDIR
    def __init__(self, reader, vars_to_retrieve=None, 
                 start=None, stop=None, **kwargs):
    
        self.reader = reader
       
        self.vars_to_retrieve = vars_to_retrieve
        self._start = start
        self._stop = stop
        
        self.loaded_data = None
        
        # get latest file in data directory of obs network ...
        newest = max(glob.iglob(os.path.join(self.data_dir, '*')), 
                     key=os.path.getctime)
        self.newest_file_in_read_dir = newest
        
        # ... and corresponding file date
        self.newest_file_date_in_read_dir = os.path.getctime(newest)
       
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
        return os.path.join(self.CACHE_DIR, self.file_name)
    
    def check_and_load(self):
        if not os.path.isfile(self.file_path):
            logger.info('No cache file available for query of dataset '
                        '{}'.format(self.dataset_to_read))
            return False
    
        in_handle = open(self.file_path, 'rb')
        # read meta information about file
        newest_file_in_read_dir_saved = pickle.load(in_handle)
        newest_file_date_in_read_dir_saved = pickle.load(in_handle)
        revision_saved = pickle.load(in_handle)
        object_version_saved = pickle.load(in_handle)
        if (newest_file_in_read_dir_saved != self.newest_file_in_read_dir
            or newest_file_date_in_read_dir_saved != self.newest_file_date_in_read_dir
            or revision_saved != self.reader.data_revision
            or object_version_saved != self.reader.__version__):
            in_handle.close()
            return False
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
        if not isinstance(data, UngriddedData):
            raise TypeError('Invalid input, need instance of UngriddedData, '
                            'got {}'.format(type(data)))
        logger.info('Writing cache file: {}'.format(self.file_path))
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
            pickle.dump(data, out_handle, pickle.HIGHEST_PROTOCOL)
        except:
            logger.exception('Failed to write cache')
        finally:    
            out_handle.close()
        
        logger.info('Success!')