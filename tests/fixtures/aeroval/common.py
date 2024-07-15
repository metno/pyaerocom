from __future__ import annotations

from pathlib import Path

import iris
import numpy as np
from cf_units import Unit

from pyaerocom import GriddedData

# to make things work from iris 3.8
iris.FUTURE.save_split_attrs = True


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


def make_griddeddata(var_name, units, ts_type, vert_code, name, **kwargs) -> GriddedData:
    cube = make_dummy_cube_3D_daily(**kwargs)
    cube.var_name = var_name
    cube.units = units

    data = GriddedData(cube)
    data.metadata["data_id"] = name
    data.metadata["vert_code"] = vert_code
    if ts_type != "daily":
        data = data.resample_time(ts_type)
    return data


def add_dummy_model_data(
    var_name, units, ts_type, vert_code, tmp_path: str | Path, name=None, **kwargs
) -> str:
    if name is None:
        name = "DUMMY-MODEL"
    if isinstance(tmp_path, str):
        tmp_path = Path(tmp_path)

    out_path = tmp_path / name / "renamed"
    out_path.mkdir(exist_ok=True, parents=True)
    data = make_griddeddata(var_name, units, ts_type, vert_code, name=name, **kwargs)
    data.to_netcdf(out_dir=out_path)
    return str(out_path)
