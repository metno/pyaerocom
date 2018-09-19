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
    """Convert atmosphere sigma coordinate to altitude in m
    
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


class VerticalCoordinate(BrowseDict):

    FUNS = dict(atmosphere_sigma_coordinate=
                atmosphere_sigma_coordinate_to_pressure)
    
    ARG_NAMES = dict(atmosphere_sigma_coordinate=dict(sigma=['lev', 'sigma'],
                                                      ps=['ps'],
                                                      ptop=['ptop']))
    
    LEV_INCREASES_WITH_ALT = dict(atmosphere_sigma_coordinate=False)
    
    def __init__(self, name=None):
        if not name in self.supported:
            raise ValueError('Invalid name for vertical coordinate')
            
    @property
    def supported(self):
        return list(self.VARS.keys())
    
    def calc_pressure(self, **kwargs):
        """Compute pressure levels for input vertical coordinate
        
        Parameters
        ----------
        standard_name : str
            standard name of vertical coordinate
        **kwargs
            additional  keyword args required for computation of pressure
            levels (cf. :attr:`FUNS` and corresponding inputs for method 
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
        return self.FUNS[self.name](coord_values, **kwargs)
    
    def calc_altitude(self, standard_name, **kwargs):
        """Compute altitude for input vertical coordinates
        
        Parameters
        ----------
        standard_name : str
            standard name of vertical coordinate
        **kwargs
            additional  keyword args required for computation of pressure
            levels (cf. :attr:`FUNS` and corresponding inputs for method 
            available)
            
        Returns
        -------
        ndarray
            pressure levels in Pa
        """
        return pressure2altitude(self.calc_pressure(standard_name, **kwargs))
        
if __name__ == '__main__':
    import pyaerocom as pya
    
    MODEL_ID_3D = 'SPRINTARS-T213_AP3-CTRL2016-PD'
    
    data = pya.io.ReadGridded(MODEL_ID_3D).read_var('ec550aer3d',
                             start_time=2010)
    
    surfp = data.grid.coord('surface_air_pressure')
    
    print(data)