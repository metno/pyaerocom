import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from seaborn import heatmap

from pyaerocom.mathutils import exponent


def _format_annot_heatmap(annot, annot_fmt_rows, annot_fmt_exceed):
    """
    Process annotation formatting info for :func:`df_to_heatmap`

    Parameters
    ----------
    annot : ndarray
        2D pre-existing annotation information.
    annot_fmt_rows : list
        annotation formatting strings for each row of the input table. This
        parameter is only considered if `annot_fmt_rowwise` is True. See also
        :func:`_format_annot_heatmap`.
    annot_fmt_exceed : list, optional
        how to format annotated values that exceed a certain threshold.
        The list contains 2 entries, 1. the threshold values, 2. how values
        exceeding this threshold should be formatted. .

    Returns
    -------
    ndarray
        updated annotation information (input `annot`)
    list
        row formatting info.


    """
    _annot = []
    if not isinstance(annot_fmt_rows, list):
        annot_fmt_rows = []
        for row in annot:
            mask = row[~np.isnan(row)]
            if len(mask) == 0:  # all NaN
                annot_fmt_rows.append("")
                continue
            mask = mask[mask != 0]
            exps = exponent(mask)
            minexp = exps.min()
            if minexp < -3:
                annot_fmt_rows.append(".1E")
            elif minexp < 0:
                annot_fmt_rows.append(f".{-minexp + 1}f")
            elif minexp in [0, 1]:
                annot_fmt_rows.append(".1f")
            else:
                annot_fmt_rows.append(".0f")
    if isinstance(annot_fmt_exceed, list):
        exceed_val, exceed_fmt = annot_fmt_exceed
    else:
        exceed_val, exceed_fmt = None, None

    for i, row in enumerate(annot):
        rowfmt = annot_fmt_rows[i]
        if rowfmt == "":
            row_fmt = [""] * len(row)
        else:
            row_fmt = []
            for val in row:
                if np.isnan(val):
                    valstr = ""
                else:
                    if exceed_val is not None and val > exceed_val:
                        valstr = format(val, exceed_fmt)
                    else:
                        valstr = format(val, rowfmt)

                row_fmt.append(valstr)
        _annot.append(row_fmt)
    annot = np.asarray(_annot)
    return annot, annot_fmt_rows


