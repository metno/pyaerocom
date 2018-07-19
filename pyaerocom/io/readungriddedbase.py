#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import abc
import glob, os
import logging
import numpy as np
from fnmatch import fnmatch

from pyaerocom.io.helpers import get_obsnetwork_dir
from pyaerocom import LOGLEVELS

class ReadUngriddedBase(abc.ABC):
    """TEMPLATE: Abstract base class template for reading of ungridded data
    
    .. note::
    
        Even though this is a template for a reading class, it prodides the 
        option to compute variables during import, that are not contained in 
        the actual data files. These can be specified for each auxiliary 
        parameter using the two class attributes ``AUX_REQUIRES`` (what 
        additional variables are required to perform the computation) and 
        ``AUX_FUNS`` (functions used to perform the computations). 
        See, for instance, the class :class:`ReadAeronetSunV2`, which includes 
        the computation of the AOD at 550nm and the Angstrom coefficient 
        (in 440-870 nm range).
    """
    #: dictionary containing information about additionally required variables
    #: for each auxiliary variable (i.e. each variable that is not provided
    #: by the original data but computed on import)
    AUX_REQUIRES = {}
    
    #: Functions that are used to compute additional variables (i.e. one 
    #: for each variable defined in AUX_REQUIRES)
    AUX_FUNS = {}
    
    @abc.abstractproperty
    def _FILEMASK(self):
        """Mask for identifying datafiles (e.g. '*.txt')
        
        Note
        ----
        May be implemented as global constant in header
        """
        pass
    
    @abc.abstractproperty
    def __version__(self):
        """Version of reading class
        
        Keeps track of changes in derived reading class (e.g. to assess whether 
        potential cache-files are outdated).
        
        Note
        ----
        May be implemented as global constant in header
        """
        pass
    
    @abc.abstractproperty
    def REVISION_FILE(self):
        """Name of data revision file located in data directory
        
        Note
        ----
        
        May be implemented as global constant in header of derieved class
        
        """
        pass
    
    @abc.abstractproperty
    def DATASET_NAME(self):
        """Name of dataset (OBS_ID)
        
        Note
        ----
        
        - May be implemented as global constant in header of derieved class
        - May be multiple that can be specified on init (see example below)
        
        """
        pass        
    
    @abc.abstractproperty
    def SUPPORTED_DATASETS(self):
        """List of all datasets supported by this interface
        
        Note
        ----
        
        - best practice to specify in header of class definition
        - needless to mention that :attr:`DATASET_NAME` needs to be in this list
        """
        pass
    
    @abc.abstractproperty
    def PROVIDES_VARIABLES(self):
        """List of variables that are provided by this dataset
        
        Note
        ----
        May be implemented as global constant in header
        """
        pass
    
    @abc.abstractproperty
    def col_index(self):
        """Dictionary that specifies the index for each data column
        
        Note
        ----
        
        Implementation depends on the data. For instance, if the variable 
        information is provided in all files (of all stations) and always in 
        the same column, then this can be set as a fixed dictionary in the 
        __init__ function of the implementation (see e.g. class
        :class:`ReadAeronetSunV2`). 
        In other cases, it may not be ensured
        that each variable is available in all files or the column definition
        may differ between different stations (see )
        """
        pass
    
    @property
    def DATASET_PATH(self):
        """Path to datafiles of specified dataset 
        
        Is retrieved automatically based on network ID (:attr:`DATASET_NAME`)
        using :func:`get_obsnetwork_dir` (which uses the information in 
        ``pyaerocom.const``).
        """
        return get_obsnetwork_dir(self.DATASET_NAME)
     
        
    @abc.abstractmethod
    def read_file(self, filename, vars_to_retrieve=None):
        """Read single file 
        
        Parameters
        ----------
        filename : str
            string specifying filename
        vars_to_retrieve : :obj:`list` or similar, optional,
            list containing variable IDs that are supposed to be read. If None, 
            all variables in :attr:`PROVIDES_VARIABLES` are loaded
        
        Returns
        -------
        :obj:`dict` or :obj:`TimeSeriesFileData` or :obj:`StationData`
            imported data
        """
        pass
    
    @abc.abstractmethod
    def read(self, vars_to_retrieve=None, files=[], first_file=None, 
             last_file=None):
        """Method that reads list of files as instance of :class:`UngriddedData`
        
        Parameters
        ----------
        vars_to_retrieve : :obj:`list` or similar, optional,
            list containing variable IDs that are supposed to be read. If None, 
            all variables in :attr:`PROVIDES_VARIABLES` are loaded
        files : :obj:`list`, optional
            list of files to be read. If None, then the file list is used that
            is returned on :func:`get_file_list`.
        first_file : :obj:`int`, optional
            index of first file in file list to read. If None, the very first
            file in the list is used
        last_file : :obj:`int`, optional
            index of last file in list to read. If None, the very last file 
            in the list is used
            
        Returns
        -------
        UngriddedData
            data object
        """
        pass

    ### Concrete implementations of methods that are the same for all (or most)
    # of the derived reading classes
    def __init__(self, dataset_to_read=None):
        self.data = None #object that holds the loaded data
        self.files = []
        # list that will be updated in read method to store all files that
        # could not be read. It is the responsibility of developers of derived
        # classes to include a try / except block in method read, where the 
        # method read_file is called, and in case of an Exception, append the
        # corresponding file path to this list.
        self.read_failed = []
        # 
        self.logger = logging.getLogger(__name__)
        self._add_aux_variables()
        
        if dataset_to_read is not None:
            if not dataset_to_read in self.SUPPORTED_DATASETS:
                raise AttributeError("Dataset {} not supported by this "
                                     "interface".format(dataset_to_read))
            self.DATASET_NAME = dataset_to_read
            
    @property
    def AUX_VARS(self):
        """List of auxiliary variables (keys of attr. :attr:`AUX_REQUIRES`)
        
        Auxiliary variables are those that are not included in original files
        but are computed from other variables during import
        """
        return list(self.AUX_REQUIRES.keys())
    
    @property
    def data_revision(self):
        """Revision string from file Revision.txt in the main data directory
        """
        try:
            revision_file = os.path.join(self.DATASET_PATH, self.REVISION_FILE)
            if os.path.isfile(revision_file):
                with open(revision_file, 'rt') as in_file:
                    revision = in_file.readline().strip()
                    in_file.close()
    
                return revision
        except Exception as e:
            raise IOError("Failed to access revision info for dataset {}. "
                          "Error message: {}".format(self.DATASET_NAME,
                                          repr(e)))
    @property
    def verbosity_level(self):
        """Current level of verbosity of logger"""
        return self.logger.level
    
    @verbosity_level.setter
    def verbosity_level(self, val):
        if isinstance(val, str):
            if not val in LOGLEVELS:
                raise ValueError("Invalid input for loglevel")
            val = LOGLEVELS[val]
        self.logger.setLevel(val)
        
    def _add_aux_variables(self):
        """Helper that makes sure all auxiliary variables can be computed"""
        for var in self.AUX_REQUIRES.keys():
            if not var in self.AUX_FUNS:
                raise AttributeError("Fatal: no computation method defined for "
                                     "auxiliary variable {}. Please specify "
                                     "method in class header dictionary "
                                     "AUX_FUNS".format(var))
            if not var in self.PROVIDES_VARIABLES:
                self.PROVIDES_VARIABLES.append(var)
                
    def _add_additional_vars(self, vars_to_retrieve):
        """Add required additional variables for computation to input list
        
        Helper method that is called in :func:`check_vars_to_retrieve` 
        in order to find all variables that are required for a specified 
        retrieval. This is relevant for additionally computed variables 
        (attribute ``AUX_VARS``) that are not available in the original data 
        files, but are computed from available parameters. 
        
        Parameters
        ----------
        vars_to_retrieve : list
            list of variables supported by this interface (i.e. must be 
            contained in ``PROVIDES_VARIABLES``)
        
        Returns
        -------
        tuple
            2-element tuple, containing
            
            - bool : boolean, specifying whether variables were added to \
            input list
            - list : modified / unmodified input list 
        """
        added = False
        added_vars = []
        for var in vars_to_retrieve:
            if var in self.AUX_VARS:
                add_vars = self.AUX_REQUIRES[var]
                for add_var in add_vars:
                    if not add_var in vars_to_retrieve:
                        added_vars.append(add_var)
                        added = True
        return (added, added_vars)
    
    def check_vars_to_retrieve(self, vars_to_retrieve):
        """Separate variables that are in file from those that are computed
        
        Some of the provided variables by this interface are not included in
        the data files but are computed within this class during data import
        (e.g. od550aer, ang4487aer). 
        
        The latter may require additional parameters to be retrieved from the 
        file, which is specified in the class header (cf. attribute
        ``AUX_REQUIRES``).
        
        This function checks the input list that specifies all required 
        variables and separates them into two lists, one that includes all
        variables that can be read from the files and a second list that
        specifies all variables that are computed in this class.
        
        Parameters
        ----------
        vars_to_retrieve : list
            all parameter names that are supposed to be loaded
        
        Returns
        -------
        tuple
            2-element tuple, containing
            
            - list: list containing all variables to be read
            - list: list containing all variables to be computed
        """
        if vars_to_retrieve is None:
            vars_to_retrieve = self.PROVIDES_VARIABLES
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        if not(all([x in self.PROVIDES_VARIABLES for x in vars_to_retrieve])):
            raise AttributeError("One or more of the desired variables is not "
                                 "supported by this dataset.")
        repeat = True
        while repeat:
            repeat, add_vars = self._add_additional_vars(vars_to_retrieve)
            # it is important to insert the additionally required variables in
            # the beginning, as these need to be computed first later on 
            # Example: if vars_to_retrieve=['od550aer'] then this loop will
            # find out that this requires 'ang4487aer' to be computed as 
            # well. So at the end of this function, ang4487aer needs to be 
            # before od550aer in the list vars_to_compute, since the method
            # @"compute_additional_vars" loops over that list in the specified
            # order
            vars_to_retrieve = add_vars + vars_to_retrieve
        
        # unique list containing all variables that are supposed to be read, 
        # either because they are required to be retrieved, or because they 
        # are supposed to be read because they are required to compute one 
        # of the output variables
        vars_to_retrieve = list(dict.fromkeys(vars_to_retrieve))
        
        # in the following, vars_to_retrieve is separated into two arrays, one 
        # containing all variables that can be read from the files, and the 
        # second containing all variables that are computed
        vars_to_read = []
        vars_to_compute = []
        
        for var in vars_to_retrieve:
            if not var in self.PROVIDES_VARIABLES:
                raise ValueError("Invalid variable {}".format(var))
            elif var in self.AUX_REQUIRES:
                vars_to_compute.append(var)
            else:
                vars_to_read.append(var)
        return (vars_to_read, vars_to_compute)
    
    def compute_additional_vars(self, data, vars_to_compute):
        """Compute all additional variables
        
        The computations for each additional parameter are done using the 
        specified methods in ``AUX_FUNS``.
        
        Parameters
        ----------
        data : dict-like
            data object containing imported results
        
        Returns
        -------
        dict
            updated data object
        """
        for var in vars_to_compute:
            required = self.AUX_REQUIRES[var]
            if all([req_var in data for req_var in required]):
                data[var] = self.AUX_FUNS[var](data)
            else:
                data[var] = np.ones(len(data['dtime']))*np.nan
                self.logger.warning("Could not compute variable {}. One or "
                                    "more of the required variables {} is "
                                    "missing in data. Filling with NaNs"
                                    .format(var, required))
        return data
    
    def find_in_file_list(self, pattern=None):
        """Find all files that match a certain wildcard pattern
        
        Parameters
        ----------
        pattern : :obj:`str`, optional
            wildcard pattern that may be used to narrow down the search (e.g.
            use ``pattern=*Berlin*`` to find only files that contain Berlin 
            in their filename)
            
        Returns
        -------
        list 
            list containing all files in :attr:`files` that match pattern
            
        Raises
        ------
        IOError
            if no matches can be found
        """
        if len(self.files) == 0:
            self.get_file_list()
        files = [f for f in self.files if fnmatch(f, pattern)]
        if not len(files) > 0:
            raise IOError("No files could be detected that match the "
                          "pattern".format(pattern))
        return files
    
    def get_file_list(self):
        """Search all files to be read
        
        
            
        Returns
        -------
        list
            list containing retrieved file locations
        
        Raises
        IOError
            if no files can be found
        """
        self.logger.info('Fetching data files. This might take a while...')
        files = sorted(glob.glob(os.path.join(self.DATASET_PATH, 
                                              self._FILEMASK)))
        if not len(files) > 0:
            raise IOError("No files could be detected...")
        self.files = files
        return files
    
    def read_station(self, station_id_filename, **kwargs):
        """Read data from a single station into :class:`UngriddedData`
        
        Find all files that contain the station ID in their filename and then
        call :func:`read`, providing the reduced filelist as input, in order 
        to read all files from this station into data object.
        
        Parameters
        ----------
        station_id_filename : str
            name of station (MUST be encrypted in filename)
        **kwargs
            additional keyword args passed to :func:`read` 
            (e.g. ``vars_to_retrieve``)
            
        Returns
        -------
        UngriddedData
            loaded data
        
        Raises
        ------
        IOError
            if no files can be found for this station ID
        """
        files = self.find_in_file_list('*{}*'.format(station_id_filename))
        return self.read(files=files, **kwargs)
        
    def read_first_file(self, **kwargs):
        """Read first file returned from :func:`get_file_list`
        
        This method may be used for test purposes. It calls :func:`get
        
        Parameters
        ----------
        **kwargs
            keyword args passed to :func:`read_file` (e.g. vars_to_retrieve)
            
        Returns
        -------
        dict-like
            dictionary or similar containing loaded results from first file
        """
        files = self.files
        if len(files) == 0:
            files = self.get_file_list()
        return self.read_file(files[0], **kwargs)

if __name__=="__main__":
    
    from pyaerocom import const
    class ReadUngriddedImplementationExample(ReadUngriddedBase):
        _FILEMASK = ".txt"
        DATASET_NAME = "Blaaa"
        __version__ = "0.01"
        PROVIDES_VARIABLES = ["od550aer"]
        REVISION_FILE = const.REVISION_FILE
        
        def __init__(self, dataset_to_read=None):
            if dataset_to_read is not None:
                self.DATASET_NAME = dataset_to_read
        
        def read(self):
            raise NotImplementedError
            
        def read_file(self):
            raise NotImplementedError
            
    c = ReadUngriddedImplementationExample(dataset_to_read='AeronetSunV2Lev1.5.daily')
    print(c.DATASET_PATH)
