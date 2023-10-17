from pyaro_config import PyaroConfig

from pyaerocom_readers import TimeseriesReader
from pyaerocom_readers.csvreader import CSVTimeseriesReader

from pyaerocom.io.readungriddedbase import ReadUngriddedBase
from pyaerocom import UngriddedData

import numpy as np


class ReadPyaro(ReadUngriddedBase):
    __version__ = "0.0.1"

    def __init__(self, config: PyaroConfig) -> None:
        self.config: PyaroConfig = config
        self.reader: TimeseriesReader = config.engine
        self.converter = PyaroToUngriddedData(self.reader)

    """
    Definition of abstract methods from ReadUngriddedBase
    """

    def DATA_ID(self):
        return self.config.data_id

    def PROVIDES_VARIABLES(self):
        """
        return self.reader.get_variables()
        """
        return []

    def DEFAULT_VARS(self):
        return self.PROVIDES_VARIABLES

    def TS_TYPE(self):
        """
        To be provided by the reader or engine
        """
        return "undefined"

    def _FILEMASK(self):
        return self.config.filename_or_obj_or_url

    def SUPPORTED_DATASETS(self):
        return [self.data_id]

    def read(self, vars_to_retrieve=None, files=..., first_file=None, last_file=None):
        self._open_reader()
        return self.converter.read(vars_to_retrieve=vars_to_retrieve)

    def read_file(self, filename, vars_to_retrieve=None):
        return self.read(vars_to_retrieve)

    """
    Methods specisfic to this reader
    """

    def _open_reader(self) -> TimeseriesReader:
        filename = self.config.filename_or_obj_or_url
        filters = self.config.filters

        return self.reader.open_reader(filename, filters=filters)


class PyaroToUngriddedData:
    def __init__(self, reader: TimeseriesReader) -> None:
        self.data: UngriddedData = UngriddedData()
        self.reader: TimeseriesReader = reader

    def _convert_to_ungriddeddata(self):
        data_array = np.ones_like(self.data._data)
        pass

    def read(self, vars_to_retrieve=None):
        ...


if __name__ == "__main__":
    data_id = "csv_reader"

    config = PyaroConfig(
        data_id=data_id,
        filename_or_obj_or_url="/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/pyaerocom-readers/src/pyaerocom_readers/csvreader/testdata/csvReader_testdata.csv",
        filters=[],
    )
    reader = CSVTimeseriesReader()
    rp = ReadPyaro(reader, config)
