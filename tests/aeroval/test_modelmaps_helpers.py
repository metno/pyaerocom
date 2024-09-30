from pyaerocom.aeroval.modelmaps_helpers import _jsdate_list


def test__jsdate_list(data_tm5):
    vals = _jsdate_list(data_tm5)
    assert len(vals) == 12
    assert vals[0] == 1263513600000
    assert vals[-1] == 1292371200000
