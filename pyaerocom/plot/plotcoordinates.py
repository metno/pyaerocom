#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from pyaerocom.plot.mapping import init_map
import cartopy

def plot_coordinates(lons, lats, xlim=(-180, 180), ylim=(-90, 90),
                     label=None, legend=True, color='r', marker='o',
                     markersize=8, fontsize_base=10,
                     ax=None, **kwargs):
    """Plot input coordinates on a map

    lons : :obj:`ndarray`
        array of longitude coordinates (can also be list or tuple)
    lats : :obj:`ndarray`
        array of latitude coordinates (can also be list or tuple)

    """
    if not isinstance(ax, cartopy.mpl.geoaxes.GeoAxes):
        ax = init_map(xlim, ylim, ax=ax, **kwargs)

    if label is None:
        label = '{} stations'.format(len(lons))

    ax.scatter(lons, lats, markersize, marker=marker, color=color,
               label=label)

    if legend and label:
        ax.legend()

    return ax

if __name__ == '__main__':
    import pyaerocom as pya
    import matplotlib.pyplot as plt
    plt.close('all')
    r = pya.io.ReadUngridded()

    d = r.read(pya.const.AERONET_SUN_V3L2_AOD_DAILY_NAME,
               vars_to_retrieve=['od550aer'])

    d1 = r.read('EBASMC', vars_to_retrieve=['scatc550aer'])

    ax = plot_coordinates(d.longitude, d.latitude, label='AERONET L2V3',
                          legend=False)

    ax = plot_coordinates(d1.longitude, d1.latitude, label='EBAS',
                          legend=True, ax=ax,
                          color='lime', markersize=22, marker='^')
