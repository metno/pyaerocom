import pytest
import numpy as np
import pyaerocom.plot.plotscatter as mod
from matplotlib.axes import Axes
from ..conftest import does_not_raise_exception


def test_plot_scatter():
    val = mod.plot_scatter(np.ones(10), np.ones(10))
    assert isinstance(val,Axes)

@pytest.mark.parametrize('args,raises', [
    (dict(x_vals=np.ones(10), y_vals=np.ones(10)), does_not_raise_exception())
])
def test_plot_scatter_aerocom(args,raises):
    with raises:
        val = mod.plot_scatter_aerocom(**args)
        assert isinstance(val,Axes)