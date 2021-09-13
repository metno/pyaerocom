import pytest

from pyaerocom.plot import config as mod

def test__cmap_lighttheme():
    assert mod._cmap_lighttheme == 'Blues'

def test__COLOR_THEMES():
    assert list(mod._COLOR_THEMES) == ['light', 'dark']

@pytest.mark.parametrize('name', [
    ('bla', 'light', 'dark')
])
def test_ColorTheme___init__(name):

    theme = mod.ColorTheme(name)
    if not name in mod._COLOR_THEMES:
        assert theme.name == mod.DEFAULT_THEME
    else:
        assert theme.name == name

def test_ColorTheme_to_dict():
    value = mod.ColorTheme('dark').to_dict()
    assert isinstance(value, dict)
    assert value == {'name': 'dark',
                     'cmap_map': 'viridis',
                     'cmap_map_div': 'PuOr_r',
                     'cmap_map_div_shifted': True,
                     'color_coastline': '#e6e6e6',
                     'color_map_text': 'r'}

def test_ColorTheme_to_dict():
    value = mod.ColorTheme('dark').to_dict()

    theme = mod.ColorTheme()
    theme.from_dict(value)
    for key, val in value.items():
        assert getattr(theme, key) == val

def test_ColorTheme___str__():
    assert isinstance(str(mod.ColorTheme('dark')), str)