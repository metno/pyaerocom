#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 09:03:31 2018

@author: jonasg
"""

import os
import urllib
import glob 
      
from pyaerocom import logger, print_log
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.griddeddata import GriddedData
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.region import Region
#from pyaerocom import const

from pyaerocom.land_sea_mask import (load_region_mask_xr, available_region_mask, 
                                     get_mask, download_mask)

#from pyaerocom.land_sea_mask import load_region_mask_iris, load_region_mask_xr

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

    LAND_OCN_FILTERS = ['LAND', 'OCN']    

    NO_FILTER_NAME = 'WORLD-wMOUNTAINS'
    def __init__(self, name=None, region=None, altitude_filter=None, land_ocn = None, **kwargs):
        # default name (i.e. corresponds to no filtering)
        self._name = self.NO_FILTER_NAME
        self._region = None
        
        self.lon_range = None
        self.lat_range = None
        self.alt_range = None
        self.mask = None
        self.land_ocn = None
        
        if name is not None:
            self.infer_from_name(name)
        else:
            self.infer_from_name(self._name)
            
        if region is not None:
            self.set_region(region)
              
        if land_ocn is not None:
            self.set_land_sea_filter(land_ocn)
            
        if altitude_filter is not None:
            self.set_altitude_filter(altitude_filter)

        self.update(**kwargs)
        
        self._check_if_htap_region_are_available_and_download()
        
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
        
        """
        Expand this to infer from name if you want square region or masks.
        Without the user needs to know the word htap.
        
        if htap --> load the attribute mask, can load lat lon range too since they exist.
        else --> load lat lon range.
        
        """
        # intitialise
        self.set_region(spl[0])
        if len(spl) > 1:
            alt_filter = spl[1]
        else:
            alt_filter = 'wMOUNTAINS'
        if len(spl) > 2: 
            land_sea = spl[2]
            self.set_land_sea_filter(land_sea)
        self.set_altitude_filter(alt_filter)
    
    def set_land_sea_filter(self, filter_name):
        """Set default altitude filter"""
        if not filter_name in self.LAND_OCN_FILTERS:
            raise AttributeError('No such land sea filter: {}. Available '
                                 'filters are: {}'.format(filter_name, 
                                               self.LAND_OCN_FILTERS))
        #self.alt_range = self.LAND_OCN_FILTERS[filter_name]
        self.land_ocn = filter_name
        #spl = self.name.split('-')
        #self._name = '{}-{}-{}'.format(spl[0], filter_name)
        return         
        
    def set_altitude_filter(self, filter_name):
        """Set default altitude filter"""
        if not filter_name in self.ALTITUDE_FILTERS:
            raise AttributeError('No such altitude filter: {}. Available '
                                 'filters are: {}'.format(filter_name, 
                                               self.ALTITUDE_FILTERS.keys()))
        self.alt_range = self.ALTITUDE_FILTERS[filter_name]
        
        spl = self.name.split('-')
        if self.land_ocn:
            self._name = '{}-{}-{}'.format(spl[0], filter_name, self.land_ocn)
        else:
            self._name = '{}-{}'.format(spl[0], filter_name)
        return 
    
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
        
        if self.land_ocn:
            self._name = '{}-{}-{}'.format(region.name, spl[1], self.land_ocn)
        else:
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
                'alt_range' :   self.alt_range, 
                'land_sea'  :   self.land_ocn}
    
    # TODO move this inside the respective classes.
    # Move into respective objects filter_region 
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

    def _check_if_htap_region_are_available_and_download(self):
        
        #path = '/home/hannas/MyPyaerocom/htap_masks/'
        from pyaerocom import const
        #region_list = const.HTAP_REGIONS
        path = const.FILTERMASKKDIR

        if os.path.exists(path):
            # check if htap regions are available in 
            nbr_files = len(glob.glob( os.path.join(path, 'htap_masks') + '*.nc'  ) ) 
            if nbr_files <= 0:
                print("Directory exit but doesn't contain any masks.")
                # download 
                download_mask()
            else:
                print('Masks are available in MyPyaerocom')
                return 
        else:
            # download 
            print("Creates directory {}.".format(path))
            try: 
                os.mkdir(path) 
                download_mask()
            except OSError as error: 
                print(error)     
                return 
        return
    
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
        
        spl = self.name.split('-')
        if self._region.is_htap: 
            # The region object is still "EUROPE" or "EUR".
            if len(spl) > 2:
                r_id = [spl[0], spl[1]]
            else:
                r_id = spl[0]
            return data_obj.filter_region(region_id=r_id) 
            
        else:
            # applies first land and sea mask, then the dquare region mask
            if len(spl) > 2:
                data_obj = data_obj.filter_region(region_id=spl[-1])
                #data_obj.quickplot_map()
                
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
    import pyaerocom as pya
    import matplotlib.pyplot as plt
    plt.close("all")
    f = Filter(name = 'EUR-noMOUNTAINS-OCN')
    # data can either coloc, gridded, ungridded
    #data = f.apply(data)

    #print(f.region)
    #data = pya.io.ReadGridded('ECMWF_CAMS_REAN').read_var('od550aer')

    
    #data.quickplot_map()
    #data.filter_region(region_id  = 'EUROPE-noMOUNTAINS-OCN')



    ungridded_data = pya.io.ReadUngridded().read('EBASMC', 'absc550aer')
    ungridded_data = f.apply(ungridded_data)
    #ungridded_data.plot_station_coordinates(marker = 'o', markersize=12, color='lime')
    
    #ungridded = f.apply(ungridded_data)
    #ungridded_data = f.apply(ungridded_data)
    #ungridded.plot_station_coordinates(marker = 'o', markersize=12, color='lime')
    