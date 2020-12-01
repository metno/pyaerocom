#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import numpy as np
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom import const

class DataSource(BrowseDict):
    """Dict-like object defining a data source

    Attributes
    ----------
    data_id
        name (or ID) of dataset (e.g. AeronetSunV3Lev2.daily)
    dataset_name
        name of dataset (e.g. AERONET)
    data_product
        data product (e.g. SDA, Inv, Sun for Aeronet)
    data_version
        version of data (e.g. 3)
    data_level
        level of data (e.g. 2)
    framework : str
        ID of framework to which data is associated (e.g. ACTRIS, GAW)
    instr_vert_loc : str
        Vertical location of measuring instrument(s).
    revision_date
        last revision date of dataset
    ts_type_src
        sampling frequency as defined in data files (use None if undefined)
    stat_merge_pref_attr : str
        optional, a metadata attribute that is available in data and that
        is used to order the individual stations by relevance in case overlaps
        occur. The associated values of this attribute need to be sortable
        (e.g. revision_date). This is only relevant in case overlaps occur.
    """
    SUPPORTED_VERT_LOCS = ["ground", "space", "airborne"]

    _types = dict(dataset_name          =   str,
                  data_product          =   str,
                  data_version          =   float,
                  data_level            =   float,
                  framework             =   str,
                  instr_vert_loc        =   str,
                  ts_type_src           =   str,
                  stat_merge_pref_attr  =   str,
                  revision_date         =   np.datetime64,
                  website               =   str)

    _ini_file_name = 'data_sources.ini'
    def __init__(self, **info):

        self.data_id = None
        self.dataset_name = None
        self.data_product = None
        self.data_version = None
        self.data_level = None

        self.framework = None
        self.instr_vert_loc = None
        self.revision_date = None
        self.website = None

        self.ts_type_src = None

        self.stat_merge_pref_attr = None

        self.update(**info)
        if self.data_id is not None:
            self._parse_source_info_from_ini()

    @property
    def data_dir(self):
        """Directory containing data files"""
        from pyaerocom.io.helpers import get_obsnetwork_dir
        return get_obsnetwork_dir(self.data_id)

    def dataset_str(self):
        s = ''
        if self.dataset_name is not None:
            s += self.dataset_name
            hasv = False
            if self.data_version is not None:
                s += '(v{}'.format(self.data_version)
                hasv = True
            if self.data_level is not None:
                if hasv:
                    s += ', Lev {})'.format(self.data_level)
                else:
                    s += '(Lev {})'.format(self.data_level)
            else:
                s += ')'
        else:
            s += self.data_id
        return s

    def load_dataset_info(self):
        """Wrapper for :func:`_parse_source_info_from_ini`"""
        try:
            self._parse_source_info_from_ini()
        except Exception:
            pass

    def _parse_source_info_from_ini(self):
        """Parse source info from ini file"""
        from configparser import ConfigParser
        cfg = ConfigParser()
        file = os.path.join(const.DIR_INI_FILES, self._ini_file_name)
        if not os.path.exists(file):
            raise IOError('File {} does not exist'.format(self._ini_file_name))
        cfg.read(file)
        if self.data_id in cfg:
            for k, v in cfg[self.data_id].items():
                if k in self._types:
                    self[k] = self._types[k](v)
                else:
                    self[k] = str(v)

class StationMetaData(DataSource):
    """This object defines a standard for station metadata in pyaerocom

    Variable names associated with meta data can vary significantly between
    different conventions (e.g. conventions in modellers community vs.
    observations community).

    Note
    ----
    - This object is a dictionary and can be easily expanded
    - In many cases, only some of the attributes are relevant

    Attributes
    ----------
    filename : str
        name of file (may be full path or only filename)
    station_id : str
        Code or unique ID of station
    station_name :str
        name or ID of a station. Note, that the concept of a station in
        pyaerocom is not necessarily related to a fixed coordinate. A station
        can also be a satellite, ship, or a human walking around and measuring
        something
    instrument_name : str
        name (or ID) of instrument
    PI : str
        principal investigator
    country : str
        string specifying country (or country ID)
    ts_type : str
        frequency of data (e.g. monthly). Note the difference between
        :attr:`ts_type_src` of :class:`DataSource`, which specifies the freq.
        of the original files.
    latitude : float
        latitude coordinate
    longitude : float
        longitude coordinate
    altitude : float
        altitude coordinate

    """
    def __init__(self, **info):

        self.filename = None

        self.station_id = None
        self.station_name = None
        self.instrument_name = None
        self.PI = None

        self.country = None
        self.country_code = None

        self.ts_type = None

        self.latitude = np.nan
        self.longitude = np.nan
        self.altitude = np.nan

        super(StationMetaData, self).__init__(**info)

