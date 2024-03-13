"""
This module contains functionality related to regions in pyaerocom
"""

from __future__ import annotations

import numpy as np

from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.config import ALL_REGION_NAME
from pyaerocom.helpers_landsea_masks import get_mask_value, load_region_mask_xr
from pyaerocom.region_defs import HTAP_REGIONS  # list of HTAP regions
from pyaerocom.region_defs import REGION_DEFS  # all region definitions
from pyaerocom.region_defs import OLD_AEROCOM_REGIONS, REGION_NAMES  # custom names (dict)

POSSIBLE_REGION_OCEAN_NAMES = ["OCN", "Oceans"]


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

    def __init__(self, region_id=None, **kwargs):
        if region_id is None:
            region_id = ALL_REGION_NAME

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
        latc = self.lat_range[0] + (self.lat_range[1] - self.lat_range[0]) / 2
        lonc = self.lon_range[0] + (self.lon_range[1] - self.lon_range[0]) / 2
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
        return calc_distance(lat0=cc[0], lon0=cc[1], lat1=lat, lon1=lon)

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

        lat_lb = self.lat_range[0]
        lat_ub = self.lat_range[1]
        lon_lb = self.lon_range[0]
        lon_ub = self.lon_range[1]
        # latitude bounding boxes should always be defined with the southern most boundary less than the northernmost
        lat_ok = lat_lb <= lat <= lat_ub
        # if the longitude bounding box has a lowerbound less than the upperbound
        if lon_lb < lon_ub:
            # it suffices to check that lon is between these values
            lon_ok = lon_lb <= lon <= lon_ub
        # if the longitude lowerbound has a value lessthan the upperbound
        elif lon_ub < lon_lb:
            # lon is contained in the bounding box in two cases
            lon_ok = lon < lon_ub or lon > lon_lb
        else:
            lon_ok = False  # safeguard
        return lat_ok * lon_ok

    def mask_available(self):
        if not self.is_htap():
            return False
        return True

    def get_mask_data(self):
        if not self.mask_available():
            raise AttributeError(f"No binary mask data available for region {self.region_id}.")
        if self._mask_data is None:
            self._mask_data = load_region_mask_xr(self.region_id)
        return self._mask_data

    def plot_mask(self, ax, color, alpha=0.2):
        mask = self.get_mask_data()
        # import numpy as np
        data = mask.data
        data[data == 0] = np.nan
        mask.data = data

        mask.plot(ax=ax)
        return ax

    def plot_borders(self, ax, color, lw=2):
        raise NotImplementedError("Coming soon...")

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
            raise ValueError("Invalid input for ax: need cartopy GeoAxes..")

        if self.mask_available():
            self.plot_mask(ax, color="r")

        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        name = self.name
        if not name == self.region_id:
            name += f" (ID={self.region_id})"

        ax.set_title(name)

        return ax

    def __contains__(self, val):
        if not isinstance(val, tuple):
            raise TypeError("Invalid input, need tuple")
        if not len(val) == 2:
            raise ValueError("Invalid input: coordinate must contain 2 elements (lat, lon)")
        return self.contains_coordinate(lat=val[0], lon=val[1])

    def __repr__(self):
        return f"Region {self.name} {super().__repr__()}"

    def __str__(self):
        s = (
            f"pyaeorocom Region\nName: {self.name}\n"
            f"Longitude range: {self.lon_range}\n"
            f"Latitude range: {self.lat_range}\n"
            f"Longitude range (plots): {self.lon_range_plot}\n"
            f"Latitude range (plots): {self.lat_range_plot}"
        )
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
        regs[reg] = Region(reg)
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
    """Get the region that contains an input coordinate

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
        regions = get_all_default_regions()
    ocean_mask = load_region_mask_xr("OCN")
    on_ocean = bool(get_mask_value(lat, lon, ocean_mask))
    for rname, reg in regions.items():
        if rname == ALL_REGION_NAME:  # always True for ALL_REGION_NAME
            matches.append(rname)
            continue
        # OCN needs special handling determined by the rname, not hardcoded to return OCN b/c of HTAP issues
        if rname in POSSIBLE_REGION_OCEAN_NAMES:
            if on_ocean:
                matches.append(rname)
            continue
        if reg.contains_coordinate(lat, lon) and not on_ocean:
            matches.append(rname)
    if len(matches) == 0:
        matches.append(ALL_REGION_NAME)
    return matches


def find_closest_region_coord(
    lat: float, lon: float, regions: dict | None = None, **kwargs
) -> list[str]:
    """Finds list of regions sorted by their center closest to input coordinate

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
    list[str]
        sorted list of region IDs of identified regions
    """
    if regions is None:
        regions = get_all_default_regions()
    matches = get_regions_coord(lat, lon, regions)
    matches.sort(key=lambda id: regions[id].distance_to_center(lat, lon))
    if kwargs.get("regions_how") == "htap":
        # keep only first entry and Oceans if it exists
        keep = matches[:1]
        if "Oceans" in matches[1:]:
            keep += ["Oceans"]
        if ALL_REGION_NAME in matches[1:]:
            keep += [ALL_REGION_NAME]
        return list(set(keep))
    return matches
