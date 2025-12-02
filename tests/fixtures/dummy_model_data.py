import pytest
import iris
import numpy as np
from pyaerocom import GriddedData


@pytest.fixture
def fake_model_data_with_altitude():
    longitude = iris.coords.DimCoord(
        np.linspace(-15, 25, 20),
        var_name="lon",
        standard_name="longitude",
        units="degrees",
    )
    latitude = iris.coords.DimCoord(
        np.linspace(50, 55, 10),
        var_name="lat",
        standard_name="latitude",
        units="degrees",
    )
    altitude = iris.coords.DimCoord(
        np.linspace(0, 60000, 10000),
        var_name="alt",
        standard_name="altitude",
        units="meters",
    )
    time = iris.coords.DimCoord(
        np.arange(18892, 18892 + 7, 1),
        var_name="time",
        standard_name="time",
        units="days since epoch",
    )
    dummy = iris.cube.Cube(
        np.ones((time.shape[0], longitude.shape[0], latitude.shape[0], altitude.shape[0]))
    )

    latitude.guess_bounds()
    longitude.guess_bounds()
    altitude.guess_bounds()

    dummy.add_dim_coord(time, 0)
    dummy.add_dim_coord(longitude, 1)
    dummy.add_dim_coord(latitude, 2)
    dummy.add_dim_coord(altitude, 3)

    dummy.var_name = "bsc532aer"

    data = GriddedData(dummy)

    data.units = "km-1 sr-1"

    return data
