import numpy as np


class DynamicRecArrayException(Exception):
    pass


class DynamicRecArray:
    def __init__(self, dtype, capacity: int = 10):
        """A dynamic record based array of type dtype.

        :param dtype: Datatype of the array. Must be readable by :class:`~numpy.dtype`
        :param capacity: optional initial capacity
        """
        self.dtype = np.dtype(dtype)
        self.length = 0
        self.capacity = capacity
        self._data = np.empty(self.capacity, dtype=self.dtype)

    def __len__(self):
        return self.length

    def keys(self):
        """all available data-fields, excluding variable and units which are
        considered metadata"""
        return self._data.dtype.names

    def append(self, rec):
        """append this dataset with a record of the same type

        :param rec: a numpy array of the same datatype
        """
        if self.length == self.capacity:
            self.capacity += 10 + (self.capacity >> 3)  # 20 + 1.125*self.capacity
            self._data = np.resize(self._data, self.capacity)
        self._data[self.length] = rec
        self.length += 1

    def append_array(self, **kwargs):
        for key in self.keys():
            if key not in kwargs:
                raise DynamicRecArrayException(f"missing key {key} in arguments")
            if kwargs[key].shape[0] != kwargs["values"].shape[0]:
                raise DynamicRecArrayException(
                    f"array {key} size ({kwargs['values'].shape[0]}) != values size ({kwargs['values'].shape[0]})"
                )
        add_len = kwargs["values"].shape[0]
        if add_len > 0:
            last_pos = len(self)
            data = np.resize(self.data, last_pos + add_len)
            for key in self.keys():
                data[key][last_pos:] = kwargs[key]
            self.data = data

    @property
    def data(self):
        """Return the numpy array

        :return: np.arry of type dtype
        """
        if self.capacity != self.length:
            self._data = self._data[:][: self.length]
            self.capacity = len(self._data)
        return self._data

    @data.setter
    def data(self, data):
        """Set the data of the record

        :param data: numpy array with the same dtype
        """
        self.length = len(data)
        self.capacity = len(data)
        self._data = data
