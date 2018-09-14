#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Methods to convert different standards of vertical coordinates

For details see here:
    
    http://cfconventions.org/Data/cf-conventions/cf-conventions-1.0/build/apd.html
"""

from pyaerocom import GEONUM_AVAILABLE
    
def atmosphere_sigma_coordinate_to_pressure(sigma, psurf, ptop):
    """Convert atmosphere sigma coordinate to altitude in m
    
    Note
    ----
    This formula only works at one lon lat coordinate and at one instant in 
    time. 
    
    **Formula**:
    
    .. math::
        
        p(k) = p_{top} + \\sigma(k) \\cdot (p_{surf} - p_{top})
    
    Parameters
    ----------
    sigma : ndarray
        sigma coordinate (1D) array
    psurf : :obj:`float` or :obj:`ndarray`
        surface pressure (may be multidimensional). Note that it 
    """
    if not isinstance(ptop, float):
        try:
            ptop = float(ptop)
        except Exception as e:
            raise ValueError('Invalid input for ptop. Need floating point\n'
                             'Error: {}'.format(repr(e)))
    return ptop * sigma * (psurf - ptop)

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

if __name__ == '__main__':
    import pyaerocom as pya
    
    MODEL_ID_3D = 'SPRINTARS-T213_AP3-CTRL2016-PD'
    
    data = pya.io.ReadGridded(MODEL_ID_3D).read_var('ec550aer3d',
                             start_time=2010)
    
    surfp = data.grid.coord('surface_air_pressure')
    
    print(data)