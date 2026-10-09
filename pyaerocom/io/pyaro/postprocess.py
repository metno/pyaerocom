import dataclasses
import logging

import numpy as np
from pyaro.timeseries import Data, DataStationIdStructured, Reader

from pyaerocom.units.constants import M_N, M_O, M_S
from pyaerocom.units.units_helpers import get_unit_conversion_fac
from pyaerocom.utils import NpArrayIndexer

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class VariableScaling:
    REQ_VAR: str
    IN_UNIT: str
    OUT_UNIT: str
    SCALING_FACTOR: float
    OUT_VARNAME: str
    NOTE: str | None = None

    def required_input_variables(self) -> list[str]:
        return [self.REQ_VAR]

    def out_varname(self) -> str:
        return self.OUT_VARNAME


@dataclasses.dataclass
class VariableCombiner:
    REQ_VARS: tuple[str, str]
    IN_UNITS: tuple[str, str]
    OUT_UNIT: str
    OUT_VARNAME: str
    OP: str

    def required_input_variables(self) -> list[str]:
        return self.REQ_VARS

    def out_varname(self) -> str:
        return self.OUT_VARNAME


TRANSFORMATIONS = {
    "proxyconcpm10dust_from_concpm10": VariableScaling(
        REQ_VAR="concpm10",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug m-3",
        SCALING_FACTOR=1,
        OUT_VARNAME="proxyconcpm10dust",
    ),
    "proxyconcpm10wf_from_concpm10": VariableScaling(
        REQ_VAR="concpm10",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug m-3",
        SCALING_FACTOR=1,
        OUT_VARNAME="proxyconcpm10wf",
    ),
    "proxyconcpm10ss_from_concpm10": VariableScaling(
        REQ_VAR="concpm10",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug m-3",
        SCALING_FACTOR=1,
        OUT_VARNAME="proxyconcpm10ss",
    ),
    "concNno_from_concno": VariableScaling(
        REQ_VAR="concno",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug N m-3",
        SCALING_FACTOR=M_N / (M_N + M_O),
        OUT_VARNAME="concNno",
    ),
    "concNno2_from_concno2": VariableScaling(
        REQ_VAR="concno2",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug N m-3",
        SCALING_FACTOR=M_N / (M_N + 2 * M_O),
        OUT_VARNAME="concNno2",
    ),
    "concSso2_from_concso2": VariableScaling(
        REQ_VAR="concso2",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug S m-3",
        SCALING_FACTOR=M_S / (M_S + 2 * M_O),
        OUT_VARNAME="concSso2",
    ),
    # I think they should be scaled with just 1, since M_C/M_C = 1(?). This is how it is done for EMEP reader
    "concCecpm10_from_concecpm10": VariableScaling(
        REQ_VAR="concecpm10",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug C m-3",
        SCALING_FACTOR=1,
        OUT_VARNAME="concCecpm10",
    ),
    "concCocpm10_from_concocpm10": VariableScaling(
        REQ_VAR="concocpm10",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug C m-3",
        SCALING_FACTOR=1,
        OUT_VARNAME="concCocpm10",
    ),
    "concCecpm25_from_concecpm25": VariableScaling(
        REQ_VAR="concecpm25",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug C m-3",
        SCALING_FACTOR=1,
        OUT_VARNAME="concCecpm25",
    ),
    "concCocpm25_from_concocpm25": VariableScaling(
        REQ_VAR="concocpm25",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug C m-3",
        SCALING_FACTOR=1,
        OUT_VARNAME="concCocpm25",
    ),
    "concCec_from_concec": VariableScaling(
        REQ_VAR="concec",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug C m-3",
        SCALING_FACTOR=1,
        OUT_VARNAME="concCec",
    ),
    "concCoc_from_concoc": VariableScaling(
        REQ_VAR="concoc",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug C m-3",
        SCALING_FACTOR=1,
        OUT_VARNAME="concCoc",
    ),
    "vmro3_from_conco3": VariableScaling(
        REQ_VAR="conco3",
        IN_UNIT="µg m-3",
        OUT_UNIT="ppb",
        SCALING_FACTOR=0.5011,  # 20C and 1013 hPa
        OUT_VARNAME="vmro3",
        NOTE="The vmro3_from_conco3 transform is only valid at T=20C, p=1013hPa",
    ),
    "vmro3max_from_conco3": VariableScaling(  # Requires `resample_how`
        REQ_VAR="conco3",
        IN_UNIT="µg m-3",
        OUT_UNIT="ppb",
        SCALING_FACTOR=0.5011,  # 20C and 1013 hPa
        OUT_VARNAME="vmro3max",
        NOTE="The vmro3max_from_conco3 transform is only valid at T=20C, p=1013hPa, and the transform requires the use of resample_how to obtain the daily maximum",
    ),
    "vmrno2_from_concno2": VariableScaling(
        REQ_VAR="concno2",
        IN_UNIT="ug m-3",
        OUT_UNIT="ppb",
        SCALING_FACTOR=0.5229,  # 20C and 1013 hPa
        OUT_VARNAME="vmrno2",
        NOTE="The vmrno2_from_concno2 transform is only valid at T=20C, p=1013hPa",
    ),
    "vmrso2_from_concso2": VariableScaling(
        REQ_VAR="concso2",
        IN_UNIT="ug m-3",
        OUT_UNIT="ppb",
        SCALING_FACTOR=0.3758,  # 20C and 1013 hPa
        OUT_VARNAME="vmrso2",
        NOTE="The vmrso2_from_concso2 transform is only valid at T=20C, p=1013hPa",
    ),
    "vmrco_from_concco": VariableScaling(
        REQ_VAR="concco",
        IN_UNIT="ug m-3",
        OUT_UNIT="ppb",
        SCALING_FACTOR=0.8589,  # 20C and 1013 hPa
        OUT_VARNAME="vmrco",
        NOTE="The vmrco_from_concco transform is only valid at T=20C, p=1013hPa",
    ),
    "vmrox_from_vmrno2_vmro3": VariableCombiner(
        REQ_VARS=("vmrno2", "vmro3"),
        IN_UNITS=("nmol mol-1", "nmol mol-1"),
        OUT_UNIT="nmol mol-1",
        OUT_VARNAME="vmrox",
        OP="ADD",
    ),
}


