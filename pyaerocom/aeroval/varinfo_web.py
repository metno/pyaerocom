from pyaerocom.mathutils import is_strictly_monotonic, make_binlist
from pyaerocom.variable_helpers import get_variable


class VarinfoWeb:
    """
    Additional variable information relevant for AeroVal web output

    Attributes
    ----------
    var_name : str
        Name of variable (AeroCom name, not web display name)
    cmap_bins : list
        Value bins for web display
    cmap : str
        name of colormap for web display

    Parameters
    ----------
    var_name : str
        Name of variable (AeroCom name, not web display name)
    cmap : str, optional
        name of colormap for web display. If None, the
        colormap associated with the input variable is used (via
        :func:`pyaerocom.variable.Variable.get_cmap`). Defaults to None.
    cmap_bins : list, optional
        Value bins for web display. If None, then they are inferred from input
        vmin and vmax, or, if the latter are also None,
        from attrs :attr:`pyaerocom.variable.Variable.minimum` and
        :attr:`pyaerocom.variable.Variable.maximum`. If the latter are not
        defined an AttributeError will be thrown on initialisation.
    vmin : float, optional
        lower end of range
    vmax : float, optional
        upper end of range
    """

    _num_bins = 8

    def __init__(
        self,
        var_name: str,
        cmap: str = None,
        cmap_bins: list = None,
        vmin: float | None = None,
        vmax: float | None = None,
    ):
        if cmap_bins is not None:
            if vmin is not None or vmax is not None:
                raise ValueError("please provide either vmin and vmax OR cmap_bins, not both...")
            if not is_strictly_monotonic(cmap_bins):
                raise ValueError("cmap_bins need to be strictly monotonic")

        self.var_name = var_name
        self.cmap_bins = cmap_bins
        self.cmap = cmap
        self.autofill_missing(vmin, vmax)

    @property
    def vmin(self) -> float:
        """
        Lower end of range
        """
        return self.cmap_bins[0]

    @property
    def vmax(self) -> float:
        """
        Upper end of range
        """
        return self.cmap_bins[-1]

    def autofill_missing(self, vmin: float = None, vmax: float = None) -> None:
        """
        Autofill missing attributes related to cmap bins and cmap

        Parameters
        ----------
        vmin : float, optional
            lower end of range
        vmax : float, optional
            upper end of range

        Returns
        -------
        None

        """
        var = None
        if vmin is not None and vmax is not None:
            self.cmap_bins = make_binlist(vmin, vmax, self._num_bins)
        elif self.cmap_bins is None:
            var = get_variable(self.var_name)
            self.cmap_bins = var.get_cmap_bins(infer_if_missing=True)

        if self.cmap is None:
            if var is None:
                var = get_variable(self.var_name)
            self.cmap = var.get_cmap()

    @staticmethod
    def from_dict(dict):
        """
        Instantiate from dictionary

        Parameters
        ----------
        dict : dict
            settings

        Returns
        -------
        VarinfoWeb
            instantiated instance
        """
        return VarinfoWeb(**dict)

    def to_dict(self):
        """
        Convert to dictionary

        Returns
        -------
        dict
        """
        dd = {**self.__dict__}
        dd["vmin"] = self.vmin
        dd["vmax"] = self.vmax
        return dd
