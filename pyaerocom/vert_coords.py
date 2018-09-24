#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods to convert different standards of vertical coordinates

For details see here:
    
    http://cfconventions.org/Data/cf-conventions/cf-conventions-1.0/build/apd.html
"""

from pyaerocom import GEONUM_AVAILABLE
from pyaerocom.exceptions import CoordinateNameError
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
    p0 : reference pressure (only relevant for alternative formula 1)
    
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
    *args, **kwargs:
        additional arguments supported by :func:`geonum.atmosphere.
        pressure2altitude` (cf. `geonum docs <https://geonum.readthedocs.io/
        en/latest/api.html#geonum.atmosphere.pressure2altitude>`__)
        
    Returns
    -------
    float
        altitude corresponding to pressure level in defined atmosphere
    """
    if not GEONUM_AVAILABLE:
        raise ModuleNotFoundError('Feature disabled: need geonum library')
    from geonum import atmosphere as atm
    return atm.pressure2altitude(p)


def supported(standard_name):
    return True if standard_name in VerticalCoordinate._FUNS else False

class VerticalCoordinate(BrowseDict):
    _FUNS = dict(
        atmosphere_sigma_coordinate=
        atmosphere_sigma_coordinate_to_pressure,
        atmosphere_hybrid_sigma_pressure_coordinate=
        atmosphere_hybrid_sigma_pressure_coordinate_to_pressure)
    
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
            raise ValueError('Invalid name for vertical coordinate')
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
    
    def calc_pressure(self, **kwargs):
        """Compute pressure levels for input vertical coordinate
        
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
        if not self.name in self.VARS:
            raise CoordinateNameError('Invalid standard name: {}. Supported '
                                      'coordinate names are: {}'
                                      .format(self.name,
                                              self.VARS.keys()))
        coord_values = kwargs.pop(self.name)
        return self._FUNS[self.name](coord_values, **kwargs)
    
    def calc_altitude(self, **kwargs):
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
        return pressure2altitude(self.calc_pressure(**kwargs))
        
if __name__ == '__main__':
    import pyaerocom as pya
    
    MODEL_ID_3D = 'SPRINTARS-T213_AP3-CTRL2016-PD'
    
    data = pya.io.ReadGridded(MODEL_ID_3D).read_var('ec550aer3d',
                             start=2010)
    
    surfp = data.grid.coord('surface_air_pressure')
    
    print(data)