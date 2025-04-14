from collections.abc import Iterator
from abc import ABC, abstractmethod
import datetime
import os
import pathlib

from pyaerocom.griddeddata import GriddedData
from pyaerocom.io.gridded_reader import GriddedReader
from pyaerocom.exceptions import MissingOptionalDependencyError

import sys

from pyaerocom.units.datetime.tstype import TsType
from pyaerocom.variable_helpers import get_variable

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

import logging
from typing import NamedTuple

import glob

# TODO: Make dependency actually optional
try:
    import rasterio
except ImportError as e:
    raise MissingOptionalDependencyError("rasterio") from e

logger = logging.getLogger(__name__)


class FileMetadata(NamedTuple):
    file_path: str
    var: str
    tstype: TsType
    year: int
    start_time: datetime.datetime
    end_time: datetime.datetime


class FileMetadataExtractor(ABC):
    """Defines an interface for extracting metadata from a file path, which can be used
    to override file metadata extraction.
    """

    @abstractmethod
    def __call__(self, file: os.PathLike) -> FileMetadata: ...


class DefaultFileMetadataExtractor(FileMetadataExtractor):
    """Simple extraction of metadata. It will.
    - Ignore anything except the base name.
    - Split it by '_'.
    - See if any element matches a variable name in variables.ini
    - See if any element is a year (ie. 4digit number)

    This will only work for yearly data.

    :param FileMetadataExtractor: Metadata for the file.

    """

    @override
    def __call__(self, fp: os.PathLike) -> FileMetadata:
        base_name = pathlib.Path(fp).stem.lower()

        var: str | None = None
        tstype: TsType | None = None
        year: int | None = None
        start_time: datetime.datetime | None = None
        end_time: datetime.datetime | None = None

        for v in base_name.split("_"):
            if len(v) == 4 and v.isdigit():
                # Assume year of data.
                if tstype is not None:
                    logger.warning(
                        f"Multiple possible years found in file name '{base_name}'. Only the first one will be used."
                    )
                    continue

                tstype = TsType("yearly")
                year = int(v)
                start_time = datetime.datetime(year=year, month=1, day=1)
                end_time = datetime.datetime(year=year + 1, month=1, day=1)

            else:
                # Check if recognizable variable name.
                try:
                    get_variable(v)
                except Exception:
                    continue

                if var is not None:
                    logger.warning(
                        f"Multiple possible variable names found in file name '{base_name}'. Only the first one will be used."
                    )
                    continue

                var = v

        if any([x is None for x in [var, tstype, year, start_time, end_time]]):
            # TODO: Clean up exception.
            raise Exception("Unable to extract metadata.")

        return FileMetadata(str(fp), var, tstype, year, start_time, end_time)  # type: ignore


class FileFilter(ABC):
    @abstractmethod
    def __call__(self, data_dir: str) -> list[os.PathLike]: ...


class DefaultFileFilter(FileFilter):
    def __call__(self, data_dir: str) -> list[os.PathLike]:
        assert isinstance(data_dir, str)

        if "*" in data_dir:
            # Assuming glob.
            logger.info(f"Assuming '{data_dir}' to be a glob pattern...")
            return list(glob.glob(data_dir))

        if os.path.isfile(data_dir):
            logger.info(f"'{data_dir}' is a file. Returning file...")
            return [data_dir]

        if os.path.isdir(data_dir):
            logger.info(f"Assuming '{data_dir}' to be a directory. Returning all files in dir.")

            return list(glob.glob(f"{glob.escape(data_dir)}/*"))

        assert False


class RastorioReader(GriddedReader):
    """
    This reader provides an interface for reading Gridded data supported by rasterio.
    While the goal is that all drivers should work it has only been tested with
    geotiff so far.

    Currently it's behaviour can be customized by overriding the following strategies:
    - A file filter can be provided which is a callable that receives all files in data_dir,
    selecting the valid file.
    - A file metadata extractor can be provided which extracts metadata for each file name.

    Parameters:
    -----------
    data_id : str
        string ID of model (e.g. "AATSR_SU_v4.3","CAM5.3-Oslo_CTRL2016")
    data_dir : str, optional
        TODO: Write Documentation.
    """

    def __init__(
        self,
        data_id: str | None = None,
        data_dir: str | None = None,
        *,
        file_filter: FileFilter | None = None,
        file_metadata_extractor: FileMetadataExtractor | None = None,
    ) -> None:
        self._data_id = data_id
        self._data_dir = data_dir

        self._fmetadata_extractor = file_metadata_extractor
        if self._fmetadata_extractor is None:
            self._fmetadata_extractor = DefaultFileMetadataExtractor()

        self._file_filter = file_filter
        if self._file_filter is None:
            self._file_filter = DefaultFileFilter()

    @property
    def _files(self) -> list[os.PathLike]:
        # TODO: Consider caching if this is ever used on lots of files.
        return self._file_filter(self._data_dir)

    @property
    def _meta(self) -> list[FileMetadata]:
        # TODO: Consider caching if this is ever used on lots of files.
        return [self._fmetadata_extractor(f) for f in self._files]

    @property
    @override
    def data_id(self) -> str:
        return self._data_id

    @property
    @override
    def ts_types(self) -> Iterator[str]:
        ts_types = set([str(meta.tstype) for meta in self._meta])
        for ts in ts_types:
            yield ts

    @property
    @override
    def years_avail(self) -> Iterator[str]:
        years = set([meta.year for meta in self._meta])
        for y in years:
            yield str(y)

    @property
    @override
    def vars_provided(self) -> Iterator[str]:
        vars = set([meta.var for meta in self._meta])
        for v in vars:
            yield v

    @override
    def has_var(self, var_name: str) -> bool:
        return var_name in self.vars_provided

    @override
    def read_var(self, var_name: str, ts_type=None, **kwargs) -> GriddedData:
        for fp in self._files:
            meta = self._fmetadata_extractor(fp)
            if meta.var != var_name:
                continue

            if meta.tstype != ts_type:
                continue

            logger.info(f"Reading file '{fp}'.")
            with rasterio.open(fp) as ds:
                data = ds.read(1)

                # TODO
