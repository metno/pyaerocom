from __future__ import annotations

from typing import Type

import cartopy.mpl.geoaxes
import numpy as np
import pytest
from matplotlib.figure import Figure

from pyaerocom import GriddedData
from pyaerocom.colocateddata import ColocatedData
from pyaerocom.exceptions import DataDimensionError
from pyaerocom.plot.config import ColorTheme, get_color_theme
from pyaerocom.plot.mapping import (
    get_cmap_maps_aerocom,
    init_map,
    plot_griddeddata_on_map,
    plot_map_aerocom,
    plot_nmb_map_colocateddata,
    set_map_ticks,
)


@pytest.mark.parametrize(
    "color_theme,vmin,vmax,name",
    [
        (None, None, None, "Blues"),
        (None, -1, 1, "shiftedcmap"),
        (get_color_theme("light"), None, None, "Blues"),
        (get_color_theme("dark"), None, None, "viridis"),
    ],
)
def test_get_cmap_maps_aerocom(color_theme, vmin, vmax, name):
    cmap = get_cmap_maps_aerocom(color_theme, vmin, vmax)
    assert cmap.name == name


def test_set_cmap_ticks():
    ax = init_map()
    ax = set_map_ticks(ax, None, None)
    assert isinstance(ax, cartopy.mpl.geoaxes.GeoAxes)
    xticks = [-90, 0, 90]
    yticks = [-60, 5, 60]
    ax = set_map_ticks(ax, xticks=xticks, yticks=yticks)
    assert list(ax.get_xticks()) == xticks
    assert list(ax.get_yticks()) == yticks


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(),
        dict(projection="PlateCarree"),
        dict(projection="Mercator"),
        dict(projection="Miller"),
        dict(fig=Figure()),
        dict(fix_aspect=True),
        dict(color_theme="dark"),
        dict(color_theme=ColorTheme("dark")),
    ],
)
def test_init_map(kwargs: dict):
    ax = init_map(**kwargs)
    assert isinstance(ax, cartopy.mpl.geoaxes.GeoAxes)


@pytest.mark.parametrize(
    "kwargs,error",
    [
        pytest.param(
            dict(projection="blaaa"),
            "no such projection blaaa",
            id="unknown projection",
        ),
        pytest.param(
            dict(projection=42),
            "Input for projection needs to be instance of cartopy.crs.Projection",
            id="wrong projection",
        ),
    ],
)
def test_init_map_error(kwargs: dict, error: str):

    with pytest.raises(ValueError) as e:
        init_map(**kwargs)
    assert str(e.value) == error


fake_gridded = type("FakeData", (GriddedData,), {"content": dict(_has_latlon_dims=True, ndim=4)})


@pytest.mark.parametrize(
    "data,kwargs",
    [
        (None, dict()),
        (None, dict(add_cbar=False)),
        (None, dict(cbar_levels=[0.2, 0.4, 0.6])),
        (None, dict(cbar_levels=[0.2, 0.6], cmap="Blues")),
        (None, dict(cbar_levels=[0.2, 0.6], add_zero=True)),
        (None, dict(vmin=-0.2, log_scale=True)),
        (None, dict(vmin=-0.2, log_scale=False)),
        (None, dict(vmin=-0.1, log_scale=True, vmax=2, cmap="Reds")),
        (None, dict(discrete_norm=False)),
        (None, dict(vmin=-0.1, discrete_norm=False)),
        ("negval", dict(discrete_norm=False)),
        (None, dict(log_scale=False, add_zero=True)),
        (None, dict(log_scale=False, cmap="viridis")),
        (None, dict(c_over="r", c_under="b")),
        (None, dict(cbar_levels=[0.2, 0.6], c_over="r", c_under="b")),
        (None, dict(cbar_levels=[0.2, 0.6], c_over="r")),
        (None, dict(add_cbar=True, var_name="od550aer", unit="ug")),
        (None, dict(add_cbar=True, cbar_ticks=[0.1, 0.2, 0.3])),
        (None, dict(add_cbar=True, cbar_ticks=[0.1, 0.2, 0.3], cbar_ticks_sci=True)),
    ],
)
@pytest.mark.filterwarnings("ignore:More than 20 figures have been opened:RuntimeWarning")
def test_plot_griddeddata_on_map(
    data_tm5: GriddedData, data: GriddedData | str | None, kwargs: dict
):
    if data is None:
        data = data_tm5
    elif data == "allnan":
        data = data_tm5.copy()
        data.grid.data = data.grid.data * np.nan
    elif data == "negval":
        data = data_tm5.copy()
        data.grid.data[0, 0, 0] = -100
    elif data == "const":
        data = data_tm5.copy()
        data.grid.data[:, :, :] = 1
    val = plot_griddeddata_on_map(data, **kwargs)
    assert isinstance(val, Figure)


