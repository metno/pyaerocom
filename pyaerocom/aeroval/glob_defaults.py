#: Default variable ranges for web display
var_ranges_defaults = {
    "default": {"scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10], "colmap": "coolwarm"},
    "ang4487aer": {
        # "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2],
        "scale": [
            -0.2,
            -0.1,
            0.0,
            0.1,
            0.2,
            0.3,
            0.4,
            0.5,
            0.6,
            0.7,
            0.8,
            0.9,
            1.0,
            1.1,
            1.2,
            1.3,
            1.4,
            1.5,
            1.6,
            1.7,
            1.8,
            1.9,
            2.0,
        ],
        "colmap": "coolwarm",
    },
    "od550aer": {
        # "scale": [0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        "scale": [
            0.0,
            0.01,
            0.02,
            0.03,
            0.04,
            0.05,
            0.06,
            0.07,
            0.08,
            0.09,
            0.1,
            0.2,
            0.3,
            0.4,
            0.5,
            0.6,
            0.7,
            0.8,
            0.90,
            1.0,
            2.0,
        ],
        "colmap": "coolwarm",
    },
    "od550lt1aer": {
        # "scale": [0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        "scale": [
            0.0,
            0.01,
            0.02,
            0.03,
            0.04,
            0.05,
            0.06,
            0.07,
            0.08,
            0.09,
            0.1,
            0.2,
            0.3,
            0.4,
            0.5,
            0.6,
            0.7,
            0.8,
            0.90,
            1.0,
            2.0,
        ],
        "colmap": "coolwarm",
    },
    "od550gt1aer": {
        # "scale": [0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        "scale": [
            0.0,
            0.01,
            0.02,
            0.03,
            0.04,
            0.05,
            0.06,
            0.07,
            0.08,
            0.09,
            0.1,
            0.2,
            0.3,
            0.4,
            0.5,
            0.6,
            0.7,
            0.8,
            0.90,
            1.0,
            2.0,
        ],
        "colmap": "coolwarm",
    },
    "od550dust": {
        # "scale": [0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        "scale": [
            0.0,
            0.01,
            0.02,
            0.03,
            0.04,
            0.05,
            0.06,
            0.07,
            0.08,
            0.09,
            0.1,
            0.2,
            0.3,
            0.4,
            0.5,
            0.6,
            0.7,
            0.8,
            0.90,
            1.0,
            2.0,
        ],
        "colmap": "coolwarm",
    },
    "abs550aer": {
        "scale": [0, 0.0125, 0.025, 0.0375, 0.05, 0.0625, 0.075, 0.0875, 0.1],
        "colmap": "coolwarm",
    },
    "absc550aer": {"scale": [0, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100], "colmap": "coolwarm"},
    "scatc550dryaer": {
        "scale": [0, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100],
        "colmap": "coolwarm",
    },
    "extinction": {
        "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1],
        "colmap": "coolwarm",
    },
    "backscatter": {
        "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1],
        "colmap": "coolwarm",
    },
    "concso4": {
        "scale": [0, 0.75, 1.5, 2.25, 3.0, 3.75, 4.5, 5.25, 6.0, 6.75, 7.5, 8.25],
        "colmap": "coolwarm",
    },
    "concso2": {
        "scale": [0, 0.75, 1.5, 2.25, 3.0, 3.75, 4.5, 5.25, 6.0, 6.75, 7.5, 8.25],
        "colmap": "coolwarm",
    },
    "concpm10": {"scale": [0, 10, 20, 30, 40, 50, 60, 70, 80], "colmap": "coolwarm"},
    "concpm25": {"scale": [0, 5, 10, 15, 20, 25, 30, 35, 40, 45], "colmap": "coolwarm"},
    "conco3": {"scale": [0, 15, 30, 45, 60, 75, 90, 105, 120], "colmap": "coolwarm"},
    "vmro3": {"scale": [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70], "colmap": "coolwarm"},
    "concno2": {"scale": [0, 10, 20, 30, 40, 50, 60, 70, 80], "colmap": "coolwarm"},
    "vmrno2": {"scale": [0, 5, 10, 15, 20, 25, 30, 35, 40], "colmap": "coolwarm"},
    "vmro3max": {"scale": [0, 7.5, 15, 22.5, 30, 37.5, 45, 52.5, 60], "colmap": "coolwarm"},
    "concNhno3": {
        "scale": [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5],
        "colmap": "coolwarm",
    },
    "concNno3pm10": {
        "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1],
        "colmap": "coolwarm",
    },
    "concNno3pm25": {
        "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1],
        "colmap": "coolwarm",
    },
    "concNnh3": {
        "scale": [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
        "colmap": "coolwarm",
    },
    "concNnh4": {"scale": [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0], "colmap": "coolwarm"},
    "concNtno3": {
        "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0],
        "colmap": "coolwarm",
    },
    "concNtnh": {
        "scale": [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
        "colmap": "coolwarm",
    },
    "concsspm25": {"scale": [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0], "colmap": "coolwarm"},
    "concsspm10": {
        "scale": [0, 0.75, 1.5, 2.25, 3.0, 3.75, 4.5, 5.25, 6.0, 6.75, 7.5, 8.25],
        "colmap": "coolwarm",
    },
    "concCecpm25": {"scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10], "colmap": "coolwarm"},
    "concCocpm25": {
        "scale": [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
        "colmap": "coolwarm",
    },
    "wetoxs": {"scale": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5], "colmap": "coolwarm"},
    "wetoxn": {"scale": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5], "colmap": "coolwarm"},
    "wetrdn": {
        "scale": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5],
        "colmap": "coolwarm",
    },
    "prmm": {"scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10], "colmap": "coolwarm"},
    "dryoxs": {"scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10], "colmap": "coolwarm"},
    "dryoxn": {"scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10], "colmap": "coolwarm"},
    "dryrdn": {"scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10], "colmap": "coolwarm"},
    "depdust": {
        "scale": [0.0, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0],
        # "scale": [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
        "colmap": "coolwarm",
    },
    "drydust": {
        # "scale": [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
        "scale": [0.0, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0],
        "colmap": "coolwarm",
    },
    "wetdust": {
        # "scale": [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
        "scale": [0.0, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0],
        "colmap": "coolwarm",
    },
    "concdust": {
        "scale": [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
        "colmap": "coolwarm",
    },
    "vmrco": {
        "scale": [100.0, 125.0, 150.0, 175.0, 200.0, 225.0, 250.0, 275.0, 300.0],
        "colmap": "coolwarm",
    },
    "concco": {
        "scale": [100.0, 125.0, 150.0, 175.0, 200.0, 225.0, 250.0, 275.0, 300.0],
        "colmap": "coolwarm",
    },
    "ts": {"scale": [265, 270, 275, 280, 285, 290, 300, 305, 310, 315, 320], "colmap": "coolwarm"},
    "proxydryo3": {"scale": [0, 0.5, 1, 15, 20, 25, 0.30, 40, 50], "colmap": "coolwarm"},
    "proxydrypm10": {"scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2], "colmap": "coolwarm"},
    "proxydrypm25": {"scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2], "colmap": "coolwarm"},
    "proxydryno2": {
        "scale": [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4],
        "colmap": "coolwarm",
    },
    "proxydryhono": {"scale": [0.001, 0.002, 0.003, 0.004, 0.005, 0.006], "colmap": "coolwarm"},
    "proxydryn2o5": {"scale": [0.01, 0.02, 0.03, 0.04, 0.05], "colmap": "coolwarm"},
    "proxydryhno3": {
        "scale": [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4],
        "colmap": "coolwarm",
    },
    "proxydryno3c": {
        "scale": [0.01, 0.02, 0.03, 0.04, 0.05],
        "colmap": "coolwarm",
    },
    "proxydryno3f": {"scale": [0.01, 0.02, 0.03, 0.04, 0.05], "colmap": "coolwarm"},
    "proxydrynh3": {
        "scale": [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80],
        "colmap": "coolwarm",
    },
    "proxydrynh4": {
        "scale": [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4],
        "colmap": "coolwarm",
    },
    "proxydryso2": {
        "scale": [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4],
        "colmap": "coolwarm",
    },
    "proxydryso4": {
        "scale": [0.01, 0.02, 0.03, 0.04, 0.05],
        "colmap": "coolwarm",
    },
    "proxydryoxs": {
        "scale": [0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        "colmap": "coolwarm",
    },
    "proxydryoxn": {
        "scale": [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80],
        "colmap": "coolwarm",
    },
    "proxydryrdn": {
        "scale": [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80],
        "colmap": "coolwarm",
    },
    "depoxs": {"scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2], "colmap": "coolwarm"},
    "depoxn": {"scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2], "colmap": "coolwarm"},
    "deprdn": {"scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2], "colmap": "coolwarm"},
}

#: Default information for statistical parameters
statistics_defaults = {
    "nmb": {
        "name": "NMB",
        "longname": "Normalized Mean Bias",
        "scale": [-100, -75, -50, -25, 0, 25, 50, 75, 100],
        "colmap": "bwr",
        "unit": "%",
        "decimals": 1,
        "forecast": True,
    },
    "mnmb": {
        "name": "MNMB",
        "longname": "Modified Normalized Mean Bias",
        "scale": [-100, -75, -50, -25, 0, 25, 50, 75, 100],
        "colmap": "bwr",
        "unit": "%",
        "decimals": 1,
        "forecast": True,
    },
    "mb": {
        "name": "Mean Bias",
        "longname": "Mean Bias",
        "scale": [
            -0.15,
            -0.1,
            -0.05,
            0,
            0.05,
            0.1,
            0.15,
        ],  # factor to be multiplied by range of data
        "colmap": "bwr",
        "unit": "var",
        "decimals": 1,
    },
    "mab": {
        "name": "MAB",
        "longname": "Mean Absolute Bias",
        "scale": [
            0,
            0.025,
            0.05,
            0.075,
            0.1,
            0.125,
            0.15,
        ],  # factor to be multiplied by range of data
        "colmap": "bwr",
        "unit": "var",
        "decimals": 1,
    },
    "R": {
        "name": "R",
        "longname": "Correlation Coefficient",
        "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1],
        "colmap": "RdYlGn",
        "unit": "1",
        "decimals": 2,
        "forecast": True,
    },
    "R_spearman": {
        "name": "R Spearman",
        "longname": "R Spearman Correlation",
        "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1],
        "colmap": "RdYlGn",
        "unit": "1",
        "decimals": 2,
    },
    "fge": {
        "name": "FGE",
        "longname": "Fractional Gross Error",
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2],
        "colmap": "reverseColmap(RdYlGn)",
        "unit": "1",
        "decimals": 2,
        "forecast": True,
    },
    "nrms": {
        "name": "NRMSE",
        "longname": "Normalized Root Mean Square Error",
        "scale": [0, 25, 50, 75, 100, 125, 150, 175, 200],
        "colmap": "Reds",
        "unit": "%",
        "decimals": 1,
    },
    "rms": {
        "name": "RMSE",
        "longname": "Root Mean Square Error",
        "scale": None,
        "colmap": "coolwarm",
        "unit": "1",
        "decimals": 2,
        "forecast": True,
    },
    "data_mean": {
        "name": "Mean-Mod",
        "longname": "Model Mean",
        "scale": None,
        "colmap": "coolwarm",
        "unit": "1",
        "decimals": 2,
    },
    "refdata_mean": {
        "name": "Mean-Obs",
        "longname": "Observation Mean",
        "scale": None,
        "colmap": "coolwarm",
        "unit": "1",
        "decimals": 2,
    },
    "num_valid": {
        "name": "Nb. Obs",
        "longname": "Number of Valid Observations",
        "scale": None,
        "colmap": None,
        "overall_only": True,
        "unit": "1",
        "decimals": 0,
    },
    "num_coords_with_data": {
        "name": "Nb. Stations",
        "longname": "Number of Stations with data",
        "scale": None,
        "colmap": None,
        "overall_only": True,
        "unit": "1",
        "decimals": 0,
    },
}

# Default information for additional statistical parameters
extended_statistics = {
    "R_spatial_mean": {
        "name": "R-Space",
        "longname": "Spatial R computed from yearly averages",
        "overall_only": True,
        "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1],
        "colmap": "RdYlGn",
        "unit": "1",
        "decimals": 2,
        "time_series": False,
    },
    "R_temporal_median": {
        "name": "R-Temporal",
        "longname": "R temporal median",
        "overall_only": True,
        "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1],
        "colmap": "RdYlGn",
        "unit": "1",
        "decimals": 2,
        "time_series": False,
    },
}

#: Default information about trend display
statistics_trend = {
    "obs/mod_trend": {
        "name": "Obs/Mod-Trends",
        "longname": "Trends",
        "scale": [-10.0, -7.5, -5.0, -2.5, 0, 2.5, 5.0, 7.5, 10.0],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1,
    },
    "obs_trend": {
        "name": "Obs-Trends",
        "longname": "Observed Trends",
        "scale": [-10.0, -7.5, -5.0, -2.5, 0, 2.5, 5.0, 7.5, 10.0],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1,
    },
    "mod_trend": {
        "name": "Mod-Trends",
        "longname": "Modelled Trends",
        "scale": [-10, -7.5, -5.0, -2.5, 0, 2.5, 5.0, 7.5, 10.0],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1,
    },
}
# If doing an obs_only experiement, the only statistics which make sense relate just to the observations
statistics_obs_only = {
    "refdata_mean": {
        "name": "Mean-Obs",
        "longname": "Model Mean",
        "scale": None,
        "colmap": "coolwarm",
        "unit": "1",
        "decimals": 2,
    },
}

# For experiments where only model data is interesting, as with proxy drydep
statistics_model_only = {
    "data_mean": {
        "name": "Mean-Mod",
        "longname": "Observation Mean",
        "scale": None,
        "colmap": "coolwarm",
        "unit": "1",
        "decimals": 2,
    },
}

#: Mapping of pyaerocom variable names to web naming conventions
## Note: A 2D variable is defined under Column on the website, 3D is defined under Surface
var_web_info = dict(
    od550aer=["AOD", "2D", "Optical properties"],
    od550csaer=["AOD (clear sky)", "2D", "Optical properties"],
    od550lt1aer=["AODf", "2D", "Optical properties"],
    od550gt1aer=["AODc", "2D", "Optical properties"],
    od550dust=["AODdust", "2D", "Optical properties"],
    abs550aer=["AAOD", "2D", "Optical properties"],
    ang4487aer=["AE", "2D", "Optical properties"],
    angabs4487aer=["AAE", "2D", "Optical properties"],
    ang4487csaer=["AE (clear sky)", "2D", "Optical properties"],
    sc550dryaer=["Scat. coef. (dry)", "3D", "Optical properties"],
    sc550aer=["Scat. coef.", "3D", "Optical properties"],
    ac550aer=["Abs. coef.", "3D", "Optical properties"],
    ac550dryaer=["Abs. coef. (dry)", "3D", "Optical properties"],
    ec532aer=["Ext. coeff.", "3D", "Optical properties"],
    bsc532aer=["Backscat. coeff.", "3D", "Optical properties"],
    concso4pr=["SO4 (precip.)", "3D", "Particle concentrations"],
    concbc=["BC", "3D", "Particle concentrations"],
    concoa=["OA", "3D", "Particle concentrations"],
    concss=["SS", "3D", "Particle concentrations"],
    conco3=["O3", "3D", "Gas concentrations"],
    concno310=["NO3_PM10", "3D", "Particle concentration"],
    concno325=["NO3_PM25", "3D", "Particle concentration"],
    proxyod550bc=["OD (Black Carbon)", "2D", "Optical properties"],
    proxyod550dust=["OD (Dust)", "2D", "Optical properties"],
    proxyod550oa=["OD (Organic Matter)", "2D", "Optical properties"],
    proxyod550so4=["OD (SO4)", "2D", "Optical properties"],
    proxyod550ss=["OD (Sea Salt)", "2D", "Optical properties"],
    proxyod550nh4=["OD (NH4)", "2D", "Optical properties"],
    proxyod550no3=["OD (NO3)", "2D", "Optical properties"],
    # Gases
    concNno=["NO", "3D", "Concentration"],
    concno2=["NO2", "3D", "Gas concentrations"],
    concNno2=["NO2", "3D", "Gas concentrations"],
    vmrno=["NO", "3D", "Volume mixing ratios"],
    vmrno2=["NO2", "3D", "Volume mixing ratios"],
    concno3=["NO3", "3D", "Gas concentrations"],
    conctno3=["tNO3", "3D", "Concentration"],
    concNtno3=["tNO3", "3D", "Concentration"],
    conchno3=["HNO3", "3D", "Concentration"],
    concNhno3=["HNO3", "3D", "Concentration"],
    concnh3=["NH3", "3D", "Concentration"],
    concNnh3=["NH3", "3D", "Concentration"],
    conctnh=["tNH", "3D", "Concentration"],
    concNtnh=["tNH", "3D", "Concentration"],
    concnh4=["NH4", "3D", "Gas concentrations"],
    concNnh4=["NH4", "3D", "Gas concentrations"],
    concso2=["SO2", "3D", "Gas concentrations"],
    concSso2=["SO2", "3D", "Gas concentrations"],
    vmrso2=["SO2", "3D", "Gas volume mixing ratio"],
    concso4=["SO4", "3D", "Particle concentrations"],
    vmro3=["O3", "3D", "Volume mixing ratios"],
    vmro3max=["O3Max", "3D", "Volume mixing ratios"],
    vmrox=["OX", "3D", "Gas volume mixing ratio"],
    concco=["CO", "3D", "Particle concentration"],
    vmrco=["CO", "3D", "Volume mixing ratios"],
    vmrc2h2=["Ethyne", "3D", "Volume mixing ratios"],
    vmrc2h4=["Ethylene", "3D", "Volume mixing ratios"],
    vmrc2h6=["Ethane", "3D", "Volume mixing ratios"],
    vmrhcho=["Formaldehyde", "3D", "Volume mixing ratios"],
    vmrisop=["Isoprene", "3D", "Volume mixing ratios"],
    # PMs
    concpm10=["PM10", "3D", "Particle concentrations"],
    concpm25=["PM2.5", "3D", "Particle concentrations"],
    concNno3pm10=["NO3 PM10", "3D", "Particle concentration"],
    concNno3pm25=["NO3 PM25", "3D", "Particle concentration"],
    concno3pm10=["NO3 PM10", "3D", "Particle concentration"],
    concno3pm25=["NO3 PM25", "3D", "Particle concentration"],
    concnh4coarse=["NH4 PM10", "3D", "Particle concentrations"],
    concnh4fine=["NH4 PM2.5", "3D", "Particle concentrations"],
    concso4t=["SO4 total", "3D", "Particle concentration"],
    concso4c=["SO4 sea salt corrected", "3D", "Particle concentration"],
    concso4coarse=["SO4 PM10", "3D", "Particle concentration"],
    concso4fine=["SO4 PM2.5", "3D", "Particle concentration"],
    concss10=["SS PM10", "3D", "Particle concentration"],
    concss25=["SS PM25", "3D", "Particle concentration"],
    concec=["EC", "3D", "Particle concentration"],
    conccoc=["OC", "3D", "Particle concentration"],
    concsspm10=["SS PM10", "3D", "Particle concentration"],
    concsspm25=["SS PM25", "3D", "Particle concentration"],
    concCecpm25=["EC PM2.5", "3D", "Particle concentration"],
    concCocpm25=["OC PM2.5", "3D", "Particle concentration"],
    concCecpm10=["EC PM10", "3D", "Particle concentration"],
    concCocpm10=["OC PM10", "3D", "Particle concentration"],
    concCoc25=["OC PM2.5", "3D", "Particle concentration"],
    # Depositions
    drysox=["DryOXS", "3D", "Deposition"],
    dryoxs=["proxyDryOXS", "3D", "Deposition"],
    dryoxn=["proxyDryOXN", "3D", "Deposition"],
    dryrdn=["proxyDryRDN", "3D", "Deposition"],
    depoxs=["TotDepOXS", "3D", "Total Deposition"],
    depoxn=["TotDepOXN", "3D", "Total Deposition"],
    deprdn=["TotDepRDN", "3D", "Total Deposition"],
    wetoxs=["WetOXS", "3D", "Deposition"],
    wetoxsc=["WetOXScorr", "3D", "Deposition"],
    wetoxst=["WetOXStot", "3D", "Deposition"],
    wetoxn=["WetOXN", "3D", "Deposition"],
    wetrdn=["WetRDN", "3D", "Deposition"],
    prmm=["Precipitation", "3D", "Deposition"],
    # Temperature
    ts=["Surface Temperature", "3D", "Temperature"],
    # proxy drydep
    proxydryoxs=["proxyDryOXS", "3D", "Deposition"],
    proxydryso2=["proxyDrySO2", "3D", "Deposition"],
    proxydryso4=["proxyDrySO4", "3D", "Deposition"],
    proxydryoxn=["proxyDryOXN", "3D", "Deposition"],
    proxydryno2=["proxyDryNO2", "3D", "Deposition"],
    proxydryno2no2=["proxyDryNO2NO2", "3D", "Deposition"],
    proxydryhono=["proxyDryHONO", "3D", "Deposition"],
    proxydryn2o5=["proxyDryN2O5", "3D", "Deposition"],
    proxydryhno3=["proxyDryHNO3", "3D", "Deposition"],
    proxydryno3c=["proxyDryNO3Coarse", "3D", "Deposition"],
    proxydryno3f=["proxyDryNO3Fine", "3D", "Deposition"],
    proxydryrdn=["proxyDryRDN", "3D", "Deposition"],
    proxydrynh3=["proxyDryNH3", "3D", "Deposition"],
    proxydrynh4=["proxyDryNH4", "3D", "Deposition"],
    proxydryo3=["proxyDryO3", "3D", "Deposition"],
    proxydrypm10=["proxyDryPM10", "3D", "Deposition"],
    proxydrypm25=["proxyDryPM2.5", "3D", "Deposition"],
)
