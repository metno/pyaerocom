import warnings
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
from geonum.helpers import shifted_color_map
from matplotlib.colors import BoundaryNorm, LogNorm, Normalize
from numpy import ceil, linspace, meshgrid
from pandas import to_datetime

from pyaerocom._warnings import ignore_warnings
from pyaerocom.exceptions import DataDimensionError
from pyaerocom.mathutils import exponent
from pyaerocom.plot.config import COLOR_THEME, MAP_AXES_ASPECT, ColorTheme
from pyaerocom.plot.helpers import (
    calc_figsize,
    calc_pseudolog_cmaplevels,
    custom_mpl,
    projection_from_str,
)
from pyaerocom.region import Region

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="pyaerocom")
    MPL_PARAMS = custom_mpl()


def get_cmap_maps_aerocom(color_theme=None, vmin=None, vmax=None):
    """Get colormap using pyAeroCom color scheme

    Parameters
    ----------
    color_theme : :ColorTheme, optional
        instance of pyaerocom color theme. If None, the default schemes is used
    vmin : float, optional
        lower end of value range (only considered for diverging color maps
        with non-symmetric mapping)
    vmax : float, optional
        upper end of value range only considered for diverging color maps
        with non-symmetric mapping)

    Returns
    -------
    colormap
    """
    warnings.warn(
        "matplotlib based plotting is no longer directly supported. This function may be removed in future versions.",
        DeprecationWarning,
    )

    if color_theme is None:
        color_theme = COLOR_THEME
    if vmin is not None and vmax is not None and vmin < 0 and vmax > 0:
        cmap = plt.get_cmap(color_theme.cmap_map_div)
        if color_theme.cmap_map_div_shifted:
            cmap = shifted_color_map(vmin, vmax, cmap)
        return cmap
    return plt.get_cmap(color_theme.cmap_map)


def set_map_ticks(ax, xticks=None, yticks=None):
    """Set or update ticks in instance of GeoAxes object (cartopy)

    Parameters
    ----------
    ax : cartopy.GeoAxes
        map axes instance
    xticks : iterable, optional
        ticks of x-axis (longitudes)
    yticks : iterable, optional
        ticks of y-axis (latitudes)

    Returns
    -------
    cartopy.GeoAxes
        modified axes instance
    """
    warnings.warn(
        "matplotlib based plotting is no longer directly supported. This function may be removed in future versions.",
        DeprecationWarning,
    )
    lonleft, lonright = ax.get_xlim()
    digits = 2 - exponent(lonleft)
    digits = 0 if digits < 0 else digits
    tick_format = f".{digits:d}f"
    if xticks is None:
        num_lonticks = 7 if lonleft == -lonright else 6
        xticks = linspace(lonleft, lonright, num_lonticks)
    if yticks is None:
        latleft, latright = ax.get_ylim()
        num_latticks = 7 if latleft == -latright else 6
        yticks = linspace(latleft, latright, num_latticks)
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())

    lon_formatter = LongitudeFormatter(
        number_format=tick_format, degree_symbol="", dateline_direction_label=True
    )
    lat_formatter = LatitudeFormatter(number_format=tick_format, degree_symbol="")

    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    return ax


