import cartopy.crs as ccrs
import matplotlib
import matplotlib.pyplot as plt
from cartopy.mpl.geoaxes import GeoAxes
from matplotlib.axes import Axes
from matplotlib.colors import ListedColormap, to_hex
from seaborn import color_palette
import io
import xarray
import pandas as pd
import glob
import os

try:
    from geojsoncontour import contourf_to_geojson
except ModuleNotFoundError:
    contourf_to_geojson = None

from pyaerocom import GriddedData
from pyaerocom.aeroval.coldatatojson_helpers import _get_jsdate
from pyaerocom.helpers import make_datetime_index
from pyaerocom.tstype import TsType


# names of modelmaps type options
CONTOUR = "contour"
OVERLAY = "overlay"


def _jsdate_list(data):
    tst = TsType(data.ts_type)
    if isinstance(data, GriddedData):
        start_yr = data.start
        stop_yr = data.stop
    elif isinstance(data, xarray.DataArray):
        start_yr = pd.Timestamp(data.time.min().values).year
        stop_yr = pd.Timestamp(data.time.max().values).year
    else:
        raise ValueError("data not correct type")
    idx = make_datetime_index(start_yr, stop_yr, tst.to_pandas_freq())
    return _get_jsdate(idx.values).tolist()


def calc_contour_json(data, cmap, cmap_bins):
    """
    Convert gridded data into contours for json output

    Parameters
    ----------
    data : GriddedData
        input data
    cmap : str
        colormap of output
    cmap_bins : list
        list containing the bins to which the values are mapped.

    Returns
    -------
    dict
        dictionary containing contour data

    """
    if contourf_to_geojson is None:
        raise ModuleNotFoundError(
            "Map processing for aeroval interface requires "
            "the geojsoncontour package which is not part of the "
            "standard conda installation of pyaerocom."
        )

    plt.close("all")
    matplotlib.use("Agg")
    GeoAxes._pcolormesh_patched = Axes.pcolormesh

    cm = ListedColormap(color_palette(cmap, len(cmap_bins) - 1))

    proj = ccrs.PlateCarree()
    ax = plt.axes(projection=proj)

    try:
        data.check_dimcoords_tseries()
    except Exception:
        data.reorder_dimensions_tseries()

    nparr = data.cube.data
    lats = data.latitude.points
    lons = data.longitude.points

    geojson = {}
    tst = _jsdate_list(data)
    for i, date in enumerate(tst):
        datamon = nparr[i]
        contour = ax.contourf(
            lons,
            lats,
            datamon,
            transform=proj,
            colors=cm.colors,
            levels=cmap_bins,
            extend="max",
        )

        result = contourf_to_geojson(contourf=contour)

        geojson[str(date)] = eval(result)

    ax.figure.colorbar(contour, ax=ax)
    colors_hex = [to_hex(val) for val in cm.colors]

    geojson["legend"] = {
        "colors": colors_hex,
        "levels": list(cmap_bins),
        "var_name": data.var_name,
        "units": str(data.units),
    }

    plt.close("all")
    return geojson


def plot_overlay_pixel_maps(
    data: xarray.DataArray, cmap: str, cmap_bins: list[float], format: str
):  # pragma: no cover
    plt.close("all")
    matplotlib.use("Agg")
    proj = ccrs.epsg(3857)

    fig, axis = plt.subplots(
        1,
        1,
        subplot_kw=dict(projection=proj),
        figsize=(8, 8),
    )

    data.plot(
        ax=axis,
        transform=ccrs.PlateCarree(),
        add_colorbar=False,
        add_labels=False,
        vmin=cmap_bins[0],
        vmax=cmap_bins[-1],
        cmap=cmap,
    )

    with io.BytesIO() as buffer:  # use buffer memory
        plt.savefig(
            buffer,
            bbox_inches="tight",
            transparent=True,
            format=format,
            pad_inches=0,
        )
        buffer.seek(0)
        image = buffer.getvalue()

    plt.close("all")

    return image


def find_netcdf_files(directory, strings):
    matching_files = []
    # Use glob to find all NetCDF files recursively
    for nc_file in glob.iglob(os.path.join(glob.escape(directory), "**", "*.nc"), recursive=True):
        # Check if all specified strings are in the filename
        if all(s in os.path.basename(nc_file) for s in strings):
            matching_files.append(nc_file)
    return matching_files
