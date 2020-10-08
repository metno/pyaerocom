################################################################
# read_aeronet_sunv3.py
#
# read Aeronet direct sun V3 data
#
# this file is part of the pyaerocom package
#
#################################################################
# Created 20180626 by Jan Griesfeller for Met Norway
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
import os

import numpy as np
import pandas as pd

from pyaerocom import const
from pyaerocom.mathutils import (calc_ang4487aer, calc_od550aer)
from pyaerocom.io.readaeronetbase import ReadAeronetBase
from pyaerocom.stationdata import StationData

class ReadAeronetSunV3(ReadAeronetBase):
    """Interface for reading Aeronet direct sun version 3 Level 1.5 and 2.0 data

    .. seealso::

        Base classes :class:`ReadAeronetBase` and :class:`ReadUngriddedBase`

    """
    #: Mask for identifying datafiles
    _FILEMASK = '*.lev*'

    #: version log of this class (for caching)
    __version__ = '0.08_' + ReadAeronetBase.__baseversion__

    #: Name of dataset (OBS_ID)
    DATA_ID = const.AERONET_SUN_V3L2_AOD_DAILY_NAME

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.AERONET_SUN_V3L15_AOD_DAILY_NAME,
                          const.AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME,
                          const.AERONET_SUN_V3L2_AOD_DAILY_NAME,
                          const.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME]

    #: dictionary assigning temporal resolution flags for supported datasets
    #: that are provided in a defined temporal resolution
    TS_TYPES = {const.AERONET_SUN_V3L15_AOD_DAILY_NAME :    'daily',
                const.AERONET_SUN_V3L2_AOD_DAILY_NAME  :    'daily'}

    #: default variables for read method
    DEFAULT_VARS = ['od550aer', 'ang4487aer']

    #: value corresponding to invalid measurement
    #NAN_VAL = -9999.
    NAN_VAL = -999.

    #: Mappings for identifying variables in file
    VAR_PATTERNS_FILE = {'AOD_([0-9]*)nm' : 'od*aer'}

    #: dictionary specifying the file column names (values) for each Aerocom
    #: variable (keys)
    VAR_NAMES_FILE = {}
    VAR_NAMES_FILE['od340aer'] = 'AOD_340nm'
    VAR_NAMES_FILE['od440aer'] = 'AOD_440nm'
    VAR_NAMES_FILE['od500aer'] = 'AOD_500nm'
    # VAR_NAMES_FILE['od865aer'] = 'AOD_865nm'
    VAR_NAMES_FILE['od870aer'] = 'AOD_870nm'
    VAR_NAMES_FILE['ang4487aer'] = '440-870_Angstrom_Exponent'

    #: dictionary specifying the file column names (values) for each
    #: metadata key (cf. attributes of :class:`StationData`, e.g.
    #: 'station_name', 'longitude', 'latitude', 'altitude')
    META_NAMES_FILE = {}
    META_NAMES_FILE['data_quality_level'] = 'Data_Quality_Level'
    META_NAMES_FILE['instrument_number'] = 'AERONET_Instrument_Number'
    META_NAMES_FILE['station_name'] = 'AERONET_Site'
    META_NAMES_FILE['latitude'] = 'Site_Latitude(Degrees)'
    META_NAMES_FILE['longitude'] = 'Site_Longitude(Degrees)'
    META_NAMES_FILE['altitude'] = 'Site_Elevation(m)'
    META_NAMES_FILE['date'] = 'Date(dd:mm:yyyy)'
    META_NAMES_FILE['time'] = 'Time(hh:mm:ss)'
    META_NAMES_FILE['day_of_year'] = 'Day_of_Year'

    META_NAMES_FILE_ALT = {'AERONET_Site' : ['AERONET_Site_Name']}
    #: dictionary containing information about additionally required variables
    #: for each auxiliary variable (i.e. each variable that is not provided
    #: by the original data but computed on import)
    AUX_REQUIRES = {'ang44&87aer'   :   ['od440aer',
                                             'od870aer'],
                    'od550aer'          :   ['od440aer',
                                             'od500aer',
                                             'ang4487aer']}

    #: Functions that are used to compute additional variables (i.e. one
    #: for each variable defined in AUX_REQUIRES)
    AUX_FUNS = {'ang44&87aer'   :   calc_ang4487aer,
                'od550aer'      :   calc_od550aer}

    #: List of variables that are provided by this dataset (will be extended
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    PROVIDES_VARIABLES = list(VAR_NAMES_FILE.keys())

    def read_file(self, filename, vars_to_retrieve=None,
                  vars_as_series=False, read_all_possible=False):
        """Read Aeronet Sun V3 level 1.5 or 2 file

        Parameters
        ----------
        filename : str
            absolute path to filename to read
        vars_to_retrieve : :obj:`list`, optional
            list of str with variable names to read. If None, use
            :attr:`DEFAULT_VARS`
        vars_as_series : bool
            if True, the data columns of all variables in the result dictionary
            are converted into pandas Series objects
        read_all_possible : bool
            if True, than all available variables belonging to either of the
            variable families that are specified in :attr:`VAR_PATTERNS_FILE`
            are read from the file (in addition to the ones that are specified
            via vars_to_retrieve).

        Returns
        -------
        StationData
            dict-like object containing results
        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        # implemented in base class
        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)

        #create empty data object (is dictionary with extended functionality)
        data_out = StationData()
        data_out.data_id = self.data_id
        # create empty arrays for meta information
        for item in self.META_NAMES_FILE:
            data_out[item] = []

        # Iterate over the lines of the file
        self.logger.info("Reading file {}".format(filename))
        with open(filename, 'rt') as in_file:
            _lines_ignored = []
            _lines_ignored.append(in_file.readline())
            _lines_ignored.append(in_file.readline())
            _lines_ignored.append(in_file.readline())
            _lines_ignored.append(in_file.readline())
            # PI line
            dummy_arr = in_file.readline().strip().split(';')
            data_out['PI'] = dummy_arr[0].split('=')[1]
            data_out['PI_email'] = dummy_arr[1].split('=')[1]
            data_out['ts_type'] = self.TS_TYPE

            data_type_comment = in_file.readline()
            _lines_ignored.append(data_type_comment)
            # TODO: delete later
            self.logger.debug("Data type comment: {}".format(data_type_comment))

            # put together a dict with the header string as key and the index number as value so that we can access
            # the index number via the header string
            col_index_str = in_file.readline()
            if col_index_str != self._last_col_index_str:
                self.logger.info("Header has changed, reloading col_index map")
                self._update_col_index(col_index_str,
                                       use_all_possible=read_all_possible)
            col_index = self.col_index

            # create empty arrays for all variables that are supposed to be read
            # from file
            for var in vars_to_read:
                data_out[var] = []
            # dependent on the station, some of the required input variables
            # may not be provided in the data file. These will be ignored
            # in the following list that iterates over all data rows and will
            # be filled below, with vectors containing NaNs after the file
            # reading loop
            vars_available = {}
            for var in vars_to_read:
                if var in col_index:
                    vars_available[var] = col_index[var]
                else:
                    self.logger.warning("Variable {} not available in file {}"
                                        .format(var, os.path.basename(filename)))
            pl = None
            for i, line in enumerate(in_file):
                # process line
                dummy_arr = line.split(self.COL_DELIM)

                if pl is not None and len(dummy_arr) != len(pl):
                    const.print_log.exception('Data line {} in {} is corrupt, '
                                              'skipping...'.format(i, filename))
                    continue
                # copy the meta data (array of type string)
                for var in self.META_NAMES_FILE:
                    try:
                        val = dummy_arr[col_index[var]]
                    except IndexError as e:
                        const.print_log.exception(repr(e))

                    try:
                        # e.g. lon, lat, altitude
                        val = float(val)
                    except Exception:
                        pass
                    data_out[var].append(val)

                # This uses the numpy datestring64 functions that e.g. also
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

                # TODO: remove elif if ensured that it works
                for var, idx in vars_available.items():
                    val = np.float_(dummy_arr[idx])
                    if val == self.NAN_VAL:
                        val = np.nan
                    data_out[var].append(val)

                pl = dummy_arr
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

        # convert data vectors to pandas.Series (if applicable)
        if vars_as_series:
            for var in (vars_to_read + vars_to_compute):
                if var in vars_to_retrieve:
                    data_out[var] = pd.Series(data_out[var],
                                              index=data_out['dtime'])
                else:
                    del data_out[var]
        self.logger.debug('The following lines were ignored: {}'.format(
                          _lines_ignored))
        return data_out

if __name__=="__main__":
    import matplotlib.pyplot as plt
    plt.close('all')

    #file = '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev2.0.AP/renamed/19930101_20190511_CEILAP-BA.lev20'

    reader = ReadAeronetSunV3(const.AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME)
    od = reader.read('od550aer')
