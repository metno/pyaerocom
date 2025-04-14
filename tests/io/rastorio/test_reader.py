from pyaerocom.io.rastorio.reader import RastorioReader


def test_reader():
    reader = RastorioReader("test", "mean_dryHNO3_2008_hm.tif")  # TODO: Fix file path location.

    assert set(reader.years_avail) == {"2008"}
    assert reader.has_var("dryhno3")
    assert set(reader.ts_types) == {"yearly"}
    assert len(reader._files) == 1
    assert len(reader._meta) == 1


def test_reader2():
    reader = RastorioReader("test", "mean_dryHNO3_2008_hm.tif")  # TODO: Fix file path location.

    data = reader.read_var("dryhno3", ts_type="yearly")

    assert True
