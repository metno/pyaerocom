import logging

import numpy as np

# from pyaerocom import const
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.exceptions import (  # CoordinateError,; DataCoverageError,; DataSourceError,; MetaDataError,; NetcdfError,; UnknownRegion,; VarNotAvailableError,
    DataDimensionError,
)
from pyaerocom.geodesy import get_country_info_coords

# from pyaerocom.helpers import to_datestring_YYYYMMDD
# from pyaerocom.helpers_landsea_masks import get_mask_value, load_region_mask_xr
from pyaerocom.mathutils import calc_statistics
from pyaerocom.plot.plotscatter import plot_scatter

# import os
# import warnings
# from ast import literal_eval
# from pathlib import Path

# import pandas as pd
# import xarray

# from pyaerocom.region import Region
# from pyaerocom.region_defs import REGION_DEFS
# from pyaerocom.time_resampler import TimeResampler

logger = logging.getLogger(__name__)


class ColocatedData2D(ColocatedData):
    """
    Class derived from ColocatedData which represents 2D colcated data. Everything specific to the 2D case will be put here
    """

    # def __init__(self, data=None, **kwargs):
    #     super().__init__(data, **kwargs)

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
            stacked = obs.stack(x=["latitude", "longitude"])
            invalid = stacked.isnull().all(dim="time")
            coords = stacked.x[~invalid].values
            coords = zip(*list(coords))
        else:
            invalid = obs.isnull().all(dim="time")
            lats = list(obs.latitude[~invalid].values)
            lons = list(obs.longitude[~invalid].values)
            coords = (lats, lons)
        return list(coords)

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
                raise DataDimensionError("Invalid dimensions in 4D ColocatedData")
            lats, lons = self.data.latitude.data, self.data.longitude.data
            coords = np.dstack(np.meshgrid(lats, lons))
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
            raise DataDimensionError(
                "Countries cannot be assigned to 4D"
                "ColocatedData with othorgonal lat / lon "
                "dimensions. Please consider stacking "
                "the latitude and longitude dimensions-"
            )
        if assign_to_dim is None:
            assign_to_dim = "station_name"

        if not assign_to_dim in self.dims:
            raise DataDimensionError("No such dimension", assign_to_dim)

        coldata = self if inplace else self.copy()

        if "country" in coldata.data.coords:
            logger.info("Country information is available")
            return coldata
        coords = coldata._get_stat_coords()

        info = get_country_info_coords(coords)

        countries, codes = [], []
        for item in info:
            countries.append(item["country"])
            codes.append(item["country_code"])

        arr = coldata.data
        arr = arr.assign_coords(
            country=(assign_to_dim, countries), country_code=(assign_to_dim, codes)
        )
        coldata.data = arr
        return coldata

    def calc_temporal_statistics(self, aggr=None, **kwargs):
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
            aggr = "mean"
        nc = self.num_coords
        try:
            ncd = self.num_coords_with_data
        except:
            ncd = np.nan
        if self.has_latlon_dims:
            dim = ("latitude", "longitude")
        else:
            dim = "station_name"

        if aggr == "mean":
            arr = self.data.mean(dim=dim)
        elif aggr == "median":
            arr = self.data.median(dim=dim)
        else:
            raise ValueError("So far only mean and median are supported aggregators")
        obs, mod = arr[0].values.flatten(), arr[1].values.flatten()
        stats = calc_statistics(mod, obs, **kwargs)
        stats["num_coords_tot"] = nc
        stats["num_coords_with_data"] = ncd
        return stats

    def calc_spatial_statistics(self, aggr=None, use_area_weights=False, **kwargs):
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
            aggr = "mean"
        if use_area_weights and not "weights" in kwargs and self.has_latlon_dims:
            weights = self.area_weights[0]  # 3D (time, lat, lon)
            assert self.dims[1] == "time"
            kwargs["weights"] = np.nanmean(weights, axis=0).flatten()

        nc, ncd = self.num_coords, self.num_coords_with_data
        # ToDo: find better solution to parse aggregator without if conditions,
        # e.g. xr.apply_ufunc or similar, with core aggregators that are
        # supported being defined in some dictionary in some pyaerocom config
        # module or class. Also aggregation could go into a separate method...
        if aggr == "mean":
            arr = self.data.mean(dim="time")
        elif aggr == "median":
            arr = self.data.median(dim="time")
        else:
            raise ValueError("So far only mean and median are supported aggregators")

        obs, mod = arr[0].values.flatten(), arr[1].values.flatten()
        stats = calc_statistics(mod, obs, **kwargs)
        stats["num_coords_tot"] = nc
        stats["num_coords_with_data"] = ncd
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
        try:
            num_points = self.num_coords_with_data
        except DataDimensionError:
            num_points = np.nan
        try:
            vars_ = meta["var_name"]
        except KeyError:
            vars_ = ["N/D", "N/D"]
        try:
            xn, yn = meta["data_source"]
        except KeyError:
            xn, yn = "N/D", "N/D"

        if vars_[0] != vars_[1]:
            var_ref = vars_[0]
        else:
            var_ref = None
        try:
            tst = meta["ts_type"]
        except KeyError:
            tst = "N/D"
        try:
            fn = meta["filter_name"]
        except KeyError:
            fn = "N/D"
        try:
            unit = self.unitstr
        except KeyError:
            unit = "N/D"
        try:
            start = self.start
        except AttributeError:
            start = "N/D"

        try:
            stop = self.stop
        except AttributeError:
            stop = "N/D"

        # ToDo: include option to use area weighted stats in plotting
        # routine...
        return plot_scatter(
            x_vals=self.data.values[0].flatten(),
            y_vals=self.data.values[1].flatten(),
            var_name=vars_[1],
            var_name_ref=var_ref,
            x_name=xn,
            y_name=yn,
            start=start,
            stop=stop,
            unit=unit,
            ts_type=tst,
            stations_ok=num_points,
            filter_name=fn,
            **kwargs,
        )

    def plot_coordinates(self, marker="x", markersize=12, fontsize_base=10, **kwargs):
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
        return plot_coordinates(
            lons=lons,
            lats=lats,
            marker=marker,
            markersize=markersize,
            fontsize_base=fontsize_base,
            **kwargs,
        )
