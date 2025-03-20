from configparser import ConfigParser
from os.path import basename, splitext

from pyaerocom import const
from pyaerocom.data import resources
from pyaerocom.exceptions import FileConventionError
from pyaerocom.units.datetime import TsType


class FileConventionRead:
    """Class that represents a file naming convention for reading Aerocom files

    Attributes
    ----------
    name : str
        name of this convention (e.g. "aerocom3")
    file_sep : str
        filename delimiter for accessing different variables
    year_pos : int
        position of year information in filename after splitting using
        delimiter :attr:`file_sep`
    var_pos : int
        position of variable information in filename after splitting using
        delimiter :attr:`file_sep`
    ts_pos : int
        position of information of temporal resolution in filename after
        splitting using delimiter :attr:`file_sep`
    vert_pos : int
        position of information about vertical resolution of data
    data_id_pos : int
        position of data ID
    """

    _io_opts = const
    AEROCOM3_VERT_INFO = {
        "2d": ["surface", "column", "modellevel", "2d"],
        "3d": ["modellevelatstations"],
    }

    def __init__(
        self,
        name="aerocom3",
        file_sep="_",
        year_pos=None,
        var_pos=None,
        ts_pos=None,
        vert_pos=None,
        data_id_pos=None,
        from_file=None,
    ):
        self.name = name
        self.file_sep = file_sep

        self.year_pos = year_pos
        self.var_pos = var_pos
        self.ts_pos = ts_pos
        self.vert_pos = vert_pos
        self.data_id_pos = data_id_pos

        if from_file is not None:
            self.from_file(from_file)
        else:
            try:
                self.import_default(self.name)
            except Exception:
                pass

    @property
    def info_init(self):
        """Empty dictionary containing init values of infos to be
        extracted from filenames
        """
        return dict(
            year=None,
            var_name=None,
            ts_type=None,
            vert_code="",
            is_at_stations=False,
            data_id="",
        )

    def from_file(self, file):
        """Identify convention from a file

        Currently only two conventions (aerocom2 and aerocom3) exist that are
        identified by the delimiter used.

        Parameters
        ----------
        file : str
            file path or file name

        Returns
        -------
        FileConventionRead
            this object (with updated convention)

        Raises
        ------
        FileConventionError
            if convention cannot be identified

        Example
        -------
        >>> from pyaerocom.io import FileConventionRead
        >>> filename = 'aerocom3_CAM5.3-Oslo_AP3-CTRL2016-PD_od550aer_Column_2010_monthly.nc'
        >>> print(FileConventionRead().from_file(filename))
        <BLANKLINE>
        pyaeorocom FileConventionRead
        name: aerocom3
        file_sep: _
        year_pos: -2
        var_pos: -4
        ts_pos: -1
        vert_pos: -3
        data_id_pos: 1
        """

        if basename(file).count("_") >= 4:
            self.import_default("aerocom3")
        elif basename(file).count(".") >= 4:
            self.import_default("aerocom2")
        else:
            raise FileConventionError(
                f"Could not identify convention from input file {basename(file)}"
            )
        self.check_validity(file)
        return self

    def check_validity(self, file):
        """Check if filename is valid"""
        info = self.get_info_from_file(file)
        year = info["year"]
        if not TsType.valid(info["ts_type"]):
            raise FileConventionError(
                f"Invalid ts_type {info['ts_type']} in filename {basename(file)}"
            )
        elif not (const.MIN_YEAR <= year <= const.MAX_YEAR):
            raise FileConventionError(f"Invalid year {info['year']} in filename {basename(file)}")

    def _info_from_aerocom3(self, file: str) -> dict:
        """Extract info from filename Aerocom 3 convention

        Parameters
        -----------
        file : str
            netcdf file name

        Returns
        -------
        dict
            dictionary containing infos that were extracted from filename
        """
        # init result dictionary
        info = self.info_init

        spl = splitext(basename(file))[0].split(self.file_sep)
        # phase 3 file naming convention
        try:
            info["year"] = int(spl[self.year_pos])
        except Exception:
            raise FileConventionError(
                f"Failed to extract year information from file {basename(file)} "
                f"using file convention Aerocom 3 {self.name}"
            )
        try:
            # include vars for the surface

            if spl[self.vert_pos].lower() in self.AEROCOM3_VERT_INFO["2d"]:
                info["var_name"] = spl[self.var_pos]
            # also include 3d vars that provide station based data
            # and contain the string vmr in this case the variable name has to
            # be slightly changed to the  aerocom phase 2 naming
            elif spl[self.vert_pos].lower() in self.AEROCOM3_VERT_INFO["3d"]:
                if "vmr" in spl[self.var_pos]:
                    info["var_name"] = spl[self.var_pos].replace("vmr", "vmr3d")
                else:
                    info["var_name"] = spl[self.var_pos]
            else:
                raise FileConventionError(
                    f"Invalid file name (Aerocom 3 naming convention).\n{file}\n"
                    f"Invalid string identifier for vertical coordinate: {spl[self.vert_pos]}"
                )
        except Exception as e:
            raise FileConventionError(
                f"Failed to extract variable name from file {basename(file)} "
                f"using file convention {self.name}.\nError: {repr(e)}"
            )
        try:
            info["ts_type"] = spl[self.ts_pos]
        except Exception:
            raise FileConventionError(
                f"Failed to extract ts_type from file {basename(file)} "
                f"using file convention {self.name}"
            )
        try:
            info["vert_code"] = spl[self.vert_pos]
        except Exception:
            raise FileConventionError(
                f"Failed to extract vert_code from file {basename(file)} "
                f"using file convention {self.name}"
            )

        try:
            info["data_id"] = self.file_sep.join(spl[self.data_id_pos : self.var_pos])
        except Exception:
            raise FileConventionError(
                f"Failed to extract model name from file {basename(file)} "
                f"using file convention {self.name}"
            )
        if "atstations" in file.lower():
            info["is_at_stations"] = True
        return info

    def _info_from_aerocom2(self, file: str) -> dict:
        """Extract info from filename Aerocom 2 convention

        Parameters
        -----------
        file : str
            netcdf file name

        Returns
        -------
        dict
            dictionary containing infos that were extracted from filename
        """
        info = self.info_init
        if self.file_sep == ".":
            spl = basename(file).split(self.file_sep)
        else:
            spl = splitext(basename(file))[0].split(self.file_sep)
        try:
            info["year"] = int(spl[self.year_pos])
        except Exception:
            raise FileConventionError(
                f"Failed to extract year information from file {basename(file)} "
                f"using file convention {self.name}"
            )
        try:
            info["var_name"] = spl[self.var_pos]
        except Exception:
            raise FileConventionError(
                f"Failed to extract variable information from file {basename(file)} "
                f"using file convention {self.name}"
            )
        try:
            info["ts_type"] = spl[self.ts_pos]
        except Exception:
            raise FileConventionError(
                f"Failed to extract ts_type from file {basename(file)} "
                f"using file convention {self.name}"
            )

        try:
            info["data_id"] = ".".join(spl[self.data_id_pos : self.ts_pos])
        except Exception:
            raise FileConventionError(
                f"Failed to extract name from file {basename(file)} "
                f"using file convention {self.name}"
            )
        if "atstations" in file.lower():
            raise Exception(
                "Developers: please debug "
                "(file convention Aerocom 2 should not have atstations encoded in file name)"
            )
        return info

    def get_info_from_file(self, file: str) -> dict:
        """Identify convention from a file

        Currently only two conventions (aerocom2 and aerocom3) exist that are
        identified by the delimiter used.

        Parameters
        ----------
        file : str
            file path or file name

        Returns
        -------
        dict
            dictionary containing keys `year, var_name, ts_type` and
            corresponding variables, extracted from the filename

        Raises
        ------
        FileConventionError
            if convention cannot be identified

        Example
        -------
        >>> from pyaerocom.io import FileConventionRead
        >>> filename = 'aerocom3_CAM5.3-Oslo_AP3-CTRL2016-PD_od550aer_Column_2010_monthly.nc'
        >>> conv = FileConventionRead("aerocom3")
        >>> info = conv.get_info_from_file(filename)
        >>> for item in info.items(): print(item)
        ('year', 2010)
        ('var_name', 'od550aer')
        ('ts_type', 'monthly')
        ('vert_code', 'Column')
        ('is_at_stations', False)
        ('data_id', 'CAM5.3-Oslo_AP3-CTRL2016-PD')
        """
        if self.name == "aerocom3":
            return self._info_from_aerocom3(file)
        if self.name == "aerocom2":
            return self._info_from_aerocom2(file)
        raise FileConventionError(f"Unknown {self.name}")

    def string_mask(self, data_id, var, year, ts_type, vert_which=None):
        """Returns mask that can be used to identify files of this convention

        Parameters
        ----------
        data_id : str
            experiment ID (e.g. GISS-MATRIX.A2.CTRL)
        var : str
            variable string ID (e.g. "od550aer")
        year : int
            desired year of observation (e.g. 2012)
        ts_type : str
            string specifying temporal resolution (e.g. "daily")

        Example
        -------

        conf_aero2 = FileConventionRead(name="aerocom2")
        conf_aero3 = FileConventionRead(name="aerocom2")

        var = od550aer
        year = 2012
        ts_type = "daily"

        match_str_aero2 = conf_aero2.string_mask(var, year, ts_type)

        match_str_aero3 = conf_aero3.string_mask(var, year, ts_type)

        """
        if ts_type is None:
            ts_type = "*"
        if self.name == "aerocom2":
            if vert_which is not None:
                raise FileConventionError(
                    f"Specification of vert_which ({vert_which}) is not supported for "
                )

            return ".".join([".*", data_id, ts_type, var, str(year), "nc"])
        elif self.name == "aerocom3":
            if vert_which is None:
                vert_which = ".*"
            return "_".join([".*", data_id, var, vert_which, str(year), ts_type]) + ".nc"
        else:
            raise NotImplementedError(
                f"File matching mask for convention {self.name} not yet defined..."
            )

    def import_default(self, name: str):
        """Checks and load default information from database"""

        conf_reader = ConfigParser()
        with resources.path("pyaerocom.data", "file_conventions.ini") as path:
            conf_reader.read(path)
        if name not in conf_reader:
            raise NameError(f"No default available for {name}")
        self.name = name
        for key, val in conf_reader[name].items():
            if key in self.__dict__:
                try:
                    val = int(val)
                except Exception:
                    pass
                self.__dict__[key] = val

    def from_dict(self, new_vals):
        """Load info from dictionary

        Parameters
        ----------
        new_vals : dict
            dictionary containing information

        Returns
        -------
        self
        """
        for k, v in new_vals.items():
            if k in self.__dict__:
                self.__dict__[k] = v
        return self

    def to_dict(self):
        """Convert this object to ordered dictionary"""
        return dict(
            name=self.name,
            file_sep=self.file_sep,
            year_pos=self.year_pos,
            var_pos=self.var_pos,
            ts_pos=self.ts_pos,
            vert_pos=self.vert_pos,
            data_id_pos=self.data_id_pos,
        )

    def __repr__(self):
        return f"{self.name} {super().__repr__()}"

    def __str__(self):
        s = "\npyaeorocom FileConventionRead"
        for k, v in self.to_dict().items():
            s += f"\n{k}: {v}"
        return s
