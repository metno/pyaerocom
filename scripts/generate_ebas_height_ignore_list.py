# Script used to generate EBAS_height_ignore. Requires a recent version of pyaro to be installed,
# and access to the ebas file index.
import sqlite3
import pathlib
from pyaro.timeseries.Filter import ValleyFloorRelativeAltitudeFilter
from pyaro.timeseries.Station import Station

filter = ValleyFloorRelativeAltitudeFilter(topo="/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/GTOPO30/merged", radius=5000, lower = 500)


EBAS_FILE_INDEX = pathlib.Path(
    "/lustre/storeB/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/ebas_file_index.sqlite3"
)


con = sqlite3.connect(EBAS_FILE_INDEX)
con.row_factory = sqlite3.Row
cur = con.cursor()

cur.execute(
    """
    SELECT station_code, station_name, station_latitude, station_longitude, station_altitude FROM station
    """
)

rows = [dict(x) for x in cur.fetchall()]
stations: dict[str, Station] = {}
missing_alt_sites = []
for r in rows:
    try:
        stations[r["station_code"]] = Station(
            {
                "station": r["station_code"],
                "latitude": float(r["station_latitude"]),
                "longitude": float(r["station_longitude"]),
                "altitude": float(r["station_altitude"]),
                "long_name": "",
                "country": "",
                "url": ""
            }
        )
    except TypeError:
        print(f"Station code '{r['station_code']}' is missing one or more of latitude, longitude, altitude, which are necessary to calculate relative altitude. This station will be ignored.")
        try:
            float(r["station_altitude"])
        except Exception:
            missing_alt_sites.append(r["station_code"])
        pass



sites = list(filter.filter_stations(stations).values())

print(",\n".join([f"\"{s.station}\"" for s in sorted(sites, key=lambda x : x.station)]))

print(f"Sites filtered: {len(sites)}")
print(f"Sites missing altitude: {',\n'.join([f'\"{s}\"' for s in sorted(missing_alt_sites)])}")
