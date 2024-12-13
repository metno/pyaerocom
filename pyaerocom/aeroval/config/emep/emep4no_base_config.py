from .reporting_base import get_CFG as get_EMEP_CFG


def get_CFG(reportyear: int, year: int, model_dir: str):
    """Basically the EMEP base config with minor changes
    to work with EMEP4NO input. Please also refer to the
    EMEP config documentation as that is where the bulk
    of the configuration takes place.

    Example
    -------------

    The following snippet shows how this config can be used.

    >>> from pyaerocom.aeroval.config.emep.emep4no_base_config import get_CFG # doctest: +SKIP
    >>> import pathlib
    >>>
    >>> if __name__ == "__main__":
    >>>     import matplotlib.pyplot as plt
    >>>     import pyaerocom as pya
    >>>     from pyaerocom import const
    >>>     from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
    >>>
    >>>     # Customize cache dire to avoid disk quota issues.
    >>>     # cdir = pathlib.Path("./.cache")
    >>>     # cdir.mkdir(exist_ok=True)
    >>>     # const.CACHEDIR = str(cdir)
    >>>
    >>>     cfg = get_CFG(2024, 2022, "/lustre/storeB/project/fou/kl/emep/ModelRuns/EMEP4NO/EMEP4NO_rerun_2022/")
    >>>
    >>>     cfg.update(
    >>>         {
    >>>             #"proj_id": "<project name>",
    >>>             #"exp_id": "<experiment name>",
    >>>             #"json_basedir": "/lustre/storeB/users/thlun8736/python/aeroval/data",
    >>>             #"coldata_basedir": "/lustre/storeB/users/thlun8736/python/aeroval/coldata",
    >>>         }
    >>>     )
    >>>
    >>>     stp = EvalSetup(**cfg)
    >>>     ana = ExperimentProcessor(stp)
    >>>     res = ana.run()
    """
    cfg = get_EMEP_CFG(reportyear, year, model_dir)

    # Ensure files are matched properly by overriding 'Base_{freq}.nc'
    # matching in reader.
    cfg["model_cfg"]["EMEP"]["model_kwargs"] = {"file_pattern": r"^RERUN2022_{freq}_.+\.nc$"}

    cfg.update({"add_model_maps": False, "raise_exceptions": False})
    return cfg
