import glob
import logging

from datetime import timedelta, datetime, date

from pyaerocom.aeroval._processing_base import HasColocator, ProcessingEngine
from pyaerocom.io.cams2_83.read_obs import obs_paths


from .engine import CAMS2_83_Engine

logger = logging.getLogger(__name__)


class CAMS2_83_Processer(ProcessingEngine, HasColocator):
    def _run_single_entry(self, model_name, obs_name, var_list, analysis=False):

        logger.info(f"Running CAMS2_83_Processer._run_single_entry with var_list {var_list} and model name {model_name}")

        col = self.get_colocator(model_name, obs_name)
        forecast_days = self.cfg.statistics_opts.forecast_days

        if self.cfg.processing_opts.only_json:
            # files_to_convert = col.get_available_coldata_files(var_list) # this reads data only from standard subfolders, not folders like CAMS2-83-[model_name]-day0-FC, which are the only relevant here
            preprocessed_coldata_dir = self.cfg.path_manager.get_coldata_dir()
            mask = f"{preprocessed_coldata_dir}/CAMS2-83-{model_name}-day*/*.nc"
            files_to_convert = glob.glob(mask)

            if not analysis:
                per_mask = f"{preprocessed_coldata_dir}/CAMS2-83-{model_name}-persistence*/*.nc"
                per_files = glob.glob(per_mask)
                files_to_convert += per_files   
   

        else:
            files_to_convert = []
            for leap in range(forecast_days):
                runtype = "AN" if analysis else "FC"
                model = col.colocation_setup.model_id.split(".")[1]
                model_id = f"CAMS2-83.{model}.day{leap}.{runtype}"
                model_name = f"CAMS2-83-{model}-day{leap}-{runtype}"
                col.colocation_setup.model_id = model_id
                col.colocation_setup.model_name = model_name
                col.run(var_list)

            if not analysis:

                runtype = "FC"
                model = col.colocation_setup.model_id.split(".")[1]
                model_id = f"CAMS2-83.{model}.day0.{runtype}"
                model_name = f"CAMS2-83-{model}-persistence-{runtype}"
                if isinstance(col.colocation_setup.start, int):
                    new_start = datetime(year=col.colocation_setup.start, month=1, day=1)  - timedelta(days=1)
                else:
                    new_start = col.colocation_setup.start - timedelta(days=1)
                new_model_start = (datetime.strptime(col.colocation_setup.model_kwargs["daterange"][0], "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
                
                col.colocation_setup.model_id = model_id
                col.colocation_setup.model_name = model_name
                col.colocation_setup.start = new_start
                col.colocation_setup.model_kwargs["daterange"][0] = new_model_start

                col.run(var_list)



            files_to_convert = col.files_written

        if self.cfg.processing_opts.only_colocation:
            logger.info(
                f"FLAG ACTIVE: only_colocation: Skipping "
                f"computation of json files for {obs_name} /"
                f"{model_name} combination."
            )
        else:
            engine = CAMS2_83_Engine(self.cfg)
            engine.run(files_to_convert, var_list)

    def run(
        self,
        model_name=None,
        obs_name=None,
        var_list=None,
        update_interface=True,
        analysis=False,
        obs_path=None,
    ):
        if isinstance(var_list, str):
            var_list = [var_list]

        self.cfg._check_time_config()
        model_list = self.cfg.model_cfg.keylist(model_name)
        obs_list = self.cfg.obs_cfg.keylist(obs_name)

        logger.info("Start processing")

        if not self.cfg.processing_opts.only_model_maps:
            for obs_name in obs_list:
                for model_name in model_list:
                    self._run_single_entry(model_name, obs_name, var_list, analysis)

        if update_interface:
            self.update_interface()
        logger.info("Finished processing.")

    def update_interface(self):
        self.exp_output.update_interface()
