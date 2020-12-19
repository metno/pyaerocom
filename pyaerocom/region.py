#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functionality related to regions in pyaerocom
"""
from os.path import join, exists
from ast import literal_eval
from collections import OrderedDict as od
from configparser import ConfigParser
import numpy as np
#from pyaerocom import Config
#const = Config()
#from pyaerocom import __dir__
from pyaerocom._lowlevel_helpers import BrowseDict

class Region(BrowseDict):
    """Interface that specifies an AEROCOM region

    Note
    ----
    Extended dictionary-like object

    Attributes
    ----------
    name : str
        ID of region (e.g. "EUROPE")
    lon_range : :obj:`list` or :obj:`tuple`
        longitude range (min, max) covered by region
    lat_range : :obj:`list` or :obj:`tuple`
        latitude range (min, max) covered by region
    lon_range_plot : :obj:`list` or :obj:`tuple`
        longitude range (min, max) used for plotting region. Defaults to
        values of :attr:`lon_range` but may be extended, see e.g.
        `the example of india <http://aerocom.met.no/DATA/SURFOBS/
        ECMWF_OSUITE_NRT/plots/OD550_AER_an2018_d20180319_INDIA_MAP.ps.png>`__
    lat_range_plot : :obj:`list` or :obj:`tuple`
        latitude range (min, max) used for plotting region. Defaults to
        values of :attr:`lat_range` but may be extended, see e.g.
        `the example of india <http://aerocom.met.no/DATA/SURFOBS/
        ECMWF_OSUITE_NRT/plots/OD550_AER_an2018_d20180319_INDIA_MAP.ps.png>`__

    Parameters
    ----------
    name : str
        ID of region (e.g. "EUROPE")
    lon_range : :obj:`list` or :obj:`tuple`
        longitude range (min, max) covered by region
    lat_range : :obj:`list` or :obj:`tuple`
        latitude range (min, max) covered by region
    """
    def __init__(self, name="WORLD", lon_range=None, lat_range=None,
                 **kwargs):
        self._name = name
        # longitude / latitude range of data
        self.lon_range = lon_range
        self.lat_range = lat_range

        # longitude / latitude range of data in plots
        self.lon_range_plot = None
        self.lat_range_plot = None

        self.lon_ticks = None
        self.lat_ticks = None

        if isinstance(name, str) and any([x == None for x in [lon_range, lat_range]]):
           self.import_default(name)

        for k, v in kwargs.items():
            if k in self:
                self[k] = v

    @property
    def name(self):
        """Name of region"""
        return self._name

    @property
    def is_htap(self):
        from pyaerocom import const

        if self._name in const.HTAP_REGIONS:
            return True
        else:
            return False

    def import_default(self, name):
        """Import information about default region

        Parameters
        ----------
        name : str
            strind ID of region (must be specified in `regions.ini <https://
            github.com/metno/pyaerocom/blob/master/pyaerocom/data/regions.ini>`__
            file)

        Raises
        ------
        IOError
            if regions.ini file does not exist
        NameError
            if default region with ID specified by input parameter ``name``
            cannot be found in regions.ini file
        """
        from pyaerocom import __dir__
        name = name.upper()
        fpath = join(__dir__, "data", "regions.ini")
        if not exists(fpath):
            raise IOError("Regions ini file could not be found: %s"
                          %fpath)
        conf_reader = ConfigParser()
        conf_reader.read(fpath)

        if not name in conf_reader:
            raise AttributeError("No default region available for %s" %name)
        self._name = name
        for key, val in conf_reader[name].items():
            if key in self.keys():
                if "," in val:
                    #list of values
                    val = list(literal_eval(val))#[float(x) for x in val.split(",")]
                else:
                    try:
                        val = int(val)
                    except Exception:
                        pass
                self[key] = val
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

    def plot(self, ax=None):
        """

        Returns
        -------
        ax
            Map plot indicating region
        """
        from cartopy.mpl.geoaxes import GeoAxes
        from pyaerocom.plot.mapping import init_map
        if ax is None:
            ax = init_map()
        if not isinstance(ax, GeoAxes):
            raise ValueError('Invalid input for ax: need cartopy GeoAxes..')
        if not self.is_htap:
            return ax

        from pyaerocom.helpers_landsea_masks import load_region_mask_xr

        ax.axes.set_xlabel('Longitude')
        ax.axes.set_ylabel('Latitude')
        ax.axes.set_title("Region name: {}".format(self.name))
        mask = load_region_mask_xr(self.name)
        #import numpy as np
        data = mask.data
        data[data==0]=np.nan
        mask.data = data

        mask.plot(ax=ax)
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
    from pyaerocom import const
    return get_all_default_region_ids() + const.HTAP_REGIONS

def get_all_default_region_ids(use_all_in_ini=False):
    """Get list containing IDs of all default regions

    Parameters
    ----------
    use_all_in_ini : bool
        if True, then all regions defined in regions.ini are used, else,
        the list of regions, defined in header of :class:`Config`

    Returns
    -------
    list
        all default region IDs (sections in `regions.ini <https://github.com/
        metno/pyaerocom/blob/master/pyaerocom/data/regions.ini>`__ file)
    """
    if not use_all_in_ini:
        from pyaerocom import const
        return const.OLD_AEROCOM_REGIONS
    from pyaerocom import __dir__
    fpath = join(__dir__, "data", "regions.ini")
    if not exists(fpath):
        raise IOError("File conventions ini file could not be found: %s"
                      %fpath)
    conf_reader = ConfigParser()
    conf_reader.read(fpath)
    all_ids = []
    for rid, region in conf_reader.items():
        if not rid == "DEFAULT":
            all_ids.append(rid)

    return all_ids

def get_all_default_regions(use_all_in_ini=False):
    """Get dictionary containing all default regions from region.ini file

    Note
    ----
        The values are already :class:`Region` instances, use
        :func:`get_all_default_region_ids`

    Returns
    -------
    dict
        dictionary containing all default regions that are found in
        the `regions.ini <https://github.com/metno/pyaerocom/blob/
        master/pyaerocom/data/regions.ini>`__ file

    """
    all_regions = od()
    if not use_all_in_ini:
        from pyaerocom import const
        for region in const.OLD_AEROCOM_REGIONS:
            all_regions[region] = Region(region)
        return all_regions
    from pyaerocom import __dir__
    fpath = join(__dir__, "data", "regions.ini")
    if not exists(fpath):
        raise IOError("File conventions ini file could not be found: %s"
                      %fpath)
    conf_reader = ConfigParser()
    conf_reader.read(fpath)

    for region in conf_reader:
        if not region == "DEFAULT": # TODO this should be updated right Jonas?
            all_regions[region] = Region(region)

    return all_regions

#: ToDO: check how to handle methods properly with HTAP regions...
def get_regions_coord(lat, lon, default_regs=None, **add_regions):
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
    **add_regions
        additional regions other than default regions, that are supposed to
        be considered

    Returns
    -------
    list
        list of regions that contain this coordinate
    """

    regs = []
    if default_regs is None:
        default_regs = get_all_default_regions(use_all_in_ini=False)
    for an, ar in add_regions.items():
        if isinstance(ar, Region):
            if not ar.is_htap:
                default_regs[an] = ar

    for rname, reg in default_regs.items():
        if rname == 'WORLD':
            continue
        if reg.contains_coordinate(lat, lon):
            regs.append(rname)
    if len(regs) == 0:
        regs.append('WORLD')
    return regs

