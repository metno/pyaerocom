from pyaerocom.aeroval.varinfo_web import VarinfoWeb


def test_varinfo_web():
    info = VarinfoWeb.from_dict({"var_name": "od550aer"})
    assert info
    assert info.var_name == "od550aer"
