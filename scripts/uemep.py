import pathlib

from pyaerocom.colocation.uemep import UEMEPColocator
import logging

logging.basicConfig(
    level=logging.DEBUG, 
    handlers=[logging.StreamHandler()],
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

UEMEP_PATH = pathlib.Path(
    "/lustre/storeB/project/fou/kl/emep/ModelRuns/uEMEP/uEMEP_norway/rerun/2023/stations"
)

TEST_FILE_PATH = UEMEP_PATH / "uEMEP_Norway_station_20230101_00.nc"

def main():
    colocator = UEMEPColocator(
        uemep_station_data = UEMEP_PATH,
        obs = ["EBASMC"],
        var_names = ["conco3"],
    )
    colocator.run()

if __name__ == "__main__":
    main()
