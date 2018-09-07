
Tutorial showing how to read EBAS NASA Ames files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Note**: this notebook is currently under development

Please see
`here <https://ebas-submit.nilu.no/Submit-Data/Getting-started>`__ for
information related to the EBAS NASA Ames file format.

**Further links**: - `Pyaerocom
website <http://aerocom.met.no/pyaerocom/>`__ - `Pyaerocom installation
instructions <http://aerocom.met.no/pyaerocom/readme.html#installation>`__
- `Getting
started <http://aerocom.met.no/pyaerocom/notebooks.html#getting-started>`__

.. code:: ipython3

    import os 
    from pyaerocom.io import EbasNasaAmesFile
    
    ebasdir = "/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/"
    filename = "DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas"
    
    mc = EbasNasaAmesFile(file=ebasdir+filename,
                          only_head=False,          #set True if you only want to import header
                          replace_invalid_nan=True, #replace invalid values with NaNs
                          convert_timestamps=True,  #compute datetime64 timestamps from numerical values
                          decode_flags=True,        #decode all flags (e.g. 0.111222333 -> 111 222 333)
                          verbose=False)
    print(mc)


.. parsed-literal::

    2018-09-07 17:45:07,092:INFO:
    Reading aliases ini file: /home/jonasg/github/pyaerocom/pyaerocom/data/aliases.ini


.. parsed-literal::

    Elapsed time init all variables: 0.046215057373046875 s


.. parsed-literal::

    2018-09-07 17:45:07,989:WARNING:
    geopy library is not available. Aeolus data read not enabled
    2018-09-07 17:45:08,033:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,069:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,070:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,071:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,072:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:08,073:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    Elapsed time init pyaerocom: 0.9816727638244629 s
    Pyaerocom EbasNasaAmesFile
    --------------------------
    
       num_head_lines: 60
       num_head_fmt: 1001
       data_originator: Flentje, Harald
       sponsor_organisation: DE09L, Deutscher Wetterdienst, DWD, Met. Obs., Hohenspeissenberg, , 82283, Hohenspeissenberg, Germany
       submitter: Flentje, Harald
       project_association: EUSAAR GAW-WDCA
       vol_num: 1
       vol_totnum: 1
       ref_date: 2008 01 01 2016 07 08
       revision_date: nan
       freq: 0.041667
       descr_time_unit: days from file reference point
       num_cols_dependent: 11
       mul_factors (list, 11 items)
       [1.0
        1.0
        ...
        1.0
        1.0]
    
       vals_invalid (list, 11 items)
       [999.999999
        999.999
        ...
        9999.9
        9.999999999]
    
       descr_first_col: end_time of measurement, days from the file reference point
    
       Column variable definitions
       -------------------------------
       EbasColDef: name=starttime, unit=days, is_var=False, is_flag=False, flag_id=, 
       EbasColDef: name=endtime, unit=days, is_var=False, is_flag=False, flag_id=, 
       EbasColDef: name=aerosol_light_backscattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_id=numflag, wavelength=450.0 nm, 
       EbasColDef: name=aerosol_light_backscattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_id=numflag, wavelength=550.0 nm, 
       EbasColDef: name=aerosol_light_backscattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_id=numflag, wavelength=700.0 nm, 
       EbasColDef: name=aerosol_light_scattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_id=numflag, wavelength=450.0 nm, 
       EbasColDef: name=aerosol_light_scattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_id=numflag, wavelength=550.0 nm, 
       EbasColDef: name=aerosol_light_scattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_id=numflag, wavelength=700.0 nm, 
       EbasColDef: name=pressure, unit=hPa, is_var=True, is_flag=False, flag_id=numflag, location=instrument internal, 
       EbasColDef: name=relative_humidity, unit=%, is_var=True, is_flag=False, flag_id=numflag, location=instrument internal, 
       EbasColDef: name=temperature, unit=K, is_var=True, is_flag=False, flag_id=numflag, location=instrument internal, 
       EbasColDef: name=numflag, unit=no unit, is_var=False, is_flag=True, flag_id=, 
    
       EBAS meta data
       ------------------
       verbose: False
       data_definition: EBAS_1.1
       set_type_code: TU
       timezone: UTC
       file_name: DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
       file_creation: 20180101031050
       startdate: 20080101000000
       revision_date: 20160708144500
       statistics: arithmetic mean
       data_level: 2
       period_code: 1y
       resolution_code: 1h
       station_code: DE0043G
       platform_code: DE0043S
       station_name: Hohenpeissenberg
       station_wdca-id: GAWADE__HPB
       station_gaw-id: HPB
       station_gaw-name: Hohenpeissenberg
       station_land_use: Grassland
       station_setting: Mountain
       station_gaw_type: G
       station_wmo_region: 6
       station_latitude: 47.8014984131
       station_longitude: 11.0096197128
       station_altitude: 985.0 m
       regime: IMG
       component: 
       unit: 1/Mm
       matrix: aerosol
       laboratory_code: DE09L
       instrument_type: nephelometer
       instrument_name: tsi_neph_3563
       method_ref: DE09L_nephelometer
       originator: Flentje, Harald, Harald.Flentje@dwd.de, , , , , , , ,
       submitter: Flentje, Harald, Harald.Flentje@dwd.de, , , , , , , ,
    
       Data
       --------
    [[0.00000000e+00 4.16670000e-02            nan ...            nan
                 nan 3.94999000e-01]
     [4.16670000e-02 8.33330000e-02            nan ...            nan
                 nan 3.94999000e-01]
     [8.33330000e-02 1.25000000e-01            nan ...            nan
                 nan 3.94999000e-01]
     ...
     [3.65875000e+02 3.65916667e+02 4.75900000e+00 ... 8.50000000e+00
      2.99900000e+02 2.47000000e-01]
     [3.65916667e+02 3.65958310e+02 5.16200000e+00 ... 8.70000000e+00
      2.99900000e+02 2.47000000e-01]
     [3.65958333e+02 3.66000000e+02 5.31800000e+00 ... 9.30000000e+00
      2.99700000e+02 0.00000000e+00]]
    Colnum: 12
    Timestamps: 8784


Column information
^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    mc.print_col_info()


.. parsed-literal::

    Column 0
    Pyaerocom EbasColDef
    --------------------
    name: starttime
    unit: days
    is_var: False
    is_flag: False
    flag_id: 
    
    Column 1
    Pyaerocom EbasColDef
    --------------------
    name: endtime
    unit: days
    is_var: False
    is_flag: False
    flag_id: 
    
    Column 2
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_backscattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_id: numflag
    wavelength: 450.0 nm
    
    Column 3
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_backscattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_id: numflag
    wavelength: 550.0 nm
    
    Column 4
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_backscattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_id: numflag
    wavelength: 700.0 nm
    
    Column 5
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_scattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_id: numflag
    wavelength: 450.0 nm
    
    Column 6
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_scattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_id: numflag
    wavelength: 550.0 nm
    
    Column 7
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_scattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_id: numflag
    wavelength: 700.0 nm
    
    Column 8
    Pyaerocom EbasColDef
    --------------------
    name: pressure
    unit: hPa
    is_var: True
    is_flag: False
    flag_id: numflag
    location: instrument internal
    
    Column 9
    Pyaerocom EbasColDef
    --------------------
    name: relative_humidity
    unit: %
    is_var: True
    is_flag: False
    flag_id: numflag
    location: instrument internal
    
    Column 10
    Pyaerocom EbasColDef
    --------------------
    name: temperature
    unit: K
    is_var: True
    is_flag: False
    flag_id: numflag
    location: instrument internal
    
    Column 11
    Pyaerocom EbasColDef
    --------------------
    name: numflag
    unit: no unit
    is_var: False
    is_flag: True
    flag_id: 
    


You can see that all variable columns were assigned the same flag
column, since there is only one. This would be different if there were
multiple flag columns (e.g. one for each variable).

Access flag information
^^^^^^^^^^^^^^^^^^^^^^^

You can access the flags for each column using the ``flags`` attribute
of the file.

.. code:: ipython3

    mc.flags




.. parsed-literal::

    OrderedDict([('numflag',
                  <pyaerocom.io.ebas_nasa_ames.EbasFlagCol at 0x7fc97cfc5be0>)])



.. code:: ipython3

    flagcol = mc.flags["numflag"]

