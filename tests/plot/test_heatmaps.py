import numpy as np
import pandas as pd
import pytest
from matplotlib.axes import Axes
from matplotlib.colors import BoundaryNorm

import pyaerocom.plot.heatmaps as mod


def make_dataframe():
    colnames = ["M1", "M2", "M3"]
    rownames = ["O1", "O2", "O3", "O4"]
    arr = np.ones((len(rownames), len(colnames)))
    arr *= np.asarray([1, 2, 3])

    df = pd.DataFrame(arr, index=rownames, columns=colnames)
    return df


strannot = make_dataframe().values.astype(str)
annot_nans = np.nan * make_dataframe().values
one_nan = make_dataframe().values
one_nan[0, 0] = np.nan


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(),
        dict(sub_norm_before_div=False, normalise_rows=True),
        dict(normalise_rows=True),
        dict(norm_ref=0.1, normalise_rows=True),
        dict(normalise_rows=True, normalise_rows_how="mean"),
        dict(normalise_rows=True, normalise_rows_how="median"),
        dict(normalise_rows=True, normalise_rows_how="median"),
        dict(normalise_rows=True, normalise_rows_col="M3"),
        dict(color_rowwise=True),
        dict(norm=BoundaryNorm(boundaries=[1, 2, 3], ncolors=10, clip=False)),
        dict(annot=None),
        dict(annot=strannot),
        dict(annot_fmt_rowwise=True),
        dict(annot_fmt_rowwise=True, annot=annot_nans),
        dict(annot=make_dataframe().values, num_digits=2),
        dict(annot_fmt_rowwise=True, annot_fmt_exceed=[2, ".1E"]),
        dict(annot_fmt_rowwise=True, annot=one_nan),
        dict(title="Blaa"),
        dict(cbar_labelsize=12),
        dict(annot_fmt_rowwise=True, annot=make_dataframe().values * 1e-6),
        dict(annot_fmt_rowwise=True, annot=make_dataframe().values * 1e-2),
        dict(annot_fmt_rowwise=True, annot=make_dataframe().values * 1e6),
    ],
)
@pytest.mark.filterwarnings("ignore:More than 20 figures have been opened:RuntimeWarning")
def test_df_to_heatmap(kwargs):
    val = mod.df_to_heatmap(make_dataframe(), **kwargs)
    assert isinstance(val[0], Axes)


@pytest.mark.parametrize(
    "kwargs,error",
    [
        pytest.param(
            dict(annot=[1, 2, 3]),
            "Invalid input for annot: needs to have same shape as input dataframe",
            id="invalid annot",
        ),
        pytest.param(
            dict(normalise_rows=True, normalise_rows_how="sum"),
            "Invalid input for normalise_rows_how (sum). Choose from mean, median or sum",
            id="invalid normalise_rows_how",
        ),
        pytest.param(
            dict(normalise_rows=True, normalise_rows_how="BLAA"),
            "Invalid input for normalise_rows_how (BLAA). Choose from mean, median or sum",
            id="invalid normalise_rows_how",
        ),
        pytest.param(
            dict(normalise_rows=True, normalise_rows_col="BLAAA"),
            "Failed to localise column BLAAA",
            id="invalid normalise_rows_how",
        ),
    ],
)
def test_df_to_heatmap_error(kwargs, error: str):
    with pytest.raises(ValueError) as e:
        mod.df_to_heatmap(make_dataframe(), **kwargs)
    assert str(e.value) == error
