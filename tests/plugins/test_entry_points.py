from importlib import metadata


def test_gridded():
    assert not metadata.entry_points(group="pyaerocom.gridded")


def test_ungridded():
    names = {ep.name for ep in metadata.entry_points(group="pyaerocom.ungridded")}
    assert names, "no entry points found"
    assert names == {"ReadGAW", "ReadGhost", "ReadMEP", "ReadICOS", "ReadICPForest"}
