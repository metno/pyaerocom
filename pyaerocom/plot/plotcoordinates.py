import warnings
import cartopy

from pyaerocom.plot.mapping import init_map


def plot_coordinates(
    lons,
    lats,
    xlim=None,
    ylim=None,
    label=None,
    legend=True,
    color=None,
    marker=None,
    markersize=8,
    ax=None,
    **kwargs,
):
    """Plot input coordinates on a map

    lons : ndarray
        array of longitude coordinates (can also be list or tuple)
    lats : ndarray
        array of latitude coordinates (can also be list or tuple)
    xlim : tuple
        longitude range
    ylim : tuple
        latitude range
    label : str, optional
        label of data
    legend : bool
        whether or not to display a legend, defaults to True.
    color : str, optional
        color of markers, defaults to red
    marker : str, optional
        marker shape, defaults to 'o'
    markersize : int
        size of markers
    ax : GeoAxes
        axes instance to be plotted into
    **kwargs
        additional keyword args passed on to :func:`init_map`

    Returns
    -------
    GeoAxes

    """
    warnings.warn(
        "matplotlib based plotting is no longer directly supported. This function may be removed in future versions.",
        DeprecationWarning,
    )

    if xlim is None:
        xlim = (-180, 180)
    if ylim is None:
        ylim = (-90, 90)
    if color is None:
        color = "r"
    if marker is None:
        marker = "o"

    if not isinstance(ax, cartopy.mpl.geoaxes.GeoAxes):
        ax = init_map(xlim, ylim, ax=ax, **kwargs)

    if label is None:
        label = f"{len(lons)} stations"

    ax.scatter(lons, lats, markersize, marker=marker, color=color, label=label)

    if legend and label:
        ax.legend()

    return ax
