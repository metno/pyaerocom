"""
Module for geographical calculations

This module contains low-level methods to perform geographical calculations,
(e.g. distance between two coordinates)
"""

import logging
import os
from copy import deepcopy

import geonum
import numpy as np
from geocoder_reverse_natural_earth import Geocoder_Reverse_Exception, Geocoder_Reverse_NE

from pyaerocom import const
from pyaerocom.helpers import isnumeric

logger = logging.getLogger(__name__)


def calc_latlon_dists(latref, lonref, latlons):
    """
    Calculate distances of (lat, lon) coords to input lat, lon coordinate

    Parameters
    ----------
    latref : float
        latitude of reference coordinate
    lonref : float
        longitude of reference coordinate
    latlons : list
        list of (lat, lon) tuples for which distances to (latref, lonref) are
        computed

    Returns
    -------
    list
        list of computed geographic distances to input reference coordinate
        for all (lat, lon) coords in `latlons`

    """
    return [haversine(latref, lonref, c[0], c[1]) for c in latlons]


def find_coord_indices_within_distance(latref, lonref, latlons, radius=1):
    """
    Find indices of coordinates that match input coordinate

    Parameters
    ----------
    latref : float
        latitude of reference coordinate
    lonref : float
        longitude of reference coordinate
    latlons : list
        list of (lat, lon) tuples for which distances to (latref, lonref) are
        computed
    radius : float or int, optional
        Maximum allowed distance to input coordinate. The default is 1.

    Returns
    -------
    ndarray
        Indices of latlon coordinates in :param:`latlons` that are within
        the specified radius around (`latref`, `lonref`). The indices are
        sorted by distance to the input coordinate, starting with the
        closest

    """
    dists = np.asarray(calc_latlon_dists(latref, lonref, latlons))
    within_tol = np.where(dists < radius)[0]
    # the following statement sorts all indices in dists that are within
    # the tolerance radius, so the first entry in the returned aaray is the
    # index of the closest coordinate within the radius and the last is the
    # furthest
    return within_tol[np.argsort(dists[within_tol])]


def get_country_info_coords(coords):
    """
    Get country information for input lat/lon coordinates

    Parameters
    ----------
    coords : list or tuple
        list of coord tuples (lat, lon) or single coord tuple

    Raises
    ------
    ValueError
        if input format is incorrect

    Returns
    -------
    list
        list of dictionaries containing country information for each input
        coordinate
    """
    if isinstance(coords, np.ndarray):
        coords = list(coords)
    if not isinstance(coords, list | tuple):
        raise ValueError("Invalid input for coords, need list or tuple or array")

    geo = Geocoder_Reverse_NE()
    ret_list = []
    # that's what reverse_geocoder used to return
    # (more a list of this)
    ret_proto = {"city": "", "country_code": "", "code": ""}

    if len(coords) == 0:  # no coordinates
        pass
    elif isnumeric(coords[0]) and len(coords) == 2:  # only one coordinate
        lat, lon = coords
        try:
            dummy = geo.lookup(lat, lon)
        except Geocoder_Reverse_Exception:
            dummy = geo.lookup_nearest(lat, lon)
            if dummy is None:
                return [ret_proto]
        # return [rg.get(coords)]
        ret_dummy = deepcopy(ret_proto)
        ret_dummy["country"] = dummy["NAME"]
        ret_dummy["country_code"] = dummy["ISO_A2_EH"]
        return [ret_dummy]
    else:
        for coord in coords:
            ret_dummy = deepcopy(ret_proto)
            lat, lon = coord
            try:
                dummy = geo.lookup(lat, lon)
            except Geocoder_Reverse_Exception:
                dummy = geo.lookup_nearest(lat, lon)
            if dummy is not None:
                ret_dummy["country"] = dummy["NAME"]
                ret_dummy["country_code"] = dummy["ISO_A2_EH"]

            ret_list.append(ret_dummy)
    return ret_list
    # return rg.search(coords)


def get_topo_data(
    lat0, lon0, lat1=None, lon1=None, topo_dataset="srtm", topodata_loc=None, try_etopo1=False
):
    """Retrieve topographic altitude for a certain location

    Supports topography datasets supported by geonum.
    These are currently (20 Feb. 19) srtm (SRTM dataset, default, automatic access if online) and
    etopo1 (ETOPO1 dataset, lower resolution, must be available on local machine or server).

    Parameters
    ----------
    lat0 : float
            start longitude for data extraction
    lon0 : float
        start latitude for data extraction
    lat1 : float
        stop longitude for data extraction (default: None). If None only
        data around lon0, lat0 will be extracted.
    lon1 : float
        stop latitude for data extraction (default: None).
        If None only data around lon0, lat0 will be extracted
    topo_dataset : str
        name of topography dataset
    topodata_loc : str
        filepath or directory containing supported topographic datasets
    try_etopo1 : bool
        if True and if access fails via input arg `topo_dataset`, then try
        to access altitude using ETOPO1 dataset.

    Returns
    -------
    geonum.TopoData
        data object containing topography data in specified range

    Raises
    ------
    ValueError
        if altitude data cannot be accessed
    """
    if topodata_loc is None:
        if topo_dataset in const.SUPPLDIRS and os.path.exists(const.SUPPLDIRS[topo_dataset]):
            topodata_loc = const.SUPPLDIRS[topo_dataset]
            logger.info(f"Found default location for {topo_dataset} topodata at\n{topodata_loc}")

    try:
        access = geonum.TopoDataAccess(topo_dataset, local_path=topodata_loc)
        topodata = access.get_data(lat0, lon0, lat1, lon1)

        return topodata
    except Exception as e:
        if try_etopo1 and not topo_dataset == "etopo1":
            logger.warning(
                f"Failed to access topography data for {topo_dataset}. "
                f"Trying ETOPO1.\nError: {repr(e)}"
            )
            return get_topo_data(
                lat0,
                lon0,
                lat1,
                lon1,
                topo_dataset="etopo1",
                topodata_loc=topodata_loc,
                try_etopo1=False,
            )
        raise


