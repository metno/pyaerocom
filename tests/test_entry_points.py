from importlib import metadata


def test_gridded():
    assert not metadata.entry_points(group="pyaerocom.gridded")


def test_ungridded():
    assert not metadata.entry_points(group="pyaerocom.ungridded")
