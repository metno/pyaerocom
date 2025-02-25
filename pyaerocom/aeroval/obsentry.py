import logging
from pathlib import Path
from traceback import format_exc
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
    model_validator,
)

from pyaerocom import const
from pyaerocom.climatology_config import ClimatologyConfig
from pyaerocom._lowlevel_helpers import LayerLimits
from pyaerocom.exceptions import InitialisationError

logger = logging.getLogger(__name__)


SUPPORTED_VERT_CODES: tuple[
    str,
    str,
    str,
] = (
    "Column",
    "Profile",
    "Surface",
)

ALT_NAMES_VERT_CODES: dict = dict(ModelLevel="Profile")


SUPPORTED_VERT_LOCS: tuple[str, str, str] = (
    "ground",
    "space",
    "airborne",
)


class BulkOptions(BaseModel):
    #: Vars to be used to calculate fraction or product
    vars: tuple[str, str]
    #: Whether or not the bulk variable exist as a model var. If not, it will be calculated same way as obs vars
    model_exists: bool
    #: Is the result a product or fraction
    mode: Literal["product", "fraction"]
    #: Unit of result
    units: str

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )


class ObsEntry(BaseModel):
    """Observation configuration for evaluation (BaseModel)

    Note
    ----
    Only :attr:`obs_id` and `obs_vars` are mandatory, the rest are optional.

    Attributes
    ----------
    obs_id : str
        ID of observation network in AeroCom database
        (e.g. 'AeronetSunV3Lev2.daily')
        Note that this can also be a custom supplied obs_id if and only if bs_aux_requires is provided
    obs_vars : tuple[str, ...]
        tuple of pyaerocom variable names that are supposed to be analysed
        (e.g. ('od550aer', 'ang4487aer'))
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
    is_bulkfraction: bool
        If true numerator and denominator are colocated separately, before the fraction is calculated.
        For this to work, the numerator and denominator need to be given in bulk_options
    read_opts_ungridded : :obj:`dict`, optional
        dictionary that specifies reading constraints for ungridded reading
        (c.g. :class:`pyaerocom.io.ReadUngridded`).
    only_json : bool
        Only to be set if the obs entry already has colocated data files which were
        preprocessed outside of pyaerocom. Setting to True will skip the colcoation
        and just create the JSON output.
    coldata_dir : str
        Only to be set if the obs entry already has colocated data files which were
        preprocessed outside of pyaerocom. This is the directory in which the
        colocated data files are located.

    obs_use_climatology : ClimatologyConfig | bool, optional
        Configuration for climatology. If True is given, a default configuration is made.
        With False, climatology is turned off

    """

    ##   Pydantic ConfigDict
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        validate_assignment=True,
    )

    ## Pydantic structs

    ######################
    ## Required attributes
    ######################
    obs_vars: str | tuple[str, ...]
    obs_id: str | tuple[str, ...]
    ######################
    ## Optional attributes
    ######################
    obs_name: str | None = None  # not expected to be set directly, rather set by ObsCollection
    obs_ts_type_read: str | dict | None = None
    obs_vert_type: Literal["Column", "Profile", "Surface", "ModelLevel"] = "Surface"
    obs_aux_requires: dict[str, dict] = {}
    instr_vert_loc: str | None = None
    is_superobs: bool = False
    only_superobs: bool = False
    is_bulk: bool = False
    bulk_options: dict[str, BulkOptions] = {}
    colocation_layer_limts: tuple[LayerLimits, ...] | None = None
    profile_layer_limits: tuple[LayerLimits, ...] | None = None
    web_interface_name: str | None = None
    diurnal_only: bool = False
    obs_type: str | None = None

    read_opts_ungridded: dict = {}
    # attributes for reading colocated data files made outside of pyaerocom
    only_json: bool = False
    coldata_dir: str | Path | None = (
        None  # TODO: Would like this to be a Path but need to see if it will cause issues down the line
    )

    obs_use_climatology: ClimatologyConfig | bool = False

    #############
    ## Validators
    #############
    @field_validator("obs_vars")
    @classmethod
    def validate_obs_vars(cls, v):
        if isinstance(v, str):
            return (v,)
        return v

    @field_validator("instr_vert_loc")
    @classmethod
    def validate_instr_vert_loc(cls, v):
        if isinstance(v, str) and v not in SUPPORTED_VERT_LOCS:
            raise AttributeError(
                f"Invalid value for instr_vert_loc: {v} for {cls.obs_id}. "
                f"Please choose from: {SUPPORTED_VERT_LOCS}"
            )

    @field_validator("obs_vert_type")
    @classmethod
    def check_obs_vert_type(cls, ovt):
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
        if ovt in SUPPORTED_VERT_CODES:
            return ovt
        if ovt in ALT_NAMES_VERT_CODES:
            logger.warning(
                f"Please use {ALT_NAMES_VERT_CODES[ovt]} for obs_vert_code and not {ovt}"
            )
            ovt = ALT_NAMES_VERT_CODES[ovt]
            return ovt
        valid = SUPPORTED_VERT_CODES + list(ALT_NAMES_VERT_CODES)
        raise ValueError(f"Invalid value for obs_vert_type: {ovt}. Supported codes are {valid}.")

    @model_validator(mode="after")
    def check_cfg(self):
        if not self.is_superobs and not isinstance(self.obs_id, str | tuple | dict):
            raise ValueError(
                f"Invalid value for obs_id: {self.obs_id}. Need str, tuple, or dict "
                f"or specification of ids and variables via obs_compute_post"
            )
        if self.is_bulk:
            for var in self.obs_vars:
                if var not in self.bulk_options:
                    raise KeyError(f"Could not find bulk vars entry for {var}")

                elif len(self.bulk_options[var].vars) != 2:
                    raise ValueError(
                        f"(Only) 2 entries must be present for bulk vars to calculate fraction for {var}"
                    )

        self.check_add_obs()
        return self

    ##########
    ## Methods
    ##########

    def check_add_obs(self):
        """Check if this dataset is an auxiliary post dataset"""
        if len(self.obs_aux_requires) > 0:
            if not self.obs_type == "ungridded":
                raise NotImplementedError(
                    f"Cannot initialise auxiliary setup for {self.obs_id}. "
                    f"Aux obs reading is so far only possible for ungridded observations."
                )
            if self.obs_id not in const.OBS_IDS_UNGRIDDED:
                try:
                    const.add_ungridded_post_dataset(**self.model_dump())
                except Exception:
                    raise InitialisationError(
                        f"Cannot initialise auxiliary reading setup for {self.obs_id}. "
                        f"Reason:\n{format_exc()}"
                    )

    def get_all_vars(self) -> tuple[str, ...]:
        """
        Get a tuple of all variables associated with this entry

        Returns
        -------
        tuple[str, ...]
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
        vc = self.obs_vert_type
        if isinstance(vc, str):
            val = vc
        elif isinstance(vc, dict) and var in vc:
            val = vc[var]
        else:
            raise ValueError(f"invalid value for obs_vert_type: {vc}")
        if val not in SUPPORTED_VERT_CODES:
            raise ValueError(
                f"invalid value for obs_vert_type: {val}. Choose from {SUPPORTED_VERT_CODES}."
            )
        return val
