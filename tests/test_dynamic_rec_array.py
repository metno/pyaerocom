import numpy as np
from pyaerocom.dynamic_rec_array import DynamicRecArray


my_dtype = [("int", "i4"), ("int2", "i2")]


def test_DynamicRecArray__init__():
    ary = DynamicRecArray(my_dtype)
    assert ary._capacity == 10  # default capacity
    assert len(ary._array) == ary._capacity
    assert len(ary) == 0
    # internal structure on create
    assert isinstance(ary._array, np.ndarray)
    assert ary._array["int"].shape[0] == ary._capacity
    assert ary._array["int2"].shape[0] == ary._capacity
    # external structure should be empty
    assert isinstance(ary.data, np.ndarray)
    assert ary.data["int"].shape[0] == 0
    assert ary.data["int2"].shape[0] == 0

    ary = DynamicRecArray(my_dtype, 100)
    assert ary._capacity == 100
    assert len(ary._array) == ary._capacity
    assert len(ary) == 0

    # keys
    assert set(ary.keys()) == set([x[0] for x in my_dtype])


def test_data():
    ary = DynamicRecArray(my_dtype, 10)
    assert len(ary) == 0
    ary2 = DynamicRecArray(my_dtype, 100)
    rec_array = ary2._array
    ary.data = rec_array
    assert len(ary) == 100


def test_append():
    ary = DynamicRecArray(my_dtype, 10)
    assert len(ary) == 0
    # append single row
    ary.append([(0, 1)])
    assert len(ary) == 1
    assert ary.data[0]["int"] == 0
    assert ary.data[0]["int2"] == 1

    ary2 = DynamicRecArray(my_dtype, 100)
    rec_array = ary2._array
    rec_array["int"] = np.arange(100)
    rec_array["int2"] = 100 * rec_array["int"]
    ary2.data = rec_array
    assert len(ary2) == 100
    assert ary2.data[99]["int"] == 99
    assert ary2.data[99]["int2"] == 99 * 100

    ary.append(rec_array)
    assert len(ary) == 101
    assert ary.data[0]["int"] == 0
    assert ary.data[0]["int2"] == 1
    assert ary.data[100]["int"] == 99
    assert ary.data[100]["int2"] == 99 * 100


def test_append_array():
    ary = DynamicRecArray(my_dtype, 10)
    ary.append([(0, 1)])
    assert len(ary) == 1
    assert ary.data[0]["int"] == 0
    assert ary.data[0]["int2"] == 1

    a1 = np.zeros(100) + 1
    a2 = np.zeros(100) + 2
    ary.append_array(int=a1, int2=a2)
    assert len(ary) == 101
    assert ary.data[100]["int"] == 1
    assert ary.data[100]["int2"] == 2
