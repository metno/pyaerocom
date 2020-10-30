#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from collections import OrderedDict as od
from pyaerocom._lowlevel_helpers import dict_to_str, list_to_shortstr, BrowseDict

class VerticalProfile(object):
    """Object representing single variable profile data"""
    def __init__(self, data=None, altitude=None, dtime=None,
                 var_name=None, data_err=None, var_unit=None,
                 altitude_unit=None, **location_info):

        if data is None:
            data = []
        if data_err is None:
            data_err = []
        if dtime is None:
            dtime = []
        if altitude is None:
            altitude = []
        if var_name is None:
            var_name = 'data'

        self._var_name = None
        self._data = []
        self._data_err = []
        self._altitude = []
        self._vert_coord_name = None
        self._vert_coord_vals = od()

        self.var_info = BrowseDict()
        self.var_info['altitude'] = od()

        self.update(**location_info)

        self.var_name = var_name
        self.dtime = dtime
        self.data = data
        self.data_err = data_err
        self.altitude = altitude

        if var_unit is not None:
            self.var_unit = var_unit
        if altitude_unit is not None:
            self.altitude_unit = altitude_unit

    def update(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    @property
    def var_name(self):
        """Variable name of profile data"""
        if self._var_name  is None:
            raise ValueError('Variable name is not assigned...')
        return self._var_name

    @var_name.setter
    def var_name(self, val):
        if not isinstance(val, str):
            raise ValueError('Cannot assign {} as variable name, need string')
        if not val in self.var_info:
            self.var_info[val] = od()
        self._var_name = val

    @property
    def data(self):
        """Array containing data values corresponding to data"""
        return np.float64(self._data)

    @data.setter
    def data(self, val):
        self._data = val

    @property
    def data_err(self):
        """Array containing data values corresponding to data"""
        return np.float64(self._data_err)

    @data_err.setter
    def data_err(self, val):
        self._data_err = val

    @property
    def altitude(self):
        """Array containing altitude values corresponding to data"""
        if len(self._altitude) == len(self._data):
            return np.float64(self._altitude)
        return self.compute_altitude()

    @altitude.setter
    def altitude(self, val):
        self._altitude = val

    @property
    def var_unit(self):
        """Unit of variable (requires var_name to be available)"""
        if not 'units' in self.var_info[self.var_name]:
            add_str=''
            if 'unit' in self.var_info[self.var_name]:
                add_str = 'Note: attribute name "unit" is deprecated. Please ' \
                          'use "units"'
            raise ValueError('Unit is not defined. {}'.format(add_str))
        return self.var_info[self.var_name]['units']

    @var_unit.setter
    def var_unit(self, val):
        self.var_info[self.var_name]['units'] = val

    @property
    def altitude_unit(self):
        """Unit of altitude"""
        if not 'units' in self.var_info['altitude']:
            raise ValueError('Altitude unit is not defined')
        return self.var_info['altitude']['units']

    @altitude_unit.setter
    def altitude_unit(self, val):
        self.var_info['altitude']['units'] = val

    def compute_altitude(self):
        """Compute altitude based on vertical coorinate information"""
        raise NotImplementedError
        from pyaerocom.vert_coords import _VertCoordConverter as conv
        if not self.vert_coord_info:
            raise ValueError('No information about vertical coordinate found')
        elif not self.vert_coord_name in conv.supported:
            raise ValueError('Name of vertical coordinate not registered')

    def plot(self, plot_errs=True, whole_alt_range=False, rot_xlabels=30,
             errs_shaded=True, errs_alpha=0.1, add_vertbar_zero=True,
             **kwargs):
        """Simple plot method for vertical profile

        Parameters
        ----------
        plot_errs : bool
            if True, and if errordata is available

        """
        import matplotlib.pyplot as plt
        if 'figsize' in kwargs:
            figsize = kwargs.pop('figsize')
        else:
            figsize = (4, 8)
        if 'ax' in kwargs:
            ax = kwargs.pop('ax')
        else:
            _, ax = plt.subplots(1,1, figsize=figsize)
        p = ax.plot(self.data, self.altitude, '-x', **kwargs)

        c = p[0].get_color()
        if rot_xlabels:
            for lbl in ax.get_xticklabels():
                lbl.set_rotation(rot_xlabels)

        xlab = self.var_name
        ylab = 'Altitude'
        try:
            xlab += ' [{}]'.format(self.var_info[self.var_name]['units'])
        except Exception:
            pass

        try:
            ylab += ' [{}]'.format(self.var_info['altitude']['units'])
        except Exception:
            pass
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)

        if whole_alt_range:
            ax.set_ylim([np.min([0, self.altitude.min()]), self.altitude.max()])
        if plot_errs and len(self.data_err) == len(self.data):

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

    def __len__(self):
        return len(self['data'])

    def __str__(self):
        head = "Pyaerocom {}".format(type(self).__name__)
        s = "\n{}\n{}".format(head, len(head)*"-")
        s += ('\naltitude: {}'
              '\ndata: {}'
              '\ndata_err: {}'
              .format(list_to_shortstr(self.altitude),
                      list_to_shortstr(self.data),
                      list_to_shortstr(self.data_err)))
        arrays = ''
        for k, v in self.__dict__.items():
            if k.startswith('_'):
                continue
            if isinstance(v, dict) and len(v) > 0:
                s += "\n{} (dict)".format(k)
                s = dict_to_str(v, s)
            elif isinstance(v, list):
                s += "\n{} (list, {} items)".format(k, len(v))
                s += list_to_shortstr(v)
            elif isinstance(v, np.ndarray) and v.ndim==1:
                arrays += "\n{} (array, {} items)".format(k, len(v))
                arrays += list_to_shortstr(v)
            else:
                s += "\n%s: %s" %(k,v)
        s += arrays
        return s

if __name__=="__main__":

    d = data=[1,2,3,4,3,2,1,1,1,1]
    p = VerticalProfile(data=d,
                        altitude=np.arange(len(d)),
                        data_err=np.ones(len(d))*.3,
                        var_unit='1/Mm',
                        altitude_unit='m')
    p.plot()
