#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 09:31:56 2019

@author: jonasg
"""

VAR_MAPPING = {

    'od550aer'      : ['AOD', '2D', 'Optical properties'],
    'od550csaer'    : ['AOD (clear sky)', '2D', 'Optical properties'],
    'od550lt1aer'   : ['AODf', '2D', 'Optical properties'],
    'od550gt1aer'   : ['AODc', '2D', 'Optical properties'],
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
    'vmrox'         : ['OX', '3D', 'Gas volume mixing ratio'],
    'vmrso2'        : ['SO2', '3D', 'Gas volume mixing ratio'],
    'conctno3'      : ['tNO3', '3D', 'Concentration'],
    'conctnh'       : ['tNH', '3D', 'Concentration'],
    'concnh3'       : ['NH3', '3D', 'Concentration'],
    'conchno3'      : ['HNO3', '3D', 'Concentration'],
    'concno310'     : ['NO3_PM10', '3D', 'Particle concentration'],
    'concno325'     : ['NO3_PM25', '3D', 'Particle concentration'],
    'concss10'      : ['SS_PM10', '3D', 'Particle concentration'],
    'concss25'      : ['SS_PM25', '3D', 'Particle concentration'],
    'concec'        : ['EC', '3D', 'Particle concentration'],
    'conccoc'       : ['OC', '3D', 'Particle concentration'],
    'wetoxs'        : ['WetOXS', '3D', 'Deposition'],
    'drysox'        : ['DryOXS', '3D', 'Deposition'],
    'concnh4'       : ['NH4', '3D', 'Gas concentrations'],
    'concno3'       : ['NO3', '3D', 'Gas concentrations'],
    'vmro3'         : ['O3', '3D', 'Volume mixing ratios'],
    'vmrno2'        : ['NO2', '3D', 'Volume mixing ratios'],
}


