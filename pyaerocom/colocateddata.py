#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyaerocom import logger
from pyaerocom.mathutils import calc_statistics
from pyaerocom.helpers import to_pandas_timestamp
from pyaerocom.exceptions import DataDimensionError, NetcdfError
from pyaerocom.plot.plotscatter import plot_scatter
from pyaerocom.variable import Variable
import numpy as np
import pandas as pd
import os
import xarray

class ColocatedData(object):
    """Class representing colocated and unified data from two sources
    
    Sources may be instances of :class:`UngriddedData` or 
    :class:`GriddedData` that have been compared to each other. 
    
    Note
    ----
    Currently, it is not foreseen, that this object is instantiated from 
    scratch, but it is rather created in and returned by objects / methods
    that perform colocation.
    The purpose of this object is thus, not the creation of colocated objects,
    but solely the analysis of such data as well as I/O features (e.g. save as
    / read from .nc files, convert to pandas.DataFrame, plot station time 
    series overlays, scatter plots, etc.)
    
    In the current design, such an object comprises 3 dimensions, where the 
    first dimension (depth, index 0) is ALWAYS length 2 and specifies the two
    datasets that were compared
    
    Parameters
    ----------
    data : :obj:`xarray.DataArray` or :obj:`numpy.ndarray` or :obj:`str`, optional
        Colocated data. If str, then it is attempted to be loaded from file.
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
    __version__ = '0.05'
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
            logger.warning('Overwriting existing data in ColocatedData object')
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
    def data_source(self):
        """Coordinate array containing data sources (z-axis)"""
        return self.data.data_source
    
    @property
    def var_name(self):
        """Coordinate array containing data sources (z-axis)"""
        return self.data.var_name
    
    @property
    def longitude(self):
        """Array of longitude coordinates"""
        if not 'longitude' in self.data:
            raise AttributeError('ColocatedData does not include longitude '
                                 'coordinate')
        return self.data.longitude
    
    @property
    def latitude(self):
        """Array of latitude coordinates"""
        if not 'latitude' in self.data:
            raise AttributeError('ColocatedData does not include latitude '
                                 'coordinate')
        return self.data.latitude
    
    @property
    def time(self):
        """Array containing time stamps"""
        if not 'time' in self.data.dims:
            raise AttributeError('ColocatedData does not include time'
                                 ' coordinate')
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
            raise ValueError('Colocated data object does not contain '
                             'information about temporal resolution')
        return self.meta['ts_type']
    
    @property
    def unit(self):
        """Unit of data"""
        try:
            return self.data.attrs['unit']
        except KeyError:
            logger.warning('Failed to access unit ColocatedData class (may be an '
                        'old version of data)')
    @property
    def unitstr(self):
        unique = []
        u = self.unit
        for val in u:
            if val is None:
                val = 'N/D'
            elif not isinstance(val, str):
                val = str(val)
            if not val in unique:
                unique.append(val)
        return ', '.join(unique)
        
    @property
    def meta(self):
        """Meta data"""
        return self.data.attrs
    
    @property
    def num_grid_points(self):
        """Number of lon / lat grid points that contain data"""
        if not self.check_dimensions():
            raise DataDimensionError('Invalid dimensionality...')
        if self.ndim == 3:
            return self.data.shape[2]
        
        elif self.ndim == 4:
            if not all([x in self.data.dims for x in ('longitude', 'latitude')]):
                raise AttributeError('Cannot determine grid points. Either '
                                     'longitude or latitude are not contained '
                                     'in 4D data object, which contains the '
                                     'following dimensions: {}'.self.data.dims)
            # get all grid points that contain at least one valid data point 
            # along time dimension
            vals = np.nanmean(self.data.data[0], axis=0)
            valid = ~np.isnan(vals)
            return np.sum(valid)
     
    def min(self):
        return self.data.min()
    
    def max(self):
        return self.data.max()
    
    def check_dimensions(self):
        """Checks if data source and time dimension are at the right index"""
        dims = self.data.dims
        if not 2 < len(dims) < 5:
            logger.info('Invalid number of dimensions. Must be 3 or 4')
            return False
        try:
            if dims.index('data_source') == 0 and dims.index('time') == 1:
                return True
            raise Exception
        except:
            return False
        
    def calc_statistics(self, constrain_val_range=False, **kwargs):
        """Calculate statistics from data ensemble
        
        Wrapper for function :func:`pyaerocom.mathutils.calc_statistics` 
        
        Returns
        -------
        dict
            dictionary containing statistical parameters
        """
        if constrain_val_range:
            var = Variable(self.meta['var_name'][1])
            kwargs['lowlim'] = var.lower_limit
            kwargs['highlim'] = var.upper_limit
            
            
        return calc_statistics(self.data.values[1].flatten(),
                               self.data.values[0].flatten(),
                               **kwargs)
        
    
    def plot_scatter(self, constrain_val_range=False,  **kwargs):
        """Create scatter plot of data
        
        Parameters
        ----------
        **kwargs
            keyword args passed to :func:`pyaerocom.plot.plotscatter_new.plot_scatter`
            
        Returns
        -------
        ax 
            matplotlib axes instance
        """
        meta = self.meta
        num_points = self.num_grid_points
        vars_ = meta['var_name']
        
        if constrain_val_range:
            var = Variable(self.meta['var_name'][1])
            kwargs['lowlim_stats'] = var.lower_limit
            kwargs['highlim_stats'] = var.upper_limit
            
        if vars_[0] != vars_[1]:
            var_ref = vars_[0]
        else:
            var_ref = None
        return plot_scatter(x_vals=self.data.values[0].flatten(), 
                            y_vals=self.data.values[1].flatten(),
                            var_name=vars_[1],
                            var_name_ref = var_ref,
                            x_name=meta['data_source'][0],
                            y_name=meta['data_source'][1], 
                            start=self.start, 
                            stop=self.stop, 
                            unit=self.unitstr,
                            ts_type=meta['ts_type'], 
                            stations_ok=num_points,
                            filter_name=meta['filter_name'], 
                            **kwargs)
    
    def _load_fake_data(self, num_stations=1000, num_tstamps=365):
    
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
        
        meta = {'ts_type'         : 'daily',
                'ts_type_src'     : '3hourly',
                'year'            : 1970, 
                'data_source'     : ['AeronetSunV2L2.daily', 'ECMWF_OSUITE'],
                'var_name'        : 'od550aer',
                'filter_name'     :  'WORLD-noMOUNTAINS',
                'data_level'      : 'colocated'}
        
        arr = xarray.DataArray(data, coords={'data_source'   : meta['data_source'], 
                                             'time'     : times, 
                                             'longitude': lons,
                                             'latitude' : ('longitude', lats)},
                                dims=['data_source', 'time', 'longitude'],
                                name=meta['var_name'],
                                attrs=meta)
        self._data = arr
    
    @staticmethod
    def _aerocom_savename(var_name, obs_id, model_id, ts_type_src, start_str, 
                          stop_str, ts_type, filter_name):
        return ('{}_REF-{}_MOD-{}-{}_{}_{}_{}_{}'.format(var_name,
                                                         obs_id, 
                                                         model_id, 
                                                         ts_type_src, 
                                                         start_str, 
                                                         stop_str,
                                                         ts_type,
                                                         filter_name))
    @property
    def savename_aerocom(self):
        """Default save name for data object following AeroCom convention"""
        start_str = self.meta['start_str']
        stop_str = self.meta['stop_str']
        
        source_info = self.meta['data_source']
        ts_type_src = self.meta['ts_type_src']
        data_ref_id = source_info[0]
        if len(source_info) > 2:
            model_id = 'MultiModels'
        else:
            model_id = source_info[1]
        return self._aerocom_savename(self.name,
                                      data_ref_id,
                                      model_id,
                                      ts_type_src,
                                      start_str,
                                      stop_str,
                                      self.ts_type,
                                      self.meta['filter_name'])
        
    @staticmethod
    def get_meta_from_filename(file_path):
        """Get meta information from file name
        
        Note
        ----
        This does not yet include IDs of model and obs data as these should
        be included in the data anyways (e.g. column names in CSV file) and
        may include the delimiter _ in their name.
        
        Returns 
        -------
        dict
            dicitonary with meta information
        """
        spl = os.path.basename(file_path).split('_COLL')[0].split('_')
        
        start = to_pandas_timestamp(spl[-4])
        stop = to_pandas_timestamp(spl[-3])
        
        meta = dict(var_name      = spl[0],
                    ts_type       = spl[-2],  
                    filter_name   = spl[-1],
                    start         = start,
                    stop          = stop)
        
        if not 'REF' in spl[1]:
            raise ValueError('File name does not follow convention')
        ref_base = spl[1].split('REF-')[1]
        mod_base = ''
        in_mod = False
        for item in spl[2:-4]:
            if in_mod:
                mod_base += '_{}'.format(item)
            if item.startswith('MOD-'):
                in_mod=True
                mod_base = item.split('MOD-')[1]
            if not in_mod:
                ref_base += item
        model, ts_type_src = mod_base.rsplit('-',1)
        meta['data_source'] = [ref_base, model]
        meta['ts_type_src'] = ts_type_src
        return meta
            
    def to_netcdf(self, out_dir, savename=None, **kwargs):
        """Save data object as .nc file
        
        Wrapper for method :func:`xarray.DataArray.to_netdcf` 
        Parameters
        ----------
        out_dir : str
            output directory
        savename : :obj:`str`, optional
            name of file, if None, the default save name is used (cf. 
            :attr:`savename_aerocom`)
        **kwargs
            additional, optional keyword arguments passed to 
            :func:`xarray.DataArray.to_netdcf` 
            
        """
        if 'path' in kwargs:
            raise IOError('Path needs to be specified using input parameters '
                          'out_dir and savename')
        if savename is None:
            savename = self.savename_aerocom
        if not savename.endswith('.nc'):
            savename = '{}.nc'.format(savename)
        for k, v in self.data.attrs.items():
            if v is None:
                self.data.attrs[k] = 'None'
        self.data.to_netcdf(path=os.path.join(out_dir, savename), **kwargs)
      
    def read_netcdf(self, file_path):
        """Read data from NetCDF file
        
        Parameters
        ----------
        file_path : str
            file path
            
        """
        data = xarray.open_dataarray(file_path)
        if not 'data_level' in data.attrs or not data.attrs['data_level'] == 'colocated':
            raise NetcdfError('file misses colocated data flag in meta')
        self.data = data
        return self
    
    def to_dataframe(self):
        """Convert this object into pandas.DataFrame
        
        Note
        ----
        This does not include meta information
        """
        logger.warning('This method is currently not completely finished')
        model_vals = self.data.values[1].flatten()
        obs_vals = self.data.values[0].flatten()
        mask = ~np.isnan(obs_vals)
        return pd.DataFrame({'ref'  : obs_vals[mask],
                             'data' : model_vals[mask]})
    
    def from_dataframe(self, df):
        """Create colocated Data object from dataframe
        
        Note
        ----
        This is intended to be used as back-conversion from :func:`to_dataframe`
        and methods that use the latter (e.g. :func:`to_csv`).
        """
        raise NotImplementedError('Coming soon...')
        data = df.to_xarray()
        self.data = data
        self.check_dimensions()
        
        
    def to_csv(self, out_dir, savename=None):
        """Save data object as .csv file
        
        Converts data to pandas.DataFrame and then saves as csv
        
        Parameters
        ----------
        out_dir : str
            output directory
        savename : :obj:`str`, optional
            name of file, if None, the default save name is used (cf. 
            :attr:`savename_aerocom`)
        """
        if savename is None:
            savename = self.savename_aerocom
        if not savename.endswith('.csv'):
            savename = '{}.csv'.format(savename)
        if not self.check_dimensions():
            raise IOError('Invalid dimensionality, please check...')
        df = self.to_dataframe()
        file_path = os.path.join(out_dir, savename)
        df.to_csv(file_path)
        return file_path
        
    def from_csv(self, file_path):
        """Read data from CSV file
        
        Todo
        -----
        Complete docstring
        """
        meta = self.get_meta_from_filename(file_path)
        df = pd.read_csv(file_path)
        self.from_dataframe(df)
        self.data.attrs.update(**meta)
        
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
    
    def __contains__(self, val):
        return self.data.__contains__(val)
    
    def __repr__(self):
        return repr(self.data)
    
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
    
    testdir = '~/pyaerocom/colocated_data/CAM5.3-Oslo_AP3-CTRL2016-PD/'
    testfile = 'od550aer_REF-AeronetSunV3Lev2.daily_MOD-CAM5.3-Oslo_AP3-CTRL2016-PD-monthly_20100101_20101231_monthly_WORLD-noMOUNTAINS_COLL.nc'
    d = ColocatedData()
    
    d.read_netcdf(testdir + testfile)
    #fp = os.path.join(OUT_DIR, d.savename_aerocom + '.nc')
    print(d)
    #d1 = ColocatedData(fp)
    #print(d1)
    
        
    