import iris
import numpy as np
import xarray as xr
from cf_units import Unit


def _create_fake_MSCWCtm_data(numval=1, tst=None):
    if tst is None:
        tst = "monthly"
    from pyaerocom import TsType

    tbase = TsType(tst).cf_base_unit

    _lats_fake = np.linspace(30, 82, 10)
    _lons_fake = np.linspace(-25, 90, 15)
    # _time_fake = pd.date_range('2019-01','2019-06', freq=pd_freq)
    _time_fake = np.arange(10)
    timeattrs = {"units": f"{tbase} since 2000-01-01", "calendar": "gregorian"}
    sh = (len(_time_fake), len(_lats_fake), len(_lons_fake))
    _data_fake = numval * np.ones(sh)

    coords = {"time": ("time", _time_fake, timeattrs), "lat": _lats_fake, "lon": _lons_fake}

    dims = ["time", "lat", "lon"]

    arr = xr.DataArray(data=_data_fake, coords=coords, dims=dims)

    return arr


def make_dummy_cube_3D_daily(
    year=2010, daynum=365, lat_range=None, lon_range=None, value=1, dtype=float
):
    if lat_range is None:
        lat_range = (-30, 30)
    if lon_range is None:
        lon_range = (-10, 10)
    lat_res_deg = lon_res_deg = 5
    times = np.arange(daynum)
    startstr = f"days since {year}-01-01 00:00"
    time_unit = Unit(startstr, calendar="gregorian")

    lons = np.arange(lon_range[0] + lon_res_deg / 2, lon_range[1] + lon_res_deg / 2, lon_res_deg)
    lats = np.arange(lat_range[0] + lat_res_deg / 2, lat_range[1] + lat_res_deg / 2, lat_res_deg)

    latdim = iris.coords.DimCoord(
        lats, var_name="lat", standard_name="latitude", circular=False, units=Unit("degrees")
    )

    londim = iris.coords.DimCoord(
        lons, var_name="lon", standard_name="longitude", circular=False, units=Unit("degrees")
    )

    timedim = iris.coords.DimCoord(times, var_name="time", standard_name="time", units=time_unit)

    latdim.guess_bounds()
    londim.guess_bounds()
    vals = np.ones((len(times), len(lats), len(lons))) * value
    dummy = iris.cube.Cube(vals, units="1")

    dummy.add_dim_coord(latdim, 1)
    dummy.add_dim_coord(londim, 2)
    dummy.add_dim_coord(timedim, 0)
    dummy.var_name = "dummy_grid"

    dummy.data = dummy.data.astype(dtype)
    dummy.attributes["ts_type"] = "daily"
    for coord in dummy.coords():
        coord.points = coord.points.astype(dtype)
    return dummy
