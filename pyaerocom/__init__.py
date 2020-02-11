from ._init_helpers import (_init_supplemental, _init_logger, 
                            check_requirements, LOGLEVELS, change_verbosity)
__version__, __dir__ = _init_supplemental()

logger, print_log = _init_logger()

(GEONUM_AVAILABLE, 
 BASEMAP_AVAILABLE) = check_requirements(logger)

# Imports
from . import _lowlevel_helpers
from . import obs_io
# custom toplevel classes
from .variable import Variable
from .region import Region
from .config import Config

const = Config()
    
from . import metastandards
from . import mathutils
from . import geodesy
from . import vert_coords

from .vertical_profile import VerticalProfile
from .stationdata import StationData
from .griddeddata import GriddedData
from .ungriddeddata import UngriddedData
from .filter import Filter
from .colocateddata import ColocatedData
from .colocation_auto import ColocationSetup, Colocator
from . import colocation

from . import io
from . import plot
from . import interactive
from . import web
from . import scripts

from .io.helpers import search_data_dir_aerocom
from .io.utils import browse_database
from .variable import get_variable
from .utils import create_varinfo_table

from .filter import Filter



