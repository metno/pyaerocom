from pyaerocom.io import ReadUngridded


def main():
    DATA_ID = const.MARCO_POLO_NAME
    reader = ReadUngridded(DATA_ID)
    vars_to_cache = [
        "concpm10",
        "concpm25",
    ]

    for var_to_read in vars_to_cache:
        data = reader.read(vars_to_retrieve=var_to_read)
        print(f"# of unique stations: {len(data.unique_station_names)}")
        print(data)


if __name__ == "__main__":
    main()
