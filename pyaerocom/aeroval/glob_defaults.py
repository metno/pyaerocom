#: Default variable ranges for web display
import copy
import json
import logging
from configparser import ConfigParser
from enum import Enum
import os
from typing import NamedTuple

from pydantic import BaseModel

from pyaerocom.data import resources

logger = logging.getLogger(__name__)


# basemodel-implementation for verification
class _ScaleAndColmap(NamedTuple):
    scale: list[float]
    colmap: str


class _VarWebScaleAndColormap(BaseModel):
    scale_colmaps: dict[str, _ScaleAndColmap]


# dict-implementation for json-serialization, namedtuple not stable with json/simplejson
class ScaleAndColmap(dict[str, str | list[float]]):
    """simple dictionary container with only two keys, scale and colmap"""

    pass


class VarWebScaleAndColormap(dict[str, ScaleAndColmap]):
    def __init__(self, config_file: str = "", **kwargs):
        """This class contains scale and colmap information and is implemented as dict to allow
        json serialization. It reads it initial data from data/var_scale_colmap.ini. kwargs will be send to update.

        :param config_file: filename to additional or updated information, defaults to None
        """
        super().__init__()
        with resources.path("pyaerocom.aeroval.data", "var_scale_colmap.ini") as file:
            self.update_from_ini(file)
        if config_file != "":
            logger.info(f"Reading additional web-scales from '{config_file}'")
            if not os.path.exists(config_file):
                raise FileNotFoundError(
                    f"VarWebScaleAndColormap initialized with config_file: '{config_file}' which does not exist"
                )
            self.update_from_ini(config_file)
        self.update(**kwargs)

    def update(self, **kwargs):
        """update/add scale and colormaps by kwargs, e.g.
        update(concso2={"scale"=[0.2,1], "colormap"="bluewhite"})
        """
        wvsc = _VarWebScaleAndColormap(scale_colmaps=kwargs)
        super().update(**{x: y._asdict() for x, y in wvsc.scale_colmaps.items()})

    def update_from_ini(self, filename):
        cfg = ConfigParser()
        if not os.path.exists(filename):
            raise FileNotFoundError(
                f"VarWebScaleAndColormap update_from_ini('{filename}') which does not exist"
            )
        cfg.read(filename)
        # remove configparser default
        cfg_dict = dict()
        keys = ("scale", "colmap")
        for s in cfg.sections():
            items = []
            for k in keys:
                if k in cfg[s]:
                    if k == "scale":
                        try:
                            items.append(json.loads(cfg[s][k]))
                        except Exception as ex:
                            raise KeyError(
                                f"wrong value for '{k}' of var '{s}' in {filename}: {ex}"
                            )
                    else:
                        items.append(cfg[s][k])
                else:
                    raise KeyError(f"missing '{k}' for var '{s}' in {filename}")
            cfg_dict[s] = tuple(items)
        self.update(**cfg_dict)

    def write(self, filename: str):
        """write the scales and colormaps to a configuration file

        :param filename: path to a filename, currently a .ini file
        """
        cfg = ConfigParser()
        cfg.update(self)
        with open(filename, "w") as fh:
            cfg.write(fh)


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
    vertical_column_density = "Vertical column density"
    surface_emission = "Surface emission"
    column_burden = "Column burden"
    solar_irradiance = "Solar irradiance"
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

    def __init__(self, config_file="", **kwargs):
        """This class contains var_web_info and can be accessed like a read-only dict. It
        reads it initial data from data/var_web_info.ini

        :param config_file: filename to additional or updated VariableInfo items, defaults to None
        """
        self._var_web_info = _VarWebInfo(var_web_info=dict())
        with resources.path("pyaerocom.aeroval.data", "var_web_info.ini") as file:
            self.update_from_ini(file)
        if config_file != "":
            self.update_from_ini(config_file)
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
        keys = ("menu_name", "vertical_type", "category")
        for s in cfg.sections():
            items = []
            for k in keys:
                if k in cfg[s]:
                    items.append(cfg[s][k])
                else:
                    raise KeyError(f"missing '{k}' for var '{s}' in {filename}")
            cfg_dict[s] = tuple(items)
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
        "time_series": True,
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
        "time_series": True,
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
        "time_series": True,
    },
    "refdata_mean": {
        "name": "Mean-Obs",
        "longname": "Observation Mean",
        "scale": None,
        "colmap": "coolwarm",
        "unit": "1",
        "decimals": 2,
        "time_series": True,
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
        "category": "Regional Time Series",
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
        "category": "Regional Time Series",
        "time_series": False,
    },
}

# For adding num statistics
num_statistics = {
    "num_valid": {
        "name": "Nb. Obs",
        "longname": "Number of Valid Observations",
        "scale": None,
        "colmap": None,
        "unit": "1",
        "decimals": 0,
        "overall_only": True,
        "category": "Regional Time Series",
        "time_series": True,
    },
    "num_coords_with_data": {
        "name": "Nb. Stations",
        "longname": "Number of Stations with data",
        "scale": None,
        "colmap": None,
        "unit": "1",
        "decimals": 0,
        "overall_only": True,
        "category": "Regional Time Series",
        "time_series": True,
    },
}

#: Default information about trend display
statistics_trend = {
    "obs/mod_trend": {
        "name": "Obs/Mod-Trends",
        "longname": "Trends",
        "scale": [-5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1,
        "category": "Regional Time Series",
        "forecast": False,
    },
    "obs_trend": {
        "name": "Obs-Trends",
        "longname": "Observed Trends",
        "scale": [-5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1,
        "category": "Regional Time Series",
        "forecast": False,
    },
    "mod_trend": {
        "name": "Mod-Trends",
        "longname": "Modelled Trends",
        "scale": [-5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1,
        "category": "Regional Time Series",
        "forecast": False,
    },
}

statistics_mean_trend = {
    "obs/mod_mean_trend": {
        "name": "Mean Obs/Mod-Trends",
        "longname": "Mean Trends",
        "scale": [-5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1,
        "category": "Individual Stations",
        "time_series": False,
    },
    "obs_mean_trend": {
        "name": "Mean Obs-Trends",
        "longname": "Observed Mean Trends",
        "scale": [-5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1,
        "category": "Individual Stations",
        "time_series": False,
    },
    "mod_mean_trend": {
        "name": "Mean Mod-Trends",
        "longname": "Modelled Mean Trends",
        "scale": [-5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1,
        "category": "Individual Stations",
        "time_series": False,
    },
}

statistics_median_trend = {
    "obs/mod_median_trend": {
        "name": "Median Obs/Mod-Trends",
        "longname": "Median Trends",
        "scale": [-5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1,
        "category": "Individual Stations",
        "time_series": False,
    },
    "obs_median_trend": {
        "name": "Median Obs-Trends",
        "longname": "Observed Median Trends",
        "scale": [-5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1,
        "category": "Individual Stations",
        "time_series": False,
    },
    "mod_median_trend": {
        "name": "Median Mod-Trends",
        "longname": "Modelled Median Trends",
        "scale": [-5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0],
        "colmap": "bwr",
        "unit": "%/yr",
        "decimals": 1,
        "category": "Individual Stations",
        "time_series": False,
    },
}
# If doing an obs_only experiment, the only statistics which make sense relate just to the observations
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
