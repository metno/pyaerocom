from __future__ import annotations

import logging

from pyaro import list_timeseries_engines, open_timeseries
from pyaro.timeseries.Wrappers import VariableNameChangingReader

from pyaerocom.io.pyaro.postprocess import PostProcessingReader
from pyaerocom.io.pyaro.pyaro_config import PyaroConfig
from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom.ungriddeddata_structured import UngriddedDataStructured
from pyaro.timeseries import Reader

logger = logging.getLogger(__name__)


class ReadPyaro(ReadUngriddedBase):
    __version__ = "1.2.1"

    SUPPORTED_DATASETS = list(list_timeseries_engines().keys())

    def __init__(self, config: PyaroConfig) -> None:
        self.config: PyaroConfig = config

        self._check_id()

        self.converter = PyaroToUngriddedData(self.config)
        self.reader = self.converter.reader
        self._data_dir = self.config.filename_or_obj_or_url
        self._data_name = self.config.name
        self._data_id = self.config.name

    """
    Definition of abstract methods from ReadUngriddedBase
    """

    @property
    def DATA_ID(self):
        return self._data_name

    @property
    def PROVIDES_VARIABLES(self):
        """
        return self.reader.get_variables()
        """
        return self.reader.variables()

    @property
    def DEFAULT_VARS(self):
        return self.PROVIDES_VARIABLES

    @property
    def TS_TYPE(self):
        """
        To be provided by the reader or engine
        """
        return "undefined"

    @property
    def _FILEMASK(self):
        return self.config.filename_or_obj_or_url

    @staticmethod
    def get_pyaro_readers():
        return list_timeseries_engines()

    def read(self, vars_to_retrieve=None, files=..., first_file=None, last_file=None):
        return self.converter.read(vars_to_retrieve=vars_to_retrieve)

    def read_file(self, filename, vars_to_retrieve=None):
        return self.converter.read(vars_to_retrieve)

    def _check_id(self):
        avail_readers = list_timeseries_engines()
        if self.config.reader_id not in avail_readers:
            logger.warning(
                f"Could not find {self.config.reader_id} in list of available Pyaro readers: {avail_readers}"
            )


class PyaroToUngriddedData:
    def __init__(self, config: PyaroConfig) -> None:
        self.data: UngriddedDataStructured = UngriddedDataStructured()
        self.config = config
        self.reader: Reader = self._open_reader()

    def _open_reader(self) -> Reader:
        reader_id = self.config.reader_id
        if self.config.model_extra is not None:
            kwargs = self.config.model_extra
        else:
            kwargs = {}

        reader = open_timeseries(
            reader_id,
            self.config.filename_or_obj_or_url,
            filters=self.config.filters,
            **kwargs,
        )
        if self.config.name_map is not None:
            reader = VariableNameChangingReader(
                reader,
                self.config.name_map,
            )
        if self.config.post_processing is not None:
            reader = PostProcessingReader(
                reader,
                self.config.post_processing,
            )
        return reader

    def get_variables(self) -> list[str]:
        return self.reader.variables()

    def read(self, vars_to_retrieve=None) -> UngriddedDataStructured:
        allowed_vars = self.get_variables()
        if vars_to_retrieve is None:
            vars_to_retrieve = allowed_vars
        else:
            if isinstance(vars_to_retrieve, str):
                vars_to_retrieve = [vars_to_retrieve]

        vars_to_retrieve_clean = []
        for var in vars_to_retrieve:
            if var not in allowed_vars:
                logger.warning(
                    f"Variable {var} not in list over allowed variables for {self.config.reader_id}: {allowed_vars}"
                )
                continue
            vars_to_retrieve_clean.append(var)

        return UngriddedDataStructured.from_pyaro(
            self.config.name, self.reader, vars_to_retrieve_clean
        )
