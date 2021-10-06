import cartopy.mpl.geoaxes
import numpy as np
import pytest
from matplotlib.figure import Figure

from pyaerocom import GriddedData
from pyaerocom.exceptions import DataDimensionError
from pyaerocom.plot.config import get_color_theme, ColorTheme
import pyaerocom.plot.mapping as mod
from ..conftest import does_not_raise_exception

@pytest.mark.parametrize('color_theme,vmin,vmax,raises,name', [
    (None,None,None,does_not_raise_exception(), 'Blues'),
    (None,-1,1,does_not_raise_exception(), 'shiftedcmap'),
    (get_color_theme('light'),None,None,does_not_raise_exception(),
     'Blues'),
    (get_color_theme('dark'),None,None,does_not_raise_exception(),
     'viridis'),
])
def test_get_cmap_maps_aerocom(color_theme,vmin,vmax,raises,name):
    cmap = mod.get_cmap_maps_aerocom(color_theme,vmin,vmax)
    assert cmap.name == name

def test_set_cmap_ticks():
    ax = mod.init_map()
    ax = mod.set_map_ticks(ax,None,None)
    assert isinstance(ax, cartopy.mpl.geoaxes.GeoAxes)
    xticks = [-90, 0, 90]
    yticks = [-60,5,60]
    ax = mod.set_map_ticks(ax, xticks=xticks, yticks=yticks)
    assert list(ax.get_xticks()) == xticks
    assert list(ax.get_yticks()) == yticks

@pytest.mark.parametrize('args,raises', [
    (dict(),does_not_raise_exception()),
    (dict(projection='blaaa'),pytest.raises(ValueError)),
    (dict(projection='PlateCarree'),does_not_raise_exception()),
    (dict(projection='Mercator'),does_not_raise_exception()),
    (dict(projection='Miller'),does_not_raise_exception()),
    (dict(projection=42),pytest.raises(ValueError)),
    (dict(fig=Figure()),does_not_raise_exception()),
    (dict(fix_aspect=True),does_not_raise_exception()),
    (dict(color_theme='dark'),does_not_raise_exception()),
    (dict(color_theme=ColorTheme('dark')),does_not_raise_exception()),
])
def test_init_map(args,raises):

    with raises:
        ax = mod.init_map(**args)
        assert isinstance(ax, cartopy.mpl.geoaxes.GeoAxes)


fake_gridded = type('FakeData', (GriddedData,), {
    'content':dict(_has_latlon_dims=True,ndim=4)})


@pytest.mark.parametrize('data,args,raises', [
    (None, dict(), does_not_raise_exception()),
    (42, dict(), pytest.raises(ValueError)),
    (GriddedData(), dict(), pytest.raises(DataDimensionError)),
    (fake_gridded(), dict(), pytest.raises(DataDimensionError)),
    (None, dict(add_cbar=False), does_not_raise_exception()),
    (None, dict(ax=42), pytest.raises(ValueError)),
    (None, dict(cbar_levels=[0.2,0.4,0.6], vmin=0.1, vmax=0.2),
     pytest.raises(ValueError)),
    (None, dict(cbar_levels=[0.2,0.4,0.6]), does_not_raise_exception()),
    (None, dict(cbar_levels=[0.2,0.6],cmap='Blues'),
     does_not_raise_exception()),
    (None, dict(cbar_levels=[0.2,0.6],add_zero=True),
     does_not_raise_exception()),
    (None, dict(vmin=-0.2, log_scale=True),does_not_raise_exception()),
    (None, dict(vmin=-0.2, log_scale=False),does_not_raise_exception()),
    (None, dict(vmin=-0.1, log_scale=True, vmax=2, cmap='Reds'),
     does_not_raise_exception()),
    (None, dict(discrete_norm=False), does_not_raise_exception()),
    (None, dict(vmin=-0.1, discrete_norm=False), does_not_raise_exception()),
    ('const', dict(discrete_norm=False), pytest.raises(ValueError)),
    ('negval', dict(discrete_norm=False), does_not_raise_exception()),
    ('allnan', dict(), pytest.raises(ValueError)),
    (None, dict(), does_not_raise_exception()),
    (None, dict(log_scale=False,add_zero=True,), does_not_raise_exception()),
    (None, dict(log_scale=False,cmap='viridis'), does_not_raise_exception()),
    (None, dict(c_over='r', c_under='b'), does_not_raise_exception()),
    (None, dict(cbar_levels=[0.2,0.6], c_over='r', c_under='b'),
     does_not_raise_exception()),
    (None, dict(cbar_levels=[0.2,0.6], c_over='r'),
     does_not_raise_exception()),
    (None, dict(add_cbar=True, var_name='od550aer', unit='ug'),
     does_not_raise_exception()),
    (None, dict(add_cbar=True, cbar_ticks=[0.1,0.2,0.3]),
     does_not_raise_exception()),
    (None, dict(add_cbar=True, cbar_ticks=[0.1,0.2,0.3],
                cbar_ticks_sci=True),
     does_not_raise_exception()),
])
def test_plot_griddeddata_on_map(data_tm5,data,args,raises):
    if data is None:
        data = data_tm5
    elif data == 'allnan':
        data = data_tm5.copy()
        data.grid.data = data.grid.data * np.nan
    elif data == 'negval':
        data = data_tm5.copy()
        data.grid.data[0,0,0] = -100
    elif data == 'const':
        data = data_tm5.copy()
        data.grid.data[:,:,:] = 1
    with raises:
        val = mod.plot_griddeddata_on_map(data, **args)
        assert isinstance(val, Figure)

@pytest.mark.parametrize('region,kwargs,raises', [
    ('WORLD',{},does_not_raise_exception()),
    ('EUROPE',{},does_not_raise_exception()),
    ('EEUROPE',{},does_not_raise_exception()),
])
def test_plot_map_aerocom(data_tm5,region,kwargs,raises):
    with pytest.raises(ValueError):
        mod.plot_map_aerocom(42, 'WORLD')
    with raises:
        val = mod.plot_map_aerocom(data_tm5,region,**kwargs)
        assert isinstance(val, Figure)

def test_plot_nmb_map_colocateddata(coldata_tm5_aeronet):
    val = mod.plot_nmb_map_colocateddata(coldata_tm5_aeronet)
    assert isinstance(val, cartopy.mpl.geoaxes.GeoAxes)

def test_plot_nmb_map_colocateddata4D(coldata_tm5_tm5):
    val = mod.plot_nmb_map_colocateddata(coldata_tm5_tm5)
    assert isinstance(val, cartopy.mpl.geoaxes.GeoAxes)

def test_plot_nmb_map_colocateddataFAIL(coldata):
    cd = coldata['fake_5d']
    with pytest.raises(DataDimensionError):
        mod.plot_nmb_map_colocateddata(cd)
    cd = coldata['fake_nodims']
    with pytest.raises(AssertionError):
        mod.plot_nmb_map_colocateddata(cd)


