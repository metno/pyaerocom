#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ast import literal_eval
import numpy as np
import pandas as pd
from pathlib import Path
import os
import xarray

from pyaerocom import logger, const
from pyaerocom.mathutils import calc_statistics
from pyaerocom.helpers import (to_pandas_timestamp,to_datestring_YYYYMMDD,
                               isnumeric)
from pyaerocom.exceptions import (CoordinateError, DataDimensionError,
                                  DataCoverageError,
                                  DataSourceError,
                                  NetcdfError, VarNotAvailableError,
                                  MetaDataError)
from pyaerocom.plot.plotscatter import plot_scatter
from pyaerocom.region_defs import REGION_DEFS
from pyaerocom.region import Region
from pyaerocom.geodesy import get_country_info_coords
from pyaerocom.helpers_landsea_masks import (load_region_mask_xr,
                                             get_mask_value)

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
    series overlays, scatter plots, etc.).

    In the current design, such an object comprises 3 or 4 dimensions, where
    the first dimension (`data_source`, index 0) is ALWAYS length 2 and
    specifies the two datasets that were co-located (index 0 is obs, index 1
    is model). The second dimension is `time` and in case of 3D colocated data
    the 3rd dimension is `station_name` while for 4D colocated data the 3rd and
    4th dimension are latitude and longitude, respectively.

    3D colocated data is typically created when a model is colocated with
    station based ground based observations (
    cf :func:`pyaerocom.colocation.colocate_gridded_ungridded`) while 4D
    colocated data is created when a model is colocated with another model or
    satellite observations, that cover large parts of Earth's surface (other
    than discrete lat/lon pairs in the case of ground based station locations).

    Parameters
    ----------
    data : xarray.DataArray or numpy.ndarray or str, optional
        Colocated data. If str, then it is attempted to be loaded from file.
        Else, it is assumed that data is numpy array and that all further
        supplementary inputs (e.g. coords, dims) for the
        instantiation of :class:`DataArray` is provided via **kwargs.
    **kwargs
        Additional keyword args that are passed to init of :class:`DataArray`
        in case input `data` is numpy array.

    Raises
    ------
    IOError
        if init fails
    """
    __version__ = '0.11'
    def __init__(self, data=None, **kwargs):
        self._data = None
        if data is not None:
            if isinstance(data, Path):
                # make sure path is str instance
                data = str(data)
            if isinstance(data, str):
                self.open(data)
            elif isinstance(data, xarray.DataArray):
                self.data = data
            elif isinstance(data, np.ndarray):
                if not data.ndim in (3,4):
                    raise DataDimensionError(
                        'invalid input, need 3D or 4D numpy array'
                        )
                elif not data.shape[0] == 2:
                    raise DataDimensionError(
                        'first dimension (data_source) must be of length 2'
                        '(obs, model)')
                data = xarray.DataArray(data, **kwargs)
                self.data = data
            else:
                raise ValueError(f'Failed to interpret input {data}')

    @property
    def data(self):
        """:class:`xarray.DataArray` containing colocated data

        Raises
        ------
        AttributeError
            if data is not available

        Returns
        -------
        xarray.DataArray
            array containing colocated data and metadata (in fact, there is no
            additional attributes to `ColocatedData` and everything is contained
            in :attr:`data`).
        """
        if self._data is None:
            raise AttributeError('No data available in this object')
        return self._data

    @data.setter
    def data(self, val):
        if not isinstance(val, xarray.DataArray):
            raise ValueError('Invalid input for data attribute, need instance '
                          'of xarray.DataArray')
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
    def lon_range(self):
        """Longitude range covered by this data object"""
        lons = self.longitude.values
        return (np.nanmin(lons), np.nanmax(lons))

    @property
    def latitude(self):
        """Array of latitude coordinates"""
        if not 'latitude' in self.data.coords:
            raise AttributeError('ColocatedData does not include latitude '
                                 'coordinate')
        return self.data.latitude

    @property
    def lat_range(self):
        """Latitude range covered by this data object"""
        lats = self.latitude.values
        return (np.nanmin(lats), np.nanmax(lats))

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
        if not "ts_type" in self.metadata:
            raise ValueError('Colocated data object does not contain '
                             'information about temporal resolution')
        return self.metadata['ts_type']

    @property
    def units(self):
        """Unit of data"""
        return self.data.attrs['var_units']

    @property
    def unitstr(self):
        """String representation of obs and model units in this object"""
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
    def metadata(self):
        """Meta data dictionary (wrapper to :attr:`data.attrs`"""
        return self.data.attrs

    @property
    def num_coords(self):
        """Total number of lat/lon coordinate pairs"""
        obj = self.flatten_latlondim_station_name() if self.has_latlon_dims else self
        if not 'station_name' in obj.coords:
            raise DataDimensionError('Need dimension station_name')
        elif not obj.ndim == 3:
            raise DataDimensionError(
                'Number of coordinates can only be retrieved for 3D data'
                )
        return len(obj.data.station_name)

    @property
    def num_coords_with_data(self):
        """Number of lat/lon coordinate pairs that contain at least one datapoint

        Note
        ----
        Occurrence of valid data is only checked for obsdata (first index in
        data_source dimension).
        """
        obj = self.flatten_latlondim_station_name() if self.has_latlon_dims else self
        if not 'station_name' in obj.coords:
            raise DataDimensionError('Need dimension station_name')
        elif not obj.ndim == 3:
            raise DataDimensionError(
                'Number of coordinates can only be retrieved for 3D data'
                )
        obs = obj.data[0]
        if obj.has_time_dim:
            return (obs.count(dim='time') > 0).data.sum()
        return (obs.count() > 0).data.sum()

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
        """
        Wrapper for :func:`xarray.DataArray.min` called from :attr:`data`

        Returns
        -------
        xarray.DataArray
            minimum of data

        """
        return self.data.min()

    def max(self):
        """
        Wrapper for :func:`xarray.DataArray.max` called from :attr:`data`

        Returns
        -------
        xarray.DataArray
            maximum of data

        """
        return self.data.max()

    def resample_time(self, to_ts_type, how=None,
                      apply_constraints=None, min_num_obs=None,
                      colocate_time=False, inplace=False, **kwargs):
        """
        Resample time dimension

        The temporal resampling is done using :class:`TimeResampler`

        Parameters
        ----------
        to_ts_type : str
            desired output frequency.
        how : str or dict, optional
            aggregator used for resampling (e.g. max, min, mean, median). Can
            also be hierarchical scheme via `dict`, similar to `min_num_obs`.
            The default is None.
        apply_constraints : bool, optional
            Apply time resampling constraints. The default is None, in which
            case pyaerocom default is used, that is,
            :attr:`pyaerocom.Config.OBS_APPLY_TIME_RESAMPLE_CONSTRAINTS` (
            which is True by default in pyaerocom < v0.12.0, and probably also
            after that).
        min_num_obs : int or dict, optional
            Minimum number of observations required to resample from current
            frequency (:attr:`ts_type`) to desired output frequency. Only
            relevant if `apply_constraints` evaluates to `True` (NOTE: can also
            happen if `apply_constraints=None`, see prev. point). The default,
            is None in which case the pyaerocom default is used, which
            can be accessed via :attr:`pyaerocom.Config.`OBS_MIN_NUM_RESAMPLE`.
            Note, that the default corresponds to a hierarchical scheme (`dict`,
            pyaerocom < 0.12.0) and similar input is also accepted, e.g. if
            you want ~75% sampling coverage and if the current ts_type is
            `hourly` and output ts_type `monthly` you could input
            `min_num_obs={'monthly': {'daily': 22}, 'daily': {'hourly': 18}}`.
        colocate_time : bool, optional
            If True, the modeldata is invalidated where obs is NaN, before
            resampling. The default is False (updated in v0.11.0, before was
            True).
        inplace : bool, optional
            If True, modify this object directly, else make a copy and resample
            that one. The default is False (updated in v0.11.0, before was
            True).
        **kwargs
            Addtitional keyword args passed to :func:`TimeResampler.resample`.

        Returns
        -------
        ColocatedData
            Resampled colocated data object.

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

        data_arr.attrs.update(col.metadata)
        data_arr.attrs['ts_type'] = str(to_ts_type)

        col.data = data_arr
        col.data.attrs['colocate_time'] = colocate_time
        trs = res.last_setup
        trs['resample_how'] = trs.pop('how')
        col.data.attrs.update(trs)
        return col

    def flatten_latlondim_station_name(self):
        """Stack (flatten) lat / lon dimension into new dimension station_name

        Returns
        -------
        ColocatedData
            new colocated data object with dimension station_name and lat lon
            arrays as additional coordinates
        """
        if not self.has_latlon_dims:
            raise DataDimensionError('Need latitude and longitude dimensions')

        newdims = []
        for dim in self.dims:
            if dim == 'latitude':
                newdims.append('station_name')
            elif dim == 'longitude':
                continue
            else:
                newdims.append(dim)

        arr = self.stack(station_name=['latitude', 'longitude'],
                         inplace=False).data

        arr = arr.transpose(*newdims)
        return ColocatedData(arr)

    def stack(self, inplace=False, **kwargs):
        """Stack one or more dimensions

        For details see :func:`xarray.DataArray.stack`.

        Parameters
        ----------
        inplace : bool
            modify this object or a copy.
        **kwargs
            input arguments passed to :func:`DataArray.stack`

        Returns
        -------
        ColocatedData
            stacked data object
        """
        if inplace:
            data = self
        else:
            data = self.copy()
        data.data = data.data.stack(**kwargs)
        return data

    def unstack(self, inplace=False, **kwargs):
        """Unstack one or more dimensions

        For details see :func:`xarray.DataArray.unstack`.

        Parameters
        ----------
        inplace : bool
            modify this object or a copy.
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
            coords = zip(*list(coords))
        else:
            invalid = obs.isnull().all(dim='time')
            lats = list(obs.latitude[~invalid].values)
            lons = list(obs.longitude[~invalid].values)
            coords = (lats, lons)
        return list(coords)

    def _iter_stats(self):
        """Create a list that can be used to iterate over station dimension

        Returns
        -------
        list
            list containing 3-element tuples, one for each site i, comprising
            (latitude[i], longitude[i], station_name[i]).
        """
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
        """
        Get station coordinates

        Raises
        ------
        DataDimensionError
            if data is 4D and does not have latitude and longitude dimension

        Returns
        -------
        list
            list containing 2 element tuples (latitude, longitude)

        """
        if self.ndim == 4:
            if not self.has_latlon_dims:
                raise DataDimensionError('Invalid dimensions in 4D ColocatedData')
            lats, lons = self.data.latitude.data, self.data.longitude.data
            coords = np.dstack((np.meshgrid(lats, lons)))
            coords = coords.reshape(len(lats) * len(lons), 2)
        else:
            coords = zip(self.latitude.data, self.longitude.data)
        return list(coords)

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
                                    .format(cd.metadata['var_name'][0],
                                            cd.metadata['data_source'][0],
                                            cd.metadata['data_source'][1]))

            cd.data.data[zeros] = np.nan
        return cd

    def calc_statistics(self, use_area_weights=False, **kwargs):
        """Calculate statistics from model and obs data

        Calculate standard statistics for model assessment. This is done by
        taking all model and obs data points in this object as input for
        :func:`pyaerocom.mathutils.calc_statistics`. For instance, if the
        object is 3D with dimensions `data_source` (obs, model), `time` (e.g.
        12 monthly values) and `station_name` (e.g. 4 sites), then the input
        arrays for model and obs into
        :func:`pyaerocom.mathutils.calc_statistics` will be each of size
        12x4.

        See also :func:`calc_temporal_statistics` and
        :func:`calc_spatial_statistics`.

        Parameters
        ----------
        use_area_weights : bool
            if True and if data is 4D (i.e. has lat and lon dimension), then
            area weights are applied when caluclating the statistics based on
            the coordinate cell sizes. Defaults to False.
        **kwargs
            additional keyword args passed to
            :func:`pyaerocom.mathutils.calc_statistics`

        Returns
        -------
        dict
            dictionary containing statistical parameters
        """
        if use_area_weights and not 'weights' in kwargs and self.has_latlon_dims:
            kwargs['weights'] = self.area_weights[0].flatten()

        nc, ncd = self.num_coords, self.num_coords_with_data
        stats = calc_statistics(self.data.values[1].flatten(),
                                self.data.values[0].flatten(),
                                **kwargs)

        stats['num_coords_tot'] = nc
        stats['num_coords_with_data'] = ncd
        return stats

    def calc_temporal_statistics(self,aggr=None,**kwargs):
        """Calculate *temporal* statistics from model and obs data

        *Temporal* statistics is computed by averaging first the spatial
        dimension(s) (that is, `station_name` for 3D data, and
        `latitude` and `longitude` for 4D data), so that only `data_source` and
        `time` remains as dimensions. These 2D data are then used to calculate
        standard statistics using :func:`pyaerocom.mathutils.calc_statistics`.

        See also :func:`calc_statistics` and
        :func:`calc_spatial_statistics`.

        Parameters
        ----------
        aggr : str, optional
            aggreagator to be used, currently only mean and median are
            supported. Defaults to mean.
        **kwargs
            additional keyword args passed to
            :func:`pyaerocom.mathutils.calc_statistics`

        Returns
        -------
        dict
            dictionary containing statistical parameters
        """
        if aggr is None:
            aggr = 'mean'
        nc, ncd = self.num_coords, self.num_coords_with_data
        if self.ndim == 3:
            dim = 'station_name'
        else:
            dim = ('latitude', 'longitude')

        if aggr == 'mean':
            arr = self.data.mean(dim=dim)
        elif aggr == 'median':
            arr = self.data.median(dim=dim)
        else:
            raise ValueError(
                'So far only mean and median are supported aggregators'
                )
        obs, mod = arr[0].values.flatten(), arr[1].values.flatten()
        stats = calc_statistics(mod, obs, **kwargs)
        stats['num_coords_tot'] = nc
        stats['num_coords_with_data'] = ncd
        return stats

    def calc_spatial_statistics(self,aggr=None,use_area_weights=False,**kwargs):
        """Calculate *spatial* statistics from model and obs data

        *Spatial* statistics is computed by averaging first the time
        dimension and then, if data is 4D, flattening lat / lon dimensions into
        new station_name dimension, so that the resulting dimensions are
        `data_source` and `station_name`. These 2D data are then used to
        calculate standard statistics using
        :func:`pyaerocom.mathutils.calc_statistics`.

        See also :func:`calc_statistics` and
        :func:`calc_temporal_statistics`.

        Parameters
        ----------
        aggr : str, optional
            aggreagator to be used, currently only mean and median are
            supported. Defaults to mean.
        use_area_weights : bool
            if True and if data is 4D (i.e. has lat and lon dimension), then
            area weights are applied when caluclating the statistics based on
            the coordinate cell sizes. Defaults to False.
        **kwargs
            additional keyword args passed to
            :func:`pyaerocom.mathutils.calc_statistics`

        Returns
        -------
        dict
            dictionary containing statistical parameters
        """
        if aggr is None:
            aggr = 'mean'
        if use_area_weights and not 'weights' in kwargs and self.has_latlon_dims:
            weights = self.area_weights[0] #3D (time, lat, lon)
            assert self.dims[1] == 'time'
            kwargs['weights'] = np.nanmean(weights, axis=0).flatten()

        nc, ncd = self.num_coords, self.num_coords_with_data
        # ToDo: find better solution to parse aggregator without if conditions,
        # e.g. xr.apply_ufunc or similar, with core aggregators that are
        # supported being defined in some dictionary in some pyaerocom config
        # module or class. Also aggregation could go into a separate method...
        if aggr == 'mean':
            arr = self.data.mean(dim='time')
        elif aggr == 'median':
            arr = self.data.median(dim='time')
        else:
            raise ValueError(
                'So far only mean and median are supported aggregators'
                )

        obs, mod = arr[0].values.flatten(), arr[1].values.flatten()
        stats = calc_statistics(mod, obs, **kwargs)
        stats['num_coords_tot'] = nc
        stats['num_coords_with_data'] = ncd
        return stats

    def plot_scatter(self, **kwargs):
        """Create scatter plot of data

        Parameters
        ----------
        **kwargs
            keyword args passed to :func:`pyaerocom.plot.plotscatter.plot_scatter`

        Returns
        -------
        Axes
            matplotlib axes instance
        """
        meta = self.metadata
        num_points = self.num_coords_with_data
        try:
            vars_ = meta['var_name']
        except KeyError:
            vars_ = ['N/D', 'N/D']
        try:
            xn, yn = meta['data_source']
        except KeyError:
            xn, yn = 'N/D', 'N/D'

        if vars_[0] != vars_[1]:
            var_ref = vars_[0]
        else:
            var_ref = None
        try:
            tst = meta['ts_type']
        except KeyError:
            tst = 'N/D'
        try:
            fn = meta['filter_name']
        except KeyError:
            fn = 'N/D'
        try:
            unit = self.unitstr
        except KeyError:
            unit = 'N/D'

        # ToDo: include option to use area weighted stats in plotting
        # routine...
        return plot_scatter(x_vals=self.data.values[0].flatten(),
                            y_vals=self.data.values[1].flatten(),
                            var_name=vars_[1],
                            var_name_ref = var_ref,
                            x_name=xn,
                            y_name=yn,
                            start=self.start,
                            stop=self.stop,
                            unit=unit,
                            ts_type=tst,
                            stations_ok=num_points,
                            filter_name=fn,
                            **kwargs)

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
        if not data_source in self.metadata['data_source']:
            raise DataSourceError('No such data source {} in ColocatedData'
                                  .format(data_source))
        if not var_name in self.metadata['var_name']:
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
        # ToDo: start_str and stop_str should actually be decorator attributes
        # and not set in metadata, but this will need some checking in the
        # web tools, regarding the file conventions of the stored NetCDF files
        # needs also updates in colocation.py
        try:
            start_str = self.metadata['start_str']
        except KeyError:
            start_str = to_datestring_YYYYMMDD(self.start)
            self.metadata['start_str'] = start_str
        try:
            stop_str = self.metadata['stop_str']
        except KeyError:
            stop_str = to_datestring_YYYYMMDD(self.stop)
            self.metadata['stop_str'] = stop_str


        source_info = self.metadata['data_source']
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
                                      self.metadata['filter_name'])

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

    def get_time_resampling_settings(self):
        """Returns a dictionary with relevant settings for temporal resampling

        Returns
        -------
        dict
        """
        settings = {}
        mapping = {
            'apply_constraints'  : 'apply_time_resampling_constraints',
            'min_num_obs'        : 'min_num_obs',
            'resample_how'       : 'resample_how',
            'colocate_time'      : 'colocate_time'
            }
        for from_key, to_key in mapping.items():
            try:
                settings[to_key] = self.metadata[from_key]
            except KeyError:
                const.print_log.warning(
                    f'Meta key {from_key} not defined in ColocatedData.meta...')
                settings[to_key] = None
        return settings

    def _prepare_meta_to_netcdf(self):
        """
        Prepare metada for NetCDF format

        Returns
        -------
        meta_out : dict
            metadata ready for serialisation to NetCDF.

        """
        meta = self.data.attrs
        meta_out = {}
        for key, val in meta.items():
            if val is None:
                meta_out[key] = 'None'
            elif isinstance(val, bool):
                meta_out[key] = int(val)
            elif isinstance(val, dict):
                meta_out[f'CONV!{key}'] = str(val)
            else:
                meta_out[key] = val
        return meta_out

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

        Returns
        -------
        str
            file path of stored object.
        """
        if 'path' in kwargs:
            raise IOError('Path needs to be specified using input parameters '
                          'out_dir and savename')
        if savename is None:
            savename = self.savename_aerocom
        if not savename.endswith('.nc'):
            savename = '{}.nc'.format(savename)
        arr = self.data.copy()
        arr.attrs = self._prepare_meta_to_netcdf()
        fp = os.path.join(out_dir, savename)
        arr.to_netcdf(path=fp, **kwargs)
        return fp

    def _meta_from_netcdf(self, imported_meta):
        """
        Convert imported metadata as stored in NetCDF file

        Reason for this is that some meta values cannot be serialised when
        storing as NetCDF (e.g. nested dictionary `min_num_obs` or None values)

        Parameters
        ----------
        imported_meta : dict
            metadata as read in from colocated NetCDF file

        Returns
        -------
        meta : dict
            converted meta

        """
        meta = {}
        for key, val in imported_meta.items():
            if val == 'None':
                meta[key] = None
            elif key.startswith('CONV!'):
                key = key[5:]
                meta[key] = literal_eval(val)
            else:
                meta[key] = val
        return meta

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
            raise NetcdfError(
                f'Invalid file name for ColocatedData: {file_path}. '
                f'Error: {repr(e)}'
                )

        arr = xarray.open_dataarray(file_path)
        arr.attrs = self._meta_from_netcdf(arr.attrs)
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
        """
        Apply altitude filter

        Parameters
        ----------
        alt_range : list or tuple
            altitude range to be applied to data (2-element list)
        inplace : bool, optional
            Apply filter to this object directly or to a copy.
            The default is False.

        Raises
        ------
        NotImplementedError
            If data is 4D, i.e. it contains latitude and longitude dimensions.

        Returns
        -------
        ColocatedData
            Filtered data object .

        """
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
        """
        Apply altitude filter to 2D spatiotemporal data

        Parameters
        ----------
        arr : DataArray
            input array to be filtered
        alt_range : list or tuple
            altitude range to be applied to data (2-element list)

        Raises
        ------
        DataDimensionError
            if station_name is not the 3rd index

        Returns
        -------
        DataArray
            Filtered object.

        """
        if not list(arr.dims).index('station_name') == 2:
            raise DataDimensionError('station_name must be 3. dimensional index')

        mask = np.logical_and(arr.altitude > alt_range[0],
                              arr.altitude < alt_range[1])

        filtered = arr[:,:,mask]
        return filtered

    def _check_latlon_coords(self):
        """
        Check if latitude and longitude coordinates exists and are NOT dimensions

        Raises
        ------
        CoordinateError
            - if any or both coordinates are missing.
            - if one (and only one) of both coords is also a dimension

        Returns
        -------
        bool
            True if latitude and longitude are existing coordinates, False if
            they are also dimensions.

        """
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
        """
        Apply country filter in 2D spatiotemporal data

        Parameters
        ----------
        arr : DataArray
            data to be filtered for country.
        country : str
            name of country.
        use_country_code : bool
            If True, input value for `country` is evaluated against country
            codes rather than country names.

        Raises
        ------
        DataDimensionError
            If `country` is not a coordinate of input `DataArray`, or, in case
            `use_country_code=True`, if `country_code` is not a coordinate.
        DataCoverageError
            if filtering results in empty data object.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        what = 'country' if not use_country_code else 'country_code'
        if not what in arr.coords:
            raise DataDimensionError('Cannot filter country {}. No country '
                                     'information available in DataArray'
                                     .format(country))
        mask = arr[what] == country
        if mask.sum() == 0:
            raise DataCoverageError(
                f'No data available in country {country} in ColocatedData'
                )
        return arr[:,:,mask]

    @staticmethod
    def _filter_latlon_2d(arr, lat_range, lon_range):
        """
        Apply rectangular latitude / longitude filter for 2D data

        2D here means in terms of spatiotemporal dimensions, that is, the
        object has to have one spatial dimension `station_name` and one
        temporal dimension `time`.

        ToDo
        ----
        Use `sel` with slice, or similar, need to check though how that will
        apply to filtering that crosses the +180 -> -180 degree longitude
        border.

        Parameters
        ----------
        arr : DataArray
            data to be filtered.
        lat_range : list, optional
            latitude range that is supposed to be applied. If specified, then
            also lon_range need to be specified, else, region_id is checked
            against AeroCom default regions (and used if applicable)
        lon_range : list, optional
            longitude range that is supposed to be applied. If specified, then
            also lat_range need to be specified, else, region_id is checked
            against AeroCom default regions (and used if applicable)

        Raises
        ------
        DataDimensionError
            If index of `station_name` dimension is not at 3rd position in the
            underlying array.
        DataCoverageError
            If no data is available in the specified rectangular region.

        Returns
        -------
        ColocatedData
            Filtered data object.

        """
        if not list(arr.dims).index('station_name') == 2:
            raise DataDimensionError(
                'station_name dimension must be at 3rd index position'
                )

        lons, lats = arr.longitude.data, arr.latitude.data

        latmask = np.logical_and(lats > lat_range[0],
                                 lats < lat_range[1])
        if lon_range[0] > lon_range[1]:
            _either = np.logical_and(lons>=-180, lons<lon_range[1])
            _or = np.logical_and(lons>lon_range[0], lons<=180)
            lonmask = np.logical_or(_either, _or)
        else:
            lonmask = np.logical_and(lons > lon_range[0],
                                     lons < lon_range[1])
        mask = latmask & lonmask
        if mask.sum() == 0:
            raise DataCoverageError(
                f'No data available in latrange={lat_range} and '
                f'lonrange={lon_range} in ColocatedData'
                )

        return arr[:,:,mask]

    @staticmethod
    def _filter_latlon_3d(arr, lat_range, lon_range):
        """
        Apply rectangular latitude / longitude filter for 3D data

        32D here means in terms of spatiotemporal dimensions, that is, the
        object has to have two spatial dimensions `latitude` and `longitude`
        and one temporal dimension `time`.

        ToDo
        ----
        Implement filtering that crosses the +180 -> -180 degree longitude
        border.

        Parameters
        ----------
        arr : DataArray
            data to be filtered.
        lat_range : list, optional
            latitude range that is supposed to be applied. If specified, then
            also lon_range need to be specified, else, region_id is checked
            against AeroCom default regions (and used if applicable)
        lon_range : list, optional
            longitude range that is supposed to be applied. If specified, then
            also lat_range need to be specified, else, region_id is checked
            against AeroCom default regions (and used if applicable)

        Raises
        ------
        NotImplementedError
            If input longitude bounds cross the +180 -> -180 border.

        Returns
        -------
        ColocatedData
            Filtered data object.
        """
        if lon_range[0] > lon_range[1]:
            raise NotImplementedError(
                'Filtering longitude over 180 deg edge is not yet possible in '
                '3D ColocatedData...')
        if not isinstance(lat_range, slice):
            lat_range = slice(lat_range[0], lat_range[1])
        if not isinstance(lon_range, slice):
            lon_range = slice(lon_range[0], lon_range[1])

        return arr.sel(dict(latitude=lat_range, longitude=lon_range))

    def apply_country_filter(self, region_id, use_country_code=False,
                             inplace=False):
        """
        Apply country filter

        Parameters
        ----------
        region_id : str
            country name or code.
        use_country_code : bool, optional
            If True, input value for `country` is evaluated against country
            codes rather than country names. Defaults to False.
        inplace : bool, optional
            Apply filter to this object directly or to a copy.
            The default is False.

        Raises
        ------
        NotImplementedError
            if data is 4D (i.e. it has latitude and longitude dimensions).

        Returns
        -------
        ColocatedData
            filtered data object.

        """
        data = self if inplace else self.copy()
        is_2d = data._check_latlon_coords()
        if is_2d:
            data.data = data._filter_country_2d(data.data, region_id,
                                                use_country_code)
        else:
            raise NotImplementedError(
                'Cannot yet filter country for 3D ColocatedData object')

        return data

    def apply_latlon_filter(self, lat_range=None, lon_range=None,
                            region_id=None, inplace=False):
        """Apply rectangular latitude/longitude filter

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
        inplace : bool, optional
            Apply filter to this object directly or to a copy.
            The default is False.

        Raises
        ------
        ValueError
            if lower latitude bound exceeds upper latitude bound.

        Returns
        -------
        ColocatedData
            filtered data object
        """
        data = self if inplace else self.copy()

        is_2d = data._check_latlon_coords()

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

        if lat_range[0] > lat_range[1]:
            raise ValueError(
                f'Lower latitude bound {lat_range[0]} cannot exceed upper '
                f'latitude bound {lat_range[1]}')
        if is_2d:
            filtered = data._filter_latlon_2d(data.data, lat_range, lon_range)
        else:
            filtered = data._filter_latlon_3d(data.data, lat_range, lon_range)

        if not isinstance(region_id, str):
            region_id = 'CUSTOM'
        try:
            alt_info = filtered.attrs['filter_name'].split('-', 1)[-1]
        except Exception:
            alt_info = 'CUSTOM'

        filtered.attrs['filter_name'] = '{}-{}'.format(region_id, alt_info)
        filtered.attrs['region'] = region_id

        data.data = filtered
        return data

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

        Raises
        ------
        DataCoverageError
            if filtering results in empty data object.

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
        nstats = len(arr.station_name)
        for (lat, lon, stat) in data._iter_stats():
            if get_mask_value(lat, lon, mask) < 1:
                drop_idx.append(stat)

        ndrop = len(drop_idx)
        if ndrop == nstats:
            raise DataCoverageError(f'No data available in region {region_id}')
        elif ndrop > 0:
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
        elif region_id in REGION_DEFS:
            return self.apply_latlon_filter(region_id=region_id,
                                            inplace=inplace)
        raise AttributeError(f'no such region defined {region_id}')

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
        """
        Plot station coordinates

        Uses :func:`pyaerocom.plot.plotcoordinates.plot_coordinates`.

        Parameters
        ----------
        marker : str, optional
            matplotlib marker name used to plot site locations.
            The default is 'x'.
        markersize : int, optional
            Size of site markers. The default is 12.
        fontsize_base : int, optional
            Basic fontsize. The default is 10.
        **kwargs
            additional keyword args passed to
            :func:`pyaerocom.plot.plotcoordinates.plot_coordinates`

        Returns
        -------
        matplotlib.axes.Axes

        """

        from pyaerocom.plot.plotcoordinates import plot_coordinates

        lats, lons = self.get_coords_valid_obs()
        return plot_coordinates(lons=lons,
                                lats=lats,
                                marker=marker, markersize=markersize,
                                fontsize_base=fontsize_base, **kwargs)

    def __contains__(self, val):
        return self.data.__contains__(val)

    def __repr__(self):
        tp = type(self).__name__
        dstr = '<empty>' if self._data is None else repr(self._data)
        return f'pyaerocom.{tp}: data: {dstr}'

    def __str__(self):
        tp = type(self).__name__
        head = f'pyaerocom.{tp}'
        underline = len(head)*'-'
        dstr = '<empty>' if self._data is None else str(self._data)
        return f'{head}\n{underline}\ndata (DataArray): {dstr}'

    ### Deprecated (but still supported) stuff
    # ToDo: v0.12.0
    @property
    def unit(self):
        """DEPRECATED -> use :attr:`units`"""
        const.print_log.warning(DeprecationWarning(
            'Attr. ColocatedData.unit is deprecated (but still works), '
            'please use ColocatedData.units. '
            'Support guaranteed until pyaerocom v0.12.0'
            ))
        return self.units

    @property
    def meta(self):
        """DEPRECATED -> use :attr:`metadata`"""
        const.print_log.warning(DeprecationWarning(
            'Attr. ColocatedData.meta is deprecated (but still works), '
            'please use ColocatedData.metadata'
            'Support guaranteed until pyaerocom v0.12.0'
            ))
        return self.metadata

    @property
    def num_grid_points(self):
        """DEPRECATED -> use :attr:`num_coords`"""
        const.print_log.warning(DeprecationWarning(
            'Attr. ColocatedData.num_grid_points is deprecated (but still '
            'works), please use ColocatedData.num_coords'
            'Support guaranteed until pyaerocom v0.12.0'
            ))
        return self.num_coords

if __name__=="__main__":

    import matplotlib.pyplot as plt
    import pyaerocom as pya
    plt.close('all')

    dic = dict(monthly=3, daily=dict(minutely=4000, hourly=10),
               bla='blablub',
               lst=[1,2,3]
               )

    st = _dict_to_str(dic)

    print(st)