################################################################
# read_aeronet_sunv2.py
#
# read Aeronet direct sun V2 data
#
# this file is part of the pyaerocom package
#
#################################################################
# Created 20171026 by Jan Griesfeller for Met Norway
#
# Last changed: See git log
#################################################################

# Copyright (C) 2017 met.no
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

import numpy as np
import pandas as pd
from collections import OrderedDict as od
import re

from pyaerocom import const
from pyaerocom.mathutils import (calc_ang4487aer, calc_od550aer)
from pyaerocom.io.readaeronetbase import ReadAeronetBase
from pyaerocom.stationdata import StationData

class ReadAeronetSunV2(ReadAeronetBase):
    """Interface for reading Aeronet direct sun version 2 Level 2.0 data

    .. seealso::

        Base classes :class:`ReadAeronetBase` and :class:`ReadUngriddedBase`

    Todo
    ----
    Check level 1.5 data and include

    Parameters
    ----------
    dataset_to_read
        string specifying either of the supported datasets that are defined
        in ``SUPPORTED_DATASETS``.
    """
    #: Mask for identifying datafiles
    _FILEMASK = '*.lev20'

    #: version log of this class (for caching)
    __version__ = "0.16_" + ReadAeronetBase.__baseversion__

    #: Name of dataset (OBS_ID)
    DATA_ID = const.AERONET_SUN_V2L2_AOD_DAILY_NAME

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.AERONET_SUN_V2L2_AOD_DAILY_NAME,
                          const.AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME]

    #: dictionary assigning temporal resolution flags for supported datasets
    #: that are provided in a defined temporal resolution
    TS_TYPES = {const.AERONET_SUN_V2L2_AOD_DAILY_NAME :   'daily'}

    #: default variables for read method
    DEFAULT_VARS = ['od550aer']

    #: value corresponding to invalid measurement
    NAN_VAL = -9999.

    #: Dictionary that specifies the index for each data column
    COL_INDEX = od(date           = 0,
                   time           = 1,
                   julien_day     = 2,
                   od1640aer      = 3,
                   od1020aer      = 4,
                   od870aer       = 5,
                   od675aer       = 6,
                   od667aer       = 7,
                   od555aer       = 8,
                   od551aer       = 9,
                   od532aer       = 10,
                   od531aer       = 11,
                   od500aer       = 12,
                   od440aer       = 15,
                   od380aer       = 17,
                   od340aer       = 18,
                   ang4487aer     = 37)

    #: dictionary containing information about additionally required variables
    #: for each auxiliary variable (i.e. each variable that is not provided
    #: by the original data but computed on import)
    AUX_REQUIRES = {'od550aer'   :   ['od440aer',
                                      'od500aer',
                                      'ang4487aer'],
                    'ang4487aer_calc' :   ['od440aer',
                                           'od870aer']}

    #: Functions that are used to compute additional variables (i.e. one
    #: for each variable defined in AUX_REQUIRES)
    AUX_FUNS = {'od550aer'          :   calc_od550aer,
                'ang4487aer_calc'   :   calc_ang4487aer}

    #: List of variables that are provided by this dataset (will be extended
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    PROVIDES_VARIABLES = [k for k in COL_INDEX.keys()][3:]

    @property
    def col_index(self):
        """Dictionary that specifies the index for each data column

        Note
        ----
        Overload of method in base class
        """
        return self.COL_INDEX

    def read_file(self, filename, vars_to_retrieve=None,
                  vars_as_series=False):
        """Read Aeronet Sun V2 level 2 file

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

        Returns
        -------
        StationData
            dict-like object containing results

        Example
        -------
        >>> import pyaerocom.io.read_aeronet_sunv2
        >>> obj = pyaerocom.io.read_aeronet_sunv2.ReadAeronetSunV2()
        >>> files = obj.get_file_list()
        >>> filedata = obj.read_file(files[0])
        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        # implemented in base class
        vars_to_read, vars_to_compute = self.check_vars_to_retrieve(vars_to_retrieve)

        #create empty data object (is dictionary with extended functionality)
        data_out = StationData()
        data_out.data_id = self.data_id

        #create empty array for all variables that are supposed to be read
        for var in vars_to_read:
            data_out[var] = []

        # Iterate over the lines of the file
        self.logger.info("Reading file {}".format(filename))
        with open(filename, 'rt') as in_file:
            #added to output
            data_out.head_line = in_file.readline().strip()
            data_out.algorithm = in_file.readline().strip()
            c_dummy = in_file.readline()
            # re.split(r'=|\,',c_dummy)
            i_dummy = iter(re.split(r'=|\,', c_dummy.rstrip()))
            dict_loc = dict(zip(i_dummy, i_dummy))

            data_out['latitude'] = float(dict_loc['lat'])
            data_out['longitude'] = float(dict_loc['long'])
            data_out['altitude'] = float(dict_loc['elev'])
            data_out['station_name'] = dict_loc['Location']
            data_out['PI'] = dict_loc['PI']
            data_out['ts_type'] = self.TS_TYPE
            data_out['instrument_name'] = self.INSTRUMENT_NAME

            c_dummy = in_file.readline()

            #data_out.data_header =
            in_file.readline().strip()

            for line in in_file:
                # process line
                dummy_arr = line.split(self.COL_DELIM)

                day, month, year = dummy_arr[self.col_index['date']].split(':')

                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, dummy_arr[self.col_index['time']]])
                # NOTE JGLISS: parsing timezone offset was removed on 22/2/19
                # since it is deprecated in recent numpy versions, for details
                # see https://www.numpy.org/devdocs/reference/arrays.datetime.html#changes-with-numpy-1-11
                #datestring = '+'.join([datestring, '00:00'])

                data_out['dtime'].append(np.datetime64(datestring))

                for var in vars_to_read:
                    val = float(dummy_arr[self.col_index[var]])
                    if val == self.NAN_VAL:
                        val = np.nan
                    data_out[var].append(val)
        data_out['dtime'] = np.asarray(data_out['dtime'])
        for var in vars_to_read:
            data_out[var] = np.asarray(data_out[var])

        data_out = self.compute_additional_vars(data_out, vars_to_compute)

        # TODO: reconsider to skip conversion to Series
        # convert  the vars in vars_to_retrieve to pandas time series
        # and delete the other ones
        if vars_as_series:
            for var in (vars_to_read + vars_to_compute):
                if var in vars_to_retrieve:
                    data_out[var] = pd.Series(data_out[var],
                                              index=data_out['dtime'])
                else:
                    del data_out[var]

        return data_out

if __name__=="__main__":
    import pyaerocom as pya
    pya.change_verbosity('critical')
    data = {}
    failed = []
    for name in ReadAeronetSunV2.SUPPORTED_DATASETS:
        print('reading {}'.format(name))
        reader = ReadAeronetSunV2(name)
        try:
            data[name] = reader.read_first_file()
        except Exception as e:
            failed.append(repr(e))

    for name, sdata in data.items():
        print(name)
        print(sdata)

    read = ReadAeronetSunV2()

    read.verbosity_level = 'critical'
    first_ten = read.read(last_file=10)

    data0 = read.read_first_file(vars_as_series=True)
    data = read.read_first_file()
    print(data)

    stats = first_ten.to_station_data_all()

    read = ReadAeronetSunV2(const.AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME)
    data = read.read_first_file(vars_to_retrieve=['ang4487aer',
                                                  'ang4487aer_calc'])
    print(data)
