#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper methods for plotting sub-package
"""
from pyaerocom.mathutils import exponent
import numpy as np

def calc_figsize(lons, lats, figh=8, add_cbar=False):
    wfac = lons.shape[0] / lats.shape[0]
    if add_cbar:
        wfac += 2
    figw = figh * wfac
    return (figw, figh)
    
def custom_mpl(mpl_rcparams, **kwargs):
    small = 10
    medium = 12
    big = 14
    
    default = {'font.size'          :   small, 
               'axes.titlesize'     :   big,
               'axes.labelsize'     :   medium, 
               'xtick.labelsize'    :   medium, 
               'ytick.labelsize'    :   medium, 
               'legend.fontsize'    :   small, 
               'figure.titlesize'   :   big}
    
    for k, v in default.items():
        try:
            mpl_rcparams[k] = kwargs[k]
        except:
            mpl_rcparams[k] = v
    return mpl_rcparams
    
def get_cmap_levels_auto(vmin, vmax, num_per_mag=10):
    """Initiate pseudo-log discrete colormap levels
    
    Note
    ----
        This is a beta version and aims to 
        
    Parameters
    ----------
    vmin : float
        lower end of colormap (e.g. minimum value of data)
    vmax : float
        upper value of colormap (e.g. maximum value of data)
    """
    high = exponent(vmax)
    low = -3 if vmin == 0 else exponent(vmin)
    lvls =[0]
    if 1%vmax*10**(-high) == 0: 
        low+=1
        high-=1
    for mag in range(low, high):
        lvls.extend(np.linspace(1, 10, num_per_mag-1, endpoint=0)*10**(mag))
    lvls.extend(np.linspace(1, vmax*10**(-high), num_per_mag, endpoint=1)*10**(high))
    
    return lvls

def get_cmap_ticks_auto(lvls, num_per_mag=3):
    """Compute cmap ticks based on cmap levels 
    
    The cmap levels may be computed automatically using 
    :func:`get_cmap_levels_auto`.
    
    Parameters
    ----------
    lvls : list
        list containing colormap levels
    num_per_mag : int
        desired number of ticks per magnitude
    """
    low = exponent(lvls[1]) # second entry (first is 0)
    vmax = lvls[-1]
    high = exponent(vmax)
    
    ticks = [0]
    if 1%vmax*10**(-high) == 0: 
        for mag in range(low, high-1):
            ticks.extend(np.linspace(1, 10, num_per_mag, endpoint=0)*10**(mag))
        ticks.extend(np.linspace(1, 10, num_per_mag+1, endpoint=1)*10**(high-1))
    else:
        for mag in range(low, high):
            ticks.extend(np.linspace(1, 10, num_per_mag, endpoint=0)*10**(mag))
        ticks.extend(np.linspace(1, vmax*10**(-high), 
                     num_per_mag+1, endpoint=1)*10**(high))
        
    return ticks