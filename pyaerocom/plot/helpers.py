#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper methods for plotting sub-package
"""
from pyaerocom.mathutils import exponent
import numpy as np
import cartopy.crs as ccrs

def projection_from_str(projection_str="Stereographic"):
    """Return instance of cartopy projection class based on string ID"""
    return ccrs.__dict__[projection_str]()

def custom_mpl(mpl_rcparams=None, default_large=True, **kwargs):
    """Custom matplotlib settings"""
    if mpl_rcparams is None:
        from matplotlib import rcParams as mpl_rcparams
    small = 10
    medium = 12
    big = 14
    huge = 18
    if default_large:
        default = {'font.size'          :   huge,
                   'axes.titlesize'     :   huge,
                   'axes.labelsize'     :   huge,
                   'xtick.labelsize'    :   big,
                   'ytick.labelsize'    :   big,
                   'legend.fontsize'    :   big,
                   'figure.titlesize'   :   huge}
    else:
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
        except Exception:
            mpl_rcparams[k] = v
    return mpl_rcparams

def calc_figsize(lon_range, lat_range, figh=8):
    """Calculate figure size based on data

    The required figure width is computed based on the input height and the
    aspect ratio of the longitude and latitude arrays

    Parameters
    ----------
    lon_range : tuple
        2-element tuple specifying longitude range (may also be list or array)
    lat_range : tuple
        2-element tuple specifying latitude range (may also be list or array)
    figh : int
        figure height in inches
    add_cbar : bool
        if True, the width is adapted accordingly

    Returns
    -------
    tuple
        2-element tuple containing figure width and height
    """
    wfac = (lon_range[1] - lon_range[0]) / (lat_range[1] - lat_range[0])
    figw = int(wfac*figh)

    return (figw, figh)

def calc_pseudolog_cmaplevels(vmin, vmax, add_zero=False):
    """Initiate pseudo-log discrete colormap levels

    Parameters
    ----------
    vmin : float
        lower end of colormap (e.g. minimum value of data)
    vmax : float
        upper value of colormap (e.g. maximum value of data)
    add_zero : bool
        if True, the lower bound is set to 0 (irrelevant if vmin is 0).

    Returns
    -------
    list
        list containing boundary array for discrete colormap (e.g. using
        BoundaryNorm)

    Example
    -------
    >>> vmin, vmax = 0.02, 0.75
    >>> vals = calc_pseudolog_cmaplevels(vmin, vmax, num_per_mag=10, add_zero=True)
    >>> for val in vals: print("%.4f" %val)
    0.0000
    0.0100
    0.0126
    0.0158
    0.0200
    0.0251
    0.0316
    0.0398
    0.0501
    0.0631
    0.0794
    0.1000

    """

    if vmin < 0:
        vmin = 0
    if vmin == 0:
        vmin = 1*10.0**(exponent(vmax) - 2)
        if not add_zero:
            add_zero = True
    elif vmax < vmin:
        raise ValueError("Error: vmax must exceed vmin")
    bounds = [0] if add_zero else []
    low =  float(exponent(vmin))
    high = float(exponent(vmax))
    bounds.extend(np.arange(np.floor(vmin*10**(-low)), 10, 1)*10.0**(low))
    if low == high:
        return bounds

    for mag in range(int(low+1), int(high)):
        bounds.extend(np.linspace(1,9,9)*10**(mag))
    bounds.extend(np.arange(1, np.ceil(vmax*10**(-high)), 1)*10.0**(high))
    bounds.append(vmax)
    return bounds

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
    high = float(exponent(vmax))
    low = -3. if vmin == 0 else float(exponent(vmin))
    lvls =[]
    if 1%vmax*10**(-high) == 0:
        low+=1
        high-=1
    for mag in range(int(low), int(high)):
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

if __name__=="__main__":

    vmin, vmax = 0.02, 0.75

    vals = calc_pseudolog_cmaplevels(vmin, vmax, num_per_mag=10, add_zero=True)
    for val in vals: print("%.4f" %val)

    import doctest
    doctest.testmod()
