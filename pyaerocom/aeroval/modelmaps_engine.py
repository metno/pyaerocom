import logging
import os

from pyaerocom import GriddedData, TsType, const
from pyaerocom.aeroval._processing_base import DataImporter, ProcessingEngine
from pyaerocom.aeroval.modelmaps_helpers import (
    calc_contour_json,
    griddeddata_to_jsondict,
)
from pyaerocom.io.mscw_ctm.reader import ReadMscwCtm
from pyaerocom.colocation.colocation_setup import ColocationSetup
from pyaerocom.colocation.colocator import Colocator
from pyaerocom.aeroval.varinfo_web import VarinfoWeb
from pyaerocom.exceptions import (
    DataCoverageError,
    DataDimensionError,
    DataQueryError,
    ModelVarNotAvailable,
    TemporalResolutionError,
    VariableDefinitionError,
    VarNotAvailableError,
)
from pyaerocom.helpers import isnumeric

logger = logging.getLogger(__name__)

MODELREADERS_USE_MAP_FREQ = ["ReadMscwCtm"]


class ModelMapsEngine(ProcessingEngine, DataImporter):
    """
    Engine for processing of model maps
    """

    def _get_run_kwargs(self, **kwargs):
        try:
            model_list = kwargs["model_list"]
        except KeyError:
            model_list = self.cfg.model_cfg.keylist()
        try:
            var_list = kwargs["var_list"]
        except Exception:
            var_list = None
        return model_list, var_list

    def run(self, **kwargs):
        model_list, var_list = self._get_run_kwargs(**kwargs)

        all_files = []
        for model in model_list:
            try:
                files = self._run_model(model, var_list)
            except VarNotAvailableError:
                files = []
            if not files:
                logger.warning(f"no data for model {model}, skipping")
                continue
            all_files.extend(files)
        return files

    def _get_vars_to_process(self, model_name, var_list):
        mvars = self.cfg.model_cfg.get_entry(model_name).get_vars_to_process(
            self.cfg.obs_cfg.get_all_vars()
        )[1]
        all_vars = sorted(list(set(mvars)))
        if var_list is not None:
            all_vars = [var for var in var_list if var in all_vars]
        return all_vars

    def _run_model(self, model_name: str, var_list):
        """Run evaluation of map processing

        Create json files for model-maps display. This analysis does not
        require any observation data but processes model output at all model
        grid points, which is then displayed on the website in the maps
        section.

        Parameters
        ----------
        model_name : str
            name of model to be processed
        var_list : list, optional
            name of variable to be processed. If None, all available
            observation variables are used.

        """

        var_list = self._get_vars_to_process(model_name, var_list)
        files = []
        for var in var_list:
            logger.info(f"Processing model maps for {model_name} ({var})")

            try:
                _files = self._process_map_var(model_name, var, self.reanalyse_existing)
                files.extend(_files)

            except ModelVarNotAvailable as ex:
                logger.warning(f"{ex}")
            except (
                TemporalResolutionError,
                DataCoverageError,
                VariableDefinitionError,
                DataQueryError,
            ) as e:
                if self.raise_exceptions:
                    raise
                logger.warning(f"Failed to process maps for {model_name} {var} data. Reason: {e}.")
        return files

    def _check_dimensions(self, data: GriddedData) -> "GriddedData":
        if not data.has_latlon_dims:
            raise DataDimensionError("data needs to have latitude an longitude dimension")
        elif not data.has_time_dim:
            raise DataDimensionError("data needs to have latitude an longitude dimension")
        if data.ndim == 4:
            data = data.extract_surface_level()
        return data

    def _process_map_var(self, model_name, var, reanalyse_existing):
        """
        Process model data to create map json files

        Parameters
        ----------
        model_name : str
            name of model
        var : str
            name of variable
        reanalyse_existing : bool
            if True, already existing json files will be reprocessed

        Raises
        ------
        ValueError
            If vertical code of data is invalid or not set
        AttributeError
            If the data has the incorrect number of dimensions or misses either
            of time, latitude or longitude dimension.
        ModelVarNotAvailable
            If model/var data cannot be read
        """
        try:
            # data = self.read_model_data(model_name, var)
            data = self._read_modeldata(model_name, var)
        except Exception as e:
            raise ModelVarNotAvailable(
                f"Cannot read data for model {model_name} (variable {var}): {e}"
            )

        var_ranges_defaults = self.cfg.var_scale_colmap
        if var in var_ranges_defaults.keys():
            cmapinfo = var_ranges_defaults[var]
            varinfo = VarinfoWeb(var, cmap=cmapinfo["colmap"], cmap_bins=cmapinfo["scale"])
        else:
            cmapinfo = var_ranges_defaults["default"]
            varinfo = VarinfoWeb(var, cmap=cmapinfo["colmap"], cmap_bins=cmapinfo["scale"])

        data = self._check_dimensions(data)

        outdir = self.cfg.path_manager.get_json_output_dirs()["contour"]
        outname = f"{var}_{model_name}"
        fp_json = os.path.join(outdir, f"{outname}.json")
        fp_geojson = os.path.join(outdir, f"{outname}.geojson")

        if not reanalyse_existing:
            if os.path.exists(fp_json) and os.path.exists(fp_geojson):
                logger.info(f"Skipping processing of {outname}: data already exists.")
                return []

        freq = self._get_maps_freq()
        tst = TsType(data.ts_type)

        if tst < freq:
            raise TemporalResolutionError(f"need {freq} or higher, got{tst}")
        elif tst > freq:
            data = data.resample_time(str(freq))

        data.check_unit()
        # first calcualate and save geojson with contour levels
        contourjson = calc_contour_json(data, cmap=varinfo.cmap, cmap_bins=varinfo.cmap_bins)

        # now calculate pixel data json file (basically a json file
        # containing monthly mean timeseries at each grid point at
        # a lower resolution)
        if isnumeric(self.cfg.modelmaps_opts.maps_res_deg):
            lat_res = self.cfg.modelmaps_opts.maps_res_deg
            lon_res = self.cfg.modelmaps_opts.maps_res_deg
        else:
            lat_res = self.cfg.modelmaps_opts.maps_res_deg["lat_res_deg"]
            lon_res = self.cfg.modelmaps_opts.maps_res_deg["lon_res_deg"]

        datajson = griddeddata_to_jsondict(data, lat_res_deg=lat_res, lon_res_deg=lon_res)

        with self.avdb.lock():
            self.avdb.put_gridded_map(
                datajson,
                self.exp_output.proj_id,
                self.exp_output.exp_id,
                var,
                model_name,
            )
            self.avdb.put_contour(
                contourjson,
                self.exp_output.proj_id,
                self.exp_output.exp_id,
                var,
                model_name,
            )

        return [fp_json, fp_geojson]

    def _get_maps_freq(self) -> TsType:
        """
        Gets the maps reading frequency. If maps_freq in cfg is coarsest, it takes the coarsest
        of the given frequencies. Else it just returns the maps_freq

        Returns
        -------
        TSType
        """
        maps_freq = TsType(self.cfg.modelmaps_opts.maps_freq)
        if maps_freq == "coarsest":  # TODO: Implement this in terms of a TsType object. #1267
            freq = min(TsType(fq) for fq in self.cfg.time_cfg.freqs)
            freq = min(freq, self.cfg.time_cfg.main_freq)
        else:
            freq = maps_freq

        return freq

    def _get_read_model_freq(self, model_ts_types: list) -> TsType:
        """
        Tries to find the best TS type to read. Checks for available ts types with the following priority

        1. If the freq from _get_maps_freq is available
        2. If maps_freq is explicitly given, and is available
        3. Iterates through the freqs given in the config, and find the coarsest available ts type

        Raises
        -------

        ValueError
            If no ts types are possible to read

        Returns
        -------
        TSType
        """
        wanted_freq = self._get_maps_freq()
        if wanted_freq in model_ts_types:
            return wanted_freq

        maps_freq = TsType(self.cfg.modelmaps_opts.maps_freq)

        if maps_freq != "coarsest":
            if maps_freq not in model_ts_types:
                raise ValueError(
                    f"Could not find any model data for given maps_freq. {maps_freq} is not in {model_ts_types}"
                )
            return maps_freq

        for freq in sorted(TsType(fq) for fq in self.cfg.time_cfg.freqs):
            if freq in model_ts_types:
                logger.info(f"Found coarsest maps_freq that is available as model data: {freq}")
                return freq

        raise ValueError(f"Could not find any TS type to read maps")

    def _read_modeldata(self, model_name: str, var: str) -> GriddedData:
        """
        Function for reading the modeldata without going through the colocation object.
        This means that none of the checks normally done in the colocation class are run.

        Parameters
        ----------
        model_name : str
            name of model
        var : str
            name of variable

        Returns
        -----------
        Griddeddata
            the read data
        """
        start, stop = self.cfg.colocation_opts.start, self.cfg.colocation_opts.stop
        if self.cfg.colocation_opts.model_use_climatology:
            # overwrite start and stop to read climatology file for model
            start, stop = 9999, None

        data_id = self.cfg.model_cfg[model_name].model_id

        try:
            data_dir = self.cfg.model_cfg[model_name].model_data_dir
        except:
            data_dir = None

        try:
            model_reader = self.cfg.model_cfg[model_name].gridded_reader_id["model"]
        except:
            model_reader = None

        if model_reader is not None:
            reader_class = Colocator.SUPPORTED_GRIDDED_READERS[model_reader]
        else:
            reader_class = Colocator.SUPPORTED_GRIDDED_READERS["ReadGridded"]

        reader = reader_class(
            data_id=data_id,
            data_dir=data_dir,
            **self.cfg.colocation_opts.model_kwargs,
        )

        if var in self.cfg.model_cfg[model_name].model_read_aux:
            aux_instructions = self.cfg.model_cfg[model_name].model_read_aux[var]
            reader.add_aux_compute(var_name=var, **aux_instructions)

        kwargs = {}
        kwargs.update(**self.cfg.colocation_opts.model_kwargs)
        if var in self.cfg.colocation_opts.model_read_opts:
            kwargs.update(self.cfg.colocation_opts.model_read_opts[var])

        if model_reader is not None and model_reader in MODELREADERS_USE_MAP_FREQ:
            ts_types = reader.ts_types
            ts_type_read = str(self._get_read_model_freq(ts_types))
        else:
            ts_type_read = self.cfg.time_cfg.main_freq

        data = reader.read_var(
            var,
            start=start,
            stop=stop,
            ts_type=ts_type_read,
            vert_which=self.cfg.colocation_opts.obs_vert_type,
            flex_ts_type=self.cfg.colocation_opts.flex_ts_type,
            **kwargs,
        )

        rm_outliers = self.cfg.colocation_opts.model_remove_outliers
        outlier_ranges = self.cfg.colocation_opts.model_outlier_ranges

        if rm_outliers:
            if var in outlier_ranges:
                low, high = outlier_ranges[var]
            else:
                var_info = const.VARS[var]
                low, high = var_info.minimum, var_info.maximum
            data.check_unit()
            data.remove_outliers(low, high, inplace=True)

        return data
