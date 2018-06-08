from .config import Config

def _init_supplemental():
    from pkg_resources import get_distribution
    from os.path import abspath, dirname
    return (get_distribution('pyaerocom').version, abspath(dirname(__file__)))


def _init_config(package_dir):
    from socket import gethostname
    from os.path import join
    if gethostname() == 'aerocom-users-ng':
        print("Initiating global PATHS for Aerocom users server")
        cfg = join(package_dir, 'data', 'paths_user_server.ini')
    else:
        cfg = join(package_dir, 'data', 'paths.ini')
    return Config(config_file=cfg)

__version__, __dir__ = _init_supplemental()

const = _init_config(__dir__)
if not const.READY:
    print("WARNING: Failed to initiate data directories")
    
from . import mathutils
from . import multiproc

from . import io
from . import plot

# custom toplevel class and method im
from .variable import Variable
from .region import Region

from .griddeddata import GriddedData
#from .ungriddeddata import UngriddedData
from .io.helpers import search_data_dir_aerocom
#from .obsdata import ObsData, ProfileData, StationData