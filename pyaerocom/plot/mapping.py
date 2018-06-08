#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains plot routines for Aerocom data. So far, this includes a
low level, very flexible plot method
"""
from copy import copy
from matplotlib.pyplot import figure
from pandas import to_datetime
from matplotlib.colors import BoundaryNorm, LogNorm
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from numpy import meshgrid, linspace, ceil

from pyaerocom import const
from pyaerocom.plot.config import COLOR_THEME, ColorTheme, MAP_AXES_ASPECT
from pyaerocom.plot.helpers import (calc_figsize, custom_mpl, 
                                    calc_pseudolog_cmaplevels,
                                    projection_from_str)
from pyaerocom.mathutils import exponent
from pyaerocom.griddeddata import GriddedData
from pyaerocom.region import Region

MPL_PARAMS = custom_mpl()

def plot_map(data, xlim=(-180, 180), ylim=(-90, 90), vmin=None, vmax=None, 
             add_zero=False, c_under=None, c_over=None, log_scale=True, 
             discrete_norm=True, figh=8, fix_aspect=False, 
             cbar_levels=None, cbar_ticks=None, xticks=None, yticks=None,
             color_theme=COLOR_THEME, projection=ccrs.PlateCarree(), fig=None,
             verbose=const.VERBOSE):
    """Make a plot of grid data onto a map
    
    Parameters
    ----------
    data : :obj:`GriddedData` or :obj:`iris.cube.Cube`
        input data from one timestamp. May also be of type 
        :class:`pyaerocom.GriddedData`. Uses first time stamp if data is has
        more than one time stamp
    xlim : tuple
        2-element tuple specifying plotted longitude range
    ylim : tuple
        2-element tuple specifying plotted latitude range
    color_norm 
        data mapping norm for color display
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
        if True,
    figh : int
        height of figure in inches
    fix_aspect : :obj:`float`, optional
        if True, the aspect of the GeoAxes instance is kept fix using the
        default aspect ``MAP_AXES_ASPECT`` defined in 
        :mod:`pyaerocom.plot.config`
    cbar_levels : iterable, optional
        discrete colorbar levels. Will be computed automatically, if None 
        (and applicable)
    cbar_ticks : iterable, optional
        ticks of colorbar levels. Will be computed automatically, if None 
        (and applicable)
    xticks : iterable, optional
        ticks of x-axis (longitudes)
    yticks : iterable, optional
        ticks of y-axis (latitudes)
    color_theme : ColorTheme
        pyaerocom color theme
    projection 
        projection instance from cartopy.crs module (e.g. PlateCaree). May also
        be string
    fig : :obj:`Figure`, optional
        instance of matplotlib Figure class. If specified, the former to 
        input args (``figh`` and ``fix_aspect``) are ignored. Note that the 
        Figure is wiped clean before plotting, so any plotted content will be 
        lost
    verbose : bool
        if True, print output
    
    Returns
    -------
    fig
        matplotlib figure instance containing plot result. Use 
        ``fig.axes[0]`` to access the map axes instance (e.g. to modify the 
        title or lon / lat range, etc.)
    """
    if isinstance(projection, str):
        projection =projection_from_str(projection)
    elif not isinstance(projection, ccrs.Projection):
        raise ValueError("Input for projection needs to be instance of "
                         "cartopy.crs.Projection")
    if isinstance(data, GriddedData):
        data = data.grid
    if len(data.coord("time").points) > 1:
        if verbose:
            print("Input data contains more than one time stamp, using first "
                  "time stamp")
        data = data[0]
    if not isinstance(color_theme, ColorTheme):
        if isinstance(color_theme, str):
            color_theme = ColorTheme(color_theme)  
        else:
            color_theme = COLOR_THEME
    tstr = str(data.coord("time").cell(0))

    lons, lats = data.coord("longitude").points, data.coord("latitude").points
    if fig is None:
        figw = figh*2
        fig = figure(figsize=(figw, figh))
    else:
        fig.clf()
    ax = fig.add_axes([0.1, 0.12, 0.8, 0.8], projection=projection)
    if fix_aspect:
        ax.set_aspect(MAP_AXES_ASPECT)
    #ax.set_adjustable("datalim")

    ax_cbar = fig.add_axes([0.91, 0.12, .02, .8])
    X, Y = meshgrid(lons, lats)
    cmap = copy(color_theme.cmap_map)
    if vmin is None:
        vmin = data.data.min()
    if vmax is None:
        vmax = data.data.max()
            
    bounds = None
    if cbar_levels: #user provided levels of colorbar explicitely
        bounds = cbar_levels
        norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N, clip=False)
    else:
        if log_scale and discrete_norm:
            #to compute upper range of colour range, round up vmax
            exp = float(exponent(vmax) - 1)
            vmax_colors = ceil(vmax / 10**exp)*10**exp
            bounds = calc_pseudolog_cmaplevels(vmin=vmin, vmax=vmax_colors,
                                               add_zero=add_zero)
            norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N, clip=False)
        elif log_scale:
            norm = LogNorm(vmin=vmin, vmax=vmax, clip=True)
        else: 
            norm = None
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
      
    disp = ax.pcolormesh(X, Y, data.data, cmap=cmap, norm=norm)
    
    min_mag = -exponent(bounds[1])
    min_mag = 0 if min_mag < 0 else min_mag

    cbar = fig.colorbar(disp, cmap=cmap, norm=norm, boundaries=bounds, 
                        extend=cbar_extend, cax=ax_cbar,
                        format="%." + str(min_mag) + "f")
    #return fig
    cbar.set_label(data.var_name)
    if cbar_ticks:
        cbar.set_ticks(cbar_ticks)
    ax.coastlines(color=COLOR_THEME.color_coastline)
    
    lonleft, lonright = xlim
    digits = 2 - exponent(lonleft)
    digits = 0 if digits < 0 else digits
    tick_format = '.%df' %digits
    if not xticks:    
        num_lonticks = 7 if lonleft == -lonright else 6    
        xticks = linspace(lonleft, lonright, num_lonticks)
    if not yticks:
        latleft, latright = ylim
        num_latticks = 7 if latleft == - latright else 6
        yticks = linspace(latleft, latright, num_latticks)
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    
    
    lon_formatter = LongitudeFormatter(number_format=tick_format,
                                       degree_symbol='',
                                       dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format=tick_format,
                                      degree_symbol='')
    
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(tstr)

    return fig

def plot_map_OLD(data, xlim=(-180, 180), ylim=(-90, 90), vmin=None, vmax=None, 
             add_zero=False, c_under=None, c_over=None, log_scale=True, 
             discrete_norm=True, figh=8, fix_aspect=None, 
             cbar_levels=None, cbar_ticks=None, xticks=None, yticks=None,
             color_theme=COLOR_THEME, fig=None, verbose=const.VERBOSE):
    """Make a plot of grid data onto a map
    
    Parameters
    ----------
    data : :obj:`GriddedData` or :obj:`iris.cube.Cube`
        input data from one timestamp. May also be of type 
        :class:`pyaerocom.GriddedData`. Uses first time stamp if data is has
        more than one time stamp
    xlim : tuple
        2-element tuple specifying plotted longitude range
    ylim : tuple
        2-element tuple specifying plotted latitude range
    color_norm 
        data mapping norm for color display
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
        if True,
    figh : int
        height of figure in inches
    fix_aspect : :obj:`float`, optional
        if not None, then the figure width is computed by multiplication of
        the input float with input parameter ``figh``
        
    
    color_theme : ColorTheme
        pyaerocom color theme
    fig : :obj:`Figure`, optional
        instance of matplotlib Figure class. If specified, the former to 
        input args (``figh`` and ``fix_aspect``) are ignored. Note that the 
        Figure is wiped clean before plotting, so any plotted content will be 
        lost
    verbose : bool
        if True, print output
    
    Returns
    -------
    fig
        matplotlib figure instance containing plot result. Use 
        ``fig.axes[0]`` to access the map axes instance (e.g. to modify the 
        title or lon / lat range, etc.)
    """
    if isinstance(data, GriddedData):
        data = data.grid
    if len(data.coord("time").points) > 1:
        if verbose:
            print("Input data contains more than one time stamp, using first "
                  "time stamp")
        data = data[0]
    if not isinstance(color_theme, ColorTheme):
        if isinstance(color_theme, str):
            color_theme = ColorTheme(color_theme)  
        else:
            color_theme = COLOR_THEME
    tstr = str(data.coord("time").cell(0))

    lons, lats = data.coord("longitude").points, data.coord("latitude").points
    if fig is None:
        if fix_aspect is not None:
            figw = (MAP_AXES_ASPECT/2 + .05)*figh
            figsize = (figw, figh)
        else:
            figsize = calc_figsize(xlim, ylim, figh)
        fig = figure(figsize=figsize)
    else:
        fig.clf()
    print(figsize)
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection=ccrs.PlateCarree())
    #ax.set_adjustable("datalim")

    ax_cbar = fig.add_axes([0.9, .1, .02, .8])
    X, Y = meshgrid(lons, lats)
    cmap = copy(color_theme.cmap_map)
    if vmin is None:
        vmin = data.data.min()
    if vmax is None:
        vmax = data.data.max()
            
    bounds = None
    if cbar_levels: #user provided levels of colorbar explicitely
        bounds = cbar_levels
        norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N, clip=False)
    else:
        if log_scale and discrete_norm:
            #to compute upper range of colour range, round up vmax
            exp = float(exponent(vmax) - 1)
            vmax_colors = ceil(vmax / 10**exp)*10**exp
            bounds = calc_pseudolog_cmaplevels(vmin=vmin, vmax=vmax_colors,
                                               add_zero=add_zero)
            norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N, clip=False)
        elif log_scale:
            norm = LogNorm(vmin=vmin, vmax=vmax, clip=True)
        else: 
            norm = None
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
      
    disp = ax.pcolormesh(X, Y, data.data, cmap=cmap, norm=norm)
    
    min_mag = -exponent(bounds[1])
    min_mag = 0 if min_mag < 0 else min_mag

    cbar = fig.colorbar(disp, cmap=cmap, norm=norm, boundaries=bounds, 
                        extend=cbar_extend, cax=ax_cbar,
                        format="%." + str(min_mag) + "f")
    #return fig
    cbar.set_label(data.var_name)
    if cbar_ticks:
        cbar.set_ticks(cbar_ticks)
    ax.coastlines(color=COLOR_THEME.color_coastline)
    
    lonleft, lonright = xlim
    digits = 2 - exponent(lonleft)
    digits = 0 if digits < 0 else digits
    tick_format = '.%df' %digits
    if not xticks:    
        num_lonticks = 7 if lonleft == -lonright else 6    
        xticks = linspace(lonleft, lonright, num_lonticks)
    if not yticks:
        latleft, latright = ylim
        num_latticks = 7 if latleft == - latright else 6
        yticks = linspace(latleft, latright, num_latticks)
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    
    
    lon_formatter = LongitudeFormatter(number_format=tick_format,
                                       degree_symbol='',
                                       dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format=tick_format,
                                      degree_symbol='')
    
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(tstr)
    
# =============================================================================
#     if fix_aspect:
#         ax.set_aspect(aspect=1/MAP_AXES_ASPECT)
# =============================================================================
    return fig

def plot_map_aerocom(data, region=None, fig=None, **kwargs):
    """High level map plotting function for Aerocom default plotting
    
    Note
    ----
    This function requires does not iterate over a cube in time, but uses the
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
    fig = plot_map(data, xlim=region.lon_range_plot, ylim=region.lat_range_plot,
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
                 to_datetime(data.start_time).strftime("%Y%m%d"),
                 data.area_weighted_mean()))
    return fig
    
    
if __name__ == "__main__":
    from matplotlib.pyplot import close
    import pyaerocom
    close("all")
    
    read = pyaerocom.io.ReadGridded("AATSR_SU_v1.0")    
    data = read.read_var("od550aer")
    data.quickplot_map()
    
    run_old=False
    if run_old:
        read = pyaerocom.io.ReadGridded("ECMWF_OSUITE", start_time="2010",
                                          stop_time="2019")
        
        data = read.read_var("od550aer")
        fig0 = data.quickplot_map(fix_aspect=False)
        fig1 = data.quickplot_map(fix_aspect=True, color_theme="light")
        
        figs = []
        for region in pyaerocom.region.get_all_default_regions():
            crp = data.crop(region=region)
            figs.append(plot_map_aerocom(crp[0]))
        
        
    