The raw flags can be accessed via:

.. code:: ipython3

    flagcol.raw_data




.. parsed-literal::

    array([0.394999, 0.394999, 0.394999, ..., 0.247   , 0.247   , 0.      ])



And the processed flags are in stored in a (Nx3) numpy array where N is
the total number of timestamps.

.. code:: ipython3

    flagcol.flags




.. parsed-literal::

    array([[394, 999,   0],
           [394, 999,   0],
           [394, 999,   0],
           ...,
           [247,   0,   0],
           [247,   0,   0],
           [  0,   0,   0]])



For instance, access the flags of the 5 timestamp:

.. code:: ipython3

    flagcol.flags[4]




.. parsed-literal::

    array([394, 999,   0])



Convert object to pandas Dataframe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The conversion does currently exclude all flag columns

.. code:: ipython3

    df = mc.to_dataframe()
    df




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>aerosol_light_backscattering_coefficient</th>
          <th>aerosol_light_backscattering_coefficient</th>
          <th>aerosol_light_backscattering_coefficient</th>
          <th>aerosol_light_scattering_coefficient</th>
          <th>aerosol_light_scattering_coefficient</th>
          <th>aerosol_light_scattering_coefficient</th>
          <th>pressure</th>
          <th>relative_humidity</th>
          <th>temperature</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2008-01-01 00:30:00</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 01:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 02:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 03:30:00</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 04:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 05:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 06:30:00</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 07:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 08:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 09:30:00</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 10:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 11:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 12:30:00</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 13:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 14:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 15:30:00</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 16:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 17:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 18:30:00</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 19:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 20:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 21:30:00</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 22:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-01 23:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-02 00:30:00</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-02 01:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-02 02:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-02 03:30:00</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-02 04:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2008-01-02 05:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>2008-12-30 18:30:00</th>
          <td>0.547</td>
          <td>0.409</td>
          <td>0.303</td>
          <td>5.250</td>
          <td>3.716</td>
          <td>2.264</td>
          <td>909.0</td>
          <td>4.5</td>
          <td>300.4</td>
        </tr>
        <tr>
          <th>2008-12-30 19:29:58</th>
          <td>1.045</td>
          <td>0.688</td>
          <td>0.558</td>
          <td>7.934</td>
          <td>5.414</td>
          <td>3.308</td>
          <td>909.0</td>
          <td>5.7</td>
          <td>300.2</td>
        </tr>
        <tr>
          <th>2008-12-30 20:29:59</th>
          <td>7.862</td>
          <td>5.979</td>
          <td>4.602</td>
          <td>70.955</td>
          <td>50.095</td>
          <td>30.940</td>
          <td>909.0</td>
          <td>8.9</td>
          <td>300.4</td>
        </tr>
        <tr>
          <th>2008-12-30 21:30:00</th>
          <td>11.044</td>
          <td>8.777</td>
          <td>6.770</td>
          <td>103.578</td>
          <td>73.434</td>
          <td>45.628</td>
          <td>909.0</td>
          <td>9.2</td>
          <td>300.3</td>
        </tr>
        <tr>
          <th>2008-12-30 22:29:58</th>
          <td>6.420</td>
          <td>5.011</td>
          <td>3.801</td>
          <td>57.828</td>
          <td>40.803</td>
          <td>25.309</td>
          <td>909.0</td>
          <td>8.7</td>
          <td>300.1</td>
        </tr>
        <tr>
          <th>2008-12-30 23:29:59</th>
          <td>3.947</td>
          <td>3.107</td>
          <td>2.509</td>
          <td>41.293</td>
          <td>30.195</td>
          <td>19.253</td>
          <td>909.0</td>
          <td>8.1</td>
          <td>300.4</td>
        </tr>
        <tr>
          <th>2008-12-31 00:30:00</th>
          <td>2.950</td>
          <td>2.492</td>
          <td>1.939</td>
          <td>32.975</td>
          <td>24.133</td>
          <td>15.449</td>
          <td>908.0</td>
          <td>7.9</td>
          <td>299.8</td>
        </tr>
        <tr>
          <th>2008-12-31 01:29:58</th>
          <td>2.024</td>
          <td>1.660</td>
          <td>1.362</td>
          <td>22.381</td>
          <td>16.227</td>
          <td>10.269</td>
          <td>908.0</td>
          <td>7.5</td>
          <td>300.2</td>
        </tr>
        <tr>
          <th>2008-12-31 02:29:59</th>
          <td>0.731</td>
          <td>0.569</td>
          <td>0.508</td>
          <td>6.382</td>
          <td>4.487</td>
          <td>2.890</td>
          <td>907.0</td>
          <td>6.6</td>
          <td>299.9</td>
        </tr>
        <tr>
          <th>2008-12-31 03:30:00</th>
          <td>0.733</td>
          <td>0.659</td>
          <td>0.506</td>
          <td>6.934</td>
          <td>4.876</td>
          <td>3.026</td>
          <td>907.0</td>
          <td>6.7</td>
          <td>299.8</td>
        </tr>
        <tr>
          <th>2008-12-31 04:29:58</th>
          <td>0.994</td>
          <td>0.779</td>
          <td>0.714</td>
          <td>9.422</td>
          <td>6.621</td>
          <td>4.073</td>
          <td>907.0</td>
          <td>7.0</td>
          <td>300.2</td>
        </tr>
        <tr>
          <th>2008-12-31 05:29:59</th>
          <td>1.842</td>
          <td>1.514</td>
          <td>1.198</td>
          <td>18.791</td>
          <td>13.431</td>
          <td>8.296</td>
          <td>906.0</td>
          <td>7.5</td>
          <td>300.2</td>
        </tr>
        <tr>
          <th>2008-12-31 06:30:00</th>
          <td>4.045</td>
          <td>3.247</td>
          <td>2.608</td>
          <td>42.560</td>
          <td>31.077</td>
          <td>19.972</td>
          <td>906.0</td>
          <td>8.2</td>
          <td>299.9</td>
        </tr>
        <tr>
          <th>2008-12-31 07:29:58</th>
          <td>3.753</td>
          <td>2.974</td>
          <td>2.371</td>
          <td>40.905</td>
          <td>29.963</td>
          <td>19.293</td>
          <td>906.0</td>
          <td>8.0</td>
          <td>299.8</td>
        </tr>
        <tr>
          <th>2008-12-31 08:29:59</th>
          <td>2.799</td>
          <td>2.189</td>
          <td>1.745</td>
          <td>29.099</td>
          <td>21.226</td>
          <td>13.575</td>
          <td>906.0</td>
          <td>7.7</td>
          <td>299.9</td>
        </tr>
        <tr>
          <th>2008-12-31 09:30:00</th>
          <td>1.760</td>
          <td>1.427</td>
          <td>1.077</td>
          <td>16.988</td>
          <td>12.135</td>
          <td>7.623</td>
          <td>906.0</td>
          <td>7.1</td>
          <td>300.3</td>
        </tr>
        <tr>
          <th>2008-12-31 10:29:58</th>
          <td>2.548</td>
          <td>1.917</td>
          <td>1.455</td>
          <td>24.601</td>
          <td>17.758</td>
          <td>11.318</td>
          <td>905.0</td>
          <td>7.1</td>
          <td>300.7</td>
        </tr>
        <tr>
          <th>2008-12-31 11:29:59</th>
          <td>2.486</td>
          <td>1.909</td>
          <td>1.442</td>
          <td>24.114</td>
          <td>17.331</td>
          <td>11.010</td>
          <td>905.0</td>
          <td>7.0</td>
          <td>301.2</td>
        </tr>
        <tr>
          <th>2008-12-31 12:30:00</th>
          <td>2.660</td>
          <td>2.172</td>
          <td>1.623</td>
          <td>27.016</td>
          <td>19.509</td>
          <td>12.520</td>
          <td>905.0</td>
          <td>7.4</td>
          <td>300.9</td>
        </tr>
        <tr>
          <th>2008-12-31 13:29:58</th>
          <td>6.408</td>
          <td>5.162</td>
          <td>4.016</td>
          <td>62.217</td>
          <td>44.872</td>
          <td>28.652</td>
          <td>905.0</td>
          <td>8.7</td>
          <td>300.6</td>
        </tr>
        <tr>
          <th>2008-12-31 14:29:59</th>
          <td>8.818</td>
          <td>7.038</td>
          <td>5.385</td>
          <td>80.137</td>
          <td>56.764</td>
          <td>35.320</td>
          <td>905.0</td>
          <td>9.3</td>
          <td>301.0</td>
        </tr>
        <tr>
          <th>2008-12-31 15:30:00</th>
          <td>7.646</td>
          <td>6.019</td>
          <td>4.688</td>
          <td>69.304</td>
          <td>49.066</td>
          <td>30.776</td>
          <td>905.0</td>
          <td>9.5</td>
          <td>301.0</td>
        </tr>
        <tr>
          <th>2008-12-31 16:29:58</th>
          <td>6.733</td>
          <td>5.320</td>
          <td>4.010</td>
          <td>61.384</td>
          <td>43.327</td>
          <td>26.987</td>
          <td>904.0</td>
          <td>9.8</td>
          <td>300.3</td>
        </tr>
        <tr>
          <th>2008-12-31 17:29:59</th>
          <td>5.989</td>
          <td>4.690</td>
          <td>3.628</td>
          <td>57.607</td>
          <td>41.258</td>
          <td>25.973</td>
          <td>904.0</td>
          <td>9.2</td>
          <td>300.1</td>
        </tr>
        <tr>
          <th>2008-12-31 18:30:00</th>
          <td>7.768</td>
          <td>6.130</td>
          <td>4.776</td>
          <td>76.904</td>
          <td>55.401</td>
          <td>35.085</td>
          <td>904.0</td>
          <td>9.3</td>
          <td>299.9</td>
        </tr>
        <tr>
          <th>2008-12-31 19:29:58</th>
          <td>6.265</td>
          <td>4.834</td>
          <td>3.827</td>
          <td>61.421</td>
          <td>44.224</td>
          <td>28.044</td>
          <td>904.0</td>
          <td>8.7</td>
          <td>299.9</td>
        </tr>
        <tr>
          <th>2008-12-31 20:29:59</th>
          <td>4.425</td>
          <td>3.433</td>
          <td>2.663</td>
          <td>43.144</td>
          <td>30.726</td>
          <td>19.240</td>
          <td>903.0</td>
          <td>8.5</td>
          <td>299.8</td>
        </tr>
        <tr>
          <th>2008-12-31 21:30:00</th>
          <td>4.759</td>
          <td>3.665</td>
          <td>2.840</td>
          <td>44.719</td>
          <td>31.694</td>
          <td>19.885</td>
          <td>903.0</td>
          <td>8.5</td>
          <td>299.9</td>
        </tr>
        <tr>
          <th>2008-12-31 22:29:58</th>
          <td>5.162</td>
          <td>3.929</td>
          <td>3.217</td>
          <td>48.623</td>
          <td>34.503</td>
          <td>21.719</td>
          <td>903.0</td>
          <td>8.7</td>
          <td>299.9</td>
        </tr>
        <tr>
          <th>2008-12-31 23:29:59</th>
          <td>5.318</td>
          <td>4.307</td>
          <td>3.349</td>
          <td>54.983</td>
          <td>39.390</td>
          <td>24.721</td>
          <td>903.0</td>
          <td>9.3</td>
          <td>299.7</td>
        </tr>
      </tbody>
    </table>
    <p>8784 rows × 9 columns</p>
    </div>



