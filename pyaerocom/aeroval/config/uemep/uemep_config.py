import pyaerocom as pya
import pathlib


STATION_DATA = pathlib.Path(
    "/lustre/storeB/project/fou/kl/emep/ModelRuns/uEMEP/uEMEP_norway/rerun/2023/stations"
)


if __name__ == "__main__":
    obs_reader = pya.io.mscw_ctm.reader.ReadMscwCtm(
        "EMEP", data_dir=str(STATION_DATA), file_pattern="^uEMEP_Norway_station_\d+_\d\d\.nc$"
    )

    obs_reader.read_var("vmro3", ts_type="hourly")
