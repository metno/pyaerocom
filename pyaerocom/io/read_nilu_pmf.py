import fnmatch
import logging
import os
import re

import numpy as np
from geonum.atmosphere import T0_STD, p0
from tqdm import tqdm

from pyaerocom import const
from pyaerocom._lowlevel_helpers import BrowseDict
from pyaerocom.aux_var_helpers import (
    calc_vmro3max,
    compute_ac550dryaer,
    compute_ang4470dryaer_from_dry_scat,
    compute_sc440dryaer,
    compute_sc550dryaer,
    compute_sc700dryaer,
    compute_wetoxn_from_concprcpoxn,
    compute_wetoxs_from_concprcpoxs,
    compute_wetrdn_from_concprcprdn,
    concx_to_vmrx,
    vmrx_to_concx,
)
from pyaerocom.exceptions import (
    EbasFileError,
    MetaDataError,
    NotInFileError,
    TemporalResolutionError,
    TemporalSamplingError,
    UnitConversionError,
)
from pyaerocom.io.ebas_file_index import EbasFileIndex, EbasSQLRequest
from pyaerocom.io.ebas_nasa_ames import EbasNasaAmesFile
from pyaerocom.io.ebas_varinfo import EbasVarInfo
from pyaerocom.io.helpers import _check_ebas_db_local_vs_remote
from pyaerocom.io.read_ebas import ReadEbas, ReadEbasOptions
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.molmasses import get_molmass
from pyaerocom.stationdata import StationData
from pyaerocom.tstype import TsType
from pyaerocom.ungriddeddata import UngriddedData
from pyaerocom.units_helpers import get_unit_conversion_fac

logger = logging.getLogger(__name__)


class ReadNILUPMF(ReadUngriddedBase):
    """Interface for reading EBAS data

    Parameters
    ----------
    data_id
        string specifying either of the supported datasets that are defined
        in ``SUPPORTED_DATASETS``
    data_dir : str
        directory where data is located (NOTE: needs to point to the
        directory that contains the "ebas_file_index.sqlite3" file and not
        to the underlying directory "data" which contains the actual
        NASA Ames files.)

    TODO
    ----
    - Check for negative values vs. detection limit
    - Read uncertainties from percentiles (where available)
    """

    #: version log of this class (for caching)
    __version__ = "0.01_" + ReadUngriddedBase.__baseversion__

    #: Name of dataset (OBS_ID)
    DATA_ID = const.NILU_PMF_NAME

    #: Name of subdirectory containing data files (relative to
    #: :attr:`data_dir`)
    FILE_SUBDIR_NAME = "data"

    #: Name of sqlite database file
    # SQL_DB_NAME = "ebas_file_index.sqlite3"

    #: List of all datasets supported by this interface
    SUPPORTED_DATASETS = [const.NILU_PMF_NAME]

    #: For the following data IDs, the sqlite database file will be cached if
    #: const.EBAS_DB_LOCAL_CACHE is True
    # CACHE_SQLITE_FILE = [const.EBAS_MULTICOLUMN_NAME]

    TS_TYPE = "undefined"

    MERGE_STATIONS = {
        # "Birkenes": "Birkenes II",
        # "Rörvik": "Råö",
        # "Vavihill": "Hallahus",
        # "Virolahti II": "Virolahti III",
    }
    #'Trollhaugen'    : 'Troll'}
    #: Temporal resolution codes that (so far) can be understood by pyaerocom
    TS_TYPE_CODES = {
        "1mn": "minutely",
        "1h": "hourly",
        "1d": "daily",
        "1w": "weekly",
        "1mo": "monthly",
        "mn": "minutely",
        "h": "hourly",
        "d": "daily",
        "w": "weekly",
        "mo": "monthly",
    }

    PROVIDED_VAR = dict(
        concecff="eBCff",
        concecbb="eBCbb",
        concoc="OC",
        concec="EC",
        conclevoglucosan="levoglucosan",
    )

    #: variables required for computation of auxiliary variables
    AUX_REQUIRES = {}

    #: Meta information supposed to be migrated to computed variables
    AUX_USE_META = {}
    #: Functions supposed to be used for computation of auxiliary variables
    AUX_FUNS = {}

    #: Custom reading options for individual variables. Keys need to be valid
    #: attributes of :class:`ReadEbasOptions` and anything specified here (for
    #: a given variable) will be overwritten from the defaults specified in
    #: the options class.
    VAR_READ_OPTS = {}

    ASSUME_AAE_SHIFT_WVL = 1.0
    ASSUME_AE_SHIFT_WVL = 1  # .5

    #: list of EBAS data files that are flagged invalid and will not be imported
    IGNORE_FILES = []

    #: Ignore data columns in NASA Ames files that contain any of the listed
    #: attributes
    IGNORE_COLS_CONTAIN = ["fraction", "artifact"]

    # list of all available resolution codes (extracted from SQLite database)
    # 1d 1h 1mo 1w 4w 30mn 2w 3mo 2d 3d 4d 12h 10mn 2h 5mn 6d 3h 15mn

    #: List of variables that are provided by this dataset (will be extended
    #: by auxiliary variables on class init, for details see __init__ method of
    #: base class ReadUngriddedBase)
    def __init__(self, data_id=None, data_dir=None):

        super().__init__(data_id=data_id, data_dir=data_dir)

        self._opts = {"default": ReadEbasOptions()}

        # self.opts = ReadEbasOptions()
        #: loaded instances of aerocom variables (instances of
        #: :class:`Variable` object, is written in get_file_list
        self._loaded_aerocom_vars = {}

        #: loaded instances of variables in EBAS namespace (instances of
        #: :class:`EbasVarInfo` object, is updated in read_file
        self._loaded_ebas_vars = {}

        self._file_dir = None

        self.files_failed = []
        self._read_stats_log = BrowseDict()

        #: SQL database interface class used to retrieve file paths for vars
        self._file_index = None
        self.sql_requests = []

        #: original file lists retrieved for each variable individually using
        #: SQL request. Since some of the files in the lists for each variable
        #: might occur in multiple lists, these are merged into a single list
        #: self.files and information about which variables are to be extracted
        #: for each file is stored in attribute files_contain

        #: Originally retrieved file lists from SQL database, for each variable
        #: individually
        self._lists_orig = {}

        #: this is filled in method get_file_list and specifies variables
        #: to be read from each file
        self.files_contain = []

        self._all_stats = None

    @property
    def PROVIDES_VARIABLES(self):
        """List of variables provided by the interface"""
        return EbasVarInfo.PROVIDES_VARIABLES()
