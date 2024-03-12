from importlib import metadata


def test_gridded():
    names = {ep.name for ep in metadata.entry_points(group="pyaerocom.gridded")}
    assert names, "no entry points found"
    assert names == {"ReadMscwCtm"}


def test_ungridded():
    names = {ep.name for ep in metadata.entry_points(group="pyaerocom.ungridded")}
    assert names, "no entry points found"
    assert names == {"ReadGAW", "ReadGhost", "ReadMEP", "ReadICOS", "ReadICPForest"}
