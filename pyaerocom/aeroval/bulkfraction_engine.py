import logging

from pyaerocom import ColocatedData
from pyaerocom.aeroval._processing_base import HasColocator, ProcessingEngine
from pyaerocom.aeroval.obsentry import ObsEntry
from pyaerocom.aeroval.modelentry import ModelEntry
from pyaerocom.aeroval.coldatatojson_engine import ColdataToJsonEngine


from pyaerocom.colocation.colocator import Colocator
from pyaerocom.colocation.colocation_setup import ColocationSetup


logger = logging.getLogger(__name__)


class BulkFractionEngine(ProcessingEngine, HasColocator):
    def run(self, var_list: list[str] | str | None, model_name: str, obs_name: str):
        self.sobs_cfg = self.cfg.obs_cfg.get_entry(obs_name)
        self.smodel_cfg = self.cfg.model_cfg.get_entry(model_name)

        if var_list is None:
            var_list = self.sobs_cfg.obs_vars
        elif isinstance(var_list, str):
            var_list = [var_list]
        elif not isinstance(var_list, list):
            raise ValueError(f"invalid input for var_list: {var_list}.")

        files_to_convert = []
        for var_name in var_list:
            bulk_vars = self._get_bulk_vars(var_name, self.sobs_cfg)

            freq = self.sobs_cfg.ts_type
            cd, fp = self._run_var(
                model_name, obs_name, var_name, bulk_vars, freq, self.sobs_cfg, self.smodel_cfg
            )

            files_to_convert.append(fp)

        engine = ColdataToJsonEngine(self.cfg)
        engine.run(files_to_convert)

    def _get_bulk_vars(self, var_name: str, cfg: ObsEntry) -> list:
        bulk_vars = cfg.bulk_options
        if var_name not in bulk_vars:
            raise KeyError(f"Could not find bulk vars entry for {var_name}")

        if len(bulk_vars[var_name].vars) != 2:
            raise ValueError(
                f"(Only) 2 entries must be present for bulk vars to calculate fraction for {var_name}. Found {bulk_vars[var_name]}"
            )

        return bulk_vars[var_name].vars

    def _run_var(
        self,
        model_name: str,
        obs_name: str,
        var_name: str,
        bulk_vars: list,
        freq: str,
        obs_entry: ObsEntry,
        model_entry: ModelEntry,
    ) -> tuple[ColocatedData, str]:
        model_exists = obs_entry.bulk_options[var_name].model_exists

        cols = self.get_colocators(bulk_vars, var_name, freq, model_name, obs_name, model_exists)

        coldatas = []
        for col in cols:
            if len(list(col.keys())) != 1:
                raise ValueError(
                    "Found more than one colocated object when trying to run bulk variable"
                )
            bv = list(col.keys())[0]
            coldatas.append(col[bv].run(bv))

        num_name, denum_name = bulk_vars[0], bulk_vars[1]
        num_col = cols[0][num_name].run(num_name)
        denum_col = cols[1][denum_name].run(denum_name)

        model_num_name, model_denum_name = self._get_model_var_names(
            var_name, bulk_vars, model_exists, model_entry
        )

        cd = self._combine_coldatas(
            num_col[model_num_name][num_name],
            denum_col[model_denum_name][denum_name],
            var_name,
            obs_entry,
        )

        num_colocator = cols[0][num_name]

        fp = cd.to_netcdf(
            out_dir=num_colocator.output_dir,
            savename=cd._aerocom_savename(
                var_name,
                obs_name,
                var_name,
                model_name,
                num_colocator.get_start_str(),
                num_colocator.get_stop_str(),
                freq,
                num_colocator.colocation_setup.filter_name,
                None,  # cd.data.attrs["vert_code"],
            ),
        )
        return cd, fp

    def _combine_coldatas(
        self,
        num_coldata: ColocatedData,
        denum_coldata: ColocatedData,
        var_name: str,
        obs_entry: ObsEntry,
    ) -> ColocatedData:
        mode = obs_entry.bulk_options[var_name].mode
        model_exists = obs_entry.bulk_options[var_name].model_exists
        units = obs_entry.bulk_options[var_name].units

        if mode == "fraction":
            new_data = num_coldata.data / denum_coldata.data

        elif mode == "product":
            new_data = num_coldata.data * denum_coldata.data
        else:
            raise ValueError(f"Mode must be either fraction of product, and not {mode}")
        if model_exists:
            # TODO: Unsure if this works!!!
            new_data[1] = num_coldata.data[1].where(new_data[1])

        cd = ColocatedData(new_data)

        cd.data.attrs = num_coldata.data.attrs
        cd.data.attrs["var_name"] = [var_name, var_name]
        cd.data.attrs["var_units"] = [units, units]
        cd.metadata["var_name_input"] = [var_name, var_name]
        return cd

    def _get_model_var_names(
        self, var_name: str, bulk_vars: list[str], model_exists: bool, model_entry: ModelEntry
    ) -> tuple[str]:
        num_name, denum_name = bulk_vars[0], bulk_vars[1]
        if model_exists:
            num_name, denum_name = var_name, var_name

        model_use_vars = model_entry.model_use_vars
        if model_use_vars != {}:
            num_name, denum_name = model_use_vars[num_name], model_use_vars[denum_name]

        return num_name, denum_name

    def get_colocators(
        self,
        bulk_vars: list,
        var_name: str,
        freq: str,
        model_name: str = None,
        obs_name: str = None,
        model_exists: bool = False,
    ) -> list[dict[str | Colocator]]:
        """
        Instantiate colocation engine

        Parameters
        ----------
        model_name : str, optional
            name of model. The default is None.
        obs_name : str, optional
            name of obs. The default is None.

        Returns
        -------
        Colocator

        """
        col_cfg = {**self.cfg.colocation_opts.model_dump()}
        outdir = self.cfg.path_manager.get_coldata_dir()
        col_cfg["basedir_coldata"] = outdir

        if model_name:
            mod_cfg = self.cfg.get_model_entry(model_name)
            col_cfg["model_cfg"] = mod_cfg

            # Hack and at what lowlevel_helpers's import_from was doing
            for key, val in mod_cfg.items():
                if key in ColocationSetup.model_fields:
                    col_cfg[key] = val
        if obs_name:
            obs_cfg = self.cfg.get_obs_entry(obs_name)
            pyaro_config = obs_cfg["obs_config"] if "obs_config" in obs_cfg else None
            col_cfg["obs_config"] = pyaro_config

            # Hack and at what lowlevel_helpers's import_from was doing
            for key, val in obs_cfg.model_dump().items():
                if key in ColocationSetup.model_fields:
                    col_cfg[key] = val

            col_cfg["add_meta"].update(diurnal_only=self.cfg.get_obs_entry(obs_name).diurnal_only)
        cols = []
        col_cfg["ts_type"] = freq
        for bulk_var in bulk_vars:
            col_cfg["obs_vars"] = bulk_var
            if model_exists:
                col_cfg["model_use_vars"] = {
                    bulk_var: var_name,
                }
            col_stp = ColocationSetup(**col_cfg)
            col = Colocator(col_stp)

            cols.append({bulk_var: col})

        return cols
