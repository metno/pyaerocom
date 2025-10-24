from __future__ import annotations

import logging
from collections.abc import Iterator
from datetime import date, datetime
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
from geonum.atmosphere import T0_STD, p0  # , temperature, pressure
from tqdm import tqdm

from pyaerocom.aux_var_helpers import mmrx_to_concx
from pyaerocom.griddeddata import GriddedData
from pyaerocom.io.gridded_reader import GriddedReader
from pyaerocom.units.molecular_mass import get_mmr_to_vmr_fac, get_molmass

MODEL_LVL137_IN_METERS = 10

# array of geometric altitudes (in [m]) corresponding to levels 64 - 137, taken from this table https://confluence.ecmwf.int/display/UDOC/L137+model+level+definitions
ALTITUDES_64_137 = np.array(
    [
        15003.50,
        14680.44,
        14360.05,
        14042.30,
        13727.18,
        13414.65,
        13104.70,
        12797.30,
        12492.44,
        12190.10,
        11890.24,
        11592.86,
        11297.93,
        11005.69,
        10714.22,
        10422.64,
        10130.98,
        9839.26,
        9547.49,
        9255.70,
        8963.90,
        8672.11,
        8380.36,
        8088.67,
        7797.04,
        7505.51,
        7214.09,
        6922.80,
        6631.66,
        6340.68,
        6049.89,
        5759.30,
        5469.30,
        5180.98,
        4896.02,
        4615.92,
        4341.73,
        4074.41,
        3814.82,
        3563.69,
        3321.67,
        3089.25,
        2866.83,
        2654.69,
        2452.99,
        2261.80,
        2081.09,
        1910.76,
        1750.63,
        1600.44,
        1459.91,
        1328.70,
        1206.44,
        1092.73,
        987.15,
        889.29,
        798.72,
        715.02,
        637.76,
        566.54,
        500.95,
        440.61,
        385.16,
        334.24,
        287.52,
        244.69,
        205.44,
        169.51,
        136.62,
        106.54,
        79.04,
        53.92,
        30.96,
        10.00,
    ]
)


AEROCOM_NAMES = dict(
    no2="concno2",
    go3="conco3",
    aod550="od550aer",
    aerext1064="ec1064aer",
    pm10="concpm10",
    pm2p5="concpm25",
    ch4_c="vmrch4",
    co="vmrco",
)

KEEP_FIELDS = [
    "longitude",
    "latitude",
    "time",
    "pm10",
    "pm2p5",
    "aod550",
    "aerext1064",
    "no2",
    "go3",
    "ch4_c",
    "co",
    "level",
]

FULL_NAMES = dict(
    no2="Nitrogen Dioxide",
    go3="Ozone",
    ch4_c="Methane",
    co="Carbon Monoxide",
    aod550="AOD 550nm",
    aerext1064="Aerosol extinction coefficient 1064nm",
    pm10="PM10 Aerosol",
    pm2p5="PM2.5 Aerosol",
)

CONVERT_UNITS = {
    "no2": {
        "molmass": get_molmass("no2"),
        "fromunit": "kg kg**-1",
    },
    "go3": {
        "molmass": get_molmass("o3"),
        "fromunit": "kg kg**-1",
    },
}

TO_VMR = {
    "ch4_c": {"factor": get_mmr_to_vmr_fac("ch4") * 1e9},
    "co": {"factor": get_mmr_to_vmr_fac("co") * 1e9},
}

UNITS = dict(
    no2="kg m**-3",
    go3="kg m**-3",
    aod550=1,
    aerext1064="m**-1",
    pm10="kg m**-3",
    pm2p5="kg m**-3",
    ch4_c="ppb",
    co="ppb",
)

FILE_NAME = dict(
    no2="cIFS-00UTC_o-suite_lev137.nc",
    go3="cIFS-00UTC_o-suite_lev137.nc",
    aod550="cIFS-00UTC_o-suite_surface.nc",
    aerext1064="cIFS-00UTC_o-suite_multilev.nc",
    pm10="cIFS-00UTC_o-suite_surface.nc",
    pm2p5="cIFS-00UTC_o-suite_surface.nc",
    ch4_c="cIFS-00UTC_o-suite_lev137.nc",
    co="cIFS-00UTC_o-suite_lev137.nc",
)

