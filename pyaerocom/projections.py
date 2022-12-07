import numpy as np


class Projection:
    """Class that converts longitude and latitude coordinates into the grid coordiantes (i, j) for various projections

    Note
    ____

    - WIP
    """

    # VALID_GRID_SIZES = (6.25, 12.5, 25)

    # Valid hemisphere names.
    NORTH = "north"
    SOUTH = "south"
    VALID_HEMISPHERES = (NORTH, SOUTH)

    # Earth-parameter defualts
    TRUE_SCALE_LATITUDE = 70
    EARTH_RADIUS_KM = 6378.273
    EARTH_ECCENTRICITY = 0.081816153

    def __init__(self, projection_parameters: dict = None):
        # default projection_parameters (i.e., corresponds to no projection)
        self._projection_name = None
        self._projection_parameters = None

        self.SUPPORTED_PROJECTION_MAP = {
            "Lambert": self._convert_to_lambert_coords,
            "Polar_Stereographic": self._convert_to_polar_stereographic_coords,
        }

        if projection_parameters is not None:
            assert set(projection_parameters) <= set(self.SUPPORTED_PROJECTION_MAP)
            assert len(projection_parameters) == 1
            self._projection_parameters = projection_parameters
            self._projection_name = projection_parameters.keys()

    # Define setters and getters in case not initalized
    @property
    def projection_name(self):
        return self._projection_name

    @property
    def projection_parameters(self):
        return self._projection_parameters

    @projection_name.setter
    def projection_name(self, name):
        if name not in self.SUPPORTED_PROJECTION_MAP:
            raise ValueError(f"{name} not in {self.SUPPORTED_PROJECTION_MAP}")
        self._projection_name = name

    @projection_parameters.setter
    def projection_parameter(self, projection_parameters: dict = None):
        if not projection_parameters:
            raise ValueError(f"Expected projection_parameters, recieved {projection_parameters}")
        self._projection_parameters = projection_parameters

    def conversion_function(self, *args):
        return self.SUPPORTED_PROJECTION_MAP[self._projection_name](*args)

    def _convert_to_lambert_coords(
        self, longitudes: np.ndarray = None, latitudes: np.ndarray = None
    ):
        if not longitudes and latitudes:
            raise ValueError(f"longitudes and latitudes must be provided")
        raise NotImplementedError(f"Conversion to Lambert coordinates is a WIP")

    def _convert_to_polar_stereographic_coords(
        self, longitudes: np.ndarray = None, latitudes: np.ndarray = None
    ):

        if not longitudes and latitudes:
            raise ValueError(f"longitudes and latitudes must be provided")
        raise NotADirectoryError("Conversion to Polar Stereographic coordinates is a WIP")
