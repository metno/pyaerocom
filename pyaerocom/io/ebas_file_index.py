import logging
import os
import sqlite3

from pyaerocom._lowlevel_helpers import BrowseDict

logger = logging.getLogger(__name__)


class EbasSQLRequest(BrowseDict):
    """Low level dictionary like object for EBAS sqlite queries

    Attributes
    ----------
    variables : :obj:`tuple`, optional
        tuple containing variable names to be extracted (e.g.
        ``('aerosol_light_scattering_coefficient', 'aerosol_optical_depth')``).
        If None, all available is used
    start_date : :obj:`str`, optional
        start date of data request (format YYYY-MM-DD). If None, all available
        is used
    stop_date : :obj:`str`, optional
        stop date of data request (format YYYY-MM-DD). If None, all available
        is used
    station_names : :obj:`tuple`, optional
        tuple containing station_names of request (e.g.
        ``('Birkenes II', 'Asa')``).If None, all available is used
    matrices : :obj:`tuple`, optional
        tuple containing station_names of request (e.g.
        ``('pm1', 'pm10', 'pm25', 'aerosol')``)
        If None, all available is used
    altitude_range : :obj:`tuple`, optional
        tuple specifying altitude range of station in m (e.g.
        ``(0.0, 500.0)``). If None, all available is used
    lon_range : :obj:`tuple`, optional
        tuple specifying longitude range of station in degrees (e.g.
        ``(-20, 20)``). If None, all available is used
    lat_range : :obj:`tuple`, optional
        tuple specifying latitude range of station in degrees (e.g.
        ``(50, 80)``). If None, all available is used
    instrument_type : :obj:`str`, optional
        string specifying instrument types (e.g.
        ``("nephelometer")``)
    statistics : :obj:`tuple`, optional
        string specifying statistics code (e.g.
        ``("arithmetic mean")``)

    Parameters
    ----------
    see Attributes
    """

    def __init__(
        self,
        variables=None,
        start_date=None,
        stop_date=None,
        station_names=None,
        matrices=None,
        altitude_range=None,
        lon_range=None,
        lat_range=None,
        instrument_types=None,
        statistics=None,
        datalevel=None,
    ):
        self.variables = variables
        self.start_date = start_date
        self.stop_date = stop_date
        self.station_names = station_names
        self.matrices = matrices
        self.altitude_range = altitude_range
        self.lon_range = lon_range
        self.lat_range = lat_range
        self.instrument_types = instrument_types
        self.statistics = statistics
        self.datalevel = datalevel

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if k in self:
                self[k] = v
            else:
                logger.warning(f"Unknown EBAS SQL request key {k} (value {v})")

    @staticmethod
    def _var2sql(var):
        if isinstance(var, list):
            if len(var) > 1:
                var = tuple(var)
            else:
                var = var[0]

        if isinstance(var, tuple):
            return f"{var}"
        elif isinstance(var, str):
            return f"('{var}')"
        raise ValueError("Invalid value...")

    def make_file_query_str(self, distinct=True, **kwargs):
        """Wrapper for base method :func:`make_query_str`

        Parameters
        ----------
        distinct : bool
            return unique files
        **kwargs
            update request attributes (e.g. ``lon_range=(30, 60)``)

        Returns
        -------
        str
            SQL file request command for current specs
        """
        query = self.make_query_str(distinct=distinct, **kwargs)
        # add an extsion to get only files that have no fraction variables in them
        query = query.replace(
            ";",
            " and not exists (select * from characteristic where var_id=variable.var_id and ct_type='Fraction');",
        )
        return query

    def make_query_str(self, what=None, distinct=True, **kwargs):
        """Translate current class state into SQL query command string

        Parameters
        ----------
        what : str or tuple, optional
            what columns to retrieve (e.g. comp_name for all variables) from
            table specified. Defaults to None, in which case "filename" is used
        distinct : bool
            return unique files
        **kwargs
            update request attributes (e.g. ``lon_range=(30, 60)``)

        Returns
        -------
        str
            SQL file request command for current specs
        """
        self.update(**kwargs)
        if what is None:
            what = "filename"
        elif not isinstance(what, str):  # tuple or list of parameters to be retrieved
            what = ",".join(what)

        if distinct:
            req = f"select distinct {what} from variable"
        else:
            req = f"select {what} from variable"
        req += " join station on station.station_code=variable.station_code"
        add_cond = 0
        # add constraints from station table
        conv = self._var2sql
        if self.station_names is not None:
            req += f" where station_name in {conv(self.station_names)}"
            add_cond += 1
        if self.altitude_range is not None:
            low, high = self.altitude_range
            req += " and " if add_cond else " where "
            req += f"station_altitude>{low} and station_altitude<{high}"
            add_cond += 1
        if self.lon_range is not None:
            west, east = self.lon_range
            req += " and " if add_cond else " where "
            req += f"station_longitude>{west} and station_longitude<{east}"
            add_cond += 1
        if self.lat_range is not None:
            south, north = self.lat_range
            req += " and " if add_cond else " where "
            req += f"station_latitude>{south} and station_latitude<{north}"
            add_cond += 1
        if self.instrument_types is not None:
            req += " and " if add_cond else " where "
            req += f"instr_type in {conv(self.instrument_types)}"
            add_cond += 1
        # add constraints from variable table
        if self.variables is not None:
            req += " and " if add_cond else " where "
            req += f"comp_name in {conv(self.variables)}"
            add_cond += 1
        if self.stop_date is not None:
            req += " and " if add_cond else " where "
            req += f"first_end < '{self.stop_date}'"
            add_cond += 1
        if self.start_date is not None:
            req += " and " if add_cond else " where "
            req += f"last_start > '{self.start_date}'"
            add_cond += 1
        if self.matrices is not None:
            req += " and " if add_cond else " where "
            req += f"matrix in {conv(self.matrices)}"
            add_cond += 1
        if self.statistics is not None:
            req += " and " if add_cond else " where "
            req += f"statistics in {conv(self.statistics)}"
            add_cond += 1
        if self.datalevel is not None:
            req += " and " if add_cond else " where "
            req += f"datalevel={self.datalevel}"
            add_cond += 1
        return req + ";"

    def __str__(self):
        head = f"Pyaerocom {type(self).__name__}"
        s = f"\n{head}\n{len(head) * '-'}"
        for k, v in self.items():
            s += f"\n{k}: {v}"
        s += f"\nFilename request string:\n{self.make_file_query_str()}"
        return s


