from typing import Any
import itertools
import cartopy.crs as ccrs
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, to_hex
from seaborn import color_palette
import io
import xarray
import pandas as pd
import glob
import os
import numpy as np
import geojson
import contourpy

from pyaerocom import GriddedData
from pyaerocom.aeroval.coldatatojson_helpers import _get_jsdate
from pyaerocom.helpers import make_datetime_index
from pyaerocom.units.datetime import TsType


# names of modelmaps type options
CONTOUR = "contour"
OVERLAY = "overlay"


def _jsdate_list(data: GriddedData | xarray.DataArray):
    tst = TsType(data.ts_type)
    if isinstance(data, GriddedData):
        start_yr = data.start
        stop_yr = data.stop
    elif isinstance(data, xarray.DataArray):
        start_yr = pd.Timestamp(data.time.min().values).year
        stop_yr = pd.Timestamp(data.time.max().values).year
    else:
        raise ValueError(f"data is of type {type(data)}, expected GriddedData or DataArray.")
    idx = make_datetime_index(start_yr, stop_yr, tst.to_pandas_freq())
    return _get_jsdate(idx.values).tolist()


def _filled_contours_to_geojson_features(
    x, y, z, levels: list[float], properties: list[dict[str, Any]] | None = None
) -> geojson.FeatureCollection:
    """Convert a grid to geojson contours
    Input:
        x: 1D or 2D array
        y: 1D or 2D array
        z: 2D array, can be masked
        levels: cutoffs for the contours. Must be monotonically increasing. Can be ±np.inf
        properties: fed to the Feature of each polygon. Length must be one less than levels
    """
    if len(levels) < 2:
        raise ValueError("Must have at least two levels")

    if properties is None:
        properties = [{} for _ in range(len(levels) - 1)]
    else:
        if len(properties) != len(levels) - 1:
            raise ValueError(
                "properties must be an array of size {len(levels)-1} to match levels (size {len(levels)})"
            )

    contours_generator = contourpy.contour_generator(x=x, y=y, z=z, fill_type="OuterOffset")
    multicontours = contours_generator.multi_filled(levels)

    features = []
    for (level_polygons, level_offsets), prop in zip(multicontours, properties):
        combined_poly = []
        for chunk_polygons, chunk_offsets in zip(level_polygons, level_offsets):
            polygon = []
            for w0, w1 in itertools.pairwise(chunk_offsets):
                polygon.append(chunk_polygons[w0:w1].tolist())

            combined_poly.append(polygon)

        if len(combined_poly) == 0:
            continue
        mp = geojson.MultiPolygon(coordinates=combined_poly, precision=3)
        feature = geojson.Feature(geometry=mp, properties=prop)
        features.append(feature)

    fc = geojson.FeatureCollection(features)
    return fc


def calc_contour_json(data: GriddedData, cmap: str, cmap_bins: list[float]):
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
    cm = ListedColormap(color_palette(cmap, len(cmap_bins) - 1))

    try:
        data.check_dimcoords_tseries()
    except Exception:
        data.reorder_dimensions_tseries()

    nparr = data.cube.data
    lats = data.latitude.points
    lons = data.longitude.points

    colors_hex = [to_hex(val) for val in cm.colors]
    levels = list(cmap_bins)
    titles = [f"{l0}-{l1}" for l0, l1 in itertools.pairwise(levels)]

    # Include a final contour with the same colour as the second to last
    levels = [*levels, np.inf]
    titles = [*titles, f">{cmap_bins[-1]}"]
    colors = [*colors_hex, colors_hex[-1]]

    geojsons = {}
    tst = _jsdate_list(data)
    for i, date in enumerate(tst):
        datamon = nparr[i]

        geojson = _filled_contours_to_geojson_features(
            lons,
            lats,
            datamon,
            levels=levels,
            properties=[
                {"fill": val, "fill-opacity": 0.9, "title": title}
                for val, title in zip(colors, titles)
            ],
        )
        geojsons[str(date)] = geojson

    return geojsons


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
