#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods to convert different standards of vertical coordinates

For details see here:
    
    http://cfconventions.org/Data/cf-conventions/cf-conventions-1.0/build/apd.html
"""

from pyaerocom import GEONUM_AVAILABLE, const
from pyaerocom.exceptions import (CoordinateNameError, CoordinateError,
                                  VariableNotFoundError,
                                  AltitudeAccessError,
                                  DataDimensionError)
from pyaerocom.helpers import get_standard_unit


def atmosphere_sigma_coordinate_to_pressure(sigma, ps, ptop):
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
        try:
            ptop = float(ptop)
        except Exception as e:
            raise ValueError('Invalid input for ptop. Need floating point\n'
                             'Error: {}'.format(repr(e)))
    return ptop + sigma * (ps - ptop)
    

def atmosphere_hybrid_sigma_pressure_coordinate_to_pressure(a, b, ps, p0=None):
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
        raise ValueError('Invalid input: a and b must have the same length')
    if p0 is None:
        return a + b*ps
    return a*p0 + b*ps

def geopotentialheight2altitude(geopotential_height):
    """Convert geopotential height in m to altitude in m
    
    Note
    ----
    This is a dummy function that returns the input, as the conversion is not
    yet implemented.
    
    Parameters
    ----------
    geopotential_height
        input geopotential height values in m
    
    Returns
    -------
    Computed altitude levels
    """
        
    const.print_log.warning('Conversion method of geopotential height to '
                            'altitude is not yet implemented and returns the '
                            'input values. The introduced error is small at '
                            'tropospheric altitudes')
    return geopotential_height

def pressure2altitude(p, *args, **kwargs):
    """General formula to convert atm. pressure to altitude
    
    Wrapper method for :func:`geonum.atmosphere.pressure2altitude`
    
    **Formula:**
        
    .. math::
        
        h = h_{ref} + \\frac{T_{ref}}{L} \\left(\\exp\\left[-\\frac{\\ln\\left(\\frac{p}{p_{ref}} \\right)}{\\beta}\\right] - 1\\right) \\quad [m]
    
    where:
        
        - :math:`$h_{ref}$` is a reference altitude         
        - :math:`$T_{ref}$` is a reference temperature
        - :math:`$L$` is the atmospheric lapse-rate (cf. :attr:`L_STD_ATM`, \
                                                     :attr:`L_DRY_AIR`)
        - :math:`$p$` is the pressure (cf. :func:`pressure`)
        - :math:`$p_{ref}$` is a reference pressure
        - :math:`$\\beta$` is computed using :func:`beta_exp`
    
    Parameters
    ----------
    p
        pressure in Pa
    *args 
        additional non-keyword args passed to 
        :func:`geonum.atmosphere.pressure2altitude` 
    **kwargs
        additional keyword args passed to
        :func:`geonum.atmosphere.pressure2altitude` 
        
    Returns
    -------
    altitudes in m corresponding to input pressure levels in defined atmosphere
    """
    if not GEONUM_AVAILABLE:
        raise ModuleNotFoundError('Feature disabled: need geonum library')
    from geonum import atmosphere as atm
    return atm.pressure2altitude(p, *args, **kwargs)


def supported(standard_name):
    return True if standard_name in VerticalCoordinate.REGISTERED else False

    
class VerticalCoordinate(object):
    
    REGISTERED = {
    'altitude'                                      : 'z', 
    'air_pressure'                                  : 'pres',
    'geopotential_height'                           : 'gph',
    'atmosphere_sigma_coordinate'                   : 'asc', 
    'atmosphere_hybrid_sigma_pressure_coordinate'   : 'ahspc',
    }

    CONVERSION_METHODS = {
    'asc'   :   atmosphere_sigma_coordinate_to_pressure,
    'ahspc' :   atmosphere_hybrid_sigma_pressure_coordinate_to_pressure,
    'gph'   :   geopotentialheight2altitude
    }

    CONVERSION_REQUIRES = {

    'asc'   :   ['sigma', 'ps', 'ptop'],
    'ahspc' :   ['a', 'b', 'ps', 'p0'],
    'gph'   :   []
    }
    
    FUNS_YIELD = {
    'asc'   :   'air_pressure',
    'ahspc' :   'air_pressure',
    'gph'   :   'altitude'
    }
    
    _LEV_INCREASES_WITH_ALT = dict(
        atmosphere_sigma_coordinate=False,
        atmosphere_hybrid_sigma_pressure_coordinate=False)
    
    def __init__(self, name=None):
        if not name in self.CONVERSION_METHODS:
            raise ValueError('Invalid name for vertical coordinate. Choose '
                             'from {}'.format(list(self.CONVERSION_METHODS)))
        self.name = name
    
    @property
    def fun(self):
        """Function used to convert levels into pressure"""
        return self.CONVERSION_METHODS[self.name]
    
    @property
    def conversion_requires(self):
        """Valid argument names for :func:`fun`"""
        return self.CONVERSION_REQUIRES[self.name]
    
    @property
    def lev_increases_with_alt(self):
        """Boolean specifying whether coordinate levels increase with altitude
        
        Returns
        -------
        True
        """
        if not self.name in self._LEV_INCREASES_WITH_ALT:
            raise ValueError('Failed to access information '
                             'lev_increases_with_alt for vertical coordinate {}'
                             .format(self.name))
        return self._LEV_INCREASES_WITH_ALT[self.name]
    
    def calc_pressure(self, vals, **kwargs):
        """Compute pressure levels for input vertical coordinate
        
        Parameters
        ----------
        vals 
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
        if not self.name in self.VARS:
            raise CoordinateNameError('Invalid standard name: {}. Supported '
                                      'coordinate names are: {}'
                                      .format(self.name,
                                              self.VARS.keys()))
        coord_values = kwargs.pop(self.name)
        return self.fun(coord_values, **kwargs)
    
    def calc_altitude(self, p, **kwargs):
        """Compute altitude for input vertical coordinates
        
        Parameters
        ----------
        standard_name : str
            standard name of vertical coordinate
        **kwargs
            additional  keyword args required for computation of pressure
            levels (cf. :attr:`CONVERSION_METHODS` and corresponding inputs for method 
            available)
            
        Returns
        -------
        ndarray
            pressure levels in Pa
        """         
        return pressure2altitude(p, **kwargs)
     
