def _init_supplemental():
    from pkg_resources import get_distribution
    from os.path import abspath, dirname
    return (get_distribution('pyaerocom').version, abspath(dirname(__file__)))

__version__, __dir__ = _init_supplemental()

from .ioconfig import IOConfig
config = IOConfig()

from . import glob
from . import mathutils
from . import multiproc

from . import io
from . import plot

from .variable import Variable
from .region import Region
from .modeldata import ModelData
from .obsdata import ObsData, ProfileData, StationData

 