@pytest.mark.parametrize(
    "data,args,exception",
    [
        (42, dict(), ValueError),
        (GriddedData(), dict(), DataDimensionError),
        (fake_gridded(), dict(), DataDimensionError),
        (None, dict(ax=42), ValueError),
        (None, dict(cbar_levels=[0.2, 0.4, 0.6], vmin=0.1, vmax=0.2), ValueError),
        ("const", dict(discrete_norm=False), ValueError),
        ("allnan", dict(), ValueError),
    ],
)
@pytest.mark.filterwarnings("ignore:More than 20 figures have been opened:RuntimeWarning")
def test_plot_griddeddata_on_map_error(
    data_tm5: GriddedData, data: GriddedData | str | None, args: dict, exception: Type[Exception]
):
    if data is None:
        data = data_tm5
    elif data == "allnan":
        data = data_tm5.copy()
        data.grid.data = data.grid.data * np.nan
    elif data == "negval":
        data = data_tm5.copy()
        data.grid.data[0, 0, 0] = -100
    elif data == "const":
        data = data_tm5.copy()
        data.grid.data[:, :, :] = 1
    with pytest.raises(exception) as e:
        val = plot_griddeddata_on_map(data, **args)
        assert isinstance(val, Figure)


@pytest.mark.parametrize(
    "region",
    [
        "WORLD",
        "EUROPE",
        pytest.param(
            "EEUROPE",
            marks=pytest.mark.filterwarnings("ignore:Out of bound index found:DeprecationWarning"),
        ),
    ],
)
def test_plot_map_aerocom(data_tm5: GriddedData, region: str):
    val = plot_map_aerocom(data_tm5, region)
    assert isinstance(val, Figure)


def test_plot_map_aerocom_error():
    with pytest.raises(ValueError):
        plot_map_aerocom(42, "WORLD")


def test_plot_nmb_map_colocateddata(coldata_tm5_aeronet: ColocatedData):
    val = plot_nmb_map_colocateddata(coldata_tm5_aeronet)
    assert isinstance(val, cartopy.mpl.geoaxes.GeoAxes)


def test_plot_nmb_map_colocateddata4D(coldata_tm5_tm5: ColocatedData):
    val = plot_nmb_map_colocateddata(coldata_tm5_tm5)
    assert isinstance(val, cartopy.mpl.geoaxes.GeoAxes)


@pytest.mark.parametrize(
    "key,exception,error",
    [
        pytest.param(
            "fake_5d",
            DataDimensionError,
            "only 3D or 4D colocated data objects are supported",
            id="5d",
        ),
        pytest.param(
            "fake_nodims",
            AssertionError,
            "",
            id="nodims",
        ),
    ],
)
def test_plot_nmb_map_colocateddataFAIL(coldata, key: str, exception: Type[Exception], error: str):
    data = coldata[key]
    with pytest.raises(exception) as e:
        plot_nmb_map_colocateddata(data)
    assert str(e.value) == error
