#: Default variable ranges for web display
import copy
import os
from configparser import ConfigParser
from enum import Enum
from typing import NamedTuple

from pydantic import BaseModel

var_ranges_defaults = {
    "default": {"scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10], "colmap": "coolwarm"},
    "ang4487aer": {
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2],
        "colmap": "coolwarm",
    },
    "od550aer": {
        "scale": [0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        "colmap": "coolwarm",
    },
    "od550lt1aer": {
        "scale": [0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        "colmap": "coolwarm",
    },
    "od550gt1aer": {
        "scale": [0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
        "colmap": "coolwarm",
    },
    "ratpm25pm10": {
        "scale": [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        "colmap": "coolwarm",
    },
    "ratpm10pm25": {
        "scale": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
        "colmap": "coolwarm",
    },
    "od550dust": {
        "scale": [0, 0.0125, 0.025, 0.0375, 0.05, 0.0625, 0.075, 0.0875, 0.1],
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
    "ssa670aer": {
        "scale": [0.75, 0.775, 0.8, 0.825, 0.85, 0.875, 0.9, 0.925, 0.95, 0.975, 1],
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
    "vmrno": {
        "scale": [0, 0.75, 1.5, 2.25, 3.0, 3.75, 4.5, 5.25, 6.0, 6.75, 7.5, 8.25],
        "colmap": "coolwarm",
    },
    "vmrso2": {
        "scale": [0, 0.75, 1.5, 2.25, 3.0, 3.75, 4.5, 5.25, 6.0, 6.75, 7.5, 8.25],
        "colmap": "coolwarm",
    },
    "concpm10": {"scale": [0, 10, 20, 30, 40, 50, 60, 70, 80], "colmap": "coolwarm"},
    "concpm25": {"scale": [0, 5, 10, 15, 20, 25, 30, 35, 40, 45], "colmap": "coolwarm"},
    "conco3": {"scale": [0, 15, 30, 45, 60, 75, 90, 105, 120], "colmap": "coolwarm"},
    "vmro3": {"scale": [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70], "colmap": "coolwarm"},
    "vmrox": {"scale": [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70], "colmap": "coolwarm"},
    "concno2": {"scale": [0, 10, 20, 30, 40, 50, 60, 70, 80], "colmap": "coolwarm"},
    "concNno2": {"scale": [0, 0.3, 0.5, 1, 1.3, 1.5, 2, 3, 5], "colmap": "coolwarm"},
    "vmrno2": {"scale": [0, 5, 10, 15, 20, 25, 30, 35, 40], "colmap": "coolwarm"},
    "vmro3max": {"scale": [0, 7.5, 15, 22.5, 30, 37.5, 45, 52.5, 60], "colmap": "coolwarm"},
    "vmro3mda8": {"scale": [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70], "colmap": "coolwarm"},
    "concNhno3": {
        "scale": [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 1],
        "colmap": "coolwarm",
    },
    "concNno3pm10": {
        "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1, 1.5, 2, 5, 10],
        "colmap": "coolwarm",
    },
    "concNno3pm25": {
        "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1, 1.5, 2, 5, 10],
        "colmap": "coolwarm",
    },
    "concNnh3": {
        "scale": [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 7.5, 10.0, 20],
        "colmap": "coolwarm",
    },
    "concNnh4": {
        "scale": [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0],
        "colmap": "coolwarm",
    },
    "concNtno3": {
        "scale": [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0, 1.5, 2, 5],
        "colmap": "coolwarm",
    },
    "concNtnh": {
        "scale": [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 7.5, 10.0, 20, 50],
        "colmap": "coolwarm",
    },
    "concsspm25": {
        "scale": [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 5, 10],
        "colmap": "coolwarm",
    },
    "concsspm10": {
        "scale": [0, 0.75, 1.5, 2.25, 3.0, 3.75, 4.5, 5.25, 6.0, 6.75, 7.5, 8.25, 10, 15, 20, 50],
        "colmap": "coolwarm",
    },
    "concCecpm25": {"scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10], "colmap": "coolwarm"},
    "concCec25": {"scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10], "colmap": "coolwarm"},
    "concCocpm25": {
        "scale": [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 10],
        "colmap": "coolwarm",
    },
    "concCoc25": {
        "scale": [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 10],
        "colmap": "coolwarm",
    },
    "concom25": {
        "scale": [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
        "colmap": "coolwarm",
    },
    "wetoxs": {"scale": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 5], "colmap": "coolwarm"},
    "wetna": {
        "scale": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 5, 10, 20, 50, 100],
        "colmap": "coolwarm",
    },
    "wetoxn": {"scale": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 5], "colmap": "coolwarm"},
    "wetrdn": {
        "scale": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 5, 10],
        "colmap": "coolwarm",
    },
    "wetoxsf": {"scale": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 5], "colmap": "coolwarm"},
    "wetoxnf": {"scale": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 5], "colmap": "coolwarm"},
    "wetrdnf": {
        "scale": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 5, 10],
        "colmap": "coolwarm",
    },
    "prmm": {"scale": [0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10], "colmap": "coolwarm"},
    "dryoxs": {
        "scale": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 5],
        "colmap": "coolwarm",
    },
    "dryoxn": {"scale": [0, 0.1, 0.2, 0.5, 1, 2.0, 5, 10, 20, 50], "colmap": "coolwarm"},
    "dryrdn": {"scale": [0, 0.1, 0.2, 0.5, 1, 2.0, 5, 10, 20, 50], "colmap": "coolwarm"},
    "depdust": {
        "scale": [0.01, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0],
        "colmap": "coolwarm",
    },
    "drydust": {
        # "scale": [0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0],
        "scale": [0.0, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0, 500.0, 1000.0],
        "colmap": "coolwarm",
    },
    "wetdust": {
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
    "vmrco2": {
        "scale": [400.0, 405.0, 410.0, 415.0, 420.0, 425.0, 430.0, 435.0, 440.0, 445.0, 450.0],
        "colmap": "coolwarm",
    },
    "vmrch4": {
        "scale": [
            1700,
            1750,
            1800,
            1850,
            1900,
            1950,
            2000,
            2050,
            2100,
            2150,
            2200,
        ],
        "colmap": "coolwarm",
    },
    "concco": {
        "scale": [100.0, 125.0, 150.0, 175.0, 200.0, 225.0, 250.0, 275.0, 300.0],
        "colmap": "coolwarm",
    },
    "ts": {"scale": [265, 270, 275, 280, 285, 290, 300, 305, 310, 315, 320], "colmap": "coolwarm"},
    "proxyzdust": {
        "scale": [0.0, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 7.5, 10.0],
        "colmap": "coolwarm",
    },
    "zdust": {
        "scale": [0.0, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 7.5, 10.0],
        "colmap": "coolwarm",
    },
    "proxyzaerosol": {
        "scale": [0.0, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 7.5, 10.0],
        "colmap": "coolwarm",
    },
    "zaerosol": {
        "scale": [0.0, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 7.5, 10.0],
        "colmap": "coolwarm",
    },
    "proxydryo3": {"scale": [0, 0.5, 1, 5, 10, 15, 20, 25, 30, 40, 50], "colmap": "coolwarm"},
    "dryo3": {"scale": [0, 0.5, 1, 5, 10, 15, 20, 25, 30, 40, 50], "colmap": "coolwarm"},
    "proxydrypm10": {"scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2], "colmap": "coolwarm"},
    "drypm10": {
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 5, 10, 20, 50, 100],
        "colmap": "coolwarm",
    },
    "proxydrypm25": {
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 5, 10, 20, 50, 100],
        "colmap": "coolwarm",
    },
    "drypm25": {"scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 5, 10], "colmap": "coolwarm"},
    "proxydryss": {"scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2], "colmap": "coolwarm"},
    "dryss": {"scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2], "colmap": "coolwarm"},
    "proxydryna": {
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 5, 10, 20, 50, 100, 200],
        "colmap": "coolwarm",
    },
    "dryna": {
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 5, 10, 20, 50, 100, 200],
        "colmap": "coolwarm",
    },
    "proxydryno2": {
        "scale": [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 1.0, 2],
        "colmap": "coolwarm",
    },
    "dryno2": {
        "scale": [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 1.0, 2],
        "colmap": "coolwarm",
    },
    "proxydryhono": {
        "scale": [0.0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.008, 0.01, 0.02],
        "colmap": "coolwarm",
    },
    "dryhono": {
        "scale": [0.0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.008, 0.01, 0.02],
        "colmap": "coolwarm",
    },
    "proxydryn2o5": {
        "scale": [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.1, 0.2],
        "colmap": "coolwarm",
    },
    "dryn2o5": {
        "scale": [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.1, 0.2],
        "colmap": "coolwarm",
    },
    "proxydryhno3": {
        "scale": [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 1.0, 2.0, 5.0],
        "colmap": "coolwarm",
    },
    "dryhno3": {
        "scale": [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 1.0, 2.0, 5.0],
        "colmap": "coolwarm",
    },
    "proxydryno3c": {
        "scale": [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.5],
        "colmap": "coolwarm",
    },
    "dryno3c": {
        "scale": [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.5],
        "colmap": "coolwarm",
    },
    "proxydryno3f": {
        "scale": [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.5],
        "colmap": "coolwarm",
    },
    "dryno3f": {"scale": [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.5], "colmap": "coolwarm"},
    "proxydrynh3": {
        "scale": [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 1, 2, 5],
        "colmap": "coolwarm",
    },
    "drynh3": {
        "scale": [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 1, 2, 5],
        "colmap": "coolwarm",
    },
    "proxydrynh4": {
        "scale": [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 1.0],
        "colmap": "coolwarm",
    },
    "drynh4": {
        "scale": [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 1.0],
        "colmap": "coolwarm",
    },
    "proxydryso2": {
        "scale": [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 1.0, 2, 5],
        "colmap": "coolwarm",
    },
    "dryso2": {
        "scale": [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 1.0, 2, 5],
        "colmap": "coolwarm",
    },
    "proxydryso4": {
        "scale": [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.5],
        "colmap": "coolwarm",
    },
    "dryso4": {
        "scale": [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.5],
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
    "depoxs": {
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 5, 10, 20],
        "colmap": "coolwarm",
    },
    "depna": {
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 5, 10, 20, 50, 100, 200],
        "colmap": "coolwarm",
    },
    "depoxn": {
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 5, 10, 20],
        "colmap": "coolwarm",
    },
    "deprdn": {
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 5, 10, 20, 50, 100, 200],
        "colmap": "coolwarm",
    },
    "depoxsf": {
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 5, 10, 20],
        "colmap": "coolwarm",
    },
    "depnaf": {
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 5, 10, 20],
        "colmap": "coolwarm",
    },
    "depoxnf": {
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 5, 10, 20],
        "colmap": "coolwarm",
    },
    "deprdnf": {
        "scale": [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 5, 10, 20, 50, 100, 200],
        "colmap": "coolwarm",
    },
    "bsc532aer": {
        "scale": [0.0, 0.0005, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.0035, 0.004],
        "colmap": "coolwarm",
    },
    "ec532aer": {
        "scale": [0, 0.004, 0.008, 0.012, 0.016, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.4],
        "colmap": "coolwarm",
    },
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
        "name": "MB",
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
        "longname": "Observation Mean",
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
        "longname": "Model Mean",
        "scale": None,
        "colmap": "coolwarm",
        "unit": "1",
        "decimals": 2,
    },
}

