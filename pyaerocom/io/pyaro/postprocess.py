import dataclasses

from pyaro.timeseries import (
    Reader,
    Data,
)

from pyaerocom.units_helpers import get_unit_conversion_fac


@dataclasses.dataclass
class VariableScaling:
    REQ_VAR: str
    IN_UNIT: str
    OUT_UNIT: str
    SCALING_FACTOR: float
    OUT_VARNAME: str
    NOTE: str | None = None

    def required_input_variables(self) -> list[str]:
        return [self.REQ_VAR]

    def out_varname(self) -> str:
        return self.OUT_VARNAME


M_N = 14.006
M_O = 15.999
M_S = 32.065

TRANSFORMATIONS = {
    "concNno_from_concno": VariableScaling(
        REQ_VAR="concno",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug N m-3",
        SCALING_FACTOR=M_N / (M_N + M_O),
        OUT_VARNAME="concNno",
    ),
    "concNno2_from_concno2": VariableScaling(
        REQ_VAR="concno2",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug N m-3",
        SCALING_FACTOR=M_N / (M_N + 2 * M_O),
        OUT_VARNAME="concNno2",
    ),
    "concSso2_from_concso2": VariableScaling(
        REQ_VAR="concso2",
        IN_UNIT="ug m-3",
        OUT_UNIT="ug S m-3",
        SCALING_FACTOR=M_S / (M_S + 2 * M_O),
        OUT_VARNAME="concSso2",
    ),
    "vmro3_from_conco3": VariableScaling(
        REQ_VAR="conco3",
        IN_UNIT="µg m-3",
        OUT_UNIT="ppb",
        SCALING_FACTOR=0.5011,  # 20C and 1013 hPa
        OUT_VARNAME="vmro3",
        NOTE="The vmro3_from_conco3 transform is only valid at T=20C, p=1013hPa",
    ),
    "vmro3max_from_conco3": VariableScaling(  # Requires `resample_how`
        REQ_VAR="conco3",
        IN_UNIT="µg m-3",
        OUT_UNIT="ppb",
        SCALING_FACTOR=0.5011,  # 20C and 1013 hPa
        OUT_VARNAME="vmro3max",
        NOTE="The vmro3max_from_conco3 transform is only valid at T=20C, p=1013hPa, and the transform requires the use of resample_how to obtain the daily maximum",
    ),
}


class PostProcessingReaderData(Data):
    def __init__(self, data: Data, variable: str, units: str, scaling: float | None):
        self._variable = variable
        self._units = units
        self.data = data
        self.scaling = scaling

    def keys(self):
        return self.data.keys()

    def slice(self, index):
        return PostProcessingReaderData(
            self.data.slice(index),
            variable=self._variable,
            units=self._units,
            scaling=self.scaling,
        )

    def __len__(self):
        return self.data.__len__()

    @property
    def values(self):
        if self.scaling is None:
            return self.data.values
        else:
            return self.data.values * self.scaling

    @property
    def stations(self):
        return self.data.stations

    @property
    def latitudes(self):
        return self.data.latitudes

    @property
    def longitudes(self):
        return self.data.longitudes

    @property
    def altitudes(self):
        return self.data.altitudes

    @property
    def start_times(self):
        return self.data.start_times

    @property
    def end_times(self):
        return self.data.end_times

    @property
    def flags(self):
        return self.data.flags

    @property
    def standard_deviations(self):
        return self.data.standard_deviations


class PostProcessingReader(Reader):
    def __init__(
        self,
        reader: Reader,
        compute_vars: list[str] | None = None,
    ):
        self.reader = reader

        self.compute_vars = dict()
        if compute_vars is not None:
            known_variables = reader.variables()
            for compute_var in compute_vars:
                transform = TRANSFORMATIONS.get(compute_var)
                if transform is None:
                    raise Exception(f"Unknown transformation ({compute_var}) encountered")
                required_input = transform.required_input_variables()
                missing = set(required_input) - set(known_variables)
                if len(missing) > 0:
                    raise Exception(
                        f"The transformation {compute_var} requires variables which are not present, missing {missing}"
                    )
                self.compute_vars[transform.out_varname()] = transform

    def data(self, varname: str) -> Data:
        if varname not in self.compute_vars:
            data = self.reader.data(varname)
            return data
        else:
            transform = self.compute_vars[varname]
            if isinstance(transform, VariableScaling):
                data = self.reader.data(transform.REQ_VAR)
                scaling = transform.SCALING_FACTOR * get_unit_conversion_fac(
                    from_unit=data.units, to_unit=transform.IN_UNIT, var_name=transform.REQ_VAR
                )
                return PostProcessingReaderData(
                    data, variable=varname, units=transform.OUT_UNIT, scaling=scaling
                )
            else:
                raise Exception(
                    f"Unknown transform {transform} encountered for variable {varname}"
                )

    def variables(self) -> list[str]:
        variables = list()
        variables.extend(self.reader.variables())
        variables.extend(self.compute_vars.keys())
        return variables

    def stations(self):
        return self.reader.stations()

    def close(self) -> None:
        self.reader.close()
