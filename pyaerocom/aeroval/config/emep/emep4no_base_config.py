from .reporting_base import get_CFG as get_EMEP_CFG


def get_CFG(year: int, model_dir: str, *, file_pattern: str = r"^RERUN2022_{freq}_.+\.nc$"):
    """Basically the EMEP base config with minor changes
    to work with EMEP4NO input. Please also refer to the
    EMEP config documentation as that is where the bulk
    of the configuration takes place.

    :param year: Year of data
    :param model_dir: Directory where EMEP4NO files are located.
    :param file_pattern: Optional regular expression against which the base name of files will
        be matched. This can be used to override the default `Base_{freq}.nc` file matching in
        the EMEP reader.

        Note that for convenience the string literal '{freq}' can be included as part of the
        pattern and will be expanded to (hour|day|month|fullrun). This is recommended, as
        the presence of these strings are used to derive ts_type, which is currently necessary
        for reading.

    :returns: A dict of model configuration which can be passed to EvalSetup.

    Example
    -------------

    The following snippet shows how this config can be used.

    >>> from pyaerocom.aeroval.config.emep.emep4no_base_config import get_CFG # doctest: +SKIP
    >>> import pathlib
    >>>
    >>> if __name__ == "__main__":
    ...     import matplotlib.pyplot as plt
    ...     import pyaerocom as pya
    ...     from pyaerocom import const
    ...     from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
    ...
    ...     # Customize cache dir to avoid disk quota issues.
    ...     # cdir = pathlib.Path("./cache")
    ...     # cdir.mkdir(exist_ok=True)
    ...     # const.CACHEDIR = str(cdir)
    ...
    ...     cfg = get_CFG(2022, "/lustre/storeB/project/fou/kl/emep/ModelRuns/EMEP4NO/EMEP4NO_rerun_2022/")
    ...
    ...     # Change any experiment details.
    ...     cfg.update(
    ...         {
    ...             #"proj_id": "<project name>",
    ...             #"exp_id": "<experiment name>",
    ...             #"json_basedir": "/lustre/storeB/users/thlun8736/python/aeroval/data",
    ...             #"coldata_basedir": "/lustre/storeB/users/thlun8736/python/aeroval/coldata",
    ...         }
    ...     )
    ...
    ...     # Run the experiment.
    ...     stp = EvalSetup(**cfg)
    ...     ana = ExperimentProcessor(stp)
    ...     res = ana.run()
    """
    cfg = get_EMEP_CFG(None, year, model_dir)

    # Ensure files are matched properly by overriding 'Base_{freq}.nc'
    # matching in reader.
    cfg["model_cfg"]["EMEP"]["model_kwargs"] = {"file_pattern": file_pattern}

    cfg.update(
        {
            "exp_id": "emep4no",
            "exp_name": "Evaluation of EMEP4NO runs",
            "exp_descr": "Evaluation of EMEP4NO runs",
            "add_model_maps": False,
            "raise_exceptions": False,
        }
    )
    return cfg
