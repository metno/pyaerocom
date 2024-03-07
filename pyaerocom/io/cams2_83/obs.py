from __future__ import annotations

import logging
from datetime import datetime, timezone, tzinfo
from pathlib import Path
from types import SimpleNamespace
from typing import Protocol

import pandas as pd

logger = logging.getLogger(__name__)


"""CAMS2-50 domain boundaries"""
CAMS2_50_DOMAIN = SimpleNamespace(
    lat=(30, 72),  # °N
    lon=(-25, 45),  # °E
)


class Domain(Protocol):
    """domain for static type checking"""

    lat: tuple[float, float]
    lon: tuple[float, float]


def in_domain(df: pd.DataFrame, *, domain: Domain) -> pd.Series:
    """check if rows are inside the domain"""
    return df["lon"].between(*domain.lon) & df["lat"].between(*domain.lat)


def add_time(df: pd.DataFrame) -> pd.DataFrame:
    """combine year/month/day/hour into a singre datetime column"""
    dt = lambda row: datetime(row.Y, row.M, row.D, row.H, tzinfo=timezone.utc)

    df = df.rename(columns={"Y": "year", "M": "month", "D": "day", "H": "hour"})
    time = pd.to_datetime(df[["year", "month", "day", "hour"]], utc=True)

    return df.assign(time=time).drop(["year", "month", "day", "hour"], axis="columns")


def conc_units(df: pd.DataFrame) -> pd.DataFrame:
    """convert kg/m3 to μg/m3"""
    return df.assign(conc=df.conc * 1e9)


def poll_names(df: pd.DataFrame) -> pd.DataFrame:
    """rename pollutant names"""
    poll = df.poll.str.upper().str.replace("PM2P5", "PM25", regex=False)
    return df.assign(poll=poll)


def read_csv(path: str | Path, *, domain: Domain = CAMS2_50_DOMAIN) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        sep=";",
        header=0,
        names="station lat lon alt poll Y M D H _ conc".split(),
        usecols=lambda x: x != "_",
    )
    df = df.pipe(add_time).pipe(conc_units).pipe(poll_names)
    if not in_domain(df, domain=domain).all():
        logger.warning("found obs outside the model domain")
        df = df[in_domain(df, domain=domain)]
    if (df.conc <= 0).any():
        logger.warning("found negative obs")
        df = df[df.conc > 0]
    return df["station lat lon alt time poll conc".split()]
