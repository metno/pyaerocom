from pydantic import BaseModel
import datetime
from getpass import getuser

from pyaerocom import __version__


class ExperimentInfo(BaseModel):
    exp_id: str
    exp_name: str = ""
    exp_descr: str = ""
    public: bool = False
    exp_pi: str = getuser()
    pyaerocom_version: str = __version__
    creation_date: str = f"{datetime.datetime.now(datetime.timezone.utc):%Y-%m-%dT%H:%M:%S.%fZ}"
