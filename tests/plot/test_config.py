import pytest

from pyaerocom.plot.config import _COLOR_THEMES, DEFAULT_THEME, ColorTheme, _cmap_lighttheme


def test__cmap_lighttheme():
    assert _cmap_lighttheme == "Blues"


def test__COLOR_THEMES():
    assert list(_COLOR_THEMES) == ["light", "dark"]


@pytest.mark.parametrize(
    "name, theme_name",
    [
        pytest.param(
            "bla",
            DEFAULT_THEME,
            id="invalid color theme",
            marks=pytest.mark.filterwarnings("ignore:Invalid name:UserWarning"),
        ),
        pytest.param("light", "light", id="light color theme"),
        pytest.param("dark", "dark", id="dark color theme"),
    ],
)
def test_ColorTheme___init__(name, theme_name):
    assert ColorTheme(name).name == theme_name


def test_ColorTheme_to_dict():
    value = ColorTheme("dark").to_dict()
    assert isinstance(value, dict)
    assert value == {
        "name": "dark",
        "cmap_map": "viridis",
        "cmap_map_div": "PuOr_r",
        "cmap_map_div_shifted": True,
        "color_coastline": "#e6e6e6",
        "color_map_text": "r",
    }


def test_ColorTheme_to_dict_items():
    value = ColorTheme("dark").to_dict()

    theme = ColorTheme()
    theme.from_dict(value)
    for key, val in value.items():
        assert getattr(theme, key) == val


def test_ColorTheme___str__():
    assert isinstance(str(ColorTheme("dark")), str)
