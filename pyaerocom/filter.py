#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 09:03:31 2018

@author: jonasg
"""
from pyaerocom.utils import BrowseDict
from pyaerocom.griddeddata import GriddedData
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.region import Region

class Filter(BrowseDict):
    """Class that can be used to filter gridded and ungridded data objects
    
    Note
    ----
    BETA version (currently being tested)
    
    Attributes
    ----------
    lon_range : list
        2-element list or array specifying longitude range
    lat_range : list
        2-element list or array specifying latitude range
    alt_range : list
        2-element list or array specifying altitude range
    """
    #: dictionary specifying altitude filters
    ALTITUDE_FILTERS = {'wMOUNTAINS'    :   None, #reserve namespace for
                        'noMOUNTAINS'   :   [-1e6, 1e3]} # 1000 m upper limit

    def __init__(self, name=None, region=None, altitude_filter=None, **kwargs):
        # default name (i.e. corresponds to no filtering)
        self._name = 'WORLD-wMOUNTAINS'
        
        self.lon_range = None
        self.lat_range = None
        self.alt_range = None
        
        if name is not None:
            self.infer_from_name(name)
        else:
            self.infer_from_name(self._name)
            
        if region is not None:
            self.set_region(region)
        if altitude_filter is not None:
            self.set_altitude_filter(altitude_filter)
        
        self.update(**kwargs)
        
    def infer_from_name(self, name):
        """Infer filter from name string
        
        Parameters
        ----------
        name : str
            name string in Aerocom format (e.g. WORLD-wMOUNTAINS)
        
        Raises
        ------
        IOError
            if region and altitude filter cannot be inferred
        """
        if not isinstance(name, str):
            raise IOError('Invalid input for name, need string, got {}'.format(type(name)))
        spl = name.split('-')
        # intitialise
        self.set_region(spl[0])
        if len(spl) > 1:
            alt_filter = spl[1]
        else:
            alt_filter = 'wMOUNTAINS'
        self.set_altitude_filter(alt_filter)
    
    def set_altitude_filter(self, filter_name):
        """Set default altitude filter"""
        if not filter_name in self.ALTITUDE_FILTERS:
            raise AttributeError('No such altitude filter: {}. Available '
                                 'filters are: {}'.format(filter_name, 
                                               self.ALTITUDE_FILTERS.keys()))
        self.alt_range = self.ALTITUDE_FILTERS[filter_name]
        
        spl = self.name.split('-')
        self._name = '{}-{}'.format(spl[0], filter_name)
        
    def set_region(self, region):
        if isinstance(region, str):
            region = Region(region)
        if not isinstance(region, Region):
            raise IOError('Invalid input for region, need string or '
                          'instance of Region class, got {}'.format(region))
        self.lon_range = region.lon_range
        self.lat_range = region.lat_range
        
        spl = self.name.split('-')
        self._name = '{}-{}'.format(region.name, spl[1])
    
    @property
    def name(self):
        return self._name
    
    def _apply_ungridded(self, data_obj):
        """Apply filter to instance of class :class:`UngriddedData`
        """
        return data_obj.filter_by_meta(stat_lon=self.lon_range, 
                                       stat_lat=self.lat_range, 
                                       stat_alt=self.alt_range)
    
    def _apply_gridded(self, data_obj):
        """Apply filter to instance of class :class:`GriddedData`
        """
        raise NotImplementedError
        
    def apply(self, data_obj):
        """Apply filter to data object
        
        Parameters
        ----------
        data_obj : :obj:`UngriddedData`, :obj:`GriddedData`
            input data object that is supposed to be filtered
            
        Returns
        -------
        :obj:`UngriddedData`, :obj:`GriddedData`
            filtered data object
            
        Raises
        ------
        IOError
            if input is invalid
        """
        if isinstance(data_obj, UngriddedData):
            return self._apply_ungridded(data_obj)
        elif isinstance(data_obj, GriddedData):
            return 
        IOError('Cannot filter {} obj, need instance of GriddedData or '
                'UngriddedData'.format(type(data_obj)))
        
    def __call__(self, data_obj):
        return self.apply(data_obj)
    
    
if __name__=="__main__":
    f = Filter('EUROPE-noMOUNTAINS')
    print(f)
    f.set_region('NAMERICA')
    print(f)  
    f.set_altitude_filter('wMOUNTAINS')     
    print(f)