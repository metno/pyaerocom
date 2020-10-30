#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Heatmap plotting functionality
"""
import numpy as np
import pandas as pd
from pyaerocom.mathutils import exponent
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from seaborn import heatmap, mpl_palette

def _format_annot_heatmap(annot, annot_fmt_rows, annot_fmt_exceed):
    _annot = []
    if not isinstance(annot_fmt_rows, list):
        annot_fmt_rows = []
        for row in annot:
            mask = row[~np.isnan(row)]
            if len(mask) == 0: #all NaN
                annot_fmt_rows.append('')
                continue
            mask = mask[mask!=0]
            exps = exponent(mask)
            minexp = exps.min()
            if minexp < -3:
                annot_fmt_rows.append('.1E')
            elif minexp < 0:
                annot_fmt_rows.append('.{}f'.format(-minexp + 1))
            elif minexp in [0,1]:
                annot_fmt_rows.append('.1f')
            else:
                annot_fmt_rows.append('.0f')
    if isinstance(annot_fmt_exceed, list):
        exceed_val, exceed_fmt = annot_fmt_exceed
    else:
        exceed_val, exceed_fmt = None, None

    for i, row in enumerate(annot):
        rowfmt = annot_fmt_rows[i]
        if rowfmt == '':
            row_fmt = ['']*len(row)
        else:
            #numdigits = -exps.min()
            row_fmt = []
            #lowest = np.min(row)
            #exp = exponent(lowest)
            for val in row:
                if np.isnan(val):
                    valstr = ''
                else:
                    #exp = exps(i)
                    #fmt = '.{}f'.format(numdigits)
                    if exceed_val is not None and val > exceed_val:
                        valstr = format(val, exceed_fmt)
                    else:
                        valstr = format(val, rowfmt)

                row_fmt.append(valstr)
        _annot.append(row_fmt)
    annot = np.asarray(_annot)
    return annot, annot_fmt_rows

def df_to_heatmap(df, cmap="bwr", center=None, low=0.3, high=0.3,
                  vmin=None, vmax=None, color_rowwise=False,
                  normalise_rows=False,
                  normalise_rows_how='median',
                  normalise_rows_col=None,
                  norm_ref=None,
                  annot=True, num_digits=None, ax=None,
                  figsize=(12,12), cbar=False, cbar_label="",
                  cbar_labelsize=None,
                  xticklabels=None, xtick_rot=45,
                  yticklabels=None, ytick_rot=45,
                  xlabel=None, ylabel=None,
                  title=None, circle=None, labelsize=12,
                  annot_fontsize=None,
                  annot_fmt_rowwise=False,
                  annot_fmt_exceed=None,
                  annot_fmt_rows=None, # explicit formatting strings for rows
                  cbar_ax=None,
                  cbar_kws=None,
                  **kwargs):

    """Plot a pandas dataframe as heatmap

    Parameters
    ----------
    df : DataFrame
        table data
    cmap : str
        string specifying colormap to be used
    center : float
        value that is mapped to center colour of colormap (e.g. 0)
    low : float
        Extends lower range of the table values so that when mapped to  the
        colormap, it’s entire range isn’t used. E.g. 0.3 roughly corresponds
        to colormap crop of 30% at the lower end.
    high : float
        Extends upper range of the table values so that when mapped to the
        colormap, it’s entire range isn’t used. E.g. 0.3 roughly corresponds
        to colormap crop of 30% at the upper end.
    color_rowwise : bool
        if True, the color mapping is applied row by row, else, for the whole
        table
    normalise_rows : bool
        if True, the table is normalised in a rowwise manner either using the
        mean value in each row (if argument ``normalise_rows_col`` is
        unspecified) or using the value in a specified column.
    normalise_rows_how : str
        aggregation string for row normalisation. Choose from ``mean, median,
        sum``. Only relevant if input arg ``normalise_rows==True``.
    normalise_rows_col : int, optional
        if provided and if prev. arg. ``normalise_rows==True``, then the
        corresponding table column is used for normalisation rather than
        the mean value of each row
    annot : bool
        if True, the table values are printed into the heatmap
    cbar_label : str
        label of colorbar (if colorbar is included, see cbar option)
    title : str
        title of heatmap
    num_digits : int
        number of digits printed in heatmap annotation
    ax : axes
        matplotlib axes instance used for plotting, if None, an axes will be
        created
    figsize : tuple
        size of figure for plot
    cbar : bool
        if True, a colorbar is included
    xticklabels : List[str]
        List of string labels.
    yticklabels : List[str]
        List of string labels.

    Returns
    -------
    axes
        plot axes instance
    """
    if cbar_label is None:
        cbar_label = ''

    if circle:
        raise NotImplementedError('Adding circles to heatmap is not implemented yet.')

    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=figsize)
    if cbar_kws is None:
        cbar_kws = {}
    if annot_fontsize is None:
        annot_fontsize = labelsize-4
    if not 'annot_kws' in kwargs:
        kwargs['annot_kws'] = {}
    kwargs['annot_kws']['size'] = annot_fontsize
    df_hm = df
    if normalise_rows:
        if norm_ref is None:
            if normalise_rows_col is not None:
                if isinstance(normalise_rows_col, str):
                    try:
                        normalise_rows_col = df.columns.to_list().index(normalise_rows_col)
                    except ValueError:
                        raise ValueError('Failed to localise column {}'
                                         .format(normalise_rows_col))
                norm_ref = df.values[:, normalise_rows_col]
                #cbar_label += " (norm. col. {})".format(normalise_rows_col)
            else:
                if normalise_rows_how == 'mean':
                    norm_ref = df.mean(axis=1)
                elif normalise_rows_how == 'median':
                    norm_ref = df.median(axis=1)
                elif normalise_rows_how == 'sum':
                    norm_ref = df.sum(axis=1)
                else:
                    raise ValueError('Invalid input for normalise_rows_how ({}). '
                                     'Choose from mean, median or sum'.format(normalise_rows_how))

        df_hm = df.subtract(norm_ref, axis=0).div(norm_ref, axis=0)

        cbar_kws['format'] = FuncFormatter(lambda x, pos: '{:.0%}'.format(x))
        #df = df.div(df.max(axis=1), axis=0)
    if color_rowwise:
        df_hm = df_hm.div(abs(df_hm).max(axis=1), axis=0)

    cbar_kws['label'] = cbar_label

    if 'norm' in kwargs:
        norm = kwargs['norm']
        vmin = norm.boundaries[0]
        vmax = norm.boundaries[-1]
    else:
        if vmin is None:
            vmin = df_hm.min().min() * (1-low)
        if vmax is None:
            vmax = df_hm.max().max() * (1+high)

    if annot is True:
        annot = df.values
    elif isinstance(annot, list):
        annot = np.asarray(annot)
    else:
        fmt = ''

    if isinstance(annot, np.ndarray):
        if not annot.shape == df.values.shape:
            raise ValueError('Invalid input for annot: needs to have same '
                             'shape as input dataframe')
        elif np.any([isinstance(x, str) for x in annot.flatten()]):
            fmt = ''
        elif annot_fmt_rowwise:
            annot, annot_fmt_rows = _format_annot_heatmap(annot,
                                                          annot_fmt_rows,
                                                          annot_fmt_exceed)
            fmt = ''

        elif num_digits is None or num_digits > 5:
            fmt = ".4g"
        else:
            fmt = ".{}f".format(num_digits)

    ax = heatmap(df_hm, cmap=cmap, center=center, annot=annot, ax=ax, # changes this from df_hm to df because the annotation and colorbar didn't work.
                 cbar=cbar, cbar_ax=cbar_ax, cbar_kws=cbar_kws, fmt=fmt,
                 vmin=vmin, vmax=vmax,
                 xticklabels=True, yticklabels=True, **kwargs)


    ax.figure.axes[-1].yaxis.label.set_size(labelsize)
    if title is not None:
        ax.set_title(title, fontsize=labelsize+2)

    if yticklabels is None:
        yticklabels = ax.get_yticklabels()

    ax.set_yticklabels(yticklabels,
                       rotation=ytick_rot,
                       fontsize=labelsize-2)

    if xticklabels is None:
        xticklabels = ax.get_xticklabels()

    ax.set_xticklabels(xticklabels,
                       rotation=xtick_rot,
                       ha='right',
                       fontsize=labelsize-2)

    #ax.set_xticklabels(xticklabels, rotation=45, ha='right')

    if xlabel is None:
        xlabel = ''

    ax.set_xlabel(xlabel, fontsize=labelsize)

    if ylabel is None:
        ylabel = ''
    ax.set_ylabel(ylabel, fontsize=labelsize)
    if cbar_labelsize is not None:
        ax.figure.axes[-1].yaxis.label.set_size(cbar_labelsize)
    #fig.tight_layout()

    return ax, annot_fmt_rows
