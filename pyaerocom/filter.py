#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 09:03:31 2018

@author: jonasg
"""

import os
import glob 
      
from pyaerocom import logger, print_log
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.griddeddata import GriddedData
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.region import Region

from pyaerocom.land_sea_mask import download_mask

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
        """Set default altitude filter."""
        if not filter_name in self.LAND_OCN_FILTERS:
            raise AttributeError('No such land sea filter: {}. Available '
                                 'filters are: {}'.format(filter_name, 
                                               self.LAND_OCN_FILTERS))
        self.land_ocn = filter_name
        return         
        
    def set_altitude_filter(self, filter_name):
        """Set default altitude filter."""
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
        """Sets default region, WORLD."""
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
        """ Checks if htap masks are available and downloades the regions 
        that is not. Usefull if someone accudentaly deletes one region. 
        """
        from pyaerocom import const
        path = const.FILTERMASKKDIR
        
        if not os.path.exists(path):
            const.print_log.info('Creating mask directory at {}'.format(path))
            os.mkdir(path)
        
        # ToDo: check for actual number of masks and not len == 0 (there may 
        # be new masks in the future)
        files = glob.glob(os.path.join(path, '*.nc'))
        nbr_files = len(files)
        
        if nbr_files != 19:
            files = glob.glob(os.path.join(path, '*.nc'))
            
            available_regions = []
            missing_reg = []
            
            for b in files:
                temp = b.split('htap')[0]
                reg = temp.split('/')[-1]
                available_regions.append(reg)
        
            for reg in pya.const.HTAP_REGIONS:
                if not reg in available_regions:
                    missing_reg.append(reg)
            
            const.logger.info('Mask directory exists but does not contain '
                  'all available masks. Downloads {}.'.format(missing_reg))                            
            download_mask(missing_reg)
            return
        const.logger.info('Masks are available in MyPyaerocom')
    
    
    
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
            
            if isinstance(data_obj, UngriddedData):
                data_obj = self._apply_ungridded(data_obj)
            elif isinstance(data_obj, GriddedData):
                data_obj = self._apply_gridded(data_obj)
            elif isinstance(data_obj, ColocatedData):
                data_obj = self._apply_colocated(data_obj)
            #raise IOError('Cannot filter {} obj, need instance of GriddedData or '
            #              'UngriddedData'.format(type(data_obj)))

            if len(spl) > 2:
                data_obj = data_obj.filter_region(region_id=spl[-1])
 
            return data_obj
        
    def __call__(self, data_obj):
        return self.apply(data_obj)
    
    
if __name__=="__main__":
    import pyaerocom as pya
    import matplotlib.pyplot as plt
    
    #plt.close("all")
    #f = Filter(name = 'EUROPE-noMOUNTAINS-OCN')
    
    #ungridded_data = pya.io.ReadUngridded().read('AeronetSunV3Lev2.daily' , 'od550aer')
    #ungridded_data.plot_station_coordinates(marker = 'o', markersize=12, color='lime')

    #data = pya.io.ReadGridded('ECMWF_CAMS_REAN').read_var('od550aer')
    #data.quickplot_map()
    #data.filter_region(region_id  = 'EUROPE-noMOUNTAINS-OCN')
    #data = f.apply(data)
    #data.quickplot_map()
    #data_coloc = pya.colocation.colocate_gridded_ungridded(data, ungridded_data, ts_type='monthly',
    #                                                       filter_name='WORLD-noMOUNTAINS')
    #data_coloc    
    pya.change_verbosity('info')
    import numpy as np
    #._check_if_htap_region_are_available_and_download()
    
    f = Filter("EAS")

    YEAR = 2010
    VAR = "od550aer"
    TS_TYPE = "daily"
    MODEL_ID = "ECMWF_CAMS_REAN"
    OBS_ID = 'AeronetSunV3Lev2.daily'
    
    model_reader = pya.io.ReadGridded(MODEL_ID)
    model_data = model_reader.read_var(VAR, start=YEAR)
    
    obs_reader = pya.io.ReadUngridded(OBS_ID, [VAR])
    obs_data = obs_reader.read()#.filter_by_meta(altitude=[0, 1000])
    
    f = Filter(name = 'EUROPE-noMOUNTAINS-OCN')
    model_data = f.apply(model_data)
    obs_data   = f.apply(obs_data)
    data_coloc_alt = pya.colocation.colocate_gridded_ungridded(model_data, obs_data, ts_type='monthly',
                                                               filter_name='EUR-noMOUNTAINS-OCN',
                                                               colocate_time=True)
    
    data_coloc_alt.plot_coordinates()#scatter(marker='o', mec='none', color='b', alpha=0.05);
    plt.show()
    
    #data_coloc_alt.plot_station_coordinates()
    #plt.show()
