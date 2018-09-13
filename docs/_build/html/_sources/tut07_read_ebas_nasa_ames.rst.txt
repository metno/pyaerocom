
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

    2018-09-13 12:07:03,951:INFO:
    Reading aliases ini file: /home/jonasg/github/pyaerocom/pyaerocom/data/aliases.ini


.. parsed-literal::

    Elapsed time init all variables: 0.02491593360900879 s


.. parsed-literal::

    2018-09-13 12:07:04,709:WARNING:
    geopy library is not available. Aeolus data read not enabled
    2018-09-13 12:07:04,760:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:04,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:04,833:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:04,835:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:04,837:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:04,839:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    Elapsed time init pyaerocom: 0.8183541297912598 s
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
                  <pyaerocom.io.ebas_nasa_ames.EbasFlagCol at 0x7f48ad8ed710>)])



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

    2018-09-13 12:07:05,079:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,084:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,085:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,085:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,087:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,091:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,091:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,091:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,093:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,097:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,098:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,098:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,101:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,106:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,106:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,107:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,109:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,114:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,115:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,115:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,117:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,121:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,122:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,122:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,124:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,129:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,130:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,130:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,132:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,135:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,136:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,136:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,138:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,144:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,144:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,145:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,147:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,152:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,153:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,153:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,155:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,160:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,161:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,161:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,164:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,169:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,170:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,170:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,173:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,177:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,179:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,181:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,184:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,189:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,191:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,193:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,196:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,202:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,204:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,206:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,209:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,214:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,216:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,217:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,222:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,227:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,229:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,230:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,234:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,239:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,241:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,242:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,245:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,251:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,252:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,254:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,257:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,264:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,265:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,267:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,272:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,277:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,279:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,280:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,283:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,288:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,289:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,290:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,293:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,297:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,298:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,299:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,301:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,306:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,306:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,307:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,308:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,313:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,314:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,315:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,318:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,323:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,324:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,324:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,326:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,330:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,331:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,331:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,333:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,337:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,338:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,338:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,341:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,345:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,346:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,346:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,348:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,353:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,355:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,357:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,361:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,367:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,369:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,371:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,374:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,380:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,381:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,383:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,386:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,392:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,394:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,396:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,401:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,407:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,408:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,409:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,412:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,417:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,419:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,420:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,422:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,427:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,428:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,429:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,431:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,435:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,436:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,437:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,438:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,442:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,443:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,443:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,445:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,449:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,449:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,450:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,452:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,457:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,459:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,460:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,463:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,468:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,468:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,469:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,471:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,475:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,476:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,476:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,478:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,483:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,483:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,484:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,486:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,490:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,490:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,491:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,492:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,497:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,497:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,498:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,500:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,504:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,504:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,505:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,506:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,511:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,511:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,512:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,514:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,519:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,519:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,520:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,522:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,526:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,527:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,527:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,529:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,535:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,535:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,536:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,538:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,542:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,544:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,545:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,550:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,555:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,557:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,558:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,562:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,567:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,568:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,569:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,572:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,577:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,577:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,578:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,581:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,585:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,586:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,587:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,588:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,595:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,596:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,598:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,602:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,602:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,603:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,605:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,609:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,610:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,611:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,614:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,618:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,619:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,620:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,622:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,626:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,627:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,627:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,629:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,634:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,635:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,635:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,638:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,642:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,642:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,643:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,645:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,649:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,650:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,650:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,652:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,656:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,657:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,658:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,660:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,665:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,665:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,666:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,668:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,672:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,674:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,675:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,679:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,684:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,685:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,686:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,689:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,693:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,693:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,694:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,697:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,701:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,702:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,705:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,710:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,710:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,711:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,714:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,718:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,718:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,719:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,722:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,726:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,727:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,727:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,729:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,733:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,734:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,735:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,737:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,740:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,741:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,741:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,744:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,750:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,751:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,751:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,768:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,776:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,778:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,780:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,784:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,791:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,793:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,794:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,799:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,806:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,808:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,810:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,815:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,822:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,823:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,824:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,826:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,830:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,830:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,831:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,834:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,838:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,839:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,839:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,842:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,847:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,849:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,851:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,855:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,862:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,864:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,865:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,869:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,874:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,875:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,877:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,882:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,887:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,889:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,891:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,894:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,900:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,901:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,903:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,907:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,908:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,908:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,911:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,915:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,916:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,916:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,920:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,927:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,929:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,930:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,934:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,940:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,942:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,944:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,947:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,953:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,955:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,956:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,960:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,966:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,968:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,969:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,973:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,978:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,979:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,980:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,983:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,989:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,989:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,990:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:05,992:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:05,997:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:05,998:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:05,998:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,001:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,006:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,007:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,007:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,012:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,017:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,017:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,018:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,021:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,025:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,026:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,026:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,029:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,033:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,034:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,034:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,037:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,043:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,044:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,045:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,047:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,053:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,054:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,055:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,058:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,062:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,064:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,065:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,067:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,071:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,072:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,072:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,075:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,079:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,080:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,080:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,087:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,091:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,092:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,093:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,095:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,099:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,099:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,100:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,102:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,107:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,107:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,108:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,110:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,114:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,115:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,116:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,118:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,123:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,124:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,124:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,126:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,131:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,132:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,133:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,135:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,139:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,140:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,141:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,143:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,147:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,148:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,148:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,151:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,155:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,155:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,156:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,158:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,162:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,162:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,163:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,165:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,169:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,170:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,170:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,173:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,178:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,178:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,179:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,181:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,186:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,187:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,187:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,189:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,194:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,196:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,197:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,207:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,209:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,211:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,214:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,220:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,222:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,223:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,228:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,235:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,237:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,238:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,242:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,248:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,250:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,251:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,256:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,261:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,263:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,264:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,269:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,274:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,275:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,276:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,278:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,282:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,283:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,284:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,286:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,292:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,292:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,293:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,296:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,301:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,301:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,302:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,305:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,310:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,310:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,311:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,313:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,317:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,319:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,321:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,325:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,332:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,334:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,336:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,340:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,346:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,348:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,350:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,354:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,361:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,362:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,364:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,368:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,375:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,376:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,378:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,382:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,388:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,390:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,391:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,395:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,401:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,403:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,404:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,407:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,413:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,414:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,415:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,419:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,426:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,426:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,427:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,430:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,437:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,437:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,438:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,442:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,449:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,450:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,450:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,453:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,457:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,458:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,458:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,460:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,468:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,470:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,471:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,473:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,477:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,478:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,478:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,480:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,485:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,486:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,487:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,489:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,493:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,494:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,494:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,497:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,501:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,502:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,503:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,505:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,509:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,510:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,511:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,513:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,517:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,517:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,518:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,520:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,524:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,525:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,526:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,528:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,532:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,533:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,533:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,536:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,541:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,542:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,542:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,545:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,550:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,550:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,551:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,554:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,558:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,559:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,560:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,562:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,567:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,569:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,570:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,574:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,581:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,582:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,584:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,589:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,599:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,601:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,603:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,608:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,615:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,617:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,619:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,623:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,629:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,631:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,632:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,636:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,643:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,644:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,645:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,648:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,653:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,654:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,655:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,658:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,665:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,666:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,667:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,670:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,675:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,676:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,677:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,679:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,685:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,686:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,687:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,690:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,698:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,699:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,700:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,702:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,708:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,709:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,710:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,712:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,717:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,719:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,721:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,725:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,731:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,733:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,735:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,739:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,745:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,748:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,750:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,753:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,759:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,761:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,763:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,786:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,792:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,793:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,795:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,799:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,807:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,809:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,811:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,814:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,820:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,822:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,824:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,827:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,837:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,839:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,841:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,845:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,851:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,853:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,854:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,859:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,864:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,866:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,870:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,875:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,876:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,877:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,880:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,887:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,888:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,889:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,894:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,900:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,901:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,905:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,910:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,911:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,911:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,915:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,921:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,922:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,923:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,926:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,932:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,934:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,935:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,939:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,946:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,948:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,950:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,954:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,959:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,961:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,963:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,967:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,972:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,974:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,976:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,980:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,985:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:06,987:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:06,988:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:06,991:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:06,997:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,000:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,002:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,006:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,014:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,016:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,017:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,021:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,026:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,027:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,029:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,032:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,037:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,039:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,041:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,046:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,051:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,053:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,055:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,058:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,064:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,065:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,067:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,071:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,078:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,080:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,081:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,085:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,093:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,095:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,096:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,101:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,106:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,107:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,108:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,112:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,118:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,119:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,119:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,122:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,128:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,129:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,129:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,131:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,136:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,136:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,137:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,139:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,143:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,144:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,144:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,146:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,151:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,152:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,152:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,154:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,159:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,159:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,160:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,162:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,165:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,166:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,166:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,168:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,171:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,172:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,173:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,174:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,178:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,179:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,180:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,181:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,186:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,186:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,187:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,189:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,193:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,193:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,194:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,198:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,204:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,205:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,205:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,208:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,214:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,214:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,215:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,217:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,221:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,222:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,223:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,225:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,230:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,231:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,231:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,233:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,238:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,239:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,239:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,241:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,245:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,245:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,246:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,248:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,253:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,254:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,254:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,257:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,263:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,263:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,264:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,266:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,270:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,271:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,271:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,273:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,277:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,279:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,281:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,286:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,292:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,294:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,296:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,301:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,307:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,309:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,311:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,314:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,320:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,322:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,324:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,327:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,332:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,334:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,335:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,338:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,344:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,345:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,346:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,349:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,354:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,356:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,357:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,361:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,366:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,369:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,370:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,373:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,378:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,379:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,380:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,382:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,388:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,388:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,389:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,392:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,398:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,399:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,399:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,401:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,405:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,406:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,407:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,408:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,413:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,413:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,414:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,417:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,422:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,423:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,424:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,425:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,430:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,430:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,431:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,437:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,439:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,441:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,444:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,450:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,452:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,453:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,457:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,463:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,464:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,466:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,470:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,476:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,477:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,479:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,483:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,489:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,490:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,492:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,496:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,502:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,504:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,505:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,507:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,512:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,513:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,514:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,517:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,521:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,522:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,523:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,526:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,531:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,532:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,533:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,535:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,541:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,542:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,542:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,545:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,551:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,552:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,553:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,557:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,564:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,565:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,566:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,569:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,577:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,578:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,579:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,583:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,589:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,590:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,591:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,595:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,600:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,601:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,602:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,605:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,610:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,611:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,612:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,615:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,621:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,622:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,623:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,625:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,630:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,631:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,632:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,635:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,644:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,646:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,648:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,651:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,656:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,658:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,660:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,664:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,670:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,672:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,673:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,677:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,683:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,684:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,686:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,688:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,692:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,693:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,694:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,696:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,702:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,702:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,703:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,705:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,712:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,714:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,715:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,719:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,725:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,727:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,728:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,733:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,739:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,741:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,742:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,746:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,753:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,754:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,756:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,759:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,765:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,766:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,767:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,769:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,774:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,775:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,776:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,797:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,803:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,804:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,804:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,807:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,814:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,815:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,816:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,821:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,829:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,830:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,831:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,833:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,841:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,842:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,843:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,848:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,853:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,854:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,855:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,858:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,867:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,868:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,872:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,877:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,878:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,879:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,882:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,888:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,889:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,890:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,892:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,897:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,899:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,900:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,904:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,913:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,915:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,915:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,920:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,924:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,926:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,927:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,931:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,939:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,940:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,941:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,945:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,950:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,952:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,952:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,956:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,964:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,965:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,966:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,969:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,973:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,974:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,976:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,978:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,985:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,987:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:07,988:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:07,991:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:07,997:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:07,998:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,000:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,003:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,009:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,010:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,011:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,013:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,018:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,019:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,020:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,023:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,028:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,029:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,031:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,034:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,038:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,040:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,040:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,044:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,050:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,052:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,053:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,057:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,064:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,066:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,067:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,071:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,078:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,080:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,081:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,085:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,090:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,092:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,094:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,101:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,108:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,110:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,111:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,115:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,121:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,123:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,125:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,128:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,134:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,136:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,137:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,139:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,144:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,145:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,146:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,149:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,154:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,155:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,156:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,159:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,163:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,165:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,166:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,169:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,173:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,174:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,176:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,179:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,186:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,188:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,189:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,191:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,195:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,196:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,197:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,202:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,208:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,209:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,211:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,214:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,221:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,222:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,223:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,226:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,231:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,232:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,233:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,238:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,243:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,244:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,245:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,248:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,254:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,255:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,256:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,259:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,263:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,265:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,266:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,269:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,274:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,276:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,277:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,279:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,285:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,287:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,288:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,292:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,298:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,299:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,300:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,304:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,309:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,311:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,312:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,315:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,319:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,321:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,322:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,324:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,327:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,329:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,329:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,332:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,336:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,337:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,338:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,341:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,345:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,347:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,348:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,350:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,356:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,357:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,358:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,361:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,367:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,368:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,369:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,372:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,376:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,377:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,379:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,381:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,386:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,388:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,389:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,391:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,399:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,400:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,402:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,405:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,410:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,411:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,412:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,416:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,420:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,422:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,423:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,426:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,432:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,434:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,435:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,439:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,446:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,447:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,448:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,451:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,456:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,457:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,458:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,461:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,466:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,467:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,468:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,471:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,475:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,477:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,478:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,481:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,487:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,488:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,489:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,492:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,498:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,499:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,499:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,502:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,508:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,509:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,510:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,513:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,517:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,519:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,520:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,523:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,529:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,531:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,532:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,535:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,540:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,542:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,542:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,545:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,549:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,550:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,551:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,554:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,559:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,560:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,561:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,564:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,570:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,572:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,574:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,577:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,583:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,585:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,586:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,591:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,597:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,599:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,601:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,606:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,614:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,615:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,617:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,620:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,627:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,629:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,631:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,639:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,645:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,647:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,648:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,652:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,658:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,660:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,662:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,665:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,671:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,673:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,675:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,678:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,684:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,685:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,686:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,689:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,694:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,695:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,696:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,698:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,703:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,704:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,704:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,707:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,712:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,713:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,714:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,717:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,723:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,723:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,724:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,727:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,732:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,734:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,737:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,740:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,747:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,749:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,751:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,756:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,761:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,763:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,765:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,769:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,775:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,777:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,778:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,782:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,786:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,787:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,788:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,808:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,815:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,816:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,817:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,820:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,824:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,825:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,826:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,830:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,835:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,836:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,837:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,840:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,843:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,845:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,846:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,848:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,854:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,856:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,857:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,859:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,868:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,869:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,873:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,879:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,881:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,883:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,887:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,893:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,894:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,896:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,899:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,904:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,906:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,907:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,910:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,916:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,917:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,918:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,921:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,926:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,926:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,927:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,930:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,934:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,935:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,936:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,940:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,945:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,946:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,947:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,950:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,955:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,957:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,958:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,960:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,965:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,966:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,967:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,972:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,979:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,979:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,980:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,983:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,988:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,989:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:08,990:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:08,992:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:08,997:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:08,999:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,001:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,005:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,012:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,015:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,017:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,023:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,030:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,032:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,033:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,037:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,043:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,045:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,046:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,052:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,058:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,060:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,061:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,065:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,072:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,074:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,076:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,080:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,089:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,091:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,092:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,097:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,102:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,104:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,106:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,116:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,123:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,124:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,126:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,130:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,138:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,139:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,140:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,143:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,149:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,151:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,152:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,155:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,164:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,165:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,166:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,170:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,180:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,182:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,183:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,186:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,193:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,194:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,196:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,200:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,209:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,212:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,213:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,218:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,226:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,228:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,230:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,234:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,240:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,242:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,244:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,248:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,253:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,255:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,257:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,260:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,267:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,269:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,271:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,276:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,281:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,283:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,285:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,289:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,294:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,296:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,300:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,304:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,310:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,312:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,313:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,317:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,323:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,325:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,327:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,331:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,336:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,338:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,339:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,343:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,348:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,349:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,349:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,352:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,358:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,358:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,359:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,361:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,366:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,367:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,367:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,369:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,374:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,374:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,375:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,378:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,382:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,382:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,383:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,385:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,391:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,391:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,392:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,394:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,398:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,399:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,399:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,401:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,406:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,407:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,408:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,411:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,416:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,417:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,418:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,421:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,426:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,427:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,427:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,429:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,434:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,435:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,435:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,437:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,441:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,442:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,442:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,444:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,449:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,450:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,450:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,452:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,457:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,458:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,458:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,461:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,465:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,466:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,467:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,469:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,472:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,473:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,474:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,476:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,481:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,482:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,482:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,484:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,488:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,489:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,489:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,492:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,496:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,497:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,497:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,499:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,503:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,504:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,504:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,507:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,511:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,511:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,512:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,514:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,518:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,518:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,519:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,521:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,526:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,526:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,527:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,529:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,533:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,534:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,535:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,538:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,544:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,545:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,547:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,551:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,557:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,559:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,561:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,565:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,571:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,572:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,573:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,576:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,581:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,582:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,583:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,585:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,589:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,590:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,590:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,592:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,598:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,600:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,601:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,605:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,610:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,613:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,614:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,617:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,623:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,625:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,626:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,629:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,635:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,636:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,637:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,641:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,647:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,648:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,649:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,652:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,657:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,658:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,659:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,662:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,666:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,668:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,668:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,672:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,677:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,678:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,678:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,681:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,686:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,686:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,687:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,689:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,694:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,694:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,695:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,697:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,700:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,701:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,703:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,708:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,709:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,709:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,711:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,716:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,716:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,717:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,719:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,723:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,724:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,724:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,726:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,730:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,731:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,732:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,734:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,738:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,739:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,740:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,741:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,747:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,747:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,748:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,749:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,753:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,754:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,754:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,756:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,760:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,761:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,761:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,763:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,768:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,768:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,769:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,771:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,775:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,776:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,776:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,778:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,783:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,783:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,784:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,786:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,790:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,790:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,791:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,793:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,797:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,799:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,800:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,816:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,822:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,824:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,825:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,829:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,835:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,836:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,838:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,842:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,848:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,850:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,851:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,855:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,861:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,862:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,864:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,867:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,872:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,874:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,876:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,879:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,886:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,887:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,888:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,889:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,895:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,896:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,897:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,899:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,904:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,905:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,905:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,908:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,912:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,913:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,914:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,916:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,922:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,923:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,923:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,926:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,930:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,931:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,931:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,933:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,938:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,938:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,939:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,941:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,947:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,948:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,948:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,951:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,955:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,955:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,956:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,958:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,962:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,963:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,964:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,966:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,970:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,971:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,972:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,974:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,978:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,979:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,980:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,982:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,987:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,988:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,988:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,991:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:09,995:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:09,996:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:09,996:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:09,998:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,003:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,004:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,004:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,006:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,011:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,012:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,012:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,014:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,019:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,020:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,020:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,023:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,028:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,029:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,029:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,032:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,038:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,039:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,039:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,041:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,045:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,046:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,046:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,048:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,053:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,054:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,054:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,056:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,061:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,062:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,062:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,064:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,069:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,070:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,070:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,072:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,077:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,077:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,078:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,080:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,085:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,086:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,087:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,089:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,093:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,094:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,095:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,098:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,103:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,103:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,104:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,106:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,112:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,112:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,113:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,122:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,127:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,128:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,128:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,131:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,137:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,138:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,138:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,142:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,147:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,147:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,148:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,150:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,154:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,155:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,156:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,158:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,164:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,165:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,165:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,168:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,172:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,174:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,176:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,180:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,190:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,191:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,195:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,200:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,202:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,204:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,209:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,217:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,218:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,220:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,224:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,229:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,230:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,231:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,234:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,239:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,240:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,241:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,243:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,250:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,251:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,252:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,254:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,260:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,261:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,262:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,265:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,271:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,273:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,275:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,280:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,287:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,289:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,292:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,295:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,301:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,303:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,304:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,306:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,311:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,312:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,313:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,315:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,320:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,321:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,321:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,323:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,327:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,330:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,332:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,336:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,346:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,347:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,352:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,358:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,359:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,360:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,363:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,370:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,371:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,371:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,373:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,379:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,379:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,380:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,385:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,390:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,390:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,391:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,394:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,399:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,400:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,400:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,403:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,407:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,409:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,411:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,414:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,420:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,422:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,425:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,428:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,433:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,435:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,437:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,441:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,446:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,448:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,449:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,452:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,458:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,459:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,461:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,463:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,468:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,469:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,471:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,474:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,478:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,479:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,480:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,482:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,486:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,487:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,487:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,490:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,493:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,494:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,494:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,496:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,499:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,500:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,500:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,502:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,505:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,506:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,506:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,508:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,513:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,514:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,516:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,519:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,524:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,526:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,526:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,529:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,533:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,534:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,535:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,536:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,540:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,540:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,541:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,542:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,546:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,547:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,547:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,549:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,553:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,554:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,554:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,556:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,560:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,561:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,562:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,564:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,567:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,568:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,569:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,570:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,574:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,575:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,576:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,577:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,583:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,584:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,584:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,587:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,592:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,592:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,593:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,595:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,599:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,599:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,600:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,602:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,605:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,606:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,607:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,610:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,615:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,619:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,623:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,628:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,635:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,638:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,640:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,646:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,652:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,655:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,657:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,662:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,668:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,671:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,673:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,677:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,683:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,686:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,688:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,692:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,697:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,699:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,701:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,706:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,711:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,712:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,713:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,715:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,720:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,721:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,722:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,724:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,729:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,730:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,730:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,733:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,737:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,738:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,739:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,741:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,746:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,746:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,747:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,749:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,754:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,755:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,755:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,757:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,761:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,762:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,763:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,765:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,770:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,771:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,772:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,774:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,779:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,780:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,781:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,784:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,789:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,790:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,790:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,793:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,797:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,798:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,798:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,801:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,804:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,805:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,806:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,817:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,826:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,827:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,828:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,830:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,834:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,835:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,835:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,837:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,842:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,843:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,844:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,846:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,850:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,851:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,852:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,854:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,858:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,859:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,860:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,864:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,868:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,869:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,870:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,872:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,877:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,878:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,879:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,882:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,886:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,887:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,887:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,890:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,896:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,896:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,897:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,900:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,907:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,908:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,908:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,911:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,915:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,916:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,917:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,919:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,929:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,930:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,930:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,933:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,940:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,941:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,941:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,945:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,952:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,953:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,955:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,959:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,967:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,969:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,971:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,974:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,983:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,985:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:10,987:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:10,991:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:10,997:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:10,998:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,000:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,004:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,012:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,014:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,016:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,019:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,026:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,028:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,029:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,033:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,040:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,042:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,044:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,047:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,056:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,058:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,060:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,065:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,070:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,072:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,073:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,077:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,084:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,085:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,087:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,092:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,097:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,099:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,101:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,105:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,112:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,114:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,115:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,118:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,127:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,128:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,129:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,138:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,147:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,149:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,151:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,156:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,163:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,165:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,167:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,172:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,179:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,181:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,183:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,188:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,195:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,197:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,199:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,203:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,209:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,211:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,212:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,215:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,220:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,222:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,224:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,227:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,233:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,235:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,236:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,240:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,245:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,247:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,248:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,252:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,256:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,257:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,259:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,261:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,265:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,266:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,267:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,270:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,273:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,274:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,275:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,278:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,282:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,283:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,284:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,286:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,291:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,292:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,292:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,295:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,300:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,301:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,302:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,304:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,308:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,309:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,310:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,312:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,317:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,317:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,318:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,321:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,326:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,327:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,327:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,329:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,333:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,334:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,335:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,338:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,344:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,345:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,348:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,353:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,354:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,355:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,357:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,363:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,364:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,365:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,367:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,371:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,372:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,373:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,375:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,380:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,381:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,381:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,384:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,388:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,389:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,390:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,393:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,398:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,399:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,400:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,402:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,407:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,408:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,409:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,412:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,416:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,418:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,419:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,421:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,427:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,428:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,428:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,431:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,435:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,436:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,437:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,438:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,443:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,443:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,444:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,446:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,451:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,451:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,452:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,455:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,459:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,460:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,461:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,462:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,466:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,466:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,467:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,469:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,473:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,474:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,475:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,476:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,481:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,482:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,482:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,484:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,488:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,489:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,490:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,492:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,497:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,497:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,498:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,500:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,504:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,504:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,505:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,507:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,511:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,511:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,512:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,515:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,519:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,523:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,525:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,529:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,535:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,538:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,540:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,546:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,551:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,553:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,555:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,559:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,564:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,565:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,566:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,568:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,572:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,573:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,574:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,576:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,580:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,581:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,581:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,584:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,589:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,590:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,590:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,592:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,597:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,598:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,598:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,600:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,605:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,605:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,606:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,608:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,612:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,613:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,614:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,617:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,621:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,622:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,623:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,625:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,632:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,635:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,637:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,641:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,647:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,649:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,651:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,655:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,660:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,662:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,664:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,668:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,673:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,675:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,676:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,680:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,685:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,687:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,689:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,693:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,698:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,700:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,705:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,711:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,713:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,715:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,718:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,724:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,726:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,728:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,731:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,735:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,737:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,739:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,743:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,748:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,750:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,751:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,755:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,760:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,761:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,763:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,767:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,772:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,774:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,775:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,780:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,785:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,786:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,787:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,790:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,797:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,798:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,799:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,802:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,807:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,808:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,809:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,812:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,821:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,823:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,825:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,837:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,842:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,843:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,844:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,846:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,851:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,852:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,853:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,856:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,861:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,862:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,863:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,866:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,871:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,873:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,874:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,877:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,882:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,883:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,884:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,887:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,891:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,892:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,893:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,896:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,900:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,902:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,903:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,905:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,910:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,912:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,913:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,915:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,920:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,921:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,922:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,924:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,929:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,931:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,932:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,936:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,943:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,945:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,947:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,951:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,956:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,958:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,960:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,963:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,968:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,969:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,970:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,972:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,977:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,978:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,978:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,980:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,985:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,986:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,986:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,989:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:11,994:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:11,994:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:11,995:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:11,997:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,002:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,004:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,006:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,010:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,016:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,018:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,020:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,024:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,030:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,032:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,033:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,035:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,040:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,042:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,042:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,045:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,049:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,050:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,051:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,054:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,059:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,060:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,061:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,063:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,068:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,068:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,069:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,071:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,076:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,077:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,077:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,080:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,085:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,086:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,087:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,089:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,093:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,094:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,095:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,099:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,103:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,104:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,105:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,107:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,111:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,112:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,113:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,115:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,119:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,120:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,121:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,123:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,128:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,128:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,129:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,131:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,136:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,136:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,137:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,142:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,148:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,149:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,149:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,152:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,156:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,157:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,157:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,160:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,164:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,164:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,165:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,168:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,172:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,173:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,174:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,176:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,181:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,182:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,182:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,184:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,188:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,189:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,190:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,192:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,196:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,196:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,197:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,200:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,204:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,205:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,206:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,208:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,212:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,213:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,213:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,215:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,219:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,220:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,221:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,223:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,228:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,229:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,230:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,233:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,238:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,239:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,239:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,241:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,246:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,247:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,248:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,249:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,254:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,256:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,258:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,262:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,267:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,269:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,271:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,275:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,281:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,283:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,285:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,289:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,294:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,297:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,299:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,303:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,308:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,309:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,310:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,313:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,318:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,319:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,320:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,323:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,329:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,330:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,331:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,334:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,339:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,340:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,341:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,344:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,349:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,351:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,352:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,354:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,359:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,360:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,361:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,364:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,368:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,369:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,370:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,373:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,379:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,380:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,381:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,384:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,389:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,390:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,391:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,393:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,397:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,398:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,399:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,402:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,406:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,407:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,408:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,411:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,415:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,416:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,417:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,419:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,424:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,425:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,426:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,428:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,433:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,434:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,435:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,438:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,442:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,444:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,445:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,447:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,452:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,453:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,454:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,457:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,462:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,463:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,464:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,467:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,471:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,472:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,473:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,477:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,482:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,483:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,484:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,487:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,491:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,492:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,493:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,496:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,500:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,501:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,502:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,505:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,509:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,510:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,511:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,514:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,518:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,519:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,520:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,522:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,527:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,528:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,529:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,531:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,535:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,536:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,537:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,539:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,542:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,543:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,543:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,546:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,550:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,551:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,552:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,553:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,557:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,558:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,558:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,560:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,563:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,564:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,564:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,566:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,570:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,571:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,571:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,573:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,577:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,577:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,578:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,580:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,584:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,584:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,585:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,587:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,591:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,592:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,592:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,594:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,598:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,598:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,599:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,602:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,606:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,607:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,607:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,611:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,616:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,617:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,618:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,620:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,624:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,625:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,626:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,628:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,633:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,634:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,634:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,636:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,641:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,642:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,642:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,644:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,649:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,650:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,650:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,652:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,656:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,656:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,657:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,659:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,664:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,664:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,665:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,667:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,671:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,672:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,673:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,675:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,679:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,680:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,681:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,684:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,687:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,688:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,688:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,690:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,694:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,694:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,695:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,697:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,701:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,701:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,704:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,708:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,709:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,709:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,711:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,716:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,717:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,718:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,720:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,724:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,725:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,725:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,728:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,732:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,735:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,737:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,740:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,746:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,748:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,749:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,753:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,759:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,760:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,761:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,763:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,767:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,767:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,768:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,770:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,773:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,774:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,774:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,776:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,780:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,781:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,781:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,783:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,786:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,786:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,787:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,788:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,791:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,792:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,792:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,794:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,798:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,799:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,799:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,801:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,805:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,806:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,806:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,808:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,812:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,812:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,812:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,814:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,818:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,818:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,819:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,823:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,827:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,827:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,827:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,832:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,836:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,836:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,836:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,846:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,850:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,851:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,851:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,854:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,858:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,859:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,859:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,861:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,865:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,865:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,866:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,868:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,872:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,873:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,873:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,876:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,880:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,881:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,882:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,884:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,889:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,891:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,892:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,894:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,898:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,899:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,900:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,903:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,907:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,908:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,909:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,911:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,915:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,916:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,917:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,920:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,925:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,926:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,927:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,929:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,933:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,934:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,934:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,937:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,941:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,942:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,943:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,945:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,951:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,952:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,952:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,954:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,960:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,961:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,962:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,964:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,967:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,968:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,969:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,971:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,975:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,976:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,976:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,979:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,984:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,985:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,985:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,987:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:12,992:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:12,993:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:12,993:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:12,995:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,000:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,001:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,002:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,004:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,009:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,010:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,011:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,013:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,018:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,019:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,020:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,023:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,027:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,027:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,028:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,030:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,034:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,034:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,034:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,036:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,040:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,041:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,041:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,043:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,047:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,048:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,048:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,050:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,053:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,054:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,054:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,056:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,059:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,059:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,060:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,062:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,065:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,065:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,066:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,067:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,071:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,071:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,071:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,073:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,077:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,077:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,078:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,081:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,084:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,085:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,085:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,087:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,091:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,091:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,092:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,093:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,097:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,098:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,098:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,100:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,104:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,105:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,105:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,107:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,111:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,112:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,112:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,114:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,119:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,119:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,120:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,121:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,125:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,126:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,126:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,128:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,132:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,134:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,136:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,140:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,146:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,148:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,150:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,160:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,165:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,166:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,167:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,171:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,176:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,178:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,180:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,183:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,189:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,190:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,194:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,198:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,200:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,201:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,203:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,207:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,208:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,208:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,210:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,214:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,214:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,215:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,217:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,220:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,221:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,221:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,223:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,227:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,227:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,227:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,229:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,234:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,234:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,234:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,238:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,241:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,242:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,242:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,245:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,249:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,250:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,250:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,251:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,254:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,255:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,255:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,257:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,261:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,262:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,262:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,263:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,267:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,269:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,270:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,275:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,279:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,281:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,282:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,285:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,290:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,291:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,292:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,295:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,299:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,299:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,300:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,303:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,307:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,307:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,308:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,310:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,313:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,314:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,314:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,316:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,319:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,320:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,320:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,322:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,326:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,327:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,327:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,329:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,334:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,334:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,335:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,336:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,340:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,341:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,341:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,343:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,347:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,347:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,348:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,350:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,354:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,355:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,355:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,357:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,361:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,362:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,362:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,364:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,368:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,368:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,369:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,372:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,377:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,377:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,378:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,380:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,385:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,385:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,385:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:13,387:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:13,391:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:13,391:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:13,392:DEBUG:
    Ignoring line no. 24: 35
    


