import sys

if sys.version_info >= (3, 10):  # pragma: no cover
    from importlib import metadata
else:  # pragma: no cover
    import importlib_metadata as metadata


def test_gridded():
    names = {ep.name for ep in metadata.entry_points(group="pyaerocom.gridded")}
    assert names, "no entry points found"
    assert names == {"ReadMscwCtm"}


def test_ungridded():
    names = {ep.name for ep in metadata.entry_points(group="pyaerocom.ungridded")}
    assert names, "no entry points found"
    assert names == {"ReadGAW", "ReadGhost", "ReadMEP", "ReadICOS", "ReadIPCForest"}
