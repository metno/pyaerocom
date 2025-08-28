import numpy as np
import logging
from copy import deepcopy
import iris

from .griddeddata import GriddedData
from pyaerocom.stationdata import StationData
from pyaerocom.exceptions import DataCoverageError

from pyaerocom.io.gridded_reader import GriddedReader


logger = logging.getLogger(__name__)


class GriddedDataContainerException(Exception):
    pass


class GriddedDataContainer:
    def __init__(self, data_id: str, data: GriddedData | None = None):
        """
        Class for holding and working with multiple GriddedData objects.



        """
        self.data_id = data_id

        self.children: list[GriddedData] = []

        self.ndim = None

        self.from_files = []

        self.start = None
        self.stop = None

        self.proj_info = None

        self.units = None
        self.var_name = None
        self.ts_type = None

        # self.latlon_info = {}

        self._lon_res = None
        self._lat_res = None

        self._lat_points = None
        self._lon_points = None

        if data is not None:
            self.add_griddeddata(data)

    def _initiate(self, data: GriddedData):
        """
        Starts the list of children, and defines all the important attributes for objects

        Parameters
        ----------

        data: GriddedData
        """
        self.proj_info = deepcopy(data.proj_info)
        self.start = data.start
        self.stop = data.stop

        self.var_name = data.var_name
        self.ts_type = data.ts_type
        self.units = data.units

        self.ndim = data.ndim

        # self.latlon_info = self._get_latlon_info(data)

        # self._lat_res = data.lat_res
        # self._lon_res = data.lon_res

        try:
            self._lat_points = data.latitude.points
        except Exception:
            self._lat_points = None
            assert self.proj_info is not None

        try:
            self._lon_points = data.longitude.points
        except Exception:
            self._lon_points = None
            assert self.proj_info is not None

    def only_one_child(func):
        def check_child(self, *args, **kwargs):
            if len(self.children) > 1:
                raise NotImplementedError(
                    f"{func.__name__} is not implemented for cases with more than one child GriddedData"
                )
            else:
                return func(self, *args, **kwargs)

        return check_child

    def add_griddeddata(self, data: GriddedData):
        """
        Adds a new GriddedData to children after checking if this new GriddedData object is
        compatible with existing children

        Parameters
        ----------
        data: GriddedData

        Raises
        -------
        GriddedDataContainerException
            If proj_info, var_name, ts_type, units or ndims are different from the existing ones

        """
        if len(self.children) == 0:
            self._initiate(data)

        if type(data.proj_info) is not type(self.proj_info):
            raise GriddedDataContainerException(
                f"Proj info from added griddeddata and existing proj info do not have the same type: {type(data.proj_info), {type(self.proj_info)}}"
            )
        if data.proj_info is not None and self.proj_info is not None:
            if data.proj_info != self.proj_info:
                raise GriddedDataContainerException(
                    "Proj data of added griddeddata is different from the existing proj info"
                )

        if data.var_name != self.var_name:
            raise GriddedDataContainerException(
                f"var_name of added griddeddata {data.var_name} is different from the existing var name {self.var_name}"
            )

        if data.ts_type != self.ts_type:
            raise GriddedDataContainerException(
                f"ts_type of added griddeddata {data.ts_type} is different from the existing ts_type {self.ts_type}"
            )

        if data.units != self.units:
            raise GriddedDataContainerException(
                f"units of added griddeddata {data.units} is different from the existing units {self.units}"
            )

        if data.ndim != self.ndim:
            raise GriddedDataContainerException(
                f"ndim of added griddeddata {data.ndim} is different from the existing ndim {self.ndim}"
            )

        # if self.lat_res != data.lat_res or self.lon_res != data.lon_res:
        #     raise GriddedDataContainerException(
        #         f"lat_res/lon_res of added griddeddata {data.lat_res}/{data.lon_res} is different from the existing lat_res/lon_res {self.lat_res}/{self.lon_res}"
        #     )

        # new_latlon_info = self._get_latlon_info(data)
        # if new_latlon_info != self.latlon_info:
        #    raise GriddedDataContainerException(
        #        f"information of lat and lon of added griddeddata {new_latlon_info} is different from the existing lat and lon {self.latlon_info}"
        #    )

        self.start = min(self.start, data.start)
        self.stop = max(self.stop, data.stop)

        self.from_files += data.from_files

        self.children.append(data)

    def read_data(
        self,
        readers: list[GriddedReader],
        var_name: str,
        start: str,
        stop: str,
        ts_type: str,
        vert_which: str,
        flex_ts_type: str,
        **kwargs,
    ) -> None:
        for reader in readers:
            # try:
            data = reader.read_var(
                var_name,
                start=start,
                stop=stop,
                ts_type=ts_type,
                vert_which=vert_which,
                flex_ts_type=flex_ts_type,
                **kwargs,
            )
            # except Exception:
            #    continue

            self.add_griddeddata(data)

    # def _get_latlon_info(self, data: GriddedData) -> dict:
    #    return {
    #        "latitude": {
    #            "standard_name": data.latitude.standard_name
    #            if data.latitude.standard_name is not None
    #            else "latitude",
    #            "units": str(data.latatitude.units),
    #        },
    #        "longitude": {
    #            "standard_name": data.longitude.standard_name
    #            if data.longitude.standard_name is not None
    #            else "longitude",
    #            "units": str(data.longitude.units),
    #        },
    #    }

    def get_xyranges(self) -> tuple[list[tuple[float, float]]]:
        """
        Finds the max/min ranges for x and y of all children


        Returns
        -------
        tuple[list[tuple[float, float]]]
            Two list, one for xs and one for ys

        Raises
        --------
        GriddedDataContainerException
            If self has no proj_info
        ValueError
            If there is a child where x or y is not found

        """
        if self.proj_info is None:
            raise GriddedDataContainerException("X and Y cannot be found, since proj_info is None")

        xranges = []
        yranges = []
        for data in self.children:
            xrange = None
            yrange = None
            for coord in data.cube.dim_coords:
                if coord.var_name == data.proj_info.x_axis:
                    vals = coord.points
                    xrange = (np.min(vals), np.max(vals))
                if coord.var_name == data.proj_info.y_axis:
                    vals = coord.points
                    yrange = (np.min(vals), np.max(vals))
            if xrange is None or yrange is None:
                raise ValueError(
                    f"x/y axis not found in cube: {data.proj_info.x_axis}, {data.proj_info.y_axis}"
                )
            xranges.append(xrange)
            yranges.append(yrange)
        return xranges, yranges

    # def get_latlon_ranges(self) -> tuple[list[tuple[float, float]]]:
    #    """
    #    Finds the max/min ranges for lat and lon of all children
    #
    #
    #    Returns
    #    -------
    #    tuple[list[tuple[float, float]]]
    #        Two list, one for lats and one for lons
    #
    #    Raises
    #    --------
    #    GriddedDataContainerException
    #        If no lats or no lons are found
    #    """
    #    lats = []
    #    lons = []
    #
    #    for data in self.children:
    #        latitude = data.latitude.points
    #        longitude = data.longitude.points
    #        lat_range = (np.min(latitude), np.max(latitude))
    #        lon_range = (np.min(longitude), np.max(longitude))
    #
    #        lats.append(lat_range)
    #        lons.append(lon_range)
    #
    #    if len(lats) == 0 or len(lons) == 0:
    #        raise GriddedDataContainerException("Failed to find lat or lon ranges")
    #
    #    return lats, lons

    @property
    @only_one_child
    def lat_res(self):
        return self.children[0].lat_res

    @property
    @only_one_child
    def lon_res(self):
        return self.children[0].lon_res

    @property
    @only_one_child
    def latitude_points(self):
        return self._lat_points

    @property
    @only_one_child
    def longitude_points(self):
        return self._lon_points

    @property
    def longitude_circular(self):
        return all([data.longitude.circular for data in self.children])

    @property
    def latitude_circular(self):
        return all([data.latitude.circular for data in self.children])

    @only_one_child
    def get_cube_data(self):
        return self.children[0].cube.data

    def get_cube_data_all(self) -> list:
        return [data.cube.data for data in self.children]

    # Methods which are simply applied to each of the children

    # TODO: Make sure that in the children loop, obj.children[i] is updated in the loops below (eventhough the inplace should be working)

    @property
    def time(self):
        if len(self.children) > 1:
            logger.warning("Be careful with using this function with more than one child")
            points = []
            metadata = self.children[0].time.metadata
            units = self.children[0].time.units
            for data in self.children:
                if metadata != data.time.metadata:
                    raise GriddedDataContainerException(
                        "Time from different children has different metadata"
                    )
                if units != data.time.units:
                    raise GriddedDataContainerException(
                        "Time from different children has different units"
                    )
                points += list(data.time.points)

            return iris.coords.DimCoord(np.array(points), var_name="time", **units, **metadata)

        return self.children[0].time

    @property
    def has_latlon_dims(self):
        return all([data.has_latlon_dims for data in self.children])

    @property
    @only_one_child
    def grid(self):
        return self.children[0].grid

    @property
    def data_revision(self):
        revision = ""
        for i, data in enumerate(self.children):
            revision += f"nr {i}: {data.data_revision}; "
        return revision

    def time_stamps(self):
        time_stamps = []
        for data in self.children:
            time_stamps += list(data.time_stamps())

        return np.sort(np.unique(np.array(time_stamps)))

    def _check_lonlat_bounds(self):
        for data in self.children:
            data._check_lonlat_bounds()

    def check_lon_circular(self):
        return all([data.check_lon_circular() for data in self.children])

    def extract_surface_level(self):
        """Extract surface level from 4D field"""
        return self.children[0].extract_surface_level()

    def to_time_series(
        self,
        sample_points=None,
        scheme="nearest",
        vert_scheme=None,
        add_meta=None,
        use_iris=False,
        **coords,
    ) -> list[StationData]:
        """Extract time-series for provided input coordinates (lon, lat)

        Tries to apply to_time_series on all children, then makes list of all returned stations data.

        See function in GriddedData for more info


        Parameters
        ----------
        sample_points : list
            coordinates (e.g. lon / lat) at which time series is supposed to be
            retrieved
        scheme : str or iris interpolator object
            interpolation scheme (for details, see :func:`interpolate`)
        vert_scheme : str
            string specifying how to treat vertical coordinates. This is only
            relevant for data that contains vertical levels. It will be ignored
            otherwise. Note that if the input coordinate specifications contain
            altitude information, this parameter will be set automatically to
            'altitude'. Allowed inputs are all data collapse schemes that
            are supported by :func:`pyaerocom.helpers.str_to_iris` (e.g. `mean,
            median, sum`). Further valid schemes are `altitude, surface,
            profile`.
            If not other specified and if `altitude` coordinates are provided
            via sample_points (or **coords parameters) then, vert_scheme will
            be set to `altitude`. Else, `profile` is used.
        add_meta : dict, optional
            dictionary specifying additional metadata for individual input
            coordinates. Keys are meta attribute names (e.g. station_name)
            and corresponding values are lists (with length of input coords)
            or single entries that are supposed to be assigned to each station.
            E.g. `add_meta=dict(station_name=[<list_of_station_names>])`).
        **coords
            additional keyword args that may be used to provide the interpolation
            coordinates (for details, see :func:`interpolate`)

        Returns
        -------
        list
            list of result dictionaries for each coordinate. Dictionary keys
            are: ``longitude, latitude, var_name``

        """
        sd_list = []
        for data in self.children:
            try:
                sd_list += data.to_time_series(
                    sample_points, scheme, vert_scheme, add_meta, use_iris, **coords
                )
            except DataCoverageError:
                print(f"Could not resample for grid from {data.from_files}")
                logger.info(f"Could not resample for grid from {data.from_files}")

        return sd_list

    def register_var_glob(self, delete_existing=True):  # pragma: no cover
        """
        Applies register_var_glob function to first child, and returns result.

        See GriddedData for more info on this function
        """
        return self.children[0].register_var_glob(delete_existing)

    def regrid(
        self, other=None, lat_res_deg=None, lon_res_deg=None, scheme="areaweighted", **kwargs
    ):
        """
        Applies regrid function to all children.

        See GriddedData for more info on this function
        """
        for i, data in enumerate(self.children):
            self.children[i] = data.regrid(other, lat_res_deg, lon_res_deg, scheme, **kwargs)

        return self

    def filter_region(self, region_id, inplace=False, **kwargs):  # pragma: no cover
        """
        Applies filter_region function to all children.

        See GriddedData for more info on this function
        """
        obj = self if inplace else self.copy()
        for i, data in enumerate(obj.children):
            obj.children[i] = data.filter_region(region_id, inplace, **kwargs)

        return obj

    def check_dimcoords_tseries(self):  # pragma: no cover
        """
        Applies check_dimcoords_tseries function to all children.

        See GriddedData for more info on this function
        """
        for data in self.children:
            data.check_dimcoords_tseries()

    def check_unit(self):  # pragma: no cover
        """
        Applies check_unit function to all children.

        See GriddedData for more info on this function
        """

        return all([data.check_unit() for data in self.children])
        for data in self.children:
            data.check_unit()

    def convert_unit(self, new_unit: str, inplace: bool = True):  # pragma: no cover
        """
        Applies convert_unit function to all children.

        See GriddedData for more info on this function
        """

        obj = self if inplace else self.copy()
        for i, data in enumerate(obj.children):
            obj.children[i] = data.convert_unit(
                new_unit,
            )

        return obj

    def remove_outliers(self, low, high, inplace=True):  # pragma: no cover
        """
        Applies remove_outliers function to all children.

        See GriddedData for more info on this function
        """
        obj = self if inplace else self.copy()
        for i, data in enumerate(obj.children):
            obj.children[i] = data.remove_outliers(low, high, inplace=True)
        return obj

    def reorder_dimensions_tseries(self):  # pragma: no cover
        """
        Applies reorder_dimensions_tseries function to all children.

        See GriddedData for more info on this function
        """
        for data in self.children:
            data.reorder_dimensions_tseries()

    def crop(
        self, lon_range=None, lat_range=None, time_range=None, region=None
    ):  # pragma: no cover
        """
        Applies crop function to all children, and return self.

        See GriddedData for more info on this function
        """
        for i, data in enumerate(self.children):
            self.children[i] = data.crop(lon_range, lat_range, time_range, region)

        return self

    def resample_time(
        self, to_ts_type, how=None, min_num_obs=None, use_iris=False
    ):  # pragma: no cover
        """
        Applies resample_time function to all children, and return self.

        See GriddedData for more info on this function
        """
        for i, data in enumerate(self.children):
            self.children[i] = data.resample_time(to_ts_type, how, min_num_obs, use_iris)

        return self

    def filter_altitude(self, alt_range=None):  # pragma: no cover
        """
        Applies filter_altitude function to all children, and return self.

        See GriddedData for more info on this function
        """
        logger.info(
            "Altitude filtering is not applied in GriddedDataContainer and will be skipped"
        )

        return self