def init_map(
    xlim=(-180, 180),
    ylim=(-90, 90),
    figh=8,
    fix_aspect=False,
    xticks=None,
    yticks=None,
    color_theme=COLOR_THEME,
    projection=None,
    title=None,
    gridlines=False,
    fig=None,
    ax=None,
    draw_coastlines=True,
    contains_cbar=False,
):
    """Initalise a map plot

    Parameters
    ----------
    xlim : tuple
        2-element tuple specifying plotted longitude range
    ylim : tuple
        2-element tuple specifying plotted latitude range
    figh : int
        height of figure in inches
    fix_aspect : bool, optional
        if True, the aspect of the GeoAxes instance is kept fix using the
        default aspect ``MAP_AXES_ASPECT`` defined in
        :mod:`pyaerocom.plot.config`
    xticks : iterable, optional
        ticks of x-axis (longitudes)
    yticks : iterable, optional
        ticks of y-axis (latitudes)
    color_theme : ColorTheme
        pyaerocom color theme.
    projection
        projection instance from cartopy.crs module (e.g. PlateCaree). May also
        be string.
    title : str, optional
        title that is supposed to be inserted
    gridlines : bool
        whether or not to add gridlines to the map
    fig : matplotlib.figure.Figure, optional
        instance of matplotlib Figure class. If specified, the former to
        input args (``figh`` and ``fix_aspect``) are ignored. Note that the
        Figure is wiped clean before plotting, so any plotted content will be
        lost
    ax : GeoAxes, optional
        axes in which the map is plotted
    draw_coastlines : bool
        whether or not to draw coastlines
    contains_cbar : bool
        whether or not a colorbar is intended to be added to the figure (
        impacts the aspect ratio of the figure).

    Returns
    -------
    ax : cartopy.mpl.geoaxes.GeoAxes
        axes instance
    """
    warnings.warn(
        "matplotlib based plotting is no longer directly supported. This function may be removed in future versions.",
        DeprecationWarning,
    )
    if projection is None:
        projection = ccrs.PlateCarree()
    elif isinstance(projection, str):
        projection = projection_from_str(projection)
    elif not isinstance(projection, ccrs.Projection):
        raise ValueError("Input for projection needs to be instance of cartopy.crs.Projection")

    if not isinstance(ax, GeoAxes):
        if fig is None:
            if not fix_aspect:
                figsize = calc_figsize(xlim, ylim)
            else:
                figw = figh * fix_aspect
                figsize = (figw, figh)

            fig = plt.figure(figsize=figsize)
        else:
            fig.clf()
        if contains_cbar:
            ax = fig.add_axes([0.1, 0.12, 0.75, 0.8], projection=projection)
        else:
            ax = fig.add_axes([0.1, 0.12, 0.85, 0.8], projection=projection)

    if fix_aspect:
        ax.set_aspect(MAP_AXES_ASPECT)

    if not isinstance(color_theme, ColorTheme):
        if isinstance(color_theme, str):
            color_theme = ColorTheme(color_theme)
        else:
            color_theme = COLOR_THEME

    if draw_coastlines:
        ax.coastlines(color=color_theme.color_coastline)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    ax = set_map_ticks(ax, xticks, yticks)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    if title is not None:
        ax.set_title(title)
    if gridlines:
        ax.gridlines()

    return ax


