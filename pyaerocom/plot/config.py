#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Global configurations for plotting
"""
from matplotlib.pyplot import get_cmap

from pyaerocom._lowlevel_helpers import BrowseDict
from warnings import warn

_cmap_lighttheme = "Blues"

DEFAULT_THEME = "light"
_COLOR_THEMES = dict(light = dict(name="light",
                                  cmap_map=_cmap_lighttheme,
                                  cmap_map_div='bwr_r',
                                  color_coastline ="k"),
                     dark = dict(name="dark",
                                 cmap_map="viridis",
                                 cmap_map_div='PuOr_r',
                                 color_coastline ="#e6e6e6"))

MAP_AXES_ASPECT = 1.5
FIGSIZE_DEFAULT = (16, 10)
# text positions for annotations in scatter plots
SCAT_ANNOT_XYPOS = [(.01, 0.95),
                    (0.01, 0.90),
                    (0.3, 0.90),
                    (0.01, 0.86),
                    (0.3, 0.86),
                    (0.01, 0.82),
                    (0.3, 0.82),
                    (0.01, 0.78),
                    (0.3, 0.78),
                    (0.8, 0.1),
                    (0.8, 0.06)]

class MapPlotSettings(BrowseDict):
    """Class specifying predefined plot settings for a species and region

    Parameters
    ----------
    variable : :obj:`str` or :obj
    """
    def __init__(self, variable, region, **kwargs):
        self.vmin = None
        self.vmax = None
        self.lon_range = None
        self.lat_range = None
        self.cbar_bounds = None
        self.lon_ticks = None
        self.lat_ticks = None

        self.load_input(variable, region, kwargs)

    def load_input(self, variable, region, **kwargs):
        raise NotImplementedError

class ColorTheme(object):
    """Pyaerocom class specifiying plotting color theme

    Attributes
    ----------
    name : str
        name of color theme (e.g. "light" or "dark")
    cmap_map : str
        name of colormap or colormap for map plotting
    color_coastline : str
        coastline color for map plotting
    cmap_map_div : str
        name of diverging colormap (used in map plots when plotted value range
        crosses 0)
    cmap_map_div_shifted : bool
        boolean specifying whether center of diverging colormaps for map plots
        is supposed to be shifted to 0

    Example
    -------
    Load default color theme
    >>> theme = ColorTheme(name="dark")
    >>> print(theme)
    pyaerocom ColorTheme
    name : dark
    cmap_map : viridis
    color_coastline : #e6e6e6
    """
    def __init__(self, name="dark", cmap_map=None, color_coastline=None,
                 cmap_map_div=None, cmap_map_div_shifted=True):
        self.name = name
        self.cmap_map = cmap_map
        self.cmap_map_div = cmap_map_div
        self.cmap_map_div_shifted = cmap_map_div_shifted
        self.color_coastline = color_coastline
        self.color_map_text = 'r'
        if not name in _COLOR_THEMES:
            warn("Invalid name for color theme, using default theme")
            name = DEFAULT_THEME
        self.load_default(name)

    def load_default(self, theme_name="dark"):
        """Load default color theme

        Parameters
        ----------
        theme_name : str
            name of default theme

        Raises
        ------
        ValueError
            if ``theme_name`` is not a valid default theme

        """
        if not theme_name in _COLOR_THEMES:
            raise ValueError("Default theme with name %s is not available. "
                             "Choose from %s" %_COLOR_THEMES)
        self.from_dict(_COLOR_THEMES[theme_name])

    def from_dict(self, info_dict):
        """Import theme information from dictionary

        info_dict : dict
            dictionary containing theme settings
        """
        for k, v in info_dict.items():
            if k in self.__dict__:
                self[k] = v

    def to_dict(self):
        """Convert this object into dictionary

        Returns
        -------
        dict
            dictionary representation of this object

        """
        d = {}
        for k, v in self.__dict__.items():
            d[k] = v
        return d

    def __setitem__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value

    def __repr__(self):
        return self.name

    def __str__(self):
        s = "pyaerocom ColorTheme"
        for k, v in self.__dict__.items():
            s += "\n%s : %s" %(k, v)
        return s

COLOR_THEME = ColorTheme(DEFAULT_THEME)

def get_color_theme(theme_name="dark"):
# Settings for colormap (use perceptually uniform colormaps)
    if not theme_name in _COLOR_THEMES:
        raise ValueError("Invalid input for theme_name, choose from %s"
                         %_COLOR_THEMES)
    return ColorTheme(theme_name)

if __name__=="__main__":
    print(ColorTheme("dark"))
    print(ColorTheme("light"))

    import doctest
    doctest.testmod()
