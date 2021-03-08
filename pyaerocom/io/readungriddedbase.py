#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import abc
import glob, os
import logging
import numpy as np
from fnmatch import fnmatch

from pyaerocom import const
from pyaerocom._lowlevel_helpers import list_to_shortstr
from pyaerocom.io.helpers import get_obsnetwork_dir
from pyaerocom import LOGLEVELS
from pyaerocom.helpers import varlist_aerocom
from pyaerocom.exceptions import DataSourceError
# TODO: Proposal: include attribute ts_type that is by default undefined but
# may be set to either of the defined
class ReadUngriddedBase(abc.ABC):
    """TEMPLATE: Abstract base class template for reading of ungridded data

    .. note::

        The two dictionaries ``AUX_REQUIRES`` and ``AUX_FUNS`` can be filled
        with variables that are not contained in the original data files but
        are computed during the reading. The former specifies what additional
        variables are required to perform the computation and the latter
        specifies functions used to perform the computations of the auxiliary
        variables.
        See, for instance, the class :class:`ReadAeronetSunV3`, which includes
        the computation of the AOD at 550nm and the Angstrom coefficient
        (in 440-870 nm range) from AODs measured at other wavelengths.
    """
    #: version of this base class. Please update if you apply changes to this
    #: code. This version is required for caching and needs to be considered
    #: in the definition of __version__ in all derived classes, so that
    #: caching can be done reliably
    __baseversion__ = '0.08'

    #: dictionary containing information about additionally required variables
    #: for each auxiliary variable (i.e. each variable that is not provided
    #: by the original data but computed on import)
    AUX_REQUIRES = {}

    #: Functions that are used to compute additional variables (i.e. one
    #: for each variable defined in AUX_REQUIRES)
    AUX_FUNS = {}

    IGNORE_META_KEYS = []

    _FILEMASK = '*.*'

    def __str__(self):
        return ("Dataset name: {}\n"
                "Data directory: {}\n"
                "Supported variables: {}\n"
                "Last revision: {}"
                .format(self.data_id, self.DATASET_PATH,
                        self.PROVIDES_VARIABLES, self.data_revision))
    def __repr__(self):
        return str(type(self).__name__)

    @abc.abstractproperty
    def TS_TYPE(self):
        """Temporal resolution of dataset

        This should be defined in the header of an implementation class if
        it can be globally defined for the corresponding obs-network or in
        other cases it should be initated as string ``undefined`` and then,
        if applicable, updated in the reading routine of a file.

        The TS_TYPE information should ultimately be written into the meta-data
        of objects returned by the implementation of :func:`read_file` (e.g.
        instance of :class:`StationData` or a normal dictionary) and the method
        :func:`read` (which should ALWAYS return an instance of the
        :class:`UngriddedData` class).

        Note
        ----
        - Please use ``"undefined"`` if the derived class is not sampled on \
            a regular basis.
        - If applicable please use Aerocom ts_type (i.e. hourly, 3hourly, \
                                                    daily, monthly, yearly)
        - Note also, that the ts_type in a derived class may or may not be \
            defined in a general case. For instance, in the EBAS database the \
            resolution code can be found in the file header and may thus be \
            intiated as ``"undefined"`` in the initiation of the reading class \
            and then updated when the class is being read
        - For derived implementation classes that support reading of multiple \
            network versions, you may also assign
        """
        pass

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
    def DATA_ID(self):
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
        - needless to mention that :attr:`DATA_ID` needs to be in this list
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
    def DEFAULT_VARS(self):
        """List containing default variables to read"""
        pass

    @property
    def DATASET_PATH(self):
        """Path to datafiles of specified dataset

        Is retrieved automatically (if not specified explicitly on class
        instantiation), based on network ID (:attr:`DATA_ID`)
        using :func:`get_obsnetwork_dir` (which uses the information in
        ``pyaerocom.const``).
        """
        if self._dataset_path is not None and os.path.exists(self._dataset_path):
            return self._dataset_path
        return get_obsnetwork_dir(self.data_id)

    @property
    def data_dir(self):
        """
        Wrapper for :attr:`DATASET_PATH`
        """
        return self.DATASET_PATH

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
        :obj:`dict` or :obj:`StationData`, or other...
            imported data in a suitable format that can be handled by
            :func:`read` which is supposed to append the loaded results from
            this method (which reads one datafile) to an instance of
            :class:`UngriddedData` for all files.
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
            instance of ungridded data object containing data from all files.
        """
        pass

    ### Concrete implementations of methods that are the same for all (or most)
    # of the derived reading classes
    def __init__(self, dataset_to_read=None, dataset_path=None):
        self.data = None #object that holds the loaded data
        self._data_id = None
        self.files = []
        # list that will be updated in read method to store all files that
        # could not be read. It is the responsibility of developers of derived
        # classes to include a try / except block in method read, where the
        # method read_file is called, and in case of an Exception, append the
        # corresponding file path to this list.
        self.read_failed = []

        self._dataset_path = dataset_path

        #: Class own instance of logger class
        self.logger = logging.getLogger(__name__)
        self._add_aux_variables()

        if dataset_to_read is not None:
            if not dataset_to_read in self.SUPPORTED_DATASETS:
                raise AttributeError("Dataset {} not supported by this "
                                     "interface".format(dataset_to_read))
            self._data_id = dataset_to_read

    @property
    def data_id(self):
        """Wrapper for :attr:`DATA_ID` (pyaerocom standard name)"""
        return self.DATA_ID if self._data_id is None else self._data_id

    @property
    def REVISION_FILE(self):
        """Name of revision file located in data directory"""
        return const.REVISION_FILE

    @property
    def AUX_VARS(self):
        """List of auxiliary variables (keys of attr. :attr:`AUX_REQUIRES`)

        Auxiliary variables are those that are not included in original files
        but are computed from other variables during import
        """
        return list(self.AUX_REQUIRES.keys())

    @property
    def dataset_to_read(self):
        return self.data_id

    @property
    def data_revision(self):
        """Revision string from file Revision.txt in the main data directory
        """
        if '_data_revision' in self.__dict__:
            return self.__dict__['_data_revision']
        rev = 'n/d'
        try:
            revision_file = os.path.join(self.DATASET_PATH, self.REVISION_FILE)
            if os.path.isfile(revision_file):
                with open(revision_file, 'rt') as in_file:
                    rev = in_file.readline().strip()
        except Exception:
            pass
        self._data_revision = rev
        return rev

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

            - bool : boolean, specifying whether variables list of required \
            variables needs to be extended or the order was changed
            - list : additionally required variables
        """
        changed = False
        added_vars = []

        for var in vars_to_retrieve:
            if var in self.AUX_VARS:
                vars_req = self.AUX_REQUIRES[var]
                for var_req in vars_req:
                    if var_req in vars_to_retrieve:
                        idx_var = vars_to_retrieve.index(var)
                        idx_var_req = vars_to_retrieve.index(var_req)
                        if idx_var < idx_var_req: #wrong order for computation
                            vars_to_retrieve[idx_var] = var_req
                            vars_to_retrieve[idx_var_req] = var
                            # break and return that it was changed (i.e repeat
                            # calling this method until nothing is changed or
                            # added)
                            return (True, added_vars + vars_to_retrieve)
                    else:
                        added_vars.append(var_req)
                        changed = True
        # it is important to insert the additionally required variables in
        # the beginning, as these need to be computed first later on
        # Example: if vars_to_retrieve=['od550aer'] then this loop will
        # find out that this requires 'ang4487aer' to be computed as
        # well. So at the end of this function, ang4487aer needs to be
        # before od550aer in the list vars_to_compute, since the method
        # "compute_additional_vars" loops over that list in the specified
        # order
        vars_to_retrieve = added_vars + vars_to_retrieve
        return (changed, vars_to_retrieve)

    def var_supported(self, var_name):
        """
        Check if input variable is supported

        Parameters
        ----------
        var_name : str
            AeroCom variable name or alias

        Raises
        ------
        VariableDefinitionError
            if input variable is not supported by pyaerocom

        Returns
        -------
        bool
            True, if variable is supported by this interface, else False

        """
        if (var_name in self.PROVIDES_VARIABLES or
            const.VARS[var_name].var_name_aerocom in self.PROVIDES_VARIABLES):
            return True
        return False

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
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        # first, check if input variables are alias names, and replace
        vars_to_retrieve = varlist_aerocom(vars_to_retrieve)

        repeat = True
        while repeat:
            repeat, vars_to_retrieve = self._add_additional_vars(vars_to_retrieve)

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
            data object containing data vectors for variables that are required
            for computation (cf. input param ``vars_to_compute``)
        vars_to_compute : list
            list of variable names that are supposed to be computed.
            Variables that are required for the computation of the variables
            need to be specified in :attr:`AUX_VARS` and need to be
            available as data vectors in the provided data dictionary (key is
            the corresponding variable name of the required variable).

        Returns
        -------
        dict
            updated data object now containing also computed variables
        """
        if not 'var_info' in data:
            data['var_info'] = {}
        for var in vars_to_compute:
            required = self.AUX_REQUIRES[var]
            missing = []
            for req in required:
                if not req in data:
                    missing.append(req)

            if len(missing) == 0:
                data[var] = self.AUX_FUNS[var](data)
                try:
                    data['var_info'][var]['computed']=True
                except KeyError:
                    data['var_info'][var] = {'computed' : True}

        return data

    def remove_outliers(self, data, vars_to_retrieve, **valid_rng_vars):
        """Remove outliers from data

        Parameters
        ----------
        data : dict-like
            data object containing data vectors for variables that are required
            for computation (cf. input param ``vars_to_compute``)
        vars_to_retrieve : list
            list of variable names for which outliers will be removed from
            data
        **valid_rng_vars
            additional keyword args specifying variable name and corresponding
            min / max interval (list or tuple) that specifies valid range
            for the variable. For each variable that is not explicitely defined
            here, the default minimum / maximum value is used (accessed via
            ``pyaerocom.const.VARS[var_name]``)
        """
        for var in vars_to_retrieve:
            if var in data:
                if var in valid_rng_vars:
                    rng = valid_rng_vars[var]
                    low, high =  rng[0], rng[1]
                else:
                    var_info = const.VARS[var]
                    low, high = var_info['minimum'], var_info['maximum']
                vals = data[var]
                mask = np.logical_or(vals < low, vals > high)
                vals[mask] = np.nan
                data[var] = vals
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

    def get_file_list(self, pattern=None):
        """Search all files to be read

        Uses :attr:`_FILEMASK` (+ optional input search pattern, e.g.
        station_name) to find valid files for query.

        Parameters
        ----------
        pattern : str, optional
            file name pattern applied to search

        Returns
        -------
        list
            list containing retrieved file locations

        Raises
        ------
        IOError
            if no files can be found
        """
        if isinstance(pattern, str):
            pattern = (pattern + self._FILEMASK).replace('**', '*')
        else:
            pattern = self._FILEMASK
        if pattern is None:
            const.print_log.warning('_FILEMASK attr. must not be None...'
                                    'using default pattern *.* for file search')
            pattern = '*.*'
        self.logger.info('Fetching data files. This might take a while...')
        files = sorted(glob.glob(os.path.join(self.DATASET_PATH,
                                              pattern)))
        if not len(files) > 0:
            all_str = list_to_shortstr(os.listdir(self.DATASET_PATH))
            raise DataSourceError('No files could be detected matching file '
                                  'mask {} in dataset {}, files in folder {}:\n'
                                  'Files in folder:{}'.format(pattern,
                                  self.dataset_to_read,
                                  self.DATASET_PATH,
                                  all_str))
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

        Note
        ----
        This method may be used for test purposes.

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

    class ReadUngriddedImplementationExample(ReadUngriddedBase):
        _FILEMASK = ".txt"
        DATA_ID = "Blaaa"
        __version__ = "0.01"
        PROVIDES_VARIABLES = ["od550aer"]
        REVISION_FILE = const.REVISION_FILE

        def __init__(self, dataset_to_read=None):
            if dataset_to_read is not None:
                self.DATA_ID = dataset_to_read

        def read(self):
            raise NotImplementedError

        def read_file(self):
            raise NotImplementedError

    c = ReadUngriddedImplementationExample(dataset_to_read='AeronetSunV2Lev1.5.daily')
    print(c.DATASET_PATH)
