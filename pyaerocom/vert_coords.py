#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods to convert different standards of vertical coordinates

For details see here:
    
    http://cfconventions.org/Data/cf-conventions/cf-conventions-1.0/build/apd.html
"""

from pyaerocom import GEONUM_AVAILABLE, const
from pyaerocom.exceptions import (CoordinateNameError, CoordinateError,
                                  VariableNotFoundError)
from pyaerocom._lowlevel_helpers import BrowseDict

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
    sigma : ndarray
        sigma coordinate (1D) array
    ps : :obj:`float` or :obj:`ndarray`
        surface pressure (may be multidimensional). Note that it 
    
    Returns
    -------
    ndarray
        pressure levels in Pa
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
        pressure levels in Pa
    
    """
    if not len(a) == len(b):
        raise ValueError('Invalid input: a and b must have the same length')
    if p0 is None:
        return a + b*ps
    return a*p0 + b*ps

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
    p : float
        pressure in Pa
    *args 
        additional non-keyword args passed to 
        :func:`geonum.atmosphere.pressure2altitude` 
    **kwargs
        additional keyword args passed to
        :func:`geonum.atmosphere.pressure2altitude` 
        
    Returns
    -------
    float
        altitude corresponding to pressure level in defined atmosphere
    """
    if not GEONUM_AVAILABLE:
        raise ModuleNotFoundError('Feature disabled: need geonum library')
    from geonum import atmosphere as atm
    return atm.pressure2altitude(p, *args, **kwargs)


def supported(standard_name):
    return True if standard_name in VerticalCoordinate._FUNS else False

class VerticalCoordinate(object):
    _FUNS = dict(
        pressure = None,
        atmosphere_sigma_coordinate=atmosphere_sigma_coordinate_to_pressure,
        atmosphere_hybrid_sigma_pressure_coordinate=atmosphere_hybrid_sigma_pressure_coordinate_to_pressure
    
    )
    
    _ARG_NAMES = dict(
        atmosphere_sigma_coordinate=dict(sigma=['lev', 'sigma'],
                                         ps=['ps'],
                                         ptop=['ptop']),
        atmosphere_hybrid_sigma_pressure_coordinate=dict(a=['a', 'lev'],
                                                         b=['b'],
                                                         ps=['ps'],
                                                         p0=['p0']))
    
    _LEV_INCREASES_WITH_ALT = dict(
        atmosphere_sigma_coordinate=False,
        atmosphere_hybrid_sigma_pressure_coordinate=False)
    
    def __init__(self, name=None):
        if not name in self._FUNS:
            raise ValueError('Invalid name for vertical coordinate. Choose '
                             'from {}'.format(list(self._FUNS)))
        self.name = name
    
    @property
    def fun(self):
        """Function used to convert levels into pressure"""
        return self._FUNS[self.name]
    
    @property
    def arg_names(self):
        """Valid argument names for :func:`fun`"""
        return self._ARG_NAMES[self.name]
    
    @property
    def lev_increases_with_alt(self):
        """Boolean specifying whether coordinate levels increase or decrease with altitude"""
        return self._LEV_INCREASES_WITH_ALT[self.name]
    
    def calc_pressure(self, vals, **kwargs):
        """Compute pressure levels for input vertical coordinate
        
        Parameters
        ----------
        vals 
            level values that are supposed to be converted into pressure
        **kwargs
            additional  keyword args required for computation of pressure
            levels (cf. :attr:`_FUNS` and corresponding inputs for method 
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
            levels (cf. :attr:`_FUNS` and corresponding inputs for method 
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
    ADD_FILE_VARS = ['z3d', 'deltaz3d', 'pres']
    
    #: Additional variables that are required to compute altitude levels
    ADD_FILE_REQ = {'deltaz3d' : ['ps']}
    
    ADD_FILE_OPT = {'pres'  :   ['temp']}

    ALT_CONV_FUNS = {'z3d'  : NotImplementedError('Coming soon...'),
                     }
    
    def __init__(self, gridded_data):
        from pyaerocom import GriddedData, logger
        if not isinstance(gridded_data, GriddedData):
            raise ValueError('Invalid input: require instance of GriddedData '
                             'class')
        self.data_obj = gridded_data
        self.add_data = BrowseDict()
        
        self.logger = logger
        
    def _init_reader(self, print_info=True):
        """Initiate reader class for access of additional files"""
        self.data_obj.init_reader(print_info=print_info)
    
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
        _search.extend(const.VAR_PARAM[add_var_name].aliases)
        r = self.data_obj.reader
        d = self.data_obj
        for _var in _search:
            if _var in r.vars:
                return r.read_var(_var, start=d.start, stop=d.stop,
                                  ts_type=d.ts_type, flex_ts_type=False)
        raise VariableNotFoundError('Auxiliary variable {} could not be found'
                                    .format(add_var_name))
        
    def find_and_import_auxvars(self):
        """Data directory of original data input file
        
        This directory (if available) is used to check if potential files with
        altitude information are available
        """
        if self.data_obj.reader is None:
            self._init_reader()
        for add_var in self.ADD_FILE_VARS:
            result = {}
            try:
                result[add_var] = self._find_and_read_add_var(add_var)
                if add_var in self.ADD_FILE_REQ:
                    for aux_var in self.ADD_FILE_REQ[add_var]:
                        result[aux_var] = self._find_and_read_add_var(aux_var)
                if add_var in self.ADD_FILE_OPT:
                    for aux_opt in self.ADD_FILE_OPT[add_var]:
                        try:
                            result[aux_opt] = self._find_and_read_add_var(aux_opt)
                        except:
                            pass
                self.add_data = result
                return result
            except VariableNotFoundError as e:
                self.logger.warning(repr(e))
        raise CoordinateError('Could not find required additional coordinate '
                              'information for the computation of altitude '
                              'levels')
    
    def get_altitude(latitude, longitude):
        raise NotImplementedError('Coming soon...')
        
if __name__ == '__main__':
    import numpy as np
    import pyaerocom as pya
    
    pya.change_verbosity('warning')
    c = VerticalCoordinate('pressure')
    
    arr = np.linspace(1013*100, 100*100, 100)
    print(arr)
    
    print(c.calc_altitude(p=arr))
    
    
    r = pya.io.ReadGridded('CAM5.3-Oslo_AP3-CTRL2016-PD')
    print(r)
    data = r.read_var('ec5503Daer')
    
    acc = AltitudeAccess(data)
    acc.find_and_import_auxvars()
    
    
    