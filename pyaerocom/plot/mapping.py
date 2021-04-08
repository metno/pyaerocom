#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains plot routines for Aerocom data. So far, this includes a
low level, very flexible plot method
"""
import matplotlib.pyplot as plt
from pandas import to_datetime
import numpy as np
from matplotlib.colors import BoundaryNorm, LogNorm, Normalize
from mpl_toolkits.axes_grid1 import AxesGrid

import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from numpy import meshgrid, linspace, ceil

from pyaerocom import logger
from pyaerocom.plot.config import COLOR_THEME, ColorTheme, MAP_AXES_ASPECT
from pyaerocom.plot.helpers import (custom_mpl,
                                    calc_pseudolog_cmaplevels,
                                    projection_from_str,
                                    calc_figsize)
from pyaerocom.mathutils import exponent
from pyaerocom.region import Region

MPL_PARAMS = custom_mpl()

def get_cmap_maps_aerocom(color_theme=None, vmin=None, vmax=None):
    """Get colormap using pyAeroCom color scheme

    Parameters
    ----------
    color_theme : :obj:`ColorTheme`, optional
        instance of pyaerocom color theme. If None, the default schemes is used
    vmin : :obj:`float`, optional
        lower end of value range
    vmax : :obj:`float`, optional
        upper end of value range

    Returns
    -------
    colormap
    """
    if color_theme is None:
        color_theme=COLOR_THEME
    if vmin is not None and vmax is not None and vmin < 0 and vmax > 0:
        cmap = plt.get_cmap(color_theme.cmap_map_div)
        if color_theme.cmap_map_div_shifted:
            try:
                from geonum.helpers import shifted_color_map
                cmap = shifted_color_map(vmin, vmax, cmap)
            except Exception:
                logger.warning('cannot shift colormap, need geonum installation')
        return cmap
    return plt.get_cmap(color_theme.cmap_map)

def set_map_ticks(ax, xticks=None, yticks=None, add_x=True,
                  add_y=True):
    """Set or update ticks in instance of GeoAxes object (cartopy)

    Parameters
    ----------
    ax : cartopy.GeoAxes
        map axes instance
    xticks : iterable, optional
        ticks of x-axis (longitudes)
    yticks : iterable, optional
        ticks of y-axis (latitudes)
    add_x : bool
        if True, x-axis labels are added
    add_y : bool
        if True, y-axis labels are added

    Returns
    -------
    cartopy.GeoAxes
        modified axes instance
    """
    lonleft, lonright = ax.get_xlim()
    digits = 2 - exponent(lonleft)
    digits = 0 if digits < 0 else digits
    tick_format = '.%df' %digits
    if not xticks:
        num_lonticks = 7 if lonleft == -lonright else 6
        xticks = linspace(lonleft, lonright, num_lonticks)
    if not yticks:
        latleft, latright = ax.get_ylim()
        num_latticks = 7 if latleft == - latright else 6
        yticks = linspace(latleft, latright, num_latticks)
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())

    lon_formatter = LongitudeFormatter(number_format=tick_format,
                                       degree_symbol='',
                                       dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format=tick_format,
                                      degree_symbol='')

    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    return ax

def init_map(xlim=(-180, 180), ylim=(-90, 90), figh=8, fix_aspect=False,
             xticks=None, yticks=None, color_theme=COLOR_THEME,
             projection=None, title=None, gridlines=False,
             fig=None, ax=None, draw_coastlines=True, contains_cbar=False):
    """Initalise a map plot

    Parameters
    ----------
    xlim : tuple
        2-element tuple specifying plotted longitude range
    ylim : tuple
        2-element tuple specifying plotted latitude range
    figh : int
        height of figure in inches
    fix_aspect : :obj:`float`, optional
        if True, the aspect of the GeoAxes instance is kept fix using the
        default aspect ``MAP_AXES_ASPECT`` defined in
        :mod:`pyaerocom.plot.config`
    xticks : iterable, optional
        ticks of x-axis (longitudes)
    yticks : iterable, optional
        ticks of y-axis (latitudes)
    projection
        projection instance from cartopy.crs module (e.g. PlateCaree). May also
        be string.
    title : :obj:`str`, optional
        title that is supposed to be inserted
    fig : :obj:`Figure`, optional
        instance of matplotlib Figure class. If specified, the former to
        input args (``figh`` and ``fix_aspect``) are ignored. Note that the
        Figure is wiped clean before plotting, so any plotted content will be
        lost

    Returns
    -------
    ax : cartopy.mpl.geoaxes.GeoAxes
        axes instance
    """

    if projection is None:
        projection = ccrs.PlateCarree()
    elif isinstance(projection, str):
        projection = projection_from_str(projection)
    elif not isinstance(projection, ccrs.Projection):
        raise ValueError("Input for projection needs to be instance of "
                         "cartopy.crs.Projection")

    if not isinstance(ax, GeoAxes):
        if fig is None:
            if not fix_aspect:
                figsize = calc_figsize(xlim, ylim)
                #figw = figh*2
            else:
                figw = figh*fix_aspect
                figsize = (figw, figh)

            fig = plt.figure(figsize=figsize)
        else:
            fig.clf()
        if contains_cbar:
            ax = fig.add_axes([0.1, 0.12, 0.75, 0.8], projection=projection)
        else:
            ax = fig.add_axes([0.1, 0.12, 0.85, 0.8], projection=projection)

    if fix_aspect:
        ax.set_aspect(MAP_AXES_ASPECT)

    if not isinstance(color_theme, ColorTheme):
        if isinstance(color_theme, str):
            color_theme = ColorTheme(color_theme)
        else:
            color_theme = COLOR_THEME

    if draw_coastlines:
        ax.coastlines(color=COLOR_THEME.color_coastline)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    ax = set_map_ticks(ax, xticks, yticks)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    if title is not None:
        ax.set_title(title)
    if gridlines:
        ax.gridlines()

    return ax

def init_multimap_grid(nrows, ncols, add_coastlines=True, remove_outline_map=True,
                       projection=None, figsize=None, color_theme=None,
                       axes_pad_hor=0.02, axes_pad_vert=0.02,
                       cbar_mode=None, cbar_location='right',
                       cbar_pad='5%', cbar_size='3%', label_mode='',
                       **kwargs):
    if color_theme is None:
        color_theme = COLOR_THEME
    if projection is None:
        projection = ccrs.PlateCarree()

    axes_class = (GeoAxes, dict(map_projection=projection))

    if figsize is None:
        w = 20
        wmap = w / ncols
        hmap = wmap/2
        h = hmap * nrows
        figsize=(w,h)
    fig = plt.figure(figsize=figsize)

    axgr = AxesGrid(fig, 111, axes_class=axes_class,
                    nrows_ncols=(nrows, ncols),
                    axes_pad = (axes_pad_hor, axes_pad_vert),
                    cbar_location=cbar_location,
                    cbar_mode=cbar_mode,
                    cbar_pad=cbar_pad,
                    cbar_size=cbar_size,
                    label_mode=label_mode,
                    **kwargs)

    if add_coastlines or remove_outline_map:
        for ax in axgr:
            if add_coastlines:
                ax.coastlines(color=color_theme.color_coastline)
            if remove_outline_map:
                ax.outline_patch.set_edgecolor('white')
    return fig, axgr

def _init_width_ratios(width_ratios, ncols, add_cbar_axes):
    if width_ratios is None:
        sub = [30, 1] if add_cbar_axes else [30]
        width_ratios = sub*ncols
    elif isinstance(width_ratios, list):
        if len(width_ratios) == ncols and add_cbar_axes:
            wr = np.asarray(width_ratios)
            wrmax = wr.max()
            cbarw = wrmax / 30
            width_ratios = []
            for w in wr:
                width_ratios.extend([w, cbarw])

    if not isinstance(width_ratios, list):
        raise ValueError('Invalid input for width ratio')
    return width_ratios

def plot_griddeddata_on_map(data, lons=None, lats=None, var_name=None,
                            unit=None, xlim=(-180, 180), ylim=(-90, 90),
                            vmin=None, vmax=None, add_zero=False, c_under=None,
                            c_over=None, log_scale=True, discrete_norm=True,
                            cbar_levels=None, cbar_ticks=None, add_cbar=True,
                            cmap=None, cbar_ticks_sci=False,
                            color_theme=COLOR_THEME, ax=None,
                            ax_cbar=None, **kwargs):
    """Make a plot of gridded data onto a map

    Parameters
    ----------
    data : ndarray
        2D data array
    lons : ndarray
        longitudes of data
    lats : ndarray
        latitudes of data
    var_name : :obj:`str`, optional
        name of variable that is plotted
    xlim : tuple
        2-element tuple specifying plotted longitude range
    ylim : tuple
        2-element tuple specifying plotted latitude range
    vmin : :obj:`float`, optional
        lower value of colorbar range
    vmax : :obj:`float`, optional
        upper value of colorbar range
    add_zero : bool
        if True and vmin is not 0, then, the colorbar is extended down to 0.
        This may be used, e.g. for logarithmic scales that should include 0.
    c_under : :obj:`float`, optional
        colour of data values smaller than ``vmin``
    c_over : :obj:`float`, optional
        colour of data values exceeding ``vmax``
    log_scale : bool
        if True, the value to color mapping is done in a pseudo log scale
        (see :func:`get_cmap_levels_auto` for implementation)
    discrete_norm : bool
        if True, color mapping will be subdivided into discrete intervals
    cbar_levels : iterable, optional
        discrete colorbar levels. Will be computed automatically, if None
        (and applicable)
    cbar_ticks : iterable, optional
        ticks of colorbar levels. Will be computed automatically, if None
        (and applicable)

    Returns
    -------
    fig
        matplotlib figure instance containing plot result. Use
        ``fig.axes[0]`` to access the map axes instance (e.g. to modify the
        title or lon / lat range, etc.)
    """
    if add_cbar:
        kwargs['contains_cbar'] = True
    if ax is None:
        ax = init_map(xlim, ylim, color_theme=color_theme, **kwargs)
    if not isinstance(ax, GeoAxes):
        raise AttributeError('Invalid input for ax, need GeoAxes')
    fig = ax.figure
    from pyaerocom.griddeddata import GriddedData
    if isinstance(data, GriddedData):
        if not data.has_latlon_dims:
            from pyaerocom.exceptions import DataDimensionError
            raise DataDimensionError('Input data needs to have latitude and '
                                     'longitude dimension')
        if not data.ndim == 2:
            if not data.ndim == 3 or not 'time' in data.dimcoord_names:
                raise DataDimensionError('Input data needs to be 2 dimensional '
                                         'or 3D with time being the 3rd '
                                         'dimension')
            data.reorder_dimensions_tseries()

            data = data[0]

        lons = data.longitude.points
        lats = data.latitude.points
        data = data.grid.data
    elif not isinstance(data, np.ndarray) or not data.ndim == 2:
        raise IOError("Need 2D numpy array")
    elif not isinstance(lats, np.ndarray) or not isinstance(lons, np.ndarray):
        raise ValueError('Missing lats or lons input')
    if isinstance(data, np.ma.MaskedArray):
        sh = data.shape
        if data.mask.sum() == sh[0] * sh[1]:
            raise ValueError('All datapoints in input data (masked array) are '
                             'invalid')

    if add_cbar and ax_cbar is None:
        ax_cbar = _add_cbar_axes(ax)#, where='right')

    X, Y = meshgrid(lons, lats)

    bounds = None
    norm = None
    if cbar_levels is not None: #user provided levels of colorbar explicitely
        if vmin is not None or vmax is not None:
            raise ValueError('Please provide either vmin/vmax OR cbar_levels')
        bounds = list(cbar_levels)
        low, high = bounds[0], bounds[-1]
        if add_zero and low > 0:
            bounds.insert(0, 0) # insert zero bound
        if cmap is None:
            cmap = get_cmap_maps_aerocom(color_theme, low, high)
        elif isinstance(cmap, str):
            cmap = plt.get_cmap(cmap)
        norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N, clip=False)
    else:
        dmin = np.nanmin(data)
        dmax = np.nanmax(data)

        if any([np.isnan(x) for x in [dmin, dmax]]):
            raise ValueError('Cannot plot map of data: all values are NaN')
        elif dmin == dmax:
            raise ValueError('Minimum value in data equals maximum value: '
                             '{}'.format(dmin))
        if vmin is None:
            vmin = dmin
        else:
            if vmin < 0 and log_scale:
                log_scale=False
        if vmax is None:
            vmax = dmax
        if exponent(vmin) == exponent(vmax):
            log_scale=False
        if log_scale: # no negative values allowed
            if vmin < 0:
                vmin = data[data>0].min()
                if c_under is None: #special case, set c_under to indicate that there is values below 0
                    c_under = 'r'
            if cmap is None:
                cmap = get_cmap_maps_aerocom(color_theme, vmin, vmax)
            elif isinstance(cmap, str):
                cmap = plt.get_cmap(cmap)
            if discrete_norm:
                #to compute upper range of colour range, round up vmax
                exp = float(exponent(vmax) - 1)
                vmax_colors = ceil(vmax / 10**exp)*10**exp
                bounds = calc_pseudolog_cmaplevels(vmin=vmin, vmax=vmax_colors,
                                                   add_zero=add_zero)
                norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N,
                                    clip=False)

            else:
                if not vmin > 0:
                    raise ValueError('Logscale can only be applied for vmin>0')
                norm = LogNorm(vmin=vmin, vmax=vmax, clip=True)
        else:
            if add_zero and vmin > 0:
                vmin = 0
            if cmap is None:
                cmap = get_cmap_maps_aerocom(color_theme, vmin, vmax)
            elif isinstance(cmap, str):
                cmap = plt.get_cmap(cmap)
            if discrete_norm:
                bounds = np.linspace(vmin, vmax, 10)
                norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N,
                                    clip=False)
            else:
                norm = Normalize(vmin=vmin, vmax=vmax)
    cbar_extend = "neither"
    if c_under is not None:
        cmap.set_under(c_under)
        cbar_extend = "min"
        if bounds is not None:
            bounds.insert(0, bounds[0] - bounds[1])
    if c_over is not None:
        cmap.set_over(c_over)
        if bounds is not None:
            bounds.append(bounds[-1] + bounds[-2])
        if cbar_extend == "min":
            cbar_extend = "both"
        else:
            cbar_extend = "max"
    fig.norm = norm
    disp = ax.pcolormesh(X, Y, data, cmap=cmap, norm=norm)
# =============================================================================
#     fmt = None
#     if bounds is not None:
#         print(bounds)
#         min_mag = -exponent(bounds[1])
#         min_mag = 0 if min_mag < 0 else min_mag
#         print(min_mag)
#         #fmt = "%." + str(min_mag) + "f"
# =============================================================================
    if add_cbar:
        cbar = fig.colorbar(disp, cmap=cmap, norm=norm, #boundaries=bounds,
                            extend=cbar_extend, cax=ax_cbar, shrink=0.8)
        fig.cbar = cbar

        if var_name is not None:
            var_str = var_name# + VARS.unit_str
            if unit is not None:
                if not str(unit) in ['1', 'no_unit']:
                    var_str += ' [{}]'.format(unit)

            cbar.set_label(var_str)

        if cbar_ticks:
            cbar.set_ticks(cbar_ticks)
        if cbar_ticks_sci:
            lbls = []
            for lbl in cbar.ax.get_yticklabels():
                tstr = lbl.get_text()
                if bool(tstr):
                    lbls.append('{:.1e}'.format(float(tstr)))
                else:
                    lbls.append('')
            cbar.ax.set_yticklabels(lbls)

    return fig

def _add_cbar_axes(ax):#, where='right'):
    _loc = ax.bbox._bbox
    fig = ax.figure

    ax_cbar = fig.add_axes([_loc.x1 + .02,
                            _loc.y0, .02, _loc.y1 - _loc.y0])
    return ax_cbar
# =============================================================================
#     except Exception as e:
#         ax_cbar = fig.add_axes([0.91, 0.12, .02, .8])
#         print(repr(e))
# =============================================================================
def plot_map_aerocom(data, region=None, fig=None, **kwargs):
    """High level map plotting function for Aerocom default plotting

    Note
    ----
    This function does not iterate over a cube in time, but uses the
    first available time index in the data.

    Parameters
    ----------
    data : :obj:`GriddedData`
        input data from one timestamp (if data contains more than one time
        stamp, the first index is used)

    TODO
        finish docstring

    """
    #kwargs["fix_aspect"] = 1.6
    from pyaerocom import GriddedData
    if not isinstance(data, GriddedData):
        raise TypeError("This plotting method needs an instance of pyaerocom "
                         "GriddedData on input, got: %s" %type(data))
    if region:
        if isinstance(region, str):
            region = Region(region)
        if not isinstance(region, Region):
            raise TypeError("Invalid input for region, need None, str or Region")
        data = data.crop(region=region)
    if not data.suppl_info["region"]:
        data = data.crop(region="WORLD")
    region = data.suppl_info["region"]
    s = data.plot_settings
    fig = plot_griddeddata_on_map(data,
                                  xlim=region.lon_range_plot,
                                  ylim=region.lat_range_plot,
                                  vmin=s.map_vmin, vmax=s.map_vmax,
                                  c_over=s.map_c_over, c_under=s.map_c_under,
                                  cbar_levels=s.map_cbar_levels,
                                  xticks = region.lon_ticks,
                                  yticks = region.lat_ticks,
                                  cbar_ticks=s.map_cbar_ticks, **kwargs)
    ax = fig.axes[0]

    # annotate model in lower left corner
    lonr, latr = region.lon_range_plot, region.lat_range_plot
    ax.annotate(data.name,
                xy=(lonr[0] + (lonr[1] - lonr[0])*.03,
                    latr[0] + (latr[1] - latr[0])*.03),
                xycoords='data',
                horizontalalignment='left',
                color='black',
                fontsize=MPL_PARAMS['axes.titlesize'] + 2,
                bbox=dict(boxstyle='square',
                          facecolor='white',
                          edgecolor='none',
                          alpha=0.7))
    ax.annotate('source: AEROCOM',
                xy=(0.97, 0.03),
                xycoords='figure fraction',
                horizontalalignment='right',
                fontsize=MPL_PARAMS['xtick.labelsize'],
                bbox=dict(boxstyle='square',
                          facecolor='none',
                          edgecolor='black'))
    ax.set_title("{} {} mean {:.3f}".format(data.var_name.upper(),
                 to_datetime(data.start).strftime("%Y%m%d"),
                 data.area_weighted_mean()))
    return fig

def plot_map(data, *args, **kwargs):
    """Map plot of grid data

    Note
    ----
    Deprecated name of method. Please use :func:`plot_griddeddata_on_map` in
    the future.

    Parameters
    ----------
    data
        data (2D numpy array or instance of GriddedData class. The latter is
        deprecated, but will continue to work)
    *args, **kwargs
        See :func:`plot_griddeddata_on_map`

    Returns
    -------
    See :func:`plot_griddeddata_on_map`
    """
    from pyaerocom import print_log, GriddedData
    print_log.warning(DeprecationWarning('Method name plot_map is deprecated. '
                                         'Please use plot_griddeddata_on_map'))
    if isinstance(data, GriddedData):
        if 'time' in data and len(data['time'].points) > 1:
            logger.warning("Input data contains more than one time stamp, using "
                           "first time stamp")
            data = data[0]
        if not all([x in data for x in ('longitude', 'latitude')]):
            raise AttributeError('GriddedData does not contain either longitude '
                                 'or latitude coordinates')
        return plot_griddeddata_on_map(data.grid.data,
                                       data.longitude.points,
                                       data.latitude.points,
                                       *args, **kwargs)
    return plot_griddeddata_on_map(data, *args, **kwargs)

def plot_nmb_map_colocateddata(coldata, in_percent=True, vmin=-100,
                                vmax=100, cmap='bwr', s=80, marker='o',
                                step_bounds=None, add_cbar=True,
                                norm=None,
                                cbar_extend='both',
                                add_mean_edgecolor=True,
                                ax=None, ax_cbar=None,
                                cbar_outline_visible=False,
                                cbar_orientation='vertical',
                                ref_label=None, data_label=None,
                                stats_area_weighted=False,
                                **kwargs):
    """Plot map of normalised mean bias from instance of ColocatedData

    Note
    ----
    THIS IS A BETA FEATURE AND WILL BE GENERALISED IN THE FUTURE FOR OTHER
    STATISTICAL PARAMETERS

    Parameters
    ----------
    coldata : ColocatedData
        data object
    in_percent : bool
        plot bias in percent
    vmin : int
        minimum value of colormapping
    vmax : int
        maximum value of colormapping
    cmap : str or cmap
        colormap used, defaults to bwr
    s : int
        size of marker
    marker : str
        marker used
    step_bounds : int, optional
        step used for discrete colormapping (if None, continuous is used)
    cbar_extend : str
        extend colorbar
    ax : GeoAxes, optional
        axes into which the bias is supposed to be plotted
    ax_cbar : plt.Axes, optional
        axes for colorbar
    cbar_outline_visible : bool
        if False, borders of colorbar are removed
    **kwargs
        keyword args passed to :func:`init_map`

    Returns
    -------
    GeoAxes
    """
    try:
        mec = kwargs.pop('mec')
    except KeyError:
        try:
            mec = kwargs.pop('markeredgecolor')
        except KeyError:
            mec = 'face'

    try:
        mew = kwargs.pop('mew')
    except KeyError:
        mew = 1
    #_arr = coldata.data
    mean_bias = coldata.calc_nmb_array()

    if mean_bias.ndim == 1:
        (lats,
         lons,
         data) = mean_bias.latitude, mean_bias.longitude, mean_bias.data
    elif 'latitude' in mean_bias.dims and 'longitude' in mean_bias.dims:
        stacked = mean_bias.stack(latlon=['latitude', 'longitude'])
        valid = ~stacked.isnull()#.all(dim='time')
        coords = stacked.latlon[valid].values
        lats, lons = list(zip(*list(coords)))
        data = stacked.data[valid]
    else:
        raise NotImplementedError('Dimension error...')

    if ref_label is None:
        ref_label = coldata.metadata['data_source'][0]
    if data_label is None:
        data_label = coldata.metadata['data_source'][1]

    if in_percent:
        data *= 100
    if ax is None:
        ax = init_map(contains_cbar=True, **kwargs)

    if not isinstance(ax, GeoAxes):
        raise TypeError('Input axes need to be instance of cartopy.GeoAxes')

    fig = ax.figure


    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
    if norm is None and step_bounds is not None:
        bounds = np.arange(vmin, vmax+step_bounds, step_bounds)
        norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N, clip=False)



    if add_mean_edgecolor:
        nn = Normalize(vmin=vmin, vmax=vmax)
        nmb = coldata.calc_statistics(use_area_weights=stats_area_weighted)['nmb']
        if in_percent:
            nmb*=100
        ec = cmap(nn(nmb))
    else:
        ec = mec
    _sc = ax.scatter(lons, lats, c=data, marker=marker,
                     cmap=cmap, vmin=vmin, vmax=vmax, s=s, norm=norm,
                     label=ref_label, edgecolors=ec,
                     linewidths=mew)
    if add_cbar:
        if ax_cbar is None:
            ax_cbar = _add_cbar_axes(ax)
        cbar = fig.colorbar(_sc, cmap=cmap, norm=norm, #boundaries=bounds,
                            extend=cbar_extend, cax=ax_cbar,
                            orientation=cbar_orientation)

        cbar.outline.set_visible(cbar_outline_visible)
        cbar.set_label('NMB [%]')

    return ax

if __name__ == "__main__":

    plt.close('all')

    import pyaerocom as pya
    import pandas as pd

    temp = pya.io.ReadGridded('ERA5').read_var('ta').resample_time('yearly')

    ax = plot_griddeddata_on_map(temp)

    raise Exception

    #fig, axm, axc = init_multimap_grid_v0(5, 3, add_cbar_axes=True)

    reader = pya.io.ReadGridded('OsloCTM3v1.01-met2010_AP3-CTRL')

    data = reader.read_var('ec550dryaer', ts_type='monthly')

    #plot_griddeddata_on_map(data, ax=axm[0][0], ax_cbar=axc[0][0])

    fig, axgr = init_multimap_grid(3,4, figsize=(18, 7), axes_pad_hor=0.6,
                                   axes_pad_vert=0.5, cbar_mode='each')
    for ax in axgr:
        ax.coastlines()

    vmin, vmax = 0, np.ceil(data.max()/100)*100
    ts = data.time_stamps()
    for i in range(12):
        cax = axgr.cbar_axes[i]
        ax = axgr[i]
        plot_griddeddata_on_map(data[i], ax=ax, ax_cbar=cax,
                                vmin=vmin, vmax=vmax, discrete_norm=True)

        ax.set_title(pd.Timestamp(ts[i]).strftime('%B %Y'),
                     fontsize=10)

    fig = plt.figure(figsize=(18, 7))
    axes_class = (GeoAxes, dict(map_projection=ccrs.PlateCarree()))

    axgr = AxesGrid(fig, 111, axes_class=axes_class,
                    nrows_ncols=(3, 4),
                    axes_pad=(0.6, 0.5),
                    cbar_location='right',
                    cbar_mode="each",
                    cbar_pad="5%",
                    cbar_size='3%',
                    label_mode='')  # note the empty label_mode
