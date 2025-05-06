import numpy as np
import pytest

from pyaerocom.exceptions import TemporalResolutionError
from pyaerocom.units.datetime import TsType, sort_ts_types, get_lowest_resolution


def test_TsType_VALID():
    assert TsType.VALID == (
        "minutely",
        "hourly",
        "daily",
        "weekly",
        "monthly",
        "yearly",
        "native",
        "coarsest",
    )


def test_TsType_VALID_ITER():
    assert TsType.VALID_ITER == ("minutely", "hourly", "daily", "weekly", "monthly", "yearly")


def test_TsType_TOL_SECS_PERCENT():
    assert TsType.TOL_SECS_PERCENT == 5


def test_TsType_TSTR_TO_CF():
    assert TsType.TSTR_TO_CF == {"hourly": "hours", "daily": "days", "monthly": "days"}


def test_TsType_TS_MAX_VALS():
    assert TsType.TS_MAX_VALS == {
        "minutely": 360,
        "hourly": 168,  # up to weekly
        "daily": 180,  # up to 6 monthly
        "weekly": 104,  # up to ~2yearly
        "monthly": 120,
    }  # up to 10yearly


@pytest.mark.parametrize(
    "tst,mulfac",
    [
        (TsType("daily"), 10),
        (TsType("daily"), "10"),
        (TsType("daily"), 10.1),
    ],
)
def test_TsType_mulfac(tst: TsType, mulfac):
    tst.mulfac = mulfac
    assert tst.mulfac == tst._mulfac == int(mulfac)


@pytest.mark.parametrize(
    "tst,mulfac,error",
    [
        (TsType("daily"), "10.1", "mulfac needs to be int or convertible to int"),
        (TsType("daily"), 200, "Multiplication factor exceeds maximum allowed, which is 180"),
    ],
)
def test_TsType_mulfac_error(tst: TsType, mulfac, error: str):
    with pytest.raises(ValueError) as e:
        tst.mulfac = mulfac
    assert str(e.value) == error


def test_TsType_base():
    tst = TsType("daily")
    assert tst.base == tst._val == "daily"


def test_TsType_val():
    tst = TsType("daily")
    tst.val = value = "3daily"
    assert isinstance(tst.val, str)
    assert tst.val == value


@pytest.mark.parametrize(
    "value,error",
    [
        (
            "blaa",
            "Invalid input for ts_type blaa. "
            "Choose from ('minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'native', 'coarsest')",
        ),
        (
            "5000daily",
            "Invalid input for ts_type daily. "
            "Multiplication factor 5000 exceeds maximum allowed for daily, which is 180",
        ),
    ],
)
def test_TsType_val_error(value: str, error: str):
    with pytest.raises(TemporalResolutionError) as e:
        TsType("daily").val = value
    assert str(e.value) == error


def test_TsType_datetime64_str():
    assert TsType("daily").datetime64_str == "datetime64[1D]"


def test_TsType_timedelta64_str():
    assert TsType("daily").timedelta64_str == "timedelta64[1D]"


@pytest.mark.parametrize(
    "tst,unit",
    [
        pytest.param(TsType("hourly"), "hours", id="hourly"),
        pytest.param(TsType("daily"), "days", id="daily"),
        pytest.param(TsType("monthly"), "days", id="monthly"),
    ],
)
def test_TsType_cf_base_unit(tst: TsType, unit: str):
    assert tst.cf_base_unit == unit


@pytest.mark.parametrize(
    "tst,error",
    [
        (TsType("native"), "Cannot convert native to CF str"),
        (TsType("minutely"), "Cannot convert minutely to CF str"),
        (TsType("yearly"), "Cannot convert yearly to CF str"),
    ],
)
def test_TsType_cf_base_unit_error(tst: TsType, error: str):
    with pytest.raises(NotImplementedError) as e:
        tst.cf_base_unit
    assert str(e.value) == error


