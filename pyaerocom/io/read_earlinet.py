################################################################
# read_aeronet_earlinet.py
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
import os, fnmatch
import numpy as np
import pandas as pd
import xarray
from pyaerocom import const
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom import StationProfileData

class ReadEarlinet(ReadUngriddedBase):
    """Interface for EARLINET data 
    
    Todo
    ----

        - Review file search routine: iterates currently over all variables \
        thus, iterates over all files N-times if N is the number of req. \
        variables. Should iterate over all files only once and check match \
        of either variable. 
        - Check mask for dust layer height: e.g. first file found when \
        calling :func:`get_file_list` is: /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Earlinet/data/ev/f2010/ev1008192050.e532 \
        and does not contain dust layer height..
        
        
        
    """
    #: Mask for identifying datafiles 
    _FILEMASK = '*.e*'
    
    #: version log of this class (for caching)
    __version__ = "0.04"
    
    #: Name of dataset (OBS_ID)
    DATASET_NAME = const.EARLINET_NAME
    
    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.EARLINET_NAME]
    
    #: default variables for read method
    DEFAULT_VARS = ['zdust']
    
    Z3D_VARNAME = 'Altitude'
    
    #: dictionary specifying the file search patterns for each variable
    VAR_PATTERNS_FILE = {'ec5503daer'   : '*/f*/*.e5*', 
                         'ec5323daer'   : '*/f*/*.e5*', 
                         'ec3553daer'   : '*/f*/*.e3*', 
                         'zdust'        : '*/f*/*.e*'}
    
    #: dictionary specifying the file column names (values) for each Aerocom 
    #: variable (keys)
    VAR_NAMES_FILE = {'ec5503daer'  : 'Extinction', 
                      'ec5323daer'  : 'Extinction', 
                      'ec3553daer'  : 'Extinction', 
                      'zdust'       : 'DustLayerHeight'}
        
    META_NAMES_FILE = {}

    PROVIDES_VARIABLES = ['ec5503daer', 
                          'ec5323daer', 
                          'ec3553daer', 
                          'zdust']

    def __init__(self, dataset_to_read=None):
        # initiate base class
        super(ReadEarlinet, self).__init__(dataset_to_read)
        # make sure everything is properly set up
        if not all([x in self.VAR_PATTERNS_FILE for x in self.PROVIDES_VARIABLES]):
            raise AttributeError("Please specify file search masks in "
                                 "header dict VAR_PATTERNS_FILE for each "
                                 "variable defined in PROVIDES_VARIABLES")
        elif not all([x in self.VAR_NAMES_FILE for x in self.PROVIDES_VARIABLES]):
            raise AttributeError("Please specify file search masks in "
                                 "header dict VAR_NAMES_FILE for each "
                                 "variable defined in PROVIDES_VARIABLES")
    
    def read_file(self, filename, vars_to_retrieve=None,
                  vars_as_series=False):
        """Read EARLINET file and return it as instance of :class:`StationData`
        
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
        data_out.dataset_name = self.DATASET_NAME
            
        # create empty arrays for all variables that are supposed to be read
        # from file
        for var in vars_to_read:
            data_out[var] = []
        
        # Iterate over the lines of the file
        self.logger.info("Reading file {}".format(filename))
        
        data_in = xarray.open_dataset(filename)
        
        
        data_out = data_in
        return (data_out)
    
    def read(self):
        raise NotImplementedError
        
    def get_file_list(self, vars_to_retrieve=None):
        """Perform recusive file search for all input variables
        
        Note
        ----
        Overloaded implementation of base class, since for Earlinet, the 
        paths are variable dependent
        
        Parameters
        ----------
        vars_to_retrieve : list
            list of variables to retrieve
        
        Returns
        -------
        list
            list containing file paths
        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        self.logger.info('Fetching data files. This might take a while...')
        patterns = [self.VAR_PATTERNS_FILE[var] for var in vars_to_retrieve]
        matches = []
        for root, dirnames, files in os.walk(self.DATASET_PATH):
            for pattern in patterns:
                paths = [os.path.join(root, f) for f in files]
                for path in fnmatch.filter(paths, pattern):
                    matches.append(path)
        
        return list(dict.fromkeys(matches))

if __name__=="__main__":
    read = ReadEarlinet()
    read.verbosity_level = 'debug'
    
    files = read.get_file_list()
    
    data = read.read_file(files[0])