STANDARD_NAMES = dict(
    no2="mass_fraction_of_nitrogen_dioxide_in_air",
    go3="mass_fraction_of_ozone_in_air",
    aod550="atmosphere_optical_thickness_due_to_ambient_aerosol_particles",
    aerext1064="volume_extinction_coefficient_in_air_due_to_ambient_aerosol_particles",
    pm10="mass_concentration_of_pm10_ambient_aerosol_in_air",
    pm2p5="mass_concentration_of_pm2p5_ambient_aerosol_in_air",
    ch4_c="mass_fraction_of_methane_in_air",
    co="mass_fraction_of_carbon_monoxide_in_air",
)


DATA_FOLDER_PATH = Path("/lustre/storeB/project/fou/kl/CAMS2_82/cifs-models/o-suite/")


DEBUG = True


logger = logging.getLogger(__name__)


def fix_names(ds: xr.Dataset) -> xr.Dataset:
    ds = ds[KEEP_FIELDS]
    ds["longitude"].attrs.update(
        long_name="longitude", standard_name="longitude", units="degrees_east"
    )
    ds["latitude"].attrs.update(
        long_name="latitude", standard_name="latitude", units="degrees_north"
    )
    ds["time"].attrs.update(standard_name="time")
    if "level" in ds.coords:
        ds = ds.rename({"level": "altitude"})
        ds = ds.assign_coords(altitude=ALTITUDES_64_137)  # / 1000.0)
        ds["altitude"] = ds["altitude"].assign_attrs(units="m")  # "km")

    for var_name, aerocom_name in AEROCOM_NAMES.items():
        ds[var_name].attrs.update(long_name=aerocom_name)
        ds[var_name].attrs.update(standard_name=STANDARD_NAMES[var_name])
        ds[var_name].attrs.update(units=UNITS[var_name])
    return ds.rename(AEROCOM_NAMES)


def convert_units(ds: xr.Dataset) -> xr.Dataset:
    for var_name, attrs in CONVERT_UNITS.items():
        data = ds[var_name].data

        ds[var_name].data = mmrx_to_concx(
            data,
            p_pascal=p0,  # pressure(MODEL_LVL137_IN_METERS),
            T_kelvin=T0_STD,  # temperature(MODEL_LVL137_IN_METERS),
            mmr_unit=attrs["fromunit"],
            to_unit=UNITS[var_name],
        )

    for var_name, attrs in TO_VMR.items():
        data = ds[var_name].data
        ds[var_name].data = data * attrs["factor"]

    return ds


def drop_vars(ds: xr.Dataset) -> xr.Dataset:
    """
    Drop variables not used in the evaluation
    """
    ds = ds.drop_vars([var for var in ds.data_vars if var not in KEEP_FIELDS])
    return ds


def fix_missing_vars(ds: xr.Dataset) -> xr.Dataset:
    """
    TODO: Check if all variables are there. If not:
    make the rest of the variables, filled with nans.
    Log an error when this is done

    Might not be possible...
    """
    vars_list = [i for i in ds.data_vars]
    nb_vars = len(vars_list)
    if nb_vars < 6:
        logger.warning(f"Found only {vars_list}. Filling the rest with NaNs")

        dummy_var = ds[vars_list[0]]
        dummy_var_name = vars_list[0]
        for species in AEROCOM_NAMES:
            if species not in vars_list:
                ds = ds.assign(**{species: dummy_var * np.nan})
                attrs = ds[dummy_var_name].attrs
                attrs["species"] = FULL_NAMES[species]
                attrs["standard_name"] = STANDARD_NAMES[species]
                ds[species] = ds[species].assign_attrs(attrs)
    return ds


def only_first_day(ds: xr.Dataset) -> xr.Dataset:
    first_day = ds.time[0].dt.day
    return ds.sel(time=ds.time.dt.day == first_day)