def find_closest_region_coord(lat, lon, default_regs=None, **add_regions):
    """Find region that has it's center closest to input coordinate

    Parameters
    ----------
    lat : float
        latitude of coordinate
    lon : float
        longitude of coordinate
    **add_regions
        additional regions other than default regions, that are supposed to
        be considered

    Returns
    -------
    str
        name of square region
    """
    regs = get_regions_coord(lat, lon, default_regs=default_regs,
                             **add_regions)

    if len(regs) == 1:
        return regs[0]
    else:
        default_ids = get_all_default_region_ids()
        min_dist = 1e6
        best = None
        for rname in regs:
            if rname in default_ids:
                r = Region(rname)
            else:
                r = add_regions[rname]
            d = r.distance_to_center(lat, lon)
            if d < min_dist:
                min_dist = d
                best=rname
        return best

def valid_default_region(name):
    """Boolean specifying whether input region is valid or not"""
    if isinstance(name, str):
        return True if name.upper() in get_all_default_region_ids() else False
    return False

if __name__=="__main__":
    import matplotlib.pyplot as plt
    plt.close('all')
    r = Region("EUR")
    ax = r.plot()

    import numpy as np
    from pyaerocom.helpers_landsea_masks import load_region_mask_xr

    mask = load_region_mask_xr('EUR', 'PAN')

    print(r.is_htap)
    r.import_default("EUROPE")

    all_ids = get_all_default_region_ids(True)

    lat, lon = 10, 20
    reg = find_closest_region_coord(lat, lon)

    print(reg)
    print(valid_default_region)
