#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Low level classes and methods for io
"""
from collections import OrderedDict as od
from os.path import join, exists, basename, splitext
from pyaerocom import const
from pyaerocom.tstype import TsType
from pyaerocom.exceptions import FileConventionError
from configparser import ConfigParser

class FileConventionRead(object):
    """Class that represents a file naming convention for reading Aerocom files

    Attributes
    ----------
    name : str
        name of this convention (e.g. "aerocom3")
    file_sep : str
        filename delimiter for accessing different variables
    year_pos : int
        position of year information in filename after splitting using
        delimiter :attr:`file_sep`
    var_pos : int
        position of variable information in filename after splitting using
        delimiter :attr:`file_sep`
    ts_pos : int
        position of information of temporal resolution in filename after
        splitting using delimiter :attr:`file_sep`
    vert_pos : int
        position of information about vertical resolution of data
    data_id_pos : int
        position of data ID
    """
    _io_opts = const
    AEROCOM3_VERT_INFO = {'2d'  : ['surface', 'column', 'modellevel'],
                          '3d'  : ['modellevelatstations']}

    def __init__(self, name="aerocom3", file_sep="_", year_pos=None,
                 var_pos=None, ts_pos=None, vert_pos=None, data_id_pos=None,
                 from_file=None):

        self.name = name
        self.file_sep = file_sep

        self.year_pos = year_pos
        self.var_pos = var_pos
        self.ts_pos = ts_pos
        self.vert_pos = vert_pos
        self.data_id_pos = data_id_pos

        if from_file is not None:
            self.from_file(from_file)
        else:
            try:
                self.import_default(self.name)
            except Exception:
                pass

    @property
    def info_init(self):
        """Empty dictionary containing init values of infos to be
        extracted from filenames
        """
        return od(year=None, var_name=None, ts_type=None, vert_code='',
                  is_at_stations=False, data_id='')

    def from_file(self, file):
        """Identify convention from a file

        Currently only two conventions (aerocom2 and aerocom3) exist that are
        identified by the delimiter used.

        Parameters
        ----------
        file : str
            file path or file name

        Returns
        -------
        FileConventionRead
            this object (with updated convention)

        Raises
        ------
        FileConventionError
            if convention cannot be identified

        Example
        -------
        >>> from pyaerocom.io import FileConventionRead
        >>> filename = 'aerocom3_CAM5.3-Oslo_AP3-CTRL2016-PD_od550aer_Column_2010_monthly.nc'
        >>> print(FileConventionRead().from_file(filename))
        pyaeorocom FileConventionRead
        name: aerocom3
        file_sep: _
        year_pos: -2
        var_pos: -4
        ts_pos: -1
        """

        if basename(file).count("_") >= 4:
            self.import_default("aerocom3")
        elif basename(file).count(".") >= 4:
            self.import_default("aerocom2")
        else:
            raise FileConventionError('Could not identify convention from '
                                      'input file {}'.format(basename(file)))
        self.check_validity(file)
        return self

    def check_validity(self, file):
        """Check if filename is valid"""
        info = self.get_info_from_file(file)
        year = info["year"]
        if not TsType.valid(info['ts_type']):
            raise FileConventionError("Invalid ts_type %s in filename %s"
                                           %(info['ts_type'], basename(file)))
        elif not (const.MIN_YEAR <= year <= const.MAX_YEAR):
            raise FileConventionError("Invalid year %d in filename %s"
                          %(info['year'], basename(file)))

    def _info_from_aerocom3(self, file):
        """Extract info from filename Aerocom 3 convention

        Parameters
        -----------
        file : str
            netcdf file name

        Returns
        -------
        dict
            dictionary containing infos that were extracted from filename
        """
        # init result dictionary
        info = self.info_init

        spl = splitext(basename(file))[0].split(self.file_sep)
        # phase 3 file naming convention
        try:
            info["year"] = int(spl[self.year_pos])
        except Exception:
            msg = ("Failed to extract year information from file {} "
                   "using file convention Aerocom 3".format(basename(file),
                                                            self.name))
            raise FileConventionError(msg)
        try:
            # include vars for the surface
            if spl[self.vert_pos].lower() in self.AEROCOM3_VERT_INFO['2d']:
                info["var_name"] = spl[self.var_pos]
            # also include 3d vars that provide station based data
            # and contain the string vmr in this case the variable name has to
            # be slightly changed to the  aerocom phase 2 naming
            elif spl[self.vert_pos].lower() in self.AEROCOM3_VERT_INFO['3d']:
                if 'vmr' in spl[self.var_pos]:
                    info['var_name'] = spl[self.var_pos].replace('vmr', 'vmr3d')
                else:
                    info['var_name'] = spl[self.var_pos]
            else:
                raise FileConventionError('Invalid file name (Aerocom 3 '
                                          'naming convention).\n'
                                          '{}\nInvalid string identifier for '
                                          'vertical coordinate: {}'
                                          .format(file, spl[self.vert_pos]))
        except Exception as e:
            raise FileConventionError('Failed to extract variable name from '
                                      'file {} using file convention {}.\n'
                                      'Error: {}'.format(basename(file),
                                                         self.name, repr(e)))
        try:
            info["ts_type"] = spl[self.ts_pos]
        except Exception:
            raise FileConventionError('Failed to extract ts_type from '
                                      'file {} using file convention {}'
                                      .format(basename(file), self.name))
        try:
            info["vert_code"] = spl[self.vert_pos]
        except Exception:
            raise FileConventionError('Failed to extract vert_code from '
                                      'file {} using file convention {}'
                                      .format(basename(file), self.name))

        try:
            info["data_id"] = self.file_sep.join(spl[self.data_id_pos:self.var_pos])
        except Exception:
            raise FileConventionError('Failed to extract model name from '
                                      'file {} using file convention {}'
                                      .format(basename(file), self.name))
        if'atstations' in file.lower():
            info['is_at_stations'] = True
        return info

    def _info_from_aerocom2(self, file):
        """Extract info from filename Aerocom 2 convention

        Parameters
        -----------
        file : str
            netcdf file name

        Returns
        -------
        dict
            dictionary containing infos that were extracted from filename
        """
        info = self.info_init
        if self.file_sep == ".":
            spl = basename(file).split(self.file_sep)
        else:
            spl = splitext(basename(file))[0].split(self.file_sep)
        try:
            info["year"] = int(spl[self.year_pos])
        except Exception:
            raise FileConventionError('Failed to extract year information '
                                      'from file {} using file '
                                      'convention {}'
                                      .format(basename(file), self.name))
        try:
            info["var_name"] = spl[self.var_pos]
        except Exception:
            raise FileConventionError('Failed to extract variable information '
                                      'from file {} using file '
                                      'convention {}'
                                      .format(basename(file), self.name))
        try:
            info["ts_type"] = spl[self.ts_pos]
        except Exception:
            raise FileConventionError('Failed to extract ts_type '
                                      'from file {} using file '
                                      'convention {}'
                                      .format(basename(file), self.name))

        try:
            info['data_id'] = '.'.join(spl[self.data_id_pos:self.ts_pos])
        except Exception:
            raise FileConventionError('Failed to extract name '
                                      'from file {} using file '
                                      'convention {}'
                                      .format(basename(file), self.name))
        if 'atstations' in file.lower():
            raise Exception('Developers: please debug (file convention '
                            'Aerocom 2 should not have atstations '
                            'encoded in file name)')
        return info

    def get_info_from_file(self, file):
        """Identify convention from a file

        Currently only two conventions (aerocom2 and aerocom3) exist that are
        identified by the delimiter used.

        Parameters
        ----------
        file : str
            file path or file name

        Returns
        -------
        OrderedDict
            dictionary containing keys `year, var_name, ts_type` and
            corresponding variables, extracted from the filename

        Raises
        ------
        FileConventionError
            if convention cannot be identified

        Example
        -------
        >>> from pyaerocom.io import FileConventionRead
        >>> filename = 'aerocom3_CAM5.3-Oslo_AP3-CTRL2016-PD_od550aer_Column_2010_monthly.nc'
        >>> conv = FileConventionRead("aerocom3")
        >>> info = conv.get_info_from_file(filename)
        >>> for item in info.items(): print(item)
        ('year', 2010)
        ('var_name', 'od550aer')
        ('ts_type', 'monthly')
        """
        if self.name == 'aerocom3':
            return self._info_from_aerocom3(file)
        elif self.name == 'aerocom2':
            return self._info_from_aerocom2(file)

    def string_mask(self, data_id, var, year, ts_type, vert_which=None):
        """Returns mask that can be used to identify files of this convention

        Parameters
        ----------
        data_id : str
            experiment ID (e.g. GISS-MATRIX.A2.CTRL)
        var : str
            variable string ID (e.g. "od550aer")
        year : int
            desired year of observation (e.g. 2012)
        ts_type : str
            string specifying temporal resolution (e.g. "daily")

        Example
        -------

        import re
        conf_aero2 = FileConventionRead(name="aerocom2")
        conf_aero3 = FileConventionRead(name="aerocom2")

        var = od550aer
        year = 2012
        ts_type = "daily"

        match_str_aero2 = conf_aero2.string_mask(var, year, ts_type)

        match_str_aero3 = conf_aero3.string_mask(var, year, ts_type)

        """
        if ts_type is None:
            ts_type = '*'
        if self.name == "aerocom2":
            if vert_which is not None:
                raise FileConventionError('Specification of vert_which ({}) is '
                                          'not supported for '
                                          'aerocom2 naming convention'
                                          .format(vert_which))

            return ".".join(['.*', data_id, ts_type, var, str(year), 'nc'])
        elif self.name == "aerocom3":
            if vert_which is None:
                vert_which = '.*'
            return "_".join(['.*',  data_id, var, vert_which, str(year), ts_type]) + '.nc'
        else:
            raise NotImplementedError("File matching mask for convention %s "
                                      "not yet defined..." %self.name)

    def import_default(self, name):
        """Checks and load default information from database"""
        from pyaerocom import __dir__
        fpath = join(__dir__, "data", "file_conventions.ini")
        if not exists(fpath):
            raise IOError("File conventions ini file could not be found: %s"
                          %fpath)
        conf_reader = ConfigParser()
        conf_reader.read(fpath)
        if not name in conf_reader:
            raise NameError("No default available for %s" %name)
        self.name = name
        for key, val in conf_reader[name].items():
            if key in self.__dict__:
                try:
                    val = int(val)
                except Exception:
                    pass
                self.__dict__[key] = val

    def from_dict(self, new_vals):
        """Load info from dictionary

        Parameters
        ----------
        new_vals : dict
            dictionary containing information

        Returns
        -------
        self
        """
        for k, v in new_vals.items():
            if k in self.__dict__:
                self.__dict__[k] = v
        return self

    def to_dict(self):
        """Convert this object to ordered dictionary"""
        return od(name = self.name,
                  file_sep = self.file_sep,
                  year_pos = self.year_pos,
                  var_pos = self.var_pos,
                  ts_pos = self.ts_pos,
                  vert_pos = self.vert_pos,
                  data_id_pos = self.data_id_pos)

    def __repr__(self):
       return ("%s %s" %(self.name, super(FileConventionRead, self).__repr__()))

    def __str__(self):
        s = "\npyaeorocom FileConventionRead"
        for k, v in self.to_dict().items():
            s += "\n%s: %s" %(k, v)
        return s

if __name__=="__main__":
    conf = FileConventionRead()

    print(conf)

    d = od(name = "Fake",
           file_sep = 10,
           year_pos = -6,
           var_pos = 15,
           ts_pos = 3)
    print(conf.from_dict(d))
    try:
        conf.import_default("blaaa")
    except NameError:
        print("Works as expected")
    conf.import_default("aerocom3")
    print(conf)

    conf = FileConventionRead(name="aerocom2")
    print(conf)

    fname = 'aerocom3_TM5_AP3-INSITU_vmrch4_ModelLevelAtStations_2010_monthly.nc'

    print('\nFrom file: {}'.format(conf.from_file(fname)))
    print(conf.get_info_from_file(fname))

    ff = FileConventionRead(from_file='aerocom.CALIOP3.monthly.ec5323Ddust.2006.nc')
    print(ff)
