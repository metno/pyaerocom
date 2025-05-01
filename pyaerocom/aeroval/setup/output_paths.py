import os

from pathlib import Path

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


from pyaerocom import const
from pyaerocom.aeroval.modelmaps_helpers import CONTOUR, OVERLAY

PLOT_TYPE_OPTIONS = ({OVERLAY}, {CONTOUR}, {OVERLAY, CONTOUR})


class OutputPaths(BaseModel):
    """
    Setup class for output paths of json files and co-located data

    This interface generates all paths required for an experiment.

    Attributes
    ----------
    proj_id : str
        project ID
    exp_id : str
        experiment ID
    json_basedir : str, Path
    avdb_resource : str, Path, None
        An aerovaldb resource identifier as expected by aerovaldb.open()[1].
        If not provided, pyaerocom will fall back to using json_basedir, for
        backwards compatibility.

        [1] https://aerovaldb.readthedocs.io/en/latest/api.html#aerovaldb.open
    """

    # Pydantic ConfigDict
    model_config = ConfigDict(arbitrary_types_allowed=True)

    _JSON_SUBDIRS: list[str] = [
        "map",
        "ts",
        "ts/diurnal",
        "scat",
        "hm",
        "hm/ts",
        "contour",
        "profiles",
        "overlay",
    ]
    avdb_resource: Path | str | None = None

    json_basedir: Path | str = Field(
        default=os.path.join(const.OUTPUTDIR, "aeroval/data"), validate_default=True
    )
    coldata_basedir: Path | str = Field(
        default=os.path.join(const.OUTPUTDIR, "aeroval/coldata"), validate_default=True
    )

    @field_validator("json_basedir", "coldata_basedir")
    @classmethod
    def validate_basedirs(cls, v):
        if not os.path.exists(v):
            tmp = Path(v) if isinstance(v, str) else v
            tmp.mkdir(parents=True, exist_ok=True)
        return v

    proj_id: str
    exp_id: str

    def _check_init_dir(self, loc, assert_exists):
        if assert_exists and not os.path.exists(loc):
            os.makedirs(loc)
        return loc

    def get_coldata_dir(self, assert_exists=True):
        loc = os.path.join(self.coldata_basedir, self.proj_id, self.exp_id)
        return self._check_init_dir(loc, assert_exists)

    def get_json_output_dirs(self, assert_exists=True):
        out = {}
        base = os.path.join(self.json_basedir, self.proj_id, self.exp_id)
        for subdir in self._JSON_SUBDIRS:
            loc = self._check_init_dir(os.path.join(base, subdir), assert_exists)
            out[subdir] = loc
        # for cams2_83 the extra 'forecast' folder will contain the median scores if computed
        if self.proj_id == "cams2-83":
            loc = self._check_init_dir(os.path.join(base, "forecast"), assert_exists)
            out["forecast"] = loc
        return out