def plot_griddeddata_on_map(
    data,
    lons=None,
    lats=None,
    var_name=None,
    unit=None,
    xlim=(-180, 180),
    ylim=(-90, 90),
    vmin=None,
    vmax=None,
    add_zero=False,
    c_under=None,
    c_over=None,
    log_scale=True,
    discrete_norm=True,
    cbar_levels=None,
    cbar_ticks=None,
    add_cbar=True,
    cmap=None,
    cbar_ticks_sci=False,
    color_theme=None,
    ax=None,
    ax_cbar=None,
    **kwargs,
):
    """Make a plot of gridded data onto a map

    Parameters
    ----------
    data : ndarray
        2D data array
    lons : ndarray
        longitudes of data
    lats : ndarray
        latitudes of data
    var_name : :obj:`str`, optional
        name of variable that is plotted
    xlim : tuple
        2-element tuple specifying plotted longitude range
    ylim : tuple
        2-element tuple specifying plotted latitude range
    vmin : :obj:`float`, optional
        lower value of colorbar range
    vmax : :obj:`float`, optional
        upper value of colorbar range
    add_zero : bool
        if True and vmin is not 0, then, the colorbar is extended down to 0.
        This may be used, e.g. for logarithmic scales that should include 0.
    c_under : :obj:`float`, optional
        colour of data values smaller than ``vmin``
    c_over : :obj:`float`, optional
        colour of data values exceeding ``vmax``
    log_scale : bool
        if True, the value to color mapping is done in a pseudo log scale
        (see :func:`get_cmap_levels_auto` for implementation)
    discrete_norm : bool
        if True, color mapping will be subdivided into discrete intervals
    cbar_levels : iterable, optional
        discrete colorbar levels. Will be computed automatically, if None
        (and applicable)
    cbar_ticks : iterable, optional
        ticks of colorbar levels. Will be computed automatically, if None
        (and applicable)

    Returns
    -------
    fig
        matplotlib figure instance containing plot result. Use
        ``fig.axes[0]`` to access the map axes instance (e.g. to modify the
        title or lon / lat range, etc.)
    """
    warnings.warn(
        "matplotlib based plotting is no longer directly supported. This function may be removed in future versions.",
        DeprecationWarning,
    )
    if color_theme is None:
        color_theme = COLOR_THEME
    if add_cbar:
        kwargs["contains_cbar"] = True
    if ax is None:
        ax = init_map(xlim, ylim, color_theme=color_theme, **kwargs)
    if not isinstance(ax, GeoAxes):
        raise ValueError("Invalid input for ax, need GeoAxes")
    fig = ax.figure

    from pyaerocom.griddeddata import GriddedData

    if not isinstance(data, GriddedData):
        raise ValueError("need GriddedData")

    if not data.has_latlon_dims:
        raise DataDimensionError("Input data needs to have latitude and longitude dimension")
    if not data.ndim == 2:
        if not data.ndim == 3 or "time" not in data.dimcoord_names:
            raise DataDimensionError(
                "Input data needs to be 2 dimensional "
                "or 3D with time being the 3rd "
                "dimension"
            )
        data.reorder_dimensions_tseries()
        data = data[0]

    lons = data.longitude.points
    lats = data.latitude.points
    data = data.grid.data

    if add_cbar and ax_cbar is None:
        ax_cbar = _add_cbar_axes(ax)

    X, Y = meshgrid(lons, lats)

    bounds = None
    if cbar_levels is not None:  # user provided levels of colorbar explicitely
        if vmin is not None or vmax is not None:
            raise ValueError("Please provide either vmin/vmax OR cbar_levels")
        bounds = list(cbar_levels)
        low, high = bounds[0], bounds[-1]
        if add_zero and low > 0:
            bounds.insert(0, 0)  # insert zero bound
        if cmap is None:
            cmap = get_cmap_maps_aerocom(color_theme, low, high)
        elif isinstance(cmap, str):
            cmap = plt.get_cmap(cmap)
        norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N, clip=False)
    else:
        with ignore_warnings(RuntimeWarning, "All-NaN axis encountered"):
            dmin = np.nanmin(data)
            dmax = np.nanmax(data)

        if any([np.isnan(x) for x in [dmin, dmax]]):
            raise ValueError("Cannot plot map of data: all values are NaN")
        elif dmin == dmax:
            raise ValueError(f"Minimum value in data equals maximum value: {dmin}")
        if vmin is None:
            vmin = dmin
        else:
            if vmin < 0 and log_scale:
                log_scale = False
        if vmax is None:
            vmax = dmax
        if exponent(vmin) == exponent(vmax):
            log_scale = False
        if log_scale:  # no negative values allowed
            if vmin < 0:
                vmin = data[data > 0].min()
                if (
                    c_under is None
                ):  # special case, set c_under to indicate that there is values below 0
                    c_under = "r"
            if cmap is None:
                cmap = get_cmap_maps_aerocom(color_theme, vmin, vmax)
            elif isinstance(cmap, str):
                cmap = plt.get_cmap(cmap)
            if discrete_norm:
                # to compute upper range of colour range, round up vmax
                exp = float(exponent(vmax) - 1)
                vmax_colors = ceil(vmax / 10**exp) * 10**exp
                bounds = calc_pseudolog_cmaplevels(vmin=vmin, vmax=vmax_colors, add_zero=add_zero)
                norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N, clip=False)

            else:
                norm = LogNorm(vmin=vmin, vmax=vmax, clip=True)
        else:
            if add_zero and vmin > 0:
                vmin = 0
            if cmap is None:
                cmap = get_cmap_maps_aerocom(color_theme, vmin, vmax)
            elif isinstance(cmap, str):
                cmap = plt.get_cmap(cmap)
            if discrete_norm:
                bounds = np.linspace(vmin, vmax, 10)
                norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N, clip=False)
            else:
                norm = Normalize(vmin=vmin, vmax=vmax)
    cbar_extend = "neither"
    if c_under is not None:
        cmap = cmap.copy()
        cmap.set_under(c_under)
        cbar_extend = "min"
        if bounds is not None:
            bounds.insert(0, bounds[0] - bounds[1])
    if c_over is not None:
        cmap = cmap.copy()
        cmap.set_over(c_over)
        if bounds is not None:
            bounds.append(bounds[-1] + bounds[-2])
        if cbar_extend == "min":
            cbar_extend = "both"
        else:
            cbar_extend = "max"
    fig.norm = norm
    disp = ax.pcolormesh(X, Y, data, cmap=cmap, norm=norm, shading="auto")

    if add_cbar:
        cbar = fig.colorbar(disp, extend=cbar_extend, cax=ax_cbar, shrink=0.8)
        fig.cbar = cbar

        if var_name is not None:
            var_str = var_name  # + VARS.unit_str
            if unit is not None:
                if str(unit) not in ["1", "no_unit"]:
                    var_str += f" [{unit}]"

            cbar.set_label(var_str)

        if cbar_ticks:
            cbar.set_ticks(cbar_ticks)
        if cbar_ticks_sci:
            lbls = []
            for lbl in cbar.ax.get_yticklabels():
                tstr = lbl.get_text()
                if bool(tstr):
                    lbls.append(f"{float(tstr):.1e}")
                else:
                    lbls.append("")
            cbar.ax.set_yticklabels(lbls)

    return fig


