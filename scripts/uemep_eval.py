from pyaerocom.aeroval.config.uemep.reporting_base import get_CFG
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import pyaerocom as pya
    from pyaerocom import const
    from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
    cfg = get_CFG(2024, 2022, "/lustre/storeB/project/fou/kl/emep/ModelRuns/2024_uEMEP_rerun_2022_aeroval")
    
    plt.close("all")
    stp = EvalSetup()

    ana = ExperimentProcessor(stp)

    res = ana.run()