#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Global configurations for plotting 


"""
try:
    from cmocean.cm import dense
    _cmap_lighttheme = dense
except:
    _cmap_lighttheme = "Blues"

DEFAULT_THEME = "dark"
_COLOR_THEMES = dict(light = dict(name="light", 
                                  cmap_map=_cmap_lighttheme, 
                                  color_coastline ="k"),
                     dark = dict(name="dark", 
                                 cmap_map="viridis", 
                                 color_coastline ="#e6e6e6"))

class ColorTheme(object):
    """Pyaerocom class specifiying plotting color theme
    
    Attributes
    ----------
    name : str
        name of color theme (e.g. "light" or "dark")
    cmap_map 
        name of colormap or colormap for map plotting
    color_coastline : str
        coastline color for map plotting
        
    Example
    -------
    Load default color theme
    >>> theme = ColorTheme(name="dark")
    >>> print(theme)
    pyaerocom ColorTheme
    name : dark
    cmap_map : viridisss
    color_coastline : #e6e6e6
    """
    def __init__(self, name="dark", cmap_map=None, color_coastline=None):
        self.name = name
        self.cmap_map = cmap_map
        self.color_coastline = color_coastline
        
        if name in _COLOR_THEMES:
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