def _add_cbar_axes(ax):  # , where='right'):
    _loc = ax.bbox._bbox
    fig = ax.figure

    ax_cbar = fig.add_axes([_loc.x1 + 0.02, _loc.y0, 0.02, _loc.y1 - _loc.y0])
    return ax_cbar


def plot_map_aerocom(data, region, **kwargs):
    """High level map plotting function for Aerocom default plotting

    Note
    ----
    This function does not iterate over a cube in time, but uses the
    first available time index in the data.

    Parameters
    ----------
    data : GriddedData
        input data from one timestamp (if data contains more than one time
        stamp, the first index is used)
    region : str or Region
        valid region ID or region

    """
    warnings.warn(
        "matplotlib based plotting is no longer directly supported. This function may be removed in future versions.",
        DeprecationWarning,
    )
    from pyaerocom import GriddedData

    if not isinstance(data, GriddedData):
        raise ValueError(
            "This plotting method needs an instance of pyaerocom "
            f"GriddedData on input, got: {type(data)}"
        )

    if isinstance(region, str):
        region = Region(region)
    elif not isinstance(region, Region):
        raise ValueError("Invalid input for region, need None, str or Region")

    data = data.filter_region(region.region_id)
    s = data.plot_settings

    vmin, vmax, levs = s.map_vmin, s.map_vmax, None
    if isinstance(s.map_cbar_levels, list) and len(s.map_cbar_levels) > 0:
        vmin, vmax = None, None
        levs = s.map_cbar_levels
    fig = plot_griddeddata_on_map(
        data,
        xlim=region.lon_range_plot,
        ylim=region.lat_range_plot,
        vmin=vmin,
        vmax=vmax,
        c_over=s.map_c_over,
        c_under=s.map_c_under,
        cbar_levels=levs,
        xticks=region.lon_ticks,
        yticks=region.lat_ticks,
        cbar_ticks=s.map_cbar_ticks,
        **kwargs,
    )
    ax = fig.axes[0]

    # annotate model in lower left corner
    lonr, latr = region.lon_range_plot, region.lat_range_plot
    ax.annotate(
        data.data_id,
        xy=(lonr[0] + (lonr[1] - lonr[0]) * 0.03, latr[0] + (latr[1] - latr[0]) * 0.03),
        xycoords="data",
        horizontalalignment="left",
        color="black",
        fontsize=MPL_PARAMS["axes.titlesize"] + 2,
        bbox=dict(boxstyle="square", facecolor="white", edgecolor="none", alpha=0.7),
    )
    ax.annotate(
        "source: AEROCOM",
        xy=(0.97, 0.03),
        xycoords="figure fraction",
        horizontalalignment="right",
        fontsize=MPL_PARAMS["xtick.labelsize"],
        bbox=dict(boxstyle="square", facecolor="none", edgecolor="black"),
    )

    var = data.var_name.upper()
    avg = data.mean()
    start = to_datetime(data.start).strftime("%Y%m%d")
    tit = f"{var} {start} mean {avg.round(3)}"
    ax.set_title(tit)
    return fig


