import glob
import logging

import aerovaldb
import xarray as xr

from pyaerocom import ColocatedData, GriddedData, TsType, __version__, const
from pyaerocom.aeroval._processing_base import DataImporter, ProcessingEngine
from pyaerocom.aeroval.json_utils import round_floats
from pyaerocom.aeroval.modelmaps_helpers import (
    CONTOUR,
    OVERLAY,
    _jsdate_list,
    calc_contour_json,
    find_netcdf_files,
    plot_overlay_pixel_maps,
)
from pyaerocom.aeroval.varinfo_web import VarinfoWeb
from pyaerocom.colocation.colocator import Colocator
from pyaerocom.exceptions import (
    DataCoverageError,
    DataDimensionError,
    DataQueryError,
    EntryNotAvailable,
    ModelVarNotAvailable,
    TemporalResolutionError,
    VariableDefinitionError,
    VarNotAvailableError,
)


logger = logging.getLogger(__name__)

MODELREADERS_USE_MAP_FREQ = ["ReadMscwCtm"]  # , "ReadCAMS2_83"]


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

        for model in model_list:
            try:
                self._run_model(model, var_list)
            except VarNotAvailableError:
                logger.warning(f"no data for model {model}, skipping")
                continue

        self.cfg.modelmaps_opts.maps_freq = (
            self._get_maps_freq()
        )  # if needed, reassign "coarsest" to actual coarsest frequency

    def _get_vars_to_process(self, model_name, var_list):
        mvars = self.cfg.model_cfg.get_entry(model_name).get_vars_to_process(
            self.cfg.obs_cfg.get_all_vars()
        )[1]
        all_vars = sorted(list(set(mvars)))
        if var_list is not None:
            all_vars = [var for var in var_list if var in all_vars]
        return all_vars

    def _get_obs_vars_to_process(self, obs_name, var_list):
        ovars = self.cfg.obs_cfg.get_entry(obs_name).get_all_vars()
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
        if not var_list:
            raise VarNotAvailableError("List of variables is empty.")
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
                if CONTOUR in self.cfg.modelmaps_opts.plot_types or make_contour:
                    self._process_contour_map_var(model_name, var, self.reanalyse_existing)

                if OVERLAY in self.cfg.modelmaps_opts.plot_types or make_overlay:
                    # create overlay (pixel) plots
                    self._process_overlay_map_var(model_name, var, self.reanalyse_existing)

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
        return

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

        freq = self._get_maps_freq()
        tst = TsType(data.ts_type)

        if tst < freq:
            raise TemporalResolutionError(f"need {freq} or higher, got{tst}")
        elif tst > freq:
            data = data.resample_time(str(freq))

        data.check_unit()

        if not reanalyse_existing:
            # check if all files have already been produced
            # if even just one is missing, all is gonna be recomputed
            ts = _jsdate_list(data)

            uris_contour = self.avdb.query(
                aerovaldb.routes.Route.CONTOUR_TIMESPLIT,
                project=self.exp_output.proj_id,
                experiment=self.exp_output.exp_id,
            )
            all_times = [int(uri.meta["timestep"]) for uri in uris_contour]

            if all([date in all_times for date in ts]):
                logger.info(
                    f"Skipping contour processing of {var}_{model_name}: data already exists {uris_contour}."
                )
                return

        # first calculate and save geojson with contour levels
        contourjson = calc_contour_json(data, cmap=varinfo.cmap, cmap_bins=varinfo.cmap_bins)

        with self.avdb.lock():
            for time, contour in contourjson.items():
                self.avdb.put_contour(
                    contour,
                    self.exp_output.proj_id,
                    self.exp_output.exp_id,
                    self.cfg.model_cfg.get_entry(model_name).model_rename_vars.get(var, var),
                    model_name,
                    timestep=time,
                )

    def _process_overlay_map_var(self, model_name, var, reanalyse_existing):  # pragma: no cover
        """Process overlay map (pixels) for either model or obserations
        argument model_name is a misnomer because this can also be applied to observation networks

        Args:
            model_name (str): name of model or obs to make overlay pixel maps of
            var (str): variable name
        """

        if self.cfg.processing_opts.only_json:  # we have colocated data
            data = self._process_only_json(model_name, var)
        else:
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

        if not self.cfg.processing_opts.only_json:
            data = self._check_dimensions(data)

        freq = self._get_maps_freq()

        tst = TsType(data.ts_type)

        if tst < freq:
            raise TemporalResolutionError(f"need {freq} or higher, got{tst}")
        elif tst > freq:
            if isinstance(data, GriddedData):
                data = data.resample_time(str(freq))
            elif isinstance(data, xr.DataArray):
                data = data.resample(time=str(freq)[0].capitalize()).mean()

        ts = _jsdate_list(data)
        if isinstance(data, GriddedData):
            data.check_unit()
            data = data.to_xarray().load()

        if self.cfg.processing_opts.only_model_maps:
            self._check_ts_for_only_model_maps(model_name, var, ts, data)

        for i, date in enumerate(ts):
            try:
                write_var_name = self.cfg.model_cfg.get_entry(model_name).model_rename_vars.get(
                    var, var
                )
            except EntryNotAvailable:
                write_var_name = var

            # Note this should match the output location defined in aerovaldb
            overlay_uris = self.avdb.query(
                aerovaldb.routes.Route.MAP_OVERLAY,
                project=self.exp_output.proj_id,
                experiment=self.exp_output.exp_id,
            )

            if not reanalyse_existing:
                if any(
                    uri.meta["variable"] == write_var_name
                    and uri.meta["source"] == model_name
                    and uri.meta["date"] == date
                    for uri in overlay_uris
                ):
                    logger.info(
                        f"Skipping overlay processing for model={model_name}, var={write_var_name}, date={date}: data already exists."
                    )
                    continue

            overlay_plot = plot_overlay_pixel_maps(
                data[i],
                cmap="gray",
                cmap_bins=varinfo.cmap_bins,
                format=self.cfg.modelmaps_opts.overlay_save_format,
            )

            with self.avdb.lock():
                self.avdb.put_map_overlay(
                    overlay_plot,
                    self.exp_output.proj_id,
                    self.exp_output.exp_id,
                    model_name,
                    write_var_name,
                    str(date),
                )

    def _get_maps_freq(self) -> TsType:
        """
        Gets the maps reading frequency. If maps_freq in cfg is coarsest, it takes the coarsest
        of the given frequencies. Else it just returns the maps_freq

        Returns
        -------
        TsType
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
        Tries to find the best TsType to read. Checks for available ts types with the following priority

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

        freq = min(TsType(fq) for fq in model_ts_types)
        logger.info(f"Found coarsest freq available as model data: {freq}")
        return freq

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

        data_id = self.cfg.model_cfg.get_entry(model_name).model_id

        try:
            data_dir = self.cfg.model_cfg.get_entry(model_name).model_data_dir
        except Exception as e:
            logger.info(f"Could not find model dir. Setting to None. Error {str(e)}")
            data_dir = None

        try:
            model_reader = self.cfg.model_cfg.get_entry(model_name).gridded_reader_id["model"]
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

        if var in self.cfg.model_cfg.get_entry(model_name).model_read_aux:
            aux_instructions = self.cfg.model_cfg.get_entry(model_name).model_read_aux[var]
            reader.add_aux_compute(var_name=var, **aux_instructions)

        kwargs = {}
        kwargs.update(**self.cfg.colocation_opts.model_kwargs)
        if var in self.cfg.colocation_opts.model_read_opts:
            kwargs.update(self.cfg.colocation_opts.model_read_opts[var])
        kwargs.update(self.cfg.get_model_entry(model_name).get("model_kwargs", {}))

        if model_reader is not None and model_reader in MODELREADERS_USE_MAP_FREQ:
            ts_types = reader.ts_types
            ts_type_read = str(self._get_read_model_freq(ts_types))
        else:
            model_ts_type_read = self.cfg.model_cfg.get_entry(model_name).model_ts_type_read
            if model_ts_type_read:
                ts_type_read = model_ts_type_read
            else:
                ts_type_read = (
                    self.cfg.colocation_opts.ts_type
                )  # emulates the old way closer than None

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

    def _check_ts_for_only_model_maps(
        self, name: str, var: str, dates: list[int], data: xr.Dataset
    ):  # pragma: no cover
        maps_freq = str(self._get_maps_freq())
        if name in self.cfg.obs_cfg.keylist():
            with self.avdb.lock():
                timeseries = self.avdb.get_timeseries(
                    self.cfg.proj_info.proj_id,
                    self.cfg.exp_info.exp_id,
                    "ALL",
                    name,
                    var,
                    self.cfg.obs_cfg.get_entry(name).obs_vert_type,
                    default={},
                )

                for model_name in self.cfg.model_cfg.keylist():
                    if (
                        model_name in timeseries
                        and timeseries[model_name].get(maps_freq + "_mod", False)
                        and timeseries[model_name].get(maps_freq + "_obs", False)
                    ):
                        continue

                    timeseries.setdefault(model_name, {})
                    timeseries[model_name].setdefault(maps_freq + "_date", dates)
                    timeseries[model_name].setdefault(
                        maps_freq + "_obs",
                        list(round_floats(data.mean(dim=("latitude", "longitude")).values)),
                    )

                    timeseries[model_name].setdefault("obs_var", var)
                    if hasattr(data, "units"):
                        timeseries[model_name].setdefault("obs_unit", data.units)
                    elif hasattr(data, "var_units"):
                        timeseries[model_name].setdefault("obs_unit", data.var_units[1])
                    else:
                        raise ValueError("Can not determine obs units")
                    timeseries[model_name].setdefault("obs_name", name)
                    timeseries[model_name].setdefault(
                        "var_name_web", self.cfg.obs_cfg.get_web_interface_name(name)
                    )
                    timeseries[model_name].setdefault(
                        "vert_code", self.cfg.obs_cfg.get_entry(name).obs_vert_type
                    )
                    timeseries[model_name].setdefault("obs_freq_src", maps_freq)

                self.avdb.put_timeseries(
                    timeseries,
                    self.cfg.proj_info.proj_id,
                    self.cfg.exp_info.exp_id,
                    "ALL",
                    name,
                    var,
                    self.cfg.obs_cfg.get_entry(name).obs_vert_type,
                )
        elif name in self.cfg.model_cfg.keylist():
            with self.avdb.lock():
                for obs_name in self.cfg.obs_cfg.keylist():
                    timeseries = self.avdb.get_timeseries(
                        self.cfg.proj_info.proj_id,
                        self.cfg.exp_info.exp_id,
                        "ALL",
                        obs_name,
                        var,
                        self.cfg.obs_cfg.get_entry(obs_name).obs_vert_type,
                        default={},
                    )

                    if (
                        name in timeseries
                        and timeseries[name].get(maps_freq + "_mod", False)
                        and timeseries[name].get(maps_freq + "_obs", False)
                    ):
                        continue

                    timeseries.setdefault(name, {})
                    timeseries[name].setdefault(maps_freq + "_date", dates)
                    timeseries[name].setdefault(
                        maps_freq + "_mod",
                        list(round_floats(data.mean(dim=("latitude", "longitude")).values)),
                    )
                    timeseries[name].setdefault("station_name", "ALL")
                    timeseries[name].setdefault("pyaerocom_version", __version__)
                    timeseries[name].setdefault("mod_var", var)
                    if hasattr(data, "units"):
                        timeseries[name].setdefault("mod_unit", data.units)
                    elif hasattr(data, "var_units"):
                        timeseries[name].setdefault("mod_unit", data.var_units[0])
                    else:
                        raise ValueError("Can not determine model units")
                    timeseries[name].setdefault("model_name", name)
                    timeseries[name].setdefault("mod_freq_src", maps_freq)

                    self.avdb.put_timeseries(
                        timeseries,
                        self.cfg.proj_info.proj_id,
                        self.cfg.exp_info.exp_id,
                        "ALL",
                        obs_name,
                        var,
                        self.cfg.obs_cfg.get_entry(obs_name).obs_vert_type,
                    )
        else:
            raise ValueError(
                f"{name=} not is not in either {self.cfg.obs_cfg.keylist()=} nor {self.cfg.model_cfg.keylist()=}"
            )

    def _process_only_json(self, model_name, var):  # pragma: no cover
        """Process data from ColocatedData for overlay map for if only_json = True."""
        try:
            preprocessed_coldata_dir = glob.escape(
                self.cfg.model_cfg.get_entry(model_name).model_data_dir
            )
            mask = f"{preprocessed_coldata_dir}/*.nc"
            file_to_convert = glob.glob(mask)
        except KeyError:
            preprocessed_coldata_dir = glob.escape(
                self.cfg.obs_cfg.get_entry(model_name).coldata_dir
            )
            mask = f"{preprocessed_coldata_dir}/{model_name}/*.nc"
            matching_files = find_netcdf_files(
                directory=preprocessed_coldata_dir, strings=[model_name, var]
            )

            if len(matching_files) > 1:
                logger.info(
                    f"Found more than one colocated data file for {model_name=} {var=}. Using the first one found - this theoretically should be consistent across files."
                )
            file_to_convert = matching_files[:1]

        if len(file_to_convert) != 1:
            raise ValueError(
                "Can only handle one colocated data object for plotting for a given (model, obs, var). "
                "Note that when providing a colocated data object, it must be provided via the model_data_dir argument in a ModelEntry instance. "
                "It must also be provided via the coldata_dir argument in the ObsEntry instance. "
                "Additionally, note that the coldatadir does not contain the model_name at the end of the directory, "
                "whereas the coldata_dir does not."
            )

        coldata = ColocatedData(data=file_to_convert[0])
        data = coldata.data.sel(data_source=model_name)
        data = data.drop_vars("data_source")
        data = data.transpose("time", "latitude", "longitude")
        data = data.sortby(["latitude", "longitude"])
        return data
