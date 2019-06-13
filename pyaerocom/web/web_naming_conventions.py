#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 09:31:56 2019

@author: jonasg
"""

VAR_MAPPING = {'od550aer'       : ['AOD', '2D'],
               'od550lt1aer'    : ['AOD<1um', '2D'],
               'od550gt1aer'    : ['AOD>1um', '2D'],
               'abs550aer'      : ['AAOD', '2D'],
               'ang4487aer'     : ['AE', '2D'],
               'scatc550dryaer' : ['Scat. coef. (dry)', '3D'],
               'scatc550aer'    : ['Scat. coef.', '3D'],
               'absc550aer'     : ['Abs. coef.', '3D'],
               'sconcpm10'      : ['PM10', '3D'],
               'sconcpm25'      : ['PM2.5', '3D'],
               'sconco3'        : ['O3', '3D'],
               'sconcso4'       : ['SO4 (Aerosol)', '3D'],
               'sconcso4pr'     : ['SO4 (precip.)', '3D'],
               'sconcso2'       : ['SO2', '3D'],
               'ec532aer'       : ['Ext. coeff.', '3D'],
               'bscatc532aer'   : ['Backscat. coeff.', '3D']}