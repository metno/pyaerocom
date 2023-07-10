#!/usr/bin/env python3

import logging
from multiprocessing import dummy

from pyaerocom.aeroval._processing_base import HasColocator, ProcessingEngine
from pyaerocom.aeroval.coldatatojson_engine import ColdataToJsonEngine
from pyaerocom.aeroval.helpers import delete_dummy_model, make_dummy_model
from pyaerocom.aeroval.modelmaps_engine import ModelMapsEngine
from pyaerocom.aeroval.superobs_engine import SuperObsEngine

logger = logging.getLogger(__name__)


class ExperimentProcessor(ProcessingEngine, HasColocator):
    """Processing engine for AeroVal experiment

    By default, this class processes one configuration file, represented by
    :class:`EvalSetup`. As such, an instance of :class:`EvalSetup` represents
    an AeroVal experiment, comprising a list of models, a list of observations
    (and variables).

    For each possible (or defined) model / obs / variable combination, the
    processing engine will perform spatial and temporal co-location and will
    store on co-located NetCDF file (e.g. if there are 2 models, 2 observation
    networks and 2 variables there will be 4 co-located NetCDF files).
    The co-location is done using :class:`pyaerocom.colocation_auto.Colocator`.

    """

    def _run_single_entry(self, model_name, obs_name, var_list):
        if model_name == obs_name:
            msg = f"Cannot run same dataset against each other ({model_name} vs. {obs_name})"
            logger.info(msg)
            return
        ocfg = self.cfg.get_obs_entry(obs_name)
        if ocfg["is_superobs"]:
            try:
                engine = SuperObsEngine(self.cfg)
                engine.run(
                    model_name=model_name,
                    obs_name=obs_name,
                    var_list=var_list,
                    try_colocate_if_missing=True,
                )
            except Exception:
                if self.raise_exceptions:
                    raise
                logger.warning("failed to process superobs...")
        elif ocfg["only_superobs"]:
            logger.info(
                f"Skipping json processing of {obs_name}, as this is "
                f"marked to be used only as part of a superobs "
                f"network"
            )
        else:
            col = self.get_colocator(model_name, obs_name)
            if self.cfg.processing_opts.only_json:
                files_to_convert = col.get_available_coldata_files(var_list)
            else:
                col.run(var_list)
                files_to_convert = col.files_written

            if self.cfg.processing_opts.only_colocation:
                logger.info(
                    f"FLAG ACTIVE: only_colocation: Skipping "
                    f"computation of json files for {obs_name} /"
                    f"{model_name} combination."
                )
            else:
                engine = ColdataToJsonEngine(self.cfg)
                engine.run(files_to_convert)

    def run(self, model_name=None, obs_name=None, var_list=None, update_interface=True):
        """Create colocated data and json files for model / obs combination

        Parameters
        ----------
        model_name : str or list, optional
            Name or pattern specifying model that is supposed to be analysed.
            Can also be a list of names or patterns to specify multiple models.
            If None (default), then all models are run that are part of this
            experiment.
        obs_name : :obj:`str`, or :obj:`list`, optional
            Like :attr:`model_name`, but for specification(s) of observations
            that are supposed to be used. If None (default) all observations
            are used.
        var_list : list, optional
            list variables supposed to be analysed. If None, then all
            variables available are used. Defaults to None. Can also be
            `str` type.
        update_interface : bool
            if true, relevant json files that determine what is displayed
            online are updated after the run, including the the menu.json file
            and also, the model info table (minfo.json) file is created and
            saved in :attr:`exp_dir`.

        Returns
        -------
        list
            list containing all colocated data objects that have been converted
            to json files.
        """
        if isinstance(var_list, str):
            var_list = [var_list]

        self.cfg._check_time_config()

        obs_list = self.cfg.obs_cfg.keylist(obs_name)
        if not self.cfg.model_cfg:
            logging.info("No model found, will make dummy model data")
            self.cfg.webdisp_opts.hide_charts = ["scatterplot"]
            self.cfg.webdisp_opts.hide_pages = ["maps.php", "intercomp.php", "overall.php"]
            model_id = make_dummy_model(obs_list, self.cfg)
            self.cfg.processing_opts.obs_only = True
            use_dummy_model = True
        else:
            model_id = None
            use_dummy_model = False

        model_list = self.cfg.model_cfg.keylist(model_name)

        logger.info("Start processing")

        # compute model maps (completely independent of obs-eval
        # processing below)
        if self.cfg.webdisp_opts.add_model_maps:
            engine = ModelMapsEngine(self.cfg)
            engine.run(model_list=model_list, var_list=var_list)

        if not self.cfg.processing_opts.only_model_maps:
            for obs_name in obs_list:
                for model_name in model_list:
                    self._run_single_entry(model_name, obs_name, var_list)

        if update_interface:
            self.update_interface()
        if use_dummy_model:
            delete_dummy_model(model_id)
        logger.info("Finished processing.")

    def update_interface(self):
        """Update aeroval interface

        Things done here:

            - Update menu file
            - Make aeroval info table json (tab informations in interface)
            - update and order heatmap file
        """
        self.exp_output.update_interface()
