from textwrap import dedent

import pytest
from typer.testing import CliRunner

from pyaerocom.scripts.cams2_82.converter import app

runner = CliRunner()


@pytest.fixture
def aeronet_io(tmp_path):
    """Raw input data goes in the subfolder raw_input (the reader reads any csv in the passed path
    so it cannot be shared with the output), while the root itself will be use for output"""
    aeronet_file = tmp_path / "raw_input/2025.csv"
    aeronet_file.parent.mkdir(exist_ok=True, parents=True)
    # end first line with \ to avoid the empty line!
    data = """\
        AERONET Data Download (Version 3 Direct Sun)
        AERONET Version 3
        Version 3: AOD Level 1.5
        The following data are cloud cleared and quality controls have been applied but these data may not have final calibration applied.  These data may change.
        Contact: Please visit https://aeronet.gsfc.nasa.gov/new_web/data_usage.html to properly cite these data and contact principal investigators at https://aeronet.gsfc.nasa.gov/new_web/site_info_v3
        AERONET_Site,Date(dd:mm:yyyy),Time(hh:mm:ss),Day_of_Year,Day_of_Year(Fraction),AOD_1640nm,AOD_1020nm,AOD_870nm,AOD_865nm,AOD_779nm,AOD_675nm,AOD_667nm,AOD_620nm,AOD_560nm,AOD_555nm,AOD_551nm,AOD_532nm,AOD_531nm,AOD_510nm,AOD_500nm,AOD_490nm,AOD_443nm,AOD_440nm,AOD_412nm,AOD_400nm,AOD_380nm,AOD_340nm,Precipitable_Water(cm),AOD_681nm,AOD_709nm,AOD_Empty,AOD_Empty,AOD_Empty,AOD_Empty,AOD_Empty,Triplet_Variability_1640,Triplet_Variability_1020,Triplet_Variability_870,Triplet_Variability_865,Triplet_Variability_779,Triplet_Variability_675,Triplet_Variability_667,Triplet_Variability_620,Triplet_Variability_560,Triplet_Variability_555,Triplet_Variability_551,Triplet_Variability_532,Triplet_Variability_531,Triplet_Variability_510,Triplet_Variability_500,Triplet_Variability_490,Triplet_Variability_443,Triplet_Variability_440,Triplet_Variability_412,Triplet_Variability_400,Triplet_Variability_380,Triplet_Variability_340,Triplet_Variability_Precipitable_Water(cm),Triplet_Variability_681,Triplet_Variability_709,Triplet_Variability_AOD_Empty,Triplet_Variability_AOD_Empty,Triplet_Variability_AOD_Empty,Triplet_Variability_AOD_Empty,Triplet_Variability_AOD_Empty,440-870_Angstrom_Exponent,380-500_Angstrom_Exponent,440-675_Angstrom_Exponent,500-870_Angstrom_Exponent,340-440_Angstrom_Exponent,440-675_Angstrom_Exponent[Polar],Data_Quality_Level,AERONET_Instrument_Number,AERONET_Site_Name,Site_Latitude(Degrees),Site_Longitude(Degrees),Site_Elevation(m),Solar_Zenith_Angle(Degrees),Optical_Air_Mass,Sensor_Temperature(Degrees_C),Ozone(Dobson),NO2(Dobson),Last_Date_Processed,Number_of_Wavelengths,Exact_Wavelengths_of_AOD(um)_1640nm,Exact_Wavelengths_of_AOD(um)_1020nm,Exact_Wavelengths_of_AOD(um)_870nm,Exact_Wavelengths_of_AOD(um)_865nm,Exact_Wavelengths_of_AOD(um)_779nm,Exact_Wavelengths_of_AOD(um)_675nm,Exact_Wavelengths_of_AOD(um)_667nm,Exact_Wavelengths_of_AOD(um)_620nm,Exact_Wavelengths_of_AOD(um)_560nm,Exact_Wavelengths_of_AOD(um)_555nm,Exact_Wavelengths_of_AOD(um)_551nm,Exact_Wavelengths_of_AOD(um)_532nm,Exact_Wavelengths_of_AOD(um)_531nm,Exact_Wavelengths_of_AOD(um)_510nm,Exact_Wavelengths_of_AOD(um)_500nm,Exact_Wavelengths_of_AOD(um)_490nm,Exact_Wavelengths_of_AOD(um)_443nm,Exact_Wavelengths_of_AOD(um)_440nm,Exact_Wavelengths_of_AOD(um)_412nm,Exact_Wavelengths_of_AOD(um)_400nm,Exact_Wavelengths_of_AOD(um)_380nm,Exact_Wavelengths_of_AOD(um)_340nm,Exact_Wavelengths_of_PW(um)_935nm,Exact_Wavelengths_of_AOD(um)_681nm,Exact_Wavelengths_of_AOD(um)_709nm,Exact_Wavelengths_of_AOD(um)_Empty,Exact_Wavelengths_of_AOD(um)_Empty,Exact_Wavelengths_of_AOD(um)_Empty,Exact_Wavelengths_of_AOD(um)_Empty,Exact_Wavelengths_of_AOD(um)_Empty
        Tucson,01:01:2025,16:09:58,1,1.673588,0.013169,0.020531,0.021847,-999.000000,-999.000000,0.025140,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,0.031839,-999.000000,-999.000000,0.036004,-999.000000,-999.000000,0.036988,0.032347,0.420877,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,0.002624,0.002856,0.001850,-999.000000,-999.000000,0.002091,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,0.002153,-999.000000,-999.000000,0.001198,-999.000000,-999.000000,0.001418,0.001145,0.003264,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,-999.000000,0.732349,0.534973,0.828936,0.682894,-0.383201,-999.000000,lev15,1410,Tucson,32.233002,-110.953003,779.000000,72.548345,3.302701,11.200000,280.160008,0.177869,23:06:2025,9,1.639130,1.019793,0.870438,-999.,-999.,0.675163,-999.,-999.,-999.,-999.,-999.,-999.,-999.,-999.,0.500129,-999.,-999.,0.439786,-999.,-999.,0.379597,0.339634,0.937285,-999.,-999.,-999.,-999.,-999.,-999.,-999.
        """
    aeronet_file.write_text(dedent(data))
    return tmp_path


def test_aeronet(aeronet_io):
    out_file = aeronet_io / "result.csv"
    options = f"{aeronet_io}/raw_input {out_file} 2025-01-01 2025-01-02"
    result = runner.invoke(app, options.split())
    assert result.exit_code == 0
    assert out_file.is_file()
    with open(out_file) as f:
        data = f.read()
    assert (
        data
        == "Tucson,01:01:2025,16:09:58,1,lev15,Tucson,32.233002,-110.953003,779.0,0.031839,0.500129,0.682894,0.0298379587784637,AOD_550nm,1,2025-01-01T16:09:58.000000\n"
    )
