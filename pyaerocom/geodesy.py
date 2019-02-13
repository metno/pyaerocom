#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for geographical calculations 

This module contains low-level methods to perform geographical calculations, 
(e.g. distance between two coordinates)
"""
from pyaerocom import GEONUM_AVAILABLE
from pyaerocom import print_log
import numpy as np

def calc_distance(lat0, lon0, lat1, lon1, alt0=None, alt1=None,
                  auto_altitude_srtm=False):
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
        (requires geonum to be available and works only for coordinates where
        SRTM topographic data is accessible).
        
    Returns
    -------
    float
        distance between points in km
    """
    if not GEONUM_AVAILABLE and auto_altitude_srtm:
        raise ModuleNotFoundError('Require Geonum library for accessing '
                                  'topographic altitude using SRTM database')
    if GEONUM_AVAILABLE:
        import geonum
        p0 = geonum.GeoPoint(lat0, lon0, alt0, 
                             auto_topo_access=auto_altitude_srtm)
        p1 = geonum.GeoPoint(lat1, lon1, alt1, 
                             auto_topo_access=auto_altitude_srtm)
        if auto_altitude_srtm:
            if p0.altitude_err == p0._ALTERR_DEFAULT:
                raise ValueError('Failed to access topographic height for coord '
                                 '{} using SRTM topographic database'.format(p0))
            elif p1.altitude_err == p1._ALTERR_DEFAULT:
                raise ValueError('Failed to access topographic height for coord '
                                 '{} using SRTM topographic database'.format(p1))
        return (p0 - p1).magnitude
    else:
        print_log.warn('geonum is not installed, computing approximate '
                       'distance using haversine formula')
        hordist = haversine(lat0, lon0, lat1, lon1)
        if alt0 == None:
            alt0 = 0
        if alt1 == None:
            alt1 = 0 
        return np.linalg.norm((hordist, (alt0 - alt1)/1000))
        
    
def is_within_radius_km(lat0, lon0, lat1, lon1, maxdist_km, alt0=0, alt1=0, 
                        **kwargs):
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
    hav = lambda d_theta: np.sin(d_theta / 2.0) ** 2
    
    d_lon = np.radians(lon1 - lon0)
    d_lat = np.radians(lat1 - lat0)
    lat0 = np.radians(lat0)
    lat1 = np.radians(lat1)
 
    a = hav(d_lat) + np.cos(lat0) * np.cos(lat1) * hav(d_lon)
    c = 2 * np.arcsin(np.sqrt(a))
 
    return earth_radius * c