class AltitudeAccess(object):
    
    #: Additional variable names (in AEROCOM convention) that are used
    #: to search for additional files that can be used to access or compute 
    #: the altitude levels at each grid point
    ADD_FILE_VARS = ['z', 'z3d', 'deltaz3d', 'pres']
    
    #: Additional variables that are required to compute altitude levels
    ADD_FILE_REQ = {'deltaz3d' : ['ps']}
    
    ADD_FILE_OPT = {'pres'  :   ['temp']}
    
    def __init__(self, gridded_data):
        from pyaerocom import logger
        from pyaerocom.griddeddata import GriddedData
        if not isinstance(gridded_data, GriddedData):
            raise ValueError('Invalid input: require instance of GriddedData '
                             'class')
        if not gridded_data.has_latlon_dims:
            raise NotImplementedError('Altitude access requires latitude and '
                                      'longitude dimensions to be available '
                                      'in  input GriddedData: {}'
                                      .format(gridded_data.short_str()))
        self.data_obj = gridded_data
        self._has_access = False
        self.logger = logger
        
    @property
    def all_search_keys(self):
        all_vars = [x for x in self.ADD_FILE_VARS]
        for add_vars in self.ADD_FILE_REQ.values():
            if not isinstance(add_vars, list):
                raise Exception
            all_vars.extend(add_vars)
        for opt_vars in self.ADD_FILE_OPT.values():
            if not isinstance(opt_vars, list):
                raise Exception
            all_vars.extend(opt_vars)
        return list(dict.fromkeys(all_vars))
    
    def __setitem__(self, key, val):
        self.__dict__[key] = val
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __contains__(self, key):
        return True if key in self.__dict__ else False
            
    @property
    def has_access(self):
        """Boolean specifying whether altitudes can be accessed
        
        Note
        ----
        Performs access check using :func:`check_altitude_access` if access 
        flag is False
        """
        if not self._has_access:
            self._has_access = self.check_altitude_access()
        return self._has_access
    
    def _find_and_read_add_var(self, add_var_name):
        """Search an additionally required variable in external file
        
        Parameter
        --------
        add_var_name : str
            Variable name in AEROCOM convention
        
        Returns
        -------
        GriddedData
            additional data file
        """
        _search = [add_var_name]
        _search.extend(const.VARS[add_var_name].aliases)
        r = self.data_obj.reader
        d = self.data_obj
        for _var in _search:
            if _var in r.vars:
                return r.read_var(_var, start=d.start, stop=d.stop,
                                  ts_type=d.ts_type, flex_ts_type=False)
        raise VariableNotFoundError('Auxiliary variable {} could not be found'
                                    .format(add_var_name))
    
    def check_and_import_add_var(self, add_var):
        
        add_var_data = self._find_and_read_add_var(add_var)
        _req = []
        if add_var in self.ADD_FILE_REQ:
            for aux_var in self.ADD_FILE_REQ[add_var]:
                _req[aux_var] = self._find_and_read_add_var(aux_var)
        _opt = []
        if add_var in self.ADD_FILE_OPT:
            for aux_opt in self.ADD_FILE_OPT[add_var]:
                try:
                    _opt[aux_opt] = self._find_and_read_add_var(aux_opt)
                except:
                    pass
        
        self._check_altitude_access(add_var_data, 
                                    add_var_data_req=_req,
                                    add_var_data_opt=_opt)
        self[add_var] = add_var_data
        for item in _req:
            self[item.var_name] = item
        for item in _opt:
            self[item.var_name] = item
        
    def _check_coord_conversion(self, add_var_data, add_var_data_req,
                                add_var_data_opt):
        
        coord = VerticalCoordinate(add_var_data.standard_name)
        
    def _check_altitude_access(self, add_var_data, add_var_data_req=None,
                               add_var_data_opt=None):
        """Checks if altitude can be computed based on input fields
        
        See :func:`check_and_import_add_var` for details on usage. 
        
        """
        var = add_var_data.var_name
        if var == 'z':
            if not add_var_data.shape == self.data_obj.shape:
                raise NotImplementedError('Altitude field must have the same '
                                          'shape as input data object')
            unit_std = get_standard_unit(add_var_data.var_name)
            if not add_var_data.unit == unit_std:
                add_var_data.convert_unit(unit_std)
            if add_var_data.standard_name == 'altitude':
                return True
            elif add_var_data.standard_name == 'geopotential_height':
                self._check_coord_conversion(add_var_data, add_var_data_req,
                                             add_var_data_opt)
        
    def extract_1D_subset_from_data(self, **coord_info):
        """Extract 1D subset containing only vertical coordinate dimension
        
        Note
        ----
        So far this Works only for 4D or 3D data that contains latitude and 
        longitude dimension and a vertical coordinate, optionally also a time
        dimension.
        
        The subset is extracted for a test coordinate (latitude, longitude) 
        that may be specified optinally via :attr:`coord_info`.
        
        Parameters
        ----------
        **coord_info
            optional test coordinate specifications for other than vertical 
            dimension. For all dimensions that are not specified explicitely,
            the first available coordinate in :attr:`data_obj` is used.
        """
        
        d = self.data_obj
        if not d.has_latlon_dims:
            raise DataDimensionError('Gridded data object needs both latitude '
                                     'and longitude dimensions')
        try:
            d.check_dimcoords_tseries()
        except DataDimensionError:
            d.reorder_dimensions_tseries()
        test_coord = {}
        for dim_coord in d.dimcoord_names[:-1]:
            if dim_coord in coord_info:
                test_coord[dim_coord] = coord_info[dim_coord]
            else:
                test_coord[dim_coord] = d[dim_coord].points[0]    
        subset = d.sel(**test_coord)
        if not subset.ndim == 1:
            raise DataDimensionError('Something went wrong with extraction of '
                                     '1D subset at coordinate {}. Resulting '
                                     'data object has {} dimensions instead'
                                     .format(test_coord, subset.ndim))
        return subset
    
    def check_altitude_access(self, **coord_info):
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
        
        access_okay = False
            
        subset = self.extract_1D_subset_from_data(**coord_info)
        
        coord_name = subset.dimcoord_names[0]
        
        if 'altitude' in subset.dimcoord_names:
            access_okay = True
        else:
            coord = VerticalCoordinate()
        
        return access_okay
    
    def find_and_import_auxvars(self, reader=None):
        """Find and read auxiliary variables for altitude access
        
        This directory (if available) is used to check if potential files with
        altitude information are available
        
        Parameters
        ----------
        reader : ReadGridded
            instance of reader class, if None, then the reader is accessed from
            :attr:`data_obj` (instance of :class:`GriddedData`)
        """
        if reader is None:
            reader = self.data_obj.reader
        for add_var in self.ADD_FILE_VARS:
            try:
                self.check_and_import_add_var(add_var)
            except (VariableNotFoundError, AltitudeAccessError) as e:
                self.logger.warning(repr(e))
        raise CoordinateError('Could not find required additional coordinate '
                              'information for the computation of altitude '
                              'levels')
    
    
    def get_altitude(self, latitude, longitude):
        pass
    


