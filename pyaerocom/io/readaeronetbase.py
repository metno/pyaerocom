#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import OrderedDict as od
from datetime import datetime
import numpy as np
from tqdm import tqdm

from pyaerocom.time_config import TS_TYPES
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.mathutils import numbers_in_str
from pyaerocom.helpers import varlist_aerocom
from pyaerocom.exceptions import MetaDataError, VariableNotFoundError
from pyaerocom import const, print_log

class ReadAeronetBase(ReadUngriddedBase):
    """TEMPLATE: Abstract base class template for reading of Aeronet data

    Extended abstract base class, derived from low-level base class
    :class:`ReadUngriddedBase` that contains some more functionality.
    """
    __baseversion__ = '0.12_' + ReadUngriddedBase.__baseversion__

    #: column delimiter in data block of files
    COL_DELIM = ','

    #: dictionary assigning temporal resolution flags for supported datasets
    #: that are provided in a defined temporal resolution. Key is the name
    #: of the dataset and value is the corresponding ts_type
    TS_TYPES = {}

    #: dictionary specifying the file column names (values) for each Aerocom
    #: variable (keys)
    VAR_NAMES_FILE = {}

    #: Mappings for identifying variables in file (may be specified in addition
    #: to explicit variable names specified in VAR_NAMES_FILE)
    VAR_PATTERNS_FILE = {}

    #: OPTIONAL: dictionary specifying alternative column names for variables
    #: defined in :attr:`VAR_NAMES_FILE`
    ALT_VAR_NAMES_FILE = {}

    #: dictionary specifying the file column names (values) for each
    #: metadata key (cf. attributes of :class:`StationData`, e.g.
    #: 'station_name', 'longitude', 'latitude', 'altitude')
    META_NAMES_FILE = {}

    META_NAMES_FILE_ALT = {},

    #: name of measurement instrument
    INSTRUMENT_NAME = 'sun_photometer'

    #: Default data unit that is assigned to all variables that are not
    #: specified in UNITS dictionary (cf. :attr:`UNITS`)
    DEFAULT_UNIT = '1'

    #: Variable specific units, only required for variables that deviate from
    #: :attr:`DEFAULT_UNIT` (is irrelevant for all variables that are
    #: so far supported by the implemented Aeronet products, i.e. all variables
    #: are dimensionless as specified in :attr:`DEFAULT_UNIT`)
    UNITS = {}

    IGNORE_META_KEYS = ['date', 'time', 'day_of_year']
    def __init__(self, dataset_to_read=None):
        super(ReadAeronetBase, self).__init__(dataset_to_read)

        # dictionary that contains information about the file columns
        # is written in method _update_col_index
        self._col_index = od()

        # header string referring to the content in attr. col_index. Is
        # updated whenever the former is updated (i.e. when method
        # _update_col_index is called). Can be used to check if
        # file structure changed between subsequent files so that
        # col_index is only recomputed when the file structure changes
        # and not for each file individually
        self._last_col_index_str = None
        self._last_col_order = []

        self._alt_var_cols = {}

    def _ts_type_from_data_id(self):
        if '.' in self.data_id:
            ts_type = self.data_id.split('.')[-1]
            if ts_type in TS_TYPES:
                self.TS_TYPES[self.data_id] = ts_type
                return ts_type
        raise AttributeError('Failed to retrieve ts_type from data_id')

    @property
    def TS_TYPE(self):
        """Default implementation of string for temporal resolution"""
        try:
            return self.TS_TYPES[self.data_id]
        except KeyError:
            try:
                return self._ts_type_from_data_id()
            except AttributeError:
                return 'undefined'

    @property
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
        may differ between different stations. In the latter case you may
        automise the column index retrieval by providing the header names for
        each meta and data column you want to extract using the attribute
        dictionaries :attr:`META_NAMES_FILE` and :attr:`VAR_NAMES_FILE` by
        calling :func:`_update_col_index` in your implementation of
        :func:`read_file` when you reach the line that contains the header
        information.
        """
        return self._col_index

    def infer_wavelength_colname(self, colname, low=250, high=2000):
        """Get variable wavelength from column name

        Parameters
        ----------
        colname : str
            string of column name
        low : int
            lower limit of accepted value range
        high : int
            upper limit of accepted value range

        Returns
        -------
        str
            wavelength in nm as floating str

        Raises
        ------
        ValueError
            if None or more than one number is detected in variable string
        """
        nums = numbers_in_str(colname)
        if len(nums) == 1:
            if low <= int(nums[0]) <= high:
                self.logger.debug('Succesfully extracted wavelength {} nm '
                                 'from column name {}'.format(nums[0], colname))
                return nums[0]
        raise ValueError('Failed to extract wavelength from colname {}'
                         .format(colname))

    def _update_col_index(self, col_index_str, use_all_possible=False):
        """Update file column information for fast access during read_file

        Note
        ----
        If successful (no exceptions raised), then this methods overwrites the
        current column index information stored in :attr:`col_index`.

        Parameters
        ----------
        col_index_str : str
            header string of data table in files
        use_all_possible : bool
            if True, than all available variables belonging to either of the
            variable families that are specified in :attr:`VAR_PATTERNS_FILE`
            are identified from the file header.

        Returns
        -------
        dict
            dictionary containing indices (values) for each data /
            metadata key specified in ``VAR_NAMES_FILE`` and ``META_NAMES_FILE``.

        Raises
        ------
        MetaDataError
            if one of the specified meta data columns does not exist in data
        """
        cols = col_index_str.strip().split(self.COL_DELIM)
        mapping = od()
        for idx, info_str in enumerate(cols):
            if info_str in mapping:
                mapping[info_str] = 'MULTI'
            else:
                mapping[info_str] = idx

        if use_all_possible:
            col_index = self._find_vars_pattern_based(mapping)
        else:
            col_index = self._find_vars_name_based(mapping, cols)
        self._col_index = col_index
        self._last_col_index_str = col_index_str
        self._last_col_order = cols
        return col_index

    def _check_alternative_colnames(self, val, mapping):
        if val in self.META_NAMES_FILE_ALT:
            alt_names = self.META_NAMES_FILE_ALT[val]
            if isinstance(alt_names, str) and alt_names in mapping:
                return alt_names
            elif isinstance(alt_names, list):
                for alt_name in alt_names:
                    if alt_name in mapping:
                        return alt_name
        raise MetaDataError("Required meta-information string {} could "
                            "not be found in file header".format(val))

    def _find_vars_pattern_based(self, mapping):
        raise NotImplementedError('Coming soon... maybe... if needed')
        col_index = od()
        # find meta indices
        for key, val in self.META_NAMES_FILE.items():
            if not val in mapping:
                val = self._check_alternative_colnames(val, mapping)
            col_index[key] = mapping[val]
        p = self.VAR_PATTERNS_FILE

        for pattern, aerocom_name in self.VAR_PATTERNS_FILE.items():
            if not '*' in aerocom_name:
                raise ValueError('Invalid entry in search pattern for Aerocom '
                                 'var pattern {} (search key {}): Aerocom var '
                                 'pattern must require * (which is used to '
                                 'replace identified value from search group '
                                 'in file header'
                                 .format(aerocom_name, pattern))
            if '*' in pattern:
                import fnmatch

# =============================================================================
#             for col_name, idx in mapping.items():
#                 result = re.match(pattern, col_name)
#                 if result is not None:
#                     if len(result.groups()) != 1:
#                         raise Exception('Found more than one match')
# =============================================================================
        return col_index

    def _find_vars_name_based(self, mapping, cols):
        col_index = od()
        # find meta indices
        for key, val in self.META_NAMES_FILE.items():
            if not val in mapping:
                val = self._check_alternative_colnames(val, mapping)
            col_index[key] = mapping[val]
        for var, colname in self.VAR_NAMES_FILE.items():
            if colname in mapping:
                col_index[var] = mapping[colname]
            elif const.OBS_ALLOW_ALT_WAVELENGTHS:
                known = False
                if var in self.ALT_VAR_NAMES_FILE:
                    for alt_colname in self.ALT_VAR_NAMES_FILE[var]:
                        if alt_colname in mapping:
                            known = True
                            col_index[var] = mapping[alt_colname]
                if not known:
                    try:
                        idx = self._search_var_wavelength_tol(var, cols)
                        col_index[var] = idx
                    except Exception as e:
                        self.logger.info('Failed to infer data column of '
                                         'variable {} within wavelength tolerance '
                                         'range.Error:\n{}'.format(var, repr(e)))
        return col_index

    def _search_var_wavelength_tol(self, var, cols):
        """Find alternative variable within acceptance range"""
        var_info = const.VARS[var]
        colname = self.VAR_NAMES_FILE[var]

        wvl = var_info.wavelength_nm
        tol = var_info.obs_wavelength_tol_nm
        low, high = wvl - tol, wvl + tol
        if wvl is None:
            raise AttributeError('Variable {} does not contain '
                                 'wavelength information'.format(var))

        # variable information exists and contains wavelength info
        wvl_str = self.infer_wavelength_colname(colname)
        check_mask = colname.replace(wvl_str, '')
        if not wvl == float(wvl_str):
            raise ValueError('Wavelength mismatch between '
                             'pyaerocom Variable {} and '
                             'wavelength inferred from '
                             'Aeronet column name {}'.
                             format(var, colname))

        # it is possible to extract wavelength from column
        # name and the extracted number corresponds to
        # the expected wavelength as inferred from
        # pyaerocom.Variable instance
        wvl_diff_min = 1e6

        # loop over header
        for i, col in enumerate(cols):
            try:
                wvl_str_col = self.infer_wavelength_colname(col)
            except Exception:
                pass
            else:
                wvl_col = float(wvl_str_col)
                if low <= wvl_col <= high:
                    mask = col.replace(wvl_str_col, '')
                    if check_mask == mask:
                        diff = abs(wvl_col - wvl)
                        if diff < wvl_diff_min:
                            wvl_diff_min = diff
                            if not var in self._alt_var_cols:
                                self._alt_var_cols[var] = []
                            if not col in self._alt_var_cols[var]:
                                self._alt_var_cols[var].append(col)
                            return i
        raise VariableNotFoundError('Did not find an alternative data column '
                                    'for variable {} within allowed wavelength '
                                    'tolerance range of +/- {} nm.'
                                    .format(var, tol))
    def print_all_columns(self):
        for col in self._last_col_order:
            print(col)

    def read(self, vars_to_retrieve=None, files=None, first_file=None,
             last_file=None, file_pattern=None, common_meta=None):
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
            file in the list is used. Note: is ignored if input parameter
            `file_pattern` is specified.
        last_file : :obj:`int`, optional
            index of last file in list to read. If None, the very last file
            in the list is used. Note: is ignored if input parameter
            `file_pattern` is specified.
        file_pattern : str, optional
            string pattern for file search (cf :func:`get_file_list`)
        common_meta : dict, optional
            dictionary that contains additional metadata shared for this
            network (assigned to each metadata block of the
            :class:`UngriddedData` object that is returned)

        Returns
        -------
        UngriddedData
            data object
        """
        if common_meta is None:
            common_meta = {}
        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]
        vars_to_retrieve = varlist_aerocom(vars_to_retrieve)
        if files is None:
            if len(self.files) == 0:
                self.get_file_list(pattern=file_pattern)
            files = self.files

        if file_pattern is None:
            if first_file is None:
                first_file = 0
            if last_file is None:
                last_file = len(files)

            files = files[first_file:last_file]

        self.read_failed = []

        data_obj = UngriddedData()
        meta_key = 0.0
        idx = 0

        #assign metadata object
        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx

        num_vars = len(vars_to_retrieve)
        num_files = len(files)
        print_log.info('Reading AERONET data')
        for i in tqdm(range(num_files)):

            _file = files[i]
            station_data = self.read_file(_file,
                                          vars_to_retrieve=vars_to_retrieve)
            # Fill the metatdata dict
            # the location in the data set is time step dependant!
            # use the lat location here since we have to choose one location
            # in the time series plot
            meta = od()
            meta['var_info'] = od()
            meta.update(station_data.get_meta())
            #metadata[meta_key].update(station_data.get_station_coords())
            meta['data_id'] = self.data_id
            meta['ts_type'] = self.TS_TYPE
            #meta['variables'] = vars_to_retrieve
            if 'instrument_name' in station_data and station_data['instrument_name'] is not None:
                instr = station_data['instrument_name']
            else:
                instr = self.INSTRUMENT_NAME
            meta['instrument_name'] = instr
            meta['data_revision'] = self.data_revision
            meta['filename'] = _file

            meta.update(**common_meta)
            # this is a list with indices of this station for each variable
            # not sure yet, if we really need that or if it speeds up things
            meta_idx[meta_key] = od()

            num_times = len(station_data['dtime'])

            #access array containing time stamps
            # TODO: check using index instead (even though not a problem here
            # since all Aerocom data files are of type timeseries)
            times = np.float64(station_data['dtime'])

            totnum = num_times * num_vars

            #check if size of data object needs to be extended
            if (idx + totnum) >= data_obj._ROWNO:
                #if totnum < data_obj._CHUNKSIZE, then the latter is used
                data_obj.add_chunk(totnum)

            for var_idx, var in enumerate(vars_to_retrieve):
                values = station_data[var]
                start = idx + var_idx * num_times
                stop = start + num_times

                #write common meta info for this station (data lon, lat and
                #altitude are set to station locations)
                data_obj._data[start:stop,
                               data_obj._LATINDEX] = station_data['latitude']
                data_obj._data[start:stop,
                               data_obj._LONINDEX] = station_data['longitude']
                data_obj._data[start:stop,
                               data_obj._ALTITUDEINDEX] = station_data['altitude']
                data_obj._data[start:stop,
                               data_obj._METADATAKEYINDEX] = meta_key

                # write data to data object
                data_obj._data[start:stop, data_obj._TIMEINDEX] = times
                data_obj._data[start:stop, data_obj._DATAINDEX] = values
                data_obj._data[start:stop, data_obj._VARINDEX] = var_idx

                meta_idx[meta_key][var] = np.arange(start, stop)

                if var in station_data['var_info']:
                    if 'units' in station_data['var_info'][var]:
                        u = station_data['var_info'][var]['units']
                    elif 'unit' in station_data['var_info'][var]:
                        from pyaerocom.exceptions import MetaDataError
                        raise MetaDataError('Metadata attr unit is deprecated, '
                                            'please use units')
                    else:
                        u = self.DEFAULT_UNIT
                elif var in self.UNITS:
                    u = self.UNITS[var]
                else:
                    u = self.DEFAULT_UNIT
                meta['var_info'][var] = od(units=u)
                if not var in data_obj.var_idx:
                    data_obj.var_idx[var] = var_idx

            idx += totnum
            metadata[meta_key] = meta
            meta_key = meta_key + 1.

        # shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]
        #data_obj.data_revision[self.data_id] = self.data_revision
        self.data = data_obj
        return data_obj

if __name__=="__main__":
    class ReadUngriddedImplementationExample(ReadUngriddedBase):
        _FILEMASK = ".txt"
        DATA_ID = "Blaaa"
        SUPPORTED_DATASETS = ['Blaaa', 'Blub']
        __version__ = "0.01"
        PROVIDES_VARIABLES = ["od550aer"]

        def __init__(self, dataset_to_read=None):
            if dataset_to_read is not None:
                self.DATA_ID = dataset_to_read

        @property
        def col_index(self):
            raise NotImplementedError

        def read(self):
            raise NotImplementedError

        def read_file(self):
            raise NotImplementedError

    c = ReadUngriddedImplementationExample(dataset_to_read='AeronetSunV2Lev1.5.daily')
    print(c.DATASET_PATH)
