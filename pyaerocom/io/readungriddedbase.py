#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import abc
import glob, os
import logging

from pyaerocom.io.helpers import get_obsnetwork_dir
from pyaerocom import LOGLEVELS
logger = logging.getLogger(__name__)
# TODO: implement dict-like class for output of read_file method, that avoids 
# creating pandas.Series instances in the first place but keeps the individual 
# data columns
class ReadUngriddedBase(abc.ABC):
    """Abstract base class template for reading of ungridded data"""
    def __init__(self):
        self.data = None #object that holds the loaded data
        self.files = []
        # list that will be updated in read method to store all files that
        # could not be read. It is the responsibility of developers of derived
        # classes to include a try / except block in method read, where the 
        # method read_file is called, and in case of an Exception, append the
        # corresponding file path to this list.
        self.read_failed = []
        # 
        self.logger = logging.getLogger(__name__)
      
    @abc.abstractproperty
    def REVISION_FILE(self):
        """Location of data revision file
        
        Note
        ----
        1. May be implemented as global constant in header of derieved class
        
        """
        pass
    
    @abc.abstractproperty
    def DATASET_NAME(self):
        """Name of dataset (OBS_ID)
        
        Note
        ----
        1. May be implemented as global constant in header of derieved class
        2. May be multiple that can be specified on init (see example below)
        
        """
        pass
    
    @abc.abstractproperty
    def PROVIDES_VARIABLES(self):
        """List of variables that are provided by this dataset
        
        Note
        ----
        May be implemented as global constant in header
        """
        pass
    
    @abc.abstractproperty
    def _FILEMASK(self):
        """Mask for identifying datafiles (e.g. '*.txt')
        
        Note
        ----
        May be implemented as global constant in header
        """
        pass
    
    @abc.abstractproperty
    def __version__(self):
        """Version of reading class
        
        Keep track of changes in derived reading class (e.g. to assess whether 
        potential cache-files are outdated)
        
        Note
        ----
        May be implemented as global constant in header
        """
        pass
    
    
    @property
    def DATASET_PATH(self):
        return get_obsnetwork_dir(self.DATASET_NAME)
     
        
    @abc.abstractmethod
    def read_file(self, filename, vars_to_retrieve=None):
        """Method that reads a single data file and returns the result
        
        Parameters
        ----------
        filename : str
            string specifying filename
        vars_to_retrieve : :obj:`list` or similar, optional,
            list containing variable IDs that are supposed to be read. If None, 
            all variables in :attr:`PROVIDES_VARIABLES` are loaded
        
        Returns
        -------
        dict
            dictionary containing results 
        """
        pass
    
    @abc.abstractmethod
    def read(self, vars_to_retrieve=None, first_file=None, last_file=None):
        """Method that reads a single data file and returns the result
        
        Parameters
        ----------
        vars_to_retrieve : :obj:`list` or similar, optional,
            list containing variable IDs that are supposed to be read. If None, 
            all variables in :attr:`PROVIDES_VARIABLES` are loaded
        first_file : int
            index of first file in file list to read. If None, the very first
            file in the list is used
        last_file : int
            index of last file in list to read. If None, the very last file 
            in the list is used
            
        Returns
        -------
        UngriddedData
            data object
        """
        pass

    ### Concrete implementations of methods that are the same for all (or most)
    # of the derived reading classes
    def get_file_list(self):
        """Search all files to be read"""
        logger.info('searching for data files. This might take a while...')
        self.files = glob.glob(os.path.join(self.DATASET_PATH, self._FILEMASK))
        return self.files
    
    def read_first_file(self, **kwargs):
        """Read first file returned from :func:`get_file_list`
        
        This method may be used for test purposes. It calls :func:`get
        
        Parameters
        ----------
        **kwargs
            keyword args passed to :func:`read_file` (e.g. vars_to_retrieve)
            
        Returns
        -------
        dict-like
            dictionary or similar containing loaded results from first file
        """
        files = self.files
        if len(files) == 0:
            files = self.get_file_list()
        return self.read_file(files[0], **kwargs)
    
    @property
    def data_revision(self):
        """Revision string from the file Revision.txt in the main data directory
        
        Returns
        -------
        
        """
        try:
            revision_file = os.path.join(self.DATASET_PATH, self.REVISION_FILE)
            if os.path.isfile(revision_file):
                with open(revision_file, 'rt') as in_file:
                    revision = in_file.readline().strip()
                    in_file.close()
    
                return revision
        except Exception as e:
            raise IOError("Failed to access revision info for dataset {}. "
                          "Error message: {}".format(self.DATASET_NAME,
                                          repr(e)))
    @property
    def verbosity_level(self):
        """Current level of verbosity of logger"""
        return self.logger.level
    
    @verbosity_level.setter
    def verbosity_level(self, val):
        if isinstance(val, str):
            if not val in LOGLEVELS:
                raise ValueError("Invalid input for loglevel")
            val = LOGLEVELS[val]
        self.logger.setLevel(val)
        
if __name__=="__main__":
    
    from pyaerocom import const
    class ReadUngriddedImplementationExample(ReadUngriddedBase):
        _FILEMASK = ".txt"
        DATASET_NAME = "Blaaa"
        __version__ = "0.01"
        PROVIDES_VARIABLES = ["od550aer"]
        REVISION_FILE = const.REVISION_FILE
        
        def __init__(self, dataset_to_read=None):
            if dataset_to_read is not None:
                self.DATASET_NAME = dataset_to_read
        
        def read(self):
            raise NotImplementedError
            
        def read_file(self):
            raise NotImplementedError
            
    c = ReadUngriddedImplementationExample(dataset_to_read='AeronetSunV2Lev1.5.daily')
    print(c.DATASET_PATH)
