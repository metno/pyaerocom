from pyaerocom.io.mscw_ctm.additional_variables import (
    calc_concNhno3,
    calc_concNnh3,
    calc_concNnh4,
    calc_concNno3pm10,
    calc_concNno3pm25,
    calc_concNtnh,
    calc_conNtno3,
    calc_ratpm10pm25,
    calc_ratpm25pm10,
    update_EC_units,
)
from tests.fixtures.mscw_ctm import create_fake_MSCWCtm_data
from pyaerocom.units.constants import M_N, M_O, M_H


def test_calc_concNhno3():
    conchno3 = create_fake_MSCWCtm_data()

    concNhno3_from_func = calc_concNhno3(conchno3)

    concNhno3 = conchno3 * (M_N / (M_H + M_N + M_O * 3))
    concNhno3.attrs["units"] = "ug N m-3"
    assert (concNhno3 == concNhno3_from_func).all()


def test_calc_concNno3pm10():
    concno3c = create_fake_MSCWCtm_data()
    concno3f = create_fake_MSCWCtm_data()

    concNno3pm10_from_func = calc_concNno3pm10(concno3f, concno3c)

    fac = M_N / (M_N + 3 * M_O)
    concno3pm10 = concno3f + concno3c
    concNno3pm10 = concno3pm10 * fac
    concNno3pm10.attrs["var_name"] = "concNno3pm10"
    concNno3pm10.attrs["units"] = "ug N m-3"
    assert (concNno3pm10 == concNno3pm10_from_func).all()


def test_calc_concNno3pm25():
    concno3c = create_fake_MSCWCtm_data()
    concno3f = create_fake_MSCWCtm_data()

    concNno3pm10_from_func = calc_concNno3pm25(concno3f, concno3c)

    fac = M_N / (M_N + 3 * M_O)
    concno3pm10 = concno3f + 0.134 * concno3c
    concNno3pm10 = concno3pm10 * fac
    concNno3pm10.attrs["var_name"] = "concNno3pm10"
    concNno3pm10.attrs["units"] = "ug N m-3"
    assert (concNno3pm10 == concNno3pm10_from_func).all()


def test_calc_conNtno3():
    conchno3 = create_fake_MSCWCtm_data()
    concno3f = create_fake_MSCWCtm_data()
    concno3c = create_fake_MSCWCtm_data()

    concNtno3_from_func = calc_conNtno3(conchno3, concno3f, concno3c)

    concNhno3 = calc_concNhno3(conchno3)
    concNno3pm10 = calc_concNno3pm10(concno3f, concno3c)

    concNtno3 = concNhno3 + concNno3pm10
    concNtno3.attrs["units"] = "ug N m-3"
    assert (concNtno3 == concNtno3_from_func).all()


def test_calc_concNtnh():
    concnh3 = create_fake_MSCWCtm_data()
    concnh4 = create_fake_MSCWCtm_data()

    concNtnh_from_func = calc_concNtnh(concnh3, concnh4)

    concNnh3 = calc_concNnh3(concnh3)
    concNnh4 = calc_concNnh4(concnh4)

    concNtnh = concNnh3 + concNnh4
    concNtnh.attrs["units"] = "ug N m-3"
    assert (concNtnh == concNtnh_from_func).all()


def test_calc_concpm10pm25():
    concpm10 = create_fake_MSCWCtm_data()
    concpm25 = create_fake_MSCWCtm_data()

    ratpm10pm25_from_func = calc_ratpm10pm25(concpm10, concpm25)
    assert ratpm10pm25_from_func.attrs["units"] == "1"


def test_calc_concpm25pm10():
    concpm10 = create_fake_MSCWCtm_data()
    concpm25 = create_fake_MSCWCtm_data()

    ratpm25pm10_from_func = calc_ratpm25pm10(concpm25, concpm10)
    assert ratpm25pm10_from_func.attrs["units"] == "1"


def test_calc_concNnh3():
    concnh3 = create_fake_MSCWCtm_data()

    concNnh3_from_func = calc_concNnh3(concnh3)

    concNnh3 = concnh3 * (M_N / (M_H * 3 + M_N))
    concNnh3.attrs["units"] = "ug N m-3"
    assert (concNnh3 == concNnh3_from_func).all()


def test_calc_concNnh4():
    concnh4 = create_fake_MSCWCtm_data()

    concNnh4_from_func = calc_concNnh4(concnh4)

    concNnh4 = concnh4 * (M_N / (M_H * 4 + M_N))
    concNnh4.attrs["units"] = "ug N m-3"
    assert (concNnh4 == concNnh4_from_func).all()


def test_update_EC_units():
    concecpm25 = create_fake_MSCWCtm_data()

    concCecpm25_from_func = update_EC_units(concecpm25)

    concCecpm25 = concecpm25
    concCecpm25.attrs["units"] = "ug C m-3"

    assert (concCecpm25 == concCecpm25_from_func).all()
    assert concCecpm25.units == concCecpm25_from_func.units
