import numpy as np
from cf_units import Unit

from pyaerocom.exceptions import UnitConversionError
from pyaerocom.helpers import isnumeric, resample_time_dataarray
from pyaerocom.time_config import SI_TO_TS_TYPE
from pyaerocom.tstype import TsType
from pyaerocom.units_helpers import get_unit_conversion_fac

# ToDo: check if still needed
DEP_IMPLICIT_UNITS = [Unit("mg N m-2"), Unit("mg S m-2"), Unit("mg m-2")]
PR_IMPLICIT_UNITS = [Unit("mm")]
DEP_TEST_UNIT = "kg m-2 s-1"


# ToDo: check if still needed
def translate_rate_units_implicit(unit_implicit, ts_type):
    unit = Unit(unit_implicit)

    freq = TsType(ts_type)
    freq_si = freq.to_si()

    # check if unit is explicitly defined as implicit and if yes add frequency
    # string
    if unit in DEP_IMPLICIT_UNITS:
        unit = f"{unit} {freq_si}-1"

    # Check if frequency in unit corresponds to sampling frequency (e.g.
    # ug m-2 h-1 for hourly data).
    freq_si_str = f"{freq_si}-1"
    freq_si_str_alt = f"/{freq_si}"
    if str(unit).endswith(freq_si_str_alt):
        # make sure frequency is denoted as e.g. m s-1 instead of m/s
        _new = str(unit).replace(freq_si_str_alt, freq_si_str)
        unit = Unit(_new)

    # for now, raise NotImplementedError if wdep unit is, e.g. ug m-2 s-1 but
    # ts_type is hourly (later, use units_helpers.implicit_to_explicit_rates)
    if freq_si_str not in str(unit):
        raise NotImplementedError(
            f"Cannot yet handle wdep in {unit} but {freq} sampling frequency"
        )
    return unit


def _check_unit_conversion_fac(unit, test_unit, non_si_info=None):  # pragma: no cover
    raise NotImplementedError("under revision")
    if non_si_info is None:
        non_si_info = []
    try:
        get_unit_conversion_fac(unit, DEP_TEST_UNIT)
        return True
    except UnitConversionError:
        for substr in non_si_info:
            if substr in unit:
                check = unit.replace(substr, "")
                return _check_unit_conversion_fac(check, test_unit)
    return False


# ToDo: check if still needed
def check_pr_units(gridded):  # pragma: no cover
    raise NotImplementedError("under revision")
    # ToDo: harmonise input and output with translate_rate_units_implicit
    unit = Unit(gridded.units)
    freq = TsType(gridded.ts_type)
    freq_si = freq.to_si()

    # check if precip unit is implicit
    if any([unit == x for x in PR_IMPLICIT_UNITS]):
        unit = f"{unit} {freq_si}-1"
        gridded.units = unit

    # Check if frequency in unit corresponds to sampling frequency (e.g.
    # ug m-2 h-1 for hourly data).
    freq_si_str = f" {freq_si}-1"
    freq_si_str_alt = f"/{freq_si}"
    if freq_si_str_alt in str(unit):
        # make sure frequencey is denoted as e.g. m s-1 instead of m/s
        unit = str(unit).replace(freq_si_str_alt, freq_si_str)

        gridded.units = unit

    # for now, raise NotImplementedError if wdep unit is, e.g. ug m-2 s-1 but
    # ts_type is hourly (later, use units_helpers.implicit_to_explicit_rates)
    if freq_si_str not in str(unit):
        raise NotImplementedError(
            f"Cannot yet handle wdep in {unit} but {freq} sampling frequency"
        )
    return gridded


# ToDo: check if still needed
def _check_prlim_units(prlim, prlim_units):  # pragma: no cover
    raise NotImplementedError("under revision")
    # ToDo: cumbersome for now, make it work first, then make it simpler...
    if not prlim_units.endswith("-1"):
        raise ValueError(
            "Please specify prlim_unit as string ending with -1 (e.g. mm h-1) or similar"
        )

    spl = prlim_units.split()
    if not len(spl) == 2:
        raise ValueError("Invalid input for prlim_units (only one whitespace is allowed)")
    # make sure to be in the correct length unit
    mulfac = get_unit_conversion_fac(spl[0], "m")
    prlim *= mulfac

    prlim_units = f"m {spl[1]}"
    prlim_freq = spl[1][:-2]  # it endswith -1
    # convert the freque
    if prlim_freq not in SI_TO_TS_TYPE:
        raise ValueError(
            f"frequency in prlim_units must be either of the "
            f"following values: {list(SI_TO_TS_TYPE)}."
        )

    prlim_tstype = TsType(SI_TO_TS_TYPE[prlim_freq])
    return (prlim, prlim_units, prlim_tstype)


# ToDo: check if still needed
def _apply_prlim_wdep(wdeparr, prarr, prlim, prlim_unit, prlim_set_under):  # pragma: no cover
    raise NotImplementedError("under revision")
    if prlim_unit is None:
        raise ValueError(f"Please provide prlim_unit for prlim={prlim}")
    elif prlim_set_under is None:
        raise ValueError(f"Please provide prlim_set_under for prlim={prlim}")
    elif not isnumeric(prlim_set_under):
        raise ValueError(
            f"Please provide a numerical value or np.nan for "
            f"prlim_set_under, got {prlim_set_under}"
        )

    prmask = prarr.data < prlim
    wdeparr.data[prmask] = prlim_set_under

    return wdeparr, prmask


