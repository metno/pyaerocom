import logging
from pyaerocom.units.units import UnitConversionCallbackInfo

logger = logging.getLogger(__name__)


class LoggingCallback:
    """Class intended to be used as a callback for unit conversion
    in pyaerocom.units.Unit. It logs as either DEBUG or LOG depending
    on if the values where changed (ie. if factor is 1).
    """

    def __init__(self, log: logging.Logger | None = None) -> None:
        """
        :param log: Instance of logger to be used. If not provided, the logger
            of this module will be used, which may be undesired due to hiding the
            real source of the error so it is recommended to provide your own.
        """
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
            "Successfully converted unit of variable '%s' from '%s' to '%s' using conversion factor '%d'.",
            info.from_aerocom_var,
            info.from_cf_unit,
            info.to_cf_unit,
            info.factor,
        )
