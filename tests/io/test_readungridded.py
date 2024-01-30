import pytest

from pyaerocom import const
from pyaerocom.io import ReadUngridded

from pyaerocom.io import PyaroConfig, ReadPyaro
from tests.fixtures.pyaro import pyaro_test_data_file, make_csv_test_file, pyaro_testconfig


def test_invalid_init_data_dirs():
    data_dirs = "/bla/blub"
    with pytest.raises(ValueError) as e:
        ReadUngridded(["EBASMC", "GHOST.EEA.daily"], data_dirs=data_dirs)
    assert str(e.value) == f"Invalid input for data_dirs ({data_dirs}); needs to be a dictionary."


def test_supported():
    supported_datasets = ReadUngridded().supported_datasets
    assert len(supported_datasets) >= 17
    datasets = {
        "AeronetInvV3Lev2.daily",
        "AeronetInvV3Lev1.5.daily",
        "AeronetInvV3L2Subset.daily",
        "AeronetInvV2Lev2.daily",
        "AeronetInvV2Lev1.5.daily",
        "AeronetSDAV2Lev2.daily",
        "AeronetSDAV3Lev1.5.daily",
        "AeronetSDAV3Lev2.daily",
        "AeronetSDAV3L2Subset.daily",
        "AeronetSunV2Lev2.daily",
        "AeronetSunV2Lev2.AP",
        "AeronetSunV3Lev1.5.daily",
        "AeronetSunV3Lev1.5.AP",
        "AeronetSunV3Lev2.daily",
        "AeronetSunV3Lev2.AP",
        "AeronetSunV3L2Subset.daily",
        "EARLINET",
        "EBASMC",
        "EBASSubset",
        "DMS_AMS_CVO",
        "GAWTADsubsetAasEtAl",
        "GHOST.EEA.monthly",
        "GHOST.EEA.hourly",
        "GHOST.EEA.daily",
        "GHOST.EBAS.monthly",
        "GHOST.EBAS.hourly",
        "GHOST.EBAS.daily",
    }
    assert datasets <= set(supported_datasets)


@pytest.mark.parametrize("data_ids", [None, "Blaaaaaa"])
@pytest.mark.parametrize("ignore_cache", [False, True])
def test_ReadUngridded___init__(data_ids, ignore_cache):
    _caching = const.CACHING
    ReadUngridded(data_ids=data_ids, ignore_cache=ignore_cache)
    if ignore_cache:
        assert not const.CACHING
    const.CACHING = _caching


@pytest.mark.parametrize(
    "filter_post,nst,nmeta",
    [
        (None, 22, 22),
        (dict(station_name="La_Paz"), 1, 1),
        (dict(station_name=["La_Paz", "AAO*"]), 2, 2),
        (dict(altitude=[1000, 10000]), 3, 3),
        (dict(altitude=[1000, 10000], ignore_station_names=dict(od550aer="La_Paz")), 2, 2),
        (dict(altitude=[1000, 10000], ignore_station_names="La_*"), 2, 2),
        (dict(altitude=[1000, 10000], ignore_station_names=["La_*", "Mauna_Loa"]), 1, 1),
    ],
)
@pytest.mark.parametrize(
    "only_cached,caching",
    [(False, False), (True, True), (False, True)],
)
def test_ReadUngridded_read(only_cached, filter_post, nst, nmeta, caching):
    reader = ReadUngridded()

    const.CACHING = caching
    data = reader.read(
        data_ids="AeronetSunV3L2Subset.daily",
        vars_to_retrieve="od550aer",
        only_cached=only_cached,
        filter_post=filter_post,
    )

    assert len(data.metadata) == nmeta
    assert len(data.unique_station_names) == nst

    const.CACHING = True


def test_ReadUngridded_read_error():
    reader = ReadUngridded()

    with pytest.raises(NotImplementedError) as e:
        reader.read(
            data_ids="AeronetSunV3L2Subset.daily",
            vars_to_retrieve=["od550aer", "ang4487aer"],
            filter_post=dict(altitude=[1000, 10000], ignore_station_names=dict(od550aer="La_Paz")),
        )
    assert str(e.value).startswith(
        "Cannot filter different sites for multivariable UngriddedData objects"
    )


def test_basic_attributes():
    reader = ReadUngridded()
    assert not reader.ignore_cache
    assert reader.data_ids == []
    with pytest.raises(ValueError):
        reader.get_lowlevel_reader()
    with pytest.raises(AttributeError):
        reader.dataset_provides_variables()


#########################################
# Tests for use of PyaroConfig
#########################################


def test_init_config(pyaro_testconfig):
    reader = ReadUngridded(config=pyaro_testconfig)

    assert reader.data_id == pyaro_testconfig.data_id


def test_get_lowlevel_reader_config(pyaro_testconfig):
    reader = ReadUngridded(config=pyaro_testconfig)

    ll_reader = reader.get_lowlevel_reader(data_id=None, config=pyaro_testconfig)
    assert isinstance(ll_reader, ReadPyaro)


def test_supported_pyaro(pyaro_testconfig):
    reader = ReadUngridded(config=pyaro_testconfig)

    assert ReadPyaro in reader.SUPPORTED_READERS
    assert pyaro_testconfig.data_id in reader.supported_datasets


def test_read_pyaro_and_other(pyaro_testconfig):
    data_ids = ["AeronetInvV3L2Subset.daily"]
    reader = ReadUngridded(config=pyaro_testconfig)

    data = reader.read(data_ids, config=pyaro_testconfig)
    assert len(data.contains_datasets) == 2
    assert pyaro_testconfig.data_id in data.contains_datasets


##
# Tests that raises errors
##


def test_different_data_id(pyaro_testconfig):
    diff_data_id = "invalid"
    reader = ReadUngridded(config=pyaro_testconfig)

    with pytest.raises(
        ValueError, match="DATA ID and config are both given, but they are not equal"
    ):
        reader.get_lowlevel_reader(data_id=diff_data_id, config=pyaro_testconfig)
