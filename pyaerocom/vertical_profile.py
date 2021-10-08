import matplotlib.pyplot as plt
import numpy as np
from pyaerocom._lowlevel_helpers import BrowseDict

# ToDo: complete docstring
class VerticalProfile(object):
    """Object representing single variable profile data"""
    def __init__(self, data, altitude, dtime, var_name, data_err, var_unit,
                 altitude_unit):

        self.var_name = var_name
        self.dtime = dtime
        self.data = data
        self.data_err = data_err
        self.altitude = altitude

        self.var_info = BrowseDict()
        self.var_info['altitude'] = dict(units=altitude_unit)
        self.var_info[self.var_name] = dict(units=var_unit)

        assert len(self.data) == len(self.data_err) == len(self.altitude)


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

    # ToDo: complete docstring
    def plot(self, plot_errs=True, whole_alt_range=False, rot_xlabels=30,
             errs_shaded=True, errs_alpha=0.1, add_vertbar_zero=True,
             figsize=None, ax=None, **kwargs):
        """Simple plot method for vertical profile
        """
        if figsize is None:
            figsize = (4, 8)
        if ax is None:
            _, ax = plt.subplots(1,1, figsize=figsize)

        p = ax.plot(self.data, self.altitude, '-x', **kwargs)

        c = p[0].get_color()
        if rot_xlabels:
            for lbl in ax.get_xticklabels():
                lbl.set_rotation(rot_xlabels)

        unit = self.var_info[self.var_name]['units']
        aunit = self.var_info['altitude']['units']

        xlab = f'{self.var_name} [{unit}]'
        ylab = f'Altitude [{aunit}]'

        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)

        if whole_alt_range:
            ax.set_ylim([np.min([0, self.altitude.min()]), self.altitude.max()])
        if plot_errs:

            lower = self.data - self.data_err
            upper = self.data + self.data_err
            if errs_shaded:
                ax.fill_betweenx(self.altitude, lower, upper,
                                 color=c, alpha=errs_alpha)
            else:
                ax.errorbar(self.data, self.altitude, xerr=self.data_err,
                            ls=' ', marker=' ', color='#cccccc')
        if add_vertbar_zero:
            xl = ax.get_xlim()
            if xl[0] < 0 < xl[1]:
                ax.plot([0,0], ax.get_ylim(), '--', color='#cccccc')
        ax.figure.tight_layout()

        return ax