#: Mapping of pyaerocom variable names to web naming conventions


class VerticalType(str, Enum):
    """A 2D variable is defined under Column on the website, 3D is defined under Surface"""

    T2D = "2D"
    T3D = "3D"
    UNDEFINED = "UNDEFINED"

    def __str__(self):
        return self.value


class CategoryType(str, Enum):
    optical = "Optical properties"
    particle_conc = "Particle concentrations"
    height = "Height"
    concentration = "Concentration"
    gas_conc = "Gas concentrations"
    vmr = "Volume mixing ratios"
    gas_vmr = "Gas volume mixing ratio"
    deposition = "Deposition"
    temperature = "Temperature"
    particle_ratio = "Particle ratio"
    UNDEFINED = "UNDEFINED"

    def __str__(self):
        return self.value


class VariableInfo(NamedTuple):
    menu_name: str
    vertical_type: VerticalType
    category: CategoryType


class _VarWebInfo(BaseModel):
    """Pydantic helper class to ensure the VarWebInfo container always contains the correct data

    :param BaseModel: _description_
    """

    var_web_info: dict[str, VariableInfo]


class VarWebInfo:
    _var_web_info: _VarWebInfo

    def __init__(self, ini_file=None, /, **kwargs):
        """This class contains var_web_info and can be accessed like a read-only dict. It
        reads it inital data from data/var_web_info.ini

        :param ini_file: filename to additional or updated VariableInfo items, defaults to None
        """
        self._var_web_info = _VarWebInfo(var_web_info=dict())
        file = os.path.join(os.path.dirname(__file__), "data", "var_web_info.ini")
        self.update_from_ini(file)
        if ini_file is not None:
            self.update_from_ini(file)
        self.update(**kwargs)

    def update(self, *args, **kwargs):
        d = copy.deepcopy(self._var_web_info.var_web_info)
        d.update(*args, **kwargs)
        self._var_web_info = _VarWebInfo(var_web_info=d)

    def update_from_ini(self, filename):
        cfg = ConfigParser()
        cfg.read(filename)
        # remove configparser default
        cfg_dict = dict()
        for s in cfg.sections():
            cfg_dict[s] = tuple([cfg[s][x] for x in "menu_name,vertical_type,category".split(",")])
        self.update(**cfg_dict)

    ## below functions to behave like a read-only dict
    def copy(self):
        return self._var_web_info.var_web_info.copy()

    def __getitem__(self, key):
        return self._var_web_info.var_web_info[key]

    def __len__(self, key):
        return self._var_web_info.var_web_info.__len__()

    def __repr__(self):
        return repr(self._var_web_info.var_web_info)

    def keys(self):
        return self._var_web_info.var_web_info.keys()

    def has_key(self, k):
        return k in self._var_web_info.var_web_info

    def values(self):
        return self._var_web_info.var_web_info.values()

    def items(self):
        return self._var_web_info.var_web_info.items()

    def __cmp__(self, dict_):
        return self._var_web_info.var_web_info.__cmp__(dict_)

    def __contains__(self, item):
        return self._var_web_info.var_web_info.__contains__(item)

    def __iter__(self):
        return self._var_web_info.var_web_info.__iter__()

    def __unicode__(self):
        return self._var_web_info.var_web_info.__unicode__()


var_web_info = VarWebInfo()
