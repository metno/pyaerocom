from .config import Config
import logging

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

###############################################################################
### LOGGING
# Note: configuration will be propagated to all child modules of
# pyaerocom, for details see 
# http://eric.themoritzfamily.com/learning-python-logging.html
logger = logging.getLogger('pyaerocom')


default_formatter = logging.Formatter(\
   "%(asctime)s:%(levelname)s:\n%(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(default_formatter)

logger.addHandler(console_handler)

logger.setLevel(logging.DEBUG)

LOGLEVELS = {'debug': 10,
             'info': 20,
             'warning': 30,
             'error': 40,
             'critical': 50}

###############################################################################

const = _init_config(__dir__)
if not const.READY:
    print("WARNING: Failed to initiate data directories")
    
from . import mathutils
from . import multiproc

from .griddeddata import GriddedData
from .ungriddeddata import UngriddedData

from . import io
from . import plot
from . import utils

# custom toplevel class
from .variable import Variable
from .region import Region

#from .ungriddeddata import UngriddedData
from .io.helpers import search_data_dir_aerocom
#from .obsdata import ObsData, ProfileData, StationData