def df_to_heatmap(
    df,
    cmap=None,
    center=None,
    low=0.3,
    high=0.3,
    vmin=None,
    vmax=None,
    color_rowwise=False,
    normalise_rows=False,
    normalise_rows_how=None,
    normalise_rows_col=None,
    norm_ref=None,
    sub_norm_before_div=True,
    annot=True,
    num_digits=None,
    ax=None,
    figsize=(12, 12),
    cbar=False,
    cbar_label=None,
    cbar_labelsize=None,
    xticklabels=None,
    xtick_rot=45,
    yticklabels=None,
    ytick_rot=45,
    xlabel=None,
    ylabel=None,
    title=None,
    labelsize=12,
    annot_fontsize=None,
    annot_fmt_rowwise=False,
    annot_fmt_exceed=None,
    annot_fmt_rows=None,  # explicit formatting strings for rows
    cbar_ax=None,
    cbar_kws=None,
    **kwargs,
):
    """Plot a pandas dataframe as heatmap

    Parameters
    ----------
    df : DataFrame
        table data
    cmap : str, optional
        string specifying colormap to be used
    center : float, optional
        value that is mapped to center colour of colormap (e.g. 0)
    low : float, optional
        Extends lower range of the table values so that when mapped to  the
        colormap, it’s entire range isn’t used. E.g. 0.3 roughly corresponds
        to colormap crop of 30% at the lower end.
    high : float, optional
        Extends upper range of the table values so that when mapped to the
        colormap, it’s entire range isn’t used. E.g. 0.3 roughly corresponds
        to colormap crop of 30% at the upper end.
    vmin : float, optional
        lower end of value range to be plotted. If specified, input arg `low`
        will be ignored.
    vmax : float, optional
        upper end of value range to be plotted. If specified, input arg `low`
        will be ignored.
    color_rowwise : bool, optional
        if True, the color mapping is applied row by row, else, for the whole
        table. Defaults to False.
    normalise_rows : bool, optional
        if True, the table is normalised in a rowwise manner either using the
        mean value in each row (if argument ``normalise_rows_col`` is
        unspecified) or using the value in a specified column. Defaults to
        False.
    normalise_rows_how : str, optional
        aggregation string for row normalisation. Choose from mean or median.
        Only relevant if input arg ``normalise_rows==True``.
    normalise_rows_col : int, optional
        if provided and if arg. ``normalise_rows==True``, then the
        corresponding table column is used for normalisation rather than
        the mean value of each row.
    norm_ref : float or ndarray, optional
        reference value(s) used for rowwise normalisation. Only relevant if
        normalise_rows is True. If specified, normalise_rows_how and
        normalise_rows_col will be ignored.
    sub_norm_before_div : bool, optional
        if True, the rowwise normilisation is applied by subtracting the
        normalisation value for each row before dividing by it. This can be
        useful to visualise positive or negative departures from the mean or
        median.
    annot : bool or list or ndarray, optional
        if True, the table values are printed into the heatmap. Defaults to
        True, in which case the values are computed based on the table content.
        If list or ndarray, the shape needs to be the same as input table shape
        (no of rows and cols), in which case the values of that 2D frame are
        used.
    num_digits : int, optional
        number of digits printed in heatmap annotation.
    ax : axes, optional
        matplotlib axes instance used for plotting, if None, an axes will be
        created
    figsize : tuple, optional
        size of figure for plot
    cbar : bool, optional
        if True, a colorbar is included
    cbar_label : str, optional
        label of colorbar (if colorbar is included, see cbar option)
    cbar_labelsize : int, optional
        size of colorbar label
    xticklabels : list, optional
        List of x axis labels.
    xtick_rot : int, optional
        rotation of x axis labels, defaults to 45 degrees.
    yticklabels : list, optional
        List of string labels.
    ytick_rot : int, optional
        rotation of y axis labels, defaults to 45 degrees.
    xlabel : str, optional
        x axis label
    ylabel : str, optional
        y axis label
    title : str, optional
        title of heatmap
    labelsize : int, optional
        fontsize of labels, default to 12
    annot_fontsize : int, optional
        fontsize of annotated text.
    annot_fmt_rowwise : bool
        rowwise formatting of annotation values, based on row value ranges.
        Defaults to False.
    annot_fmt_exceed : list, optional
        how to format annotated values that exceed a certain threshold.
        The list contains 2 entries, 1. the threshold values, 2. how values
        exceeding this thrshold should be formatted. This parameter is only
        considered if `annot_fmt_rowwise` is True. See also
        :func:`_format_annot_heatmap`.
    annot_fmt_rows : list
        annotation formatting strings for each row of the input table. This
        parameter is only considered if `annot_fmt_rowwise` is True. See also
        :func:`_format_annot_heatmap`.
    cbar_ax : Axes, optional
        axes instance for colorbar, parsed to :func:`seaborn.heatmap`.
    cbar_kws : dict, optional
        keywords for colorbar formatting, , parsed to :func:`seaborn.heatmap`.
    **kwargs
        further keyword args parsed to :func:`seaborn.heatmap`

    Raises
    ------
    ValueError
        if input `annot` is list or ndarray and has a different shape than
        the input `df`.

    Returns
    -------
    Axes
        plot axes instance
    list or None
        annotation information for rows

    """
    if cmap is None:
        cmap = "bwr"
    if cbar_label is None:
        cbar_label = ""
    if normalise_rows_how is None:
        normalise_rows_how = "median"

    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=figsize)
    if cbar_kws is None:
        cbar_kws = {}
    if annot_fontsize is None:
        annot_fontsize = labelsize - 4
    if not "annot_kws" in kwargs:
        kwargs["annot_kws"] = {}
    kwargs["annot_kws"]["size"] = annot_fontsize
    df_hm = df
    if normalise_rows:
        if norm_ref is None:
            if normalise_rows_col is not None:
                if isinstance(normalise_rows_col, str):
                    try:
                        normalise_rows_col = df.columns.to_list().index(normalise_rows_col)
                    except ValueError:
                        raise ValueError(f"Failed to localise column {normalise_rows_col}")
                norm_ref = df.values[:, normalise_rows_col]
            else:
                if normalise_rows_how == "mean":
                    norm_ref = df.mean(axis=1)
                elif normalise_rows_how == "median":
                    norm_ref = df.median(axis=1)
                else:
                    raise ValueError(
                        f"Invalid input for normalise_rows_how ({normalise_rows_how}). "
                        f"Choose mean or median"
                    )

        if sub_norm_before_div:
            df_hm = df.subtract(norm_ref, axis=0).div(norm_ref, axis=0)
        else:
            df_hm = df.div(norm_ref, axis=0)
        cbar_kws["format"] = FuncFormatter(lambda x, pos: f"{x:.0%}")

    if color_rowwise:
        df_hm = df_hm.div(abs(df_hm).max(axis=1), axis=0)

    cbar_kws["label"] = cbar_label

    if "norm" in kwargs:
        norm = kwargs["norm"]
        vmin = norm.boundaries[0]
        vmax = norm.boundaries[-1]
    else:
        if vmin is None:
            vmin = df_hm.min().min()  # * (1 - low)
        if vmax is None:
            vmax = df_hm.max().max()  # * (1 + high)
        vmin -= abs(vmin) * low
        vmax += abs(vmax) * high

    if annot is True:
        annot = df.values
    elif isinstance(annot, list):
        annot = np.asarray(annot)
    else:
        fmt = ""

    if isinstance(annot, np.ndarray):
        if not annot.shape == df.values.shape:
            raise ValueError(
                "Invalid input for annot: needs to have same shape as input dataframe"
            )
        elif np.any([isinstance(x, str) for x in annot.flatten()]):
            fmt = ""
        elif annot_fmt_rowwise:
            annot, annot_fmt_rows = _format_annot_heatmap(annot, annot_fmt_rows, annot_fmt_exceed)
            fmt = ""

        elif num_digits is None or num_digits > 5:
            fmt = ".4g"
        else:
            fmt = f".{num_digits}f"

    ax = heatmap(
        df_hm,
        cmap=cmap,
        center=center,
        annot=annot,
        ax=ax,
        # changes this from df_hm to df because the annotation and colorbar didn't work.
        cbar=cbar,
        cbar_ax=cbar_ax,
        cbar_kws=cbar_kws,
        fmt=fmt,
        vmin=vmin,
        vmax=vmax,
        xticklabels=True,
        yticklabels=True,
        **kwargs,
    )

    ax.figure.axes[-1].yaxis.label.set_size(labelsize)
    if title is not None:
        ax.set_title(title, fontsize=labelsize + 2)

    if yticklabels is None:
        yticklabels = ax.get_yticklabels()

    ax.set_yticklabels(yticklabels, rotation=ytick_rot, fontsize=labelsize - 2)

    if xticklabels is None:
        xticklabels = ax.get_xticklabels()

    ax.set_xticklabels(xticklabels, rotation=xtick_rot, ha="right", fontsize=labelsize - 2)

    if xlabel is None:
        xlabel = ""

    ax.set_xlabel(xlabel, fontsize=labelsize)

    if ylabel is None:
        ylabel = ""
    ax.set_ylabel(ylabel, fontsize=labelsize)
    if cbar_labelsize is not None:
        ax.figure.axes[-1].yaxis.label.set_size(cbar_labelsize)

    return ax, annot_fmt_rows