Performance
^^^^^^^^^^^

Read only header

.. code:: ipython3

    %%timeit
    EbasNasaAmesFile(file=ebasdir+filename,
                     only_head=True, verbose=False)


.. parsed-literal::

    2018-09-07 17:45:08,322:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,326:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,326:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,327:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,329:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,332:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,333:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,333:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,335:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,338:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,338:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,339:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,340:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,343:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,344:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,345:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,348:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,349:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,350:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,352:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,354:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,355:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,356:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,357:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,360:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,361:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,361:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,363:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,366:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,367:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,367:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,369:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,372:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,372:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,372:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,374:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,377:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,377:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,378:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,380:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,384:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,385:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,386:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,388:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,390:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,392:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,392:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,394:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,397:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,398:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,399:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,400:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,403:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,404:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,404:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,406:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,409:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,409:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,409:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,411:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,413:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,414:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,414:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,416:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,418:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,419:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,420:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,421:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,424:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,425:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,426:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,427:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,430:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,431:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,431:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,432:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,435:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,436:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,436:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,438:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,441:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,442:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,442:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,444:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,447:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,447:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,447:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,449:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,452:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,452:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,453:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,454:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,457:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,457:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,457:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,459:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,461:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,462:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,463:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,464:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,467:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,468:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,468:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,470:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,474:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,475:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,475:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,477:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,480:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,481:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,481:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,483:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,486:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,487:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,487:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,489:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,493:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,493:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,494:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,496:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,500:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,500:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,501:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,503:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,506:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,507:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,508:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,509:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,513:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,513:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,513:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,515:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,518:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,518:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,519:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,521:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,524:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,524:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,525:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,527:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,530:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,530:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,531:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,532:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,535:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,535:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,536:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,537:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,541:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,541:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,542:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,544:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,547:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,548:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,548:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,550:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,553:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,553:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,554:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,555:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,558:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,558:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,559:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,560:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,563:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,564:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,565:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,567:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,570:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,570:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,571:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,572:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,576:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,577:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,577:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,579:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,582:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,583:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,584:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,585:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,589:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,589:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,590:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,591:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,595:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,595:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,597:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,600:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,601:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,601:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,603:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,606:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,607:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,608:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,609:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,613:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,613:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,614:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,615:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,618:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,618:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,619:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,620:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,623:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,624:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,625:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,626:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,630:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,630:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,631:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,632:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,635:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,636:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,637:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,638:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,641:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,642:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,643:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,644:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,647:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,648:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,648:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,650:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,653:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,654:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,654:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,656:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,659:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,659:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,660:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,661:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,665:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,665:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,666:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,668:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,671:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,671:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,672:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,673:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,676:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,676:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,677:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,678:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,681:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,682:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,683:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,684:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,689:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,697:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,697:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,699:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,702:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,702:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,703:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,704:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,707:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,708:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,708:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,710:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,713:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,713:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,714:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,715:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,718:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,719:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,719:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,720:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,724:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,724:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,724:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,726:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,729:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,729:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,729:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,731:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,734:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,734:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,735:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,736:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,739:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,739:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,739:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,741:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,743:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,744:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,744:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,745:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,748:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,749:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,749:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,750:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,753:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,754:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,754:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,755:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,758:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,758:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,759:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,760:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,763:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,764:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,764:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,765:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,768:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,769:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,769:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,770:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,774:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,775:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,775:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,776:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,779:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,780:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,780:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,781:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,784:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,784:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,785:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,787:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,790:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,790:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,790:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,792:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,795:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,795:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,796:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,797:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,800:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,800:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,801:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,803:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,806:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,807:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,807:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,808:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,811:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,812:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,812:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,813:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,816:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,817:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,817:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,818:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,821:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,821:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,822:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,823:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,825:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,826:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,826:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,827:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,831:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,831:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,833:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,835:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,836:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,836:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,837:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,840:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,841:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,841:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,842:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,847:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,847:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,848:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,849:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,852:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,852:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,852:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,854:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,856:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,856:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,857:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,858:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,861:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,861:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,862:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,863:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,867:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,868:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,871:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,872:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,872:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,873:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,876:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,876:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,876:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,878:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,881:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,881:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,882:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,883:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,885:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,886:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,887:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,888:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,890:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,891:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,891:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,892:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,895:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,896:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,896:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,897:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,900:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,900:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,901:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,902:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,905:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,905:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,905:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,906:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,909:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,910:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,910:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,911:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,914:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,915:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,915:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,917:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,919:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,920:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,920:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,922:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,924:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,925:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,925:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,926:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,929:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,930:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,930:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,932:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,934:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,935:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,935:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,937:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,940:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,940:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,941:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,942:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,945:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,946:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,946:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,948:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,951:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,952:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,953:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,954:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,957:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,958:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,958:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,960:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,963:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,963:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,964:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,965:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,968:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,969:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,969:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,971:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,974:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,975:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,975:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,977:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,980:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,981:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,981:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,983:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,986:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,986:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,987:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,988:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,991:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,992:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,992:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:08,994:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:08,997:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:08,998:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:08,998:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,000:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,003:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,003:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,004:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,005:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,009:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,009:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,010:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,011:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,015:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,015:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,016:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,017:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,020:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,021:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,021:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,023:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,026:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,026:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,027:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,036:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,039:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,039:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,040:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,041:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,044:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,044:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,045:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,046:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,049:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,049:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,050:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,051:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,054:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,054:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,055:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,056:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,059:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,059:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,060:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,061:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,064:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,064:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,065:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,066:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,069:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,070:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,071:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,072:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,075:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,076:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,076:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,078:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,081:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,082:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,082:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,084:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,087:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,087:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,088:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,089:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,092:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,092:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,093:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,094:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,097:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,097:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,098:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,099:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,103:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,103:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,104:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,105:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,108:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,109:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,109:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,111:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,114:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,114:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,115:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,116:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,119:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,120:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,120:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,122:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,125:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,125:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,125:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,127:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,130:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,130:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,130:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,132:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,134:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,135:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,135:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,136:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,139:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,140:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,140:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,141:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,144:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,144:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,145:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,146:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,149:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,149:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,150:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,151:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,153:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,154:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,154:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,155:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,158:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,158:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,159:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,160:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,163:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,163:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,164:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,165:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,168:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,168:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,168:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,170:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,172:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,173:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,173:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,174:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,177:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,178:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,178:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,179:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,182:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,182:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,183:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,184:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,187:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,187:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,189:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,192:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,192:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,193:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,194:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,197:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,198:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,198:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,200:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,203:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,203:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,204:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,205:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,208:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,209:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,209:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,210:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,213:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,213:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,214:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,215:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,218:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,218:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,219:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,220:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,223:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,224:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,224:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,226:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,229:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,229:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,230:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,231:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,234:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,234:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,234:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,236:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,238:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,239:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,239:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,240:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,243:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,243:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,244:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,245:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,248:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,248:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,248:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,250:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,252:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,253:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,253:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,254:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,257:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,257:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,258:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,259:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,262:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,262:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,263:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,264:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,266:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,267:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,267:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,269:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,272:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,273:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,273:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,275:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,278:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,278:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,279:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,280:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,283:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,284:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,284:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,286:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,289:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,289:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,290:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,291:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,294:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,295:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,295:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,297:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,300:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,301:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,302:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,303:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,306:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,307:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,307:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,308:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,311:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,311:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,312:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,313:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,316:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,316:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,317:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,318:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,321:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,322:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,322:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,325:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,328:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,328:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,328:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,331:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,334:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,335:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,335:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,337:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,340:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,340:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,341:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,342:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,345:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,346:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,346:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,347:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,351:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,351:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,352:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,353:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,356:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,357:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,357:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,359:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,362:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,362:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,363:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,364:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,368:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,368:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,368:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,370:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,373:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,374:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,374:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,376:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,378:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,379:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,379:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,381:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,384:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,384:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,385:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,386:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,389:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,389:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,390:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,391:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,394:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,394:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,395:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,397:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,400:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,400:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,401:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,402:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,406:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,406:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,407:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,409:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,412:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,412:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,413:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,414:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,417:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,418:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,418:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,420:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,423:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,423:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,424:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,425:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,428:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,429:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,429:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,431:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,434:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,435:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,435:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,437:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,440:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,440:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,441:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,442:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,445:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,446:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,447:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,448:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,451:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,452:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,452:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,454:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,457:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,457:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,458:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,459:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,462:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,463:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,464:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,465:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,468:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,468:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,469:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,470:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,473:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,474:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,475:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,476:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,479:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,480:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,480:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,482:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,484:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,485:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,485:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,487:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,490:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,490:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,491:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,492:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,495:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,495:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,496:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,497:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,500:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,501:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,501:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,503:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,506:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,507:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,507:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,509:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,512:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,512:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,513:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,514:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,518:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,518:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,519:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,520:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,523:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,524:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,524:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,526:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,528:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,529:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,530:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,531:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,534:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,535:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,535:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,537:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,540:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,540:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,541:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,542:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,545:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,546:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,546:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,548:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,550:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,551:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,551:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,552:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,555:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,556:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,556:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,557:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,560:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,561:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,561:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,562:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,565:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,566:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,568:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,570:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,573:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,573:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,574:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,576:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,579:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,582:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,582:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,585:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,589:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,589:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,590:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,591:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,595:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,596:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,598:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,602:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,603:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,604:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,607:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,608:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,609:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,610:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,613:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,614:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,614:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,616:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,619:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,619:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,620:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,621:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,624:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,625:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,626:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,627:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,630:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,631:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,631:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,633:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,635:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,636:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,636:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,638:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,640:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,641:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,642:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,643:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,646:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,646:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,646:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,648:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,650:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,651:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,651:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,652:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,655:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,656:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,656:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,657:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,661:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,661:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,661:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,663:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,665:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,666:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,666:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,667:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,670:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,670:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,671:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,672:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,675:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,675:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,676:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,677:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,680:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,681:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,681:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,683:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,686:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,687:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,687:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,689:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,693:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,693:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,694:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,695:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,698:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,698:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,699:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,700:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,703:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,703:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,703:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,705:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,708:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,709:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,709:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,711:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,714:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,714:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,715:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,716:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,719:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,719:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,719:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,721:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,724:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,724:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,724:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,726:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,728:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,729:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,729:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,730:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,733:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,734:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,734:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,735:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,738:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,738:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,739:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,740:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,743:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,744:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,744:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,745:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,748:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,748:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,749:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,750:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,753:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,754:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,754:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,756:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,759:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,759:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,760:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,761:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,764:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,765:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,765:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,767:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,769:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,770:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,770:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,772:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,774:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,775:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,775:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,777:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,780:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,780:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,781:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,782:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,785:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,786:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,787:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,788:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,791:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,791:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,792:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,793:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,796:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,797:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,797:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,798:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,801:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,802:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,802:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,803:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,807:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,807:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,808:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,809:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,812:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,813:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,813:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,814:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,817:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,818:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,818:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,819:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,822:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,822:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,823:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,824:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,827:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,827:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,827:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,828:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,832:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,832:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,833:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,836:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,837:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,837:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,838:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,841:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,841:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,842:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,843:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,846:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,846:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,846:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,848:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,851:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,851:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,851:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,852:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,855:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,856:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,856:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,858:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,861:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,861:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,862:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,863:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,867:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,868:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,871:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,871:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,872:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,873:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,876:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,876:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,876:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,878:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,880:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,880:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,881:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,883:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,886:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,887:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,887:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,889:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,892:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,893:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,894:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,896:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,899:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,900:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,901:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,904:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,905:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,905:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,907:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,910:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,911:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,911:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,913:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,916:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,916:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,917:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,919:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,922:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,922:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,923:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,924:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,927:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,927:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,928:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,929:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,931:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,932:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,932:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,934:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,937:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,937:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,938:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,940:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,942:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,943:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,943:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,945:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,948:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,948:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,949:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,950:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,953:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,954:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,954:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,956:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,959:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,959:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,960:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,961:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,964:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,965:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,965:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,967:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,970:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,970:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,971:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,972:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,975:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,975:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,976:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,977:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,980:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,981:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,981:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,982:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,986:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,986:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,987:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,988:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,991:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,991:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,992:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,993:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:09,996:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:09,996:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:09,997:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:09,998:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,001:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,002:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,002:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,004:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,007:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,007:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,008:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,009:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,012:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,013:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,013:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,015:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,018:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,018:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,019:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,020:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,023:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,024:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,024:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,025:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,028:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,029:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,030:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,034:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,040:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,040:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,041:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,046:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,050:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,051:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,051:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,053:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,056:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,057:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,058:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,060:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,063:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,064:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,065:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,066:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,070:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,070:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,071:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,073:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,076:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,076:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,077:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,078:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,082:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,083:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,084:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,085:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,088:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,088:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,089:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,090:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,093:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,094:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,094:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,096:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,101:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,101:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,102:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,103:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,107:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,107:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,107:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,109:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,112:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,112:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,112:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,114:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,117:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,117:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,117:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,119:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,122:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,123:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,123:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,124:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,128:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,128:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,128:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,130:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,133:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,133:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,134:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,135:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,138:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,138:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,139:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,140:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,143:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,144:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,145:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,146:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,149:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,150:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,151:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,152:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,155:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,155:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,156:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,157:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,159:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,160:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,160:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,161:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,164:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,165:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,165:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,166:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,169:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,170:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,170:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,172:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,175:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,176:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,176:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,178:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,181:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,181:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,182:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,183:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,186:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,187:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,187:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,189:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,192:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,192:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,193:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,194:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,198:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,199:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,199:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,204:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,204:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,204:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,206:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,209:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,210:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,210:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,212:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,215:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,215:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,216:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,217:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,220:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,221:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,222:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,224:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,228:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,228:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,229:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,230:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,233:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,234:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,235:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,237:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,241:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,242:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,242:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,244:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,247:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,248:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,248:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,250:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,252:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,253:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,253:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,254:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,258:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,258:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,258:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,260:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,262:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,263:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,263:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,265:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,268:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,268:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,269:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,270:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,273:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,274:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,274:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,276:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,279:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,280:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,280:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,281:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,284:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,285:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,285:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,287:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,290:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,290:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,291:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,293:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,296:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,297:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,297:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,299:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,302:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,302:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,303:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,304:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,307:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,307:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,308:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,309:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,312:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,312:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,313:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,314:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,317:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,317:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,317:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,319:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,321:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,322:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,322:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,323:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,326:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,327:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,327:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,330:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,332:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,333:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,333:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,336:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,339:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,340:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,340:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,341:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,344:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,345:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,345:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,346:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,349:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,350:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,350:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,352:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,354:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,355:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,355:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,356:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,359:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,360:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,360:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,361:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,365:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,365:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,365:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,367:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,370:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,370:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,371:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,372:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,374:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,375:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,375:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,376:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,379:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,380:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,380:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,381:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,384:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,385:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,385:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,386:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,390:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,390:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,391:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,392:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,395:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,396:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,396:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,398:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,401:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,401:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,402:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,403:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,406:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,407:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,407:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,409:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,412:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,413:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,414:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,415:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,419:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,419:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,420:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,421:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,424:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,424:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,424:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,426:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,428:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,429:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,429:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,431:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,434:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,434:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,434:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,436:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,439:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,439:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,440:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,441:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,444:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,445:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,445:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,447:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,450:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,451:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,451:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,452:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,456:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,456:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,456:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,458:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,461:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,461:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,461:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,463:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,465:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,466:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,466:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,468:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,471:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,471:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,472:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,473:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,476:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,476:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,476:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,478:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,481:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,481:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,482:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,483:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,487:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,487:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,488:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,489:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,493:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,493:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,495:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,498:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,499:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,499:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,501:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,504:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,504:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,505:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,506:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,509:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,510:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,511:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,512:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,515:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,516:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,516:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,518:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,521:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,521:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,522:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,523:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,526:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,527:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,527:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,529:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,532:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,532:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,533:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,535:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,538:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,538:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,539:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,540:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,543:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,544:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,544:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,546:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,549:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,549:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,549:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,551:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,554:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,555:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,555:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,556:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,560:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,560:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,561:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,562:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,565:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,566:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,566:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,568:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,571:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,571:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,572:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,573:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,576:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,577:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,577:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,579:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,582:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,582:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,583:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,584:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,587:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,588:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,588:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,589:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,593:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,593:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,594:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,595:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,598:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,599:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,599:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,600:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,603:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,604:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,604:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,606:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,608:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,609:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,609:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,610:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,613:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,614:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,614:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,615:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,618:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,618:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,619:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,620:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,623:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,623:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,624:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,626:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,629:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,629:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,630:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,631:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,634:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,635:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,635:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,637:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,640:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,640:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,641:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,642:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,645:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,646:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,647:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,648:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,651:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,651:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,652:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,653:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,656:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,656:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,657:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,658:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,661:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,661:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,661:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,662:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,665:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,666:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,666:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,667:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,670:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,671:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,671:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,672:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,675:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,676:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,677:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,679:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,683:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,683:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,684:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,686:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,689:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,689:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,690:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,691:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,694:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,695:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,696:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,697:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,700:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,701:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,701:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,703:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,706:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,707:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,708:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,709:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,712:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,713:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,713:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,715:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,718:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,719:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,719:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,721:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,724:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,724:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,725:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,727:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,730:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,730:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,731:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,733:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,736:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,737:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,737:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,739:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,742:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,742:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,743:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,745:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,748:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,749:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,749:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,751:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,755:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,755:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,756:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,758:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,762:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,763:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,763:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,765:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,769:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,769:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,770:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,771:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,775:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,776:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,776:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,778:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,781:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,782:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,783:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,785:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,788:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,788:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,789:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,791:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,794:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,795:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,795:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,797:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,801:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,801:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,802:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,804:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,807:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,808:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,809:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,812:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,815:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,816:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,817:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,818:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,822:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,822:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,823:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,824:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,827:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,828:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,829:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,830:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,833:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,834:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,835:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,837:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,840:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,841:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,842:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,843:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,846:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,847:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,848:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,849:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,853:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,854:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,855:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,856:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,859:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,860:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,860:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,862:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,865:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,866:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,868:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,871:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,872:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,873:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,874:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,877:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,879:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,879:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,881:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,884:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,885:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,885:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,887:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,890:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,891:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,891:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,893:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,896:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,897:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,897:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,899:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,902:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,903:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,903:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,905:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,908:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,909:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,909:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,911:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,914:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,915:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,916:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,917:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,920:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,921:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,921:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,923:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,926:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,927:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,928:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,929:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,932:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,933:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,933:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,935:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,938:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,939:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,939:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,941:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,944:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,944:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,945:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,946:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,949:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,950:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,950:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,952:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,955:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,955:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,956:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,957:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,960:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,961:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,962:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,964:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,967:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,967:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,968:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,969:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,972:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,973:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,973:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,975:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,978:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,979:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,979:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,981:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,984:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,985:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,985:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,987:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,990:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,990:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,991:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,992:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:10,995:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:10,996:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:10,996:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:10,998:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,002:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,002:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,003:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,005:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,008:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,009:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,010:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,012:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,016:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,017:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,017:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,019:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,022:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,023:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,023:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,025:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,028:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,029:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,029:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,031:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,034:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,035:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,035:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,041:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,044:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,045:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,045:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,048:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,052:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,052:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,053:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,056:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,060:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,061:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,061:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,063:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,066:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,066:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,067:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,068:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,071:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,072:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,073:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,074:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,077:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,078:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,079:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,080:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,083:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,084:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,084:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,086:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,089:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,089:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,090:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,091:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,094:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,095:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,096:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,097:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,101:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,101:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,102:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,103:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,106:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,107:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,107:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,109:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,112:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,113:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,113:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,115:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,118:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,119:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,119:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,121:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,124:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,124:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,125:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,127:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,130:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,130:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,131:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,133:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,137:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,137:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,138:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,139:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,142:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,143:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,143:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,145:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,148:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,149:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,149:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,151:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,154:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,155:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,155:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,157:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,160:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,161:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,162:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,163:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,166:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,167:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,167:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,169:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,172:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,173:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,174:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,175:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,178:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,179:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,179:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,181:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,184:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,185:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,185:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,187:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,190:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,190:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,191:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,192:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,195:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,196:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,196:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,198:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,201:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,202:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,202:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,204:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,207:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,207:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,208:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,210:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,214:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,215:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,215:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,217:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,220:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,221:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,222:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,223:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,227:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,228:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,228:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,230:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,233:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,233:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,234:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,235:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,238:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,239:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,239:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,241:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,244:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,245:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,245:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,246:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,250:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,250:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,251:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,252:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,255:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,255:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,256:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,257:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,260:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,261:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,261:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,263:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,265:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,266:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,266:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,268:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,272:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,273:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,273:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,274:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,277:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,278:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,278:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,280:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,283:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,283:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,284:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,285:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,288:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,288:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,289:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,290:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,293:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,294:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,294:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,296:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,298:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,299:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,299:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,301:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,304:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,304:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,305:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,306:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,309:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,309:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,310:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,311:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,314:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,315:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,315:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,317:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,320:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,320:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,321:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,322:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,325:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,325:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,326:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,327:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,330:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,331:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,331:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,334:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,338:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,338:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,339:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,341:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,344:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,345:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,345:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,347:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,350:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,350:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,351:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,352:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,355:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,356:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,356:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,357:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,361:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,361:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,361:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,363:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,366:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,366:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,367:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,368:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,371:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,372:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,373:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,374:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,377:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,378:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,378:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,380:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,382:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,383:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,383:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,385:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,388:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,389:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,389:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,390:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,393:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,394:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,394:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,396:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,399:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,400:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,400:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,402:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,405:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,405:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,405:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,407:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,410:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,412:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,412:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,414:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,418:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,418:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,419:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,420:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,423:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,424:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,424:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,426:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,429:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,429:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,430:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,431:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,434:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,435:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,435:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,437:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,440:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,440:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,441:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,442:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,445:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,445:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,446:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,447:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,450:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,450:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,451:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,452:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,455:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,456:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,456:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,457:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,460:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,461:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,461:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,462:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,465:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,466:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,466:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,467:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,471:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,471:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,471:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,473:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,475:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,476:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,476:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,478:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,481:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,481:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,482:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,483:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,486:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,487:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,487:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,489:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,492:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,493:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,494:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,497:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,498:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,498:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,500:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,503:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,503:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,504:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,505:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,508:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,509:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,509:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,511:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,514:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,514:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,515:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,516:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,519:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,520:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,520:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,521:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,524:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,525:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,525:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,527:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,531:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,532:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,532:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,533:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,537:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,537:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,538:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,540:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,543:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,544:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,544:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,546:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,549:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,549:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,550:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,551:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,554:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,554:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,555:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,556:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,559:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,560:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,560:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,562:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,565:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,566:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,566:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,568:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,571:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,571:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,572:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,573:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,576:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,577:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,577:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,578:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,581:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,582:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,582:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,583:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,586:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,587:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,587:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,588:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,591:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,592:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,592:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,593:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,596:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,596:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,597:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,598:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,601:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,601:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,603:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,606:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,606:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,606:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,608:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,611:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,611:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,612:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,613:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,616:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,617:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,617:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,618:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,621:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,622:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,622:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,624:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,627:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,627:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,628:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,629:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,632:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,632:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,633:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,634:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,637:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,637:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,638:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,639:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,642:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,642:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,643:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,644:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,647:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,648:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,648:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,650:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,653:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,653:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,654:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,655:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,658:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,658:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,659:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,660:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,664:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,664:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,665:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,666:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,669:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,670:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,670:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,671:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,674:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,675:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,675:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,677:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,679:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,680:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,680:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,682:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,685:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,685:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,686:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,687:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,690:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,690:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,691:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,693:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,696:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,697:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,697:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,699:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,702:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,703:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,703:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,705:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,708:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,708:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,709:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,711:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,714:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,715:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,715:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,717:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,719:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,720:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,721:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,722:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,725:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,726:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,727:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,728:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,731:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,732:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,733:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,734:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,737:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,738:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,739:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,740:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,743:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,743:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,744:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,745:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,748:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,749:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,749:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,751:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,754:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,754:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,755:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,757:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,760:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,760:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,761:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,762:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,765:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,765:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,765:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,767:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,769:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,770:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,770:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,771:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,775:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,775:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,775:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,776:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,779:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,780:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,780:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,781:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,784:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,785:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,785:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,787:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,790:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,790:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,790:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,792:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,794:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,795:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,795:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,796:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,799:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,800:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,800:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,802:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,805:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,805:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,806:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,807:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,810:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,811:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,811:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,812:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,815:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,816:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,816:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,818:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,821:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,821:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,822:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,823:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,826:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,826:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,827:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,828:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,832:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,832:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,834:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,837:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,837:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,838:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,839:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,842:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,842:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,843:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,844:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,847:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,848:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,848:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,850:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,853:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,854:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,854:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,856:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,859:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,859:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,860:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,861:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,864:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,864:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,865:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,866:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,869:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,869:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,870:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,871:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,874:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,874:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,875:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,876:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,879:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,879:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,879:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,881:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,883:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,884:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,884:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,885:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,888:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,889:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,889:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,890:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,893:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,894:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,894:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,895:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,898:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,898:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,899:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,900:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,903:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,903:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,903:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,905:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,907:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,908:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,908:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,910:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,912:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,913:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,913:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,915:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,918:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,918:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,919:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,920:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,923:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,923:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,924:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,925:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,927:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,928:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,928:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,929:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,932:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,933:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,933:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,934:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,937:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,937:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,938:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,939:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,943:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,943:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,943:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,945:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,948:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,948:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,949:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,950:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,953:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,953:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,954:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,955:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,958:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,959:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,959:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,961:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,964:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,964:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,965:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,966:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,969:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,970:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,970:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,973:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,976:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,977:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,977:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,978:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,982:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,982:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,983:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,984:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,987:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,987:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,988:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,989:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,992:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,993:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,993:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:11,995:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:11,998:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:11,998:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:11,999:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,000:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,003:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,003:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,003:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,004:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,007:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,008:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,009:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,010:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,013:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,014:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,014:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,016:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,019:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,019:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,020:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,021:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,024:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,024:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,025:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,026:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,029:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,030:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,031:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,032:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,035:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,036:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,036:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,038:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,041:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,041:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,042:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,047:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,050:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,051:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,051:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,054:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,057:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,057:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,058:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,061:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,064:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,064:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,065:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,066:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,069:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,070:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,070:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,072:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,075:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,075:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,076:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,077:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,080:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,081:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,081:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,083:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,086:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,086:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,087:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,089:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,092:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,093:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,093:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,095:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,099:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,099:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,100:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,101:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,104:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,105:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,105:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,107:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,110:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,111:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,111:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,113:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,116:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,117:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,117:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,118:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,121:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,122:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,123:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,124:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,127:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,128:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,129:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,130:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,133:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,134:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,134:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,136:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,139:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,139:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,140:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,142:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,145:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,145:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,146:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,147:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,150:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,150:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,151:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,152:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,155:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,155:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,156:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,157:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,160:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,161:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,161:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,162:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,165:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,166:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,166:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,167:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,170:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,171:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,171:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,172:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,175:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,175:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,176:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,177:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,179:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,180:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,180:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,182:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,185:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,185:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,186:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,187:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,190:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,191:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,191:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,192:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,195:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,196:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,196:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,197:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,201:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,201:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,202:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,203:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,206:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,207:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,207:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,208:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,211:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,212:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,212:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,213:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,217:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,217:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,218:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,219:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,222:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,223:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,223:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,224:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,229:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,229:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,230:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,231:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,235:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,235:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,236:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,237:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,240:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,241:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,241:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,243:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,246:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,246:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,247:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,248:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,251:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,252:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,252:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,254:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,257:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,257:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,258:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,259:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,263:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,263:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,264:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,266:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,269:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,269:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,270:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,271:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,275:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,275:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,276:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,277:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,280:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,281:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,281:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,283:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,286:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,287:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,287:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,289:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,291:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,292:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,292:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,294:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,297:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,297:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,298:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,299:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,302:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,303:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,304:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,305:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,308:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,309:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,309:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,311:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,314:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,315:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,315:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,317:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,320:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,321:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,321:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,322:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,326:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,326:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,326:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,328:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,331:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,331:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,331:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,333:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,336:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,336:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,337:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,340:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,343:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,344:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,347:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,350:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,351:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,351:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,353:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,356:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,356:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,357:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,358:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,361:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,362:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,362:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,363:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,367:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,367:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,368:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,369:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,372:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,372:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,373:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,374:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,377:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,378:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,378:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,380:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,383:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,383:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,384:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,386:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,389:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,389:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,390:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,391:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,394:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,395:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,395:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,397:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,400:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,400:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,401:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,402:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,405:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,406:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,406:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,407:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,411:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,411:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,412:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,413:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,416:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,417:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,417:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,419:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,421:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,422:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,422:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,423:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,426:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,426:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,427:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,428:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,431:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,431:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,432:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,436:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,436:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,437:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,438:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,441:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,441:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,441:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,443:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,445:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,446:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,446:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,447:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,450:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,451:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,451:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,452:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,455:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,456:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,456:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,457:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,460:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,460:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,461:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,462:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,465:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,466:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,466:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,467:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,470:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,471:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,471:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,472:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,475:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,475:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,476:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,477:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,480:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,480:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,481:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,482:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,485:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,485:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,486:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,487:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,491:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,491:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,492:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,493:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,496:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,497:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,498:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,499:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,502:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,503:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,503:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,504:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,507:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,508:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,509:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,510:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,513:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,513:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,514:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,515:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,518:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,518:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,518:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,520:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,523:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,523:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,523:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,525:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,528:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,528:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,528:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,530:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,533:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,533:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,533:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,535:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,538:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,538:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,538:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,540:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,542:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,543:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,543:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,545:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,548:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,548:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,548:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,549:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,552:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,553:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,553:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,555:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,558:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,558:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,559:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,560:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,563:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,564:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,564:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,566:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,569:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,569:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,570:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,571:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,575:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,575:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,575:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,577:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,580:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,581:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,581:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,582:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,586:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,586:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,587:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,588:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,592:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,592:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,593:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,594:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,597:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,598:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,598:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,599:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,603:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,603:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,604:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,605:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,609:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,609:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,610:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,611:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,615:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,615:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,615:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,617:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,620:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,621:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,621:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,623:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,626:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,627:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,627:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,629:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,632:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,632:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,633:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,634:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,638:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,638:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,639:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,640:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,643:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,643:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,644:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,645:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,648:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,649:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,649:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,651:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,654:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,655:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,655:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,656:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,660:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,660:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,661:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,662:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,665:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,666:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,666:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,667:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,671:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,671:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,672:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,673:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,676:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,676:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,677:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,678:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,681:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,681:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,682:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,683:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,686:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,686:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,687:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,688:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,691:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,691:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,692:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,693:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,696:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,696:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,697:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,698:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,701:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,701:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,701:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,703:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,705:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,706:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,707:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,708:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,711:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,712:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,712:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,714:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,717:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,717:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,718:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,719:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,723:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,723:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,724:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,726:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,729:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,730:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,730:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,731:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,735:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,735:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,735:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,737:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,740:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,740:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,740:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,743:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,745:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,746:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,746:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,747:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,750:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,751:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,751:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,753:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,756:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,756:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,757:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,758:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,761:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,761:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,762:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,763:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,766:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,766:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,767:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,769:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,772:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,772:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,772:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,774:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,777:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,777:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,778:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,779:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,782:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,783:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,783:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,784:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,787:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,788:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,788:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,789:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,793:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,793:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,794:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,795:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,798:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,798:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,799:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,800:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,802:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,803:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,803:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,804:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,807:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,808:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,808:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,809:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,812:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,812:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,813:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,814:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,816:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,817:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,817:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:12,818:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:12,821:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:12,822:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:12,822:DEBUG:
    Ignoring line no. 24: 35
    