class ScalingReaderData(Data):
    def __init__(self, data: Data, variable: str, units: str, scaling: float | None):
        self._data = data
        self._variable = variable
        self._units = units
        self._scaling = scaling

    def slice(self, index):
        return ScalingReaderData(
            self._data.slice(index),
            variable=self._variable,
            units=self._units,
            scaling=self._scaling,
        )

    @property
    def variable(self) -> str:
        return self._variable

    @property
    def units(self) -> str:
        return self._units

    @property
    def values(self):
        if self._scaling is None:
            return self._data.values
        else:
            return self._data.values * self._scaling

    @property
    def standard_deviations(self):
        if self._scaling is None:
            return self._data.standard_deviations
        else:
            return self._data.standard_deviations * self._scaling

    # below functions implement all abstract methods from Wrapped _dataqq
    def __len__(self):
        return len(self._data)

    def stations_by_ids(self, ids):
        return self._data.stations_by_ids(ids)

    @property
    def stations(self):
        return self._data.stations

    @property
    def station_ids(self):
        return self._data.station_ids

    @property
    def altitudes(self):
        return self._data.altitudes

    @property
    def latitudes(self):
        return self._data.latitudes

    @property
    def longitudes(self):
        return self._data.longitudes

    @property
    def start_times(self):
        return self._data.start_times

    @property
    def end_times(self):
        return self._data.end_times

    @property
    def flags(self):
        return self._data.flags


class PostProcessingReaderException(Exception):
    pass


