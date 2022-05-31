import numpy as np

from pyaerocom import region
from pyaerocom.config import ALL_REGION_NAME


class Filter:
    """Class that can be used to filter gridded and ungridded data objects

    Note
    ----
    - BETA version (currently being tested)
    - Can only filter spatially
    - Might be renamed to RegionFilter at some point in the future

    Todo
    ----
    Include also temporal filtering and other filter options (e.g. variable,
    etc.)
    """

    #: dictionary specifying altitude filters
    ALTITUDE_FILTERS = {
        "wMOUNTAINS": None,  # reserve namespace for
        "noMOUNTAINS": [-1e6, 1e3],
    }  # 1000 m upper limit

    LAND_OCN_FILTERS = ["LAND", "OCN"]  # these are HTAP filters

    NO_REGION_FILTER_NAME = ALL_REGION_NAME
    NO_ALTITUDE_FILTER_NAME = "wMOUNTAINS"

    _DELIM = "-"

    def __init__(self, name=None, region=None, altitude_filter=None, land_ocn=None, **kwargs):
        # default name (i.e. corresponds to no filtering)
        self._name = None

        # this will be used to store instance of Region associated with filter
        self._region = None
        if name is not None:
            self.name = name
        else:
            self.name = f"{self.NO_REGION_FILTER_NAME}-{self.NO_ALTITUDE_FILTER_NAME}"

    @property
    def name(self):
        """Name of filter

        String containing up to 3 substrings (delimited using dash -)
        containing: <region_id>-<altitude_filter>-<land_or_sea_only_info>
        """
        return self._name

    @name.setter
    def name(self, val):
        self._name = self._check_name_valid(val)

    def _check_name_valid(self, val):
        if not isinstance(val, list):
            if not isinstance(val, str):
                raise ValueError(f"Need list or string as input for name attr got {val}")
            spl = val.split(self._DELIM)
        else:
            spl = val
        # make sure there are no duplicate strings in the name
        spl = list(np.unique(spl))
        if len(spl) > 3:
            raise ValueError("Filter name must not exceed 3 specifications")
        reg = None
        alt_filter = None
        landsea = None
        for entry in spl:
            if entry in self.valid_regions:
                if entry in self.LAND_OCN_FILTERS:
                    if landsea is not None:
                        raise ValueError("Filter name must only contain one landsea specification")
                    landsea = entry
                else:
                    if reg is not None:
                        raise ValueError("Only one region may be specified")
                    reg = entry

            elif entry in self.valid_alt_filter_codes:
                if alt_filter is not None:
                    raise ValueError("Only one altitude filter can be specified")
                alt_filter = entry
            else:
                raise ValueError(f"Invalid input for filter name {entry}")
        if reg is None:
            reg = ALL_REGION_NAME
        if alt_filter is None:
            alt_filter = "wMOUNTAINS"

        lst = [reg, alt_filter]
        if landsea is not None:
            lst.append(landsea)
        return f"{self._DELIM}".join(lst)

    @property
    def spl(self):
        return self._name.split(self._DELIM)

    @property
    def region_name(self):
        """Name of region"""
        return self.spl[0]

    @property
    def region(self):
        """Region associated with this filter (instance of :class:`Region`)"""
        r = self._region
        if not isinstance(r, region.Region) or not r.name == self.region_name:
            self._region = region.Region(self.region_name)
        return self._region

    @property
    def lon_range(self):
        """Longitude range of region"""
        return self.region.lon_range

    @property
    def lat_range(self):
        """Latitude range of region"""
        return self.region.lat_range

    @property
    def alt_range(self):
        """Altitude range of filter"""
        return self.ALTITUDE_FILTERS[self.spl[1]]

    def from_list(self, lst):
        """Set filter name based on input list"""
        if not isinstance(lst, list):
            raise TypeError("Invalid input, need list...")
        if len(lst) > 3:
            raise ValueError(
                f"Maximum length 3 of individual filter entries exceeded for input {lst}"
            )
        self.name = "-".join(lst)

    @property
    def valid_alt_filter_codes(self):
        """Valid codes for altitude filters"""
        return list(self.ALTITUDE_FILTERS)

    @property
    def valid_land_sea_filter_codes(self):
        """Codes specifying land/sea filters"""
        return self.LAND_OCN_FILTERS

    @property
    def valid_regions(self):
        """Names of valid regions (AeroCom regions and HTAP regions)"""
        return region.all()

    @property
    def land_ocn(self):
        return None if len(self.spl) < 3 else self.spl[2]

    def to_dict(self):
        """Convert filter to dictionary"""
        return {
            "region": self.region_name,
            "lon_range": self.lon_range,
            "lat_range": self.lat_range,
            "alt_range": self.alt_range,
            "land_sea": self.land_ocn,
        }

    def apply(self, data_obj):
        """Apply filter to data object

        Parameters
        ----------
        data_obj : :obj:`UngriddedData`, :obj:`GriddedData`
            input data object that is supposed to be filtered

        Returns
        -------
        :obj:`UngriddedData`, :obj:`GriddedData`
            filtered data object

        Raises
        ------
        IOError
            if input is invalid
        """
        spl = self.spl

        if spl[0] != self.NO_REGION_FILTER_NAME:
            data_obj = data_obj.filter_region(spl[0])
        if spl[1] != self.NO_ALTITUDE_FILTER_NAME:
            alt_range = self.ALTITUDE_FILTERS[spl[1]]
            data_obj = data_obj.filter_altitude(alt_range)
        if len(spl) > 2:
            data_obj = data_obj.filter_region(spl[2])
        return data_obj

    def __call__(self, data_obj):
        return self.apply(data_obj)
