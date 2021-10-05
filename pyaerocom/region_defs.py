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
    'PAN': {'lat_range': [-54.74999999999966, 11.550000000000823], 'lon_range': [112, -134]},
    'EAS': {'lat_range': [18.25000000000084, 53.55000000000134], 'lon_range': [73.64999999999412, 145.74999999999002]},
    'NAF': {'lat_range': [19.05000000000085, 37.25000000000111], 'lon_range': [-17.050000000005937, 35.74999999999427]},
    'MDE': {'lat_range': [12.150000000000821, 39.65000000000114], 'lon_range': [34.24999999999425, 63.249999999994664]},
    'LAND': {'lat_range': [-59.449999999999726, 71.15000000000109], 'lon_range': [-180, 180]},
    'SAS': {'lat_range': [-9.749999999999135, 37.050000000001106], 'lon_range': [46.349999999994424, 97.34999999999278]},
    'SPO': {'lat_range': [-89.94999999999831, -60.049999999999734], 'lon_range': [-179.95000000000002, 179.94999999998808]},
    'OCN': {'lat_range': [-59.94999999999973, 66.25000000000136], 'lon_range': [-180, 180]},
    'SEA': {'lat_range': [-11.649999999999128, 28.450000000000983], 'lon_range': [92.24999999999307, 155.94999999998944]},
    'RBU': {'lat_range': [29.450000000000998, 66.25000000000136], 'lon_range': [22, -170]},
    'EEUROPE': {'lat_range': [34.65000000000107, 59.550000000001425], 'lon_range': [12.14999999999401, 44.7499999999944]},
    'NAM': {'lat_range': [18.95000000000085, 71.15000000000109], 'lon_range': [172, -52]},
    'WEUROPE': {'lat_range': [27.750000000000973, 66.45000000000135], 'lon_range': [-31.25000000000614, 31.449999999994215]},
    'SAF': {'lat_range': [-54.449999999999655, 27.250000000000966], 'lon_range': [-25.350000000006055, 77.5499999999939]},
    'USA': {'lat_range': [18.95000000000085, 49.35000000000128], 'lon_range': [-159.75000000000117, -56.250000000006494]},
    'SAM': {'lat_range': [-59.449999999999726, 5.150000000000846], 'lon_range': [-109.35000000000403, -26.250000000006068]},
    'EUR': {'lat_range': [27.750000000000973, 66.45000000000135], 'lon_range': [-31.25000000000614, 44.7499999999944]},
    'NPO': {'lat_range': [59.85000000000143, 89.95000000000002], 'lon_range': [-179.95000000000002, 179.94999999998808]},
    'MCA': {'lat_range': [-4.149999999999155, 32.65000000000104], 'lon_range': [-118.35000000000352, -51.65000000000643]}
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
HTAP_REGIONS_DEFAULT = list(_HTAP_NAMES)
HTAP_REGIONS = list(_HTAP_DEFS)
OTHER_REGIONS = list(_OTHER_REG_DEFS)

if __name__ == '__main__':
    import pyaerocom as pya
    import matplotlib.pyplot as plt
    plt.close('all')
    for key in REGION_NAMES:
        assert key in REGION_DEFS, key

    plot = ['NAM', 'PAN', 'RBU']

    for rn in plot:
        pya.Region(rn).plot()




