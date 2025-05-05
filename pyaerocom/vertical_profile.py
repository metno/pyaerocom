import numpy as np
import numpy.typing as npt

from pyaerocom._lowlevel_helpers import BrowseDict


class VerticalProfile:
    """Object representing single variable profile data"""

    def __init__(
        self,
        data: npt.ArrayLike,
        altitude: npt.ArrayLike,
        dtime,
        var_name: str,
        data_err: npt.ArrayLike | None,
        var_unit: str,
        altitude_unit: str,
    ):
        self.var_name = var_name
        self.dtime = dtime
        self.data = data
        self.data_err = data_err
        self.altitude = altitude

        self.var_info = BrowseDict()
        self.var_info["altitude"] = dict(units=altitude_unit)
        self.var_info[self.var_name] = dict(units=var_unit)

        # Guard against having data (and data errors) with missing associated altitude info
        if hasattr(self.data_err, "__len__"):
            if not self.data.shape[-1] == self.altitude.shape[-1] == self.data_err.shape[-1]:
                raise ValueError(
                    "Data, data errors, and altitude arrays must have the same length."
                )
        else:
            if not self.data.shape[-1] == self.altitude.shape[-1]:
                raise ValueError(
                    "Data and altitude arrays must have the same length along the last axis."
                )

    @property
    def data(self):
        """Array containing data values corresponding to data"""
        return self._data

    @data.setter
    def data(self, val):
        if isinstance(val, list):
            val = np.asarray(val)
        self._data = val

    @property
    def data_err(self):
        """Array containing data values corresponding to data"""
        return self._data_err

    @data_err.setter
    def data_err(self, val):
        if isinstance(val, list):
            val = np.asarray(val)
        self._data_err = val

    @property
    def altitude(self):
        """Array containing altitude values corresponding to data"""
        return self._altitude

    @altitude.setter
    def altitude(self, val):
        if isinstance(val, list):
            val = np.asarray(val)
        self._altitude = val
