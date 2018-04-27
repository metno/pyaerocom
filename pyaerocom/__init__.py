def _init_supplemental():
    from pkg_resources import get_distribution
    from os.path import abspath, dirname
    return (get_distribution('pyaerocom').version, abspath(dirname(__file__)))


def _init_config():
    from .config import Config
    from socket import gethostname
    
    if gethostname() == 'aerocom-users-ng':
        print("Initiating global PATHS for Aerocom users server")
        bdir = "/metno/aerocom-users-database"
        const = Config(model_base_dir=bdir, 
                       obs_base_dir=bdir)        
    else:
        const = Config()
        
    return const

__version__, __dir__ = _init_supplemental()

const = _init_config()

from . import mathutils
from . import multiproc

from . import io
from . import plot

from .variable import Variable
from .region import Region
from .modeldata import ModelData
from .obsdata import ObsData, ProfileData, StationData

 