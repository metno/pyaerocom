# isort:skip_file
from importlib import metadata

from ._logging import change_verbosity
from ._warnings import ignore_basemap_warning, ignore_earth_radius_warning

__version__ = metadata.version(__package__)

import iris

# Enable new iris functionality to suppress deprecation warning.
# https://scitools-iris.readthedocs.io/en/latest/generated/api/iris.html#iris.FUTURE
iris.FUTURE.save_split_attrs = True

try:
    iris.FUTURE.date_microseconds = True
except AttributeError:
    # Old iris version that doesn't support this override. Use old behaviour.
    pass

from .config import Config

# Instantiate default configuration
const = Config()
ignore_basemap_warning()
ignore_earth_radius_warning()

# Sub-packages
from . import io

from . import scripts

# Imports
from . import obs_io
from . import metastandards
from . import vertical_profile
from . import mathutils
from . import geodesy
from . import region_defs
from . import region

# from . import vert_coords
from . import stationdata
from . import griddeddata
from . import ungriddeddata
from . import colocation
from . import var_groups
from . import combine_vardata_ungridded
from . import helpers_landsea_masks
from . import helpers
from . import trends_helpers
from . import trends_engine

# custom toplevel classes
from .variable import Variable
from .region import Region
from .vertical_profile import VerticalProfile
from .stationdata import StationData
from .griddeddata import GriddedData
from .ungriddeddata import UngriddedData
from .colocation.colocated_data import ColocatedData
from .colocation.colocator import Colocator
from .colocation.colocation_setup import ColocationSetup
from .filter import Filter
from .units.datetime import TsType
from .time_resampler import TimeResampler
from .io.helpers import search_data_dir_aerocom
from .variable_helpers import get_variable
from .utils import create_varinfo_table

from . import aeroval

from .sample_data_access import download_minimal_dataset
