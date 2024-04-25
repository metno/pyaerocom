"""
Methods to convert different standards of vertical coordinates

For details see here:

http://cfconventions.org/Data/cf-conventions/cf-conventions-1.0/build/apd.html

Note
----
UNDER DEVELOPMENT -> NOT READY YET
"""

import logging

import numpy as np
from geonum import atmosphere as atm

from pyaerocom import const
from pyaerocom.exceptions import (
    CoordinateNameError,
    DataDimensionError,
    VariableDefinitionError,
    VariableNotFoundError,
)

logger = logging.getLogger(__name__)


def atmosphere_sigma_coordinate_to_pressure(
    sigma: np.ndarray | float, ps: float, ptop: float
) -> np.ndarray | float:
    """Convert atmosphere sigma coordinate to pressure in Pa

    Note
    ----
    This formula only works at one lon lat coordinate and at one instant in
    time.

    **Formula**:

    .. math::

        p(k) = p_{top} + \\sigma(k) \\cdot (p_{surface} - p_{top})

    Parameters
    ----------
    sigma : ndarray or float
        sigma coordinate (1D) array
    ps : float
        surface pressure
    ptop : float
        ToA pressure

    Returns
    -------
    ndarray or float
        computed pressure levels in Pa (standard_name=air_pressure)
    """
    if not isinstance(ptop, float):
        if not isinstance(ptop, np.ndarray):
            try:
                ptop = float(ptop)
            except ValueError as e:
                raise ValueError(f"Invalid input for ptop. Need floating point\nError: {repr(e)}")
    return ptop + sigma * (ps - ptop)


def atmosphere_hybrid_sigma_pressure_coordinate_to_pressure(
    a: np.ndarray, b: np.ndarray, ps: float, p0: float | None = None
) -> np.ndarray:
    """Convert atmosphere_hybrid_sigma_pressure_coordinate to  pressure in Pa

    **Formula**:

    Either

    .. math::

        p(k) = a(k) \\cdot p_0 + b(k) \\cdot p_{surface}

    or

    .. math::

        p(k) = ap(k) + b(k) \\cdot p_{surface}

    Parameters
    ----------
    a : ndarray
        sigma level values (a(k) in formula 1, and ap(k) in formula 2)
    b : ndarray
        dimensionless fraction per level (must be same length as a)
    ps : float
        surface pressure
    p0 :
        reference pressure (only relevant for alternative formula 1)

    Returns
    -------
    ndarray
        computed pressure levels in Pa (standard_name=air_pressure)

    """
    if not len(a) == len(b):
        raise ValueError("Invalid input: a and b must have the same length")
    if p0 is None:
        return a + b * ps
    return a * p0 + b * ps


def geopotentialheight2altitude(geopotential_height):
    """Convert geopotential height in m to altitude in m

    Note
    ----
    This is a dummy function that returns the input, as the conversion is not
    yet implemented.

    Parameters
    ----------
    geopotential_height : float
        input geopotential height values in m

    Returns
    -------
    Computed altitude levels
    """
    raise NotImplementedError("This function is a dummy function")
    logger.warning(
        "Conversion method of geopotential height to "
        "altitude is not yet implemented and returns the "
        "input values. The introduced error is small at "
        "tropospheric altitudes"
    )
    return geopotential_height


