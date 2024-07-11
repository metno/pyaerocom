#: Default variable ranges for web display
import copy
import json
from configparser import ConfigParser
from enum import Enum
from typing import NamedTuple

from pydantic import BaseModel

from pyaerocom.data import resources


# basemodel-implementation for verification
class _ScaleAndColmap(NamedTuple):
    scale: list[float]
    colmap: str


class _WebVariableScalesAndColormaps(BaseModel):
    scale_colmaps: dict[str, _ScaleAndColmap]


# dict-implementation for json-serialization, namedtuple not stable with json/simplejson
class ScaleAndColmap(dict[str, str | list[float]]):
    """simple dictionary container with only two keys, scale and colmap

    :param dict: initialization dictionary
    """

    pass


class WebVariableScalesAndColormaps(dict[str, ScaleAndColmap]):
    def __init__(self, *args, **kwargs):
        # run arguments through pydantic
        wvsc = _WebVariableScalesAndColormaps(scale_colmaps=kwargs)
        super().__init__(**{x: y._asdict() for x, y in wvsc.scale_colmaps.items()})

    def __init__(self, extra_config=None, /, **kwargs):
        """This class contains scale and colmap informations and is implemented as dict to allow
        json serialization. It reads it inital data from data/var_scale_colmap.ini.

        :param extra_config: filename to additional or updated information, defaults to None
        """
        super().__init__()
        with resources.path("pyaerocom.aeroval.data", "var_scale_colmap.ini") as file:
            self.update_from_ini(file)
        if extra_config is not None:
            self.update_from_ini(extra_config)
        self.update(**kwargs)

    def update(self, **kwargs):
        wvsc = _WebVariableScalesAndColormaps(scale_colmaps=kwargs)
        super().update(**{x: y._asdict() for x, y in wvsc.scale_colmaps.items()})

    def update_from_ini(self, filename):
        cfg = ConfigParser()
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


var_ranges_defaults = WebVariableScalesAndColormaps()
# WebVariableScalesAndColormaps(**_var_ranges_defaults)


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
        with resources.path("pyaerocom.aeroval.data", "var_web_info.ini") as file:
            self.update_from_ini(file)
        if ini_file is not None:
            self.update_from_ini(ini_file)
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


var_web_info = VarWebInfo()
