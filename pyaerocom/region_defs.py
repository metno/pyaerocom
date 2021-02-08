#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Definitions of rectangular regions used in pyaerocom

Created: 8 Feb 2021
Author: J. Gliss

NOTE: replaces former regions.ini in pyaerocom/data dir
"""
_AEROCOM_DEFS = {
    'WORLD': {'lat_range': [-90, 90], 'lon_range': [-180, 180], 'lon_range_plot': [-180, 180], 'lon_ticks': [-180.0, -135.0, -90.0, -45.0, 0.0, 45, 90, 135, 180], 'lat_ticks': [-90.0, -60, -30, 0.0, 30, 60, 90]},
    'ASIA': {'lat_range': [0, 72], 'lon_range': [50, 150], 'lon_range_plot': [50, 150]},
    'AUSTRALIA': {'lat_range': [-50, -10], 'lon_range': [110, 155], 'lon_range_plot': [90, 180]},
    'CHINA': {'lat_range': [20, 50], 'lon_range': [90, 130], 'lon_range_plot': [90, 140]},
    'EUROPE': {'lat_range': [40, 72], 'lon_range': [-10, 40], 'lon_range_plot': [-10, 40], 'lon_ticks': [-20, -10, 0, 10, 20, 30, 40, 50, 60, 70], 'lat_ticks': [30, 40, 50, 60, 70, 80]},
    'INDIA': {'lat_range': [5, 35], 'lon_range': [65, 90], 'lon_range_plot': [50, 100]},
    'NAFRICA': {'lat_range': [0, 40], 'lon_range': [-17, 50], 'lon_range_plot': [-17, 50]},
    'SAFRICA': {'lat_range': [-35, 0], 'lon_range': [10, 40], 'lon_range_plot': [10, 40]},
    'SAMERICA': {'lat_range': [-60, 20], 'lon_range': [-105, -30], 'lon_range_plot': [-105, -30]},
    'NAMERICA': {'lat_range': [20, 80], 'lon_range': [-150, -45], 'lon_range_plot': [-150, -45]}
    }

_HTAP_DEFS = {
    'PAN': {'lat_range': [-54.75, 11.55], 'lon_range': [-23.05, 109.55], 'lon_range_plot': [-23.05, 109.55]},
    'EAS': {'lat_range': [18.25, 53.55], 'lon_range': [-107.05, -36.45], 'lon_range_plot': [-107.05, -36.45]},
    'NAF': {'lat_range': [19.05, 37.25], 'lon_range': [-74.45, -38.05], 'lon_range_plot': [-74.45, -38.05]},
    'MDE': {'lat_range': [12.15, 39.65], 'lon_range': [-79.25, -24.25], 'lon_range_plot': [-79.25, -24.25]},
    'LAND': {'lat_range': [-59.45, 71.15], 'lon_range': [-142.35, 118.85], 'lon_range_plot': [-142.35, 118.85]},
    'SAS': {'lat_range': [-9.75, 37.05], 'lon_range': [-74.05, 19.55], 'lon_range_plot': [-74.05, 19.55]},
    'SPO': {'lat_range': [-89.95, -60.05], 'lon_range': [120.05, 179.95], 'lon_range_plot': [120.05, 179.95]},
    'OCN': {'lat_range': [-59.95, 66.25], 'lon_range': [-132.55, 119.95], 'lon_range_plot': [-132.55, 119.95]},
    'SEA': {'lat_range': [-11.65, 28.45], 'lon_range': [-56.85, 23.35], 'lon_range_plot': [-56.85, 23.35]},
    'RBU': {'lat_range': [29.45, 66.25], 'lon_range': [-132.45, -58.85], 'lon_range_plot': [-132.45, -58.85]},
    'EEUROPE': {'lat_range': [34.65, 59.55], 'lon_range': [-119.05, -69.25], 'lon_range_plot': [-119.05, -69.25]},
    'NAM': {'lat_range': [18.95, 71.15], 'lon_range': [-142.35, -37.95], 'lon_range_plot': [-142.35, -37.95]},
    'WEUROPE': {'lat_range': [27.75, 66.45], 'lon_range': [-132.95, -55.55], 'lon_range_plot': [-132.95, -55.55]},
    'SAF': {'lat_range': [-54.45, 27.25], 'lon_range': [-54.55, 108.95], 'lon_range_plot': [-54.55, 108.95]},
    'USA': {'lat_range': [18.95, 49.35], 'lon_range': [-98.75, -37.95], 'lon_range_plot': [-98.75, -37.95]},
    'SAM': {'lat_range': [-59.45, 5.15], 'lon_range': [-10.35, 118.85], 'lon_range_plot': [-10.35, 118.85]},
    'EUR': {'lat_range': [27.75, 66.45], 'lon_range': [-132.95, -55.55], 'lon_range_plot': [-132.95, -55.55]},
    'NPO': {'lat_range': [59.85, 89.95], 'lon_range': [-179.95, -119.75], 'lon_range_plot': [-179.95, -119.75]},
    'MCA': {'lat_range': [-4.15, 32.65], 'lon_range': [-65.35, 8.25], 'lon_range_plot': [-65.35, 8.25]}
    }

_OTHER_REG_DEFS = {'NHEMISPHERE': {'lat_range': [0, 90], 'lon_range': [-180, 180], 'lon_range_plot': [-180, 180]},
                   'SHEMISPHERE': {'lat_range': [-90, 0], 'lon_range': [-180, 180], 'lon_range_plot': [-180, 180]}}


REGION_DEFS = {
    **_AEROCOM_DEFS,
    **_HTAP_DEFS,
    **_OTHER_REG_DEFS
    }

# optional: alternative names for regions (e.g. used for plotting)
# if undefined the corresponding ID is used as name. Names are adapetd from
# https://publications.jrc.ec.europa.eu/repository/bitstream/JRC102552/lbna28255enn.pdf
# (Fig. 3, P11)
_HTAP_NAMES = {
    'NAM' : 'N America',
    'EUR' : 'Europe',
    'EEUROPE' : 'E Europe',
    'RBU' : 'Rus,Bel,Ukr',
    'MDE' : 'Middle East',
    'EAS' : 'E Asia',
    'SAS' : 'S Asia',
    'SEA' : 'SE Asia',
    'NAF' : 'N Africa',
    'MCA' : 'C America',
    'SAF' : 'S Africa',
    'SAM' : 'S America',
    'PAN' : 'Pacific,Aust,NZ',
    'OCN' : 'Oceans'
    }


REGION_NAMES = {
    **_HTAP_NAMES
    }

OLD_AEROCOM_REGIONS = list(_AEROCOM_DEFS)
HTAP_REGIONS = list(_HTAP_NAMES)
OTHER_REGIONS = list(_OTHER_REG_DEFS)

for key in REGION_NAMES:
    assert key in REGION_DEFS, key
print('BLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa')





