#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import abc
from pyaerocom.io.readungriddedbase import ReadUngriddedBase

class ReadAeronetBase(ReadUngriddedBase):
    """Abstract base class template for reading of Aeronet data
    
    Extended abstract base class, derived from low-level base class
    :class:`ReadUngriddedBase` that contains some more functionality
    """
    

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
