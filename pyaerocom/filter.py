#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 09:03:31 2018

@author: jonasg
"""
from pyaerocom import logger, print_log
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.griddeddata import GriddedData
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.region import Region

class Filter(BrowseDict):
    """Class that can be used to filter gridded and ungridded data objects
    
    Note
    ----
    BETA version (currently being tested)
    
    Todo
    ----
    Include also temporal filtering and other filter options (e.g. variable, 
    etc.)
    
    Attributes
    ----------
    lon_range : list
        2-element list or array specifying longitude range
    lat_range : list
        2-element list or array specifying latitude range
    alt_range : list
        2-element list or array specifying altitude range
        
    Example
    -------
    >>> import pyaerocom as pya
    >>> data = pya.io.ReadGridded('ECMWF_OSUITE').read_var('od550aer')
    >>> data
    pyaerocom.GriddedData
    Grid data: <iris 'Cube' of Aerosol optical depth at 550 nm / (1) (time: 3287; latitude: 161; longitude: 320)>
    >>> regfilter = pya.Filter('EUROPE-noMOUNTAINS')
    >>> data_filtered = regfilter(data)
    >>> data_filtered
    pyaerocom.GriddedData
    Grid data: <iris 'Cube' of Aerosol optical depth at 550 nm / (1) (time: 3287; latitude: 45; longitude: 80)>
    """
    #: dictionary specifying altitude filters
    ALTITUDE_FILTERS = {'wMOUNTAINS'    :   None, #reserve namespace for
                        'noMOUNTAINS'   :   [-1e6, 1e3]} # 1000 m upper limit
    NO_FILTER_NAME = 'WORLD-wMOUNTAINS'
    def __init__(self, name=None, region=None, altitude_filter=None, **kwargs):
        # default name (i.e. corresponds to no filtering)
        self._name = self.NO_FILTER_NAME
        self._region = None
        
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
        self._region = region
        
        spl = self.name.split('-')
        self._name = '{}-{}'.format(region.name, spl[1])
    
    @property
    def region_name(self):
        return self._region.name
    
    @property
    def name(self):
        return self._name
    
    def to_dict(self):
        """Convert filter to dictionary"""
        return {'region'    :   self.region_name, 
                'lon_range' :   self.lon_range,
                'lat_range' :   self.lat_range,
                'alt_range' :   self.alt_range}
        
    def _apply_ungridded(self, data_obj):
        """Apply filter to instance of class :class:`UngriddedData`
        """
        return data_obj.filter_by_meta(longitude=self.lon_range,
                                       latitude=self.lat_range,
                                       altitude=self.alt_range)
    
    def _apply_gridded(self, data_obj):
        """Apply filter to instance of class :class:`GriddedData`
        """
        print_log.warning('Applying regional cropping in GriddedData using Filter '
                       'class. Note that this does not yet include potential '
                       'cropping in the vertical dimension. Coming soon...')
        return data_obj.crop(region=self._region)
    
    def _apply_colocated(self, data_obj):
        print_log.warning('Applying regional cropping in ColocatedData using Filter '
                       'class. Note that this does not yet include potential '
                       'cropping in the vertical dimension. Coming soon...')
        return data_obj.apply_latlon_filter(region_id=self.region_name)
        
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
        if self.name == self.NO_FILTER_NAME:
            logger.info('NO FILTER flag: {} -> no filtering will be applied '
                        'in {}. Returning unchanged object.'
                        .format(self.NO_FILTER_NAME, type(data_obj)))
            return data_obj
        if isinstance(data_obj, UngriddedData):
            return self._apply_ungridded(data_obj)
        elif isinstance(data_obj, GriddedData):
            return self._apply_gridded(data_obj)
        elif isinstance(data_obj, ColocatedData):
            return self._apply_colocated(data_obj)
        raise IOError('Cannot filter {} obj, need instance of GriddedData or '
                'UngriddedData'.format(type(data_obj)))
      
    def __call__(self, data_obj):
        return self.apply(data_obj)
    
    
if __name__=="__main__":
    f = Filter('EUROPE-wMOUNTAINS')
    print(f)
    f.set_region('NAMERICA')
    print(f)  
    f.set_altitude_filter('noMOUNTAINS')     
    print(f.to_dict())
    