.. parsed-literal::

    5.54 ms ± 218 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


Read raw:

.. code:: ipython3

    %%timeit
    EbasNasaAmesFile(file=ebasdir+filename,
                          only_head=False,          #set True if you only want to import header
                          replace_invalid_nan=False, #replace invalid values with NaNs
                          convert_timestamps=False,  #compute datetime64 timestamps from numerical values
                          decode_flags=False,        #decode all flags (e.g. 0.111222333 -> 111 222 333)
                          verbose=False)


.. parsed-literal::

    2018-09-07 17:45:14,412:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:14,415:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:14,416:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:14,416:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:14,417:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:14,417:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:14,493:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:14,497:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:14,497:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:14,498:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:14,498:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:14,499:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:14,559:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:14,563:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:14,564:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:14,564:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:14,565:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:14,565:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:14,613:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:14,617:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:14,618:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:14,618:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:14,619:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:14,619:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:14,705:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:14,710:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:14,710:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:14,711:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:14,711:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:14,712:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:14,760:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:14,763:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:14,763:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:14,764:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:14,764:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:14,765:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:14,814:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:14,818:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:14,819:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:14,819:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:14,820:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:14,821:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:14,871:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:14,875:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:14,875:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:14,876:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:14,876:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:14,877:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:14,929:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:14,933:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:14,933:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:14,934:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:14,934:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:14,935:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:14,985:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:14,988:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:14,989:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:14,989:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:14,990:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:14,990:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:15,041:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:15,044:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:15,050:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:15,052:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:15,053:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:15,054:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:15,113:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:15,117:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:15,117:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:15,118:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:15,118:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:15,119:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:15,164:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:15,169:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:15,169:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:15,170:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:15,170:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:15,170:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:15,217:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:15,220:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:15,221:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:15,221:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:15,222:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:15,222:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:15,268:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:15,272:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:15,273:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:15,273:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:15,274:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:15,274:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:15,334:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:15,337:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:15,338:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:15,340:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:15,340:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:15,340:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:15,428:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:15,432:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:15,432:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:15,433:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:15,433:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:15,434:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:15,481:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:15,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:15,493:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:15,494:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:15,494:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:15,495:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:15,571:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:15,579:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:15,581:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:15,581:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:15,582:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:15,583:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:15,659:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:15,663:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:15,663:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:15,664:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:15,664:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:15,665:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:15,720:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:15,723:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:15,724:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:15,724:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:15,725:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:15,725:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:15,788:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:15,792:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:15,792:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:15,793:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:15,793:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:15,793:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:15,840:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:15,844:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:15,845:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:15,845:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:15,846:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:15,847:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:15,933:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:15,937:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:15,938:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:15,939:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:15,940:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:15,940:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,023:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,026:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,027:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,027:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,028:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,028:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,089:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,093:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,093:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,094:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,094:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,095:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,155:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,158:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,159:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,159:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,160:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,161:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,215:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,219:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,219:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,219:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,220:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,220:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,265:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,269:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,269:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,270:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,270:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,271:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,315:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,319:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,319:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,319:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,320:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,320:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,365:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,368:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,369:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,369:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,369:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,370:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,414:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,427:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,428:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,428:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,429:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,429:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,478:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,481:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,482:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,482:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,483:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,483:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,529:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,533:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,533:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,533:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,534:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,534:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,579:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,582:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,582:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,583:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,583:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,584:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,628:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,631:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,631:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,632:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,632:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,633:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,677:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,680:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,681:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,681:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,682:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,683:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,727:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,730:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,731:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,731:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,732:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,732:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,777:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,781:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,781:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,781:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,782:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,782:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,827:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,831:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,832:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,832:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,833:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,878:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,882:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,882:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,883:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,883:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,884:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,929:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,932:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,932:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,933:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,933:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,934:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:16,982:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:16,985:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:16,986:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:16,986:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:16,987:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:16,987:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,033:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,036:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,036:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,037:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,038:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,038:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,092:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,096:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,096:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,097:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,097:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,097:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,143:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,148:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,148:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,149:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,149:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,150:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,214:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,218:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,218:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,219:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,219:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,219:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,265:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,268:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,269:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,269:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,270:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,270:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,316:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,319:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,320:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,321:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,321:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,322:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,367:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,371:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,371:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,371:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,372:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,372:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,418:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,423:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,424:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,424:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,425:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,425:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,496:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,500:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,500:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,501:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,501:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,502:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,547:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,551:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,551:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,552:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,552:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,553:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,598:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,602:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,602:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,602:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,603:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,603:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,648:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,652:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,652:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,653:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,653:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,654:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,699:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,703:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,703:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,704:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,704:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,705:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,751:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,754:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,755:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,755:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,756:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,756:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,802:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,805:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,805:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,805:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,806:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,806:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,851:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,854:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,855:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,855:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,856:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,856:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,902:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,905:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,905:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,906:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,907:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,907:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:17,972:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:17,976:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:17,976:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:17,977:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:17,978:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:17,978:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,047:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,050:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,051:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,051:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,052:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,052:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,122:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,125:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,126:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,127:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,127:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,128:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,191:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,194:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,195:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,195:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,196:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,196:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,262:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,266:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,266:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,267:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,267:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,268:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,313:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,317:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,317:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,318:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,318:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,318:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,364:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,367:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,368:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,368:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,369:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,369:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,416:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,419:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,420:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,420:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,421:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,421:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,482:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,486:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,487:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,487:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,488:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,489:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,545:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,548:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,549:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,550:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,550:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,551:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,598:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,601:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,602:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,602:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,602:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,647:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,651:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,651:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,652:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,652:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,653:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,698:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,701:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,701:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,703:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,703:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,749:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,753:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,754:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,754:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,755:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,756:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,801:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,804:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,805:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,805:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,805:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,806:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,850:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,854:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,854:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,854:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,855:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,855:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,901:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,904:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,905:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,905:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,905:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,906:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:18,977:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:18,981:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:18,981:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:18,982:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:18,983:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:18,983:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:19,056:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:19,060:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:19,060:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:19,061:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:19,062:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:19,062:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:19,136:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:19,140:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:19,140:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:19,140:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:19,141:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:19,141:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:19,186:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:19,190:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:19,190:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:19,191:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:19,191:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:19,192:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    58.9 ms ± 4.81 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


