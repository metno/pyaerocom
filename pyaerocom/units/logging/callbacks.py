import logging
from pyaerocom.units.units import UnitConversionCallbackInfo


class LoggingCallback:
    """Class intended to be used as a callback for unit conversion
    in pyaerocom.units.Unit. It logs as either DEBUG or LOG depending
    on if the values where changed (ie. if factor is not 1).
    """

    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

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
