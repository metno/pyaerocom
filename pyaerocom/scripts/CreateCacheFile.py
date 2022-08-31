from pyaerocom import const
from pyaerocom.io import ReadUngridded

CACHE_CONFIG = {
    const.MARCO_POLO_NAME: dict(
        vars_to_cache=[
            "concpm10",
            "concpm25",
            "vmrno2",
            "vmro3",
        ]
    ),
    const.AERONET_SUN_V3L2_SDA_DAILY_NAME: dict(
        vars_to_cache=['od550gt1aer']
    ),
    const.AERONET_SUN_V2L2_AOD_DAILY_NAME: dict(
        vars_to_cache=['ang4487aer', 'od550aer', ]
    ),
    const.AERONET_SUN_V3L15_SDA_DAILY_NAME: dict(
        vars_to_cache=['od550gt1aer']
    ),
    const.AERONET_SUN_V2L15_AOD_DAILY_NAME: dict(
        vars_to_cache=['ang4487aer', 'od550aer', ]
    ),
    const.EBAS_MULTICOLUMN_NAME: dict(
        vars_to_cache=[
            "concpm10",
            "concpm25",
            "vmrno2",
            "vmro3",
        ]
    ),
    const.EEA_NRT_NAME: dict(
        vars_to_cache=[
            "concpm10",
            "concpm25",
            "vmrno2",
            "vmro3",
        ]
    ),
    const.AIR_NOW_NAME: dict(
        vars_to_cache=[
            "concpm10",
            "concpm25",
            "vmrno2",
            "vmro3",
        ]
    ),

}


def main():
    for data_id in CACHE_CONFIG:
        reader = ReadUngridded(data_id)
        for var_to_read in CACHE_CONFIG[data_id]["vars_to_cache"]:
            data = reader.read(vars_to_retrieve=var_to_read)
            print(f"# of unique stations: {len(data.unique_station_names)}")
            print(data)


if __name__ == "__main__":
    main()
