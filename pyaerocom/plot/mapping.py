#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains plot routines for Aerocom data. So far, this includes a
low level, very flexible plot method
"""
from matplotlib.pyplot import figure, get_cmap
from pandas import to_datetime
import numpy as np
from matplotlib.colors import BoundaryNorm, LogNorm, Normalize

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
        cmap = get_cmap(color_theme.cmap_map_div)
        if color_theme.cmap_map_div_shifted:
            try:
                from geonum.helpers import shifted_color_map
                cmap = shifted_color_map(vmin, vmax, cmap)
            except:
                logger.warning('cannot shift colormap, need geonum installation')
        return cmap
    return get_cmap(color_theme.cmap_map)
    

def set_map_ticks(ax, xticks=None, yticks=None):
    """Set or update ticks in instance of GeoAxes object (cartopy)
    
    Parameters
    ----------
    ax : cartopy.GeoAxes
        map axes instance
    xticks : iterable, optional
        ticks of x-axis (longitudes)
    yticks : iterable, optional
        ticks of y-axis (latitudes)
        
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
        be string
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
                    
            fig = figure(figsize=figsize)
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

def plot_griddeddata_on_map(data, lons=None, lats=None, var_name=None, 
                            unit=None, xlim=(-180, 180), ylim=(-90, 90), 
                            vmin=None, vmax=None, add_zero=False, c_under=None, 
                            c_over=None, log_scale=True, discrete_norm=True, 
                            cbar_levels=None, cbar_ticks=None, add_cbar=True,
                            cmap=None, cbar_ticks_sci=False, 
                            color_theme=COLOR_THEME, **kwargs):
    """Make a plot of gridded data onto a map
    
    Note
    ----
    This is a lowlevel plotting method
    
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
    kwargs['contains_cbar'] = True
    ax = init_map(xlim, ylim, color_theme=color_theme, **kwargs)
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
    _loc = ax.bbox._bbox
    try:
        ax_cbar = fig.add_axes([_loc.x1 + .02,
                                _loc.y0, .02, _loc.y1 - _loc.y0])
    except Exception as e:
        ax_cbar = fig.add_axes([0.91, 0.12, .02, .8])
        print(repr(e))
    X, Y = meshgrid(lons, lats)
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
    
    bounds = None
    if cbar_levels: #user provided levels of colorbar explicitely
        if vmin is not None or vmax is not None:
            raise ValueError('Please provide either vmin/vmax OR cbar_levels')
        bounds = list(cbar_levels)
        low, high = bounds[0], bounds[-1]
        if add_zero and low > 0:
            bounds.insert(0, 0) # insert zero bound
        if cmap is None or isinstance(cmap, str):
            cmap = get_cmap_maps_aerocom(color_theme, low, high)
        norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N, clip=False)
    else:
        if log_scale: # no negative values allowed
            if vmin < 0:
                vmin = data[data>0].min()
                if c_under is None: #special case, set c_under to indicate that there is values below 0
                    c_under = 'r'
            if cmap is None or isinstance(cmap, str):
                cmap = get_cmap_maps_aerocom(color_theme, vmin, vmax)
            if discrete_norm:
                #to compute upper range of colour range, round up vmax
                exp = float(exponent(vmax) - 1)
                vmax_colors = ceil(vmax / 10**exp)*10**exp
                bounds = calc_pseudolog_cmaplevels(vmin=vmin, vmax=vmax_colors,
                                                   add_zero=add_zero)
                norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N, clip=False)
        
            else:
                norm = LogNorm(vmin=vmin, vmax=vmax, clip=True)
        else: 
            if cmap is None or isinstance(cmap, str):
                cmap = get_cmap_maps_aerocom(color_theme, vmin, vmax)
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
        cbar = fig.colorbar(disp, cmap=cmap, norm=norm, boundaries=bounds, 
                            extend=cbar_extend, cax=ax_cbar)
        
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
   
if __name__ == "__main__":
    from matplotlib.pyplot import close
    import pyaerocom as pya
    close("all")
    
    d = pya.io.ReadGridded('ECMWF-IFS-CY42R1-CAMS-RA-CTRL_AP3-CTRL2016-PD').read_var('ang4487aer', start=2010)
    d.quickplot_map(vmin=-1, vmax=4)