if __name__ == '__main__':
    import pyaerocom as pya
# =============================================================================
#     reader1 = pya.io.ReadGridded('ECMWF_CAMS_REAN')
#     
#     d1 = reader1.read_var('ec532aer', 
#                          vert_which='ModelLevel', 
#                          start=2010)
#     
#     aac1 = d1.altitude_access
#     
#     subset1 = aac1.extract_1D_subset_from_data()
# =============================================================================
    
    reader2 = pya.io.ReadGridded('OsloCTM3v1.01')
    
    d2 = reader2.read_var('ec550aer', 
                          vert_which='ModelLevel', 
                          start=2010)
    d2['lon']
    aac2 = d2.altitude_access
    
    subset2 = aac2.extract_1D_subset_from_data()
    
    
    #print(subset1)
    print(subset2)
    
    
# =============================================================================
#     import numpy as np
#     import pyaerocom as pya
#     
#     pya.change_verbosity('warning')
#     c = VerticalCoordinate('pressure')
#     
#     arr = np.linspace(1013*100, 100*100, 100)
#     print(arr)
#     
#     print(c.calc_altitude(p=arr))
#     
#     
#     r = pya.io.ReadGridded('CAM5.3-Oslo_AP3-CTRL2016-PD')
#     print(r)
#     data = r.read_var('ec5503Daer')
#     
#     acc = AltitudeAccess(data)
#     acc.find_and_import_auxvars()
#     
#     
# =============================================================================
    