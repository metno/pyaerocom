import getpass
import logging
import os
from configparser import ConfigParser
from pathlib import Path

import numpy as np

from pyaerocom import obs_io
from pyaerocom._lowlevel_helpers import (
    check_dir_access,
    check_write_access,
    chk_make_subdir,
    list_to_shortstr,
)
from pyaerocom.data import resources
from pyaerocom.exceptions import DataIdError, DataSourceError
from pyaerocom.grid_io import GridIO
from pyaerocom.region_defs import ALL_REGION_NAME, HTAP_REGIONS, OLD_AEROCOM_REGIONS
from pyaerocom.varcollection import VarCollection
from pyaerocom.variable import Variable

logger = logging.getLogger(__name__)


class Config:
    """Class containing relevant paths for read and write routines

    A loaded instance of this class is created on import of pyaerocom and
    can be accessed via `pyaerocom.const`.

    TODO: provide more information
    """

    # NAMES
    # default names of the different obs networks
    # might get overwritten from paths.ini see func read_config

    #: ICP Forests
    ICPFORESTS_NAME = "ICPFORESTS"

    #: Aeronet Sun V2 access names
    AERONET_SUN_V2L15_AOD_DAILY_NAME = "AeronetSunV2Lev1.5.daily"
    AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME = "AeronetSun_2.0_NRT"
    AERONET_SUN_V2L2_AOD_DAILY_NAME = "AeronetSunV2Lev2.daily"
    AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME = "AeronetSunV2Lev2.AP"

    #: Aeronet SDA V2 access names
    AERONET_SUN_V2L2_SDA_DAILY_NAME = "AeronetSDAV2Lev2.daily"
    AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME = "AeronetSDAV2Lev2.AP"

    # Aeronet V2 inversion products
    AERONET_INV_V2L15_DAILY_NAME = "AeronetInvV2Lev1.5.daily"
    AERONET_INV_V2L15_ALL_POINTS_NAME = "AeronetInvV2Lev1.5.AP"
    AERONET_INV_V2L2_DAILY_NAME = "AeronetInvV2Lev2.daily"
    AERONET_INV_V2L2_ALL_POINTS_NAME = "AeronetInvV2Lev2.AP"

    #: Aeronet Sun V3 access names
    AERONET_SUN_V3L15_AOD_DAILY_NAME = "AeronetSunV3Lev1.5.daily"
    AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME = "AeronetSunV3Lev1.5.AP"
    AERONET_SUN_V3L2_AOD_DAILY_NAME = "AeronetSunV3Lev2.daily"
    AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME = "AeronetSunV3Lev2.AP"

    #: Aeronet SDA V3 access names
    AERONET_SUN_V3L15_SDA_DAILY_NAME = "AeronetSDAV3Lev1.5.daily"
    AERONET_SUN_V3L15_SDA_ALL_POINTS_NAME = "AeronetSDAV3Lev1.5.AP"
    AERONET_SUN_V3L2_SDA_DAILY_NAME = "AeronetSDAV3Lev2.daily"
    AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME = "AeronetSDAV3Lev2.AP"

    #: Aeronet V3 inversions
    AERONET_INV_V3L15_DAILY_NAME = "AeronetInvV3Lev1.5.daily"
    AERONET_INV_V3L2_DAILY_NAME = "AeronetInvV3Lev2.daily"

    # : CAMS2_83 name
    CAMS2_83_NRT_NAME = "CAMS2_83.NRT"

    #: EBAS name
    EBAS_MULTICOLUMN_NAME = "EBASMC"

    #: EEA nmea
    EEA_NAME = "EEAAQeRep"

    #: EEA.NRT name
    EEA_NRT_NAME = "EEAAQeRep.NRT"

    #: EEAV2 name
    EEA_V2_NAME = "EEAAQeRep.v2"

    #: Earlinet access name
    EARLINET_NAME = "EARLINET"

    #: EPROFILE access name
    EPROFILE_NAME = "EPROFILE"

    #: GAW TAD subset aas et al paper
    GAWTADSUBSETAASETAL_NAME = "GAWTADsubsetAasEtAl"

    #: DMS
    DMS_AMS_CVO_NAME = "DMS_AMS_CVO"

    #: CNEMC name (formally MEP)
    CNEMC_NAME = "CNEMC"

    #: ICOS name
    ICOS_NAME = "ICOS"

    # TROPOMI access names
    TROPOMI_XEMEP_R01x01_NAME = "TROPOMI_XEMEP_R01x01"

    TROPOMI_COBRA_XEMEP_R01x01_NAME = "TROPOMI_COBRA_XEMEP_R01x01"

    # basename of paths.ini
    PATHS_INI_NAME = "paths.ini"

    #: boolean specifying whether EBAS DB is copied to local cache for faster
    #: access, defaults to True
    EBAS_DB_LOCAL_CACHE = True

    #: Lowest possible year in data
    MIN_YEAR = 0
    #: Highest possible year in data
    MAX_YEAR = 20000

    #: standard names for coordinates
    STANDARD_COORD_NAMES = ["latitude", "longitude", "altitude"]
    #: Information specifying default vertical grid for post processing of
    #: profile data. The values are in units of m.
    DEFAULT_VERT_GRID_DEF = dict(lower=0, upper=15000, step=250)
    #: maximum allowed RH to be considered dry
    RH_MAX_PERCENT_DRY = 40

    DEFAULT_REG_FILTER = f"{ALL_REGION_NAME}-wMOUNTAINS"

    #: Time resample strategies for certain cominations, first level refers
    #: to TO, second to FROM and values are minimum number of observations
    OBS_MIN_NUM_RESAMPLE = dict(
        yearly=dict(monthly=3),
        monthly=dict(daily=7),
        daily=dict(hourly=6),
        hourly=dict(minutely=15),
    )

    #: This boolean can be used to enable / disable the former (i.e. use
    #: available wavelengths of variable in a certain range around variable
    #: wavelength).
    OBS_ALLOW_ALT_WAVELENGTHS = obs_io.OBS_ALLOW_ALT_WAVELENGTHS

    #: Wavelength tolerance for observations imports
    OBS_WAVELENGTH_TOL_NM = obs_io.OBS_WAVELENGTH_TOL_NM

    CLIM_START = 2005
    CLIM_STOP = 2015
    CLIM_FREQ = "monthly"
    CLIM_RESAMPLE_HOW = "mean"  # median, ...
    # as a function of climatological frequency
    CLIM_MIN_COUNT = dict(
        daily=30,  # at least 30 daily measurements in each month over whole period
        monthly=5,  # analogue to daily ...
    )

    # names for the satellite data sets
    SENTINEL5P_NAME = "Sentinel5P"
    AEOLUS_NAME = "AeolusL2A"

    OLD_AEROCOM_REGIONS = OLD_AEROCOM_REGIONS

    URL_HTAP_MASKS = "https://pyaerocom.met.no/pyaerocom-suppl/htap_masks/"

    HTAP_REGIONS = HTAP_REGIONS

    RM_CACHE_OUTDATED = True

    #: Name of the file containing the revision string of an obs data network
    REVISION_FILE = "Revision.txt"

    #: timeout to check if one of the supported server locations can be
    #: accessed
    SERVER_CHECK_TIMEOUT = 1  # s

    #: Environment variable to declare the number of parallel workers to use when parallel processing is available. Currently implemented in :func:`pyaerocom.aeroval.coldatatojson_helpers.py::_process_stats_timeseries_for_all_regions`
    PYAEROCOM_NUM_WORKERS = "PYAEROCOM_NUM_WORKERS"

    def __init__(self, config_file=None, try_infer_environment=True):
        # Directories
        self._outputdir = None
        self._cache_basedir = None
        self._colocateddatadir = None
        self._logdir = None
        self._filtermaskdir = None
        self._local_tmp_dir = None
        self._downloaddatadir = None
        self._confirmed_access = []
        self._rejected_access = []

        # Options
        self._caching_active = True

        self._var_param = None
        self._coords = None

        # Custom variables
        self._custom_var_dict = None

        # Attributes that are used to store search directories
        self.OBSLOCS_UNGRIDDED = {}
        self.OBS_UNGRIDDED_POST = {}
        self.SUPPLDIRS = {}
        self._search_dirs = []

        self.WRITE_FILEIO_ERR_LOG = True

        self.last_config_file = None
        self._ebas_flag_info = None

        self._outhomename = "MyPyaerocom"

        with resources.path("pyaerocom.data", "paths.ini") as path:
            self._config_ini_lustre = str(path)
        with resources.path("pyaerocom.data", "variables.ini") as path:
            self._var_info_file = str(path)
        with resources.path("pyaerocom.data", "coords.ini") as path:
            self._coords_info_file = str(path)

        self._user = getpass.getuser()
        self.my_pyaerocom_dir = os.path.join(f"{os.path.expanduser('~')}", self._outhomename)

        self.DO_NOT_CACHE_FILE = None

        self.ERA5_SURFTEMP_FILENAME = "era5.msl.t2m.201001-201012.nc"

        self._LUSTRE_CHECK_PATH = "/"

        #: Settings for reading and writing of gridded data
        self.GRID_IO = GridIO()

        if config_file is not None:
            if not os.path.exists(config_file):
                raise FileNotFoundError(f"input config file does not exist {config_file}")
            elif not config_file.endswith("ini"):
                raise ValueError("Need path to an ini file for input config_file")

            basedir, config_file = os.path.split(config_file)
        elif try_infer_environment:
            try:
                config_file = self.infer_config()
            except FileNotFoundError:
                pass

        if config_file is not None:
            try:
                self.read_config(
                    config_file,
                )
            except Exception as e:
                logger.warning(f"Failed to read config. Error: {repr(e)}")
        # create MyPyaerocom directory
        chk_make_subdir(self.HOMEDIR, self._outhomename)

    def _check_access(self, loc, timeout=None):
        """Uses multiprocessing approach to check if location can be accessed

        Parameters
        ----------
        loc : str
            path that is supposed to be checked

        Returns
        -------
        bool
            True, if location is accessible, else False
        """
        if loc is None:
            return False
        loc = str(Path(loc))  # make sure the path is set correctly
        if loc in self._confirmed_access:
            return True
        elif loc in self._rejected_access:
            return False

        logger.info(f"Checking access to: {loc}")
        if check_dir_access(loc):
            self._confirmed_access.append(loc)
            return True
        self._rejected_access.append(loc)
        return False

    def _basedirs_search_db(self):
        return [self.ROOTDIR, self.HOMEDIR]

    def _infer_config_from_basedir(self, basedir):
        basedir = os.path.normpath(basedir)
        for env_id, chk_sub in self._check_subdirs_cfg.items():
            chkdir = os.path.join(basedir, chk_sub)
            if self._check_access(chkdir):
                return (self._config_files[env_id], env_id)

        raise FileNotFoundError(
            f"Could not infer environment configuration for input directory: {basedir}"
        )

    def infer_config(self):
        """
        check if ~/MyPyaerocom/paths.ini exists.
        if not, use the default paths.ini
        """

        self._paths_ini = os.path.join(self.my_pyaerocom_dir, self.PATHS_INI_NAME)
        if os.path.exists(self._paths_ini):
            logger.info(f"using user specific config file: {self._paths_ini}")
        else:
            with resources.path("pyaerocom.data", self.PATHS_INI_NAME) as path:
                self._paths_ini = str(path)
                logger.info(f"using default config file: {self._paths_ini}")

        return self._paths_ini

    def register_custom_variables(
        self, vars: dict[str, Variable] | dict[str, dict[str, str]]
    ) -> None:
        var_dict = {}
        for key, item in vars.items():
            if isinstance(item, Variable):
                var_dict[key] = item
            elif isinstance(item, dict):
                if "var_name" in item and "units" in item:
                    var_dict[key] = Variable(**item)
                else:
                    raise ValueError(
                        f"Dict item {item} must at least have the keys 'var_name' and 'units'"
                    )
            else:
                raise ValueError(f"Item {item} must be either dict or Variable")
        self._custom_var_dict = var_dict.copy()
        self._var_param = None

    @property
    def has_access_users_database(self):
        chk_dir = self._check_subdirs_cfg["users-db"]
        chk_paths = [
            os.path.join("/metno/aerocom_users_database/", chk_dir),
            os.path.join(self.HOMEDIR, "/aerocom_users_database/", chk_dir),
        ]
        for p in chk_paths:
            if self._check_access(p):
                return True
        return False

    @property
    def has_access_lustre(self):
        """Boolean specifying whether MetNO AeroCom server is accessible"""
        for path in self._search_dirs:
            if self._LUSTRE_CHECK_PATH in path and self._check_access(path):
                return True
        return False

    @property
    def ALL_DATABASE_IDS(self):
        """ID's of available database configurations"""
        return list(self._config_files)

    @property
    def ROOTDIR(self):
        """Local root directory"""
        return os.path.abspath(os.sep)

    @property
    def HOMEDIR(self):
        """Home directory of user"""
        return os.path.expanduser("~") + "/"

    @property
    def OUTPUTDIR(self):
        """Default output directory"""
        self._outputdir = chk_make_subdir(self.HOMEDIR, self._outhomename)
        return self._outputdir

    @property
    def DATA_SEARCH_DIRS(self):
        """
        Directories which pyaerocom will consider for data access

        Note
        ----
        This corresponds to directories considered for searching gridded
        data (e.g. models and level 3 satellite products).  Please
        see :attr:`OBSLOCS_UNGRIDDED` for available data directories
        for reading of ungridded data.

        Returns
        -------
        list
            list of directories

        """
        return self._search_dirs

    @property
    def FILTERMASKKDIR(self):
        if not check_write_access(self._filtermaskdir):
            outdir = self.OUTPUTDIR
            self._filtermaskdir = chk_make_subdir(outdir, "filtermasks")
        return self._filtermaskdir

    @property
    def COLOCATEDDATADIR(self):
        """Directory for accessing and saving colocated data objects"""
        if not check_write_access(self._colocateddatadir):
            outdir = self.OUTPUTDIR
            self._colocateddatadir = chk_make_subdir(outdir, "colocated_data")
        return self._colocateddatadir

    @property
    def LOCAL_TMP_DIR(self):
        """Local TEMP directory"""
        if self._local_tmp_dir is None:
            self._local_tmp_dir = f"{self.OUTPUTDIR}/tmp"
        if not self._check_access(self._local_tmp_dir):
            os.makedirs(self._local_tmp_dir, exist_ok=True)
        return self._local_tmp_dir

    @LOCAL_TMP_DIR.setter
    def LOCAL_TMP_DIR(self, val):
        self._local_tmp_dir = val

    @property
    def DOWNLOAD_DATADIR(self):
        """Directory where data is downloaded into"""
        if self._downloaddatadir is None:
            self._downloaddatadir = chk_make_subdir(self.OUTPUTDIR, "data")
        return self._downloaddatadir

    @DOWNLOAD_DATADIR.setter
    def DOWNLOAD_DATADIR(self, val):
        if not isinstance(val, str):
            raise ValueError("Please provide str")
        elif not os.path.exists(val):
            try:
                os.mkdir(val)
            except Exception:
                raise OSError(f"Input directory {val} does not exist and can also not be created")
        self._downloaddatadir = val

    @property
    def user(self):
        """User ID"""
        return getpass.getuser()

    @property
    def cache_basedir(self):
        """Base directory for caching

        The actual files are cached in user subdirectory, cf :attr:`CACHEDIR`
        """
        cd = self._cache_basedir
        if not check_write_access(cd):
            outdir = self.OUTPUTDIR
            cd = chk_make_subdir(outdir, "_cache")
            self._cache_basedir = cd
        return cd

    @cache_basedir.setter
    def cache_basedir(self, val):
        if not check_write_access(val):
            raise ValueError(val)
        self._cache_basedir = os.path.abspath(val)

    @property
    def CACHEDIR(self):
        """Cache directory for UngriddedData objects"""
        try:
            return chk_make_subdir(self.cache_basedir, self.user)
        except Exception as e:
            logger.warning(f"Failed to access CACHEDIR: {repr(e)}\nDeactivating caching")
            self._caching_active = False

    @CACHEDIR.setter
    def CACHEDIR(self, val):
        """Cache directory"""
        if not check_write_access(val):
            raise ValueError(
                f"Cannot set cache directory. "
                f"Input directory {val} does not exist or write permission is not granted"
            )
        spl = os.path.split(val)
        if spl[-1] == self.user:
            val = spl[0]
        self._cache_basedir = val

    @property
    def CACHING(self):
        """Activate writing of and reading from cache files"""
        return self._caching_active

    @CACHING.setter
    def CACHING(self, val):
        self._caching_active = bool(val)

    @property
    def VAR_PARAM(self):
        """Deprecated name, please use :attr:`VARS` instead"""
        logger.warning("Deprecated (but still functional) name VAR_PARAM. Please use VARS")
        return self.VARS

    @property
    def VARS(self):
        """Instance of class VarCollection (for default variable information)"""
        if self._var_param is None:  # has not been accessed before
            self._var_param = VarCollection(self._var_info_file)

            if self._custom_var_dict is not None:
                for var in self._custom_var_dict:
                    self._var_param.add_var(self._custom_var_dict[var])
        return self._var_param

    @property
    def COORDINFO(self):
        """Instance of :class:`VarCollection` containing coordinate info"""
        if self._coords is None:
            self._coords = VarCollection(self._coords_info_file)
        return self._coords

    @property
    def LOGFILESDIR(self):
        """Directory where logfiles are stored"""
        if self._logdir is None:
            self._logdir = chk_make_subdir(self.OUTPUTDIR, "_log")
        return self._logdir

    @property
    def ETOPO1_AVAILABLE(self):
        """
        Boolean specifying if access to ETOPO1 dataset is provided

        Returns
        -------
        bool
        """
        if "etopo1" in self.SUPPLDIRS and os.path.exists(self.SUPPLDIRS["etopo1"]):
            return True
        return False

    @property
    def EBAS_FLAGS_FILE(self):
        """Location of CSV file specifying meaning of EBAS flags"""
        with resources.path("pyaerocom.data", "ebas_flags.csv") as path:
            return str(path)

    @property
    def OBS_IDS_UNGRIDDED(self):
        """List of all data IDs of supported ungridded observations"""
        ids = list(self.OBSLOCS_UNGRIDDED)
        ids.extend(self.OBS_UNGRIDDED_POST)
        return ids

    @property
    def ERA5_SURFTEMP_FILE(self):
        if "era5" in self.SUPPLDIRS:
            sdir = self.SUPPLDIRS["era5"]
            if os.path.exists(sdir) and self.ERA5_SURFTEMP_FILENAME in os.listdir(sdir):
                return os.path.join(sdir, self.ERA5_SURFTEMP_FILENAME)
        raise FileNotFoundError(
            "ERA Interim surface temperature data cannot be accessed (check lustre connection)"
        )

    def make_default_vert_grid(self):
        """Makes default vertical grid for resampling of profile data"""
        step = self.DEFAULT_VERT_GRID_DEF["step"]
        offs = int(step / 2)
        return np.arange(
            self.DEFAULT_VERT_GRID_DEF["lower"] + offs,
            self.DEFAULT_VERT_GRID_DEF["upper"] - offs,
            step,
        )

    def add_data_search_dir(self, *dirs):
        """Add data search directories for database browsing"""
        for loc in dirs:
            if not self._check_access(loc):
                raise FileNotFoundError(f"Input location {loc} could not be accessed")
            self._search_dirs.append(loc)

    def add_ungridded_obs(self, obs_id, data_dir, reader=None, check_read=False):
        """Add a network to the data search structure

        Parameters
        ----------
        obs_id : str
            name of network. E.g. MY_OBS or EBASMC
        data_dir : str
            directory where data files are stored
        reader : pyaerocom.io.ReadUngriddedBase, optional
            reading class used to import these data. If `obs_id` is known
            (e.g. EBASMC) this is not needed.

        Raises
        ------
        AttributeError
            if the network name is already reserved in :attr:`OBSLOCS_UNGRIDDED`
        ValueError
            if the data directory does not exist
        """
        if obs_id in self.OBS_IDS_UNGRIDDED:
            raise DataIdError(
                f"Network with ID {obs_id} is already registered at "
                f"{self.OBSLOCS_UNGRIDDED[obs_id]}"
            )
        elif not self._check_access(data_dir):
            raise ValueError("Input data directory cannot be accessed")
        if reader is None:
            from pyaerocom.io.utils import get_ungridded_reader

            reader = get_ungridded_reader(obs_id)

        if obs_id not in reader.SUPPORTED_DATASETS:
            reader.SUPPORTED_DATASETS.append(obs_id)
        self.OBSLOCS_UNGRIDDED[obs_id] = data_dir
        if check_read:
            self._check_obsreader(obs_id, data_dir, reader)

    def add_ungridded_post_dataset(
        self,
        obs_id,
        obs_vars,
        obs_aux_requires,
        obs_merge_how,
        obs_aux_funs: dict[str, str] | None = None,
        obs_aux_units=None,
        **kwargs,
    ):
        """
        Register new ungridded dataset

        Other than :func:`add_ungridded_obs`, this method adds required logic
        for a "virtual" ungridded observation datasets, that is, a dataset that
        can only be computed from other ungridded datasets but not read from
        disk.

        If all input parameters are okay, the new dataset will be registered
        in :attr:`OBS_UNGRIDDED_POST` and will then be accessible for import
        in ungridded reading factory class :class:`pyaerocom.io.ReadUngridded`.

        Parameters
        ----------
        obs_id : str
            Name of new dataset.
        obs_vars : str or list
            variables supported by this dataset.
        obs_aux_requires : dict
            dictionary specifying required datasets and variables for each
            variable supported by the auxiliary dataset.
        obs_merge_how : str or dict
            info on how to derive each of the supported coordinates (e.g. eval,
            combine). For valid input args see
            :mod:`pyaerocom.combine_vardata_ungridded`. If value is string,
            then the same method is used for all variables.
        obs_aux_funs : dict[str, str], optional
            dictionary specifying computation methods for auxiliary variables
            that are supposed to be retrieved via `obs_merge_how='eval'`.
            Keys are variable names, values are respective computation methods
            passed to :mod:`pyaerocom.combine_vardata_ungridded`.
            The function only supports addition/multiplication/.. on two variables.
            This input is optional, but mandatory if any of the `obs_vars`
            is supposed to be retrieved via `merge_how='eval'`.
        obs_aux_units : dict, optional
            output units of auxiliary variables (only needed for variables
            that are derived via `merge_how='eval'`)
        **kwargs
            additional keyword arguments (unused, but serves the purpose to
            allow for parsing info from dictionaries and classes that
            contain additional attributes than the ones needed here).

        Raises
        ------
        ValueError
            if input obs_id is already reserved


        Returns
        -------
        None.

        """
        if obs_id in self.OBS_IDS_UNGRIDDED:
            raise ValueError(f"Network with ID {obs_id} is already registered...")
        elif obs_aux_units is None:
            obs_aux_units = {}
        # this class will do the required sanity checking and will only
        # initialise if everything is okay
        addinfo = obs_io.AuxInfoUngridded(
            data_id=obs_id,
            vars_supported=obs_vars,
            aux_requires=obs_aux_requires,
            aux_merge_how=obs_merge_how,
            aux_funs=obs_aux_funs,
            aux_units=obs_aux_units,
        )

        self.OBS_UNGRIDDED_POST[obs_id] = addinfo.to_dict()

    def _check_obsreader(self, obs_id, data_dir, reader):
        """
        Check if files can be accessed when registering new dataset

        Parameters
        ----------
        obs_id : str
            name of obsnetwork
        data_dir : str
            directory containing data files
        reader : ReadUngriddedBase
            reading interface
        """
        check = reader(obs_id)
        path = check.data_dir
        assert path == data_dir
        try:
            check.get_file_list()
        except DataSourceError:
            if "renamed" not in os.listdir(data_dir):
                raise
            logger.warning(
                f"Failed to register {obs_id} at {data_dir} using ungridded "
                f"reader {reader} but input dir has a renamed subdirectory, "
                f"trying to find valid data files in there instead"
            )
            chk_dir = os.path.join(data_dir, "renamed")
            self.OBSLOCS_UNGRIDDED.pop(obs_id)
            self.add_ungridded_obs(obs_id, chk_dir, reader, check_read=True)

    @property
    def ebas_flag_info(self):
        """Information about EBAS flags

        Note
        ----
        Is loaded upon request -> cf.
        :attr:`pyaerocom.io.ebas_nasa_ames.EbasFlagCol.FLAG_INFO`

        Dictionary containing 3 dictionaries (keys: ```valid, values, info```)
        that contain information about validity of each flag (```valid```),
        their actual values (```values```, e.g. V, M, I)
        """
        if self._ebas_flag_info is None:
            from pyaerocom.io.helpers import read_ebas_flags_file

            self._ebas_flag_info = read_ebas_flags_file(self.EBAS_FLAGS_FILE)
        return self._ebas_flag_info

    def reload(self, keep_basedirs=True):
        """Reload config file (for details see :func:`read_config`)"""
        self.read_config(self.last_config_file, keep_basedirs)

    def read_config(
        self,
        config_file,
        basedir=None,
        init_obslocs_ungridded=False,
        init_data_search_dirs=False,
    ):
        """
        Import paths from one of the config ini files

        Parameters
        ----------
        config_file : str
            file location of config ini file
        basedir : str, optional
            Base directory to be used for relative model and obs dirs specified
            via BASEDIR in config file. If None, then the BASEDIR value in the
            config file is used. The default is None.
        init_obslocs_ungridded : bool, optional
            If True, :attr:`OBSLOCS_UNGRIDDED` will be re-instantiated (i.e.
            all currently set obs locations will be deleted).
            The default is False.
        init_data_search_dirs : bool, optional
            If True, :attr:`DATA_SEARCH_DIRS` will be re-instantiated (i.e.
            all currently set data search directories will be deleted).
            The default is False.

        Raises
        ------
        FileNotFoundError
            If input config file is not a file or does not exist.

        Returns
        -------
        None.

        """

        if not os.path.isfile(config_file):
            raise FileNotFoundError(
                f"Configuration file paths.ini at {config_file} does not exist or is not a file"
            )

        if init_obslocs_ungridded:
            self.OBSLOCS_UNGRIDDED = {}
        if init_data_search_dirs:
            self._search_dirs = []

        cr = ConfigParser()
        cr.optionxform = str
        cr.read(config_file)
        # init base directories for Model data
        if cr.has_section("modelfolders"):
            self._add_searchdirs(cr, basedir)

        if cr.has_section("obsfolders"):
            self._add_obsconfig(cr, basedir)

        if cr.has_section("outputfolders"):
            self._init_output_folders_from_cfg(cr)

        if cr.has_section("supplfolders"):
            if basedir is None and "BASEDIR" in cr["supplfolders"]:
                basedir = cr["supplfolders"]["BASEDIR"]

            for name, path in cr["supplfolders"].items():
                if "${BASEDIR}" in path:
                    path = path.replace("${BASEDIR}", basedir)
                self.SUPPLDIRS[name] = path

        cr.clear()
        self.GRID_IO.load_aerocom_default()
        self.last_config_file = config_file

    def _resolve_basedir(self, locs, chk_dirs):
        repl = "${BASEDIR}"
        for loc in locs:
            if repl in loc:
                for chk_dir in chk_dirs:
                    chk = Path(loc.replace(repl, chk_dir))
                    if self._check_access(chk):
                        return chk_dir
        raise FileNotFoundError("Could not confirm any directory...")

    def _add_searchdirs(self, cr, basedir=None):
        chk_dirs = []
        if basedir is not None and self._check_access(basedir):
            chk_dirs.append(basedir)

        mcfg = cr["modelfolders"]

        # check and update model base directory if applicable
        if "BASEDIR" in mcfg:
            _dir = mcfg["BASEDIR"]
            if "${HOME}" in _dir:
                _dir = _dir.replace("${HOME}", os.path.expanduser("~"))
            elif "${USER}" in _dir:
                _dir = _dir.replace("${USER}", self._user)
            if _dir not in chk_dirs and self._check_access(_dir):
                chk_dirs.append(_dir)
        if len(chk_dirs) == 0:
            return False

        # get all locations defined in config file as list
        locs = mcfg["dir"].replace("\n", "").split(",")

        # find first location that contains BASEDIR to determine
        try:
            basedir = str(self._resolve_basedir(locs, chk_dirs))
        except FileNotFoundError:
            basedir = None
        repl_str = "${BASEDIR}"
        for loc in locs:
            if repl_str in loc:
                if basedir is None:
                    continue
                loc = loc.replace(repl_str, basedir)

            if loc not in self._search_dirs:
                self._search_dirs.append(loc)
        return True

    def _add_obsconfig(self, cr, basedir=None):
        chk_dirs = []
        if basedir is not None and self._check_access(basedir):
            chk_dirs.append(basedir)

        cfg = cr["obsfolders"]

        # check and update model base directory if applicable
        if "BASEDIR" in cfg:
            _dir = cfg["BASEDIR"]
            if "${HOME}" in _dir:
                _dir = _dir.replace("${HOME}", os.path.expanduser("~"))
            if "${USER}" in _dir:
                _dir = _dir.replace("${USER}", self._user)
            if _dir not in chk_dirs and self._check_access(_dir):
                chk_dirs.append(_dir)
        if len(chk_dirs) == 0:
            return False

        names_cfg = self._add_obsnames_config(cr)

        candidates = {}
        dirconfirmed = None
        repl = "${BASEDIR}"
        if cr.has_section("obsfolders"):
            for obsname, path in cr["obsfolders"].items():
                if obsname.lower() == "basedir":
                    continue
                name_str = f"{obsname.upper()}_NAME"
                if name_str in names_cfg:
                    ID = self.__dict__[name_str]
                else:
                    ID = self._add_obsname(obsname)
                candidates[ID] = path
                # candidate for checking access
                if dirconfirmed is None and repl in path:
                    for chk_dir in chk_dirs:
                        chk = Path(path.replace(repl, chk_dir))
                        if self._check_access(chk):
                            dirconfirmed = str(chk_dir)
        homedir = os.path.expanduser("~")
        for name, loc in candidates.items():
            if repl in loc:
                if dirconfirmed is None:
                    continue
                loc = loc.replace(repl, dirconfirmed)
            if "${HOME}" in loc:
                loc = loc.replace("${HOME}", homedir)

            self.OBSLOCS_UNGRIDDED[name] = loc

    def _init_output_folders_from_cfg(self, cr):
        cfg = cr["outputfolders"]
        if "CACHEDIR" in cfg and not self._check_access(self._cache_basedir):
            self._cache_basedir = cfg["CACHEDIR"]

        if "OUTPUTDIR" in cfg and not self._check_access(self._outputdir):
            self._outputdir = cfg["OUTPUTDIR"]

        if "COLOCATEDDATADIR" in cfg and not self._check_access(self._colocateddatadir):
            self._colocateddatadir = cfg["COLOCATEDDATADIR"]

        if "LOCALTMPDIR" in cfg:
            _dir = cfg["LOCALTMPDIR"]
            # expand ${HOME}
            if "${HOME}" in _dir:
                _dir = _dir.replace("${HOME}", os.path.expanduser("~"))
            if "${USER}" in _dir:
                _dir = _dir.replace("${USER}", getpass.getuser())

            self._local_tmp_dir = _dir

    def _add_obsname(self, name):
        name_str = f"{name.upper()}_NAME"
        self[name_str] = name
        return name_str

    def _add_obsnames_config(self, cr):
        names_cfg = []
        if cr.has_section("obsnames"):
            for obsname, ID in cr["obsnames"].items():
                name_str = f"{obsname.upper()}_NAME"
                self[name_str] = ID
                names_cfg.append(name_str)
        return names_cfg

    def short_str(self):
        """Deprecated method"""
        return self.__str__()

    def __setitem__(self, key, val):
        self.__dict__[key] = val

    def __str__(self):
        head = f"Pyaerocom {type(self).__name__}"
        s = f"\n{head}\n{len(head) * '-'}\n"
        for k, v in self.__dict__.items():
            if k.startswith("_"):
                pass
            if k == "VARS":
                s += f"\n{k}\n{list_to_shortstr(v.all_vars)}"
            elif isinstance(v, dict):
                s += f"\n{k} (dict)"
            elif isinstance(v, list):
                s += f"\n{k} (list)"
                s += list_to_shortstr(v)
            else:
                s += f"\n{k}: {v}"
        return s
