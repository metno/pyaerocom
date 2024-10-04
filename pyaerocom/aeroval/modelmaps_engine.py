import logging
import os

from pyaerocom import GriddedData, TsType, const
from pyaerocom.aeroval._processing_base import DataImporter, ProcessingEngine
from pyaerocom.aeroval.modelmaps_helpers import (
    calc_contour_json,
    plot_overlay_pixel_maps,
    _jsdate_list,
    CONTOUR,
    OVERLAY,
)
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
    EntryNotAvailable,
)

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

    def _get_obs_vars_to_process(self, obs_name, var_list):
        ovars = self.cfg.obs_cfg.get(obs_name).get_all_vars()
        all_vars = sorted(list(set(ovars)))
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

        try:
            var_list = self._get_vars_to_process(model_name, var_list)
        except EntryNotAvailable:
            var_list = self._get_obs_vars_to_process(model_name, var_list)

        files = []
        for var in var_list:
            logger.info(f"Processing model maps for {model_name} ({var})")

            try:  # pragma: no cover
                make_contour, make_overlay = False, False
                if isinstance(self.cfg.modelmaps_opts.plot_types, dict):
                    make_contour = CONTOUR in self.cfg.modelmaps_opts.plot_types.get(
                        model_name, False
                    )
                    make_overlay = OVERLAY in self.cfg.modelmaps_opts.plot_types.get(
                        model_name, False
                    )

                if self.cfg.modelmaps_opts.plot_types == {CONTOUR} or make_contour:
                    _files = self._process_contour_map_var(
                        model_name, var, self.reanalyse_existing
                    )
                    files.extend(_files)
                if self.cfg.modelmaps_opts.plot_types == {OVERLAY} or make_overlay:
                    # create overlay (pixel) plots
                    _files = self._process_overlay_map_var(
                        model_name, var, self.reanalyse_existing
                    )

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

    def _process_contour_map_var(self, model_name, var, reanalyse_existing):  # pragma: no cover
        """
        Process model data to create map geojson files

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
            data = self._read_model_data(model_name, var)
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
        fp_geojson = os.path.join(outdir, f"{outname}.geojson")

        if not reanalyse_existing:
            if os.path.exists(fp_geojson):
                logger.info(f"Skipping contour processing of {outname}: data already exists.")
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

        with self.avdb.lock():
            self.avdb.put_contour(
                contourjson,
                self.exp_output.proj_id,
                self.exp_output.exp_id,
                var,
                model_name,
            )

        return fp_geojson

    def _process_overlay_map_var(self, model_name, var, reanalyse_existing):  # pragma: no cover
        """Process overlay map (pixels) for either model or obserations
        argument model_name is a misnomer because this can also be applied to observation networks

        Args:
            model_name (str): name of model or obs to make overlay pixel maps of
            var (str): variable name
        """

        try:
            data = self.read_gridded_obsdata(model_name, var)
        except EntryNotAvailable:
            try:
                data = self._read_model_data(model_name, var)
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

        outdir = self.cfg.path_manager.get_json_output_dirs()["contour/overlay"]

        freq = self._get_maps_freq()

        tst = TsType(data.ts_type)

        if tst < freq:
            raise TemporalResolutionError(f"need {freq} or higher, got{tst}")
        elif tst > freq:
            data = data.resample_time(str(freq))

        data.check_unit()

        tst = _jsdate_list(data)
        data = data.to_xarray()
        for i, date in enumerate(tst):
            outname = f"{model_name}_{var}_{date}"

            # Note should matche the output location defined in aerovaldb
            fp_overlay = os.path.join(outdir, outname)

            if not reanalyse_existing:
                if os.path.exists(fp_overlay):
                    logger.info(f"Skipping overlay processing of {outname}: data already exists.")
                    continue

            overlay_plot = plot_overlay_pixel_maps(
                data[i],
                cmap=varinfo.cmap,
                cmap_bins=varinfo.cmap_bins,
                format=self.cfg.modelmaps_opts.overlay_save_format,
            )

            with self.avdb.lock():
                self.avdb.put_map_overlay(
                    overlay_plot,
                    self.exp_output.proj_id,
                    self.exp_output.exp_id,
                    model_name,
                    var,
                    date,
                )

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

        raise ValueError("Could not find any TS type to read maps")

    def _read_model_data(self, model_name: str, var: str) -> GriddedData:
        """
        Function for reading the model data without going through the colocation object.
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
        except Exception as e:
            logger.info(f"Could not find model dir. Setting to None. Error {str(e)}")
            data_dir = None

        try:
            model_reader = self.cfg.model_cfg[model_name].gridded_reader_id["model"]
        except Exception as e:
            logger.info(f"Could not find model reader. Setting to None. Error {str(e)}")
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
