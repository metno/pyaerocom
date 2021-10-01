from ._init_helpers import (_init_supplemental, _init_logger,
                            LOGLEVELS, change_verbosity)
__version__, __dir__ = _init_supplemental()

logger, print_log = _init_logger()

from .config import Config
const = Config()

# Imports
from . import _lowlevel_helpers
from . import obs_io
from . import metastandards
from . import vertical_profile
from . import mathutils
from . import geodesy
from . import region
from . import vert_coords
from . import stationdata
from . import griddeddata
from . import ungriddeddata
from . import colocation
from . import io
from . import plot
from . import web
from . import scripts
from . import var_groups

# custom toplevel classes
from .variable import Variable
from .region import Region
from .vertical_profile import VerticalProfile
from .stationdata import StationData
from .griddeddata import GriddedData
from .ungriddeddata import UngriddedData
from .filter import Filter
from .colocateddata import ColocatedData
from .colocation_auto import ColocationSetup, Colocator
from .tstype import TsType
from .time_resampler import TimeResampler
from .io.helpers import search_data_dir_aerocom
from .io.utils import browse_database
from .variable import get_variable
from .utils import create_varinfo_table
from .testdata_access import initialise as initialise_testdata
