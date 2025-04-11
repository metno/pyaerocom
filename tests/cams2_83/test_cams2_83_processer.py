from datetime import datetime, timedelta

from pyaerocom.aeroval import EvalSetup
from pyaerocom.scripts.cams2_83.processer import CAMS2_83_Processer
from tests.conftest import lustre_unavail


@lustre_unavail
def test__run_single_entry(patched_config, tmp_path):
    setup = EvalSetup(**patched_config)
    processer = CAMS2_83_Processer(setup)
    processer.cfg._check_time_config()
    assert processer.cfg.colocation_opts.start == "2025/03/01 00:00:00"

    col = processer.get_colocator("EMEP", "EEA")
    startstring = datetime.strptime(
        col.colocation_setup.model_kwargs["daterange"][0], "%Y-%m-%d"
    ).strftime("%Y%m%d")
    stopstring = datetime.strptime(
        col.colocation_setup.model_kwargs["daterange"][1], "%Y-%m-%d"
    ).strftime("%Y%m%d")
    newstartstring = (
        datetime.strptime(col.colocation_setup.model_kwargs["daterange"][0], "%Y-%m-%d")
        - timedelta(days=1)
    ).strftime("%Y%m%d")

    var = "concno2"
    model_name = "EMEP"
    processer._run_single_entry(
        model_name=model_name, obs_name="EEA", var_list=[var], analysis=False
    )

    assert col.colocation_setup.model_name == model_name
    d0 = (
        tmp_path
        / f"{processer.cfg.proj_id}/{processer.cfg.exp_id}/CAMS2-83-{model_name}-day0-FC/{var}_{var}_MOD-CAMS2-83-{model_name}-day0-FC_REF-EEA-UTD_{startstring}_{stopstring}_hourly_ALL-wMOUNTAINS.nc"
    )
    dp = (
        tmp_path
        / f"{processer.cfg.proj_id}/{processer.cfg.exp_id}/CAMS2-83-{model_name}-persistence-FC/{var}_{var}_MOD-CAMS2-83-{model_name}-persistence-FC_REF-EEA-UTD_{newstartstring}_{stopstring}_hourly_ALL-wMOUNTAINS.nc"
    )

    assert d0.is_file()
    assert dp.is_file()
