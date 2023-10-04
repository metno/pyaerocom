"""
This module contains scatter plot routines for Aerocom data.
"""
import matplotlib.pyplot as plt
import numpy as np

from pyaerocom import const
from pyaerocom._warnings import ignore_warnings
from pyaerocom.helpers import start_stop_str
from pyaerocom.mathutils import calc_statistics, exponent


def plot_scatter(x_vals, y_vals, **kwargs):
    """Scatter plot

    Currently a wrapper for high-level method plot_scatter_aerocom (same module,
    see there for details)
    """
    return plot_scatter_aerocom(x_vals, y_vals, **kwargs)


def plot_scatter_aerocom(
    x_vals,
    y_vals,
    var_name=None,
    var_name_ref=None,
    x_name=None,
    y_name=None,
    start=None,
    stop=None,
    ts_type=None,
    unit=None,
    stations_ok=None,
    filter_name=None,
    lowlim_stats=None,
    highlim_stats=None,
    loglog=None,
    ax=None,
    figsize=None,
    fontsize_base=11,
    fontsize_annot=None,
    marker=None,
    color=None,
    alpha=0.5,
    **kwargs,
):
    """Method that performs a scatter plot of data in AEROCOM format

    Parameters
    ----------
    y_vals : ndarray
        1D array (or list) of model data points (y-axis)
    x_vals : ndarray
        1D array (or list) of observation data points (x-axis)
    var_name : :obj:`str`, optional
        name of variable that is plotted
    var_name_ref : :obj:`str`, optional
        name of variable of reference data
    x_name : :obj:`str`, optional
        Name of observation network
    y_name : :obj:`str`, optional
        Name / ID of model
    start : :obj:`str` or :obj`datetime` or similar
        start time of data
    stop : :obj:`str` or :obj`datetime` or similar
        stop time of data
    ts_type : str
        frequency of data
    unit : str, optional
        unit of data
    stations_ok : int, optional
        number of stations from which data were generated
    filter_name : str, optional
        name of filter
    lowlim_stats : float, optional
        lower value considered for statistical parameters
    highlim_stats : float, optional
        upper value considered for statistical parameters
    loglog : bool, optional
        plot log log scale, if None, pyaerocom default is used
    ax : Axes
        axes into which the data are to be plotted
    figsize : tuple
        size of figure (if new figure is created, ie ax is None)
    fontsize_base : int
        basic fontsize, defaults to 11
    fontsize_annot : int, optional
        fontsize used for annotations
    marker : str, optional
        marker used for data, if None, '+' is used
    color : str, optional
        color of markers, default to 'k'
    alpha : float, optional
        transparency of markers (does not apply to all marker types),
        defaults to 0.5.
    **kwargs
        additional keyword args passed to :func:`ax.plot`


    Returns
    -------
    matplotlib.axes.Axes
        plot axes
    """
    if marker is None:
        marker = "+"
    if color is None:
        color = "k"
    if isinstance(y_vals, list):
        y_vals = np.asarray(y_vals)
    if isinstance(x_vals, list):
        x_vals = np.asarray(x_vals)
    try:
        var = const.VARS[var_name]
    except Exception:
        var = const.VARS["DEFAULT"]

    try:
        var_ref = const.VARS[var_name_ref]
    except Exception:
        var_ref = const.VARS["DEFAULT"]

    if loglog is None:
        loglog = var_ref.scat_loglog

    xlim = var["scat_xlim"]
    ylim = var_ref["scat_ylim"]

    if xlim is None or ylim is None:
        low = np.min([np.nanmin(x_vals), np.nanmin(y_vals)])
        high = np.max([np.nanmax(x_vals), np.nanmax(y_vals)])

        xlim = [low, high]
        ylim = [low, high]

    if ax is None:
        if figsize is None:
            figsize = (10, 8)
        fig, ax = plt.subplots(figsize=figsize)
    if var_name is None:
        var_name = "n/d"

    statistics = calc_statistics(y_vals, x_vals, lowlim=lowlim_stats, highlim=highlim_stats)

    if loglog:
        ax.loglog(x_vals, y_vals, ls="none", color=color, marker=marker, alpha=alpha, **kwargs)
    else:
        ax.plot(x_vals, y_vals, ls="none", color=color, marker=marker, alpha=alpha, **kwargs)

    try:
        title = start_stop_str(start, stop, ts_type)
        if ts_type is not None:
            title += f" ({ts_type})"
    except Exception:
        title = ""

    if not loglog:
        xlim[0] = 0
        ylim[0] = 0
    elif any(x[0] < 0 for x in [xlim, ylim]):
        low = np.nanmin(y_vals)
        if low != 0:
            low = 10 ** (float(exponent(abs(low)) - 1))
        xlim[0] = low
        ylim[0] = low
    with ignore_warnings(
        UserWarning,
        "Attempted to set non-positive left xlim on a log-scaled axis",
        "Attempt to set non-positive xlim on a log-scaled axis will be ignored.",
    ):
        ax.set_xlim(xlim)
    with ignore_warnings(
        UserWarning,
        "Attempted to set non-positive bottom ylim on a log-scaled axis",
        "Attempt to set non-positive ylim on a log-scaled axis will be ignored.",
    ):
        ax.set_ylim(ylim)
    xlbl = f"{x_name}"
    if var_name_ref is not None:
        xlbl += f" ({var_name_ref})"
    ax.set_xlabel(xlbl, fontsize=fontsize_base + 4)
    ax.set_ylabel(f"{y_name}", fontsize=fontsize_base + 4)

    ax.set_title(title, fontsize=fontsize_base + 4)

    ax.tick_params(labelsize=fontsize_base)

    ax.plot(xlim, ylim, "--", color="#cccccc")

    xypos = {
        "var_info": (0.01, 0.95),
        "refdata_mean": (0.01, 0.90),
        "data_mean": (0.01, 0.86),
        "nmb": (0.01, 0.82),
        "mnmb": (0.35, 0.82),
        "R": (0.01, 0.78),
        "rms": (0.35, 0.78),
        "R_kendall": (0.01, 0.74),
        "fge": (0.35, 0.74),
        "ts_type": (0.8, 0.1),
        "filter_name": (0.8, 0.06),
    }

    var_str = var_name
    _ndig = abs(exponent(statistics["refdata_mean"]) - 2)
    if unit is None:
        unit = "N/D"
    if not str(unit) in ["1", "no_unit"]:
        var_str += f" [{unit}]"

    if fontsize_annot is None:
        fontsize_annot = fontsize_base
    ax.annotate(
        f"{var_str} #: {statistics['num_valid']} # st: {stations_ok}",
        xy=xypos["var_info"],
        xycoords="axes fraction",
        fontsize=fontsize_annot + 4,
        color="red",
    )

    ax.annotate(
        f"Mean (x-data): {statistics['refdata_mean']:.{_ndig}f}; "
        f"Rng: [{np.nanmin(x_vals):.{_ndig}f}, {np.nanmax(x_vals):.{_ndig}f}]",
        xy=xypos["refdata_mean"],
        xycoords="axes fraction",
        fontsize=fontsize_annot,
        color="red",
    )

    ax.annotate(
        f"Mean (y-data): {statistics['data_mean']:.{_ndig}f}; "
        f"Rng: [{np.nanmin(y_vals):.{_ndig}f}, {np.nanmax(y_vals):.{_ndig}f}]",
        xy=xypos["data_mean"],
        xycoords="axes fraction",
        fontsize=fontsize_annot,
        color="red",
    )

    ax.annotate(
        f"NMB: {statistics['nmb']*100:.1f}%",
        xy=xypos["nmb"],
        xycoords="axes fraction",
        fontsize=fontsize_annot,
        color="red",
    )

    ax.annotate(
        f"MNMB: {statistics['mnmb']*100:.1f}%",
        xy=xypos["mnmb"],
        xycoords="axes fraction",
        fontsize=fontsize_annot,
        color="red",
    )

    ax.annotate(
        f"R (Pearson): {statistics['R']:.3f}",
        xy=xypos["R"],
        xycoords="axes fraction",
        fontsize=fontsize_annot,
        color="red",
    )

    ax.annotate(
        f"RMS: {statistics['rms']:.3f}",
        xy=xypos["rms"],
        xycoords="axes fraction",
        fontsize=fontsize_annot,
        color="red",
    )

    ax.annotate(
        f"R (Kendall): {statistics['R_kendall']:.3f}",
        xy=xypos["R_kendall"],
        xycoords="axes fraction",
        fontsize=fontsize_annot,
        color="red",
    )

    ax.annotate(
        f"FGE: {statistics['fge']:.1f}",
        xy=xypos["fge"],
        xycoords="axes fraction",
        fontsize=fontsize_annot,
        color="red",
    )
    # right lower part
    ax.annotate(
        f"{ts_type}",
        xy=xypos["ts_type"],
        xycoords="axes fraction",
        ha="center",
        fontsize=fontsize_annot,
        color="black",
    )
    ax.annotate(
        f"{filter_name}",
        xy=xypos["filter_name"],
        xycoords="axes fraction",
        ha="center",
        fontsize=fontsize_annot,
        color="black",
    )

    ax.set_aspect("equal")
    return ax
