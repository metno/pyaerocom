import numpy as np
from numpy.typing import DTypeLike


class DynamicRecArrayException(Exception):
    pass


class DynamicRecArray:
    def __init__(self, dtype: DTypeLike, capacity: int = 10):
        """A dynamic record based array of type dtype.

        :param dtype: Datatype of the array. Must be readable by :class:`~numpy.dtype`
        :param capacity: optional initial capacity, i.e. initial hidden array-size.
            Use a large capacity if you intent use many `append` operation on the data.
        """
        self._dtype = np.dtype(dtype)
        self._length = 0
        self._capacity = capacity
        self._array = np.empty(self._capacity, dtype=self._dtype)

    def __len__(self):
        return self._length

    def keys(self):
        """all available data-fields, excluding variable and units which are
        considered metadata"""
        return self._array.dtype.names

    def append(self, rec: list[tuple] | np.ndarray):
        """append this dataset with a record of the same type

        Example: append two rows to a three-datatype array
        ary.append([(0, 1, 3),
                    (4, 5, 6)])

        :param rec: a numpy array of the same datatype, or a list of tuples with the same number of elements

        """
        newlength = self._length + len(rec)
        resize = False
        while self._capacity <= newlength:
            self._capacity += 10 + (self._capacity >> 3)  # 20 + 1.125*self._capacity
            resize = True
        if resize:
            self._array = np.resize(self._array, self._capacity)
        self._array[self._length : newlength] = rec
        self._length = newlength

    def append_array(self, **kwargs):
        """append data using a dictionary of np-arrays

        :raises DynamicRecArrayException: if keys are missing, or shapes are not equal
        """
        key0 = self.keys()[0]
        for key in self.keys():
            if key not in kwargs:
                raise DynamicRecArrayException(f"missing key {key} in arguments")
            if kwargs[key].shape[0] != kwargs[key0].shape[0]:
                raise DynamicRecArrayException(
                    f"array {key} size ({kwargs[key0].shape[0]}) != {key0} size ({kwargs[key0].shape[0]})"
                )
        add_len = kwargs[key0].shape[0]
        if add_len > 0:
            last_pos = len(self)
            data = np.resize(self.data, last_pos + add_len)
            for key in self.keys():
                data[key][last_pos:] = kwargs[key]
            self.data = data

    @property
    def data(self) -> np.array:
        """Return the numpy array. Access to the data array will also shring the capacity
        to the length of the array. The returned array is not a copy but a internal view.

        :return: np.aarry of type dtype
        """
        if self._capacity != self._length:
            self._array = self._array[:][: self._length]
            self._capacity = len(self._array)
        return self._array

    @data.setter
    def data(self, data):
        """Set the data of the record

        :param data: numpy array with the same dtype
        """
        self._length = len(data)
        self._capacity = len(data)
        self._array = data
