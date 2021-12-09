from enum import Enum


class ModelName(str, Enum):
    EMEP = "emep"
    DEHM = "dehm"
    EURAD = "euradim"
    GEMAQ = "gemaq"
    LOTOS = "lotos"
    MATCH = "match"
    SILAM = "silam"
    MOCAGE = "mocage"
    CHIMERE = "chimere"
    ENSEMBLE = "ensemble"

    def __str__(self) -> str:
        return self.value


# Change this to use the correct species names that are used in the netCDF file
class PollutantName(str, Enum):
    NO2 = "nitrogen_dioxide"
    O3 = "ozone"
    PM10 = "particulate_matter_10um"
    PM25 = "particulate_matter_2.5um"
    SO2 = "sulphur_dioxide"
    CO = "carbon_monoxide"

    def __str__(self) -> str:
        return self.value
