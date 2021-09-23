#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NOTE: parts of this should be migrated into variables.ini if possible
Created on Thu Jun 13 09:31:56 2019

@author: jonasg
"""
var_ranges_defaults = {
    # "default": {
    #     "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
    #     "colmap": "coolwarm"
    # },
    "ang4487aer": {
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2],
        "colmap": "coolwarm"
    },
    "od550aer": {
        "scale": [0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        "colmap": "coolwarm"
    },
    "od550lt1aer": {
        "scale": [0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        "colmap": "coolwarm"
    },
    "od550gt1aer": {
        "scale": [0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        "colmap": "coolwarm"
    },
    "abs550aer": {
        "scale": [0, 0.0125, 0.025, 0.0375, 0.05, 0.0625, 0.075, 0.0875, 0.1],
        "colmap": "coolwarm"
    },
    "absc550aer": {
        "scale": [0, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100],
        "colmap": "coolwarm"
    },
    "scatc550dryaer": {
        "scale": [0, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100],
        "colmap": "coolwarm"
    },
    "extinction": {
        "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1],
        "colmap": "coolwarm"
    },
    "backscatter": {
        "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1],
        "colmap": "coolwarm"
    },
    "concso4": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "concso2": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "concpm10": {
        "scale": [0, 10, 20, 30, 40, 50, 60, 70, 80],
        "colmap": "coolwarm"
    },
    "concpm25": {
        "scale": [0, 10, 20, 30, 40, 50, 60, 70, 80],
        "colmap": "coolwarm"
    },
    "conco3": {
        "scale": [0, 15, 30, 45, 60, 75, 90, 105, 120],
        "colmap": "coolwarm"
    },
    "vmro3": {
        "scale": [0, 7.5, 15, 22.5, 30, 37.5, 45, 52.5, 60],
        "colmap": "coolwarm"
    },
    "concno2": {
        "scale": [0, 10, 20, 30, 40, 50, 60, 70, 80],
        "colmap": "coolwarm"
    },
    "vmrno2": {
        "scale": [0, 5, 10, 15, 20, 25, 30, 35, 40],
        "colmap": "coolwarm"
    },
    "concNhno3": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "concNno3pm10": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "concNno3pm25": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "concNnh3": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "concNnh4": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "concNtno3": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "concNtnh": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "concsspm25": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "concsspm10": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "concCecpm25": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "concCocpm25": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "wetoxs": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "wetoxn": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "wetrdn": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "dryoxs": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "dryoxn": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
    "dryrdn": {
        "scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10],
        "colmap": "coolwarm"
    },
}


statistics_defaults = {
  "nmb": {
    "name": "NMB",
    "longname": "Normalized Mean Bias",
    "scale": [-100, -75, -50, -25, 0, 25, 50, 75, 100],
    "colmap": "bwr",
    "unit": "%",
    "decimals": 1
  },
  "mnmb": {
    "name": "MNMB",
    "longname": "Modified Normalized Mean Bias",
    "scale": [-100, -75, -50, -25, 0, 25, 50, 75, 100],
    "colmap": "bwr",
    "unit": "%",
    "decimals": 1
  },
  "R": {
    "name": "R",
    "longname": "Correlation Coefficient",
    "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1],
    "colmap": "RdYlGn",
    "unit": "1",
    "decimals": 2
  },
  "R_spearman": {
    "name": "R Spearman",
    "longname": "R Spearman Correlation",
    "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1],
    "colmap": "RdYlGn",
    "unit": "1",
    "decimals": 2
  },
  "fge": {
    "name": "FGE",
    "longname": "Fractional Gross Error",
    "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2],
    "colmap": "reverseColmap(RdYlGn)",
    "unit": "1",
    "decimals": 2
    },
  "nrms": {
    "name": "NRMSE",
    "longname": "Normalized Root Mean Square Error",
    "scale": [0, 25, 50, 75, 100, 125, 150, 175, 200],
    "colmap": "Reds",
    "unit": "%",
    "decimals": 1
  },
  "rms": {
    "name": "RMSE",
    "longname": "Root Mean Square Error",
    "scale": None,
    "colmap": "coolwarm",
    "unit": "1",
    "decimals": 2
  },
  "data_mean": {
    "name": "Mean-Mod",
    "longname": "Model Mean",
    "scale": None,
    "colmap": "coolwarm",
    "unit": "1",
    "decimals": 2
  },
  "refdata_mean": {
    "name": "Mean-Obs",
    "longname": "Observation Mean",
    "scale": None,
    "colmap": "coolwarm",
    "unit": "1",
    "decimals": 2
  },
  

}

statistics_trend = {
    "obs/mod_trend": {
        "name": "Obs/Mod-Trends",
        "longname": "Trends",
        "scale": [
            -10.0,
            -7.5,
            -5.0,
            -2.5,
            0,
            2.5,
            5.0,
            7.5,
            10.0
        ],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1
    },
    "obs_trend": {
        "name": "Obs-Trends",
        "longname": "Observed Trends",
        "scale": [
            -10.0,
            -7.5,
            -5.0,
            -2.5,
            0,
            2.5,
            5.0,
            7.5,
            10.0
        ],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1
    },
    "mod_trend": {
        "name": "Mod-Trends",
        "longname": "Modelled Trends",
        "scale": [
            -10,
            -7.5,
            -5.0,
            -2.5,
            0,
            2.5,
            5.0,
            7.5,
            10.0
        ],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1
    },
}


var_web_info = {

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


