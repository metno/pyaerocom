import pytest

from pyaerocom import const
from pyaerocom.io import ReadUngridded


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
