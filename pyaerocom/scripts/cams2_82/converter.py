import typer
from pathlib import Path
from typing import Optional
import polars as pl
from datetime import datetime
import numpy as np
import logging

logger = logging.getLogger(__name__)

app = typer.Typer(add_completion=False, no_args_is_help=True)


@app.command()
def aeronet(
    raw_data_path: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        writable=False,
        help="Path of original raw aeronet files.",
    ),
    result_path: Path = typer.Argument(
        ...,
        help="Name and location of processed data file",
    ),
    start_date: datetime = typer.Argument(
        ..., formats=["%Y-%m-%d", "%Y%m%d"], help="evaluation start date"
    ),
    end_date: datetime = typer.Argument(
        ..., formats=["%Y-%m-%d", "%Y%m%d"], help="evaluation end date"
    ),):
   
    FLAG = -999

    def convert(aod500, lambda500, alpha):
        # if aod500 == FLAG or lambda500 == FLAG or alpha == FLAG:
        #     return np.nan
        return aod500 * (0.55 / lambda500) ** (-alpha)

    opath = result_path

    FIELDS = dict(
        aod500="AOD_500nm",
        lambda500="Exact_Wavelengths_of_AOD(um)_500nm",
        alpha="500-870_Angstrom_Exponent",
    )

    KEEP = [
        "AERONET_Site",
        "Date(dd:mm:yyyy)",
        "Time(hh:mm:ss)",
        "Day_of_Year",
        "Data_Quality_Level",
        "AERONET_Site_Name",
        "Site_Latitude(Degrees)",
        "Site_Longitude(Degrees)",
        "Site_Elevation(m)",
    ] + list(FIELDS.values())

    start_yr = start_date.year
    end_yr = end_date.year

    data = pl.DataFrame()
    for file in raw_data_path.glob("*.csv"):
        if file.stem == str(start_yr) or file.stem == str(end_yr):
            read_data = pl.read_csv(file, skip_lines=5, has_header=True, null_values=[" ","","-"])
            data = pl.concat([data, read_data])

    #Removes rows with any NULL data
    new_data = data[KEEP].drop_nulls()
    logger.info(f"Removed {len(data) - len(new_data)} rows due to them containing nulls")

    # Creates values for AOD 550
    new_data = new_data.with_columns(
        (
            pl.when(
                pl.col(FIELDS["aod500"]) == FLAG
            ).then(
                pl.lit(np.nan)
            ).otherwise(
                convert(
                    pl.col(FIELDS["aod500"]),
                    pl.col(FIELDS["lambda500"]),
                    pl.col(FIELDS["alpha"]),
                )

            )
        ).alias("AOD_550nm")
    )

    #Adds extra needed columns
    new_data = new_data.with_columns(pl.lit("AOD_550nm").alias("variable_name"))
    new_data = new_data.with_columns(pl.lit("1").alias("units"))

    # Create correct Datetime column
    new_data = new_data.with_columns(
        (pl.col("Date(dd:mm:yyyy)") + " " + pl.col("Time(hh:mm:ss)"))
        .str.to_datetime("%d:%m:%Y %H:%M:%S")
        .alias("Datetime")
    )

    # Filters on dates
    new_data = new_data.filter(pl.col("Datetime").is_between(start_date, end_date))

    #Removes unwanted stations
    logger.info(f"Before removing DRAGON {len(new_data)}")
    new_data = new_data.remove(pl.col("AERONET_Site").str.contains("DRAGON"))
    logger.info(f"After removing DRAGON {len(new_data)}")

    # Saves file
    new_data.write_csv(opath, include_header=False)
    logger.info(f"Wrote processed aeronet file to {opath}")
    