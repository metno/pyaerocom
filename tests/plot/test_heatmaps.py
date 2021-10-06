import pytest
import pandas as pd
import numpy as np
from matplotlib.axes import Axes
from matplotlib.colors import BoundaryNorm

import pyaerocom.plot.heatmaps as mod
from ..conftest import does_not_raise_exception

def make_dataframe():
    colnames = ['M1', 'M2', 'M3']
    rownames = ['O1', 'O2', 'O3', 'O4']
    arr = np.ones((len(rownames), len(colnames)))
    arr *= np.asarray([1,2,3])

    df = pd.DataFrame(arr, index=rownames, columns=colnames)
    return df

strannot = make_dataframe().values.astype(str)
annot_nans = np.nan * make_dataframe().values
one_nan = make_dataframe().values
one_nan[0,0] = np.nan

@pytest.mark.parametrize('args,raises', [
    (dict(df=make_dataframe()), does_not_raise_exception()),
    (dict(df=make_dataframe(), annot=[1,2,3]), pytest.raises(ValueError)),
    (dict(df=make_dataframe(), sub_norm_before_div=False, normalise_rows=True),
     does_not_raise_exception()),
    (dict(df=make_dataframe(), normalise_rows=True), does_not_raise_exception()),
    (dict(df=make_dataframe(), norm_ref=0.1, normalise_rows=True),
     does_not_raise_exception()),
    (dict(df=make_dataframe(), normalise_rows=True, normalise_rows_how='mean'),
     does_not_raise_exception()),
    (dict(df=make_dataframe(), normalise_rows=True,
          normalise_rows_how='median'), does_not_raise_exception()),
    (dict(df=make_dataframe(), normalise_rows=True,
          normalise_rows_how='median'), does_not_raise_exception()),
    (dict(df=make_dataframe(), normalise_rows=True,
          normalise_rows_how='sum'), pytest.raises(ValueError)),
    (dict(df=make_dataframe(), normalise_rows=True,
          normalise_rows_how='BLAA'), pytest.raises(ValueError)),
    (dict(df=make_dataframe(), normalise_rows=True,
          normalise_rows_col='BLAAA'), pytest.raises(ValueError)),
    (dict(df=make_dataframe(), normalise_rows=True,
          normalise_rows_col='M3'), does_not_raise_exception()),
    (dict(df=make_dataframe(), color_rowwise=True),
     does_not_raise_exception()),
    (dict(df=make_dataframe(),
          norm=BoundaryNorm(boundaries=[1,2,3], ncolors=10, clip=False)),
    does_not_raise_exception()),
    (dict(df=make_dataframe(), annot=None),
     does_not_raise_exception()),
    (dict(df=make_dataframe(), annot=strannot),
     does_not_raise_exception()),
    (dict(df=make_dataframe(), annot_fmt_rowwise=True),
     does_not_raise_exception()),
    (dict(df=make_dataframe(), annot_fmt_rowwise=True, annot=annot_nans),
     does_not_raise_exception()),
    (dict(df=make_dataframe(), annot=make_dataframe().values, num_digits=2),
     does_not_raise_exception()),
    (dict(df=make_dataframe(), annot_fmt_rowwise=True,
          annot_fmt_exceed=[2, '.1E']),
     does_not_raise_exception()),
    (dict(df=make_dataframe(), annot_fmt_rowwise=True, annot=one_nan),
     does_not_raise_exception()),
    (dict(df=make_dataframe(), title='Blaa'), does_not_raise_exception()),
    (dict(df=make_dataframe(), cbar_labelsize=12),
     does_not_raise_exception()),
    (dict(df=make_dataframe(), annot_fmt_rowwise=True,
          annot=make_dataframe().values*1e-6),
     does_not_raise_exception()),
    (dict(df=make_dataframe(), annot_fmt_rowwise=True,
          annot=make_dataframe().values*1e-2),
     does_not_raise_exception()),
    (dict(df=make_dataframe(), annot_fmt_rowwise=True,
          annot=make_dataframe().values*1e6),
     does_not_raise_exception()),

])
def test_df_to_heatmap(args,raises):
    with raises:
        val = mod.df_to_heatmap(**args)
        assert isinstance(val[0], Axes)