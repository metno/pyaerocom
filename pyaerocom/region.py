#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functionality related to regions in pyaerocom
"""
import numpy as np

from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.helpers_landsea_masks import load_region_mask_xr
from pyaerocom.region_defs import (REGION_DEFS, # all region definitions
                                   HTAP_REGIONS, # list of HTAP regions
                                   OLD_AEROCOM_REGIONS,
                                   REGION_NAMES) # custom names (dict)

class Region(BrowseDict):
    """Class specifying a region

    Attributes
    ----------
    region_id : str
        ID of region (e.g. EUROPE)
    name : str
        name of region (e.g. Europe) used e.g. in plotting.
    lon_range : list
        longitude range (min, max) covered by region
    lat_range : list
        latitude range (min, max) covered by region
    lon_range_plot : list
        longitude range (min, max) used for plotting region.
    lat_range_plot : list
        latitude range (min, max) used for plotting region.
    lon_ticks : list
        list of longitude ticks used for plotting
    lat_ticks : list
        list of latitude ticks used for plotting

    Parameters
    ----------
    region_id : str
        ID of region (e.g. "EUROPE"). If the input region ID is registered as
        a default region in :mod:`pyaerocom.region_defs`, then the default
        information is automatically imported on class instantiation.
    **kwargs
        additional class attributes (see above for available default attributes).
        Note, any attr. values provided by kwargs are preferred over
        potentially defined default attrs. that are imported automatically.
    """
    def __init__(self, region_id=None,**kwargs):

        if region_id is None:
            region_id = 'WORLD'

        if region_id in REGION_NAMES:
            name = REGION_NAMES[region_id]
        else:
            name = region_id

        self.region_id = region_id
        self.name = name

        self.lon_range = None
        self.lat_range = None

        # longitude / latitude range of data in plots
        self.lon_range_plot = None
        self.lat_range_plot = None

        self.lon_ticks = None
        self.lat_ticks = None

        self._mask_data = None
        if region_id in REGION_DEFS:
            self.import_default(region_id)



        self.update(**kwargs)

    def is_htap(self):
        """Boolean specifying whether region is an HTAP binary region"""
        return True if self.region_id in HTAP_REGIONS else False

    def import_default(self, region_id):
        """Import region definition

        Parameters
        ----------
        region_id : str
            ID of region

        Raises
        ------
        KeyError
            if no region is registered for the input ID
        """
        self.update(REGION_DEFS[region_id])

        if self.lon_range_plot is None:
            self.lon_range_plot = self.lon_range
        if self.lat_range_plot is None:
            self.lat_range_plot = self.lat_range

    @property
    def center_coordinate(self):
        """Center coordinate of this region"""
        latc = self.lat_range[0] + (self.lat_range[1] - self.lat_range[0])/2
        lonc = self.lon_range[0] + (self.lon_range[1] - self.lon_range[0])/2
        return (latc, lonc)

    def distance_to_center(self, lat, lon):
        """Compute distance of input coordinate to center of this region

        Parameters
        ----------
        lat : float
            latitude of coordinate
        lon : float
            longitude of coordinate

        Returns
        -------
        float
            distance in km
        """
        from pyaerocom.geodesy import calc_distance
        cc = self.center_coordinate
        return calc_distance(lat0=cc[0],
                             lon0=cc[1],
                             lat1=lat,
                             lon1=lon)

    def contains_coordinate(self, lat, lon):
        """Check if input lat/lon coordinate is contained in region

        Parameters
        ----------
        lat : float
            latitude of coordinate
        lon : float
            longitude of coordinate

        Returns
        -------
        bool
            True if coordinate is contained in this region, False if not
        """
        lat_ok = self.lat_range[0] <= lat <= self.lat_range[1]
        lon_ok = self.lon_range[0] <= lon <= self.lon_range[1]
        return lat_ok * lon_ok

    def mask_available(self):
        if not self.is_htap():
            return False
        return True

    def get_mask_data(self):
        if not self.mask_available():
            raise AttributeError(
                f'No binary mask data available for region {self.region_id}.'
                )
        if self._mask_data is None:
            self._mask_data = load_region_mask_xr(self.region_id)
        return self._mask_data

    def plot_mask(self, ax, color, alpha=0.2):

        mask = self.get_mask_data()
        #import numpy as np
        data = mask.data
        data[data==0] = np.nan
        mask.data = data

        mask.plot(ax=ax)
        return ax

    def plot_borders(self, ax, color, lw=2):
        raise NotImplementedError('Coming soon...')

    def plot(self, ax=None):
        """
        Plot this region

        Draws a rectangle of the outer bounds of the region and if a binary
        mask is available for this region, it will be plotted as well.

        Parameters
        ----------
        ax : GeoAxes, optional
            axes instance to be used for plotting. Defaults to None in which
            case a new instance is created.

        Returns
        -------
        GeoAxes
            axes instance used for plotting

        """
        from cartopy.mpl.geoaxes import GeoAxes
        from pyaerocom.plot.mapping import init_map
        if ax is None:
            ax = init_map()
        elif not isinstance(ax, GeoAxes):
            raise ValueError('Invalid input for ax: need cartopy GeoAxes..')

        if self.mask_available():
            self.plot_mask(ax, color='r')

        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        name = self.name
        if not name ==  self.region_id:
            name += f' (ID={self.region_id})'

        ax.set_title(name)

        return ax

    def __contains__(self, val):
        if not isinstance(val, tuple):
            raise TypeError('Invalid input, need tuple')
        if not len(val) == 2:
            raise ValueError('Invalid input: coordinate must contain 2 '
                             'elements (lat, lon)')
        return self.contains_coordinate(lat=val[0], lon=val[1])

    def __repr__(self):
       return ("Region %s %s" %(self.name, super(Region, self).__repr__()))

    def __str__(self):
        s = ("pyaeorocom Region\nName: %s\n"
             "Longitude range: %s\n"
             "Latitude range: %s\n"
             "Longitude range (plots): %s\n"
             "Latitude range (plots): %s"
             %(self.name, self.lon_range, self.lat_range,
               self.lon_range_plot, self.lat_range_plot))
        return s

def all():
    """Wrapper for :func:`get_all_default_region_ids`"""
    return list(REGION_DEFS)

def get_all_default_region_ids():
    """Get list containing IDs of all default regions

    Returns
    -------
    list
        IDs of all predefined default regions
    """
    return OLD_AEROCOM_REGIONS

def _get_regions_helper(reg_ids):
    """
    Get dictionary of :class:`Region` instances for input IDs

    Parameters
    ----------
    reg_ids : list
        list of region IDs

    Returns
    -------
    dict
        keys are input region IDs, values are loaded :class:`Region` instances
    """
    regs = {}
    for reg in reg_ids:
        reg[reg] = Region(reg)
    return regs

def get_old_aerocom_default_regions():
    """
    Load dictionary with default AeroCom regions

    Returns
    -------
    dict
        keys are region ID's, values are instances of :class:`Region`
    """
    return _get_regions_helper(OLD_AEROCOM_REGIONS)


def get_htap_regions():
    """
    Load dictionary with HTAP regions

    Returns
    -------
    dict
        keys are region ID's, values are instances of :class:`Region`
    """
    return _get_regions_helper(HTAP_REGIONS)

def get_all_default_regions():
    """Get dictionary containing all default regions from region.ini file

    Returns
    -------
    dict
        dictionary containing all default regions; keys are region ID's, values
        are instances of :class:`Region`.

    """
    return get_old_aerocom_default_regions()

#: ToDO: check how to handle methods properly with HTAP regions...
def get_regions_coord(lat, lon, regions=None):
    """Get all regions that contain input coordinate

    Note
    ----
    This does not yet include HTAP, since this causes troules in automated
    AeroCom processing

    Parameters
    ----------
    lat : float
        latitude of coordinate
    lon : float
        longitude of coordinate
    regions : dict, optional
        dictionary containing instances of :class:`Region` as values, which
        are considered. If None, then all default regions are used.

    Returns
    -------
    list
        list of regions that contain this coordinate
    """

    matches = []
    if regions is None:
        regions = get_all_default_regions(use_all_in_ini=False)
    for rname, reg in regions.items():
        if rname == 'WORLD': # always True
            continue
        if reg.contains_coordinate(lat, lon):
            matches.append(rname)
    if len(matches) == 0:
        matches.append('WORLD')
    return matches

def find_closest_region_coord(lat, lon, regions=None):
    """Find region that has it's center closest to input coordinate

    Parameters
    ----------
    lat : float
        latitude of coordinate
    lon : float
        longitude of coordinate
    regions : dict, optional
        dictionary containing instances of :class:`Region` as values, which
        are considered. If None, then all default regions are used.

    Returns
    -------
    str
        region ID of identified region
    """
    if regions is None:
        regions = get_all_default_regions(use_all_in_ini=False)

    matches = get_regions_coord(lat, lon, regions)

    if len(matches) == 1:
        return matches[0]

    min_dist = 1e6
    best = None
    for match in matches:
        region = regions[match]
        dist = region.distance_to_center(lat, lon)
        if dist < min_dist:
            min_dist = dist
            best=match
    return best

if __name__=="__main__":
    import matplotlib.pyplot as plt
    plt.close('all')
    import pyaerocom as pya
    res = {}
    reg = Region('NAM')
    reg.plot()

# =============================================================================
#     for reg in pya.region_defs.HTAP_REGIONS:
#
#         mask = pya.helpers_landsea_masks.load_region_mask_xr(reg)
#         res[reg] = info = pya.helpers_landsea_masks.get_lat_lon_range_mask_region(mask)
#         lonr, latr = info['lon_range'], info['lat_range']
#
#
#         print(f'[{reg}]')
#         print(f'lon_range={lonr[0]:.3f},{lonr[1]:.3f}')
#         print(f'lat_range={latr[0]:.3f},{latr[1]:.3f}')
#         print()
# =============================================================================
