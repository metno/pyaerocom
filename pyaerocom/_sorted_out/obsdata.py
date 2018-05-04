#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file could contain classes, that represent observation data. Below are 
some dummies inserted.
"""
from abc import ABCMeta, abstractmethod
 
class ObsData(metaclass=ABCMeta):
    """Abstract base class for observation data
    
    This class could contain everything that all observationals have in common.
    The abstract class interface can be used to ensure the implementation of 
    certain class methods that are required to be implemented in subclasses 
    (declared with @abstractmethod decorator).
    """
    def __init__(self, *args, **kwargs):
        self.data = None
        self.meta = {}
    
    @abstractmethod
    def time_stamps(self):
        """Return array containing time stamps of observations"""
        pass
    
    @abstractmethod
    def longitude(self):
        """Get longitude(s) of data"""
        pass
    
    @abstractmethod
    def latitude(self):
        """Get latitude(s) of data"""
        pass
    
    @abstractmethod
    def import_data(self, file_path):
        """Declaration of abstract data import method
        
        If declared here, it is required to be implemented in subclasses
        """
        pass
        

    
class ProfileData(ObsData):
    """Data object for profile observations
    """
    
    @property
    def time_stamps(self):
        """Returns time stamp array"""
        raise NotImplementedError
    
    def longitude(self):
        raise NotImplementedError
    
    def latitude(self):
        raise NotImplementedError
        
    def import_data(self, file_path):
        print(file_path)
        
    
        
    

class StationData(ObsData):
    pass


if __name__ == "__main__":
    prof = ProfileData()
    # the following won't work since the abstract methods are not yet 
    # implemented in the class
    station = StationData()
    

