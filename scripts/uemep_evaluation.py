from pyaerocom.aeroval.config.uemep.uemep_base import get_CFG


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import pyaerocom as pya
    from pyaerocom import const
    from pyaerocom.aeroval import EvalSetup, ExperimentProcessor

    plt.close("all")
    cfg = get_CFG(2024, 2022, "/lustre/storeB/project/fou/kl/emep/ModelRuns/EMEP4NO/EMEP4NO_rerun_2022/")

    cfg.update(
        {
            "add_model_maps": False,
            "proj_id": "uemep_test",
            "exp_id": "20241231",
            "exp_pi": "thlun8736@met.no",
            "json_basedir": "/lustre/storeB/users/thlun8736/python/aeroval/data",
            "coldata_basedir": "/lustre/storeB/users/thlun8736/python/aeroval/coldata",
            "raise_exceptions": False
        }
    )
    cfg["model_cfg"]["EMEP"]["model_kwargs"] = {
        "file_pattern": r"^RERUN2022_{freq}_.+\.nc$"
    }
    stp = EvalSetup(**cfg)

    ana = ExperimentProcessor(stp)

    res = ana.run()