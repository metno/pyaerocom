################################################################
# read_aeronet_sdav2.py
#
# read Aeronet SDA V2 data
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
import re, os
from collections import OrderedDict as od
from pyaerocom import const as const
from pyaerocom.mathutils import (calc_ang4487aer,
                                 calc_od550aer,
                                 calc_od550gt1aer,
                                 calc_od550lt1aer)
from pyaerocom.stationdata import StationData
from pyaerocom.io.readaeronetbase import ReadAeronetBase

class ReadAeronetSdaV2(ReadAeronetBase):
    """Interface for reading Aeronet Sun V2 Level 2 data

    Todo
    ----
    Check if also level 1.5 works and include

    Parameters
    ----------
    dataset_to_read
        string specifying either of the supported datasets that are defined
        in ``SUPPORTED_DATASETS``.

    """
    #: Mask for identifying datafiles
    _FILEMASK = '*.ONEILL_20'

    #: version log of this class (for caching)
    __version__ = '0.08_' + ReadAeronetBase.__baseversion__

    #: Name of dataset (OBS_ID)
    DATA_ID = const.AERONET_SUN_V2L2_SDA_DAILY_NAME

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.AERONET_SUN_V2L2_SDA_DAILY_NAME]

    #: dictionary assigning temporal resolution flags for supported datasets
    #: that are provided in a defined temporal resolution
    TS_TYPES = {const.AERONET_SUN_V2L2_SDA_DAILY_NAME   :  'daily'}

    #: default variables for read method
    DEFAULT_VARS = ['od550aer', 'od550gt1aer','od550lt1aer']

    #: value corresponding to invalid measurement
    NAN_VAL = -9999.

    # Comment jgliss 20180719: translated most varname to Aerocom convention.
    # Those, for which no defined name is known were named with a leading
    # underscore (e.g. _eta500lt1 for fine mode fraction at 500nm)
    #: Dictionary that specifies the index for each data column
    COL_INDEX = od(date                 = 0, # Date(dd:mm:yyyy)
                   time                 = 1, # Time(hh:mm:ss),
                   julien_day           = 2, # Julian_Day
                   od500aer             = 3, # Total_AOD_500nm[tau_a]
                   od500lt1aer          = 4, # Fine_Mode_AOD_500nm[tau_f]
                   od500gt1aer          = 5, # Coarse_Mode_AOD_500nm[tau_c]
                   _eta500lt1           = 6, # FineModeFraction_500nm[eta]
                   _aod500aer_fiterr    = 7, # 2nd_Order_Reg_Fit_Error-Total_AOD_500nm[regression_dtau_a]
                   _aod500lt1aer_rmse   = 8, # RMSE_Fine_Mode_AOD_500nm[Dtau_f]
                   _aod500gt1aer_rmse   = 9, # RMSE_Coarse_Mode_AOD_500nm[Dtau_c]
                   _eta500lt1_rmse      = 10, # RMSE_FineModeFraction_500nm[Deta]
                   _ang50aer            = 11, # Angstrom_Exponent(AE)-Total_500nm[alpha]
                   od870aer             = 15, # 870nm_Input_AOD
                   od675aer             = 16, # 675nm_Input_AOD
                   od667aer             = 17, # 667nm_Input_AOD
                   od555aer             = 18, # 555nm_Input_AOD
                   od551aer             = 19, # 551nm_Input_AOD
                   od532aer             = 20, # 532nm_Input_AOD
                   od531aer             = 21, # 531nm_Input_AOD
                   od500aer_input       = 22, # 500nm_Input_AOD
                   od490aer             = 23, # 490nm_Input_AOD
                   od443aer             = 24, # 443nm_Input_AOD
                   od440aer             = 25, # 440nm_Input_AOD
                   od412aer             = 26, # 412nm_Input_AOD
                   od380aer             = 27) # 380nm_Input_AOD

    # FURTHER HEADER COLUMN INDICES

    # i_dAE/dln(wavelength)-Total_500nm[alphap]=12,
    #i_AE-Fine_Mode_500nm[alpha_f]=13,
    #i_dAE/dln(wavelength)-Fine_Mode_500nm[alphap_f]=14,
    #LAST_PROCESSING_DATE_INDEX = 28, #Last_Processing_Date
    #NUMBER_OF_WAVELENGTHS_INDEX = 29, # Number_of_Wavelengths
    #UMBER_OF_OBSERVATIONS_INDEX = 30, #Number_of_Observations
    #EXACT_WAVELENGTHS_FOR_INPUT_AOD_INDEX = 31) # Exact_Wavelengths_for_Input_AOD

    # specify required dependencies for auxiliary variables, i.e. variables
    # that are NOT in Aeronet files but are computed within this class.
    # For instance, the computation of the AOD at 550nm requires import of
    # the AODs at 440, 500 and 870 nm.

    #: dictionary containing information about additionally required variables
    #: for each auxiliary variable (i.e. each variable that is not provided
    #: by the original data but computed on import)
    AUX_REQUIRES = {'ang4487aer'    :   ['od440aer',
                                         'od870aer'],
                    'od550aer'      :   ['od500aer', 'ang4487aer'],
                    'od550gt1aer'   :   ['od500gt1aer', 'ang4487aer'],
                    'od550lt1aer'   :   ['od500lt1aer', 'ang4487aer']}

    #: Functions that are used to compute additional variables (i.e. one
    #: for each variable defined in AUX_REQUIRES)
    AUX_FUNS = {'ang4487aer'    :   calc_ang4487aer,
                'od550aer'      :   calc_od550aer,
                'od550gt1aer'   :   calc_od550gt1aer,
                'od550lt1aer'   :   calc_od550lt1aer}

    #: List of variables that are provided by this dataset (will be extended
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    PROVIDES_VARIABLES = list(COL_INDEX.keys())

    # This how the beginning of data file looks like

    # Level 2.0 Quality Assured Data. The following AERONET-SDA data are
    # derived from AOD data which are pre and post-field calibrated and
    # manually inspected. SDA Version 4.1 (tauf_tauc),Note: the labels in
    # square brackets that follow some of the parameter (column) names are
    # the symbols associated with these parameters in the original SDA
    # publication of O'Neill et al. (2003)
    # Location=Zvenigorod,Latitude=55.695000,Longitude=36.775000,
    # Elevation[m]=200.000000,PI=Brent_Holben,Email=Brent.N.Holben@nasa.gov
    # SDA from Level 2.0 AOD,Daily Average,UNITS can be found at
    # http://aeronet.gsfc.nasa.gov/data_menu.html
    # Date(dd:mm:yyyy),
    # Time(hh:mm:ss),
    # Julian_Day,Total_AOD_500nm[tau_a],Fine_Mode_AOD_500nm[tau_f],
    # Coarse_Mode_AOD_500nm[tau_c],FineModeFraction_500nm[eta],
    # 2nd_Order_Reg_Fit_Error-Total_AOD_500nm[regression_dtau_a],
    # RMSE_Fine_Mode_AOD_500nm[Dtau_f],RMSE_Coarse_Mode_AOD_500nm[Dtau_c],
    # RMSE_FineModeFraction_500nm[Deta],Angstrom_Exponent(AE)-
    # Total_500nm[alpha],dAE/dln(wavelength)-Total_500nm[alphap],
    # AE-Fine_Mode_500nm[alpha_f],
    # dAE/dln(wavelength)-Fine_Mode_500nm[alphap_f],
    # 870nm_Input_AOD,675nm_Input_AOD,667nm_Input_AOD,555nm_Input_AOD,
    # 551nm_Input_AOD,532nm_Input_AOD,531nm_Input_AOD,
    # 500nm_Input_AOD,490nm_Input_AOD,443nm_Input_AOD,440nm_Input_AOD,
    # 412nm_Input_AOD,380nm_Input_AOD,Last_Processing_Date,
    # Number_of_Wavelengths,Number_of_Observations,
    # Exact_Wavelengths_for_Input_AOD
    # 16:09:2006,00:00:00,259.000000,0.059239,0.032410,0.026828,0.571506,
    # 0.004645,0.007370,0.005064,0.091573,1.278830,-0.656569,2.354811,
    # 1.413517,0.036734,0.039337,-999.,-999.,-999.,-999.,-999.,0.064670,
    # -999.,-999.,0.069614,-999.,0.083549,27:11:2007,5,11,0.868800,
    # 0.675600,0.440400,0.500500,0.380100

    @property
    def col_index(self):
        """Dictionary that specifies the index for each data column

        Note
        ----
        Pointer to :attr:`COL_INDEX`
        """
        return self.COL_INDEX

    def read_file(self, filename, vars_to_retrieve=None,
                  vars_as_series=False):
        """Read Aeronet Sun SDA V2 file

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

        # create empty arrays for all variables that are supposed to be read
        # from file
        for var in vars_to_read:
            data_out[var] = []

        # Iterate over the lines of the file
        self.logger.info("Reading file {}".format(filename))
        # Iterate over the lines of the file
        with open(filename, 'rt') as in_file:

            c_head_line = in_file.readline()
            c_algorithm = in_file.readline()

            self.logger.info(c_head_line)
            self.logger.info(c_algorithm)

            c_dummy = in_file.readline()
            # re.split(r'=|\,',c_dummy)
            i_dummy = iter(re.split(r'=|\,', c_dummy.rstrip()))
            dict_loc = dict(zip(i_dummy, i_dummy))

            data_out['latitude'] = float(dict_loc['Latitude'])
            data_out['longitude'] = float(dict_loc['Longitude'])
            data_out['altitude'] = float(dict_loc['Elevation[m]'])
            data_out['station_name'] = dict_loc['Location']
            data_out['PI'] = dict_loc['PI']
            data_out['ts_type'] = self.TS_TYPE

            c_dummy = in_file.readline()
            c_Header = in_file.readline()

            self.logger.info(c_Header)

            col_index = self.col_index

            vars_available = {}
            for var in vars_to_read:
                if var in col_index:
                    vars_available[var] = col_index[var]
                else:
                    self.logger.warning("Variable {} not available in file {}"
                                        .format(var, os.path.basename(filename)))

            for line in in_file:
                # process line
                dummy_arr = line.split(self.COL_DELIM)

                # This uses the numpy datestring64 functions that e.g. also
                # support Months as a time step for timedelta
                # Build a proper ISO 8601 UTC date string
                day, month, year = dummy_arr[col_index['date']].split(':')
                # pdb.set_trace()
                datestring = '-'.join([year, month, day])
                datestring = 'T'.join([datestring, dummy_arr[col_index['time']]])
                # NOTE JGLISS: parsing timezone offset was removed on 22/2/19
                # since it is deprecated in recent numpy versions, for details
                # see https://www.numpy.org/devdocs/reference/arrays.datetime.html#changes-with-numpy-1-11
                #datestring = '+'.join([datestring, '00:00'])
                data_out['dtime'].append(np.datetime64(datestring))

                # copy the data fields
                for var, idx in vars_available.items():
                    val = np.float_(dummy_arr[idx])
                    if val == self.NAN_VAL:
                        val = np.nan
                    data_out[var].append(val)

        # convert all lists to numpy arrays
        data_out['dtime'] = np.asarray(data_out['dtime'])

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

        return data_out

if __name__ == "__main__":
    read = ReadAeronetSdaV2()

    read.verbosity_level = 'debug'

    first_ten = read.read(last_file=10)

    data = read.read_first_file()
    print(data)