@pytest.mark.parametrize(
    "tst,seconds",
    [
        pytest.param(TsType("minutely"), 60, id="minutely"),
        pytest.param(TsType("3minutely"), 180, id="3minutely"),
        pytest.param(TsType("4minutely"), 240, id="4minutely"),
        pytest.param(TsType("daily"), 86400, id="daily"),
        pytest.param(TsType("weekly"), 86400 * 7, id="weekly"),
        pytest.param(
            TsType("monthly"), 2629743.831225, id="monthly"
        ),  # not sure how cf_units calculates that
    ],
)
def test_TsType_num_secs(tst: TsType, seconds: float):
    assert tst.num_secs == seconds


@pytest.mark.parametrize(
    "tst,seconds",
    [
        pytest.param(TsType("minutely"), 3, id="minutely"),
        pytest.param(TsType("3minutely"), 9, id="3minutely"),
        pytest.param(TsType("4minutely"), 12, id="4minutely"),
        pytest.param(TsType("daily"), 4320, id="daily"),
        pytest.param(TsType("weekly"), 30240, id="weekly"),
        pytest.param(TsType("monthly"), 131488, id="monthly"),
    ],
)
def test_TsType_tol_secs(tst: TsType, seconds: int):
    assert tst.tol_secs == seconds


@pytest.mark.parametrize(
    "tst,ref_time,time_str",
    [
        pytest.param(TsType("daily"), np.datetime64("2010-10-01", "D"), "2010-10-02", id="days"),
        pytest.param(TsType("2monthly"), np.datetime64("2010-10", "M"), "2010-12", id="months"),
        pytest.param(
            TsType("3hourly"),
            np.datetime64("2010-10-01T15:00:00", "h"),
            "2010-10-01T18",
            id="hours",
        ),
    ],
)
def test_TsType_to_timedelta64(tst: TsType, ref_time: np.datetime64, time_str: str):
    assert str(ref_time + tst.to_timedelta64()) == time_str


@pytest.mark.parametrize(
    "tst,value",
    [
        pytest.param(TsType("3minutely"), "minutely", id="3minutely"),
        pytest.param(TsType("hourly"), "minutely", id="hourly"),
        pytest.param(TsType("3hourly"), "hourly", id="3hourly"),
        pytest.param(TsType("weekly"), "daily", id="weekly"),
        pytest.param(TsType("monthly"), "weekly", id="monthly"),
        pytest.param(TsType("yearly"), "monthly", id="yearly"),
    ],
)
def test_TsType_next_higher(tst: TsType, value: str):
    assert tst.next_higher.val == value


def test_TsType_next_higher_error():
    with pytest.raises(IndexError) as e:
        TsType("minutely").next_higher.val
    assert str(e.value) == "No higher resolution available than minutely"


@pytest.mark.parametrize(
    "tst,value",
    [
        pytest.param(TsType("yearly"), "2yearly", id="yearly"),
        pytest.param(TsType("monthly"), "yearly", id="monthly"),
        pytest.param(TsType("3monthly"), "yearly", id="3monthly"),
        pytest.param(TsType("8daily"), "2weekly", id="8daily"),
        pytest.param(TsType("13monthly"), "2yearly", id="13monthly"),
        pytest.param(TsType("1000yearly"), "1001yearly", id="1000yearly"),
    ],
)
def test_TsType_next_lower(tst: TsType, value: str):
    assert tst.next_lower.val == value


def test_TsType_next_lower_error():
    with pytest.raises(TemporalResolutionError) as e:
        TsType("120monthly").next_lower.val
    assert str(e.value) == "Failed to determine next lower resolution for 120monthly"


@pytest.mark.parametrize(
    "ts_type,valid",
    [
        ("daily", True),
        ("60000daily", False),
        ("bla", False),
    ],
)
def test_TsType_valid(ts_type: str, valid: bool):
    assert TsType.valid(ts_type) == valid


@pytest.mark.parametrize(
    "tst,freq",
    [
        pytest.param(TsType("3hourly"), "3h", id="3hourly"),
        pytest.param(TsType("daily"), "1D", id="daily"),
    ],
)
def test_TsType_to_numpy_freq(tst: TsType, freq: str):
    assert tst.to_numpy_freq() == freq


def test_TsType_to_numpy_freq_error():
    with pytest.raises(TemporalResolutionError) as e:
        TsType("native").to_numpy_freq()
    assert str(e.value) == "numpy frequency not available for native"


