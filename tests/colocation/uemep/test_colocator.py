from ...conftest import lustre_unavail
from pyaerocom.colocation.uemep import UEMEPColocator
import pathlib

UEMEP_STATION_FOLDER = pathlib.Path(
    "/lustre/storeB/project/fou/kl/emep/ModelRuns/uEMEP/uEMEP_norway/rerun/2023/stations"
)
UEMEP_STATION_FILES = sorted(list(UEMEP_STATION_FOLDER.glob("*.nc")))[:7]  # One week of files.


@lustre_unavail
def test_UEMEPColocator(tmpdir):
    colocator = UEMEPColocator(
        uemep_station_data=UEMEP_STATION_FILES, var_names="conco3", obs=["EBASMC"], out_dir=tmpdir
    )
    colocator.run()

    files = list(pathlib.Path(tmpdir).glob("*.nc"))
    assert len(files) == 1
    assert (
        files[0].name
        == "conco3_conco3_MOD-uemep_REF-EBASMC_20230101_20230108_hourly_ALL-wMOUNTAINS.nc"
    )
