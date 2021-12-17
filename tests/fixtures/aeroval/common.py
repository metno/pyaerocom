import os
from pathlib import Path

from pyaerocom import GriddedData

from ..._conftest_helpers import make_dummy_cube_3D_daily

TMPDIR = Path("~/tmp/pyatest").expanduser()
AEROVAL_OUT = TMPDIR / "aeroval"
ADD_MODELS_DIR = TMPDIR / "modeldata"

TMPDIR.mkdir(exist_ok=True)
AEROVAL_OUT.mkdir(exist_ok=True)
ADD_MODELS_DIR.mkdir(exist_ok=True)


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


def add_dummy_model_data(var_name, units, ts_type, vert_code, tmpdir, name=None, **kwargs):
    if name is None:
        name = "DUMMY-MODEL"
    outdir = os.path.join(tmpdir, name, "renamed")
    os.makedirs(outdir, exist_ok=True)
    data = make_griddeddata(var_name, units, ts_type, vert_code, name=name, **kwargs)
    data.to_netcdf(out_dir=outdir)
    return outdir