@pytest.mark.parametrize(
    "tst,freq",
    [
        pytest.param(TsType("3hourly"), "3h", id="3hourly"),
        pytest.param(TsType("daily"), "D", id="daily"),
    ],
)
def test_TsType_to_pandas_freq(tst: TsType, freq: str):
    assert tst.to_pandas_freq() == freq


def test_TsType_to_pandas_freq_error():
    with pytest.raises(TemporalResolutionError) as e:
        TsType("native").to_pandas_freq()
    assert str(e.value) == "pandas frequency not available for native"


@pytest.mark.parametrize(
    "tst,unit",
    [
        pytest.param(TsType("hourly"), "h", id="hourly"),
        pytest.param(TsType("3hourly"), "(3h)", id="3hourly"),
        pytest.param(TsType("daily"), "d", id="daily"),
        pytest.param(TsType("minutely"), "min", id="minutely"),
        pytest.param(TsType("weekly"), "week", id="weekly"),
        pytest.param(TsType("monthly"), "month", id="monthly"),
        pytest.param(TsType("4weekly"), "(4week)", id="4weekly"),
    ],
)
def test_TsType_to_si(tst: TsType, unit: str):
    assert tst.to_si() == unit


def test_TsType_to_si_error():
    with pytest.raises(ValueError) as e:
        TsType("native").to_si()
    assert str(e.value) == "Cannot convert ts_type=native to SI unit string..."


@pytest.mark.parametrize(
    "from_tst,to_tst,min_num_obs,num",
    [
        (TsType("hourly"), TsType("hourly"), {}, 0),
        (TsType("12hourly"), TsType("6daily"), {"daily": {"hourly": 12}}, 6),
        (TsType("84hourly"), TsType("6daily"), {"daily": {"hourly": 24}}, 2),
        (TsType("84hourly"), TsType("6daily"), {"daily": {"hourly": 1}}, 0),
        (TsType("84hourly"), TsType("6daily"), {"daily": {"hourly": 12}}, 1),
        (TsType("84hourly"), TsType("4daily"), {"daily": {"84hourly": 0.1}}, 0),
        (TsType("84hourly"), TsType("6daily"), {"daily": {"84hourly": 0.1}}, 1),
        (TsType("2hourly"), TsType("3daily"), {"3daily": {"2hourly": 4}}, 4),
        (TsType("2hourly"), TsType("3daily"), {"3daily": {"hourly": 4}}, 2),
        (TsType("10hourly"), TsType("monthly"), {"monthly": {"hourly": 100}}, 10),
    ],
)
def test_TsType_get_min_num_obs(from_tst: TsType, to_tst: TsType, min_num_obs: dict, num: int):
    assert from_tst.get_min_num_obs(to_tst, min_num_obs) == num


@pytest.mark.parametrize(
    "from_tst,to_tst,exception,error",
    [
        (
            TsType("84hourly"),
            TsType("3daily"),
            TemporalResolutionError,
            "input ts_type 3daily is lower resolution than current 84hourly",
        ),
        (
            TsType("hourly"),
            TsType("minutely"),
            TemporalResolutionError,
            "input ts_type minutely is lower resolution than current hourly",
        ),
        (
            TsType("hourly"),
            TsType("daily"),
            ValueError,
            "could not infer min_num_obs value from input dict {} for conversion from hourly to daily",
        ),
    ],
)
def test_TsType_get_min_num_obs_error(from_tst: TsType, to_tst: TsType, exception, error: str):
    with pytest.raises(exception) as e:
        from_tst.get_min_num_obs(to_tst, {})
    assert str(e.value) == error


@pytest.mark.parametrize(
    "tst,seconds,check",
    [
        (TsType("hourly"), 3600, True),
        (TsType("hourly"), 3605, True),
        (TsType("20minutely"), 1200, True),
        (TsType("native"), 1200, False),
    ],
)
def test_TsType_check_match_total_seconds(tst: TsType, seconds: float, check: bool):
    assert tst.check_match_total_seconds(seconds) == check


