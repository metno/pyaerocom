from pyaerocom.aeroval import EvalSetup
from pyaerocom.aeroval.config.emep.reporting_base import get_CFG


def test_aeroval_config_emep():
    # Setup for models used in analysis
    CFG = get_CFG(
        reportyear=2024,
        year=2021,
        model_dir="/lustre/storeB/project/fou/kl/emep/ModelRuns/2024_REPORTING/EMEP01_rv5.3_metyear2021_emis2022",
    )

    CFG.update(
        dict(
            exp_id="test-2021met_2022emis",
            exp_name="Test runs for 2024 EMEP reporting",
            exp_descr=(
                "Test run from Agnes for 2024_REPORTING/EMEP01_rv5.3_metyear2021_emis2022, i.e. 2021met and 2022emis"
            ),
            exp_pi="S. Tsyro, A. Nyiri, H. Klein",
        )
    )

    # remove "concCocpm10", not in model-output
    for obs in CFG["obs_cfg"]:
        if "concCocpm10" in CFG["obs_cfg"][obs]["obs_vars"]:
            CFG["obs_cfg"][obs]["obs_vars"].remove("concCocpm10")

    # remove "no, pm10, pm25" from EBAS-hourly
    CFG["obs_cfg"]["EBAS-h-diurnal"]["obs_vars"].remove("concNno")
    CFG["obs_cfg"]["EBAS-h-diurnal"]["obs_vars"].remove("concpm10")
    CFG["obs_cfg"]["EBAS-h-diurnal"]["obs_vars"].remove("concpm25")

    stp = EvalSetup(**CFG)

    assert stp.periods == ["2021"]
    assert stp.exp_pi == "S. Tsyro, A. Nyiri, H. Klein"
    assert stp.proj_id == "emep"
