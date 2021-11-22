import numpy as np
import pytest

from pyaerocom.exceptions import TemporalResolutionError
from pyaerocom.tstype import TsType


def test_TsType_VALID():
    assert TsType.VALID == ["minutely", "hourly", "daily", "weekly", "monthly", "yearly", "native"]


def test_TsType_VALID_ITER():
    assert TsType.VALID_ITER == ["minutely", "hourly", "daily", "weekly", "monthly", "yearly"]


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
    "base,mulfac",
    [
        ("daily", 10),
        ("daily", "10"),
        ("daily", 10.1),
    ],
)
def test_TsType_mulfac(base, mulfac):
    tst = TsType(base)
    tst.mulfac = mulfac
    assert int(mulfac) == tst._mulfac == tst.mulfac


@pytest.mark.parametrize(
    "base,mulfac,error",
    [
        ("daily", "10.1", "mulfac needs to be int or convertible to int"),
        ("daily", 200, "Multiplication factor exceeds maximum allowed, which is 180"),
    ],
)
def test_TsType_mulfac_error(base, mulfac, error: str):
    tst = TsType(base)
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
            "Choose from ['minutely', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'native']",
        ),
        (
            "5000daily",
            "Invalid input for ts_type daily. "
            "Multiplication factor 5000 exceeds maximum allowed for daily, which is 180",
        ),
    ],
)
def test_TsType_val_error(value: str, error: str):
    tst = TsType("daily")
    with pytest.raises(TemporalResolutionError) as e:
        tst.val = value
    assert str(e.value) == error


def test_TsType_datetime64_str():
    assert TsType("daily").datetime64_str == "datetime64[1D]"


def test_TsType_timedelta64_str():
    assert TsType("daily").timedelta64_str == "timedelta64[1D]"


@pytest.mark.parametrize(
    "base,value",
    [
        ("hourly", "hours"),
        ("daily", "days"),
        ("monthly", "days"),
    ],
)
def test_TsType_cf_base_unit(base, value):
    tst = TsType(base)
    assert tst.cf_base_unit == value


@pytest.mark.parametrize(
    "base,error",
    [
        ("native", "Cannot convert native to CF str"),
        ("minutely", "Cannot convert minutely to CF str"),
        ("yearly", "Cannot convert yearly to CF str"),
    ],
)
def test_TsType_cf_base_unit_error(base, error: str):
    tst = TsType(base)
    with pytest.raises(NotImplementedError) as e:
        assert tst.cf_base_unit == None
    assert str(e.value) == error


@pytest.mark.parametrize(
    "ts_type,should_be",
    [
        ("minutely", 60),
        ("3minutely", 180),
        ("4minutely", 240),
        ("daily", 86400),
        ("weekly", 86400 * 7),
        ("monthly", 2629743.831225),  # not sure how cf_units calculates that
    ],
)
def test_TsType_num_secs(ts_type, should_be):
    val = TsType(ts_type).num_secs
    assert val == should_be


@pytest.mark.parametrize(
    "ts_type,should_be",
    [
        ("minutely", 3),
        ("3minutely", 9),
        ("4minutely", 12),
        ("daily", 4320),
        ("weekly", 30240),
        ("monthly", 131488),
    ],
)
def test_TsType_tol_secs(ts_type, should_be):
    val = TsType(ts_type).tol_secs
    assert val == should_be


@pytest.mark.parametrize(
    "ts_type,ref_time_str,np_dt_str,output_str",
    [
        ("daily", "2010-10-01", "D", "2010-10-02"),
        ("2monthly", "2010-10", "M", "2010-12"),
        ("3hourly", "2010-10-01T15:00:00", "h", "2010-10-01T18"),
    ],
)
def test_TsType_to_timedelta64(ts_type, ref_time_str, np_dt_str, output_str):
    tref = np.datetime64(ref_time_str, np_dt_str)
    assert str(tref + TsType(ts_type).to_timedelta64()) == output_str


@pytest.mark.parametrize(
    "ts_type,value",
    [
        ("3minutely", "minutely"),
        ("hourly", "minutely"),
        ("3hourly", "hourly"),
        ("weekly", "daily"),
        ("monthly", "weekly"),
        ("yearly", "monthly"),
    ],
)
def test_TsType_next_higher(ts_type, value):
    assert TsType(ts_type).next_higher.val == value


def test_TsType_next_higher_error():
    with pytest.raises(IndexError) as e:
        assert TsType("minutely").next_higher.val == None
    assert str(e.value) == "No higher resolution available than minutely"


@pytest.mark.parametrize(
    "ts_type,value",
    [
        ("yearly", "2yearly"),
        ("monthly", "yearly"),
        ("3monthly", "yearly"),
        ("8daily", "2weekly"),
        ("13monthly", "2yearly"),
        ("13monthly", "2yearly"),
        ("1000yearly", "1001yearly"),
    ],
)
def test_TsType_next_lower(ts_type, value):
    assert TsType(ts_type).next_lower.val == value


def test_TsType_next_lower_error():
    with pytest.raises(TemporalResolutionError) as e:
        assert TsType("120monthly").next_lower.val == None
    assert str(e.value) == "Failed to determine next lower resolution for 120monthly"


@pytest.mark.parametrize("val,valid", [("bla", False), ("60000daily", False), ("daily", True)])
def test_TsType_valid(val, valid):
    assert TsType.valid(val) == valid


