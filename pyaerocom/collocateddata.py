#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 14:55:01 2018

@author: jonasg
"""
from pyaerocom import logger
from pyaerocom.mathutils import calc_statistics
from pyaerocom.helpers import to_datestring_YYYYMMDD
from pyaerocom.exceptions import DataDimensionError
from pyaerocom.plot.plotscatter_new import plot_scatter
import numpy as np
import os
import xarray

class CollocatedData(object):
    """Class representing collocated and unified data from two sources
    
    Sources may be instances of :class:`UngriddedData` or 
    :class:`GriddedData` that have been compared to each other. 
    
    Note
    ----
    Currently, it is not foreseen, that this object is instantiated from 
    scratch, but it is rather created in and returned by objects / methods
    that perform collocation. 
    The purpose of this object is thus, not the creation of collocated objects,
    but solely the analysis of such data as well as I/O features (e.g. save as
    / read from .nc files, convert to pandas.DataFrame, plot station time 
    series overlays, scatter plots, etc.)
    
    In the current design, such an object comprises 3 dimensions, where the 
    first dimension (depth, index 0) is ALWAYS length 2 and specifies the two
    datasets that were compared
    
    Parameters
    ----------
    data : :obj:`xarray.DataArray` or :obj:`numpy.ndarray` or :obj:`str`, optional
        Collocated data. If str, then it is attempted to be loaded from file.
        Else, it is assumed that data is numpy array and that all further 
        supplementary inputs (e.g. coords, dims) for the 
        instantiation of :class:`DataArray` is provided via **kwargs. I
    **kwargs
        Additional keyword args that are passed to init of :class:`DataArray` 
        in case input :arg:`data` is numpy array.
        
    Raises
    ------
    IOError
        if init fails
    """
    def __init__(self, data=None, **kwargs):
        self._data = None
        if data is not None:
            # check if input is DataArray and if not, try to create instance
            # of DataArray. If this fails, raise Exception
            if isinstance(data, xarray.DataArray):
                self.data = data
            elif isinstance(data, np.ndarray):
                try:
                    data = xarray.DataArray(data, **kwargs)
                except Exception as e:
                    raise IOError('Failed to initiate DataArray from input.\n'
                                  'Error: {}'.format(repr(e)))
                self.data = data
            elif isinstance(data, str):
                self.open(data)
            else:
                raise IOError('Failed to interpret input {}'.format(data))
                    
    
    @property
    def data(self):
        """Data object (instance of :class:`xarray.DataArray`)"""
        if self._data is None:
            raise AttributeError('No data available in this object')
        return self._data
    
    @data.setter
    def data(self, val):
        if not isinstance(val, xarray.DataArray):
            raise IOError('Invalid input for data attribute, need instance '
                             'of xarray.DataArray')
        if self._data is not None:
            logger.warning('Overwriting existing data in CollocatedData object')
        self._data = val
    
    @property
    def name(self):
        """Name of data (should be variable name)"""
        return self.data.name
    
    @name.setter
    def name(self, val):
        self.data.name = val
        
    @property
    def ndim(self):
        """Dimension of data array"""
        return self.data.ndim
    
    @property
    def shape(self):
        """Shape of data array"""
        return self.data.shape
    
    @property
    def longitude(self):
        """Array of longitude coordinates"""
        if not 'longitude' in self.data:
            raise AttributeError('CollocatedData does not include longitude '
                                 'coordinate')
        return self.data.longitude
    
    @property
    def latitude(self):
        """Array of latitude coordinates"""
        if not 'latitude' in self.data:
            raise AttributeError('CollocatedData does not include latitude '
                                 'coordinate')
        return self.data.latitude
    
    @property
    def time(self):
        """Array containing time stamps"""
        if not 'time' in self.data:
            raise AttributeError('CollocatedData does not include time'
                                 'coordinate')
        return self.data.time
    
    @property
    def start(self):
        """Start datetime of data"""
        return self.time.values[0]
    
    @property
    def stop(self):
        """Stop datetime of data"""
        return self.time.values[-1]
    
    @property
    def ts_type(self):
        """String specifying temporal resolution of data"""
        if not "ts_type" in self.meta:
            raise ValueError('Collocated data object does not contain '
                             'information about temporal resolution')
        return self.meta['ts_type']
    
    @property
    def meta(self):
        """Meta data"""
        return self.data.attrs
    
    def calc_statistics(self):
        """Calculate statistics from data ensemble
        
        Wrapper for function :func:`pyaerocom.mathutils.calc_statistics` 
        
        Returns
        -------
        dict
            dictionary containing statistical parameters
        """
        return calc_statistics(self.data.values[1].flatten(),
                               self.data.values[0].flatten())
        
    def plot_scatter(self, **kwargs):
        """Create scatter plot of data"""
        statistics = self.calc_statistics()
        meta = self.meta
        
        return plot_scatter(model_vals=self.data.values[1].flatten(), 
                            obs_vals=self.data.values[0].flatten(), 
                            model_id=meta['grid_data_name'], 
                            var_name=meta['var_name'],
                            obs_id=meta['dataset_name'],
                            start=meta['start'], 
                            stop=meta['stop'], 
                            ts_type=meta['ts_type'], 
                            stations_ok=self.shape[2],
                            filter_name=meta['filter_name'], 
                            statistics=statistics, **kwargs)
    
    
    def load_fake_data(self, num_stations=1000, num_tstamps=365):
    
        data = np.empty((2, num_tstamps, num_stations))
        
        # supposed to be like station coordinate, i.e. the final data type
        lons = np.linspace(10, 40, num_stations)
        lats = np.linspace(30, 50, num_stations)
        
        times = np.linspace(1,30, num_tstamps).astype('datetime64[D]')
        
        times = times.astype('datetime64[ns]')
        
        model = np.ones(num_tstamps).reshape((num_tstamps,1)) * np.linspace(1, 2, num_stations)
        
        obs = np.ones(num_tstamps).reshape((num_tstamps,1))*2 * np.linspace(1, 1.5, num_stations)
        
        data[0] = model
        data[1] = obs
        
        meta = {'ts_type'       : 'daily',
                'year'          : 1970, 
                'model_id'      : 'ECMWF_OSUITE',
                'obs_id'        : 'AeronetSunV2L2.daily',
                'var_name'      : 'od550aer',
                'filter_name'   :  'WORLD-noMOUNTAINS'}
        
        arr = xarray.DataArray(data, coords={'source'   : [meta['model_id'],
                                                           meta['obs_id']], 
                                         'time'     : times, 
                                         'longitude': lons,
                                         'latitude' : ('longitude', lats)},
                            dims=['source', 'time', 'longitude'],
                            name=meta['var_name'],
                            attrs=meta)
        self._data = arr
    
    @property
    def save_name_aerocom(self):
        """Default save name for data object following AeroCom convention"""
        start_str = to_datestring_YYYYMMDD(self.start)
        stop_str = to_datestring_YYYYMMDD(self.stop)
        return ('{}_OBS-{}_MOD-{}_{}_{}_{}_{}_COLL'.format(self.name,
                                                        self.meta['obs_id'], 
                                                        self.meta['model_id'],  
                                                        start_str,
                                                        stop_str,
                                                        self.ts_type,
                                                        self.meta['filter_name']))
    
    def to_netcdf(self, out_dir, save_name=None, **kwargs):
        """Save data object as .nc file
        
        Wrapper for method :func:`xarray.DataArray.to_netdcf` 
        Parameters
        ----------
        out_dir : str
            output directory
        save_name : :obj:`str`, optional
            name of file, if None, the default save name is used (cf. 
            :attr:`save_name_aerocom`)
        **kwargs
            additional, optional keyword arguments passed to 
            :func:`xarray.DataArray.to_netdcf` 
            
        """
        if 'path' in kwargs:
            raise IOError('Path needs to be specified using input parameters '
                          'out_dir and save_name')
        if save_name is None:
            save_name = self.save_name_aerocom
        if not save_name.endswith('.nc'):
            save_name = '{}.nc'.format(save_name)
        self.data.to_netcdf(path=os.path.join(out_dir, save_name), **kwargs)
       
    def open(self, file_path):
        """High level helper for reading from supported file sources
        
        Parameters
        ----------
        file_path : str
            file path
        """
        if file_path.endswith('nc'):
            self.read_netcdf(file_path)
            return
        
        raise IOError('Failed to import file {}. File type is not supported '
                      .format(os.path.basename(file_path)))
        
    def read_netcdf(self, file_path):
        """Read data from NetCDF file
        
        Parameters
        ----------
        file_path : str
            file path
            
        """
        self._data = xarray.open_dataarray(file_path)
        
    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}".format(head, len(head)*"-")
        try:
            data_str = str(self.data)
            s += '\nData: {}'.format(data_str)
        except:
            pass
        return s


    
if __name__=="__main__":
    OUT_DIR = '../dev_scripts/out'
    d = CollocatedData()
    d.load_fake_data()
    
    d.to_netcdf(OUT_DIR)
    
    fp = os.path.join(OUT_DIR, d.save_name_aerocom + '.nc')
    
    d1 = CollocatedData(fp)
    print(d1)
    
        
    