.. parsed-literal::

    10.4 ms ± 1.17 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)


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

    2018-09-13 12:07:14,744:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:14,750:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:14,751:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:14,752:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:14,753:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:14,754:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:14,812:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:14,817:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:14,818:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:14,819:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:14,820:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:14,820:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:14,862:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:14,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:14,866:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:14,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:14,867:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:14,868:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:14,913:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:14,918:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:14,918:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:14,919:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:14,919:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:14,920:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:14,963:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:14,968:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:14,968:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:14,969:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:14,969:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:14,970:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,013:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,018:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,019:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,019:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,020:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,020:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,066:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,071:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,072:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,072:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,072:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,073:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,116:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,121:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,122:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,122:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,123:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,123:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,166:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,170:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,171:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,171:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,172:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,172:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,216:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,221:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,222:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,222:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,222:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,223:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,265:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,269:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,271:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,272:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,274:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,275:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,326:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,330:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,331:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,331:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,332:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,332:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,378:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,383:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,383:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,384:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,384:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,385:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,434:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,439:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,439:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,440:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,440:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,441:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,483:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,488:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,488:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,489:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,489:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,490:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,535:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,541:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,543:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,544:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,545:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,546:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,595:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,602:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,604:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,606:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,607:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,608:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,669:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,673:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,674:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,674:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,675:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,675:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,718:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,725:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,727:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,728:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,729:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,730:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,802:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,807:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,809:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,812:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,814:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,815:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,888:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,893:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,893:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,894:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,894:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,895:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,939:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,943:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,944:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,944:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,945:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,946:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:15,989:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:15,994:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:15,995:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:15,995:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:15,996:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:15,996:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,042:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,048:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,050:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,051:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,053:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,055:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,124:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,130:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,130:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,131:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,131:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,132:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,184:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,191:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,191:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,191:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,192:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,192:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,254:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,259:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,260:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,260:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,261:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,261:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,305:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,309:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,310:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,310:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,311:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,311:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,356:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,360:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,361:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,361:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,362:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,362:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,405:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,409:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,410:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,411:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,411:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,412:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,455:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,461:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,462:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,462:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,462:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,463:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,509:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,513:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,514:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,514:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,515:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,515:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,558:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,562:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,562:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,563:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,563:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,564:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,607:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,611:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,612:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,612:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,613:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,613:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,659:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,663:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,664:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,664:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,665:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,665:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,708:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,713:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,714:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,714:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,715:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,716:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,762:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,767:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,768:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,768:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,769:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,769:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,837:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,842:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,843:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,843:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,844:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,844:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,892:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,899:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,900:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,900:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,901:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,946:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:16,950:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:16,950:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:16,951:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:16,951:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:16,952:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:16,997:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,002:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,002:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,003:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,003:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,004:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,047:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,052:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,053:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,054:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,054:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,055:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,105:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,110:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,111:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,111:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,112:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,113:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,159:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,164:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,165:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,165:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,166:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,166:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,209:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,213:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,214:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,214:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,214:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,215:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,260:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,266:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,266:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,267:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,267:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,267:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,312:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,316:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,317:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,317:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,318:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,318:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,361:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,365:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,366:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,367:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,367:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,368:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,412:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,417:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,420:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,422:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,424:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,427:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,485:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,489:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,490:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,490:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,491:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,491:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,533:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,539:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,540:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,540:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,541:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,541:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,584:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,589:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,590:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,590:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,591:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,591:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,635:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,640:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,641:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,643:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,644:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,645:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,711:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,715:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,715:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,716:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,716:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,717:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,759:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,764:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,766:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,767:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,769:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,770:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,852:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,857:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,858:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,859:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,859:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,860:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,907:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,911:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,912:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,913:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,913:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,914:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:17,958:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:17,963:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:17,965:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:17,967:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:17,969:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:17,971:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,043:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,047:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,048:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,048:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,049:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,049:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,092:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,099:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,100:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,100:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,101:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,101:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,146:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,153:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,154:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,154:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,154:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,155:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,206:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,207:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,208:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,208:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,208:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,253:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,258:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,258:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,259:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,259:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,260:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,302:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,307:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,308:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,309:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,309:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,310:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,353:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,358:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,359:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,360:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,360:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,361:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,403:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,410:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,410:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,411:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,411:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,411:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,467:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,472:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,473:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,474:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,475:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,476:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,534:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,539:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,540:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,540:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,541:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,541:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,584:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,590:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,590:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,591:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,591:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,592:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,640:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,646:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,648:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,649:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,651:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,652:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,716:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,723:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,723:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,724:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,724:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,725:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,773:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,778:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,778:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,779:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,779:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,780:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,824:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,829:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,830:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,831:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,831:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,831:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,897:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,902:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,902:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,903:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,903:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,904:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:18,949:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:18,953:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:18,954:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:18,954:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:18,955:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:18,956:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:19,001:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:19,007:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:19,008:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:19,009:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:19,009:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:19,009:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:19,055:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:19,062:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:19,064:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:19,066:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:19,067:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:19,069:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:19,138:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:19,143:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:19,144:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:19,146:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:19,148:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:19,149:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:19,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:19,207:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:19,208:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:19,208:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:19,208:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:19,209:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:19,253:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:19,258:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:19,259:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:19,259:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:19,260:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:19,260:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:19,304:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:19,309:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:19,311:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:19,313:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:19,314:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:19,315:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    57.9 ms ± 3.1 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


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

    2018-09-13 12:07:19,577:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:19,581:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:19,581:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:19,582:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:19,582:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:19,583:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:19,637:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:19,643:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:19,644:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:19,644:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:19,645:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:19,646:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:19,697:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:19,701:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:19,702:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:19,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:19,703:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:19,703:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:19,758:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:19,763:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:19,763:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:19,764:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:19,764:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:19,765:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:19,816:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:19,820:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:19,821:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:19,821:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:19,821:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:19,822:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:19,878:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:19,884:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:19,886:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:19,887:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:19,889:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:19,890:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:19,983:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:19,988:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:19,989:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:19,989:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:19,990:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:19,990:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:20,046:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:20,050:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:20,050:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:20,051:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:20,051:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:20,051:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:20,106:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:20,112:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:20,112:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:20,113:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:20,113:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:20,113:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:20,169:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:20,174:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:20,177:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:20,178:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:20,179:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:20,180:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:20,254:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:20,259:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:20,261:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:20,263:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:20,265:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:20,266:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:20,333:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:20,338:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:20,340:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:20,342:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:20,344:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:20,346:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:20,424:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:20,428:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:20,429:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:20,429:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:20,430:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:20,430:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:20,483:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:20,488:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:20,488:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:20,489:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:20,489:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:20,489:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:20,540:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:20,544:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:20,544:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:20,545:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:20,545:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:20,546:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:20,601:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:20,607:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:20,607:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:20,607:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:20,608:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:20,609:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:20,662:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:20,666:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:20,666:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:20,667:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:20,667:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:20,668:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:20,734:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:20,738:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:20,739:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:20,739:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:20,740:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:20,740:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:20,794:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:20,799:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:20,800:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:20,801:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:20,801:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:20,801:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:20,853:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:20,858:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:20,860:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:20,861:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:20,863:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:20,864:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:20,927:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:20,932:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:20,933:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:20,933:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:20,934:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:20,935:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,010:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,015:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,015:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,016:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,016:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,017:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,082:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,087:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,088:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,088:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,088:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,089:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,142:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,146:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,147:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,147:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,148:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,148:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,199:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,203:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,204:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,204:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,205:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,206:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,257:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,262:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,262:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,263:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,264:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,264:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,318:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,323:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,324:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,324:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,325:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,325:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,378:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,383:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,384:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,384:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,385:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,385:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,439:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,445:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,447:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,448:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,450:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,451:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,516:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,520:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,521:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,521:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,522:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,522:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,574:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,578:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,579:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,579:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,580:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,580:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,644:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,650:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,650:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,651:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,651:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,652:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,704:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,709:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,711:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,712:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,714:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,715:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,786:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,791:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,792:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,792:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,792:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,793:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,844:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,851:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,851:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,852:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,852:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,853:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,906:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,911:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,912:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,912:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,912:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,913:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:21,967:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:21,972:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:21,973:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:21,973:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:21,974:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:21,974:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,048:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,053:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,056:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,057:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,060:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,062:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,133:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,137:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,138:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,138:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,139:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,139:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,192:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,199:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,199:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,199:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,200:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,200:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,255:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,259:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,260:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,260:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,260:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,261:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,314:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,319:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,320:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,320:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,321:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,321:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,374:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,379:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,380:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,380:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,381:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,381:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,434:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,438:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,439:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,441:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,443:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,444:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,504:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,510:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,511:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,511:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,512:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,512:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,563:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,568:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,569:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,569:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,570:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,570:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,622:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,626:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,627:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,628:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,628:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,630:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,686:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,691:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,692:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,692:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,693:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,693:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,744:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,748:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,749:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,749:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,749:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,750:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,801:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,805:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,806:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,806:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,807:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,807:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,859:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,865:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,865:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,866:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,866:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,867:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,919:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,923:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,923:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,924:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,924:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,924:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:22,989:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:22,993:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:22,994:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:22,994:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:22,995:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:22,995:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,069:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,073:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,074:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,075:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,075:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,076:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,130:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,134:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,134:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,135:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,135:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,136:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,187:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,191:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,192:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,192:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,193:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,193:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,248:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,252:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,252:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,253:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,253:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,254:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,309:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,314:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,314:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,315:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,315:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,316:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,367:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,372:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,373:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,373:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,374:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,374:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,427:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,432:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,433:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,433:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,434:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,434:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,491:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,496:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,496:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,497:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,497:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,498:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,551:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,556:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,556:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,557:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,557:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,558:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,612:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,617:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,618:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,618:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,619:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,619:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,671:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,678:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,679:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,679:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,680:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,680:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,733:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,738:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,739:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,739:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,740:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,740:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,794:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,799:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,799:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,800:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,800:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,801:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,858:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,863:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,864:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,864:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,864:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,865:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,916:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,920:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,921:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,921:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,921:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,922:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:23,975:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:23,982:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:23,982:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:23,983:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:23,983:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:23,984:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:24,039:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:24,042:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:24,043:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:24,044:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:24,044:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:24,045:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:24,123:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:24,128:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:24,129:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:24,130:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:24,131:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:24,131:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:24,200:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:24,205:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:24,206:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:24,206:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:24,207:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:24,207:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:24,260:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:24,265:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:24,265:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:24,266:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:24,266:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:24,267:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:24,319:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:24,323:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:24,324:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:24,325:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:24,325:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:24,326:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:24,381:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:24,388:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:24,388:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:24,389:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:24,389:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:24,389:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:24,441:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:24,445:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:24,445:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:24,446:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:24,446:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:24,447:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:24,498:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:24,505:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:24,505:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:24,506:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:24,506:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:24,507:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:24,561:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:24,565:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:24,565:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:24,566:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:24,566:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:24,567:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:24,620:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:24,624:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:24,624:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:24,625:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:24,626:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:24,626:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:24,682:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:24,687:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:24,688:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:24,689:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:24,689:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:24,689:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-13 12:07:24,743:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-13 12:07:24,747:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-13 12:07:24,747:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-13 12:07:24,748:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-13 12:07:24,749:DEBUG:
    REACHED DATA BLOCK
    2018-09-13 12:07:24,749:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    63.9 ms ± 2.42 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

