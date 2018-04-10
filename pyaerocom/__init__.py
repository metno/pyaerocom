def _init_supplemental():
    from pkg_resources import get_distribution
    from os.path import abspath, dirname
    return (get_distribution('pyaerocom').version, abspath(dirname(__file__)))

def import_test_files(proj_dir):
    """Load test files of models and observations stored in test_files.ini file
    
    The file should be available at the relative location:
        
        ./pyaerocom/data/test_files.ini
        
    Parameters
    ----------
    proj_dir : str
        project base directory (i.e. pyaerocom.__dir__)
        
    Returns
    -------
    dict
        dictionary containing two keys (`models`, `observations`), with 
        values being 2 dictionaries that contain pairs of `name` and
        test paths.
        
    Raises
    ------
    IOError
        if the test_files.ini file cannot be found in the specified loaction
        
    """
    try:
        from ConfigParser import ConfigParser
    except: 
        from configparser import ConfigParser
    from collections import OrderedDict
    from os.path import join, exists
    from warnings import warn
    fpath = join(proj_dir, "data", "test_files.ini")
    if not exists(fpath):
        raise IOError("File %s does not exist" %fpath)
    conf_reader = ConfigParser()
    conf_reader.read(fpath)
    result = OrderedDict()
    result["models"] = OrderedDict()
    result["observations"] = OrderedDict()
    
    for key, val in conf_reader["models"].items():
        result["models"][key] = val
        if not exists(val):
            warn("Default test path for model %s could not be found: %s"
                 %(key, val))
    for key, val in conf_reader["observations"].items():
        result["observations"][key] = val
        if not exists(val):
            warn("Default test path for model %s could not be found: %s"
                 %(key, val))
    return result

__version__, __dir__ = _init_supplemental()
test_files = import_test_files(__dir__)

from . import config
from . import mathutils

from . import io
from . import plot

from .region import Region
from .modeldata import ModelData
from .obsdata import ObsData, ProfileData, StationData