# ToDo: check if still needed
def _aggregate_wdep_pr(
    wdeparr, prarr, wdep_unit, pr_unit, from_tstype, to_tstype
):  # pragma: no cover
    raise NotImplementedError("under revision")
    to_tstype_pd = to_tstype.to_pandas_freq()
    to_tstype_si = to_tstype.to_si()

    from_tstype_si = from_tstype.to_si()

    wdeparr = resample_time_dataarray(wdeparr, to_tstype_pd, how="sum")
    wdep_unit = wdep_unit.replace(f"{from_tstype_si}-1", f"{to_tstype_si}-1")
    prarr = resample_time_dataarray(prarr, to_tstype_pd, how="sum")
    pr_unit = pr_unit.replace(f"{from_tstype_si}-1", f"{to_tstype_si}-1")

    return (wdeparr, prarr, wdep_unit, pr_unit)


# ToDo: check if still needed
def compute_concprcp_from_pr_and_wetdep(
    wdep, pr, ts_type=None, prlim=None, prlim_units=None, prlim_set_under=None
):  # pragma: no cover
    raise NotImplementedError("under revision")
    if ts_type is None:
        ts_type = wdep.ts_type

    wdep_tstype = TsType(wdep.ts_type)

    # get units from deposition input and precipitation; sometimes, they are
    # defined implicit, e.g. mm for precipitation, which is then already
    # accumulated over the provided time resolution in the data, that is, if
    # the data is hourly and precip is in units of mm, then it means the the
    # unit is mm/h. In addition, wet deposition units may be in mass of main
    # atom (e.g. N, or S) which are not SI and thus, not handled properly by
    # CF units.
    wdep_unit = str(wdep.units)

    wdep = translate_rate_units_implicit(wdep_unit, wdep_tstype)
    pr = check_pr_units(pr)

    # repeat the unit check steps done for wet deposition
    pr_unit = str(pr.units)
    pr_tstype = TsType(pr.ts_type)

    if not wdep_tstype == pr_tstype:
        # ToDo: this can probably fixed via time resampling with how='sum'
        # for the higher resolution dataset, but for this first draft, this
        # is not allowed.
        raise ValueError(
            "Input precipitation and wet deposition fields need to be in the same frequency..."
        )

    # assign input frequency (just for making the code better readable)
    from_tstype = wdep_tstype
    from_tstype_si = from_tstype.to_si()

    # convert data objects to xarray to do modifications and computation of
    # output variable
    prarr = pr.to_xarray()
    wdeparr = wdep.to_xarray()

    # Make sure precip unit is correct for concprcp=wdep/pr
    pr_unit_calc = f"m {from_tstype_si}-1"

    # unit conversion factor for precip
    mulfac_pr = get_unit_conversion_fac(pr_unit, pr_unit_calc)

    if mulfac_pr != 1:
        prarr *= mulfac_pr
        pr_unit = pr_unit_calc

    # Make sure wdep unit is correct for concprcp=wdep/pr
    wdep_unit_check_calc = wdep_unit.replace("N", "").replace("S", "")
    wdep_unit_calc = f"ug m-2 {from_tstype_si}-1"
    mulfac_wdep = get_unit_conversion_fac(wdep_unit_check_calc, wdep_unit_calc)

    if mulfac_wdep != 1:
        wdeparr *= mulfac_wdep
        if "N" in wdep_unit:
            wdep_unit_calc = wdep_unit_calc.replace("ug", "ug N")
        elif "S" in wdep_unit:
            wdep_unit_calc = wdep_unit_calc.replace("ug", "ug S")
        wdep_unit = wdep_unit_calc

    # final output frequency (precip limit may be applied in higher resolution)
    to_tstype = TsType(ts_type)
    to_tstype_si = to_tstype.to_si()

    # apply prlim filter if applicable
    apply_prlim, prlim_applied = False, False
    if prlim is not None:
        apply_prlim = True

        prlim, prlim_units, prlim_tstype = _check_prlim_units(prlim, prlim_units)

        if prlim_tstype == from_tstype:
            wdeparr, _ = _apply_prlim_wdep(wdeparr, prarr, prlim, prlim_units, prlim_set_under)
            prlim_applied = True

    if apply_prlim and not prlim_applied and prlim_tstype > to_tstype:
        # intermediate frequency where precip filter should be applied
        (wdeparr, prarr, wdep_unit, pr_unit) = _aggregate_wdep_pr(
            wdeparr, prarr, wdep_unit, pr_unit, from_tstype, prlim_tstype
        )

        wdeparr, _ = _apply_prlim_wdep(wdeparr, prarr, prlim, prlim_units, prlim_set_under)
        prlim_applied = True
        from_tstype = prlim_tstype

    if not from_tstype == to_tstype:
        (wdeparr, prarr, wdep_unit, pr_unit) = _aggregate_wdep_pr(
            wdeparr, prarr, wdep_unit, pr_unit, from_tstype, to_tstype
        )

    if apply_prlim and not prlim_applied:
        if not to_tstype == prlim_tstype:
            raise ValueError("... ... .. ")
        wdeparr, _ = _apply_prlim_wdep(wdeparr, prarr, prlim, prlim_units, prlim_set_under)

    # set PR=0 to NaN (as we divide py PR)
    prarr.data[prarr.data == 0] = np.nan

    concprcparr = wdeparr / prarr

    cube = concprcparr.to_iris()
    # infer output unit of concentration variable (should be ug m-3 or ug N m-3 or ug S m-3)
    conc_unit_out = wdep_unit.replace("m-2", "m-3").replace(f"{to_tstype_si}-1", "").strip()
    cube.units = conc_unit_out
    cube.attributes["ts_type"] = str(to_tstype)
    return cube
