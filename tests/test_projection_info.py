import xarray
from pytest import approx
import numpy as np

from pyaerocom.projection_information import ProjectionInformation
from tests.fixtures.data_access import TEST_DATA

ROOT = TEST_DATA["MODELS"].path


def test_projection_information():
    with xarray.open_dataset(
        str(ROOT / "emep4no20240630" / "Base_hour.nc"), decode_timedelta=True
    ) as ds:
        pi = ProjectionInformation.from_xarray(ds, "SURF_ug_PM10_rh50")
        assert pi is not None
        assert pi.x_axis == "i"
        assert pi.y_axis == "j"
        x0, y0 = float(ds["i"][0]), float(ds["j"][0])
        lon0, lat0 = float(ds["lon"][0, 0]), float(ds["lat"][0, 0])
        (lat, lon) = pi.to_latlon(x0, y0)
        assert lat == approx(lat0, abs=1e-3)
        assert lon == approx(lon0, abs=1e-3)

        x, y = pi.to_proj(lat, lon)
        assert x == approx(x0, abs=1.0)
        assert y == approx(y0, abs=1.0)


def test_projection_snap():
    x = [10, 12, 13]
    y = [60, 61]

    lons, lats = np.meshgrid(x, y)

    field = np.ones_like(lons)

    ds = xarray.Dataset(
        {
            "x": xarray.DataArray(x, coords={"x": x}, attrs={"units": "degrees_east"}),
            "y": xarray.DataArray(y, coords={"y": y}, attrs={"units": "degrees_north"}),
            "lons": xarray.DataArray(lons, dims=["y", "x"], attrs={"units": "degrees_east"}),
            "lats": xarray.DataArray(lats, dims=["y", "x"], attrs={"units": "degrees_north"}),
            "field": xarray.DataArray(
                field,
                dims=["y", "x"],
                attrs={"grid_mapping": "projection", "coordinates": "longitude latitude"},
            ),
            "projection": xarray.DataArray(0, attrs={"grid_mapping_name": "latitude_longitude"}),
        }
    )
    pi = ProjectionInformation.from_xarray(ds, "field")
    assert pi._x_axis == "x"
    assert pi._y_axis == "y"

    # Transform like an identity matrix
    y0, x0 = 11, 61.5
    (lat, lon) = pi.to_latlon(x0, y0)
    assert x0 == approx(lon, abs=1e-3)
    assert y0 == approx(lat, abs=1e-3)
