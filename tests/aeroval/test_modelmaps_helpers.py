from pyaerocom.aeroval.modelmaps_helpers import _jsdate_list, griddeddata_to_jsondict


def test__jsdate_list(data_tm5):
    vals = _jsdate_list(data_tm5)
    assert len(vals) == 12
    assert vals[0] == 1263513600000
    assert vals[-1] == 1292371200000


def test_griddeddata_to_jsondict(data_tm5):
    result = griddeddata_to_jsondict(data_tm5)
    assert isinstance(result, dict)
    assert "metadata" in result
    assert len(result["metadata"]) == 2
    assert "data" in result
    data = result["data"]
    assert "time" in data
    assert len(data["time"]) == 12
    assert len(data) == 2593
    del data["time"]
    pixel = list(data.values())[0]
    assert "lat" in pixel
    assert isinstance(pixel["lat"], float)
    assert "lon" in pixel
    assert isinstance(pixel["lon"], float)
    assert "data" in pixel
    assert len(pixel["data"]) == 12
