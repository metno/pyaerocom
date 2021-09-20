#!/usr/bin/env python
"""
Read ETEX1 observations into a Pandas DataFrame

TODO:
proper integration as an new observation ID
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Generator

import pandas as pd
from numpy import sign

from pyaerocom.ungriddeddata import UngriddedData

ETEX1 = SimpleNamespace(
    long_name="PMCH concentration above ambient level",
    units="ng/m3",
    version="etex1_v1.1.960505",
    stations=Path("/lustre/storeB/users/magnusu/ETEX-1/stationlist.950130"),
    concentrations=Path("/lustre/storeB/users/magnusu/ETEX-1/pmch.dat"),
    quality=Path("/lustre/storeB/users/magnusu/ETEX-1/pmch.cod"),
    samples=[f"{n:02}" for n in range(30)],
    sample_start=[
        datetime(1994, 10, 23, 15, tzinfo=timezone.utc) + timedelta(h) for h in range(30)
    ],
    sample_end=[datetime(1994, 10, 23, 18, tzinfo=timezone.utc) + timedelta(h) for h in range(30)],
    flags={
        0: "not sampled",
        1: "valid sample, no tracer found",
        11: "valid sample, tracer found",
        21: "concentration within 2std of background variation",
        31: "concentration given or higher",
        41: "tracer detected, but can't be quantified",
        10: "lost in sampling",
        20: "lost in analysis",
        30: "lost in shipment",
    },
)


def read_etex1() -> UngriddedData:
    def reader() -> Generator[dict]:
        station = read_stations().set_index("cc")
        for cc, df in read_data().groupby("cc"):
            site = station.loc[cc]
            conc = df.rename(columns={"end": "time"}).set_index("time").concentration
            conc.name = "concch"
            yield dict(
                station_id=site.name,
                station_name=site["Station name"],
                latitude=site.Long,
                longitude=site.Lat,
                altitude=site.Alt,
                concch=conc,
                var_info=dict(concch=dict(units=ETEX1.units, ts_type="3hourly")),
            )

    return UngriddedData.from_station_data(list(reader()))


def degrees_with_minutes(x: str) -> float:
    """
    trasnform station coordiantes "degree.minutes" to float
    """
    degrees, minutes = x.split(".")
    return int(degrees) + int(minutes) / 60 * sign(float(x))


def read_stations(path: Path = ETEX1.stations) -> pd.DataFrame:
    return pd.read_csv(
        path,
        delimiter=", ",
        header=3,
        skipfooter=26,
        engine="python",
        converters=dict(Lat=degrees_with_minutes, Long=degrees_with_minutes),
    ).astype(
        {
            "cc": "string",
            "Station name": "string",
            "Lat": "float16",
            "Long": "float16",
            "Alt": "int16",
            "WMOCode": "string",
            "Remarks": "string",
        }
    )


def read_pmch(path: Path, name: str, **kwargs) -> pd.DataFrame:
    columns = ["index", "cc"] + ETEX1.samples
    series = pd.read_csv(
        path,
        delim_whitespace=True,
        header=1,
        names=columns,
        usecols=columns[1:],
        index_col="cc",
        **kwargs,
    ).unstack()
    series.index.names = ["sample", "cc"]
    series.name = name
    return series.reset_index()


def read_data() -> pd.DataFrame:
    dat = read_pmch(ETEX1.concentrations, "concentration", na_values=[-0.99, -0.88])
    cod = read_pmch(ETEX1.quality, "quality")
    cod["quality"] = pd.Categorical(cod.quality).rename_categories(ETEX1.flags)

    time = pd.DataFrame(
        {"sample": ETEX1.samples, "start": ETEX1.sample_start, "end": ETEX1.sample_end}
    )
    return pd.merge(dat, cod).merge(time, on="sample").drop("sample", axis="columns")


if __name__ == "__main__":
    print(f"{ETEX1.long_name} [{ETEX1.units}]")

    data = read_etex1()
    print(data)
