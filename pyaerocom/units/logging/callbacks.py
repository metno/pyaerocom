import logging
from pyaerocom.units.units import UnitConversionCallbackInfo

logger = logging.getLogger(__name__)


class LoggingCallback:
    """Class intended to be used as a callback for unit conversion
    in pyaerocom.units.Unit. It logs as either DEBUG or LOG depending
    on if the values where changed (ie. if factor is not 1).
    """

    def __init__(self, log: logging.Logger | None = None) -> None:
        if log is None:
            log = logger
        self._logger = log

    def __call__(self, info: UnitConversionCallbackInfo) -> None:
        if info.factor == 1:
            level = logging.DEBUG
        else:
            level = logging.INFO

        self._logger.log(
            level,
            "Units for variable '%s' converted from '%s' to '%s' using conversion factor '%d'.",
            info.from_aerocom_var,
            info.from_cf_unit,
            info.to_cf_unit,
            info.factor,
        )
