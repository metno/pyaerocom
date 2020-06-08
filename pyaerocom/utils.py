#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyaerocom.io import ReadGridded
import fnmatch
import os
import pandas as pd

def create_varinfo_table(model_ids, vars_or_var_patterns, read_data=False,
                         sort_by_cols=['Var', 'Model']):
    """Create an info table for model list based on variables

    The method iterates over all models in :attr:`model_list` and creates an
    instance of :class:`ReadGridded`. Variable matches are searched based on
    input list :attr:`vars_or_var_patterns` (you may also use wildcards to
    specify a family of variables) and for each match the information below
    is collected. The search also includes variables that are not directly
    available in the model data but can be computed from other available
    variables. That is, all variables that are defined in
    :attr:`ReadGridded.AUX_REQUIRES`.

    The output table (DataFrame) then consists of the following columns:

        - Var: variable name
        - Model: model name
        - Years: available years
        - Freq: frequency
        - Vertical: information about vertical dimension (inferred from \
          Aerocom file name)
        - At stations: data is at stations (inferred from filename)
        - AUX vars: Auxiliary variable required to compute Var (col 1). Only \
          relevant for variables that are computed by the interface
        - Dim: number of dimensions (only retrieved if *read_data* is True)
        - Dim names: names of dimension coordinates (only retrieved if \
                                                     *read_data* is True)
        - Shape: Shape of data (only retrieved if *read_data* is True)
        - Read ok: reading was successful (only retrieved if *read_data* \
                                           is True)

    Parameters
    ----------
    model_ids : list
        list of model ids to be analysed (can also be string -> single model)
    vars_or_var_patterns : list
        list of variables or variable patterns to be analysed (can also be
        string -> single variable or variable family)
    read_data : bool
        if True, more information about the imported data will be available
        in the table (e.g. no. of dimensions, names of dimension coords)
        but the routine will run longer since the data is imported
    sort_by_cols : list
        column sort order (use header names in listing above). Defaults
        to `['Var', 'Model']`

    Returns
    -------
    pandas.DataFrame
        dataframe including result table (ready to be saved as csv or other
        tabular format or to be displayed in a jupyter notebook)

    Example
    -------
    >>> from pyaerocom import create_varinfo_table
    >>> models = ['INCA-BCext_CTRL2016-PD',
                  'GEOS5-freegcm_CTRL2016-PD']
    >>> vars = ['ang4487aer', 'od550aer', 'ec*']
    >>> df = create_varinfo_table(models, vars)
    >>> print(df)
    """
    if isinstance(model_ids, str):
        model_ids = [model_ids]
    if isinstance(vars_or_var_patterns, str):
        vars_or_var_patterns = [vars_or_var_patterns]

    failed = []

    header = ['Var', 'Model', 'Years', 'Freq', 'Vertical', 'At stations',
              'AUX vars', 'Dim', 'Dim names','Shape', 'Read ok']
    result = []
    table_cols = ['year', 'ts_type', 'vert_code', 'is_at_stations', 'aux_vars']
    for i, model in enumerate(model_ids):
        print('At model: {} ({} of {})'.format(model, i, len(model_ids)))
        try:
            reader = ReadGridded(model)
            var_info = reader.get_var_info_from_files()
            for var_avail, info in var_info.items():
                for var in vars_or_var_patterns:
                    if fnmatch.fnmatch(var_avail, var):
                        for freq in info['ts_type']:
                            sub_res = [var_avail, model]
                            for key in table_cols:
                                if key in info:
                                    sub_res.append(info[key])
                                else:
                                    sub_res.append(None)
                            try:
                                if not read_data:
                                    raise Exception
                                data = reader.read_var(var_avail, ts_type=freq, flex_ts_type=False)
                                dim_names = [d.name() for d in data.grid.dim_coords]
                                sub_res.extend([data.ndim, dim_names, data.shape, True])

                            except Exception:
                                sub_res.extend([None, None, None, False])
                            result.append(sub_res)

        except IOError as e:
            dummy = [None]*len(header)
            dummy[1] = model
            result.append(dummy)
            print(repr(e))
            failed.append(model)

    df = pd.DataFrame(result, columns=header)
    #df.set_index(['Var'], inplace=True)
    if sort_by_cols:
        df.sort_values(sort_by_cols, inplace=True)
    return df

def print_file(file_path):
    if not os.path.exists(file_path):
        raise IOError('File not found...')
    with open(file_path) as f:
        for line in f:
            if line.strip():
                print(line)