@pytest.mark.parametrize(
    "base,seconds,ts_type",
    [
        ("daily", 86400 * 2, "2daily"),
        ("daily", 86400, "daily"),
        ("daily", 86000, "daily"),  # 5% tolerance
        ("yearly", 31556925, "yearly"),
    ],
)
def test_TsType__try_infer_from_total_seconds(base: str, seconds: float, ts_type: str):
    tst = TsType._try_infer_from_total_seconds(base, seconds)
    assert isinstance(tst, TsType)
    assert str(tst) == ts_type


def test_TsType__try_infer_from_total_seconds_error():
    base, seconds = "yearly", 31556925 * 2
    error = f"Period {seconds}s could not be associated with any allowed multiplication factor of base frequency {base}"
    with pytest.raises(TemporalResolutionError) as e:
        TsType._try_infer_from_total_seconds(base, seconds)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "seconds,value",
    [
        (86400 * 2, "2daily"),
        (3605, "hourly"),
        (1200, "20minutely"),
        (31556925 * 2, "24monthly"),
    ],
)
def test_TsType_from_total_seconds(seconds: str, value):
    tst = TsType.from_total_seconds(seconds)
    assert tst.val == value


@pytest.mark.parametrize("seconds", [(30), (31556925 * 12)])
def test_TsType_from_total_seconds_error(seconds: float):
    with pytest.raises(TemporalResolutionError) as e:
        TsType.from_total_seconds(seconds)
    assert str(e.value) == f"failed to infer ts_type based on input dt={seconds} s"


@pytest.mark.parametrize(
    "tst1,tst2,value",
    [
        ("daily", "daily", True),
        (TsType("daily"), "daily", True),
        ("daily", TsType("daily"), True),
        (TsType("daily"), TsType("monthly"), False),
        (TsType("3daily"), TsType("2daily"), False),
        (TsType("3daily"), TsType("daily"), False),
    ],
)
def test_TsType__eq__(tst1, tst2, value):
    assert (tst1 == tst2) == value


@pytest.mark.parametrize(
    "tst1,tst2,value",
    [
        (TsType("daily"), "daily", False),
        (TsType("2daily"), TsType("monthly"), False),
        (TsType("2daily"), TsType("1daily"), True),
    ],
)
def test_TsType__lt__(tst1, tst2, value):
    assert (tst1 < tst2) == value


@pytest.mark.parametrize(
    "tst1,tst2,value",
    [
        (TsType("daily"), "daily", True),
        (TsType("2daily"), TsType("monthly"), False),
        (TsType("2daily"), TsType("1daily"), True),
    ],
)
def test_TsType__le__(tst1, tst2, value):
    assert (tst1 <= tst2) == value


@pytest.mark.parametrize(
    "tst1,tst2,value",
    [
        (TsType("daily"), "daily", False),
        (TsType("2daily"), TsType("monthly"), True),
        (TsType("2daily"), TsType("1daily"), False),
    ],
)
def test_TsType__gt__(tst1, tst2, value):
    assert (tst1 > tst2) == value


@pytest.mark.parametrize(
    "tst1,tst2,value",
    [
        (TsType("daily"), "daily", True),
        (TsType("2daily"), TsType("monthly"), True),
        (TsType("2daily"), TsType("1daily"), False),
        (TsType("6daily"), TsType("MS"), True),
        (TsType("50daily"), TsType("MS"), False),
    ],
)
def test_TsType__ge__(tst1, tst2, value):
    assert (tst1 >= tst2) == value


def test_TsType__call__():
    assert TsType("daily")() == "daily"


def test_TsType__str__():
    assert str(TsType("daily")) == "daily"


def test_TsType__repr__():
    assert repr(TsType("daily")) == "daily"


@pytest.mark.parametrize(
    "input,expected",
    (
        pytest.param(
            ["monthly", "weekly", "daily", "hourly"], ["hourly", "daily", "weekly", "monthly"]
        ),
        pytest.param(
            ["3daily", "4daily", "6daily", "13daily"], ["3daily", "4daily", "6daily", "13daily"]
        ),
    ),
)
def test_sort_tstypes(input, expected):
    assert sort_ts_types(input) == expected


def test_get_lowest_resolution():
    assert get_lowest_resolution("3hourly", "hourly", "monthly", "yearly") == "yearly"
