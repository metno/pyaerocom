from pyaerocom.aeroval.collections import ObsCollection, ModelCollection
from pyaerocom.aeroval.obsentry import ObsEntry
from pyaerocom.aeroval.modelentry import ModelEntry
import pytest


def test_obscollection_init_and_add_entry():
    oc = ObsCollection()
    oc.add_entry("model1", dict(obs_id="bla", obs_vars="od550aer", obs_vert_type="Column"))
    assert oc

    oc.add_entry(
        "AN-EEA-MP",
        dict(
            is_superobs=True,
            obs_id=("AirNow", "EEA-NRT-rural", "MarcoPolo"),
            obs_vars=["concpm10", "concpm25", "vmro3", "vmrno2"],
            obs_vert_type="Surface",
        ),
    )

    assert "AN-EEA-MP" in oc.keylist()


def test_obscollection_add_and_get_entry():
    collection = ObsCollection()
    entry = ObsEntry(obs_id="obs1", obs_vars=("var1",))
    collection.add_entry("key1", entry)
    retrieved_entry = collection.get_entry("key1")
    assert retrieved_entry == entry


def test_obscollection_add_and_remove_entry():
    collection = ObsCollection()
    entry = ObsEntry(obs_id="obs1", obs_vars=("var1",))
    collection.add_entry("key1", entry)
    collection.remove_entry("key1")
    with pytest.raises(KeyError):
        collection.get_entry("key1")


def test_obscollection_get_web_interface_name():
    collection = ObsCollection()
    entry = ObsEntry(obs_id="obs1", obs_vars=("var1",), web_interface_name="web_name")
    collection.add_entry("key1", entry)
    assert collection.get_web_interface_name("key1") == "web_name"


def test_obscollection_all_vert_types():
    collection = ObsCollection()
    entry1 = ObsEntry(
        obs_id="obs1", obs_vars=("var1",), obs_vert_type="Surface"
    )  # Assuming ObsEntry has an obs_vert_type attribute
    entry2 = ObsEntry(obs_id="obs2", obs_vars=("var2",), obs_vert_type="Profile")
    collection.add_entry("key1", entry1)
    collection.add_entry("key2", entry2)
    assert set(collection.all_vert_types) == {"Surface", "Profile"}


def test_modelcollection_init_and_add_entry():
    mc = ModelCollection()
    mc.add_entry("model1", dict(model_id="bla", obs_vars="od550aer", obs_vert_type="Column"))
    assert mc

    mc.add_entry(
        "ECMWF_OSUITE",
        dict(
            model_id="ECMWF_OSUITE",
            obs_vars=["concpm10"],
            obs_vert_type="Surface",
        ),
    )

    assert "ECMWF_OSUITE" in mc.keylist()


def test_modelcollection_add_and_get_entry():
    collection = ModelCollection()
    entry = ModelEntry(model_id="mod1")
    collection.add_entry("key1", entry)
    retrieved_entry = collection.get_entry("key1")
    assert retrieved_entry == entry


def test_modelcollection_add_and_remove_entry():
    collection = ModelCollection()
    entry = ModelEntry(model_id="obs1")
    collection.add_entry("key1", entry)
    collection.remove_entry("key1")
    with pytest.raises(KeyError):
        collection.get_entry("key1")
