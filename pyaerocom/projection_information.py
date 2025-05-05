import xarray
from pyproj import CRS, transformer


class ProjectionInformationException(Exception):
    pass


class ProjectionInformation:
    def __init__(self):
        self._crs = None
        self._x_axis = None
        self._y_axis = None
        self._units = None

    @property
    def x_axis(self):
        return self._x_axis

    @property
    def y_axis(self):
        return self._y_axis

    def to_proj(self, latitude, longitude):
        """convert latitude and longitude to x and y

        :param latitude: latitude values
        :param longitude: longitude values
        :return: tuple of x and y coordinates
        """
        trans = transformer.Transformer.from_crs(4326, self._crs)
        return trans.transform(latitude, longitude)

    def to_latlon(self, x, y):
        """convert x and y to latitude and longitude

        :param x: x values
        :param y: y values
        :return: tuple of latitude and longitude coordinates
        """
        trans = transformer.Transformer.from_crs(self._crs, 4326)
        return trans.transform(x, y)

    @staticmethod
    def from_xarray(ds: xarray.Dataset, var: str):
        """initialize the ProjectionInformation from an xarray variable

        returns None if no projection exists for the variable or ProjectionInformation
        """
        da = ds[var]
        if "grid_mapping" not in da.attrs:
            return None
        pi = ProjectionInformation()
        grid_mapping = ds[da.attrs["grid_mapping"]]
        pi._crs = CRS.from_cf(grid_mapping.attrs)

        for c in da.coords:
            if len(da.coords[c].dims) != 1:
                continue
            if "standard_name" in da.coords[c].attrs:
                if da.coords[c].standard_name in (
                    "longitude",
                    "grid_longitude",
                    "projection_x_coordinate",
                ):
                    pi._x_axis = c
                    break
            if "axis" in da.coords[c].attrs:
                if da.coords[c].axis in ("x", "X"):
                    pi._x_axis = c
                    break
            units = ds.coords[c].attrs.get("units")
            if units in [
                "degrees_east",
                "degree_east",
                "degree_E",
                "degrees_E",
                "degreeE",
                "degreesE",
            ]:
                pi._x_axis = c
                break
        for c in da.coords:
            if len(da.coords[c].dims) != 1:
                continue
            if "standard_name" in da.coords[c].attrs:
                if da.coords[c].standard_name in (
                    "latitude",
                    "grid_latitude",
                    "projection_y_coordinate",
                ):
                    pi._y_axis = c
                    break
            if "axis" in da.coords[c].attrs:
                if da.coords[c].axis in ("y", "Y"):
                    pi._y_axis = c
                    break
            units = ds.coords[c].attrs.get("units")
            if units in [
                "degrees_north",
                "degree_north",
                "degree_N",
                "degrees_N",
                "degreeN",
                "degreesN",
            ]:
                pi._y_axis = c
                break
        if pi._x_axis is None or pi._y_axis is None:
            raise ProjectionInformationException(f"no x or y axis found for variable '{var}'")
        pi._units = da.coords[pi._y_axis].units
        return pi
