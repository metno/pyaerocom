"""
Module containing time resampling functionality
"""

import logging

import pandas as pd
import xarray as xarr

from pyaerocom.exceptions import TemporalResolutionError
from pyaerocom.helpers import isnumeric, resample_time_dataarray, resample_timeseries
from pyaerocom.units.datetime import TsType

logger = logging.getLogger(__name__)


class TimeResampler:
    """Object that can be use to resample timeseries data

    It supports hierarchical resampling of :class:`xarray.DataArray` objects
    and :class:`pandas.Series` objects.

    Hierarchical means, that resampling constraints can be applied for each
    level, that is, if hourly data is to be resampled to monthly, it may be
    specified to first required minimum number of hours per day, and minimum
    days per month, to create the output data.
    """

    AGGRS_UNIT_PRESERVE = ("mean", "median", "std", "max", "min")
    DEFAULT_HOW = "mean"

    def __init__(self, input_data=None):
        self.last_setup = None
        # the following attribute is updated whenever a resampling operation is
        # performed and it will check if any of the specified resampling
        # aggregators invalidates unit preservation (e.g. using how=add for
        # for accumulating precipitation...). See also attr. AGGRS_UNIT_PRESERVE
        self._last_units_preserved = None
        self._input_data = None

        if input_data is not None:
            self.input_data = input_data

    @property
    def last_units_preserved(self):
        """Boolean indicating if last resampling operation preserves units"""
        if self._last_units_preserved is None:
            raise AttributeError("Please call resample first...")
        return self._last_units_preserved

    @property
    def input_data(self):
        """Input data object that is to be resampled"""
        return self._input_data

    @input_data.setter
    def input_data(self, val):
        if not isinstance(val, pd.Series | xarr.DataArray):
            raise ValueError("Invalid input: need Series or DataArray")
        self._input_data = val

    @property
    def fun(self):
        """Resampling method (depends on input data type)"""
        if isinstance(self.input_data, pd.Series):
            return resample_timeseries
        return resample_time_dataarray

    def _get_resample_how(self, fr, to, how):
        if not isinstance(how, str | dict):
            val = self.DEFAULT_HOW
        elif isinstance(how, dict):
            if to.val in how and fr.val in how[to.val]:
                val = how[to.val][fr.val]
            else:
                val = self.DEFAULT_HOW
        else:
            val = how
        return val

    def _get_idx_entry(self, fr, to, min_num_obs, how):
        min_num = fr.get_min_num_obs(to, min_num_obs)

        _how = self._get_resample_how(fr, to, how)

        return (to.val, min_num, _how)

    def _gen_idx(self, from_ts_type, to_ts_type, min_num_obs, how):
        """Generate hierarchical resampling index

        Return
        ------
        list
            list (can be considered the iterator) of 3-element tuples for each\
            resampling step, containing

            - frequency to which the current is converted
            - minimum number of not-NaN values required for that step
            - aggregator to be used (e.g. mean, median, ...)

        """
        if isnumeric(min_num_obs):
            if not isinstance(how, str):
                raise ValueError(
                    f"Error initialising resampling constraints. "
                    f"min_num_obs is numeric ({min_num_obs}) and input how is {how} "
                    f"(would need to be string, e.g. mean)"
                )
            return [(to_ts_type.val, int(min_num_obs), how)]
        if not isinstance(min_num_obs, dict):
            raise ValueError(
                f"Invalid input for min_num_obs, need dictionary or integer, got {min_num_obs}"
            )

        base_freqs = TsType.VALID

        start_base = base_freqs.index(from_ts_type.base)
        stop_base = base_freqs.index(to_ts_type.base)

        last_from = from_ts_type
        idx = []
        # loop from next base freq to end base freq, note that min_num_obs as
        # well as input freqs may have multiplication factors, which may
        # require min_num_obs values to be updated accordingly
        for i in range(start_base + 1, stop_base + 1):
            to_base = TsType(base_freqs[i])
            try:
                entry = self._get_idx_entry(last_from, to_base, min_num_obs, how)
                idx.append(entry)
                last_from = to_base
            except (TemporalResolutionError, ValueError):
                continue
        if len(idx) == 0 or not idx[-1][0] == to_ts_type.val:
            try:
                last_entry = self._get_idx_entry(last_from, to_ts_type, min_num_obs, how)
            except (TemporalResolutionError, ValueError):
                _how = self._get_resample_how(last_from, to_ts_type, how)
                last_entry = (to_ts_type.val, 0, _how)
            idx.append(last_entry)
        return idx

    def resample(
        self, to_ts_type, input_data=None, from_ts_type=None, how=None, min_num_obs=None, **kwargs
    ):
        """Resample input data

        Parameters
        ----------
        to_ts_type : str or TsType
            output resolution
        input_data : pandas.Series or xarray.DataArray
            data to be resampled
        from_ts_type : str or TsType, optional
            current temporal resolution of data
        how : str
            string specifying how the data is to be aggregated, default is mean
        min_num_obs : dict or int, optional
            integer or nested dictionary specifying minimum number of
            observations required to resample from higher to lower frequency.
            For instance, if `input_data` is hourly and `to_ts_type` is
            monthly, you may specify something like::

                min_num_obs =
                    {'monthly'  :   {'daily'  : 7},
                     'daily'    :   {'hourly' : 6}}

            to require at least 6 hours per day and 7 days per month.

        **kwargs
           additional input arguments passed to resampling method

        Returns
        -------
        pandas.Series or xarray.DataArray
            resampled data object
        """
        if how is None:
            how = "mean"

        if how in self.AGGRS_UNIT_PRESERVE:
            self._last_units_preserved = True
        else:
            self._last_units_preserved = False

        if not isinstance(to_ts_type, TsType):
            to_ts_type = TsType(to_ts_type)

        if str(from_ts_type) == "native":
            from_ts_type = None

        if from_ts_type is None:
            if min_num_obs is not None:
                logger.warning("setting min_num_obs to None since from_ts_type is not specified")
                min_num_obs = None
        elif isinstance(from_ts_type, str):
            from_ts_type = TsType(from_ts_type)

        if input_data is not None:
            self.input_data = input_data
        if self.input_data is None:
            raise ValueError("Please provide data (Series or DataArray)")

        self.last_setup = dict(min_num_obs=min_num_obs, how=how)

        if from_ts_type is None:  # native == unknown
            freq = to_ts_type.to_pandas_freq()
            data_out = self.fun(self.input_data, freq=freq, how=how, **kwargs)
        elif to_ts_type > from_ts_type:
            raise TemporalResolutionError(
                f"Cannot resample time-series from {from_ts_type} to {to_ts_type}"
            )
        elif to_ts_type == from_ts_type:
            logger.debug(
                f"Input time frequency {to_ts_type.val} equals current frequency of data. "
                f"Resampling will be applied anyways which will introduce NaN values "
                f"at missing time stamps"
            )

            freq = to_ts_type.to_pandas_freq()
            self._last_units_preserved = True
            data_out = self.fun(self.input_data, freq=freq, how="mean", **kwargs)

        elif min_num_obs is None:
            freq = to_ts_type.to_pandas_freq()
            if not isinstance(how, str):
                raise ValueError(
                    f"Temporal resampling without constraints can only use string type "
                    f"argument how (e.g. how=mean). Got {how}"
                )

            data_out = self.fun(self.input_data, freq=freq, how=how, **kwargs)
        else:
            _idx = self._gen_idx(from_ts_type, to_ts_type, min_num_obs, how)
            data_out = self.input_data
            aggrs = []
            for to_ts_type, mno, rshow in _idx:
                freq = TsType(to_ts_type).to_pandas_freq()
                data_out = self.fun(data_out, freq=freq, how=rshow, min_num_obs=mno, **kwargs)
                aggrs.append(rshow)

            if all([x in self.AGGRS_UNIT_PRESERVE for x in aggrs]):
                self._last_units_preserved = True
            else:
                self._last_units_preserved = False
        return data_out
