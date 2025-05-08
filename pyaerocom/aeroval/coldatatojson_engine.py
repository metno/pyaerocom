import logging
import os
from numpy.typing import ArrayLike
from time import time

from pyaerocom import ColocatedData, TsType, const
from pyaerocom.aeroval._processing_base import ProcessingEngine
from pyaerocom.aeroval.coldatatojson_helpers import (
    _apply_annual_constraint,
    _calculate_fairmode,
    _init_data_default_frequencies,
    _init_meta_glob,
    _process_heatmap_data,
    _process_map_and_scat,
    _process_regional_timeseries,
    _process_sites,
    _process_sites_weekly_ts,
    _process_statistics_timeseries_single_region,
    _remove_less_covered,
    init_regions_web,
    process_profile_data_for_regions,
    process_profile_data_for_stations,
)
from pyaerocom.aeroval.exceptions import ConfigError
from pyaerocom.aeroval.fairmode_statistics import SPECIES, FairmodeStatistics
from pyaerocom.aeroval.json_utils import round_floats
from pyaerocom.units import Unit

logger = logging.getLogger(__name__)


class ColdataToJsonEngine(ProcessingEngine):
    def run(self, files):
        """
        Convert colocated data files to json

        Parameters
        ----------
        files : list
            list of file paths pointing to colocated data objects to be
            processed.

        Returns
        -------
        list
            list of files that have been converted.

        """
        converted = []
        for file in files:
            logger.info(f"Processing: {file}")
            coldata = ColocatedData(data=file)
            self.process_coldata(coldata)
            converted.append(file)
        return converted

    def process_coldata(self, coldata: ColocatedData):
        """
        Creates all json files for one ColocatedData object

        Parameters
        ----------
        coldata : ColocatedData
            colocated data to be processed.

        Raises
        ------
        NotImplementedError
            DESCRIPTION.
        ValueError
            DESCRIPTION.
        ConfigError
            DESCRIPTION.

        Returns
        -------
        None.

        """
        t00 = time()
        use_weights = self.cfg.statistics_opts.weighted_stats
        drop_stats = self.cfg.statistics_opts.drop_stats
        # redundant, but cheap and important to be correct
        self.cfg._check_time_config()
        freqs = self.cfg.time_cfg.freqs
        periods = self.cfg.time_cfg.periods
        seasons = self.cfg.time_cfg.get_seasons()
        use_meteorological_seasons = self.cfg.time_cfg.use_meteorological_seasons
        main_freq = self.cfg.time_cfg.main_freq
        annual_stats_constrained = self.cfg.statistics_opts.annual_stats_constrained

        regions_how = self.cfg.webdisp_opts.regions_how

        stats_min_num = self.cfg.statistics_opts.MIN_NUM

        if hasattr(coldata.data, "altitude_units"):
            if Unit(coldata.data.attrs["altitude_units"]) != Unit(
                "km"
            ):  # put everything in terms of km for viz
                # convert start and end for file naming
                self._convert_coldata_altitude_units_to_km(coldata)

        vert_code = self._get_vert_code(coldata)

        diurnal_only = coldata.get_meta_item("diurnal_only")

        add_trends = self.cfg.statistics_opts.add_trends
        trends_min_yrs = self.cfg.statistics_opts.stats_min_yrs

        min_yrs = self.cfg.statistics_opts.obs_min_yrs
        sequential_yrs = self.cfg.statistics_opts.sequential_yrs
        avg_over_trends = self.cfg.statistics_opts.avg_over_trends
        use_fairmode = self.cfg.statistics_opts.use_fairmode
        use_diurnal = self.cfg.statistics_opts.use_diurnal

        # ToDo: some of the checks below could be done automatically in
        # EvalSetup, and at an earlier stage
        if vert_code == "ModelLevel":
            raise NotImplementedError("Coming (not so) soon...")

        # this will need to be figured out as soon as there is altitude
        elif "altitude" in coldata.data.dims:
            raise ValueError("Altitude should have been dealt with already in the colocation")

        elif not isinstance(coldata, ColocatedData):
            raise ValueError(f"Need ColocatedData object, got {type(coldata)}")

        elif coldata.has_latlon_dims and regions_how == "country":
            raise NotImplementedError(
                "Cannot yet apply country filtering for 4D colocated data instances"
            )
        elif main_freq not in freqs:
            raise ConfigError(f"main_freq {main_freq} is not in experiment frequencies: {freqs}")
        if self.cfg.statistics_opts.stats_tseries_base_freq is not None:
            if self.cfg.statistics_opts.stats_tseries_base_freq not in freqs:
                raise ConfigError(
                    f"Base frequency for statistics timeseries needs to be "
                    f"specified in experiment frequencies: {freqs}"
                )
        # init some stuff
        if "var_name_input" in coldata.metadata:
            obs_var = coldata.metadata["var_name_input"][0]
            model_var = coldata.metadata["var_name_input"][1]
        elif (
            "obs_vars" in coldata.metadata
        ):  # Try and get from obs_vars. Should not be needed in reading in a ColocatedData object created with pyaerocom.
            obs_var = model_var = coldata.metadata["obs_vars"]
            coldata.metadata["var_name_input"] = [obs_var, model_var]
            logger.warning(
                "ColdataToJsonEngine: Failed to access var_name_input from coldata.metadata. "
                "This could be because you're using a ColocatedData object created outside of pyaerocom. "
                "Setting obs_var and model_data to value in obs_vars instead. "
                "Setting var_input_data to these values as well. "
            )

        else:
            raise ValueError("Unable to determine obs_var/model_var")

        model_name = str(coldata.model_name)
        obs_name = str(coldata.obs_name)

        mcfg = self.cfg.model_cfg.get_entry(model_name)
        var_name_web = mcfg.get_varname_web(model_var, obs_var)

        logger.info(
            f"Computing json files for {model_name} ({model_var}) vs. {obs_name} ({obs_var})"
        )

        meta_glob = _init_meta_glob(
            coldata,
            vert_code=vert_code,
            obs_name=obs_name,
            model_name=model_name,
            var_name_web=var_name_web,
        )
        if min_yrs > 0:
            logger.info(
                f"Removing stations with less than {min_yrs} years of data, with sequential_yrs = {sequential_yrs}"
            )
            coldata = _remove_less_covered(coldata, min_yrs, sequential_yrs)

        # get region IDs
        (regborders, regs, regnames) = init_regions_web(coldata, regions_how)

        # Synchronise regions.json file
        with self.avdb.lock():
            regions = self.avdb.get_regions(
                self.exp_output.proj_id, self.exp_output.exp_id, default={}
            )
            for region_name, region_info in regborders.items():
                regions[region_name] = round_floats(region_info)
            self.avdb.put_regions(regions, self.exp_output.proj_id, self.exp_output.exp_id)

        use_country = True if regions_how == "country" else False

        data = _init_data_default_frequencies(coldata, freqs)

        if annual_stats_constrained:
            data = _apply_annual_constraint(data)

        if not coldata.data.attrs.get("just_for_viz", False):  # make the regular json output
            if not diurnal_only:
                if (
                    use_fairmode and obs_var in SPECIES
                ):  # calculate fairmode only for species where it makes sense
                    logger.info("Processing Fairmode statistics")
                    self._process_fairmode(
                        data=data,
                        obs_name=obs_name,
                        obs_var=obs_var,
                        var_name_web=var_name_web,
                        vert_code=vert_code,
                        model_name=model_name,
                        model_var=model_var,
                        meta_glob=meta_glob,
                        periods=periods,
                        seasons=seasons,
                        regions_how=regions_how,
                        regs=regs,
                    )
                logger.info("Processing statistics timeseries for all regions")

                self._process_stats_timeseries_for_all_regions(
                    data=data,
                    coldata=coldata,
                    main_freq=main_freq,
                    regnames=regnames,
                    use_weights=use_weights,
                    drop_stats=drop_stats,
                    use_country=use_country,
                    obs_name=obs_name,
                    obs_var=obs_var,
                    var_name_web=var_name_web,
                    vert_code=vert_code,
                    model_name=model_name,
                    model_var=model_var,
                    meta_glob=meta_glob,
                    periods=periods,
                    seasons=seasons,
                    add_trends=add_trends,
                    trends_min_yrs=trends_min_yrs,
                    regions_how=regions_how,
                    regs=regs,
                    stats_min_num=stats_min_num,
                    use_fairmode=use_fairmode,
                    avg_over_trends=avg_over_trends,
                    use_meteorological_seasons=use_meteorological_seasons,
                )

            if coldata.ts_type == "hourly" and use_diurnal:
                logger.info("Processing diurnal profiles")
                self._process_diurnal_profiles(
                    coldata=coldata,
                    regions_how=regions_how,
                    regnames=regnames,
                    meta_glob=meta_glob,
                )
        else:
            logger.info("Processing profile data for visualization")

            self._process_profile_data_for_visualization(
                data=data,
                use_country=use_country,
                region_names=regnames,
                station_names=coldata.data.station_name.values,
                periods=periods,
                seasons=seasons,
                obs_name=obs_name,
                var_name_web=var_name_web,
                use_meteorological_seasons=use_meteorological_seasons,
            )

        logger.info(
            f"Finished computing json files for {model_name} ({model_var}) vs. "
            f"{obs_name} ({obs_var})"
        )

        dt = time() - t00
        logger.info(f"Time expired: {dt:.2f} s")

    def _convert_coldata_altitude_units_to_km(self, coldata: ColocatedData = None):
        alt_units = coldata.data.attrs["altitude_units"]

        coldata.data.attrs["vertical_layer"]["start"] = str(
            Unit(alt_units).convert(coldata.data.attrs["vertical_layer"]["start"], other="km")
        )

        coldata.data.attrs["vertical_layer"]["end"] = str(
            Unit(alt_units).convert(coldata.data.attrs["vertical_layer"]["end"], other="km")
        )

    def _get_vert_code(self, coldata: ColocatedData = None):
        if hasattr(coldata.data, "vertical_layer"):
            # start and end for vertical layers (display on web and name jsons)
            start = float(coldata.data.attrs["vertical_layer"]["start"])
            end = float(coldata.data.attrs["vertical_layer"]["end"])
            # format correctly (e.g., 1, 1.5, 2, 2.5, etc.)
            start = f"{round(float(start), 1):g}"
            end = f"{round(float(end), 1):g}"
            vert_code = f"{start}-{end}km"
        else:
            vert_code = coldata.get_meta_item("vert_code")
        return vert_code

    def _process_profile_data_for_visualization(
        self,
        data: dict[str, ColocatedData] = None,
        use_country: bool = False,
        region_names: dict[str:str] = None,
        station_names: ArrayLike = None,
        periods: tuple[str, ...] = None,
        seasons: tuple[str, ...] = None,
        obs_name: str = None,
        var_name_web: str = None,
        use_meteorological_seasons: bool = False,
    ):
        if region_names is None and station_names is None:
            raise ValueError("Both region_id and station_name can not both be None")

        # Loop through regions
        for regid in region_names:
            profile_viz = process_profile_data_for_regions(
                data=data,
                region_id=regid,
                use_country=use_country,
                periods=periods,
                seasons=seasons,
                use_meteorological_seasons=use_meteorological_seasons,
            )
            location = region_names[regid]
            self.exp_output.add_profile_entry(
                data,
                profile_viz,
                periods,
                seasons,
                location=location,
                network=obs_name,
                obsvar=var_name_web,
            )

        # Loop through stations
        for station_name in station_names:
            profile_viz = process_profile_data_for_stations(
                data=data,
                station_name=station_name,
                use_country=use_country,
                periods=periods,
                seasons=seasons,
                use_meteorological_seasons=use_meteorological_seasons,
            )

            self.exp_output.add_profile_entry(
                data,
                profile_viz,
                periods,
                seasons,
                location=station_name,
                network=obs_name,
                obsvar=var_name_web,
            )

    def _process_stats_timeseries_for_all_regions(
        self,
        data: dict[str, ColocatedData] | None = None,
        coldata: ColocatedData | None = None,
        main_freq: str | None = None,
        regnames: dict | None = None,
        use_weights: bool = True,
        drop_stats: tuple = (),
        use_country: bool = False,
        obs_name: str | None = None,
        obs_var: str = None,
        var_name_web: str | None = None,
        vert_code: str | None = None,
        model_name: str | None = None,
        model_var: str | None = None,
        meta_glob: dict | None = None,
        periods: tuple[str, ...] | None = None,
        seasons: tuple[str, ...] | None = None,
        add_trends: bool = False,
        trends_min_yrs: int = 7,
        regions_how: str = "default",
        regs: dict | None = None,
        stats_min_num: int = 1,
        use_fairmode: bool = False,
        avg_over_trends: bool = False,
        use_meteorological_seasons: bool = False,
    ):
        input_freq = self.cfg.statistics_opts.stats_tseries_base_freq

        args = [
            (
                reg,
                regnames,
                data,
                main_freq,
                use_weights,
                drop_stats,
                use_country,
                input_freq,
                obs_name,
                var_name_web,
                vert_code,
                model_name,
                model_var,
            )
            for reg in regnames
        ]
        num_workers = int(os.getenv(const.PYAEROCOM_NUM_WORKERS, "1"))
        if num_workers == 1:
            from multiprocessing.pool import ThreadPool as Pool
        else:
            from multiprocessing import Pool

        with Pool(processes=num_workers) as pool:
            results = pool.starmap(_process_statistics_timeseries_single_region, args)

        for (
            stats_ts,
            region,
            obs_name,
            var_name_web,
            vert_code,
            model_name,
            model_var,
        ) in results:
            self.exp_output.add_heatmap_timeseries_entry(
                stats_ts,
                region,
                obs_name,
                var_name_web,
                vert_code,
                model_name,
                model_var,
            )

        logger.info("Processing heatmap data for all regions")

        hm_all = _process_heatmap_data(
            data,
            regnames,
            use_weights,
            drop_stats,
            use_country,
            meta_glob,
            periods,
            seasons,
            add_trends,
            trends_min_yrs,
            avg_over_trends,
            use_meteorological_seasons,
        )

        for freq, hm_data in hm_all.items():
            self.exp_output.add_heatmap_entry(
                hm_data, freq, obs_name, var_name_web, vert_code, model_name, model_var
            )

        logger.info("Processing regional timeseries for all regions")
        ts_objs_regional = _process_regional_timeseries(data, regnames, regions_how, meta_glob)

        self.exp_output.write_timeseries(ts_objs_regional)
        if coldata.has_latlon_dims:
            for cd in data.values():
                if cd is not None:
                    cd.data = cd.flatten_latlondim_station_name().data

        logger.info("Processing individual site timeseries data")
        (ts_objs, map_meta, site_indices) = _process_sites(data, regs, regions_how, meta_glob)

        self.exp_output.write_timeseries(ts_objs)

        scatter_freq = min(TsType(fq) for fq in self.cfg.time_cfg.freqs)
        scatter_freq = min(scatter_freq, main_freq)

        logger.info("Processing map and scat data by period")

        for period in periods:
            # compute map_data and scat_data just for this period
            map_data, scat_data = _process_map_and_scat(
                data,
                map_meta,
                site_indices,
                [period],
                str(scatter_freq),
                stats_min_num,
                seasons,
                add_trends,
                trends_min_yrs,
                avg_over_trends,
                use_fairmode,
                obs_var,
                drop_stats,
                use_meteorological_seasons,
            )

            with self.avdb.lock():
                self.avdb.put_map(
                    map_data,
                    self.exp_output.proj_id,
                    self.exp_output.exp_id,
                    obs_name,
                    var_name_web,
                    vert_code,
                    model_name,
                    model_var,
                    period.replace("/", ""),  # Remove slashes in CAMS2_83 period.
                )

                self.avdb.put_scatter(
                    scat_data,
                    self.exp_output.proj_id,
                    self.exp_output.exp_id,
                    obs_name,
                    var_name_web,
                    vert_code,
                    model_name,
                    model_var,
                    period.replace("/", ""),  # Remove slashes in CAMS2_83 period.
                )

    def _process_diurnal_profiles(
        self,
        coldata: ColocatedData = None,
        regions_how: str = "default",
        regnames=None,
        meta_glob: dict = None,
    ):
        ts_objs_weekly, ts_objs_weekly_reg = _process_sites_weekly_ts(
            coldata, regions_how, regnames, meta_glob
        )

        for ts_data_weekly in ts_objs_weekly:
            self.exp_output.write_station_data(ts_data_weekly)
        if ts_objs_weekly_reg is not None:
            for ts_data_weekly_reg in ts_objs_weekly_reg:
                self.exp_output.write_station_data(ts_data_weekly_reg)

    def _process_fairmode(
        self,
        data: dict[str, ColocatedData] | None = None,
        obs_name: str | None = None,
        obs_var: str = None,
        var_name_web: str | None = None,
        vert_code: str | None = None,
        model_name: str | None = None,
        model_var: str | None = None,
        meta_glob: dict | None = None,
        periods: tuple[str, ...] | None = None,
        seasons: tuple[str, ...] | None = None,
        regions_how: str = "default",
        regs: dict | None = None,
        use_meteorological_seasons: bool = False,
    ):
        fairmode_statistics = FairmodeStatistics()
        species = fairmode_statistics.species
        freq = species[obs_var]["freq"]
        if freq not in data:
            if (
                "hourly" in data
            ):  # Most species use daily freq, but if daily is not present, but hourly is, then hourly can be resampled
                fm_data = data["hourly"].resample_time(freq, settings_from_meta=True)
            else:
                logger.warning(
                    f"Cannot calculate fairmode stats: Frequency {freq} could not be found for variable {obs_var}. Skipping..."
                )
            return
        else:
            fm_data = data[freq]
        (ts_objs, map_meta, site_indices) = _process_sites(data, regs, regions_how, meta_glob)

        stats = _calculate_fairmode(
            fm_data,
            fairmode_statistics,
            map_meta,
            obs_var,
            periods,
            seasons,
            use_meteorological_seasons,
        )
        fairmode_statistics.save_fairmode_stats(
            self.exp_output, stats, obs_name, var_name_web, vert_code, model_name, model_var
        )
