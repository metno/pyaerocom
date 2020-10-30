#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 09:31:56 2019

@author: jonasg
"""

VAR_MAPPING = {

    'od550aer'      : ['AOD', '2D', 'Optical properties'],
    'od550csaer'    : ['AOD (clear sky)', '2D', 'Optical properties'],
    'od550lt1aer'   : ['AOD<1um', '2D', 'Optical properties'],
    'od550gt1aer'   : ['AOD>1um', '2D', 'Optical properties'],
    'abs550aer'     : ['AAOD', '2D', 'Optical properties'],
    'ang4487aer'    : ['AE', '2D', 'Optical properties'],
    'angabs4487aer' : ['AAE', '2D', 'Optical properties'],
    'ang4487csaer'  : ['AE (clear sky)', '2D', 'Optical properties'],
    'sc550dryaer'   : ['Scat. coef. (dry)', '3D', 'Optical properties'],
    'sc550aer'      : ['Scat. coef.', '3D', 'Optical properties'],
    'ac550aer'      : ['Abs. coef.', '3D', 'Optical properties'],
    'ac550dryaer'   : ['Abs. coef. (dry)', '3D', 'Optical properties'],
    'ec532aer'      : ['Ext. coeff.', '3D', 'Optical properties'],
    'bsc532aer'     : ['Backscat. coeff.', '3D', 'Optical properties'],
    'concpm10'      : ['PM10', '3D', 'Particle concentrations'],
    'concpm25'      : ['PM2.5', '3D', 'Particle concentrations'],
    'concso4'       : ['SO4', '3D', 'Particle concentrations'],
    'concso4pr'     : ['SO4 (precip.)', '3D', 'Particle concentrations'],
    'concbc'        : ['BC', '3D', 'Particle concentrations'],
    'concoa'        : ['OA', '3D', 'Particle concentrations'],
    'concss'        : ['SS', '3D', 'Particle concentrations'],
    'conco3'        : ['O3', '3D', 'Gas concentrations'],
    'concso2'       : ['SO2', '3D', 'Gas concentrations'],
}
