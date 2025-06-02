"""
Interface for reading EEA AqERep files (formerly known as Airbase data).
"""

import glob
import gzip
import logging
import os
import pathlib
import shutil
import tempfile

import numpy as np
import pandas as pd
from tqdm import tqdm

from pyaerocom.exceptions import EEAv2FileError, TemporalResolutionError
from pyaerocom.io.helpers import get_country_name_from_iso
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.stationdata import StationData
from pyaerocom.ungriddeddata import UngriddedData

from pyaerocom.units import Unit

logger = logging.getLogger(__name__)


class ReadEEAAQEREPBase(ReadUngriddedBase):
    """Class for reading EEA AQErep data

    Extended class derived from  low-level base class
    :class:`ReadUngriddedBase` that contains some more functionality.

    Note
    ----
    Currently only single variable reading into an :class:`UngriddedData`
    object is supported.
    """

    #: Mask for identifying datafiles
    _FILEMASK = "*.csv"

    #: Version log of this class (for caching)
    __version__ = "0.09"

    #: Column delimiter
    FILE_COL_DELIM = ","

    #: Name of the dataset (OBS_ID)
    DATA_ID = ""  # change this since we added more vars?

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [DATA_ID]

    #: There is no global ts_type but it is specified in the data files...
    TS_TYPE = "variable"

    #: sampling frequencies found in data files
    TS_TYPES_FILE = {
        "hour": "hourly",
        "day": "daily",
    }

    #: Dictionary specifying values corresponding to invalid measurements
    #: there's no value for NaNs in this data set. It uses an empty string
    NAN_VAL = {}

    #: Dictionary specifying the file column names (values) for each Aerocom
    #: variable (keys)
    # There's only one variable in each file named concentration
    VAR_NAMES_FILE = {}
    VAR_NAMES_FILE["concso2"] = "concentration"
    VAR_NAMES_FILE["conco3"] = "concentration"
    VAR_NAMES_FILE["concno2"] = "concentration"
    VAR_NAMES_FILE["concco"] = "concentration"
    VAR_NAMES_FILE["concno"] = "concentration"
    VAR_NAMES_FILE["concpm10"] = "concentration"
    VAR_NAMES_FILE["concpm25"] = "concentration"
    VAR_NAMES_FILE["vmro3"] = "concentration"
    VAR_NAMES_FILE["vmro3max"] = "concentration"
    VAR_NAMES_FILE["vmrno2"] = "concentration"

    VAR_NAMES_FILE["concSso2"] = "concentration"
    VAR_NAMES_FILE["concNno"] = "concentration"
    VAR_NAMES_FILE["concNno2"] = "concentration"

    #: units of variables in files (needs to be defined for each variable supported)
    VAR_UNITS_FILE = {
        "µg/m3": "ug m-3",
        "mg/m3": "mg m-3",
        "µgS/m3": "ug S m-3",
        "µgN/m3": "ug N m-3",
        "ppb": "ppb",
    }

    #: file masks for the data files
    FILE_MASKS = dict(
        concso2="**/??_1_*_timeseries.csv*",
        concpm10="**/??_5_*_timeseries.csv*",
        conco3="**/??_7_*_timeseries.csv*",
        vmro3="**/??_7_*_timeseries.csv*",
        vmro3max="**/??_7_*_timeseries.csv*",
        concno2="**/??_8_*_timeseries.csv*",
        vmrno2="**/??_8_*_timeseries.csv*",
        concco="**/??_10_*_timeseries.csv*",
        concno="**/??_38_*_timeseries.csv*",
        concpm25="**/??_6001_*_timeseries.csv*",
        concSso2="**/??_1_*_timeseries.csv*",
        concNno2="**/??_8_*_timeseries.csv*",
        concNno="**/??_38_*_timeseries.csv*",
    )

    # conversion factor between concX and vmrX
    CONV_FACTOR = {}

    CONV_FACTOR["concSso2"] = np.float64(0.50052292274792)
    CONV_FACTOR["concNno2"] = np.float64(0.3044517868011477)
    CONV_FACTOR["concNno"] = np.float64(0.466788868521913)
    CONV_FACTOR["vmro3"] = np.float64(
        0.493
    )  # retrieved using STD atmosphere from geonum and pya.mathutils.concx_to_vmrx
    CONV_FACTOR["vmro3max"] = np.float64(
        0.493
    )  # retrieved using STD atmosphere from geonum and pya.mathutils.concx_to_vmrx
    CONV_FACTOR["vmrno2"] = np.float64(
        0.514
    )  # retrieved using STD atmosphere from geonum and pya.mathutils.concx_to_vmrx

    # unit of the converted property after the conversion
    CONV_UNIT = {}
    CONV_UNIT["concSso2"] = "µgS/m3"
    CONV_UNIT["concNno2"] = "µgN/m3"
    CONV_UNIT["concNno"] = "µgN/m3"
    CONV_UNIT["vmro3"] = "ppb"
    CONV_UNIT["vmro3max"] = "ppb"
    CONV_UNIT["vmrno2"] = "ppb"

    #: field name of the start time of the measurement (in lower case)
    START_TIME_NAME = "datetimebegin"

    #: filed name of the end time of the measurement (in lower case)
    END_TIME_NAME = "datetimeend"

    #: dictionary that connects the EEA variable codes with aerocom variable names
    VAR_CODES = {}
    VAR_CODES["1"] = "concso2"
    VAR_CODES["5"] = "concpm10"
    VAR_CODES["7"] = "conco3"
    VAR_CODES["8"] = "concno2"
    VAR_CODES["10"] = "concco"
    VAR_CODES["38"] = "concno"
    VAR_CODES["6001"] = "concpm25"

    #: column name that holds the EEA variable code
    VAR_CODE_NAME = "airpollutantcode"

    #: List of variables that are provided by this dataset (will be extended
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    PROVIDES_VARIABLES = list(VAR_NAMES_FILE)

    #: there's no general instrument name in the data
    INSTRUMENT_NAME = "unknown"

    #: max time steps to read per file (hourly data)
    # to make numpy array allocation size static
    MAX_LINES_TO_READ = 24 * 366

    #: file name of the metadata file
    #: this will be prepended with a data path later on
    # this file is in principe updated once a day.
    # so we night consider updating it from within the code later on.
    # URL: https://discomap.eea.europa.eu/map/fme/metadata/PanEuropean_metadata.csv
    DEFAULT_METADATA_FILE = "metadata.csv"

    #: Name of latitude variable in metadata file
    LATITUDENAME = "latitude"

    #: name of longitude variable in metadata file
    LONGITUDENAME = "longitude"

    #: name of altitude variable in metadata file
    ALTITUDENAME = "altitude"

    #: this class reads the European Environment Agency's Eionet data
    #: for details please read
    #: https://www.eea.europa.eu/about-us/countries-and-eionet
    WEBSITE = "https://discomap.eea.europa.eu/map/fme/AirQualityExport.htm"

    #: Eionet offers 2 data revisions
    #: E2a (near real time) and E1a (quality controlled)
    #: this class reads the E2a data for now.
    # But by changing the base path
    # and this constant, it can also read the E1a data set
    DATA_PRODUCT = ""

    AUX_REQUIRES = {
        "vmro3max": ["conco3"],
        "vmro3": ["conco3"],
        "vmrno2": ["concno2"],
        "concNno2": ["concno2"],
        "concNno": ["concno"],
        "concSso2": ["concso2"],
    }

    AUX_FUNS = {
        "vmro3": NotImplementedError(),
        "vmro3max": NotImplementedError(),
        "vmrno2": NotImplementedError(),
        "concNno2": NotImplementedError(),
        "concNno": NotImplementedError(),
        "concSso2": NotImplementedError(),
    }

    def __init__(self, data_id=None, data_dir=None):
        super().__init__(data_id=data_id, data_dir=data_dir)
        self._metadata = None

    @property
    def DEFAULT_VARS(self):
        """List of default variables"""
        return [self.VAR_CODES["7"]]

    @property
    def DATASET_NAME(self):
        """Name of the dataset"""
        return self.data_id

    def read_file(self, filename, var_name, vars_as_series=False):
        """Read a single EEA file

        Note that there's only a single variable in the file

        Parameters
        ----------
        filename : str
            Absolute path to filename to read.
        var_name : str
            Name of variable in file.
        vars_as_series : bool
            If True, the data columns of all variables in the result dictionary
            are converted into pandas Series objects.

        Returns
        -------
        StationData
            Dict-like object containing the results.

        """
        if var_name not in self.PROVIDES_VARIABLES:
            raise ValueError(f"Invalid input variable {var_name}")

        # there's only one variable in the file
        aerocom_var_name = var_name

        # Iterate over the lines of the file
        logger.info(f"Reading file {filename}")
        file_delimiter = self.FILE_COL_DELIM
        # this lists the data to keep from the original read string
        # this becomes a time series
        file_indexes_to_keep = [11, 13, 14, 15, 16]
        # used for line length control...
        max_file_index_to_keep = max(file_indexes_to_keep)
        # this is some header information
        header_indexes_to_keep = [
            0,
            3,
            8,
            9,
            10,
            12,
        ]
        # These are the indexes with a time and are stored as np.datetime64
        time_indexes = [13, 14]

        # read the file
        # enable alternative reading of .gz files here to save space on the file system
        suffix = pathlib.Path(filename).suffix
        if suffix == ".gz":
            f_out = tempfile.NamedTemporaryFile(delete=False)
            with gzip.open(filename, "r") as f_in:
                shutil.copyfileobj(f_in, f_out)
            read_filename = f_out.name
            f_out.close()
        else:
            read_filename = filename

        # input files can be either UTF-8 or UTF-16 encoded
        # try both
        # files are max 3MB in size, so no big deal terms of RAM usage
        try:
            with open(read_filename) as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(read_filename, encoding="UTF-16") as f:
                lines = f.readlines()
        except Exception:
            if suffix == ".gz":
                os.remove(f_out.name)
            raise EEAv2FileError(f"Found corrupt file {filename}. consider deleting it")

        # remove the temp file in case the input file was a gz file
        if suffix == ".gz":
            os.remove(f_out.name)

        header = lines[0].lower().rstrip().split(file_delimiter)
        # create output dict
        if len(header) < max_file_index_to_keep:
            raise EEAv2FileError(f"Found corrupt file {filename}. consider deleting it")

        data_dict = {}
        for idx in header_indexes_to_keep:
            data_dict[header[idx]] = ""

        for idx in file_indexes_to_keep:
            if idx in time_indexes:
                data_dict[header[idx]] = np.zeros(self.MAX_LINES_TO_READ, dtype="datetime64[s]")
            else:
                data_dict[header[idx]] = np.empty(self.MAX_LINES_TO_READ, dtype=np.float64)

        # read the data...
        # DE,http://gdi.uba.de/arcgis/rest/services/inspire/DE.UBA.AQD,NET.DE_BB,STA.DE_DEBB054,DEBB054,SPO.DE_DEBB054_PM2_dataGroup1,SPP.DE_DEBB054_PM2_automatic_light-scat_Duration-30minute,SAM.DE_DEBB054_2,PM2.5,http://dd.eionet.europa.eu/vocabulary/aq/pollutant/6001,hour,3.2000000000,µg/m3,2020-01-04 00:00:00 +01:00,2020-01-04 01:00:00 +01:00,1,2
        lineidx = 0
        for line in lines[1:]:
            rows = line.rstrip().split(file_delimiter)
            # Unfortunately there's a lot of corrupt files
            # skip data line if the # rows is not sufficient
            if len(rows) < max_file_index_to_keep:
                continue
            if lineidx == 0:
                for idx in header_indexes_to_keep:
                    if header[idx] != self.VAR_CODE_NAME:
                        data_dict[header[idx]] = rows[idx]
                    else:
                        # extract the EEA var code from the URL noted in the data file
                        data_dict[header[idx]] = rows[idx].split("/")[-1]

            for idx in file_indexes_to_keep:
                # if the data is a time
                if idx in time_indexes:
                    # make the time string ISO compliant so that numpy can directly read it
                    # this is not very time string forgiving but fast
                    data_dict[header[idx]][lineidx] = np.datetime64(
                        rows[idx][0:10] + "T" + rows[idx][11:19]
                    )
                    # due to the deprecation of the timezone interpretation after numpy 0.11
                    # we have to subtract the offset manually to get to UTC.
                    # np.timedelta64 does not accept a float as parameter, only an integer.
                    # Although there are time zones with a 30 minutes offset, these don't
                    # exist in Europe, so just consider integer hours here for speed
                    tz_offset = np.timedelta64(np.int64(rows[idx][20:23]), "h")
                    data_dict[header[idx]][lineidx] = data_dict[header[idx]][lineidx] - tz_offset
                else:
                    # data is not a time
                    # sometimes there's no value in the file. Set that to nan
                    try:
                        data_dict[header[idx]][lineidx] = np.float64(rows[idx])
                    except (ValueError, IndexError):
                        data_dict[header[idx]][lineidx] = np.nan

            lineidx += 1
        # if the first line in the file was empty
        if data_dict["unitofmeasurement"] == "":
            if rows[12] == "":
                raise EEAv2FileError(
                    f"Unit of Measurement could not be inferred from EEA file {filename}"
                )
            else:
                # with loss of generality get the unitofmeasurement from the last row column 12 (which should be a kept header)
                data_dict["unitofmeasurement"] = rows[12]

        unit_in_file = data_dict["unitofmeasurement"]
        # adjust the unit and apply conversion factor in case we read a variable noted in self.AUX_REQUIRES
        if var_name in self.AUX_REQUIRES:
            unit_in_file = self.CONV_UNIT[var_name]
            data_dict[self.VAR_NAMES_FILE[var_name]] = (
                data_dict[self.VAR_NAMES_FILE[var_name]] * self.CONV_FACTOR[var_name]
            )
        try:
            unit = self.VAR_UNITS_FILE[unit_in_file]
        except KeyError:
            # this will raise an Exception if pyaerocom.units cannot handle. In
            # which case the unit should be added in VAR_UNITS_FILE
            unit = str(Unit(unit_in_file))

        # Empty data object (a dictionary with extended functionality)
        data_out = StationData()
        data_out.data_id = self.data_id
        data_out.dataset_name = self.DATASET_NAME
        data_out.station_id = data_dict["airqualitystation"]
        data_out.station_name = data_dict["airqualitystation"]
        data_out.filename = filename
        data_out.instrument_name = self.INSTRUMENT_NAME
        data_out.country_code = data_dict["countrycode"]
        freq = data_dict["averagingtime"]
        try:
            tstype = self.TS_TYPES_FILE[freq]
        except KeyError:
            raise TemporalResolutionError(
                f"Found invalid ts_type {freq}. Please register in class header attr TS_TYPES_FILE"
            )

        data_out.ts_type = tstype
        # ToDo: check "variables" entry, it should not be needed anymore in UngriddedData
        data_out["variables"] = [aerocom_var_name]
        data_out["var_info"][aerocom_var_name] = {}
        data_out["var_info"][aerocom_var_name]["units"] = unit
        # TsType is
        # data_out['var_info'][aerocom_var_name]['ts_type'] = self.TS_TYPE

        # Sometimes the times in the data files are not ordered in time which causes problems when doing
        # time interpolations later on. Make sure that the data is ordered in time
        diff_unsorted = np.diff(data_dict[self.START_TIME_NAME])
        sort_flag = False
        # use a vectorised time_diff instead of scalar one as before
        time_diff = (
            data_dict[self.END_TIME_NAME][:lineidx] - data_dict[self.START_TIME_NAME][:lineidx]
        ) / 2.0

        # np.min needs an array and fails with ValueError when a scalar is supplied
        # this is the case for a single line file
        try:
            min_diff = np.min(diff_unsorted)
        except ValueError:
            min_diff = 0

        if min_diff < 0:
            # data needs to be sorted
            ordered_idx = np.argsort(data_dict[self.START_TIME_NAME][:lineidx])
            data_out["dtime"] = (
                data_dict[self.START_TIME_NAME][ordered_idx] + time_diff[ordered_idx]
            )
            sort_flag = True
        else:
            data_out["dtime"] = data_dict[self.START_TIME_NAME][:lineidx] + time_diff

        for key, value in data_dict.items():
            # adjust the variable name to aerocom standard
            if key != self.VAR_NAMES_FILE[aerocom_var_name]:
                data_out[key] = value[:lineidx]
            else:
                if sort_flag:
                    data_out[aerocom_var_name] = value[:lineidx][ordered_idx]
                else:
                    data_out[aerocom_var_name] = value[:lineidx]

        # convert data vectors to pandas.Series (if attribute
        # vars_as_series=True)
        if vars_as_series:
            data_out[aerocom_var_name] = pd.Series(
                data_out[aerocom_var_name], index=data_out["dtime"]
            )

        return data_out

    def _read_metadata_file(self, filename=None):
        """Read EEA metadata file

        Parameters
        ----------
        filename : str
            Absolute path to filename to read.

        Returns
        -------
        metadata
            Dict-like object containing the results with the keys being a combination of the
            station name and the variable and the values being all fields of the metadata file

        """

        if filename is None:
            filename = os.path.join(self.data_dir, self.DEFAULT_METADATA_FILE)
            # test also for a gzipped file...
        if not os.path.isfile(filename):
            filename = filename + ".gz"
        logger.warning(f"Reading file {filename}")

        struct_data = {}
        suffix = pathlib.Path(filename).suffix
        if suffix == ".gz":
            f_out = tempfile.NamedTemporaryFile(delete=False)
            with gzip.open(filename, "r") as f_in:
                shutil.copyfileobj(f_in, f_out)
            filename = f_out.name
            f_in.close()

        with open(filename) as f:
            # read header...
            # Countrycode Timezone Namespace   AirQualityNetwork AirQualityStation AirQualityStationEoICode   AirQualityStationNatCode   SamplingPoint  SamplingProcess Sample   AirPollutantCode  ObservationDateBegin ObservationDateEnd   Projection  Longitude   Latitude Altitude MeasurementType   AirQualityStationType   AirQualityStationArea   EquivalenceDemonstrated MeasurementEquipment InletHeight BuildingDistance  KerbDistance
            header = f.readline().lower().rstrip().split()
            min_row_no = len(header)
            # create output dict
            data_dict = {}
            for key in header:
                data_dict[key] = []
            lineidx = 0
            bad_line_no = 0
            bad_line_arr = []
            for line in f:
                rows = line.rstrip().split("\t")
                # skip too short lines
                if len(rows) < min_row_no:
                    # print(line)
                    bad_line_no += 1
                    bad_line_arr.append(line)
                    continue
                temp_dict = {}
                for idx, key in enumerate(header):
                    if header[idx] != self.VAR_CODE_NAME:
                        # data_dict[header[idx]] = rows[idx]
                        temp_dict[header[idx]] = rows[idx]
                    else:
                        # extract the EEA var code from the URL noted in the data file
                        # data_dict[header[idx]] = rows[idx].split('/')[-1]
                        temp_dict[header[idx]] = rows[idx].split("/")[-1]

                meta_key = f"{temp_dict['airqualitystation']}__{temp_dict['airpollutantcode']}"
                if meta_key not in struct_data:
                    struct_data[meta_key] = temp_dict.copy()
                else:
                    pass
                lineidx += 1

        logger.info(f"Reading file {filename} done")
        # remove the temp file in case the input file was a gz file
        if suffix == ".gz":
            f_out.close()
            os.remove(f_out.name)

        return struct_data

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

        if pattern is None:
            logger.warning("using default pattern *.* for file search")
            pattern = "*.*"

        logger.info("Fetching data files. This might take a while...")
        fp = os.path.join(self.data_dir, pattern)
        return sorted(glob.glob(fp, recursive=True))

    def get_station_coords(self, meta_key):
        """
        get a station's coordinates

        Parameters
        ----------
        meta_key : str
            string with the internal station key
        """
        ret_data = {}
        ret_data["latitude"] = float(self._metadata[meta_key][self.LATITUDENAME])
        ret_data["longitude"] = float(self._metadata[meta_key][self.LONGITUDENAME])
        ret_data["altitude"] = float(self._metadata[meta_key][self.ALTITUDENAME])
        return ret_data

    def read(
        self, vars_to_retrieve=None, files=None, first_file=None, last_file=None, metadatafile=None
    ):
        """Method that reads list of files as instance of :class:`UngriddedData`

        Parameters
        ----------
        vars_to_retrieve : :obj:`list` or similar, optional
            List containing variable IDs that are supposed to be read. If None,
            all variables in :attr:`PROVIDES_VARIABLES` are loaded.
        files : :obj:`list`, optional
            List of files to be read. If None, then the file list used is the
            returned from :func:`get_file_list`.
        first_file : :obj:`int`, optional
            Index of the first file in :obj:'file' to be read. If None, the
            very first file in the list is used.
        last_file : :obj:`int`, optional
            Index of the last file in :obj:'file' to be read. If None, the very
            last file in the list is used.
        metadatafile : :obj:'str', optional
            full qualified path to metadata file. If None, the default metadata
            file will be used

        Returns
        -------
        UngriddedData
            data object
        """

        if vars_to_retrieve is None:
            vars_to_retrieve = self.DEFAULT_VARS
        elif isinstance(vars_to_retrieve, str):
            vars_to_retrieve = [vars_to_retrieve]

        if len(vars_to_retrieve) > 1:
            raise NotImplementedError("So far, only one variable can be read at a time...")
        var_name = vars_to_retrieve[0]
        logger.info("Reading EEA data")
        if files is None:
            logger.info("Retrieving file list")
            files = self.get_file_list(self.FILE_MASKS[var_name])

        if first_file is None:
            first_file = 0
        if last_file is None:
            last_file = len(files)

        if metadatafile is None:
            metadatafile = os.path.join(self.data_dir, self.DEFAULT_METADATA_FILE)

        files = files[first_file:last_file]

        data_obj = UngriddedData()
        meta_key = 0.0
        idx = 0

        # Assign metadata object and index
        metadata = data_obj.metadata
        meta_idx = data_obj.meta_idx

        logger.info("Reading metadata file")
        # non compliant, but efficiently indexed metadata
        self._metadata = self._read_metadata_file(metadatafile)

        # returns a dict with country codes as keys and the country names as value
        _country_dict = get_country_name_from_iso()
        logger.info("Reading files...")

        for i in tqdm(range(len(files)), disable=None):
            _file = files[i]
            try:
                station_data = self.read_file(_file, var_name=var_name)
            except EEAv2FileError:
                logger.warning(f"file {_file} is corrupt! consider deleting it")
                continue
            except TemporalResolutionError as e:
                logger.warning(f"{_file} has TemporalResolutionError")
                logger.warning(f"{repr(e)}. Skipping file...")
                continue

            # readfile might fail outside of the error captured by the try statement above
            if station_data is None:
                logger.warning(f"file {_file} did not provide data. skipping...!")
                continue

            # to find the metadata quickly, we use a string internally
            _meta_key = f"{station_data['station_id']}__{station_data['airpollutantcode']}"

            # Fill the metadata dict.
            # The location in the data set is time step dependant
            if _meta_key not in self._metadata:
                logger.warning(
                    f"metadata for station {_meta_key} not found! skipping that station!"
                )
                continue
            metadata[meta_key] = {}
            meta_idx[meta_key] = {}
            metadata[meta_key].update(station_data.get_meta())
            metadata[meta_key].update(self.get_station_coords(_meta_key))
            metadata[meta_key]["variables"] = list(
                station_data.var_info.keys()
            )  # vars_to_retrieve
            metadata[meta_key]["station_classification"] = self._metadata[_meta_key][
                "airqualitystationtype"
            ]
            metadata[meta_key]["area_classification"] = self._metadata[_meta_key][
                "airqualitystationarea"
            ]
            try:
                metadata[meta_key]["country"] = _country_dict[metadata[meta_key]["country_code"]]
            except KeyError:
                pass
            metadata[meta_key]["var_info"] = station_data["var_info"]
            metadata[meta_key]["website"] = self.WEBSITE
            metadata[meta_key]["data_product"] = self.DATA_PRODUCT
            metadata[meta_key]["station_name"] = self._metadata[_meta_key][
                "airqualitystationeoicode"
            ]

            # List with indices of this station for each variable
            num_times = len(station_data["dtime"])

            # Check whether the size of the data object needs to be extended
            if (idx + num_times) >= data_obj._ROWNO:
                # if totnum < data_obj._CHUNKSIZE, then the latter is used
                data_obj.add_chunk(num_times)

            for var_idx, var in enumerate(list(station_data.var_info)):
                # set invalid data to np.nan according to
                # https://dd.eionet.europa.eu/vocabulary/aq/observationvalidity/view
                # data flagged as below the detection limit (values 2 and 3)
                # will remain in the data
                station_data[var][station_data["validity"] < 1] = np.nan

                values = station_data[var]
                start = idx + var_idx * num_times
                stop = start + num_times

                data_obj._data[start:stop, data_obj._METADATAKEYINDEX] = meta_key
                data_obj._data[start:stop, data_obj._TIMEINDEX] = station_data["dtime"]
                data_obj._data[start:stop, data_obj._DATAINDEX] = values
                data_obj._data[start:stop, data_obj._VARINDEX] = var_idx
                meta_idx[meta_key][var] = np.arange(start, stop)

                if var not in data_obj.var_idx:
                    data_obj.var_idx[var] = var_idx

            idx += num_times
            meta_key = meta_key + 1.0

        # Shorten data_obj._data to the right number of points
        data_obj._data = data_obj._data[:idx]
        # data_obj.data_revision[self.DATASET_NAME] = self.data_revision
        self._metadata = None
        self.files = files

        return data_obj
