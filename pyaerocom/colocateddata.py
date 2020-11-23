#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyaerocom import logger, const
from pyaerocom.mathutils import calc_statistics
from pyaerocom.helpers import to_pandas_timestamp
from pyaerocom.exceptions import (CoordinateError, DataDimensionError,
                                  DataSourceError,
                                  DataExtractionError,
                                  NetcdfError, VarNotAvailableError,
                                  MetaDataError)
from pyaerocom.plot.plotscatter import plot_scatter
from pyaerocom.variable import Variable
from pyaerocom.region import valid_default_region, Region
from pyaerocom.geodesy import get_country_info_coords
from pyaerocom.helpers_landsea_masks import (load_region_mask_xr, get_mask_value)

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
    data : xarray.DataArray or numpy.ndarray or str, optional
        Colocated data. If str, then it is attempted to be loaded from file.
        Else, it is assumed that data is numpy array and that all further
        supplementary inputs (e.g. coords, dims) for the
        instantiation of :class:`DataArray` is provided via **kwargs.
    ref_data_id : str, optional
        ID of reference data
    **kwargs
        Additional keyword args that are passed to init of :class:`DataArray`
        in case input `data` is numpy array.

    Raises
    ------
    IOError
        if init fails
    """
    __version__ = '0.10'
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
    def coords(self):
        """Coordinates of data array"""
        return self.data.coords

    @property
    def dims(self):
        """Names of dimensions"""
        return self.data.dims

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
        if not 'longitude' in self.data.coords:
            raise AttributeError('ColocatedData does not include longitude '
                                 'coordinate')
        return self.data.longitude

    @property
    def latitude(self):
        """Array of latitude coordinates"""
        if not 'latitude' in self.data.coords:
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
    def units(self):
        """Unit of data"""
        try:
            return self.data.attrs['var_units']
        except KeyError:
            logger.warning('Failed to access unit ColocatedData class (may be an '
                        'old version of data)')
    @property
    def unitstr(self):
        unique = []
        u = self.units
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
        const.print_log.warning(DeprecationWarning('OLD NAME: please use num_coords'))
        return self.num_coords

    @property
    def num_coords(self):
        """Total number of lat/lon coordinates"""
        if 'station_name' in self.coords:
            return len(self.data.station_name)

        elif self.ndim == 4:
            if not all([x in self.data.dims for x in ('longitude', 'latitude')]):
                raise AttributeError('Cannot determine grid points. Either '
                                     'longitude or latitude are not contained '
                                     'in 4D data object, which contains the '
                                     'following dimensions: {}'.self.data.dims)
            return len(self.data.longitude) * len(self.data.latitude)
        elif not self.has_time_dim:
            if self.has_latlon_dims:
                return np.prod(self.data[0].shape)
        raise DataDimensionError('Could not infer number of coordinates')

    @property
    def num_coords_with_data(self):
        """Number of lat/lon coordinates that contain at least one datapoint

        Todo
        ----
        check 4D data
        """
        if self.has_time_dim:
            return (self.data[0].count(dim='time') > 0).data.sum()
        # TODO: ADDED IN A RUSH BY JGLISS ON 17.06.2020, check!
        return (self.data[0].count() > 0).data.sum()

    @property
    def has_time_dim(self):
        """Boolean specifying whether data has a time dimension"""
        return True if 'time' in self.dims else False

    @property
    def has_latlon_dims(self):
        """Boolean specifying whether data has latitude and longitude dimensions"""
        return all([dim in self.dims for dim in ['latitude', 'longitude']])

    @property
    def countries_available(self):
        """
        Alphabetically sorted list of country names available

        Raises
        ------
        MetaDataError
            if no country information is available

        Returns
        -------
        list
            list of countries available in these data
        """
        if not 'country' in self.coords:
            raise MetaDataError('No country information available in '
                                'ColocatedData. You may run class method '
                                'check_set_countries to automatically assign '
                                'countries to the station_name coordinate')
        return sorted(dict.fromkeys(self.data['country'].data))

    @property
    def country_codes_available(self):
        """
        Alphabetically sorted list of country codes available

        Raises
        ------
        MetaDataError
            if no country information is available

        Returns
        -------
        list
            list of countries available in these data
        """
        if not 'country_code' in self.coords:
            raise MetaDataError('No country information available in '
                                'ColocatedData. You may run class method '
                                'check_set_countries to automatically assign '
                                'countries to the station_name coordinate')
        return sorted(dict.fromkeys(self.data['country_code'].data))

    @property
    def area_weights(self):
        """
        Wrapper for :func:`calc_area_weights`
        """
        return self.calc_area_weights()

    def get_country_codes(self):
        """
        Get country names and codes for all locations contained in these data

        Raises
        ------
        MetaDataError
            if no country information is available

        Returns
        -------
        dict
            dictionary of unique country names (keys) and corresponding country
            codes (values)
        """
        if not 'country' in self.coords:
            raise MetaDataError('No country information available in '
                                'ColocatedData. You may run class method '
                                'check_set_countries to automatically assign '
                                'countries to the station_name coordinate')
        countries = self.data['country'].data
        codes = self.data['country_code'].data
        return dict(zip(countries, codes))

    def calc_area_weights(self):
        """Calculate area weights

        Note
        ----
        Only applies to colocated data that has latitude and longitude
        dimension.

        Returns
        -------
        ndarray
            array containing weights for each datapoint (same shape as
            `self.data[0]`)
        """
        if not self.has_latlon_dims:
            raise DataDimensionError('Can only compute area weights for data '
                                     'with latitude and longitude dimension')
        if not 'units' in self.data.latitude.attrs:
            self.data.latitude.attrs['units'] = 'degrees'
        if not 'units' in self.data.longitude.attrs:
            self.data.longitude.attrs['units'] = 'degrees'
        arr = self.data
        from pyaerocom import GriddedData
        obs = GriddedData(arr.to_iris())
        return obs.calc_area_weights()

    def min(self):
        return self.data.min()

    def max(self):
        return self.data.max()

    def check_dimensions(self):
        """Checks if data source and time dimension are at the right index

        ToDo
        ----
        Check if this is needed. Little cumbersome at the moment, the data
        object can / should be more flexible! Should
        """
        raise NotImplementedError(DeprecationWarning('This method has been '
                                                     'deprecated in v0.10.0'))

    def resample_time(self, to_ts_type, how='mean',
                      apply_constraints=None, min_num_obs=None,
                      colocate_time=True, inplace=True, **kwargs):
        """Resample time dimension

        Parameters
        ----------
        to_ts_type : str
            new temporal resolution (must be lower than current resolution)

        Returns
        -------
        ColocatedData
            new data object containing resampled data

        Raises
        ------
        TemporalResolutionError
            if input resolution is higher than current resolution
        """
        if inplace:
            col = self
        else:
            col = self.copy()

        # if colocate time is activated, remove datapoints from model, where
        # there is no observation
        if colocate_time:
            mask = np.isnan(col.data[0]).data
            col.data.data[1][mask] = np.nan

        from pyaerocom.time_resampler import TimeResampler

        res = TimeResampler(col.data)
        data_arr = res.resample(to_ts_type=to_ts_type,
                                from_ts_type=col.ts_type,
                                how=how,
                                apply_constraints=apply_constraints,
                                min_num_obs=min_num_obs, **kwargs)

        data_arr.attrs.update(col.meta)
        data_arr.attrs['ts_type'] = str(to_ts_type)

        col.data = data_arr
        col.data.attrs['colocate_time'] = colocate_time
        col.data.attrs.update(res.last_setup)

        return col

    def flatten_latlondim_station_name(self):
        """Stack (flatten) lat / lon dimension into new dimension station_name

        Returns
        -------
        ColocatedData
            new colocated data object with dimension station_name and lat lon
            arrays as additional coordinates
        """
        if not 'latitude' in self.dims or not 'longitude' in self.dims:
            raise AttributeError('Need latitude and longitude dimension')
        elif 'station_name' in self.dims:
            raise AttributeError('Cannot stack lat lon dimensions to new dim '
                                 'station_name as it already exists in data')

        arr = self.stack(station_name=['latitude', 'longitude'],
                         inplace=False).data
        meta = {}
        meta.update(self.meta)
        lats = arr.latitude.values
        lons = arr.longitude.values
        time = arr.time.values
        stridx = [str(x) for x in arr.station_name.values]
        nparr = arr.data

        coords = {
                    'data_source' : meta['data_source'],
                    'time'        : time,
                    'station_name': stridx,
                    'latitude'    : ('station_name', lats),
                    'longitude'   : ('station_name', lons)
        }

        dims = ['data_source', 'time', 'station_name']

        output = ColocatedData(data=nparr, coords=coords, dims=dims,
                               name=self.name, attrs=meta)
        return output

    def stack(self, inplace=False, **kwargs):
        """Stack one or more dimensions

        Parameters
        ----------
        **kwargs
            input arguments passed to :func:`DataArray.stack`

        Returns
        -------
        ColocatedData
            stacked data object

        Example
        -------
        coldata = coldata.stack(latlon=['latitude', 'longitude'])
        """
        if inplace:
            data = self
        else:
            data = self.copy()
        data.data = data.data.stack(**kwargs)
        return data

    def unstack(self, inplace=False, **kwargs):
        """Unstack one or more dimensions

        Parameters
        ----------
        **kwargs
            input arguments passed to :func:`DataArray.unstack`

        Returns
        -------
        ColocatedData
            unstacked data object
        """
        if inplace:
            data = self
        else:
            data = self.copy()
        return data.unstack(**kwargs)

    def get_coords_valid_obs(self):
        """
        Get latitude / longitude coordinates where obsdata is available

        Returns
        -------
        list
            latitute coordinates
        list
            longitude coordinates

        """

        obs = self.data[0]
        if self.ndim == 4:
            stacked = obs.stack(x=['latitude', 'longitude'])
            invalid = stacked.isnull().all(dim='time')
            coords = stacked.x[~invalid].values
            return list(zip(*list(coords)))

        invalid = obs.isnull().all(dim='time')
        return (list(obs.latitude[~invalid].values),
                list(obs.longitude[~invalid].values))

    def _iter_stats(self):
        if not 'station_name' in self.data.dims:
            raise AttributeError('ColocatedData object has no dimension '
                                 'station_name. Consider stacking...')
        if 'latitude' in self.dims and 'longitude' in self.dims:
            raise AttributeError('Cannot init station iter index since '
                                 'latitude and longitude are othorgonal')
        lats = self.data.latitude.values
        lons = self.data.longitude.values
        stats = self.data.station_name.values

        return list(zip(lats, lons, stats))

    def _get_stat_coords(self):
        if self.ndim == 4:
            if not self.has_latlon_dims:
                raise DataDimensionError('Invalid dimensions in 4D ColocatedData')
            lats, lons = self.data.latitude.data, self.data.longitude.data
            coords = np.dstack((np.meshgrid(lats, lons)))
            coords = coords.reshape(len(lats) * len(lons), 2)
            return coords
        if not 'latitude' in self.coords:
            coords = self.data.station_name.data
            if not isinstance(coords[0], tuple) or len(coords[0]) != 2:
                raise ValueError('Cannot infer coordinates...')
            return coords
        return list(zip(self.latitude.data, self.longitude.data))

    def check_set_countries(self, inplace=True, assign_to_dim=None):
        """
        Checks if country information is available and assigns if not

        If not country information is available, countries will be assigned
        for each lat / lon coordinate using
        :func:`pyaerocom.geodesy.get_country_info_coords`.

        Parameters
        ----------
        inplace : bool, optional
            If True, modify and return this object, else a copy.
            The default is True.
        assign_to_dim : str, optional
            name of dimension to which the country coordinate is assigned.
            Default is None, in which case station_name is used.

        Raises
        ------
        DataDimensionError
            If data is 4D (i.e. if latitude and longitude are othorgonal
            dimensions)

        Returns
        -------
        ColocatedData
            data object with countries assigned

        """
        if self.has_latlon_dims:
            raise DataDimensionError('Countries cannot be assigned to 4D'
                                     'ColocatedData with othorgonal lat / lon '
                                     'dimensions. Please consider stacking '
                                     'the latitude and longitude dimensions-')
        if assign_to_dim is None:
            assign_to_dim = 'station_name'

        if not assign_to_dim in self.dims:
            raise DataDimensionError('No such dimension', assign_to_dim)
# =============================================================================
#         if self.has_latlon_dims: #4D data
#             raise NotImplementedError('Cannot yet assign countries to 4D '
#                                       'ColocatedData')
# =============================================================================
        coldata = self if inplace else self.copy()

        if 'country' in coldata.data.coords:
            logger.info('Country information is available')
            return coldata
        coords = coldata._get_stat_coords()

        info = get_country_info_coords(coords)

        countries, codes = [],[]
        for item in info:
            countries.append(item['country'])
            codes.append(item['country_code'])

        arr = coldata.data
        arr = arr.assign_coords(country = (assign_to_dim, countries),
                                country_code=(assign_to_dim, codes))
        coldata.data = arr
        return coldata

    def copy(self):
        """Copy this object"""
        return ColocatedData(self.data.copy())

    def set_zeros_nan(self, inplace=True):
        """
        Replace all 0's with NaN in data

        Parameters
        ----------
        inplace : str, optional
            Whether to modify this object or return a copy. The default is True.

        Returns
        -------
        cd : ColocatedData
            modified data object

        """
        # actual 0 entries in data will be ignored as they can skew the statistics
        # data should not be 0! Even if it's below detection limit or similar (in
        # which case it should be NaN)
        if inplace:
            cd = self
        else:
            cd = self.copy()
        zeros = cd.data.data == 0
        if zeros.any():
            const.print_log.warning("Found 0's in ColocatedData ({},{},{}). "
                                    "These will be set to NaN for web processing"
                                    .format(cd.meta['var_name'][0],
                                            cd.meta['data_source'][0],
                                            cd.meta['data_source'][1]))

            cd.data.data[zeros] = np.nan
        return cd

    def calc_statistics(self, constrain_val_range=False,
                        use_area_weights=False, **kwargs):
        """Calculate statistics from model and obs data

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

        if use_area_weights and not 'weights' in kwargs and self.has_latlon_dims:
            kwargs['weights'] = self.area_weights[0].flatten()
        elif 'weights' in kwargs:
            raise ValueError('Invalid input combination: weights are provided '
                             'but use_area_weights is set to False...')


        stats = calc_statistics(self.data.values[1].flatten(),
                                self.data.values[0].flatten(),
                                **kwargs)

        stats['num_coords_with_data'] = self.num_coords_with_data
        stats['num_coords_tot'] = self.num_coords
        return stats

    def plot_scatter(self, constrain_val_range=False,  **kwargs):
        """Create scatter plot of data

        Parameters
        ----------
        **kwargs
            keyword args passed to :func:`pyaerocom.plot.plotscatter.plot_scatter`

        Returns
        -------
        ax
            matplotlib axes instance
        """
        meta = self.meta
        num_points = self.num_coords_with_data
        vars_ = meta['var_name']

        if constrain_val_range:
            var = Variable(self.meta['var_name'][0])
            kwargs['lowlim_stats'] = var.lower_limit
            kwargs['highlim_stats'] = var.upper_limit

        if vars_[0] != vars_[1]:
            var_ref = vars_[0]
        else:
            var_ref = None
        # ToDo: include option to use area weighted stats in plotting
        # routine...
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
        raise NotImplementedError('Currently not working')
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

    def rename_variable(self, var_name, new_var_name, data_source,
                        inplace=True):
        """Rename a variable in this object

        Parameters
        ----------
        var_name : str
            current variable name
        new_var_name : str
            new variable name
        data_source : str
            name of data source (along data_source dimension)
        inplace : bool
            replace here or create new instance

        Returns
        -------
        ColocatedData
            instance with renamed variable

        Raises
        ------
        VarNotAvailableError
            if input variable is not available in this object
        DataSourceError
            if input data_source is not available in this object
        """
        if not data_source in self.meta['data_source']:
            raise DataSourceError('No such data source {} in ColocatedData'
                                  .format(data_source))
        if not var_name in self.meta['var_name']:
            raise VarNotAvailableError('No such variable {} in ColocatedData'
                                       .format(var_name))

        if inplace:
            obj = self
        else:
            obj = self.copy()
        arr = obj.data
        idx = arr.attrs['data_source'].index(data_source)
        arr.attrs['var_name'][idx] = new_var_name
        if var_name == arr.name:
            arr.name = new_var_name
        obj.data = arr
        return obj

    @staticmethod
    def _aerocom_savename(var_name, obs_id, model_id, start_str,
                          stop_str, ts_type, filter_name):
        return ('{}_REF-{}_MOD-{}_{}_{}_{}_{}'.format(var_name,
                                                      obs_id,
                                                      model_id,
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
        data_ref_id = source_info[0]
        if len(source_info) > 2:
            model_id = 'MultiModels'
        else:
            model_id = source_info[1]
        return self._aerocom_savename(self.name,
                                      data_ref_id,
                                      model_id,
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
        spl = os.path.basename(file_path).split('.nc')[0].split('_')

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
        #model, ts_type_src = mod_base.rsplit('-',1)
        meta['data_source'] = [ref_base, mod_base]
        #meta['ts_type_src'] = ts_type_src
        return meta

    def to_netcdf(self, out_dir, savename=None, **kwargs):
        """Save data object as NetCDF file

        Wrapper for method :func:`xarray.DataArray.to_netdcf`

        Parameters
        ----------
        out_dir : str
            output directory
        savename : str, optional
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
        out = None
        for k, v in self.data.attrs.items():
            if v is None:
                self.data.attrs[k] = 'None'
            elif isinstance(v, bool):
                self.data.attrs[k] = int(v)
            if k == 'min_num_obs' and isinstance(v, dict):
                out = ''
                for to, how in v.items():
                    for fr, num in how.items():
                        out += '{},{},{};'.format(to, fr, num)

        if out is not None:
            self.data.attrs['_min_num_obs'] = out
            self.data.attrs.pop('min_num_obs')
        self.data.to_netcdf(path=os.path.join(out_dir, savename), **kwargs)

    def read_netcdf(self, file_path):
        """Read data from NetCDF file

        Parameters
        ----------
        file_path : str
            file path

        """
        try:
            self.get_meta_from_filename(file_path)
        except Exception as e:
            raise NetcdfError('Invlid file name for ColocatedData: {}.Error: {}'
                              .format(os.path.basename(file_path, repr(e))))
        arr = xarray.open_dataarray(file_path)
        if '_min_num_obs' in arr.attrs:
            info = {}
            for val in arr.attrs['_min_num_obs'].split(';')[:-1]:
                to, fr, num = val.split(',')
                if not to in info:
                    info[to] = {}
                if not fr in info[to]:
                    info[to][fr] = {}
                info[to][fr] = int(num)
            arr.attrs['min_num_obs'] = info
        self.data = arr
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

    def filter_altitude(self, alt_range, inplace=False):
        if not self._check_latlon_coords():
            raise NotImplementedError('Altitude filtering for data with '
                                      'lat and lon dimension is not yet '
                                      'supported')
        filtered = self._filter_altitude_2d(self.data, alt_range)
        filtered.attrs['alt_range'] = alt_range
        if inplace:
            self.data = filtered

            return self
        return ColocatedData(filtered)

    @staticmethod
    def _filter_altitude_2d(arr, alt_range):
        if not 'station_name' in arr.dims:
            raise DataDimensionError('Cannot filter region, require dimension '
                                      'station_name')
        if not list(arr.dims).index('station_name') == 2:
            raise DataDimensionError('station_name must be 3. dimensional index')

        mask = np.logical_and(arr.altitude > alt_range[0],
                              arr.altitude < alt_range[1])

        filtered = arr[:,:,mask]
        return filtered

    def _check_latlon_coords(self):
        _check = ('latitude', 'longitude')
        if not all([x in self.coords for x in _check]):
            raise CoordinateError('Missing latitude or longitude coordinate '
                                  '(or both)')
        elif any([x in self.dims for x in _check]):
            if not all([x in self.dims for x in _check]):
                raise CoordinateError('Only one of latitude / longitude is '
                                      'dimension (require None or both)')
            return False
        return True

    @staticmethod
    def _filter_country_2d(arr, country, use_country_code):
        if not 'country' in arr.coords:
            raise DataDimensionError('Cannot filter country {}. No country '
                                     'information available in DataArray'
                                     .format(country))

        what = 'country' if not use_country_code else 'country_code'
        countries = arr[what]
        country_dims = countries.dims
        # some sanity checking (this can probably be done more elegant using
        # xarray syntax, however, did not manage to use loc, sel, etc since
        # country is not a dimension coordinate)
        assert country_dims[0] == 'station_name'
        assert len(country_dims) == 1

        assert arr.ndim == 3
        assert arr.dims[-1] == 'station_name'
        mask = arr[what] == country
        return arr[:,:,mask]

    @staticmethod
    def _filter_latlon_2d(arr, lat_range, lon_range):

        if not 'station_name' in arr.dims:
            raise DataDimensionError('Cannot filter region, require dimension '
                                      'station_name')

        if not list(arr.dims).index('station_name') == 2:
            raise DataDimensionError('station_name must be 3. dimensional index')

        mask = (np.logical_and(arr.longitude > lon_range[0],
                               arr.longitude < lon_range[1]) &
                np.logical_and(arr.latitude > lat_range[0],
                               arr.latitude < lat_range[1]))

        return arr[:,:,mask]

    @staticmethod
    def _filter_latlon_3d(arr, lat_range, lon_range):
        if not isinstance(lat_range, slice):
            lat_range = slice(lat_range[0], lat_range[1])
        if not isinstance(lon_range, slice):
            lon_range = slice(lon_range[0], lon_range[1])

        return arr.sel(dict(latitude=lat_range, longitude=lon_range))

    def apply_country_filter(self, region_id, use_country_code=False,
                             inplace=False):
        is_2d = self._check_latlon_coords()
        if is_2d:
            filtered = self._filter_country_2d(self.data, region_id,
                                               use_country_code)
        else:
            raise NotImplementedError('Cannot yet filter')
        if inplace:
            self.data = filtered
            return self
        return ColocatedData(filtered)

    def apply_latlon_filter(self, lat_range=None, lon_range=None,
                            region_id=None, inplace=False):
        """Apply regional filter

        Returns new object filtered for input coordinate range

        Parameters
        ----------
        lat_range : list, optional
            latitude range that is supposed to be applied. If specified, then
            also lon_range need to be specified, else, region_id is checked
            against AeroCom default regions (and used if applicable)
        lon_range : list, optional
            longitude range that is supposed to be applied. If specified, then
            also lat_range need to be specified, else, region_id is checked
            against AeroCom default regions (and used if applicable)
        region_id : str
            name of region to be applied. If provided (i.e. not None) then
            input args `lat_range` and `lon_range` are ignored

        Returns
        -------
        ColocatedData
            filtered data object
        """
        is_2d = self._check_latlon_coords()

        if region_id is not None:
            reg = Region(region_id)
            lon_range = reg.lon_range
            lat_range = reg.lat_range
            region_id = reg.name

        if all([x is None for x in (lat_range, lon_range)]):
            raise ValueError('Please provide input, either for lat_range or '
                             'lon_range or region_id')
        if lon_range is None:
            lon_range = [-180, 180]
        if lat_range is None:
            lat_range = [-90, 90]

        latr, lonr = self.data.attrs['lat_range'], self.data.attrs['lon_range']
        if np.equal(latr, lat_range).all() and np.equal(lonr, lon_range).all():
            const.print_log.info('Filtering of lat_range={} and lon_range={} '
                                 'results in unchanged object, returning self'
                                 .format(lon_range, lat_range))
            return self

        if lat_range[0] < latr[0]:
            lat_range[0] = latr[0]
        if lat_range[1] > latr[1]:
            lat_range[1] = latr[1]
        if lon_range[0] < lonr[0]:
            lon_range[0] = lonr[0]
        if lon_range[1] > lonr[1]:
            lon_range[1] = lonr[1]

        if is_2d:
            filtered = self._filter_latlon_2d(self.data, lat_range, lon_range)
        else:
            filtered = self._filter_latlon_3d(self.data, lat_range, lon_range)

        if not isinstance(region_id, str):
            region_id = 'CUSTOM'
        try:
            alt_info = filtered.attrs['filter_name'].split('-', 1)[-1]
        except Exception:
            alt_info = 'CUSTOM'

        filtered.attrs['filter_name'] = '{}-{}'.format(region_id, alt_info)
        filtered.attrs['region'] = region_id
        filtered.attrs['lon_range'] = lon_range
        filtered.attrs['lat_range'] = lat_range
        if inplace:
            self.data = filtered
            return self
        return ColocatedData(filtered)

    def apply_region_mask(self, region_id, inplace=False):
        """
        Apply a binary regions mask filter to data object. Available binary
        regions IDs can be found at `pyaerocom.const.HTAP_REGIONS`.

        Parameters
        ----------
        region_id : str
            ID of binary regions.
        inplace : bool, optional
            If True, the current instance, is modified, else a new instance
            of `ColocatedData` is created and filtered. The default is False.

        Returns
        -------
        data : ColocatedData
            Filtered data object.

        """

        data = self if inplace else self.copy()

        mask = load_region_mask_xr(region_id)

        if data.ndim == 4:
            data = data.flatten_latlondim_station_name()
        arr = data.data
        drop_idx = []
        for (lat, lon, stat) in data._iter_stats():

            if get_mask_value(lat, lon, mask) < 1:
                drop_idx.append(stat)

        if len(drop_idx) > 0:
            arr = arr.drop(dim='station_name', labels=drop_idx)
        data.data = arr
        return data

    def filter_region(self, region_id, check_mask=True,
                      check_country_meta=False, inplace=False):
        """Filter object by region

        Parameters
        ----------
        region_id : str
            ID of region
        inplace : bool
            if True, the filtering is done directly in this instance, else
            a new instance is returned
        check_mask : bool
            if True and region_id a valid name for a binary mask, then the
            filtering is done based on that binary mask.
        check_country_meta : bool
            if True, then the input region_id is first checked against
            available country names in metadata. If that fails, it is assumed
            that this regions is either a valid name for registered rectangular
            regions or for available binary masks.

        Returns
        -------
        ColocatedData
            filtered data object
        """
        if check_country_meta:
            if region_id in self.countries_available:
                return self.apply_country_filter(region_id,
                                                 use_country_code=False,
                                                 inplace=inplace)

            elif region_id in self.country_codes_available:
                return self.apply_country_filter(region_id,
                                                 use_country_code=True,
                                                 inplace=inplace)

        if region_id in const.HTAP_REGIONS:
            return self.apply_region_mask(region_id, inplace)
        else:
            return self.apply_latlon_filter(region_id=region_id,
                                            inplace=inplace)

    def get_regional_timeseries(self, region_id, **filter_kwargs):
        """
        Compute regional timeseries both for model and obs

        Parameters
        ----------
        region_id : str
            name of region for which regional timeseries is supposed to be
            retrieved
        **filter_kwargs
            additional keyword args passed to :func:`filter_region`.

        Returns
        -------
        dict
            dictionary containing regional timeseries for model (key `mod`)
            and obsdata (key `obs`) and name of region.
        """
        result = {}
        subset = self.filter_region(region_id, inplace=False,
                                    **filter_kwargs)
        if subset.has_latlon_dims:
            rgts = subset.data.mean(dim=('latitude', 'longitude'))
        else:
            rgts = subset.data.mean(dim='station_name')
        result['obs'] = pd.Series(rgts.data[0], rgts.time)
        result['mod'] = pd.Series(rgts.data[1], rgts.time)
        result['region'] = region_id
        return result

    def calc_nmb_array(self):
        """Calculate data array with normalised bias (NMB) values

        Returns
        -------
        DataArray
            NMBs at each coordinate
        """
        _arr = self.data
        mod, obs = _arr[1], _arr[0]
        return (mod - obs).sum('time') / obs.sum('time')

    def plot_coordinates(self, marker='x', markersize=12, fontsize_base=10,
                         **kwargs):

        from pyaerocom.plot.plotcoordinates import plot_coordinates

        lats, lons = self.get_coords_valid_obs()
        return plot_coordinates(lons=lons,
                                lats=lats,
                                marker=marker, markersize=markersize,
                                fontsize_base=fontsize_base, **kwargs)

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
        except Exception:
            pass
        return s

    ### Deprecated (but still supported) stuff
    @property
    def unit(self):
        """Unit of data"""
        const.print_log.warning(DeprecationWarning('Attr. unit is deprecated, '
                                                'please use units instead'))
        return self.units

if __name__=="__main__":

    import matplotlib.pyplot as plt
    import pyaerocom as pya
    plt.close('all')
    coldir = '/home/jonasg/github/aerocom_evaluation/coldata/PIII-optics2019-P/NorESM2-met2010_AP3-CTRL/'
    fname = 'od550csaer_REF-MODIS6.1-aqua_MOD-NorESM2_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc'
    #fname = 'od550csaer_REF-AeronetSun_MOD-NorESM2_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc'

    coldata = ColocatedData(coldir + fname)

    #ts = coldata.get_regional_timeseries('EUROPE')

    from time import time
    t0 = time()
    sub0 = coldata.filter_region('EUROPE')
    dt0 = time() - t0

    stacked = coldata.flatten_latlondim_station_name()

    t1 = time()
    sub1 = stacked.filter_region('EUROPE')
    dt1 = time() - t1

    print('Not stacked: {:.3f} s'.format(dt0))
    print('Stacked: {:.3f} s'.format(dt1))

    #c1 = coldata.check_set_countries(inplace=False)

    #c1.filter_region('Germany', check_country_meta=True, inplace=True)

    #c1.plot_coordinates()
