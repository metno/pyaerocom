#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyaerocom import const as const
from collections import OrderedDict as od
import sqlite3
import sys
import os

class EbasSQLRequest(dict):
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
        tuple specifying alEtitude range of station in m (e.g.
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
    def __init__(self, variables=None, start_date=None, stop_date=None, 
                 station_names=None, matrices=None, altitude_range=None, 
                 lon_range=None, lat_range=None, 
                 instrument_types=None, statistics=None):
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
        
    
    def update(self, verbose=True, **kwargs):
        for k, v in kwargs.items():
            if k in self:
                self[k] = v
            else:
                if verbose:
                    print("Unknown request key {} (value {})".format(k, v))
    
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
        return self.make_query_str(distinct=distinct, **kwargs)
    
    @staticmethod
    def _var2sql(var):
        if isinstance(var, list):
            var = tuple(var)
        if isinstance(var, tuple):
            return "{}".format(var)
        elif isinstance(var, str):
            return "(\'{}\')".format(var)
        else:
            raise ValueError("Invalid value encountered, need list, tuple or "
                             "str, got {}".format(type(var)))
            
    def make_query_str(self, what="filename",
                       distinct=True, **kwargs):
        """Translate current class state into SQL query command string 
        
        Parameters
        ----------
        what : :obj:`str` or :obj:`tuple`
            what columns to retrieve (e.g. comp_name for all variables) from
            table specified. 
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
        if not isinstance(what, str): #tuple or list of parameters to be retrieved
            what = ",".join(what)
        
        if distinct:
            req = 'select distinct {} from variable'.format(what)
        else:
            req = 'select {} from variable'.format(what)
        req += ' join station on station.station_code=variable.station_code'
        add_cond = 0
        # add constraints from station table
        conv = self._var2sql
        if self.station_names is not None:
            
            req += ' where station_name in {}'.format(conv(self.station_names))
            add_cond += 1
        if self.altitude_range is not None:
            low, high = self.altitude_range
            req += ' and ' if add_cond else ' where '
            req += ('station_altitude>{} and '
                    'station_altitude<{}'.format(low, high))
            add_cond += 1
        if self.lon_range is not None:
            l, r = self.lon_range
            req += ' and ' if add_cond else ' where '
            req += ('station_longitude>{} and '
                    'station_longitude<{}'.format(l, r))
            add_cond += 1
        if self.lat_range is not None:
            s, n = self.lat_range
            req += ' and ' if add_cond else ' where '
            req += ('station_latitude>{} and '
                    'station_latitude<{}'.format(s, n))
            add_cond += 1
        if self.instrument_types is not None:
            req += ' and ' if add_cond else ' where '
            req += 'instr_type in {}'.format(conv(self.instrument_types))
            add_cond += 1
        # add constraints from variable table
        if self.variables is not None:
            req += ' and ' if add_cond else ' where '
            req += 'comp_name in {}'.format(conv(self.variables))
            add_cond += 1
        if self.stop_date is not None:
            req += ' and ' if add_cond else ' where '
            req += 'first_end < \'{}\''.format(self.stop_date)
            add_cond += 1
        if self.start_date is not None:
            req += ' and ' if add_cond else ' where '
            req += 'last_start > \'{}\''.format(self.start_date)
            add_cond += 1
        
        if self.matrices is not None:
            req += ' and ' if add_cond else ' where '
            req += 'matrix in '.format(conv(self.matrices))
            add_cond += 1  
        if self.statistics is not None:
            req += ' and ' if add_cond else ' where '
            req += 'statistics in '.format(conv(self.statistics))
            add_cond += 1      
        return (req + ";")

    def __getattr__(self, key):
        return self[key]
    
    def __setattr__(self, key, val):
        self[key] = val
    
    def __str__(self):
        s=""
        for k, v in self.items():
            s += "{}: {}\n".format(k, v)
        return s
        
        
class EbasFileIndex(object):
    """EBAS SQLite I/O interface
    
    Takes care of connection to database and execution of requests
    """
    def __init__(self, database=None):
        if database is None:
            database = const.EBAS_SQLITE_DATABASE
        if not os.path.exists(database):
            raise IOError("SQLite database file does not exist")
        self.database = database
        
    def contains_variables(self, request):
        """List all variables contained in request
        
        Parameters
        ----------
        request : EbasSQLRequest
            request class
            
        Returns
        -------
        list 
            list containing result
        """
        return self.execute_request(request.make_query_str(what="comp_name"))
    
    def contains_matrices(self, request):
        """List all matrices that are contained in request
        
        Parameters
        ----------
        request : EbasSQLRequest
            request class
            
        Returns
        -------
        list 
            list containing result
        """
        return self.execute_request(request.make_query_str(what="matrix"))
    
    def contains_coordinates(self, request):
        """List all station coordinates (lon, lat) that are contained in request
        
        Parameters
        ----------
        request : EbasSQLRequest
            request class
            
        Returns
        -------
        list 
            list containing result
        """
        that = "station_longitude, station_latitude"
        return self.execute_request(request.make_query_str(what=that))
    
    def contains_altitudes(self, request):
        """List altitudes of stations contained in request
        
        Parameters
        ----------
        request : EbasSQLRequest
            request class
            
        Returns
        -------
        list 
            list containing result
        """
        return self.execute_request(request.make_query_str(what="station_altitude"))
    
    def contains_station_names(self, request):
        """List all station_names that are contained in request
        
        Parameters
        ----------
        request : EbasSQLRequest
            request class
            
        Returns
        -------
        list 
            list containing result
        """
        return self.execute_request(request.make_query_str(what='station_name'))
        
    def execute_request(self, request):
        """Connect to database and retrieve data for input request
        
        Parameters
        ----------
        request : :obj:`EbasSQLRequest` or :obj:`str`
            request specifications
        """
        if isinstance(request, EbasSQLRequest):
            request = request.make_query_str()
        if not isinstance(request, str):
            raise IOError("Invalid input: Need instance of class "
                          "EbasSQLRequest or SQL request string for query")
        try:
            con = sqlite3.connect(self.database)
            cur = con.cursor()
            cur.execute(request)
            #return [f[0] for f in cur.fetchall()]
            return [f for f in cur.fetchall()]
        except sqlite3.Error as e:
            if con:
                con.rollback()
                
            print("Error: {}".format(repr(e)))
            sys.exit(1)
        finally:
            if con:
                con.close() 
                
            
if __name__=="__main__":
    dbfile = const.EBAS_SQLITE_DATABASE
    
    db = EbasFileIndex(dbfile)
    
    req = EbasSQLRequest(variables=('aerosol_optical_depth',
                                    'aerosol_light_scattering_coefficient',
                                    'aerosol_light_backscattering_coefficient',
                                    'aerosol_optical_depth'),
                        start_date="2010-01-01", 
                        stop_date="2010-07-01")
    
    files = db.execute_request(req.make_query_str())
    
    req.update(lat_range=(80, 90))
        
    files_arctic = db.execute_request(req)
    
    print(len(files), len(files_arctic))
    
    variables = db.contains_variables(req)
    coords = db.contains_coordinates(req)
    
    
    
    
    
    
    
    