def read_dataset(paths: list[Path]) -> xr.Dataset:
    paths = check_files(paths)

    def preprocess(ds: xr.Dataset) -> xr.Dataset:
        return ds.pipe(only_first_day).pipe(drop_vars)

    ds = xr.open_mfdataset(
        paths, preprocess=preprocess, parallel=False, chunks={"level": 10, "time": 1}
    )
    return ds.pipe(fix_missing_vars).pipe(convert_units).pipe(fix_names)


def check_files(paths: list[Path]) -> list[Path]:
    if not DEBUG:
        return paths

    new_paths: list[Path] = []

    for p in tqdm(paths, disable=None):
        try:
            with xr.open_dataset(p, decode_timedelta=True) as ds:
                if len(ds.time.data) < 2:
                    logger.warning(f"Too few timestamps in {p}. Skipping file")
                    continue
                if len(set(np.array(ds.time))) != len(np.array(ds.time)):
                    logger.warning(
                        f"Ambiguous time dimension: Duplicate timestamps in {p}. Skipping file"
                    )
                    continue

            new_paths.append(p)
        except Exception as ex:
            logger.warning(f"Error when opening {p}: {ex}. Skipping file")

    return new_paths


def model_paths(
    species: str,
    *dates: datetime | date | str,
    root_path: Path | str = DATA_FOLDER_PATH,
) -> Iterator[Path]:
    for date in dates:  # noqa: F402
        date_str = date.strftime("%Y%m%d")
        paths = list(root_path.glob(f"**/{date_str}_{FILE_NAME[species]}"))
        if len(paths) > 1:
            logger.warning(f"Found more then one file for {date_str}_{FILE_NAME[species]}")
            continue
        path = list(paths)[0]
        if not path.is_file():
            logger.warning(f"Could not find {path.name}. Skipping {date}")
            continue
        yield path


def parse_daterange(
    dates: pd.DatetimeIndex | list[datetime] | tuple[datetime, datetime],
) -> pd.DatetimeIndex:
    if isinstance(dates, pd.DatetimeIndex):
        return dates
    if len(dates) != 2:
        raise ValueError("need 2 datetime objects to define a date_range")
    return pd.date_range(*dates, freq="d")


