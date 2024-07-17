import abc

from pyaerocom.griddeddata import GriddedData


class GriddedModelReader(abc.ABC):
    """Abstract base class for griddel model reader used for collocation"""

    @property
    @abc.abstractmethod
    def data_id(self) -> str:
        """
        Data ID of dataset
        """
        pass

    @property
    @abc.abstractmethod
    def ts_type(self):
        """
        Frequency of time dimension of current data file. Since a reader
        might have multiple ts_types, this value is volatile.

        Raises
        ------
        AttributeError
            if :attr:`filename` is not set.

        Returns
        -------
        str
            current ts_type.

        """
        pass

    @property
    @abc.abstractmethod
    def ts_types(self):
        """
        List of available frequencies

        Raises
        ------
        AttributeError
            if :attr:`data_dir` is not set.

        Returns
        -------
        list
            list of available frequencies

        """
        pass

    @property
    @abc.abstractmethod
    def years_avail(self) -> list:
        """
        Years available in dataset
        """
        pass

    @property
    @abc.abstractmethod
    def vars_provided(self):
        """Variables provided by this dataset"""
        pass

    @abc.abstractmethod
    def has_var(self, var_name):
        """Check if variable is supported

        Parameters
        ----------
        var_name : str
            variable to be checked

        Returns
        -------
        bool
        """
        pass

    @abc.abstractmethod
    def read_var(self, var_name, ts_type=None, **kwargs) -> GriddedData:
        """Load data for given variable.

        Parameters
        ----------
        var_name : str
            Variable to be read
        ts_type : str
            Temporal resolution of data to read. Supported are
            "hourly", "daily", "monthly" , "yearly".

        Returns
        -------
        GriddedData
        """
        pass
