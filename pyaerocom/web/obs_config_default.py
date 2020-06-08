#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Config file for registered AeroCom observations datasets and variables

UNDER DEVELOPMENT -> CURRENTLY NOT USED
"""

OBS_SOURCES = {

'EBAS-Lev3'         :   dict(obs_id='EBASMC',
                             obs_vars=['ac550aer', 'sc550dryaer'],
                             vert_scheme='surface',
                             obs_vert_type='Surface'),

'AeronetSun'        :   dict(obs_id='AeronetSunV3Lev2.daily',
                             obs_vars=['ang4487aer', 'od550aer'],
                             obs_vert_type='Column'),

'AeronetSDA'        :   dict(obs_id='AeronetSDAV3Lev2.daily',
                             obs_vars=['od550lt1aer', 'od550gt1aer'],
                             obs_vert_type='Column'),

'AeronetInv'        :   dict(obs_id='AeronetInvV3Lev2.daily',
                             obs_vars=['abs550aer'],
                             obs_vert_type='Column'),
'MODIS6-terra'      :   dict(obs_id='MODIS6.terra',
                             obs_vars=['od550aer'],
                             regrid_res_deg=5,
                             obs_vert_type='Column',
                             ts_type='daily',
                             var_outlier_ranges=dict(od550aer=[0,10])),
'MODIS6-aqua'       :   dict(obs_id='MODIS6.aqua',
                             obs_vars=['od550aer'],
                             regrid_res_deg=5,
                             obs_vert_type='Column',
                             ts_type='daily',
                             var_outlier_ranges=dict(od550aer=[0,10])),
'AATSR4.3-SU'       :   dict(obs_id='AATSR_SU_v4.3',
                            obs_vars=['od550aer', 'ang4487aer', 'od550lt1aer',
                                      'od550gt1aer', 'abs550aer'],
                            regrid_res_deg=5,
                            ts_type='daily',
                            obs_vert_type='Column'),
'CALIOPv3'          :   dict(obs_id='CALIOP_V3.00_Cloudfree_day',
                             obs_vars=['od550aer'],
                             regrid_res_deg=5,
                             ts_type='monthly',
                             var_outlier_ranges=dict(od550aer=[0.001,10]),
                             obs_vert_type='Column')
}

OBS_DEFAULTS = {

        'Column'        :   {'od550aer'          :  'AeronetSun',
                             'ang4487aer'        :  'AeronetSun',
                             'od550lt1aer'       :  'AeronetSDA',
                             'od550gt1aer'       :  'AeronetSDA',
                             'abs550aer'         :  'AeronetInv'},

        'Surface'       :   {'ac550aer'        :  'EBAS-Lev3',
                             'sc550dryaer'    :  'EBAS-Lev3'},
}

def get_default_obsnetwork(var_name, vert_which=None):
    res = []
    for k, v in OBS_DEFAULTS.items():
        if vert_which is None:
            if var_name in v:
                res.append(v[var_name])
        elif vert_which ==  k and var_name in v:
            return v[var_name]
    num = len(res)
    if num == 0:
        raise ValueError('Could not find default obs network for variable {}'
                         .format(var_name))
    elif num > 1:
        raise ValueError('Found multiple default obs networks for variable {}'
                         'Please specify vertical type via vert_which input arg'
                         .format(var_name))
    return res[0]

def get_all_vars():
    all_vars =  []
    for cfg in OBS_SOURCES.values():
        all_vars.extend(cfg['obs_vars'])
    return list(dict.fromkeys(all_vars))

if __name__ == '__main__':

    print(get_all_vars())
    print(get_default_obsnetwork('ang4487aer'))
