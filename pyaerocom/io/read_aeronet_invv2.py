################################################################
# read_aeronet_invv2.py
#
# read Aeronet inversion V2 data
#
# this file is part of the pyaerocom package
#
#################################################################
# Created 20180629 by Jan Griesfeller for Met Norway
#
# Last changed: See git log
#################################################################

# Copyright (C) 2018 met.no
# Contact information:
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# E-mail: jan.griesfeller@met.no
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA

import os, re

import numpy as np
import pandas as pd

from pyaerocom import const
from pyaerocom.io.readaeronetbase import ReadAeronetBase
from pyaerocom.mathutils import calc_abs550aer, calc_od550aer
from pyaerocom.stationdata import StationData

class ReadAeronetInvV2(ReadAeronetBase):
    """Interface for reading Aeronet inversion V2 Level 1.5 and 2.0 data

    Parameters
    ----------
    dataset_to_read
        string specifying either of the supported datasets that are defined
        in ``SUPPORTED_DATASETS``
    """
    #: Mask for identifying datafiles
    _FILEMASK = '*.dubovikday'

    #: version log of this class (for caching)
    __version__ = "0.08_" + ReadAeronetBase.__baseversion__

    #: Name of dataset (OBS_ID)
    DATA_ID = const.AERONET_INV_V2L2_DAILY_NAME

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.AERONET_INV_V2L2_DAILY_NAME,
                          const.AERONET_INV_V2L15_DAILY_NAME]

    #: dictionary assigning temporal resolution flags for supported datasets
    #: that are provided in a defined temporal resolution
    TS_TYPES = {const.AERONET_INV_V2L2_DAILY_NAME   :   'daily',
                const.AERONET_INV_V2L15_DAILY_NAME  :   'daily'}

    #: Mapping for dataset location for different data levels that can be
    #: read with this interface (can be used when creating the object)
    DATA_LEVELS = {2.0      :   SUPPORTED_DATASETS[0],
                   1.5      :   SUPPORTED_DATASETS[1]}

    #: default variables for read method
    DEFAULT_VARS = ['ssa675aer','ssa440aer', 'ssa870aer', 'ssa1020aer',
                    'abs550aer',
                    'od550aer']

    #: value corresponding to invalid measurement
    NAN_VAL = -9999.

    #: dictionary specifying the file column names (values) for each Aerocom
    #: variable (keys)
    VAR_NAMES_FILE = {}
    VAR_NAMES_FILE['ssa440aer'] = 'SSA440-T'
    VAR_NAMES_FILE['ssa675aer'] = 'SSA675-T'
    VAR_NAMES_FILE['ssa870aer'] = 'SSA870-T'
    VAR_NAMES_FILE['ssa1020aer'] = 'SSA1020-T'
    VAR_NAMES_FILE['od440aer'] = 'AOTExt440-T' #derived from inversion
    VAR_NAMES_FILE['ang4487aer'] = '870-440AngstromParam.[AOTExt]-Total'
    VAR_NAMES_FILE['abs440aer'] = 'AOTAbsp440-T'
    VAR_NAMES_FILE['angabs4487aer'] = '870-440AngstromParam.[AOTAbsp]'

    #: OPTIONAL: dictionary specifying alternative column names for variables
    #: defined in :attr:`VAR_NAMES_FILE`. Check attribute _alt_vars_cols after
    #: running read().
    ALT_VAR_NAMES_FILE = {}
    ALT_VAR_NAMES_FILE['ssa440aer'] = ['SSA439-T', 'SSA441-T', 'SSA438-T',
                                       'SSA437-T', 'SSA442-T']
    ALT_VAR_NAMES_FILE['ssa675aer'] = ['SSA676-T', 'SSA673-T', 'SSA674-T',
                                       'SSA669-T', 'SSA677-T', 'SSA668-T',
                                       'SSA672-T']
    ALT_VAR_NAMES_FILE['ssa870aer'] = ['SSA871-T', 'SSA869-T', 'SSA868-T',
                                       'SSA873-T', 'SSA867-T', 'SSA872-T']
    ALT_VAR_NAMES_FILE['ssa1020aer'] = ['SSA1022-T', 'SSA1016-T', 'SSA1018-T']
    ALT_VAR_NAMES_FILE['od440aer'] = ['AOTExt439-T', 'AOTExt441-T',
                                      'AOTExt438-T', 'AOTExt437-T',
                                      'AOTExt442-T']
    ALT_VAR_NAMES_FILE['abs440aer'] = ['AOTAbsp439-T', 'AOTAbsp441-T',
                                       'AOTAbsp438-T', 'AOTAbsp437-T',
                                       'AOTAbsp442-T']

    #: dictionary containing information about additionally required variables
    #: for each auxiliary variable (i.e. each variable that is not provided
    #: by the original data but computed on import)
    AUX_REQUIRES = {'abs550aer'     :   ['abs440aer',
                                         'angabs4487aer'],
                    'od550aer'      :   ['od440aer',
                                        'ang4487aer']}

    #: Functions that are used to compute additional variables (i.e. one
    #: for each variable defined in AUX_REQUIRES)
    AUX_FUNS = {'abs550aer'     :   calc_abs550aer,
                'od550aer'      :   calc_od550aer}

    #: dictionary specifying the file column names (values) for each
    #: metadata key (cf. attributes of :class:`StationData`, e.g.
    #: 'station_name', 'longitude', 'latitude', 'altitude')
    META_NAMES_FILE = {}
    META_NAMES_FILE['data_quality_level'] = 'DATA_TYPE'
    META_NAMES_FILE['date'] = 'Date(dd-mm-yyyy)'
    META_NAMES_FILE['time'] = 'Time(hh:mm:ss)'
    META_NAMES_FILE['day_of_year'] = 'Julian_Day'

    #: List of variables that are provided by this dataset (will be extended
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    PROVIDES_VARIABLES = list(VAR_NAMES_FILE.keys())

    def __init__(self, dataset_to_read=None, level=None):
        super(ReadAeronetInvV2, self).__init__(dataset_to_read)
        if level is not None:
            self.change_data_level(level)

    def change_data_level(self, level):
        """Change level of Inversion data

        Parameters
        ----------
        level :obj:`float` or :obj:`int`,
            data level (choose from 1.5 or 2)

        Raises
        ------
        ValueError
            if input level is not available
        """
        if not level in self.DATA_LEVELS:
            raise ValueError('Invalid input for level, please choose '
                             'from {}'.format(self.DATA_LEVELS.keys()))
        super(ReadAeronetInvV2, self).__init__(self.DATA_LEVELS[level])

    def read_file(self, filename, vars_to_retrieve=None,
                  vars_as_series=False):
        """Read Aeronet file containing results from v2 inversion algorithm

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : list
            list of str with variable names to read
        vars_as_series : bool
            if True, the data columns of all variables in the result dictionary
            are converted into pandas Series objects

        Returns
        -------
        StationData
            dict-like object containing results

        Example
        -------
        >>> import pyaerocom.io as pio
        >>> obj = pio.read_aeronet_invv2.ReadAeronetInvV2()
        >>> files = obj.get_file_list()
        >>> filedata = obj.read_file(files[0])
        """
        # implemented in base class
        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)

        #create empty data object (is dictionary with extended functionality)
        data_out = StationData()

        # create empty arrays for meta information
        for item in self.META_NAMES_FILE:
            data_out[item] = []

        # create empty arrays for all variables that are supposed to be read
        # from file
        for var in vars_to_read:
            data_out[var] = []

        # Iterate over the lines of the file
        self.logger.info("Reading file {}".format(filename))

        with open(filename, 'rt') as in_file:
            #get rid of the first com,a seperated string element...
            c_dummy = ','.join(in_file.readline().strip().split(',')[1:])
            # re.split(r'=|\,',c_dummy)
            i_dummy = iter(re.split(r'=|\,', c_dummy.rstrip()))
            dict_loc = dict(zip(i_dummy, i_dummy))

            data_out['latitude'] = float(dict_loc['lat'])
            data_out['longitude'] = float(dict_loc['long'])
            data_out['altitude'] = float(dict_loc['elev'])
            data_out['station_name'] = dict_loc['Locations']
            data_out['PI'] = dict_loc['PI']
            data_out['PI_email'] = dict_loc['Email']

            data_out['ts_type'] = self.TS_TYPE

            #skip next two lines
            self.logger.info('Skipping line:\n{}'.format(in_file.readline()))
            self.logger.info('Skipping line:\n{}'.format(in_file.readline()))

            col_index_str = in_file.readline()
            if col_index_str != self._last_col_index_str:
                self.logger.info("Header has changed, reloading col_index map")
                self._update_col_index(col_index_str)
            col_index = self.col_index

            # dependent on the station, some of the required input variables
            # may not be provided in the data file. These will be ignored
            # in the following list that iterates over all data rows and will
            # be filled below, with vectors containing NaNs after the file
            # reading loop
            vars_available = {}
            col_names = {}
            for var in vars_to_read:
                if var in col_index:
                    idx = col_index[var]
                    vars_available[var] = idx
                    col_names[var] = self._last_col_order[idx]
                else:
                    self.logger.warning("Variable {} not available in file {}"
                                        .format(var, os.path.basename(filename)))
            data_out['col_names'] = col_names
            for line in in_file:
                # process line
                dummy_arr = line.strip().split(self.COL_DELIM)

                # This uses the numpy datestring64 functions that i.e. also
                # support Months as a time step for timedelta
                # Build a proper ISO 8601 UTC date string
                day, month, year = dummy_arr[col_index['date']].split(':')
                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, dummy_arr[col_index['time']]])
                # NOTE JGLISS: parsing timezone offset was removed on 22/2/19
                # since it is deprecated in recent numpy versions, for details
                # see https://www.numpy.org/devdocs/reference/arrays.datetime.html#changes-with-numpy-1-11
                # datestring = '+'.join([datestring, '00:00'])
                data_out['dtime'].append(np.datetime64(datestring))

                for var in self.META_NAMES_FILE:
                    val = dummy_arr[col_index[var]]
                    try:
                        # e.g. lon, lat, altitude
                        val = float(val)
                    except Exception:
                        pass
                    data_out[var].append(val)

                # copy the data fields that are available (rest will be filled
                # below)
                for var, idx in vars_available.items():
                    val = np.float_(dummy_arr[idx])
                    if val == self.NAN_VAL:
                        val = np.nan
                    data_out[var].append(val)

        # convert all lists to numpy arrays
        data_out['dtime'] = np.asarray(data_out['dtime'])

        for item in self.META_NAMES_FILE:
            data_out[item] = np.asarray(data_out[item])

        for var in vars_to_read:
            if var in vars_available:
                array = np.asarray(data_out[var])
            else:
                array = np.zeros(len(data_out['dtime'])) * np.nan
            data_out[var] = array

        # compute additional variables (if applicable)
        data_out = self.compute_additional_vars(data_out, vars_to_compute)

        if vars_as_series:
            for var in (vars_to_read + vars_to_compute):
                if var in vars_to_retrieve:
                    data_out[var] = pd.Series(data_out[var],
                                              index=data_out['dtime'])
                else:
                    del data_out[var]

        return data_out

if __name__=="__main__":
    import matplotlib.pyplot as plt
    plt.close('all')
    read = ReadAeronetInvV2()
    read.verbosity_level = 'warning'

    #data = read.read(read.PROVIDES_VARIABLES)

    data  = read.read_first_file()

    wavelengths = [440, 675, 870, 1020]
    vals = [np.nanmean(data.ssa440aer),
            np.nanmean(data.ssa675aer),
            np.nanmean(data.ssa870aer),
            np.nanmean(data.ssa1020aer)]

    plt.plot(wavelengths, vals, '--og')

    avgssa550aer = np.interp(550, wavelengths, vals)

    plt.plot(550, avgssa550aer, ' xb')
    print(data)

    udat = read.read(last_file=10)
    print(udat.metadata)