class AerocomDataID(object):
    """
    Class representing a model data ID following AeroCom PhaseIII conventions

    The ID must contain 4 substrings with meta parameters:

        <ModelName>-<MeteoConfigSpecifier>_<ExperimentName>-<PerturbationName>

    E.g.

        NorESM2-met2010_CTRL-AP3

    For more information see `AeroCom diagnostics spreadsheet <https://docs.google.com/spreadsheets/d/1NiHLVTDsBo0JEBSnnDECNI2ojUnCVlxuy2PFrsRJW38/edit#gid=1475397852>`__

    This interface can be used to make sure a provided data ID is following
    this convention and to extract the corresponding meta parameters as
    dictionary (:func:`to_dict`) or to create an data_id from the corresponding
    meta parameters :func:`from_dict`.
    """
    DELIM = '_'
    SUBDELIM = '-'
    KEYS = ['model_name', 'meteo', 'experiment', 'perturbation']

    def __init__(self, data_id=None, **meta_info):

        self._data_id = None
        self._values = None

        if data_id is not None:
            self.data_id = data_id
        elif meta_info:
            self._values_from_dict(meta_info)

    @property
    def data_id(self):
        """
        str
            AeroCom data ID
        """
        return self._data_id

    @data_id.setter
    def data_id(self, val):
        self._values = self._eval_data_id(val)
        self._data_id = val

    @property
    def values(self):
        if self._values is not None:
            return self._values
        raise AttributeError('Meta value list is not set.')

    @values.setter
    def values(self, val):
        if not isinstance(val, list) or not len(val) == len(self.KEYS):
            raise ValueError('Invalid input: need list of length {}'
                             .format(len(self.KEYS)))
        # this will first create a data_id string from input values and
        # then call setter method to make sure the input is correct.
        self.data_id = self.from_values(val)

    def to_dict(self):
        """Convert data_id to dictionary

        Returns
        -------
        dict
            dictionary with metadata information
        """
        if not len(self._values) == len(self.KEYS):
            self._eval_data_id(self.data_id)
        return dict(zip(self.KEYS, self._values))

    def _values_from_dict(self, meta):
        vals = []
        for key in self.KEYS:
            if not key in meta:
                raise KeyError('Missing specification of {} in input meta dict'
                               .format(key))
            vals.append(meta[key])
        self._data_id = self.from_values(vals)
        self._values = vals

    @staticmethod
    def from_dict(meta):
        """
        Create instance of AerocomDataID from input meta dictionary

        Parameters
        ----------
        meta : dict
            dictionary containing required keys (cf. :attr:`KEYS`) and
            corresponding values to create an data_id

        Raises
        ------
        KeyError
            if not all information required is provided

        Returns
        -------
        AerocomDataID

        """
        return AerocomDataID(**meta)

    @staticmethod
    def from_values(values):
        """
        Create data_id from list of values

        Note
        ----
        The values have to be in the right order, cf. :attr:`KEYS`

        Parameters
        ----------
        values : list
            list containing values for each key in :attr:`KEYS`

        Raises
        ------
        ValueError
            if length of input list mismatches length of :attr:`KEYS`

        Returns
        -------
        str
            generated data_id

        """
        if not len(values) == 4:
            raise ValueError('Need 4 entries model_name, meteo_config, '
                             'experiment, perturbation')
        return '{}-{}_{}-{}'.format(*values)

    def _eval_data_id(self, val):
        """
        Check and extract meta information from input data_id

        Parameters
        ----------
        val : str
            data_id

        Raises
        ------
        ValueError
            if input is not string or is not in format
            <model_name>-<meteo_config>_<experiment>-<perturbation>

        Returns
        -------
        values
            DESCRIPTION.

        """
        if not isinstance(val, str):
            raise ValueError('Invalid input for data_id. Need str. Got {}'
                             .format(val))

        values = [''] * len(self.KEYS)
        spl = val.split(self.DELIM)
        if not len(spl) == 2:
            const.logger.warning('Invalid data ID {}. Need format '
                                 '<model-name>_<meteo-config>_<eperiment-name>'
                                 .format(val))
            values[0] = val
            return values

        sub = spl[0].split(self.SUBDELIM, 1)
        if len(sub) == 2:
            values[0] = sub[0] #model_name

            meteo = sub[1]
            if meteo.startswith('met'):
                values[1] = meteo #meteo_config
            else:
                const.logger.warning('Meteorology config substring in '
                                        'data_id {} needs to start with met. '
                                        .format(meteo))
                values[0] = spl[0]
        else:
            values[0] = spl[0]

        sub = spl[1].split(self.SUBDELIM, 1)
        if len(sub) == 2:
            values[2] = sub[0]
            values[3] = sub[1]
        else:
            values[2] = spl[1]
        return values

    def __eq__(self, other):
        return True if self._data_id == str(other) else False

    def __repr__(self):
        return self._data_id

    def __str__(self):
        return self._data_id

STANDARD_META_KEYS = list(StationMetaData().keys())

if __name__ == '__main__':
    meta = StationMetaData(data_id = 'AeronetSunV3Lev2.daily',
                           ts_type = 'blaaaa')
    print(meta)
    print(meta.dataset_str())

    data_id = AerocomDataID('EMEP-met2010_EXP-PERT')

    dd = data_id.to_dict()

    assert AerocomDataID(**dd) == AerocomDataID.from_dict(dd)