Perform all operations:

.. code:: ipython3

    %%timeit
    EbasNasaAmesFile(file=ebasdir+filename,
                          only_head=False,          #set True if you only want to import header
                          replace_invalid_nan=True, #replace invalid values with NaNs
                          convert_timestamps=True,  #compute datetime64 timestamps from numerical values
                          decode_flags=True,        #decode all flags (e.g. 0.111222333 -> 111 222 333)
                          verbose=False)


.. parsed-literal::

    2018-09-07 17:45:19,472:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:19,476:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:19,476:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:19,477:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:19,477:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:19,478:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:19,536:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:19,540:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:19,540:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:19,541:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:19,541:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:19,541:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:19,607:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:19,610:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:19,611:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:19,612:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:19,613:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:19,613:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:19,668:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:19,672:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:19,672:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:19,672:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:19,673:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:19,673:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:19,731:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:19,734:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:19,735:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:19,736:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:19,736:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:19,738:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:19,791:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:19,795:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:19,795:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:19,796:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:19,796:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:19,797:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:19,850:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:19,854:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:19,855:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:19,855:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:19,857:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:19,857:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:19,950:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:19,953:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:19,954:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:19,955:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:19,955:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:19,956:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:20,012:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:20,016:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:20,016:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:20,017:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:20,017:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:20,018:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:20,073:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:20,076:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:20,076:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:20,077:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:20,078:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:20,079:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:20,153:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:20,157:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:20,158:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:20,158:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:20,159:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:20,159:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:20,250:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:20,254:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:20,255:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:20,255:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:20,256:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:20,256:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:20,317:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:20,321:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:20,321:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:20,322:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:20,322:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:20,323:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:20,383:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:20,386:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:20,387:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:20,388:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:20,389:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:20,390:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:20,446:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:20,450:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:20,451:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:20,452:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:20,452:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:20,453:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:20,508:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:20,512:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:20,512:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:20,513:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:20,514:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:20,514:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:20,570:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:20,574:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:20,575:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:20,575:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:20,575:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:20,576:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:20,645:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:20,648:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:20,649:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:20,649:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:20,650:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:20,650:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:20,707:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:20,712:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:20,712:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:20,713:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:20,713:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:20,714:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:20,791:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:20,796:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:20,796:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:20,797:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:20,797:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:20,798:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:20,853:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:20,856:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:20,857:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:20,858:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:20,858:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:20,858:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:20,940:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:20,949:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:20,949:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:20,950:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:20,950:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:20,951:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:21,004:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:21,011:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:21,013:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:21,014:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:21,015:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:21,016:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:21,079:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:21,085:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:21,086:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:21,087:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:21,087:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:21,088:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:21,142:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:21,150:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:21,151:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:21,151:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:21,152:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:21,152:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:21,204:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:21,211:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:21,211:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:21,212:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:21,212:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:21,213:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:21,276:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:21,284:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:21,285:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:21,286:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:21,288:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:21,289:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:21,356:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:21,364:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:21,365:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:21,365:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:21,365:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:21,366:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:21,420:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:21,427:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:21,428:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:21,430:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:21,431:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:21,432:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:21,494:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:21,501:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:21,502:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:21,504:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:21,505:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:21,507:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:21,572:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:21,578:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:21,578:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:21,579:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:21,579:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:21,580:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:21,637:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:21,644:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:21,644:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:21,645:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:21,645:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:21,645:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:21,732:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:21,739:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:21,741:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:21,742:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:21,743:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:21,745:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:21,832:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:21,838:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:21,838:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:21,839:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:21,839:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:21,839:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:21,894:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:21,901:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:21,903:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:21,905:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:21,906:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:21,907:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:21,971:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:21,978:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:21,978:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:21,979:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:21,979:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:21,980:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:22,033:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:22,040:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:22,040:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:22,041:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:22,041:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:22,041:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:22,107:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:22,113:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:22,113:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:22,113:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:22,114:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:22,114:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:22,166:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:22,172:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:22,173:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:22,173:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:22,174:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:22,174:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:22,228:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:22,235:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:22,235:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:22,236:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:22,236:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:22,237:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:22,291:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:22,298:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:22,300:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:22,301:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:22,302:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:22,303:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:22,373:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:22,379:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:22,380:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:22,380:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:22,381:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:22,381:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:22,434:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:22,442:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:22,442:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:22,443:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:22,443:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:22,443:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:22,507:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:22,515:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:22,515:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:22,516:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:22,516:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:22,517:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:22,571:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:22,578:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:22,579:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:22,579:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:22,579:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:22,580:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:22,634:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:22,641:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:22,642:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:22,644:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:22,645:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:22,645:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:22,764:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:22,771:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:22,773:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:22,775:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:22,776:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:22,778:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:22,857:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:22,864:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:22,866:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:22,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:22,868:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:22,869:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:22,929:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:22,938:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:22,939:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:22,939:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:22,940:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:22,940:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:22,994:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:23,001:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:23,001:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:23,001:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:23,002:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:23,002:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:23,056:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:23,063:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:23,063:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:23,063:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:23,064:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:23,064:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:23,121:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:23,128:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:23,129:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:23,131:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:23,132:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:23,133:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:23,193:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:23,199:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:23,200:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:23,200:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:23,200:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:23,201:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:23,253:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:23,259:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:23,259:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:23,260:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:23,260:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:23,261:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:23,313:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:23,319:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:23,321:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:23,322:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:23,323:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:23,324:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:23,392:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:23,400:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:23,402:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:23,403:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:23,404:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:23,405:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:23,464:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:23,471:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:23,473:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:23,474:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:23,476:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:23,477:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:23,540:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:23,548:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:23,549:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:23,550:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:23,550:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:23,550:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:23,628:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:23,636:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:23,638:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:23,640:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:23,641:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:23,643:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:23,776:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:23,784:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:23,786:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:23,788:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:23,789:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:23,791:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:23,865:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:23,871:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:23,872:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:23,873:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:23,873:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:23,874:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:23,937:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:23,944:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:23,945:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:23,947:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:23,948:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:23,949:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:24,014:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:24,021:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:24,022:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:24,023:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:24,024:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:24,025:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:24,084:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:24,091:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:24,093:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:24,095:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:24,096:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:24,097:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:24,158:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:24,165:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:24,165:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:24,166:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:24,166:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:24,167:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:24,221:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:24,227:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:24,228:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:24,228:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:24,228:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:24,229:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:24,282:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:24,289:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:24,290:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:24,290:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:24,291:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:24,291:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:24,346:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:24,353:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:24,354:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:24,354:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:24,355:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:24,355:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:24,408:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:24,415:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:24,415:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:24,416:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:24,416:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:24,416:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:24,471:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:24,479:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:24,480:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:24,480:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:24,480:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:24,481:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:24,547:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:24,555:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:24,556:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:24,556:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:24,557:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:24,557:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:24,612:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:24,619:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:24,620:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:24,621:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:24,621:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:24,622:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:24,677:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:24,684:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:24,686:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:24,687:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:24,688:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:24,689:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:24,801:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:24,810:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:24,812:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:24,814:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:24,815:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:24,817:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:24,904:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:24,910:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:24,911:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:24,912:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:24,912:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:24,913:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:24,970:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:24,976:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:24,978:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:24,980:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:24,981:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:24,982:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:25,044:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:25,050:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:25,051:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:25,051:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:25,052:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:25,052:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:25,109:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:25,115:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:25,116:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:25,116:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:25,117:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:25,117:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:25,183:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:25,190:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:25,190:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:25,191:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:25,191:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:25,191:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:25,244:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:25,251:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:25,255:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:25,256:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:25,257:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:25,259:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-07 17:45:25,325:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-07 17:45:25,331:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-07 17:45:25,333:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-07 17:45:25,334:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-07 17:45:25,336:DEBUG:
    REACHED DATA BLOCK
    2018-09-07 17:45:25,337:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    73.8 ms ± 5.17 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

