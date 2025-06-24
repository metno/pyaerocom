import numpy as np
import logging
from copy import deepcopy

from .griddeddata import GriddedData
from pyaerocom.stationdata import StationData
from iris.coords import DimCoord, AuxCoord
from pyaerocom.exceptions import DataCoverageError


logger = logging.getLogger(__name__)


class MultiGriddedDataException(Exception):
    pass


class MultiGriddedData:
    def __init__(self, data_id: str):
        self.children: list[GriddedData] = []
        self.lat_map: dict[tuple[float, float], int] = {}
        self.lon_map: dict[tuple[float, float], int] = {}

        self.data_id = data_id

        self.ndim = None

        self.latitude: DimCoord | AuxCoord | None = None
        self.longitude: DimCoord | AuxCoord | None = None

        self.from_files = []

        self.start = None
        self.stop = None

        self.proj_info = None
        self.base_year = None
        self.units = None
        self.var_name = None
        self.ts_type = None

    def _initiate(self, data: GriddedData):
        self.proj_info = deepcopy(data.proj_info)
        self.start = data.start
        self.stop = data.stop

        self.var_name = data.var_name
        self.ts_type = data.ts_type
        self.units = data.units

        self.ndim = data.ndim
        self.ts_type = data.ts_type

        self.latitude = data.latitude[:]
        self.longitude = data.longitude[:]

        self.xranges = []
        self.yranges = []

        # self.base_year = data.base_year

    def add_griddeddata(self, data: GriddedData):
        if len(self.children) == 0:
            self._initiate(data)

        if data.proj_info != self.proj_info:
            raise MultiGriddedDataException(
                "Proj data of added griddeddata is different from the existing proj info"
            )

        if data.var_name != self.var_name:
            raise MultiGriddedDataException(
                f"Var name of added griddeddata {data.var_name} is different from the existing var name {self.var_name}"
            )

        if data.ts_type != self.ts_type:
            raise MultiGriddedDataException(
                f"ts_type of added griddeddata {data.ts_type} is different from the existing ts_type {self.ts_type}"
            )

        if data.units != self.units:
            raise MultiGriddedDataException(
                f"units of added griddeddata {data.units} is different from the existing units {self.units}"
            )

        if data.ndim != self.ndim:
            raise MultiGriddedDataException(
                f"ndim of added griddeddata {data.ndim} is different from the existing ndim {self.ndim}"
            )

        self.start = min(self.start, data.start)
        self.stop = max(self.stop, data.stop)

        # self.longitude = self._add_coord(self.longitude, data.longitude)
        # self.latitude = self._add_coord(self.latitude, data.latitude)

        # self.base_year = min(self.base_year, data.base_year)

        self.from_files += data.from_files

        self.children.append(data)

    def _add_coord(
        self, old_dim: DimCoord | AuxCoord, new_dim: DimCoord | AuxCoord
    ) -> DimCoord | AuxCoord:
        points = np.concatenate((old_dim.points, new_dim.points))

        if type(new_dim) is not type(new_dim):
            raise MultiGriddedDataException("New dim was not of the same type as old dim")
        if isinstance(old_dim, AuxCoord):
            return_dim = AuxCoord
        else:
            return_dim = DimCoord

        return return_dim(
            points,
            standard_name=old_dim.standard_name,
            long_name=old_dim.long_name,
            var_name=old_dim.var_name,
            units=old_dim.units,
            bounds=old_dim.bounds,
            attributes=old_dim.attributes,
            coord_system=old_dim.coord_system,
        )

    def get_min_max_x_y(self) -> tuple[list[float, float]] | None:
        if self.proj_info is None:
            return None

        x = []
        y = []
        for data in self.children:
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
            if len(x) == 0:
                x = xrange[:]
                y = yrange[:]
            else:
                new_x = [np.min([x[0], xrange[0]]), np.max([x[1], xrange[1]])]
                new_y = [np.min([y[0], yrange[0]]), np.max([y[1], yrange[1]])]

                x = new_x[:]
                y = new_y[:]

        return x, y

    def get_xyranges(self) -> tuple[list[tuple[float, float]]] | None:
        if self.proj_info is None:
            return None

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

    def check_dimcoords_tseries(self):
        for data in self.children:
            data.check_dimcoords_tseries()

    def reorder_dimensions_tseries(self):
        for data in self.children:
            data.check_dimcoords_tseries()

    def crop(self, lon_range=None, lat_range=None, time_range=None, region=None):
        for data in self.children:
            data.crop(lon_range, lat_range, time_range, region)

        return self

    def resample_time(self, to_ts_type, how=None, min_num_obs=None, use_iris=False):
        for data in self.children:
            data.resample_time(to_ts_type, how, min_num_obs, use_iris)

        return self

    def to_time_series(
        self,
        sample_points=None,
        scheme="nearest",
        vert_scheme=None,
        add_meta=None,
        use_iris=False,
        **coords,
    ) -> list[StationData]:
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

    def register_var_glob(self, delete_existing=True):
        return self.children[0].register_var_glob(delete_existing)

    def regrid(
        self, other=None, lat_res_deg=None, lon_res_deg=None, scheme="areaweighted", **kwargs
    ):
        for data in self.children:
            data.regrid(other, lat_res_deg, lon_res_deg, scheme, **kwargs)

    def filter_region(self, region_id, inplace=False, **kwargs):
        for data in self.children:
            data.filter_region(region_id, inplace, **kwargs)
