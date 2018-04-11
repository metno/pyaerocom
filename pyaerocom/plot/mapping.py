#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The mapping module contains functionality to plot maps
"""
from matplotlib.colors import BoundaryNorm
from matplotlib.backends.backend_agg import FigureCanvasAgg #canvas

from functools import partial
from matplotlib.pyplot import get_cmap
import numpy as np
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


import multiprocessing

class MultiPlot(multiprocessing.pool.Pool):
    pass

def plot_grid_data(cube, day_idx=0, lon_range=(-180, 180), 
                   lat_range=(-90, 90), vmin=None, vmax=None, 
                   cmap_id="jet"):
    """Plot variable on map using pcolormesh
    
    Parameters
    ----------
    cube : iris.cube.Cube
        cube containing data. Note that the input cube must correspond 2D cube
        containing data from one time stamp (i.e. ndim=2).
    day_idx : int
        index of timestamp that is to be plotted
    lon_range : tuple
        tuple specifying plotted longitude range 
    lat_range : tuple
        tuple specifying plotted latitude range
    vmin : float
        lower limit for AOD display
    vmax : float
        upper limit for AOD display
    cmap_id : str
        string ID of matplotlib colormap supposed to be used
    """    
    if fig.canvas is None:
        FigureCanvasAgg(fig)
    if cube.ndim != 3:
        msg = ("Invalid dimension %d of input cube, need ndim=2 (i.e. data "
               "corresponding to one timestamp" %cube.ndim)
        raise ValueError(msg)
    dat = cube[day_idx]
    
    geo_ax = fig.add_axes([0.1, .1, .8, .8], projection=ccrs.PlateCarree())
    ax_cbar = fig.add_axes([0.85, .1, .02, .8])
    
    lvls = funs.init_cmap_levels(vmin, vmax)
    cmap = get_cmap(cmap_id)
    norm = BoundaryNorm(lvls, ncolors=cmap.N, clip=True)
    
    lons, lats = dat.coord("longitude").points, dat.coord("latitude").points
    X, Y = np.meshgrid(lons, lats)
    mesh = geo_ax.pcolormesh(X, Y, dat.data, cmap=cmap, norm=norm)#, figure=fig)
    #mesh = iplt.pcolormesh(cube,cmap=cmap, norm=norm, figure=fig)
    geo_ax.coastlines(color=COASTLINE_COLOR)
    #things that do not need to be done when day is updated
    
    ticks = funs.get_cmap_ticks(lvls)
# =============================================================================
#     try:
#         ax_cbar = fig.axes[1]
#         [x.remove for x in ax_cbar.artists]
# =============================================================================
    cbar = fig.colorbar(mesh, norm=norm, boundaries=lvls, cax=ax_cbar)
# =============================================================================
#     except:
#         cbar = fig.colorbar(mesh, norm=norm, boundaries=lvls)
# =============================================================================
    # Set some suitable fixed "logarithmic" colourbar tick positions.
    cbar.set_ticks(ticks)
    cbar.set_label(funs.var_str(dat))
    # Modify the tick labels so that the centre one shows "+/-<minumum-level>".
    #tick_levels[3] = r'$\pm${:g}'.format(minimum_log_level)
    cbar.set_ticklabels(["%.3f" %x for x in ticks])
    
    geo_ax.set_xlim([lon_range[0], lon_range[1]])
    geo_ax.set_ylim([lat_range[0], lat_range[1]])
    
    geo_ax.set_xticks(np.linspace(lon_range[0], lon_range[1], 7), 
                   crs=ccrs.PlateCarree())
    geo_ax.set_yticks(np.linspace(lat_range[0], lat_range[1], 7), 
                   crs=ccrs.PlateCarree())
    
    lon_formatter = LongitudeFormatter(number_format='.1f',
                                       degree_symbol='',
                                       dateline_direction_label=True)
    lat_formatter = LatitudeFormatter(number_format='.1f',
                                      degree_symbol='')
    
    geo_ax.xaxis.set_major_formatter(lon_formatter)
    geo_ax.yaxis.set_major_formatter(lat_formatter)

    geo_ax.set_xlabel("Longitude", fontsize=12)
    geo_ax.set_ylabel("Latitude", fontsize=12)
    # Label the colourbar to show the units.
    #bar.set_label('[{}, log scale]'.format(anomaly.units))
    tit = ("%s %s mean: %.3f" %(funs.var_str(dat), 
                                funs.daystring(cube, day_idx),
                                funs.area_weighted_mean(dat)))
    geo_ax.set_title(tit)
    return fig

