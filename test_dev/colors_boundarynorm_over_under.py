#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 17:40:10 2018

@author: jonasg
"""

from copy import copy
from matplotlib.pyplot import figure, get_cmap
from matplotlib.colors import BoundaryNorm, LogNorm
from matplotlib.colorbar import ColorbarBase
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from numpy import meshgrid, linspace, ceil
from pyaerocom.glob import VERBOSE
from pyaerocom.plot.config import COLOR_THEME
from pyaerocom.plot.helpers import (calc_figsize, get_cmap_levels_auto,
                                    custom_mpl)
from pyaerocom.mathutils import exponent
import numpy as np

if __name__=="__main__":
    
    fig = figure()
    ax =fig.add_axes([.1,.1,.8,.8])
    ax_cbar =fig.add_axes([.92,.1,.03,.8])
    data = np.random.random_sample((20,20))
    
    vmin = 0.2
    vmax = 0.8
    cmap = get_cmap("viridis")
    cmap.set_under("w")
    cmap.set_over("r")
    
    levels = get_cmap_levels_auto(vmin, vmax)
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=False)
    
    X, Y = np.meshgrid(np.linspace(0,20,20), np.linspace(0,20,20))
    disp = ax.pcolormesh(X, Y, data.data, cmap=cmap, norm=norm)
    
    cbar = fig.colorbar(disp, cmap=cmap, norm=norm, boundaries=[-1000] + levels +[10000], 
                        extend="both", cax=ax_cbar)
    