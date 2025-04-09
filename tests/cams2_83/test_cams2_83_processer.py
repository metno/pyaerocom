from pyaerocom.aeroval import EvalSetup
from pyaerocom.scripts.cams2_83.processer import CAMS2_83_Processer
from tests.conftest import lustre_unavail


@lustre_unavail
def test__run_single_entry(patched_config, tmp_path):
    setup = EvalSetup(**patched_config)
    processer = CAMS2_83_Processer(setup)
    processer.cfg._check_time_config()
    assert processer.cfg.colocation_opts.start == "2025/03/01 00:00:00"

    processer._run_single_entry(
        model_name="EMEP", obs_name="EEA", var_list=["concno2"], analysis=False
    )
    d0 = (
        tmp_path
        / "cams2-83/prototype/CAMS2-83-EMEP-day0-FC/concno2_concno2_MOD-CAMS2-83-EMEP-day0-FC_REF-EEA-UTD_20250301_20250301_hourly_ALL-wMOUNTAINS.nc"
    )
    dp = (
        tmp_path
        / "cams2-83/prototype/CAMS2-83-EMEP-persistence-FC/concno2_concno2_MOD-CAMS2-83-EMEP-persistence-FC_REF-EEA-UTD_20250228_20250301_hourly_ALL-wMOUNTAINS.nc"
    )

    assert d0.is_file()
    assert dp.is_file()
