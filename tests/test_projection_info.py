from pytest import approx
import xarray
from pyaerocom.projection_information import ProjectionInformation


def test_projection_information():
    with xarray.open_dataset("/home/heikok/tmp/emep4no20240630/Base_hour.nc") as ds:
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
