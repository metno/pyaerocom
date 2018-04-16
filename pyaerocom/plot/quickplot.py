#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from copy import copy
from matplotlib.pyplot import figure
from matplotlib.colors import BoundaryNorm, LogNorm
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from numpy import meshgrid, linspace, ceil
from pyaerocom.glob import VERBOSE
from pyaerocom.plot.config import COLOR_THEME
from pyaerocom.plot.helpers import (calc_figsize, get_cmap_levels_auto,
                                    custom_mpl)
from pyaerocom.mathutils import exponent
from pyaerocom import ModelData

custom_mpl()

def plot_map(data, xlim=(-180, 180), ylim=(-90, 90), color_theme=COLOR_THEME, 
             vmin=None, vmax=None, c_under=None, c_over=None, 
             log_scale=True, discrete_norm=True, figh=8, fix_aspect=None,
             verbose=VERBOSE, **kwargs):
    """Make a quick plot of grid data onto a map
    
    Parameters
    ----------
    data : iris.cube.Cube
        input data from one timestamp. May also be of type 
        :class:`pyaerocom.ModelData`. Uses first time stamp if data is has 
        more than one time stamp
    xlim : tuple
        2-element tuple specifying plotted longitude range
    ylim : tuple
        2-element tuple specifying plotted latitude range
    color_theme : str
        pyaerocom color theme
    color_norm 
        data mapping norm for color display
    vmin : :obj:`float`, optional
        lower value of colorbar range
    vmax : :obj:`float`, optional 
        upper value of colorbar range
    c_under : :obj:`float`, optional 
        colour of data values smaller than :param:`vmin`
    c_over : :obj:`float`, optional 
        colour of data values exceeding :param:`vmax`
    figh : int
        height of figure in inches
    fix_aspect : :obj:`float`, optional
        if not None, then the figure width is computed by multiplication of
        the input float with input parameter ``figh``
    
    Returns
    -------
    fig
        matplotlib figure instance containing plot
    """
    if isinstance(data, ModelData):
        data = data.grid
    if len(data.coord("time").points) > 1:
        if verbose:
            print("Input data contains more than one time stamp, using first "
                  "time stamp")
        data = data[0]
    tstr = str(data.coord("time").cell(0))

    lons, lats = data.coord("longitude").points, data.coord("latitude").points
    if fix_aspect is not None:
        figsize = (figh * fix_aspect, figh)
    else:
        figsize = calc_figsize(xlim, ylim, figh)
    fig = figure(figsize=figsize)
    ax = fig.add_axes([0.1, .1, .8, .8], projection=ccrs.PlateCarree())
    ax_cbar = fig.add_axes([0.85, .1, .02, .8])
    X, Y = meshgrid(lons, lats)
    cmap = copy(COLOR_THEME.cmap_map)
    if vmin is None:
        vmin = data.data.min()
    if vmax is None:
        vmax = data.data.max()
    cbar_extend = "neither"
    if c_under is not None:
        cmap.set_under(c_under, 1.0)
        cbar_extend = "min"
    if c_over is not None:
        cmap.set_over(c_over, 1.0)
        if cbar_extend == "min":
            cbar_extend = "both"
        else:
            cbar_extend = "max"
    bounds = None
    if log_scale and discrete_norm:
        #to compute upper range of colour range, round up vmax
        exp = float(exponent(vmax) - 1)
        vmax_colors = ceil(vmax / 10**exp)*10**exp
        bounds = get_cmap_levels_auto(vmin=vmin, vmax=vmax_colors, **kwargs)
        norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N, clip=True)
    elif log_scale:
        norm = LogNorm(vmin=vmin, vmax=vmax, clip=True)
    else: 
        norm = None
    disp = ax.pcolormesh(X, Y, data.data, cmap=cmap, norm=norm)
    
    min_mag = -exponent(bounds[1])
    min_mag = 0 if min_mag < 0 else min_mag
    cbar = fig.colorbar(disp, norm=norm, boundaries=bounds, 
                        extend=cbar_extend, cax=ax_cbar,
                        format="%." + str(min_mag) + "f")
    
    #lbls = [x for x in ax_cbar.yaxis.get_tick]
# =============================================================================
#     ax_cbar.set_yticklabels(["{:.{}f}".format(num, min_mag) for 
#                              num in lbls])
# =============================================================================
    #cbar.set_ticklabels(["{:.{}f}".format(num, min_mag) for num in bounds])
    cbar.set_label(data.var_name)
    ax.coastlines(color=COLOR_THEME.color_coastline)
    #things that do not need to be done when day is updated
    lonleft, lonright = xlim
    num_lonticks = 7 if lonleft == -lonright else 6
    digits = 2 - exponent(lonleft)
    digits = 0 if digits < 0 else digits
    latleft, latright = ylim
    num_latticks = 7 if latleft == - latright else 6
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    
    ax.set_xticks(linspace(lonleft, lonright, num_lonticks), 
                   crs=ccrs.PlateCarree())
    ax.set_yticks(linspace(latleft, latright, num_latticks), 
                   crs=ccrs.PlateCarree())
    
    tick_format = '.%df' %digits
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
    
    if fix_aspect:
        ax.set_aspect(fix_aspect)
    return ax
