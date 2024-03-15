import logging
from traceback import format_exc

from pyaerocom import const
from pyaerocom._lowlevel_helpers import BrowseDict, ListOfStrings, StrType
from pyaerocom.exceptions import InitialisationError
from pyaerocom.metastandards import DataSource

logger = logging.getLogger(__name__)


class ObsEntry(BrowseDict):
    """Observation configuration for evaluation (dictionary)

    Note
    ----
    Only :attr:`obs_id` and `obs_vars` are mandatory, the rest is optional.

    Attributes
    ----------
    obs_id : str
        ID of observation network in AeroCom database
        (e.g. 'AeronetSunV3Lev2.daily')
    obs_vars : list
        list of pyaerocom variable names that are supposed to be analysed
        (e.g. ['od550aer', 'ang4487aer'])
    obs_ts_type_read : :obj:`str` or :obj:`dict`, optional
        may be specified to explicitly define the reading frequency of the
        observation data (so far, this does only apply to gridded obsdata such
        as satellites). For ungridded reading, the frequency may be specified
        via :attr:`obs_id`, where applicable (e.g. AeronetSunV3Lev2.daily).
        Can be specified variable specific in form of dictionary.
    obs_vert_type : str, optional
        Aerocom vertical code encoded in the model filenames (only AeroCom 3
        and later).
    obs_aux_requires : dict, optional
        information about required datasets / variables for auxiliary
        variables.
    instr_vert_loc : str, optional
        vertical location code of observation instrument. This is used in
        the aeroval interface for separating different categories of measurements
        such as "ground", "space" or "airborne".
    is_superobs : bool
        if True, this observation is a combination of several others which all
        have to have their own obs config entry.
    only_superobs : bool
        this indicates whether this configuration is only to be used as part
        of a superobs network, and not individually.
    read_opts_ungridded : :obj:`dict`, optional
        dictionary that specifies reading constraints for ungridded reading
        (c.g. :class:`pyaerocom.io.ReadUngridded`).
    """

    SUPPORTED_VERT_CODES = ["Column", "Profile", "Surface"]  # , "2D"]
    ALT_NAMES_VERT_CODES = dict(ModelLevel="Profile")

    SUPPORTED_VERT_LOCS = DataSource.SUPPORTED_VERT_LOCS

    obs_vars = ListOfStrings()
    obs_vert_type = StrType()

    def __init__(self, **kwargs):
        self.obs_id = ""

        self.obs_vars = []
        self.obs_ts_type_read = None
        self.obs_vert_type = ""
        self.obs_aux_requires = {}
        self.instr_vert_loc = None

        self.is_superobs = False
        self.only_superobs = False
        self.colocation_layer_limts = None
        self.profile_layer_limits = None

        self.read_opts_ungridded = {}

        self.update(**kwargs)
        self.check_cfg()
        self.check_add_obs()

    def check_add_obs(self):
        """Check if this dataset is an auxiliary post dataset"""
        if len(self.obs_aux_requires) > 0:
            if not self.obs_type == "ungridded":
                raise NotImplementedError(
                    f"Cannot initialise auxiliary setup for {self.obs_id}. "
                    f"Aux obs reading is so far only possible for ungridded observations."
                )
            if not self.obs_id in const.OBS_IDS_UNGRIDDED:
                try:
                    const.add_ungridded_post_dataset(**self)
                except Exception:
                    raise InitialisationError(
                        f"Cannot initialise auxiliary reading setup for {self.obs_id}. "
                        f"Reason:\n{format_exc()}"
                    )

    def get_all_vars(self) -> list:
        """
        Get list of all variables associated with this entry

        Returns
        -------
        list
            DESCRIPTION.

        """
        return self.obs_vars

    def has_var(self, var_name):
        """
        Check if input variable is defined in entry

        Returns
        -------
        bool
            True if entry has variable available, else False
        """
        return True if var_name in self.get_all_vars() else False

    def get_vert_code(self, var):
        """Get vertical code name for obs / var combination"""
        vc = self["obs_vert_type"]
        if isinstance(vc, str):
            val = vc
        elif isinstance(vc, dict) and var in vc:
            val = vc[var]
        else:
            raise ValueError(f"invalid value for obs_vert_type: {vc}")
        if not val in self.SUPPORTED_VERT_CODES:
            raise ValueError(
                f"invalid value for obs_vert_type: {val}. Choose from "
                f"{self.SUPPORTED_VERT_CODES}."
            )
        return val

    def check_cfg(self):
        """Check that minimum required attributes are set and okay"""

        if not self.is_superobs and not isinstance(self.obs_id, (str, dict)):
            raise ValueError(
                f"Invalid value for obs_id: {self.obs_id}. Need str or dict "
                f"or specification of ids and variables via obs_compute_post"
            )
        if isinstance(self.obs_vars, str):
            self.obs_vars = [self.obs_vars]
        elif not isinstance(self.obs_vars, list):
            raise ValueError(f"Invalid input for obs_vars. Need list or str, got: {self.obs_vars}")
        ovt = self.obs_vert_type
        if ovt is None:
            raise ValueError(
                f"obs_vert_type is not defined. Please specify "
                f"using either of the available codes: {self.SUPPORTED_VERT_CODES}. "
                f"It may be specified for all variables (as string) "
                f"or per variable using a dict"
            )
        elif isinstance(ovt, str) and not ovt in self.SUPPORTED_VERT_CODES:
            self.obs_vert_type = self._check_ovt(ovt)
        elif isinstance(self.obs_vert_type, dict):
            for var_name, val in self.obs_vert_type.items():
                if not val in self.SUPPORTED_VERT_CODES:
                    raise ValueError(
                        f"Invalid value for obs_vert_type: {self.obs_vert_type} "
                        f"(variable {var_name}). Supported codes are {self.SUPPORTED_VERT_CODES}."
                    )
        ovl = self.instr_vert_loc
        if isinstance(ovl, str) and not ovl in self.SUPPORTED_VERT_LOCS:
            raise AttributeError(
                f"Invalid value for instr_vert_loc: {ovl} for {self.obs_id}. "
                f"Please choose from: {self.SUPPORTED_VERT_LOCS}"
            )

    def _check_ovt(self, ovt):
        """Check if obs_vert_type string is valid alias

        Parameters
        ----------
        ovt : str
            obs_vert_type string

        Returns
        -------
        str
            valid obs_vert_type

        Raises
        ------
        ValueError
            if `ovt` is invalid
        """
        if ovt in self.ALT_NAMES_VERT_CODES:
            _ovt = self.ALT_NAMES_VERT_CODES[ovt]
            logger.warning(f"Please use {_ovt} for obs_vert_code and not {ovt}")
            return _ovt
        valid = self.SUPPORTED_VERT_CODES + list(self.ALT_NAMES_VERT_CODES)
        raise ValueError(
            f"Invalid value for obs_vert_type: {self.obs_vert_type}. "
            f"Supported codes are {valid}."
        )
