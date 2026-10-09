import dataclasses
import logging

import numpy as np
from pyaro.timeseries import Data, DataStationIdStructured, Reader

from pyaerocom.units.constants import M_N, M_O, M_S
from pyaerocom.units.units_helpers import get_unit_conversion_fac

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

    # number of rows processed at once when building keys, limits temporary memory
    _CHUNK = 10_000_000
    # key of rows at locations not present in both datasets, sorted to the end
    _NO_KEY = np.uint64(np.iinfo(np.uint64).max)

    @staticmethod
    def _slice_rows(d: Data, rows: np.ndarray) -> tuple[Data, np.ndarray]:
        """Slice d at the given row positions using a boolean mask (Data.slice only
        supports masks). Returns the sliced data and the index into it for each of rows."""
        mask = np.zeros(len(d), dtype=bool)
        mask[rows] = True
        # the mask-slice is in row order; map each requested row to its position there
        return d.slice(mask), np.searchsorted(np.flatnonzero(mask), rows)

    @classmethod
    def _station_locations(cls, d: Data) -> tuple[np.ndarray, np.ndarray]:
        """Unique station ids of d and their lat/lon (as lat + 1j*lon) from their first row"""
        ids, first = np.unique(d.station_ids, return_index=True)
        first_data, pos = cls._slice_rows(d, first)
        coords = (
            np.asarray(first_data.latitudes, dtype=np.float64)[pos]
            + 1j * np.asarray(first_data.longitudes, dtype=np.float64)[pos]
        )
        return ids, coords

    @staticmethod
    def _loc_lookup(ids: np.ndarray, locs: np.ndarray):
        """Function mapping station ids to location codes (-1 for unknown/not shared)"""
        if len(ids) > 0 and ids[0] >= 0 and ids[-1] < 4 * len(ids) + 1_000_000:
            table = np.full(int(ids[-1]) + 1, -1, dtype=np.int64)
            table[ids] = locs
            return lambda station_ids: table[station_ids]
        return lambda station_ids: locs[np.searchsorted(ids, station_ids)]

    @classmethod
    def _int_times(cls, d: Data, time_dtype):
        """Iterate over chunks of d, yielding (slice, start as int64, duration as int64)"""
        start_times, end_times = d.start_times, d.end_times
        for i in range(0, len(d), cls._CHUNK):
            sl = slice(i, i + cls._CHUNK)
            start = start_times[sl].astype(time_dtype).astype(np.int64)
            dur = end_times[sl].astype(time_dtype).astype(np.int64) - start
            yield sl, start, dur

    @classmethod
    def _sorted_unique_keys(
        cls, d: Data, loc_lookup, time_dtype, tmin: int, dmin: int, durations, shifts
    ) -> tuple[np.ndarray, np.ndarray]:
        """Sorted unique uint64 keys (location|start|duration) of the rows at shared locations,
        and the row-index of the first occurrence of each key"""
        loc_shift, dur_bits = shifts
        n = len(d)
        station_ids = d.station_ids
        key = np.empty(n, dtype=np.uint64)
        for sl, start, dur in cls._int_times(d, time_dtype):
            dur = dur - dmin if durations is None else np.searchsorted(durations, dur)
            loc = loc_lookup(station_ids[sl])
            k = loc.astype(np.uint64) << np.uint64(loc_shift)
            k |= (start - tmin).astype(np.uint64) << np.uint64(dur_bits)
            k |= dur.astype(np.uint64)
            k[loc < 0] = cls._NO_KEY
            key[sl] = k
        # stable sort, so the first occurrence of a key comes first
        order = np.argsort(key, kind="stable")
        order = order.astype(np.uint32 if n <= np.iinfo(np.uint32).max else np.int64)
        key = key[order]
        n_valid = np.searchsorted(key, cls._NO_KEY)
        key, order = key[:n_valid], order[:n_valid]
        first = np.ones(n_valid, dtype=bool)
        np.not_equal(key[1:], key[:-1], out=first[1:])
        return key[first], order[first]

    @classmethod
    def _combine_add(
        cls, varname: str, units: str, data: list[Data], scalings: list[float]
    ) -> DataStationIdStructured:
        """Add two datasets, matching rows by location (lat/lon) and start/end time.

        Station ids are dataset-specific, so stations are matched by their lat/lon.
        All stations sharing a lat/lon are merged into one location; for duplicate
        (location, start_time, end_time) rows only the first occurrence is used.
        Altitude and station name are taken from the first matching row of data[0].
        """
        new_data = DataStationIdStructured(varname, units=units)
        if len(data[0]) == 0 or len(data[1]) == 0:
            return new_data

        logger.info("Finding shared locations (lat/lon) for the data")
        station_locs = [cls._station_locations(d) for d in data]
        nstations0 = len(station_locs[0][0])
        locations, station_loc = np.unique(
            np.concatenate([c for _, c in station_locs]), return_inverse=True
        )
        station_loc = station_loc.reshape(-1)  # numpy 2.0.0 returns input shape
        station_loc = [station_loc[:nstations0], station_loc[nstations0:]]
        shared = np.intersect1d(*station_loc)
        loc_lookups = []
        for (ids, _), locs in zip(station_locs, station_loc):
            locs = np.where(np.isin(locs, shared), locs, -1)
            loc_lookups.append(cls._loc_lookup(ids, locs))
        logger.info("Found %d shared locations", len(shared))
        if len(shared) == 0:
            return new_data

        # value ranges of times and durations, to pack them into a uint64 key
        # times are matched with a resolution of seconds
        time_dtype = np.dtype("datetime64[s]")
        tmin = min(int(d.start_times.min().astype(time_dtype).astype(np.int64)) for d in data)
        tmax = max(int(d.start_times.max().astype(time_dtype).astype(np.int64)) for d in data)
        dmin, dmax = np.iinfo(np.int64).max, np.iinfo(np.int64).min
        for d in data:
            for _, _, dur in cls._int_times(d, time_dtype):
                dmin, dmax = min(dmin, int(dur.min())), max(dmax, int(dur.max()))
        loc_bits = max(1, (len(locations) - 1).bit_length())
        start_bits = max(1, (tmax - tmin).bit_length())
        dur_bits = max(1, (dmax - dmin).bit_length())
        durations = None
        if loc_bits + start_bits + dur_bits > 63:
            # encode durations by their index in all unique durations
            durations = np.empty(0, dtype=np.int64)
            for d in data:
                for _, _, dur in cls._int_times(d, time_dtype):
                    durations = np.union1d(durations, dur)
            dur_bits = max(1, (len(durations) - 1).bit_length())
        if loc_bits + start_bits + dur_bits > 63:
            raise PostProcessingReaderException(
                f"Cannot combine {varname}: too many locations ({len(locations)}, "
                f"{loc_bits} bits), too long time-range ({tmax - tmin} s, {start_bits} bits) "
                f"or too many durations ({dur_bits} bits)"
            )
        shifts = (start_bits + dur_bits, dur_bits)

        keys = []
        for j, (d, lookup) in enumerate(zip(data, loc_lookups)):
            logger.info("Sorting %d timesteps of dataset %d", len(d), j)
            keys.append(
                cls._sorted_unique_keys(d, lookup, time_dtype, tmin, dmin, durations, shifts)
            )
        (keys0, rows0), (keys1, rows1) = keys
        del keys
        logger.info("Matching %d and %d unique timesteps", len(keys0), len(keys1))
        if len(keys0) == 0 or len(keys1) == 0:
            return new_data
        pos = np.searchsorted(keys0, keys1)
        pos[pos == len(keys0)] = 0
        match = np.flatnonzero(keys0[pos] == keys1)
        # keys1 is sorted, so lpos is sorted and the output is ordered by keys0
        lpos = pos[match]
        del pos
        lrows = rows0[lpos]
        rrows = rows1[match]
        out_loc = (keys0[lpos] >> np.uint64(shifts[0])).astype(np.int64)
        del keys0, rows0, keys1, rows1, lpos, match
        if len(lrows) == 0:
            return new_data

        new = np.empty(len(lrows), dtype=DataStationIdStructured._dtype)
        new["values"] = data[0].values[lrows] * scalings[0] + data[1].values[rrows] * scalings[1]
        new["standard_deviations"] = np.sqrt(
            np.square(data[0].standard_deviations[lrows] * scalings[0])
            + np.square(data[1].standard_deviations[rrows] * scalings[1])
        )
        new["flags"] = data[0].flags[lrows] | data[1].flags[rrows]
        new["start_times"] = data[0].start_times[lrows]
        new["end_times"] = data[0].end_times[lrows]
        del rrows

        # one station per location, described by its first (earliest) matching row
        loc_first = np.flatnonzero(np.concatenate(([True], out_loc[1:] != out_loc[:-1])))
        first_rows = lrows[loc_first]
        names = np.asarray(data[0].stations_by_ids(data[0].station_ids[first_rows]))
        # identical names share one station entry (first one wins), as in append()
        _, name_first, name_inverse = np.unique(names, return_index=True, return_inverse=True)
        name_order = np.argsort(name_first, kind="stable")
        name_station_id = np.empty(len(name_first), dtype=np.int64)
        name_station_id[name_order] = np.arange(len(name_first))
        loc_station_id = name_station_id[name_inverse.reshape(-1)]
        station_src = name_first[name_order]

        station_data = np.empty(len(station_src), dtype=DataStationIdStructured._dtype_station)
        station_data["stations"] = names[station_src]
        station_data["latitudes"] = locations[out_loc[loc_first[station_src]]].real
        station_data["longitudes"] = locations[out_loc[loc_first[station_src]]].imag
        alt_data, alt_pos = cls._slice_rows(data[0], first_rows[station_src])
        station_data["altitudes"] = np.asarray(alt_data.altitudes)[alt_pos]
        station_dict = {str(name): i for i, name in enumerate(station_data["stations"])}

        counts = np.diff(np.append(loc_first, len(lrows)))
        new["station_ids"] = np.repeat(loc_station_id, counts)
        new_data.set_data(varname, units, new, station_data, station_dict)
        return new_data

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

            if transform.OP != "ADD":
                raise PostProcessingReaderException(
                    f"Transform mode {transform.OP} is not supported"
                )
            new_data = self._combine_add(varname, transform.OUT_UNIT, data, scalings)
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
