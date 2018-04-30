#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains plot routines for Aerocom data. So far, this includes a
low level, very flexible plot method
"""
from copy import copy
from matplotlib.pyplot import figure
from matplotlib.colors import BoundaryNorm, LogNorm
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from numpy import meshgrid, linspace, ceil

from pyaerocom import const
from pyaerocom.plot.config import COLOR_THEME, ColorTheme
from pyaerocom.plot.helpers import (calc_figsize, custom_mpl, 
                                    calc_pseudolog_cmaplevels)
from pyaerocom.mathutils import exponent
from pyaerocom.modeldata import ModelData
from pyaerocom.variable import Variable
from pyaerocom.region import Region

custom_mpl()

def plot_map(data, xlim=(-180, 180), ylim=(-90, 90), vmin=None, vmax=None, 
             add_zero=False, c_under=None, c_over=None, log_scale=True, 
             discrete_norm=True, figh=8, fix_aspect=None, 
             color_theme=COLOR_THEME, fig=None, verbose=const.VERBOSE):
    """Make a plot of grid data onto a map
    
    Parameters
    ----------
    data : :obj:`ModelData` or :obj:`iris.cube.Cube`
        input data from one timestamp. May also be of type 
        :class:`pyaerocom.ModelData`. Uses first time stamp if data is has 
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
    if isinstance(data, ModelData):
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
            figsize = (figh + .05, figh)
        else:
            figsize = calc_figsize(xlim, ylim, figh)
        fig = figure(figsize=figsize)
    else:
        fig.clf()
    ax = fig.add_axes([0.1, .1, .8, .8], projection=ccrs.PlateCarree())
    ax_cbar = fig.add_axes([0.905, .1, .02, .8])
    X, Y = meshgrid(lons, lats)
    cmap = copy(color_theme.cmap_map)
    if vmin is None:
        vmin = data.data.min()
    if vmax is None:
        vmax = data.data.max()
            
    bounds = None
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

    cbar.set_label(data.var_name)
    ax.coastlines(color=COLOR_THEME.color_coastline)


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
        ax.set_aspect(aspect=fix_aspect)
    return fig

def plot_map_aerocom(data, variable, region, fig=None, **kwargs):
    """High level plotting function to produce map of species
    
    Parameters
    ----------
    data : :obj:`ModelData`
        input data from one timestamp.
        
    """
    if not isinstance(data, ModelData):
        raise TypeError("This plotting method needs an instance of pyaerocom "
                         "ModelData on input, got: %s" %type(data))
    if isinstance(variable, str):
        variable = Variable(variable)
    if not isinstance(variable, Variable):
        raise TypeError("Need input of type str or Variable for input param "
                        "variable, got: %s" %type(variable))
    if isinstance(region, str):
        region = Region(region)
    if not isinstance(region, Region):
        raise TypeError("Need input of type str or Region for input param "
                        "region, got: %s" %type(variable))    
    
if __name__ == "__main__":
    import pyaerocom
    
    read = pyaerocom.io.ReadModelData("ECMWF_OSUITE", start_time="2010",
                                      stop_time="2019")
    
    data = read.read_var("od550aer")
    [print(f) for f in read._match_files]