class VerticalCoordinate:
    NAMES_SUPPORTED = {
        "altitude": "z",
        "air_pressure": "pres",
        "geopotential_height": "gph",
        "atmosphere_sigma_coordinate": "asc",
        "atmosphere_hybrid_sigma_pressure_coordinate": "ahspc",
    }

    STANDARD_NAMES = dict(map(reversed, NAMES_SUPPORTED.items()))

    NAMES_NOT_SUPPORTED = ["model_level_number"]

    #: registered names
    REGISTERED = list(NAMES_SUPPORTED) + NAMES_NOT_SUPPORTED

    CONVERSION_METHODS = {
        "asc": atmosphere_sigma_coordinate_to_pressure,
        "ahspc": atmosphere_hybrid_sigma_pressure_coordinate_to_pressure,
        "gph": geopotentialheight2altitude,
    }

    CONVERSION_REQUIRES = {
        "asc": ["sigma", "ps", "ptop"],
        "ahspc": ["a", "b", "ps", "p0"],
        "gph": [],
    }

    FUNS_YIELD = {"asc": "air_pressure", "ahspc": "air_pressure", "gph": "altitude"}

    _LEV_INCREASES_WITH_ALT = dict(
        atmosphere_sigma_coordinate=False,
        atmosphere_hybrid_sigma_pressure_coordinate=False,
        altitude=True,
    )

    def __init__(self, name=None):
        self.var_name = None
        self.standard_name = None
        self._eval_input(name)

    def _eval_input(self, name):
        if name in self.NAMES_SUPPORTED:
            self.var_name = self.NAMES_SUPPORTED[name]
            self.standard_name = name
        elif name in self.STANDARD_NAMES:
            self.var_name = name
            self.standard_name = self.STANDARD_NAMES[name]
        elif name in self.NAMES_NOT_SUPPORTED:
            self.standard_name = name
        else:
            raise ValueError(f"Invalid name for vertical coordinate: {name}")

    @property
    def fun(self):
        """Function used to convert levels into pressure"""
        return self.CONVERSION_METHODS[self.var_name]

    @property
    def conversion_requires(self):
        """Valid argument names for :func:`fun`"""
        return self.CONVERSION_REQUIRES[self.var_name]

    @property
    def conversion_supported(self) -> bool:
        """Boolean specifying whether a conversion scheme is provided"""
        return True if self.standard_name in self.NAMES_SUPPORTED else False

    @property
    def lev_increases_with_alt(self) -> bool:
        """Boolean specifying whether coordinate levels increase with altitude

        Returns
        -------
        True
        """
        if not self.var_name in self._LEV_INCREASES_WITH_ALT:
            if self.standard_name in self._LEV_INCREASES_WITH_ALT:
                return self._LEV_INCREASES_WITH_ALT[self.standard_name]
            raise ValueError(
                f"Failed to access information lev_increases_with_alt "
                f"for vertical coordinate {self.var_name}"
            )
        return self._LEV_INCREASES_WITH_ALT[self.var_name]

    def calc_pressure(self, lev: np.ndarray, **kwargs) -> np.ndarray:
        """Compute pressure levels for input vertical coordinate

        Parameters
        ----------
        vals : ndarray
            level values that are supposed to be converted into pressure
        **kwargs
            additional  keyword args required for computation of pressure
            levels (cf. :attr:`CONVERSION_METHODS` and corresponding inputs for method
            available)

        Returns
        -------
        ndarray
            pressure levels in Pa
        """

        if not self.var_name in self.NAMES_SUPPORTED:
            raise CoordinateNameError(
                f"Variable {self.var_name} cannot be converted to pressure levels. "
                f"Conversion is only possible for supported variables:\n{self.vars_supported_str}"
            )

        coord_values = kwargs.pop(self.var_name)
        return self.fun(coord_values, **kwargs)

    @property
    def vars_supported_str(self) -> str:
        from pyaerocom._lowlevel_helpers import dict_to_str

        return dict_to_str(self.NAMES_SUPPORTED)

    def pressure2altitude(self, p, **kwargs):
        """Convert pressure to altitude

        Wrapper for method

        Parameters
        ----------

        Returns
        -------
        """
        raise NotImplementedError("Coming soon...")


