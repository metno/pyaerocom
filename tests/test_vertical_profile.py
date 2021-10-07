import pytest
import pyaerocom.vertical_profile as mod
from .conftest import does_not_raise_exception

@pytest.mark.parametrize('args,raises', [
    (dict(), pytest.raises(TypeError)),
    (dict(data=[1], altitude=[1], dtime=[1], var_name='bla',
          data_err=[1],var_unit='1',altitude_unit='1'),
     does_not_raise_exception()),
    (dict(data=[1,2], altitude=[1], dtime=[1], var_name='bla',
          data_err=[1],var_unit='1',altitude_unit='1'),
     pytest.raises(AssertionError))

])
def test_VerticalProfile___init__(args,raises):
    with raises:
        mod.VerticalProfile(**args)

@pytest.mark.parametrize('args', [
    dict(), dict(plot_errs=False), dict(whole_alt_range=True),
    dict(errs_shaded=False), dict(add_vertbar_zero=False)
])
def test_VerticalProfile_plot(args):
    vp = mod.VerticalProfile(data=[1,4,3,2,1], altitude=[1,2,3,4,5],
                             dtime=[1],
                             var_name='bla',
                             data_err=[1,1,1,1,1],var_unit='ug m-3',
                             altitude_unit='m')
    vp.plot(**args)
