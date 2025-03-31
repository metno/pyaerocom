import logging
import warnings
from ast import literal_eval
from configparser import ConfigParser

import numpy as np

from pyaerocom import var_groups
from pyaerocom._lowlevel_helpers import dict_to_str, list_to_shortstr
from pyaerocom.exceptions import VariableDefinitionError
from pyaerocom.mathutils import make_binlist
from pyaerocom.obs_io import OBS_WAVELENGTH_TOL_NM

#: helper vor checking if variable name contains str 3d or 3D
from pyaerocom.variable_helpers import (
    _check_alias_family,
    _read_alias_ini,
    get_aliases,
    parse_aliases_ini,
    parse_variables_ini,
)
from pyaerocom.varnameinfo import VarNameInfo

logger = logging.getLogger(__name__)


def literal_eval_list(val: str):
    return list(literal_eval(val))


def str2list(val: str) -> list[str]:
    return [x.strip() for x in val.split(",")]


def str2bool(val: str) -> bool:
    return val.lower() in {"true", "1", "t", "yes"}


class Variable:
    """Interface that specifies default settings for a variable

    See `variables.ini <https://github.com/metno/pyaerocom/blob/master/
    pyaerocom/data/variables.ini>`__ file for an overview of currently available
    default variables.

    Parameters
    ----------
    var_name : str
        string ID of variable (see file variables.ini for valid IDs)
    init : bool
        if True, input variable name is attempted to be read from config file
    cfg : ConfigParser
        open config parser that holds the information in config file available
        (i.e. :func:`ConfigParser.read` has been called with config file as
        input)
    **kwargs
        any valid class attribute (e.g. map_vmin, map_vmax, ...)

    Attributes
    ----------
    var_name : str
        input variable name
    var_name_aerocom : str
        AEROCOM variable name (see e.g. `AEROCOM protocol
        <http://aerocom.met.no/protocol_table.html>`__ for a list of
        available variables)
    is_3d : bool
        flag that indicates if variable is 3D
    is_dry : bool
        flag that is set based on filename that indicates if variable data
        corresponds to dry conditions.
    units : str
        unit of variable (None if no unit)
    default_vert_code : str, optional
        default vertical code to be loaded (i.e. Column, ModelLevel, Surface).
        Only relevant during reading and in case conflicts occur (e.g.
        abs550aer, 2010, Column and Surface files)
    aliases : list
        list of alternative names for this variable
    minimum : float
        lower limit of allowed value range
    upper_limit : float
        upper limit of allowed value range
    obs_wavelength_tol_nm : float    literal_eval_list = lambda val: list(literal_eval(val))

        wavelength tolerance (+/-) for reading of obsdata. Default is 10, i.e.
        if this variable is defined at 550 nm and obsdata contains measured
        values of this quantity within interval of 540 - 560, then these data
        is used
    scat_xlim : float
        x-range for scatter plot
    scat_ylim : float
        y-range for scatter plot
    scat_loglog : bool
        scatter plot on loglog scale
    scat_scale_factor : float
        scale factor for scatter plot
    map_cmap : str
        name of default colormap (matplotlib) of this variable.
    map_vmin : float
        data value corresponding to lower end of colormap in map plots of this
        quantity
    map_vmax : float
        data value corresponding to upper end of colormap in map plots of this
        quantity
    map_c_under : str
        color used for values below :attr:`map_vmin` in map plots of this
        quantity
    map_c_over : str
        color used for values exceeding :attr:`map_vmax` in map plots of this
        quantity
    map_cbar_levels : :obj:`list`, optional
        levels of colorbar
    map_cbar_ticks : :obj:`list`, optional
        colorbar ticks
    """

    _TYPE_CONV = {
        "wavelength_nm": float,
        "minimum": float,
        "maximum": float,
        "dimensions": str2list,
        "obs_wavelength_tol_nm": float,
        "scat_xlim": literal_eval_list,
        "scat_ylim": literal_eval_list,
        "scat_loglog": str2bool,
        "scat_scale_factor": float,
        "dry_rh_max": float,
        "map_cmap": str,
        "map_vmin": float,
        "map_vmax": float,
        "map_cbar_levels": literal_eval_list,
        "map_cbar_ticks": literal_eval_list,
        "_is_rate": bool,
    }

    # maybe used in config
    ALT_NAMES = {"unit": "units"}

    plot_info_keys = [
        "scat_xlim",
        "scat_ylim",
        "scat_loglog",
        "scat_scale_factor",
        "map_vmin",
        "map_vmax",
        "map_cmap",
        "map_c_under",
        "map_c_over",
        "map_cbar_levels",
        "map_cbar_ticks",
    ]
    VMIN_DEFAULT = -np.inf
    VMAX_DEFAULT = np.inf

    @staticmethod
    def _check_input_var_name(var_name):
        if "3d" in var_name:
            var_name = var_name.replace("3d", "")
        elif "3D" in var_name:
            var_name = var_name.replace("3D", "")
        elif "_" in var_name:
            raise ValueError(f"invalid variable name {var_name}. Must not contain underscore")
        return var_name

    def __init__(self, var_name=None, init=True, cfg=None, **kwargs):
        if var_name is None:
            var_name = "od550aer"
        elif not isinstance(var_name, str):
            raise ValueError(
                f"Invalid input for variable name, need str type, got {type(var_name)}"
            )
        # save orig. input for whatever reason
        self._var_name_input = var_name

        self.var_name = self._check_input_var_name(var_name)
        self._var_name_aerocom = None

        self.standard_name = None
        # Assume variables that have no unit specified in variables.ini are
        # unitless.
        self.units = "1"
        self.default_vert_code = None

        self.wavelength_nm = None
        self.dry_rh_max = 40
        self.dimensions = None
        self.minimum = self.VMIN_DEFAULT
        self.maximum = self.VMAX_DEFAULT

        self.description = None
        self.comments_and_purpose = None

        # wavelength tolerance in nm
        self.obs_wavelength_tol_nm = None

        self.scat_xlim = None
        self.scat_ylim = None
        self.scat_loglog = None
        self.scat_scale_factor = 1.0

        # settings for map plotting
        self.map_cmap = "coolwarm"
        self.map_vmin = None
        self.map_vmax = None
        self.map_c_under = None
        self.map_c_over = "r"
        self.map_cbar_levels = None
        self.map_cbar_ticks = None

        self._is_rate = False

        # imports default information and, on top, variable information (if
        # applicable)
        if init:
            self.parse_from_ini(self.var_name, cfg=cfg)

        self.update(**kwargs)
        if self.obs_wavelength_tol_nm is None:
            self.obs_wavelength_tol_nm = OBS_WAVELENGTH_TOL_NM

    @property
    def var_name_aerocom(self):
        """AeroCom variable name of the input variable"""
        vna = self._var_name_aerocom
        return self.var_name if vna is None else vna

    @property
    def var_name_input(self):
        """Input variable"""
        return self._var_name_input

    @property
    def is_3d(self):
        """True if str '3d' is contained in :attr:`var_name_input`"""
        return True if "3d" in self.var_name_input.lower() else False

    @property
    def is_wavelength_dependent(self):
        """Indicates whether this variable is wavelength dependent"""
        return True if self.wavelength_nm is not None else False

    @property
    def is_at_dry_conditions(self):
        """Indicate whether variable denotes dry conditions"""
        var_name = self.var_name_aerocom
        if var_name.startswith("dry"):  # dry deposition
            return False
        return True if "dry" in var_name else False

    @property
    def is_deposition(self):
        """
        Indicates whether input variables is a deposition rate

        Note
        ----
        This function only identifies wet and dry deposition based on the variable
        names, there might be other variables that are deposition variables but
        cannot be identified by this function.

        Parameters
        ----------
        var_name : str
            Name of variable to be checked

        Returns
        -------
        bool
            If True, then variable name denotes a deposition variables

        """
        var_name = self.var_name_aerocom
        if var_name.startswith(var_groups.drydep_startswith):
            return True
        elif var_name.startswith(var_groups.wetdep_startswith):
            return True
        elif var_name.startswith(var_groups.totdep_startswith):
            return True
        elif var_name in var_groups.dep_add_vars:
            return True
        return False

    @property
    def is_emission(self):
        """
        Indicates whether input variables is an emission rate

        Note
        ----
        This function only identifies wet and dry deposition based on the variable
        names, there might be other variables that are deposition variables but
        cannot be identified by this function.

        Parameters
        ----------
        var_name : str
            Name of variable to be checked

        Returns
        -------
        bool
            If True, then variable name denotes a deposition variables

        """
        var_name = self.var_name_aerocom
        if var_name.startswith(var_groups.emi_startswith):
            return True
        elif var_name in var_groups.emi_add_vars:
            return True
        return False

    @property
    def is_rate(self):
        """Indicates whether variable name is a rate

        Rates include e.g. deposition or emission rate variables but also
        precipitation

        Returns
        -------
        bool
            True if variable is rate, else False
        """
        if self.is_emission:
            return True
        elif self.is_deposition:
            return True
        elif self._is_rate:
            return True
        return False

    @property
    def is_alias(self):
        return True if self.var_name != self.var_name_aerocom else False

    @property
    def unit(self):
        """Unit of variable (old name, deprecated)"""
        warnings.warn(
            "Attr. name unit in Variable class is deprecated. Please use units instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.units

    @property
    def plot_info(self):
        """Dictionary containing plot information"""
        d = {}
        for k in self.plot_info_keys:
            d[k] = self[k]
        return d

    def update(self, **kwargs):
        for key, val in kwargs.items():
            self[key] = val

    @property
    def has_unit(self):
        """Boolean specifying whether variable has unit"""
        return True if self.units not in (1, None) else False

    @property
    def lower_limit(self):
        """Old attribute name for :attr:`minimum` (following HTAP2 defs)"""
        warnings.warn("Old name for attribute minimum", DeprecationWarning, stacklevel=2)
        return self.minimum

    @property
    def upper_limit(self):
        """Old attribute name for :attr:`maximum` (following HTAP2 defs)"""
        warnings.warn("Old name for attribute maximum", DeprecationWarning, stacklevel=2)
        return self.maximum

    @property
    def unit_str(self):
        """string representation of unit"""
        if self.units is None:
            return ""
        else:
            return f"[{self.units}]"

    @staticmethod
    def read_config():
        return parse_variables_ini()

    @property
    def var_name_info(self):
        return VarNameInfo(self.var_name)

    @property
    def aliases(self):
        """Alias variable names that are frequently found or used

        Returns
        -------
        list
            list containing valid aliases
        """
        return get_aliases(self.var_name)

    @property
    def long_name(self):
        """Wrapper for :attr:`description`"""
        return self.description

    def keys(self):
        return list(self.__dict__)

    @staticmethod
    def _check_aliases(var_name):
        ap = parse_aliases_ini()
        aliases = _read_alias_ini(ap)
        if var_name in aliases:
            return aliases[var_name]
        return _check_alias_family(var_name, ap)

    def get_default_vert_code(self):
        """Get default vertical code for variable name"""
        if self.default_vert_code is not None:
            return self.default_vert_code
        try:
            return VarNameInfo(self.var_name_aerocom).get_default_vert_code()
        except ValueError:
            logger.warning(
                f"default_vert_code not set for {self.var_name_aerocom} and "
                f"could also not be inferred"
            )
            return None

    def get_cmap(self):
        """
        Get cmap str for var

        Returns
        -------
        str

        """
        return self.map_cmap

    def _cmap_bins_from_vmin_vmax(self):
        """
        Calculate cmap discretisation bins from :attr:`vmin` and :attr:`vmax`

        Sets value of :attr:`map_cbar_levels`

        Raises
        ------
        AttributeError
             if :attr:`vmin` and :attr:`vmax` are not defined

        """
        if self.minimum == self.VMIN_DEFAULT or self.maximum == self.VMAX_DEFAULT:
            raise AttributeError(
                f"need minimum and maximum to be specified "
                f"for variable {self.var_name} in "
                f"order to retrieve cmap_bins"
            )
        self.map_cbar_levels = make_binlist(self.minimum, self.maximum)

    def get_cmap_bins(self, infer_if_missing=True):
        """
        Get cmap discretisation bins

        Parameters
        ----------
        infer_if_missing : bool
            if True and :attr:`map_cbar_levels` is not defined, try to infer
            using :func:`_cmap_bins_from_vmin_vmax`.

        Raises
        ------
        AttributeError
             if unavailable

        Returns
        -------
        list
            levels

        """
        if self.map_cbar_levels is None:
            if infer_if_missing:
                self._cmap_bins_from_vmin_vmax()
            else:
                raise AttributeError(
                    f"map_cbar_levels is not defined for variable {self.var_name}"
                )
        return self.map_cbar_levels

    def parse_from_ini(self, var_name=None, cfg=None):
        """Import information about default region

        Parameters
        ----------
        var_name : str
            variable name
        var_name_alt : str
            alternative variable name that is used if variable name is not
            available
        cfg : ConfigParser
            open config parser object

        Returns
        -------
        bool
            True, if default could be loaded, False if not
        """
        if cfg is None:
            cfg = self.read_config()
        elif not isinstance(cfg, ConfigParser):
            raise ValueError(f"invalid input for cfg, need config parser got {type(cfg)}")
        if var_name not in cfg:
            try:
                var_name = self._check_aliases(var_name)
            except VariableDefinitionError:
                logger.info(f"Unknown input variable {var_name}")
                return
            self._var_name_aerocom = var_name

        var_info = cfg[var_name]
        # this variable should import settings from another variable
        if "use" in var_info:
            use = var_info["use"]
            if use not in cfg:
                raise VariableDefinitionError(
                    f"Input variable {var_name} depends on {use} "
                    f"which is not available in variables.ini."
                )
            self.parse_from_ini(use, cfg)

        for key, val in var_info.items():
            if key in self.ALT_NAMES:
                key = self.ALT_NAMES[key]
            self._add(key, val)

    def _add(self, key, val):
        if key in self._TYPE_CONV:
            try:
                val = self._TYPE_CONV[key](val)
            except Exception:
                pass
        elif key == "units" and val == "None":
            val = "1"
        if val == "None":
            val = None
        self[key] = val

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return f"{self.var_name}\nstandard_name: {self.standard_name}; Unit: {self.units}"

    def __eq__(self, other):
        if isinstance(other, str):
            other = Variable(other)
        elif not isinstance(other, Variable):
            raise TypeError("Can only compare with str or other Variable instance")
        return True if other.var_name_aerocom == self.var_name_aerocom else False

    def __str__(self):
        head = f"Pyaerocom {type(self).__name__}"
        s = f"\n{head}\n{len(head) * '-'}"

        plot_s = "\nPlotting settings\n......................"

        for k, v in self.__dict__.items():
            if k in self.plot_info_keys:
                if v is None:
                    continue
                if isinstance(v, dict):
                    plot_s += f"\n{k} (dict)"
                    plot_s += dict_to_str(v, indent=3, ignore_null=True)
                elif isinstance(v, list):
                    plot_s += f"\n{k} (list, {len(v)} items)"
                    plot_s += list_to_shortstr(v)
                else:
                    plot_s += f"\n{k}: {v}"
            else:
                if isinstance(v, dict):
                    s += f"\n{k} (dict)"
                    s += dict_to_str(v, indent=3, ignore_null=True)
                elif isinstance(v, list):
                    s += f"\n{k} (list, {len(v)} items)"
                    s += list_to_shortstr(v)
                else:
                    s += f"\n{k}: {v}"

        s += plot_s
        return s
