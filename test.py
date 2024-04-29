import numpy as np


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
    if len(a) != len(b):
        raise ValueError("Invalid input: a and b must have the same length")
    if p0 is None:
        return a + b * ps
    return a * p0 + b * ps


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
    if not isinstance(ptop, float | np.ndarray):
        try:
            ptop = float(ptop)
        except ValueError as e:
            raise ValueError(
                f"Invalid input for ptop. Need floating point\nError: {repr(e)}"
            ) from e
    return ptop + sigma * (ps - ptop)


sine = np.sin(np.arange(1000))

result = atmosphere_sigma_coordinate_to_pressure(0.5, 0, 1)

print(result)
