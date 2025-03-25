from pyaerocom._lowlevel_helpers import dict_to_str
from pyaerocom.units.datetime.time_config import TS_TYPES


class GridIO:
    """Global I/O settings for gridded data

    This class includes options related to the import of gridded data. This
    includes both options related to file search as well as preprocessing
    options.

    Attributes
    ----------
    FILE_TYPE : str
        file type of data files. Defaults to .nc
    TS_TYPES : list
        list of strings specifying temporal resolution options encrypted in
        file names.
    PERFORM_FMT_CHECKS : bool
        perform formatting checks when reading netcdf data, using metadata
        encoded in filenames (requires that NetCDF file follows a registered
        naming convention)
    DEL_TIME_BOUNDS : bool
        if True, preexisting bounds on time are deleted when grid data is
        loaded. Else, nothing is done. Aerocom default is True
    SHIFT_LONS : bool
        if True, longitudes are shifted to
        -180 <= lon <= 180 when data is loaded (in case they are defined
        0 <= lon <= 360. Aerocom default is True.
    CHECK_TIME_FILENAME : bool
        the times stored in NetCDF files may be wrong or not stored according
        to the CF conventions. If True, the times are checked and if
        :attr:`CORRECT_TIME_FILENAME`, corrected for on data import based what
        is encrypted in the
        file name. In case of Aerocom models, it is ensured that the filename
        contains both the year and the temporal resolution in the filenames
        (for details see :class:`pyaerocom.io.FileConventionRead`).
        Aerocom default is True
    CORRECT_TIME_FILENAME : bool
        if True and time dimension in data is found to be different from
        filename, it is attempted to be corrected
    EQUALISE_METADATA : bool
        if True (and if metadata varies between different NetCDF files that are
        supposed to be merged in time), the metadata in all loaded objects is
        unified based on the metadata of the first grid (otherwise,
        concatenating them in time might not work using the Iris interface).
        This might need to be reviewed and should be used with care if
        specific metadata aspects of individual files need to be accessed.
        Aerocom default is True
    USE_FILECONVENTION : bool
        if True, file names are strictly required to follow one of the file
        naming conventions that can be specified in the file
        `file_conventions.ini <https://github.com/metno/pyaerocom/tree/master/
        pyaerocom/data>`__. Aerocom default is True.
    INCLUDE_SUBDIRS : bool
        if True, search for files is expanded to all subdirecories included in
        data directory. Aerocom default is False.
    INFER_SURFACE_LEVEL : bool
        if True then surface level for 4D gridded data is inferred automatically
        when necessary (e.g. when extracting surface time series from 4D
        gridded data object that does not contain sufficient information about
        vertical dimension)

    """

    UNITS_ALIASES = {"/m": "m-1"}
    _AEROCOM = {
        "FILE_TYPE": ".nc",
        "PERFORM_FMT_CHECKS": True,
        "DEL_TIME_BOUNDS": True,
        "SHIFT_LONS": True,
        "CHECK_TIME_FILENAME": True,
        "CORRECT_TIME_FILENAME": True,
        "CHECK_DIM_COORDS": True,
        "EQUALISE_METADATA": True,
        "INCLUDE_SUBDIRS": False,
    }

    _DEFAULT = {
        "FILE_TYPE": ".nc",
        "PERFORM_FMT_CHECKS": True,
        "DEL_TIME_BOUNDS": True,
        "SHIFT_LONS": True,
        "CHECK_TIME_FILENAME": True,
        "CORRECT_TIME_FILENAME": True,
        "CHECK_DIM_COORDS": True,
        "EQUALISE_METADATA": True,
        "INCLUDE_SUBDIRS": False,
    }

    def __init__(self, **kwargs):
        self.FILE_TYPE = ".nc"
        # it is important to keep them in the order from highest to lowest
        # resolution
        self.TS_TYPES = TS_TYPES

        self.PERFORM_FMT_CHECKS = True

        # delete time bounds if they exist in netCDF files
        self.DEL_TIME_BOUNDS = True
        # shift longitudes to -180 -> 180 repr (if applicable)
        self.SHIFT_LONS = True

        self.CHECK_TIME_FILENAME = True
        self.CORRECT_TIME_FILENAME = True

        self.CHECK_DIM_COORDS = False
        # check and update metadata dictionary on Cube load since
        # iris concatenate of Cubes only works if metadata is equal

        self.EQUALISE_METADATA = True

        self.INCLUDE_SUBDIRS = False

        self.INFER_SURFACE_LEVEL = True

        self.load_default()

    def load_aerocom_default(self):
        self.from_dict(self._AEROCOM)

    def load_default(self):
        self.from_dict(self._DEFAULT)

    def to_dict(self):
        """Convert object to dictionary

        Returns
        -------
        dict
            settings dictionary
        """
        return self.__dict__

    def from_dict(self, dictionary=None, **settings):
        """Import settings from dictionary"""
        if not dictionary:
            dictionary = {}
        dictionary.update(settings)
        for key, val in dictionary.items():
            self[key] = val

    def __setitem__(self, key, value):
        """Set item

        GridIO["<key>"] = value <=> GridIO.<key> = value
        <=> GridIO.__setitem__(<key>, value)

        Raises
        ------
        IOError
            if key is not a valid setting
        """
        if key not in self.__dict__:
            raise OSError("Could not update IO setting: Invalid key")
        self.__dict__[key] = value

    def __getitem__(self, key):
        """Get item using curly brackets

        GridIO["<key>"] => value

        """
        if key not in self.__dict__:
            raise OSError("Invalid attribute")
        return self.__dict__[key]

    def __str__(self):
        head = f"Pyaerocom {type(self).__name__}"
        return "\n{}\n{}\n{}".format(head, len(head) * "-", dict_to_str(self.to_dict()))
