import numpy as np
import logging
from copy import deepcopy
import iris

from .griddeddata import GriddedData

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
            data = reader.read_var(
                var_name,
                start=start,
                stop=stop,
                ts_type=ts_type,
                vert_which=vert_which,
                flex_ts_type=flex_ts_type,
                **kwargs,
            )

            self.add_griddeddata(data)

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
            xrange, yrange = self._get_xyrange(data)
            if xrange is None or yrange is None:
                raise ValueError(
                    f"x/y axis not found in cube: {data.proj_info.x_axis}, {data.proj_info.y_axis}"
                )
            xranges.append(xrange)
            yranges.append(yrange)
        return xranges, yranges

    @staticmethod
    def _get_xyrange(child: GriddedData) -> tuple[tuple[float, float]] | tuple[None]:
        """
        Finds the range of the axis. Done by taking first and last point in each dimension.
        This might be the middle point of the bounding cells

        Parameters:
        child : GriddedData
            The GriddedData to find the ranges

        Returns:
        tuple[tuple[float, float]]
            Tuple of the ranges

        """
        xrange = None
        yrange = None
        for coord in child.cube.dim_coords:
            if coord.var_name == child.proj_info.x_axis:
                vals = coord.points
                xrange = (vals[0], vals[-1])

            if coord.var_name == child.proj_info.y_axis:
                vals = coord.points
                yrange = (vals[0], vals[-1])

        return xrange, yrange

    def get_tiles(
        self,
    ) -> tuple[list[GriddedData], list[tuple[float, float]], list[tuple[float, float]]]:
        """
        Makes a list of available tiles, and lists of x- and yranges for said tiles


        Returns:
        list[GriddedData]
            list of tiles

        tuple[tuple[float, float]]
            list of the xranges

        tuple[tuple[float, float]]
            list of the yranges

        """
        tiles = []
        xranges = []
        yranges = []
        for data in self.children:
            if self.proj_info is None:
                latitude = data.latitude.points
                longitude = data.longitude.points
                xrange = [np.min(longitude), np.max(longitude)]
                yrange = [np.min(latitude), np.max(latitude)]
            else:
                xrange, yrange = self._get_xyrange(data)

            if len(xrange) == 0 or len(yrange) == 0:
                logger.warning(f"Tile {data.from_files} with no x and y range found")
                continue

            tiles.append(data)
            xranges.append(xrange)
            yranges.append(yrange)

        if not (len(tiles) == len(xranges) and len(tiles) == len(yranges)):
            raise GriddedDataContainerException(
                "Something went wrong then getting tiles. Length of ranges were different"
            )
        return tiles, xranges, yranges

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
        return self.children[0].latitude.points

    @property
    @only_one_child
    def longitude_points(self):
        return self.children[0].longitude.points

    @property
    @only_one_child
    def altitude(self):
        return self.children[0].altitude

    @property
    @only_one_child
    def latitude(self):
        return self.children[0].latitude

    @property
    @only_one_child
    def longitude(self):
        return self.children[0].longitude

    @property
    @only_one_child
    def altitude_points(self):
        return self.children[0].altitude.points

    @property
    def longitude_circular(self):
        return all([data.longitude.circular for data in self.children])

    @property
    def latitude_circular(self):
        return all([data.latitude.circular for data in self.children])

    @only_one_child
    def get_cube_data(self):
        return self.children[0].cube.data

    @only_one_child
    def to_xarray(self):
        return self.children[0].to_xarray()

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
    def has_time_dim(self):
        return all([data.has_time_dim for data in self.children])

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

    # def to_time_series(
    #     self,
    #     sample_points=None,
    #     scheme="nearest",
    #     vert_scheme=None,
    #     add_meta=None,
    #     use_iris=False,
    #     **coords,
    # ) -> list[StationData]:
    #     raise NotImplementedError(
    #         "to_time_series is not implemented for this container, due to problems with sorting returned stationdata (compared with the stations datas of the obs)"
    #     )

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
        if self.proj_info is not None:
            raise GriddedDataContainerException(
                "Could not regrid, since the data is projected. Please use data with latlon instead"
            )
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

        self.ts_type = to_ts_type
        return self

    def filter_altitude(self, alt_range=None):  # pragma: no cover
        """
        Applies filter_altitude function to all children, and return self.

        See GriddedData for more info on this function
        """
        logger.warning(
            "Altitude filtering is not applied in GriddedDataContainer and will be skipped"
        )

        return self

    def extract(self, constraint, inplace=False):
        """Extract subset

        Parameters
        ----------
        constraint : iris.Constraint
            constraint that is to be applied

        Returns
        -------
        GriddedData
            new data object containing cropped data
        """

        obj = self if inplace else self.copy()
        for i, data in enumerate(obj.children):
            obj.children[i] = data.extract(constraint, inplace=False)
        return obj

    @only_one_child
    def to_time_series(
        self,
        sample_points=None,
        scheme="nearest",
        vert_scheme=None,
        add_meta=None,
        use_iris=False,
        **coords,
    ):
        return self.children[0].to_time_series(
            sample_points, scheme, vert_scheme, add_meta, use_iris, **coords
        )

    def collapsed(self, coords, aggregator, **kwargs):
        obj = self.copy()
        for i, data in enumerate(obj.children):
            obj.children[i] = data.collapsed(coords, aggregator, **kwargs)
        return obj

    def copy(self):
        return deepcopy(self)