class EbasFileIndex:
    """EBAS SQLite I/O interface

    Takes care of connection to database and execution of requests
    """

    def __init__(self, database=None):
        self._database = database

    @property
    def database(self):
        """Path to ebas_file_index.sqlite3 file"""
        db = self._database
        if db is None or not os.path.exists(db):
            raise AttributeError(
                "EBAS SQLite database file could not be "
                "located but is needed in EbasFileIndex class"
            )
        return db

    @property
    def ALL_STATION_NAMES(self):
        """List of all available station names in database"""
        names = self.execute_request("select distinct station_name from station")
        return [x[0] for x in names]

    @property
    def ALL_STATION_CODES(self):
        """List of all available station codes in database

        Note
        ----
        Not tested whether the order is the same as the order in
        :attr:`STATION_NAMES`, i.e. the lists should not be linked to each
        other
        """
        names = self.execute_request("select distinct station_code from station")
        return [x[0] for x in names]

    @property
    def ALL_STATISTICS_PARAMS(self):
        """List of all statistical parameters available

        For more info see `here <https://ebas-submit.nilu.no/Submit-Data/
        Data-Reporting/Comments/Generic-metadata-comments/Statistics>`__
        """
        names = self.execute_request("select distinct statistics from variable")
        return [x[0] for x in names]

    @property
    def ALL_VARIABLES(self):
        """List of all variables available"""
        names = self.execute_request("select distinct comp_name from variable")
        return [x[0] for x in names]

    @property
    def ALL_MATRICES(self):
        """List of all matrix values available"""
        names = self.execute_request("select distinct matrix from variable")
        return [x[0] for x in names]

    @property
    def ALL_INSTRUMENTS(self):
        """List of all variables available"""
        names = self.execute_request("select distinct instr_type from variable")
        return [x[0] for x in names]

    def get_table_names(self):
        """Get all table names in SQLite database file"""
        return [
            x[0]
            for x in self.execute_request("SELECT name FROM sqlite_master WHERE type='table';")
        ]

    def get_table_columns(self, table_name):
        """Get all columns of a table in SQLite database file"""
        req = f"select * from {table_name} where 1=0;"
        with sqlite3.connect(f"file:{self.database}?mode=ro", uri=True) as con:
            cur = con.cursor()
            cur.execute(req)
            return [f[0] for f in cur.description]

    def execute_request(self, request, file_request=False):
        """Connect to database and retrieve data for input request

        Parameters
        ----------
        request : :obj:`EbasSQLRequest` or :obj:`str`
            request specifications

        Returns
        -------
        list
            list of tuples containing the retrieved results. The number of
            items in each tuple corresponds to the number of requested
            parameters (usually one, can be specified in
            :func:`make_query_str` using argument ``what``)

        """
        if isinstance(request, str):
            sql_str = request
        elif isinstance(request, EbasSQLRequest):
            if not file_request:
                sql_str = request.make_query_str()
            else:
                sql_str = request.make_file_query_str()
        else:
            raise ValueError(f"Unsupported request type {type(request)}")

        try:
            with sqlite3.connect(f"file:{self.database}?mode=ro", uri=True) as con:
                cur = con.cursor()
                cur.execute(sql_str)
                return [f for f in cur.fetchall()]
        except Exception as ex:
            logger.error(f"Error with {self.database} and {sql_str}")
            raise ex

    def get_file_names(self, request):
        """Get all files that match the request specifications

        Parameters
        ----------
        request : :obj:`EbasSQLRequest` or :obj:`str`
            request specifications

        Returns
        -------
        list
            list of file paths that match the request
        """
        return [f[0] for f in self.execute_request(request, file_request=True)]