def get_topo_altitude(lat, lon, topo_dataset="srtm", topodata_loc=None, try_etopo1=True):
    """Retrieve topographic altitude for a certain location

    Supports topography datasets supported by geonum.
    These are currently (20 Feb. 19) srtm (SRTM dataset, default, automatic access if online) and
    etopo1 (ETOPO1 dataset, lower resolution, must be available on local machine or server).

    Parameters
    ----------
    lat : float
        latitude of coordinate
    lon : float
        longitude of coordinate
    topo_dataset : str
        name of topography dataset
    topodata_loc : str
        filepath or directory containing supported topographic datasets
    try_etopo1 : bool
        if True and if access fails via input arg `topo_dataset`, then try
        to access altitude using ETOPO1 dataset.

    Returns
    -------
    dict
        dictionary containing input latitude, longitude, altitude and
        topographic dataset name used to retrieve the altitude.

    Raises
    ------
    ValueError
        if altitude data cannot be accessed
    """
    return get_topo_data(
        lat, lon, topo_dataset=topo_dataset, topodata_loc=topodata_loc, try_etopo1=try_etopo1
    )(lat, lon)


def calc_distance(lat0, lon0, lat1, lon1, alt0=None, alt1=None, auto_altitude_srtm=False):
    """Calculate distance between two coordinates

    Parameters
    ----------
    lat0 : float
        latitude of first point in decimal degrees
    lon0 : float
        longitude of first point in decimal degrees
    lat1 : float
        latitude of secondpoint in decimal degrees
    lon1 : float
        longitude of second point in decimal degrees
    alt0 : :obj:`float`, optional
        altitude of first point in m
    alt1 : :obj:`float`, optional
        altitude of second point in m
    auto_altitude_srtm : bool
        if True, then all altitudes that are unspecified are set to the
        corresponding topographic altitude of that coordinate, using SRTM
        (only works for coordinates where SRTM topographic data is accessible).

    Returns
    -------
    float
        distance between points in km
    """
    p0 = geonum.GeoPoint(lat0, lon0, alt0, auto_topo_access=auto_altitude_srtm)
    p1 = geonum.GeoPoint(lat1, lon1, alt1, auto_topo_access=auto_altitude_srtm)
    if auto_altitude_srtm and p0.altitude_err == p0._ALTERR_DEFAULT:
        raise ValueError(
            f"Failed to access topographic height for coord {p0} using SRTM topographic database"
        )
    if auto_altitude_srtm and p1.altitude_err == p1._ALTERR_DEFAULT:
        raise ValueError(
            f"Failed to access topographic height for coord {p1} using SRTM topographic database"
        )
    return (p0 - p1).magnitude


def is_within_radius_km(lat0, lon0, lat1, lon1, maxdist_km, alt0=0, alt1=0, **kwargs):
    """Checks if two lon/lat coordinates are within a certain distance to each other

    Parameters
    ----------
    lat0 : float
        latitude of first point in decimal degrees
    lon0 : float
        longitude of first point in decimal degrees
    lat1 : float
        latitude of second point in decimal degrees
    lon1 : float
        longitude of second point in decimal degrees
    maxdist_km : float
        maximum distance between two points in km
    alt0 : float
        altitude of first point in m
    alt1 : float
        altitude of second point in m

    Returns
    -------
    bool
        True, if coordinates are within specified distance to each other, else
        False

    """
    dist = calc_distance(lat0, lon0, lat1, lon1, alt0=alt0, alt1=alt1)
    if dist <= maxdist_km:
        return True
    return False


def haversine(lat0, lon0, lat1, lon1, earth_radius=6371.0):
    """Haversine formula

    Approximate horizontal distance between 2 points assuming a spherical
    earth using haversine formula.

    Note
    ----
    This code was copied from geonum library (date 12/11/2018, J. Gliss)

    Parameters
    ----------
    lat0 : float
        latitude of first point in decimal degrees
    lon0 : float
        longitude of first point in decimal degrees
    lat1 : float
        latitude of second point in decimal degrees
    lon1 : float
        longitude of second point in decimal degrees
    earth_radius : float
        average earth radius in km, defaults to 6371.0

    Returns
    --------
    float
        horizontal distance between input coordinates in km
    """
    hav = lambda d_theta: np.sin(d_theta / 2.0) ** 2  # noqa: E731

    d_lon = np.radians(lon1 - lon0)
    d_lat = np.radians(lat1 - lat0)
    lat0 = np.radians(lat0)
    lat1 = np.radians(lat1)

    a = hav(d_lat) + np.cos(lat0) * np.cos(lat1) * hav(d_lon)
    c = 2 * np.arcsin(np.sqrt(a))

    return earth_radius * c