def plot_nmb_map_colocateddata(
    coldata,
    in_percent=True,
    vmin=-100,
    vmax=100,
    cmap=None,
    s=80,
    marker=None,
    step_bounds=None,
    add_cbar=True,
    norm=None,
    cbar_extend=None,
    add_mean_edgecolor=True,
    ax=None,
    ax_cbar=None,
    cbar_outline_visible=False,
    cbar_orientation=None,
    ref_label=None,
    stats_area_weighted=False,
    **kwargs,
):
    """Plot map of normalised mean bias from instance of ColocatedData

    Parameters
    ----------
    coldata : ColocatedData
        data object
    in_percent : bool
        plot bias in percent
    vmin : int
        minimum value of colormapping
    vmax : int
        maximum value of colormapping
    cmap : str or cmap
        colormap used, defaults to bwr
    s : int
        size of marker
    marker : str
        marker used
    step_bounds : int, optional
        step used for discrete colormapping (if None, continuous is used)
    cbar_extend : str
        extend colorbar
    ax : GeoAxes, optional
        axes into which the bias is supposed to be plotted
    ax_cbar : plt.Axes, optional
        axes for colorbar
    cbar_outline_visible : bool
        if False, borders of colorbar are removed
    cbar_orientation : str
        e.g. 'vertical', defaults to 'vertical'
    **kwargs
        keyword args passed to :func:`init_map`

    Returns
    -------
    GeoAxes
    """
    warnings.warn(
        "matplotlib based plotting is no longer directly supported. This function may be removed in future versions.",
        DeprecationWarning,
    )
    if cbar_extend is None:
        cbar_extend = "both"
    if cbar_orientation is None:
        cbar_orientation = "vertical"
    if cmap is None:
        cmap = "bwr"
    if marker is None:
        marker = "o"
    try:
        mec = kwargs.pop("mec")
    except KeyError:
        try:
            mec = kwargs.pop("markeredgecolor")
        except KeyError:
            mec = "face"

    try:
        mew = kwargs.pop("mew")
    except KeyError:
        mew = 1
    if coldata.ndim not in (3, 4):
        raise DataDimensionError("only 3D or 4D colocated data objects are supported")
    assert "time" in coldata.dims

    mean_bias = coldata.calc_nmb_array()

    if mean_bias.ndim == 1:
        (lats, lons, data) = mean_bias.latitude, mean_bias.longitude, mean_bias.data
    elif "latitude" in mean_bias.dims and "longitude" in mean_bias.dims:
        stacked = mean_bias.stack(latlon=["latitude", "longitude"])
        valid = ~stacked.isnull()
        coords = stacked.latlon[valid].values
        lats, lons = list(zip(*list(coords)))
        data = stacked.data[tuple(valid)]

    if ref_label is None:
        ref_label = coldata.metadata["data_source"][0]

    if in_percent:
        data *= 100
    if ax is None:
        ax = init_map(contains_cbar=True, **kwargs)

    if not isinstance(ax, GeoAxes):
        raise TypeError("Input axes need to be instance of cartopy.GeoAxes")

    fig = ax.figure

    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
    if norm is None and step_bounds is not None:
        bounds = np.arange(vmin, vmax + step_bounds, step_bounds)
        norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N, clip=False)

    if add_mean_edgecolor:
        nn = Normalize(vmin=vmin, vmax=vmax)
        nmb = coldata.calc_statistics(use_area_weights=stats_area_weighted)["nmb"]
        if in_percent:
            nmb *= 100
        ec = cmap(nn(nmb))
    else:
        ec = mec
    _sc = ax.scatter(
        lons,
        lats,
        c=data,
        marker=marker,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        s=s,
        norm=norm,
        label=ref_label,
        edgecolors=ec,
        linewidths=mew,
    )
    if add_cbar:
        if ax_cbar is None:
            ax_cbar = _add_cbar_axes(ax)
        cbar = fig.colorbar(_sc, extend=cbar_extend, cax=ax_cbar, orientation=cbar_orientation)

        cbar.outline.set_visible(cbar_outline_visible)
        cbar.set_label("NMB [%]")

    return ax
