import logging
from traceback import format_exc

import numpy as np
import xarray as xr

from pyaerocom import ColocatedData
from pyaerocom.aeroval._processing_base import HasColocator, ProcessingEngine
from pyaerocom.aeroval.coldatatojson_engine import ColdataToJsonEngine
from pyaerocom.units.datetime import get_lowest_resolution

logger = logging.getLogger(__name__)


class SuperObsEngine(ProcessingEngine, HasColocator):
    """
    Class to handle the processing of combined obs datasets
    """

    def run(self, model_name, obs_name, var_list, try_colocate_if_missing=True):
        self._process_entry(
            model_name=model_name,
            obs_name=obs_name,
            var_list=var_list,
            try_colocate_if_missing=try_colocate_if_missing,
        )

    def _process_entry(self, model_name, obs_name, var_list, try_colocate_if_missing):
        sobs_cfg = self.cfg.obs_cfg.get_entry(obs_name)

        if var_list is None:
            var_list = sobs_cfg.obs_vars
        elif isinstance(var_list, str):
            var_list = [var_list]
        elif not isinstance(var_list, list):
            raise ValueError(f"invalid input for var_list: {var_list}.")

        for var_name in var_list:
            try:
                self._run_var(model_name, obs_name, var_name, try_colocate_if_missing)
            except Exception:
                if self.raise_exceptions:
                    raise
                logger.warning(
                    f"Failed to process superobs entry for {obs_name},  "
                    f"{model_name}, var {var_name}. Reason: {format_exc()}"
                )

    def _run_var(self, model_name, obs_name, var_name, try_colocate_if_missing):
        """
        Run evaluation of superobs entry

        Parameters
        ----------
        model_name : str
            name of model in :attr:`model_config`
        obs_name : str
            name of super observation in :attr:`obs_cfg`
        var_name : str
            name of variable to be processed.
        try_colocate_if_missing : bool
            if True, then missing colocated data objects are computed on the
            fly.

        Raises
        ------
        ValueError
            If multiple (or no) colocated data objects are available for
            individual obs datasets of which the superobservation is comprised.

        Returns
        -------
        None
        """
        coldata_files = []
        coldata_resolutions = []
        vert_codes = []
        obs_entry = self.cfg.obs_cfg.get_entry(obs_name)
        obs_needed = obs_entry.obs_id
        vert_code = obs_entry.obs_vert_type
        for oname in obs_needed:
            fp, ts_type, vert_code = self._get_coldata_fileinfo(
                model_name, oname, var_name, try_colocate_if_missing
            )
            coldata_files.append(fp)
            coldata_resolutions.append(ts_type)
            vert_codes.append(vert_code)

        if len(np.unique(vert_codes)) > 1 or vert_codes[0] != vert_code:
            raise ValueError(
                "Cannot merge observations with different vertical types into super observation..."
            )

        if not len(coldata_files) == len(obs_needed):
            raise ValueError(
                f"Could not retrieve colocated data files for "
                f"all required observations for super obs "
                f"{obs_name}"
            )

        to_freq = get_lowest_resolution(*coldata_resolutions)
        darrs = []
        for fp in coldata_files:
            darrs.append(self._get_dataarray(fp, to_freq, obs_name))

        merged = xr.concat(darrs, dim="station_name")
        coldata = ColocatedData(data=merged)
        engine = ColdataToJsonEngine(self.cfg)
        engine.process_coldata(coldata)

    def _get_dataarray(self, fp, to_freq, obs_name):
        """Get dataarray needed for combination to superobs"""
        data = ColocatedData(data=fp)
        if data.ts_type != to_freq:
            data.resample_time(to_ts_type=to_freq, settings_from_meta=True, inplace=True)
        arr = data.data
        ds = arr["data_source"].values
        source_new = [obs_name, ds[1]]
        arr["data_source"] = source_new  # obs, model_id
        arr.attrs["data_source"] = source_new
        arr.attrs["obs_name"] = obs_name
        return arr

    def _get_coldata_fileinfo(self, model_name, obs_name, var_name, try_colocate_if_missing):
        """Get fileinfo about existing colocated data object"""
        col = self.get_colocator(model_name, obs_name)
        if self.reanalyse_existing:
            col.run(var_list=[var_name])
            cdf = col.files_written
        else:
            cdf = col.get_available_coldata_files([var_name])
            if len(cdf) == 0 and try_colocate_if_missing:
                col.run(var_list=[var_name])
                cdf = col.files_written

        if len(cdf) != 1:
            raise ValueError(
                f"Fatal: Found multiple colocated data objects for "
                f"{model_name}, {obs_name}, {var_name}: {cdf}..."
            )
        fp = cdf[0]
        meta = ColocatedData.get_meta_from_filename(fp)
        ts_type = meta["ts_type"]
        vert_code = self.cfg.obs_cfg.get_entry(obs_name).obs_vert_type
        return (fp, ts_type, vert_code)
