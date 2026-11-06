import numpy as np
from pyaro.timeseries import DataStationIdStructured

from pyaerocom.io.pyaro.postprocess import PostProcessingReader

T0 = np.datetime64("2020-01-01T00:00:00", "s")
HOUR = np.timedelta64(1, "h")


class _DictReader:
    def __init__(self, data):
        self._data = data

    def variables(self):
        return list(self._data)

    def data(self, varname):
        return self._data[varname]


class _MaskSliceData(DataStationIdStructured):
    """Data which, like some pyaro readers, only allows slicing with boolean masks"""

    def slice(self, index):
        index = np.asarray(index)
        assert index.dtype == bool and len(index) == len(self), "slice requires a mask"
        return super().slice(index)


def _make(varname, rows):
    """rows: list of (station, lat, lon, alt, hour, value, flag)"""
    d = _MaskSliceData(varname, "nmol mol-1")
    for station, lat, lon, alt, hour, value, flag in rows:
        d.append(
            value=value,
            station=station,
            latitude=lat,
            longitude=lon,
            altitude=alt,
            start_time=T0 + hour * HOUR,
            end_time=T0 + (hour + 1) * HOUR,
            flag=flag,
            standard_deviation=1.0,
        )
    return d


def _combine(no2, o3):
    reader = PostProcessingReader(
        _DictReader({"vmrno2": no2, "vmro3": o3}), compute_vars=["vmrox_from_vmrno2_vmro3"]
    )
    return reader.data("vmrox")


def test_vmrox_combine_by_latlon_and_time():
    # station ids/names differ between datasets, matching is by lat/lon and time
    no2 = _make(
        "vmrno2",
        [
            ("A1", 10, 5, 100, 0, 1.0, 0),
            ("A1", 10, 5, 100, 1, 2.0, 0),
            ("A1", 10, 5, 100, 1, 9.0, 0),  # duplicate time, first is used
            ("A2", 20, 5, 200, 0, 3.0, 1),  # no match in o3
            ("A3", 30, 5, 300, 2, 4.0, 2),
        ],
    )
    o3 = _make(
        "vmro3",
        [
            ("B3", 30, 5, 0, 2, 40.0, 1),
            ("B1", 10, 5, 0, 1, 20.0, 0),
            ("B1", 10, 5, 0, 5, 50.0, 0),  # no match in no2
            ("B1", 10, 5, 0, 0, 10.0, 0),
        ],
    )
    out = _combine(no2, o3)
    assert out.units == "nmol mol-1"
    np.testing.assert_array_equal(out.values, [11.0, 22.0, 44.0])
    np.testing.assert_array_equal(out.stations, ["A1", "A1", "A3"])
    np.testing.assert_array_equal(out.latitudes, [10, 10, 30])
    np.testing.assert_array_equal(out.altitudes, [100, 100, 300])
    np.testing.assert_array_equal(out.start_times, T0 + np.array([0, 1, 2]) * HOUR)
    np.testing.assert_array_equal(out.flags, [0, 0, 3])
    np.testing.assert_allclose(out.standard_deviations, np.sqrt(2.0))


def test_vmrox_merges_stations_with_same_latlon():
    no2 = _make(
        "vmrno2",
        [
            ("A1", 10, 5, 100, 0, 1.0, 0),
            ("A1b", 10, 5, 100, 1, 2.0, 0),
            ("A1b", 10, 5, 100, 0, 7.0, 0),  # duplicate of A1 at hour 0, first is used
        ],
    )
    o3 = _make(
        "vmro3",
        [
            ("B1", 10, 5, 0, 0, 10.0, 0),
            ("B1b", 10, 5, 0, 1, 20.0, 0),
        ],
    )
    out = _combine(no2, o3)
    np.testing.assert_array_equal(out.values, [11.0, 22.0])
    np.testing.assert_array_equal(out.stations, ["A1", "A1"])


def test_vmrox_no_overlap():
    no2 = _make("vmrno2", [("A1", 10, 5, 100, 0, 1.0, 0)])
    o3 = _make("vmro3", [("B1", 11, 5, 0, 0, 10.0, 0)])
    out = _combine(no2, o3)
    assert len(out) == 0


def test_vmrox_station_order_differs_from_location_order():
    # A1 is added first, but A2 has the smaller latitude and comes first in the output
    no2 = _make(
        "vmrno2",
        [
            ("A1", 30, 5, 300, 0, 1.0, 0),
            ("A2", 10, 5, 100, 0, 2.0, 0),
        ],
    )
    o3 = _make(
        "vmro3",
        [
            ("B1", 30, 5, 0, 0, 10.0, 0),
            ("B2", 10, 5, 0, 0, 20.0, 0),
        ],
    )
    out = _combine(no2, o3)
    np.testing.assert_array_equal(out.stations, ["A2", "A1"])
    np.testing.assert_array_equal(out.latitudes, [10, 30])
    np.testing.assert_array_equal(out.altitudes, [100, 300])
    np.testing.assert_array_equal(out.values, [22.0, 11.0])


class _NsTimesData(_MaskSliceData):
    """Data returning start/end times as datetime64[ns], as some pyaro readers do"""

    @property
    def start_times(self):
        return super().start_times.astype("datetime64[ns]")

    @property
    def end_times(self):
        return super().end_times.astype("datetime64[ns]")


def test_vmrox_long_nanosecond_timeseries():
    # 15 years in ns need 59 bits, too many together with the location bits;
    # times are therefore matched with a resolution of seconds
    t0 = np.datetime64("2010-01-01T00:00:00", "ns")
    start = t0 + np.array([0, 1, 15 * 365 * 24], dtype="timedelta64[h]").astype("timedelta64[ns]")
    n = len(start)
    nstations = 100

    def make(varname, prefix, value):
        d = _NsTimesData(varname, "nmol mol-1")
        for i in range(nstations):  # one append per station, latitudes differ per station
            d.append(
                value=np.full(n, value, dtype=np.float32),
                station=np.full(n, f"{prefix}{i}"),
                latitude=np.full(n, i * 0.01, dtype=np.float32),
                longitude=np.zeros(n, dtype=np.float32),
                altitude=np.zeros(n, dtype=np.float32),
                start_time=start,
                end_time=start + np.timedelta64(1, "h"),
                flag=np.zeros(n, dtype=np.int16),
                standard_deviation=np.zeros(n, dtype=np.float32),
            )
        return d

    out = _combine(make("vmrno2", "A", 1.0), make("vmro3", "B", 2.0))
    assert len(out) == nstations * n
    assert len(np.unique(out.stations)) == nstations
    np.testing.assert_array_equal(out.values, 3.0)
    np.testing.assert_array_equal(
        out.start_times.astype("datetime64[ns]"), np.tile(start, nstations)
    )