class ReadCAMS2_82(GriddedReader):
    FREQ_CODES = {"hour": "hourly", "3hour": "3hourly"}
    REVERSE_FREQ_CODES = {val: key for key, val in FREQ_CODES.items()}

    def __init__(
        self,
        data_id: str | None = None,
        data_dir: str | Path | None = None,
    ) -> None:
        self._filedata: xr.Dataset | None = None
        self._filepaths: list[Path] | None = None
        self._data_dir: Path | None = None

        self._data_id: str | None = None
        self._daterange: pd.DatetimeIndex | None = None

        if data_dir is not None:
            if isinstance(data_dir, str):
                data_dir = Path(data_dir)
            self.data_dir = data_dir

        if data_id is not None:
            self.data_id = data_id

    @property
    def data_dir(self) -> Path:
        """
        Directory containing netcdf files
        """
        if self._data_dir is None:
            raise AttributeError("data_dir needs to be set before accessing")
        return self._data_dir

    @data_dir.setter
    def data_dir(self, val: str | Path | None):
        if val is None:
            raise ValueError(f"Data dir {val} needs to be a dictionary or a file")
        if isinstance(val, str):
            val = Path(val)
        if not val.is_dir():
            raise NotADirectoryError(val)
        self._data_dir = val
        self._filedata = None

    @property
    def data_id(self):
        if self._data_id is None:
            raise AttributeError("data_id needs to be set before accessing")
        return self._data_id

    @data_id.setter
    def data_id(self, val):
        self._data_id = val

    @property
    def years_avail(self):
        return np.unique(
            self.daterange.values.astype("datetime64[Y]").astype("int") + 1970
        ).astype("str")

    @property
    def ts_types(self):
        return self.REVERSE_FREQ_CODES.keys()

    @property
    def vars_provided(self):
        return AEROCOM_NAMES.values()

    @property
    def filepaths(self) -> list[Path]:
        """
        Path to data file
        """
        if self.data_dir is None and self._filepaths is None:  # type:ignore[unreachable]
            raise AttributeError("data_dir or filepaths needs to be set before accessing")
        if self._filepaths is None:
            paths = []
            for species in FILE_NAME:
                try:
                    paths += list(
                        model_paths(
                            species,
                            *self.daterange,
                            root_path=self.data_dir,
                        )
                    )
                except (IndexError, Exception) as e:
                    logger.warning(f"Could not find any files for {species}, {e}")
                    continue
            if not paths:
                raise ValueError("No files found")
            paths = sorted(list(set(paths)))
            self._filepaths = paths
        return self._filepaths

    @filepaths.setter
    def filepaths(self, value: list[Path]):
        if not bool(list):
            raise ValueError("needs to be list of paths")
        if not isinstance(value, list):
            raise ValueError("needs to be list of paths")
        if all(isinstance(path, Path) for path in value):
            raise ValueError("needs to be list of paths")
        self._filepaths = value

    @property
    def filedata(self) -> xr.Dataset:
        """
        Loaded netcdf file (:class:`xarray.Dataset`)
        """
        if self._filedata is None:
            self._filedata = read_dataset(self.filepaths)
        return self._filedata

    @property
    def daterange(self) -> pd.DatetimeIndex:
        if self._daterange is None:
            raise ValueError("The date range is not set yet")
        return self._daterange

    @daterange.setter
    def daterange(self, dates: pd.DatetimeIndex | list[datetime] | tuple[datetime]):
        if not isinstance(dates, pd.DatetimeIndex | list | tuple):
            raise TypeError(f"{dates} need to be a pandas DatetimeIndex or 2 datetimes")

        self._daterange = parse_daterange(dates)
        self._filedata = None

    @staticmethod
    def has_var(var_name):
        """Check if variable is supported

        Parameters
        ----------
        var_name : str
            variable to be checked

        Returns
        -------
        bool
        """
        return var_name in AEROCOM_NAMES.values()

    def read_var(self, var_name: str, ts_type: str | None = None, **kwargs) -> GriddedData:
        """Load data for given variable.

        Parameters
        ----------
        var_name : str
            Variable to be read
        ts_type : str
            Temporal resolution of data to read. Supported are
            "hourly", "daily", "monthly" , "yearly".

        Returns
        -------
        GriddedData
        """
        if "daterange" in kwargs:
            self.daterange = kwargs["daterange"]
        if self._daterange is None:
            raise ValueError(f"No 'daterange' in kwargs={kwargs}")

        if ts_type != "3hourly" and ts_type != "hourly" and ts_type != "daily":
            raise ValueError(
                f"Only hourly or 3hourly or daily ts_type is supported, not {ts_type}"
            )

        filedata = self.filedata[var_name]

        if ts_type == "daily":
            filedata = filedata.resample(time="D").mean()

        cube = filedata.to_iris()
        cube = cube.intersection(longitude=(-180, 180))
        gridded = GriddedData(
            cube,
            var_name=var_name,
            ts_type=ts_type,
            check_unit=True,
            convert_unit_on_init=True,
        )
        gridded.metadata["data_id"] = self.data_id
        return gridded


if __name__ == "__main__":
    # from time import perf_counter

    data_dir = str(DATA_FOLDER_PATH)
    data_id = "CAMS2-82.EMEP.day0.AN"
    reader = ReadCAMS2_82(data_dir=data_dir, data_id=data_id)
    reader.daterange = ("2025-07-01", "2025-07-07")
    print(
        np.unique(reader.daterange.values.astype("datetime64[Y]").astype("int") + 1970).astype(
            "str"
        )
    )
    print(reader.filepaths)
    # data = reader.read_var("concpm25", "3hourly")
    # dates = ("2021-12-01", "2021-12-04")

    # seconds = -perf_counter()
    # print(reader.read_var("concno2", ts_type="hourly", daterange=dates))

    # seconds += perf_counter()
    # print(timedelta(seconds=int(seconds)))
