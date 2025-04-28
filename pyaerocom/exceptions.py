"""
Module containing pyaerocom custom exceptions
"""


class AeronetReadError(IOError):
    # Aeronet reading failed somehow
    pass


class CachingError(IOError):
    pass


class CacheWriteError(CachingError):
    pass


class CacheReadError(CachingError):
    pass


class ColocationError(ValueError):
    pass


class ColocationSetupError(ValueError):
    pass


class CoordinateError(ValueError):
    pass


class CoordinateNameError(CoordinateError):
    pass


class DataRetrievalError(IOError):
    pass


class DataCoverageError(ValueError):
    pass


class DataDimensionError(ValueError):
    pass


class DataIdError(ValueError):
    pass


class DataQueryError(ValueError):
    pass


class DataSourceError(ValueError):
    pass


class DataUnitError(ValueError):
    pass


class DeprecationError(AttributeError, ValueError):
    pass


class DimensionOrderError(DataDimensionError):
    pass


class DataExtractionError(ValueError):
    pass


class DataSearchError(IOError):
    pass


class EvalEntryNameError(KeyError):
    pass


class NasaAmesReadError(IOError):
    pass


class EbasFileError(ValueError):
    pass


class EEAv2FileError(ValueError):
    pass


class EprofileFileError(ValueError):
    pass


class EarlinetFileError(ValueError):
    pass


class EntryNotAvailable(KeyError):
    pass


class InitialisationError(ValueError):
    pass


class FileConventionError(IOError):
    pass


class LongitudeConstraintError(ValueError):
    pass


class MetaDataError(AttributeError):
    pass


class ModelVarNotAvailable(IOError):
    pass


class NetworkNotSupported(NotImplementedError):
    pass


class NetworkNotImplemented(NotImplementedError):
    pass


class NetcdfError(IOError):
    pass


class NotInFileError(IOError):
    pass


class ResamplingError(ValueError):
    pass


class StationCoordinateError(CoordinateError):
    pass


class StationNotFoundError(AttributeError):
    pass


class TimeZoneError(AttributeError):
    pass


class TimeMatchError(AttributeError):
    pass


class TemporalResolutionError(ValueError):
    pass


class TemporalSamplingError(ValueError):
    pass


class UnknownRegion(ValueError):
    pass


class UnresolvableTimeDefinitionError(DataDimensionError, NetcdfError):
    """Is raised if time definition in NetCDF file is wrong and cannot be corrected"""

    pass


class VarNotAvailableError(DataCoverageError):
    pass


class VariableDefinitionError(IOError):
    pass


class VariableNotFoundError(IOError):
    pass