@pytest.mark.parametrize(
    "tst,val",
    [
        ("3hourly", "3h"),
        ("daily", "1D"),
    ],
)
def test_TsType_to_numpy_freq(tst, val):
    assert TsType(tst).to_numpy_freq() == val


def test_TsType_to_numpy_freq_error():
    with pytest.raises(TemporalResolutionError) as e:
        TsType("native").to_numpy_freq()
    assert str(e.value) == "numpy frequency not available for native"


@pytest.mark.parametrize(
    "tst,val",
    [
        ("3hourly", "3H"),
        ("daily", "D"),
    ],
)
def test_TsType_to_pandas_freq(tst, val):
    assert TsType(tst).to_pandas_freq() == val


def test_TsType_to_pandas_freq_error():
    with pytest.raises(TemporalResolutionError) as e:
        TsType("native").to_pandas_freq()
    assert str(e.value) == "pandas frequency not available for native"


@pytest.mark.parametrize(
    "ts_type,value",
    [
        ("hourly", "h"),
        ("3hourly", "(3h)"),
        ("daily", "d"),
        ("minutely", "min"),
        ("weekly", "week"),
        ("monthly", "month"),
        ("4weekly", "(4week)"),
    ],
)
def test_TsType_to_si(ts_type, value):
    assert TsType(ts_type).to_si() == value


def test_TsType_to_si_error():
    with pytest.raises(ValueError) as e:
        TsType("native").to_si()
    assert str(e.value) == "Cannot convert ts_type=native to SI unit string..."


@pytest.mark.parametrize(
    "ts_type,to_ts_type,min_num_obs,val",
    [
        ("hourly", "hourly", {}, 0),
        ("12hourly", "6daily", {"daily": {"hourly": 12}}, 6),
        ("84hourly", "6daily", {"daily": {"hourly": 24}}, 2),
        ("84hourly", "6daily", {"daily": {"hourly": 1}}, 0),
        ("84hourly", "6daily", {"daily": {"hourly": 12}}, 1),
        ("84hourly", "4daily", {"daily": {"84hourly": 0.1}}, 0),
        ("84hourly", "6daily", {"daily": {"84hourly": 0.1}}, 1),
        ("2hourly", "3daily", {"3daily": {"2hourly": 4}}, 4),
        ("2hourly", "3daily", {"3daily": {"hourly": 4}}, 2),
        ("10hourly", "monthly", {"monthly": {"hourly": 100}}, 10),
    ],
)
def test_TsType_get_min_num_obs(ts_type, to_ts_type, min_num_obs, val):
    assert TsType(ts_type).get_min_num_obs(TsType(to_ts_type), min_num_obs) == val


@pytest.mark.parametrize(
    "ts_type,to_ts_type,exception,error",
    [
        (
            "84hourly",
            "3daily",
            TemporalResolutionError,
            "input ts_type 3daily is lower resolution than current 84hourly",
        ),
        (
            "hourly",
            "minutely",
            TemporalResolutionError,
            "input ts_type minutely is lower resolution than current hourly",
        ),
        (
            "hourly",
            "daily",
            ValueError,
            "could not infer min_num_obs value from input dict {} for conversion from hourly to daily",
        ),
    ],
)
def test_TsType_get_min_num_obs_error(ts_type, to_ts_type, exception, error: str):
    with pytest.raises(exception) as e:
        TsType(ts_type).get_min_num_obs(TsType(to_ts_type), {})
    assert str(e.value) == error


@pytest.mark.parametrize(
    "ts_type, total_seconds, value",
    [
        ("hourly", 3600, True),
        ("hourly", 3605, True),
        ("20minutely", 1200, True),
        ("native", 1200, False),
    ],
)
def test_TsType_check_match_total_seconds(ts_type, total_seconds, value):
    assert TsType(ts_type).check_match_total_seconds(total_seconds) == value


@pytest.mark.parametrize(
    "base,total_seconds,val",
    [
        ("daily", 86400 * 2, "2daily"),
        ("daily", 86400, "daily"),
        ("daily", 86000, "daily"),  # 5% tolerance
        ("yearly", 31556925, "yearly"),
    ],
)
def test_TsType__try_infer_from_total_seconds(base, total_seconds, val):
    tst = TsType._try_infer_from_total_seconds(base, total_seconds)
    assert isinstance(tst, TsType)
    assert str(tst) == val


def test_TsType__try_infer_from_total_seconds_error():
    base, seconds = "yearly", 31556925 * 2
    error = f"Period {seconds}s could not be associated with any allowed multiplication factor of base frequency {base}"
    with pytest.raises(TemporalResolutionError) as e:
        TsType._try_infer_from_total_seconds(base, seconds)
    assert str(e.value) == error


@pytest.mark.parametrize(
    "total_seconds,value",
    [
        (86400 * 2, "2daily"),
        (3605, "hourly"),
        (1200, "20minutely"),
        (31556925 * 2, "24monthly"),
    ],
)
def test_TsType_from_total_seconds(total_seconds, value):
    tst = TsType.from_total_seconds(total_seconds)
    assert tst.val == value


@pytest.mark.parametrize("total_seconds", [(30), (31556925 * 12)])
def test_TsType_from_total_seconds_error(total_seconds):
    with pytest.raises(TemporalResolutionError) as e:
        TsType.from_total_seconds(total_seconds)
    assert str(e.value) == f"failed to infer ts_type based on input dt={total_seconds} s"


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