class PostProcessingReader(Reader):
    def __init__(
        self,
        reader: Reader,
        compute_vars: list[str] | None = None,
    ):
        self.reader = reader

        self.compute_vars = dict()
        if compute_vars is not None:
            known_variables = reader.variables()
            for compute_var in compute_vars:
                transform = TRANSFORMATIONS.get(compute_var)
                if transform is None:
                    raise PostProcessingReaderException(
                        f"Unknown transformation ({compute_var}) encountered"
                    )
                required_input = transform.required_input_variables()
                missing = set(required_input) - set(known_variables)
                if len(missing) > 0:
                    raise PostProcessingReaderException(
                        f"The transformation {compute_var} requires variables which are not present, missing {missing}"
                    )
                known_variables.append(transform.out_varname())
                self.compute_vars[transform.out_varname()] = transform

    def metadata(self) -> dict[str, str]:
        return self.reader.metadata()

    @staticmethod
    def _as_lat_lon_pairs(latitudes: np.ndarray, longitudes: np.ndarray):
        """Return unique lat/lon pairs and their indices"""
        pairs = np.empty(
            latitudes.shape[0], dtype=[("lat", latitudes.dtype), ("lon", longitudes.dtype)]
        )
        pairs["lat"], pairs["lon"] = latitudes, longitudes
        return pairs

    def data(self, varname: str) -> Data:
        if varname not in self.compute_vars:
            data = self.reader.data(varname)
            return data
        transform = self.compute_vars[varname]
        if isinstance(transform, VariableScaling):
            data = self.reader.data(transform.REQ_VAR)
            scaling = transform.SCALING_FACTOR * get_unit_conversion_fac(
                from_unit=data.units,
                to_unit=transform.IN_UNIT,
                var_name=transform.REQ_VAR,
            )
            return ScalingReaderData(
                data, variable=varname, units=transform.OUT_UNIT, scaling=scaling
            )
        if isinstance(transform, VariableCombiner):
            logger.info(f"Combining variables {transform.REQ_VARS} into {varname}")
            data = []
            scalings = []
            for i, var in enumerate(transform.REQ_VARS):
                logger.info(f"Reading data for variable {var}")
                d = self.data(var)
                data.append(d)
                scalings.append(
                    get_unit_conversion_fac(from_unit=d.units, to_unit=transform.IN_UNITS[i])
                )

            logger.info("Finding unique shared lat/lon / stations pairs for the data")
            # Find unique shared data based on lat/lon
            latlons = [self._as_lat_lon_pairs(d.latitudes, d.longitudes) for d in data]
            uniq_idx = [np.unique(ll, return_index=True)[1] for ll in latlons]

            # Find shared lat/lon pairs between the first two datasets
            sharedll, shared_idx_0, shared_idx_1 = np.intersect1d(
                latlons[0][uniq_idx[0]], latlons[1][uniq_idx[1]], return_indices=True
            )

            # get station_ids for the shared lat/lon pairs
            station_id = [
                data[0].station_ids[uniq_idx[0]][shared_idx_0],
                data[1].station_ids[uniq_idx[1]][shared_idx_1],
            ]
            # index the station_ids so we can quickly find all values belonging to a station
            logger.info(
                "Indexing station IDs for quick lookup, number of points: %d %d",
                len(data[0]),
                len(data[1]),
            )
            station_indexers = [NpArrayIndexer(np.ascontiguousarray(d.station_ids)) for d in data]

            new_data = DataStationIdStructured(varname, units=transform.OUT_UNIT)

            for i, latlon in enumerate(sharedll):  # Per station
                lat, lon = latlon
                if i % 100 == 0:
                    logger.info("Processing station %d of %d", i, len(sharedll))
                data_subset = []
                first = []
                for j, si in enumerate(station_indexers):
                    indices = si.get_indices(station_id[j][i])
                    first.append(indices[0])
                    mask = np.zeros(len(data[j]), dtype=bool)
                    mask[indices] = True
                    data_subset.append(data[j][mask])

                start_times = [d.start_times for d in data_subset]
                end_times = [d.end_times for d in data_subset]
                # build a combined structured array of start/end times[0]
                start_end_dtype = np.dtype(
                    [("start_time", start_times[0].dtype), ("end_time", end_times[0].dtype)]
                )
                start_end = [np.empty(len(s), dtype=start_end_dtype) for s in start_times]
                for k, se in enumerate(start_times):
                    start_end[k]["start_time"] = se
                    start_end[k]["end_time"] = end_times[k]

                _, lindex, rindex = np.intersect1d(start_end[0], start_end[1], return_indices=True)

                # no check of station-altitude changes here, we assume it is constant
                new_latitudes = np.full(len(lindex), fill_value=lat, dtype=np.float64)
                new_longitudes = np.full(len(lindex), fill_value=lon, dtype=np.float64)
                if lindex.size > 0:
                    new_altitudes = np.full(
                        len(lindex), fill_value=data_subset[0].altitudes[lindex[0]], dtype=np.int16
                    )
                    station_name = data[0].stations_by_ids(station_id[0][i])
                else:
                    new_altitudes = np.array([], dtype=np.int16)
                    station_name = np.array([], dtype="<U64")
                new_stations = np.full(
                    len(lindex), fill_value=station_name, dtype=station_name.dtype
                )

                new_starttimes = start_times[0][lindex]
                new_endtimes = end_times[0][lindex]

                if transform.OP == "ADD":
                    new_values = (
                        data_subset[0].values[lindex] * scalings[0]
                        + data_subset[1].values[rindex] * scalings[1]
                    )
                    new_stdev = np.sqrt(
                        np.square(data_subset[0].standard_deviations[lindex] * scalings[0])
                        + np.square(data_subset[1].standard_deviations[rindex] * scalings[1])
                    )
                    flags = data_subset[0].flags[lindex] | data_subset[1].flags[rindex]
                else:
                    raise PostProcessingReaderException(
                        f"Transform mode {transform.OP} is not supported"
                    )

                new_data.append(
                    station=new_stations,
                    latitude=new_latitudes,
                    longitude=new_longitudes,
                    start_time=new_starttimes,
                    end_time=new_endtimes,
                    altitude=new_altitudes,
                    value=new_values,
                    standard_deviation=new_stdev,
                    flag=flags,
                )
                if len(new_stations) > 0:
                    logger.debug(
                        f"Processed station {new_stations[0]} ({len(new_stations)} values of {varname})"
                    )
            logger.info(f"Finished combining variables {transform.REQ_VARS} into {varname}")
            return new_data
        else:
            raise PostProcessingReaderException(
                f"Unknown transform {transform} encountered for variable {varname}"
            )

    def variables(self) -> list[str]:
        variables = list()
        variables.extend(self.reader.variables())
        variables.extend(self.compute_vars.keys())
        return variables

    def stations(self):
        return self.reader.stations()

    def close(self) -> None:
        self.reader.close()
