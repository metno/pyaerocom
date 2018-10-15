#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Heatmap plotting functionality
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from seaborn import heatmap

def df_to_heatmap(df, cmap="bwr", center=None, low=0.3, high=0.3, vmin=None,
                  vmax=None, color_rowwise=True,
                  normalise_rows=False, normalise_rows_how='median',
                  normalise_rows_col=None,
                  annot=True, table_name="", num_digits=0, ax=None, 
                  figsize=(12,12), cbar=False, **kwargs):
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
    table_name : str
        title of plot and label of colorbar (if colorbar is included, see cbar
        option)
    num_digits : int
        number of digits printed in heatmap annotation
    ax : axes
        matplotlib axes instance used for plotting, if None, an axes will be
        created
    figsize : tuple
        size of figure for plot
    cbar : bool
        if True, a colorbar is included
    
    Returns
    -------
    axes
        plot axes instance
    """
    
    if not isinstance(df.columns, pd.MultiIndex):
        raise AttributeError("So far, heatmaps can only be created for "
                             "single column tabular data (e.g. Bias or "
                             "RMSE) with a partly unstacked MultiIndex")
        
    if df.columns.names[0] is None and len(df.columns.levels[0]) > 1:
        raise AttributeError("Heatmaps can only be plotted for single "
                             "column data (e.g. Bias, RMSE). Please "
                             "extract column first")
        
    num_fmt = ".{}f".format(num_digits)
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=figsize)
    else:
        fig = ax.figure
    cbar_kws = {}
    
    if normalise_rows:
        if normalise_rows_col is not None:
            norm_ref = df.values[:, normalise_rows_col]
            table_name += " (norm. col. {})".format(normalise_rows_col)
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
            #print(norm_ref)
            table_name += " (norm. row {})".format(normalise_rows_how)
        df = df.subtract(norm_ref, axis=0).div(norm_ref, axis=0)
        num_fmt = ".0%"
        
        cbar_kws['format'] = FuncFormatter(lambda x, pos: '{:.0%}'.format(x))
        #df = df.div(df.max(axis=1), axis=0)
    if color_rowwise:
        df_hm = df.div(abs(df).max(axis=1), axis=0)
        #df_hm = df.div(df.max(axis=1), axis=0)
    else:
        df_hm = df
    cbar_kws['label'] = table_name
    if annot is True:
        annot = df.values
    if vmin is None:
        vmin = df_hm.min().min() * (1-low)
    elif vmax is None:
        vmax = df_hm.max().max() * (1+high)
    #print(vmin, vmax)
    if center:
        ax = heatmap(df_hm, center=center, cmap=cmap, annot=annot, ax=ax, 
                     fmt=num_fmt,
                     cbar=cbar, cbar_kws=cbar_kws, vmin=vmin, vmax=vmax)
    else:
        ax = heatmap(df_hm, cmap=cmap, annot=annot, ax=ax, 
                 fmt=num_fmt,
                 cbar=cbar, cbar_kws=cbar_kws, vmin=vmin, vmax=vmax)
    ax.set_title(table_name, fontsize=16)
    xticklabels = ax.get_xticklabels()
    ax.set_xticklabels(xticklabels, rotation=45, ha='right')
    fig.tight_layout()
    
    return ax