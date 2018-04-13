#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from matplotlib.pyplot import figure
from iris.quickplot import pcolormesh
import cartopy.crs as ccrs
from pyaerocom.plot.config import COLOR_THEME
from pyaerocom.plot.helpers import calc_figsize

def plot_map(data, xlim=(-180, 180), ylim=(-90, 90), figh=8, 
             color_theme=COLOR_THEME, fix_aspect=None):
    """Make a quick plot onto a map
    
    Parameters
    ----------
    time_idx : int
        index in time to be plotted
    xlim : tuple
        2-element tuple specifying plotted longitude range
    ylim : tuple
        2-element tuple specifying plotted latitude range
    figh : int
        height of figure in inches
    color_theme : str
        pyaerocom color theme
    fix_aspect : :obj:`float`, optional
        if not None, then the figure width is computed by multiplication of
        the input float with input parameter ``figh``
    
    Returns
    -------
    fig
        matplotlib figure instance containing plot
    """
    if fix_aspect is not None:
        figsize = (figh * fix_aspect, figh)
    else:
        figsize = (calc_figsize(data.longitude, data.latitude, figh), figh)
    fig = figure(figsize=figsize)
    ax = fig.add_axes([0.1, .1, .8, .8], projection=ccrs.PlateCarree())
    pcolormesh(data, cmap=COLOR_THEME.cmap_map)
    
    ax.coastlines(color=COLOR_THEME.color_coastline)
    #things that do not need to be done when day is updated
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    
    ax.set_yticks([-60, -30, 0, 30, 60], crs=ccrs.PlateCarree())
    ax.set_xticks([-180, -90, 0, 90, 180], crs=ccrs.PlateCarree())
    if fix_aspect:
        ax.set_aspect(fix_aspect)
    return ax