class AltitudeAccess:
    #: Additional variable names (in AEROCOM convention) that are used
    #: to search for additional files that can be used to access or compute
    #: the altitude levels at each grid point
    ADD_FILE_VARS = ["z", "z3d", "pres", "deltaz3d"]

    #: Additional variables that are required to compute altitude levels
    ADD_FILE_REQ = {"deltaz3d": ["ps"]}

    ADD_FILE_OPT = {"pres": ["temp"]}

    def __init__(self, gridded_data):
        from pyaerocom.griddeddata import GriddedData

        if not isinstance(gridded_data, GriddedData):
            raise ValueError("Invalid input: require instance of GriddedData class")
        if not gridded_data.has_latlon_dims:
            raise NotImplementedError(
                f"Altitude access requires latitude and longitude dimensions to be available "
                f"in input GriddedData: {gridded_data.short_str()}"
            )
        self.data_obj = gridded_data
        self._subset1d = None
        self._checked_and_failed = []
        self._has_access = False
        self.logger = logger

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __getitem__(self, key):
        return self.__dict__[key]

    def __contains__(self, key):
        return True if key in self.__dict__ else False

    @property
    def has_access(self) -> bool:
        """Boolean specifying whether altitudes can be accessed

        Note
        ----
        Performs access check using :func:`check_altitude_access` if access
        flag is False
        """
        if not self._has_access:
            self._has_access = self.check_altitude_access()
        return self._has_access

    @property
    def coord_list(self):
        """List of AeroCom coordinate names for altitude access"""
        l = self.ADD_FILE_VARS + list(VerticalCoordinate.NAMES_SUPPORTED.values())
        return list(dict.fromkeys(l))

    def search_aux_coords(self, coord_list) -> bool:
        """Search and assign coordinates provided by input list

        All coordinates that are found are assigned to this object and can
        be accessed via ``self[coord_name]``.

        Parameters
        ----------
        coord_list : list
            list containing AeroCom coordinate names

        Returns
        -------
        bool
            True if all coordinates can be accessed, else False

        Raises
        ------
        CoordinateNameError
            if one of the input coordinate names is not supported by pyaerocom.
            See coords.ini file of pyaerocom for available coordinates.
        """
        all_ok = True
        if isinstance(coord_list, str):
            coord_list = [coord_list]
        d = self.data_obj
        for coord in coord_list:
            if coord in self:
                continue
            try:
                coord_info = const.COORDINFO[coord]
            except VariableDefinitionError:
                raise CoordinateNameError(f"Coordinate {coord} is not supported by pyaerocom.")
            # 1. check if coordinate is assigned in data object directly
            d._update_coord_info()
            if coord in d._coord_var_names:
                self[coord] = d[coord]
            else:
                try:
                    self[coord] = d.search_other(coord)
                    print(f"Adding coord {coord}")
                except Exception:
                    all_ok = False
        return all_ok

    @property
    def reader(self):
        """Instance of :class:`ReadGridded`"""
        return self.data_obj.reader

    def _check_vars_in_data_obj(self):
        for var in self.ADD_FILE_VARS:
            try:
                self._check_var_in_data_obj(var_name=var)
                return var
            except Exception:
                pass
        raise VariableNotFoundError()

    # ToDo: check alias names
    def _check_var_in_data_obj(self, var_name):
        c = VerticalCoordinate(var_name)

        if c.var_name in self.data_obj:
            self[var_name] = self.data_obj[var_name]
            self._verify_altitude_access()
        elif var_name in c.STANDARD_NAMES:
            std_name = c.STANDARD_NAMES[var_name]
            if std_name in self.data_obj:
                self[var_name] = self.data_obj[std_name]

    def check_altitude_access(self, **coord_info) -> bool:
        """Checks if altitude levels can be accessed

        Parameters
        ----------
        **coord_info
            test coordinate specifications for extraction of 1D data object.
            Passed to :func:`extract_1D_subset_from_data`.

        Returns
        -------
        bool
            True, if altitude access is provided, else False
        """
        # 1. check if altitude or pressure field is available in data object as
        # variable
        for coord in self.coord_list:
            if coord in self._checked_and_failed:
                continue
            elif self._check_altitude_access_helper(coord, **coord_info):
                return True
            self._checked_and_failed.append(coord)
        return False

    def _check_altitude_access_helper(self, coord_name, **coord_info) -> bool:
        cstd_name = const.COORDINFO[coord_name].standard_name

        if not self.search_aux_coords(coord_name):
            if isinstance(cstd_name, str):
                if not self.search_aux_coords(cstd_name):
                    return False

        coord = VerticalCoordinate(cstd_name)
        if coord.conversion_supported:
            if self.search_aux_coords(coord.conversion_requires):
                if self._verify_altitude_access(coord):
                    return True
        return False

    def _verify_altitude_access(self, coord, **coord_info) -> bool:
        """Verify access of altitude data

        Parameters
        ----------
        subset : GriddedData
            1-dimensional subset of input data object
        coord : VerticalCoordinate
            instance of vertical coordinate that is used to specify requirements
            for altitude computation

        Returns
        -------
        bool
            True, if altitude access was sueccessful, else False
        """
        subset = self._subset1d
        if subset is None:
            subset = self.extract_1D_subset_from_data(**coord_info)

        subset._update_coord_info()
        cstd_name = coord.standard_name
        if not subset[cstd_name].ndim == 1:
            raise DataDimensionError(
                f"Unexpected error: dimension of variable {cstd_name} should be 1"
            )
        raise NotImplementedError

    def get_altitude(self, latitude, longitude):
        raise NotImplementedError
