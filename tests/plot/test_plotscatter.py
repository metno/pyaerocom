import numpy as np
import pytest
from matplotlib.axes import Axes

import pyaerocom.plot.plotscatter as mod


def test_plot_scatter():
    val = mod.plot_scatter([1, 2], [1, 2])
    assert isinstance(val, Axes)


X, Y = np.arange(100), np.arange(100) * 2


@pytest.mark.parametrize(
    "args",
    [
        (dict(x_vals=np.ones(10), y_vals=np.ones(10))),
        (
            dict(
                x_vals=X,
                y_vals=Y,
                var_name="od550aer",
                var_name_ref="bla",
                x_name="OBS",
                y_name="MODEL",
                start=np.datetime64("2010-01-01"),
                stop=np.datetime64("2010-12-31"),
                ts_type="monthly",
                unit="ONE",
                stations_ok=10,
                filter_name="BLAAAAA",
                lowlim_stats=10,
                highlim_stats=90,
                loglog=True,
                figsize=(30, 30),
                fontsize_base=14,
                fontsize_annot=13,
                marker="o",
                color="lime",
                alpha=0.1,
            )
        ),
        (dict(x_vals=np.arange(-10, 10), y_vals=np.arange(-5, 15), loglog=True)),
    ],
)
def test_plot_scatter_aerocom(args):
    val = mod.plot_scatter_aerocom(**args)
    assert isinstance(val, Axes)
