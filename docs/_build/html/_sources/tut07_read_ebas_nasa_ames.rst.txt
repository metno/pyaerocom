
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

    2018-09-14 16:33:58,910:INFO:
    Reading aliases ini file: /home/jonasg/github/pyaerocom/pyaerocom/data/aliases.ini


.. parsed-literal::

    Elapsed time init all variables: 0.02386784553527832 s


.. parsed-literal::

    2018-09-14 16:33:59,637:WARNING:
    geopy library is not available. Aeolus data read not enabled
    2018-09-14 16:33:59,884:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:33:59,891:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:33:59,893:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:33:59,894:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:33:59,897:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:33:59,898:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    Elapsed time init pyaerocom: 0.8757307529449463 s
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
                  <pyaerocom.io.ebas_nasa_ames.EbasFlagCol at 0x7f78791159e8>)])



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

    2018-09-14 16:34:00,083:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,088:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,090:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,091:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,093:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,098:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,099:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,100:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,102:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,106:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,107:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,108:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,110:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,114:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,115:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,115:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,117:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,121:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,122:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,123:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,124:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,128:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,129:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,130:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,132:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,136:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,137:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,138:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,140:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,144:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,145:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,145:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,147:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,152:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,152:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,153:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,155:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,160:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,161:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,163:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,166:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,172:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,174:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,176:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,179:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,184:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,186:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,187:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,191:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,195:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,197:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,198:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,206:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,208:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,209:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,213:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,218:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,220:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,222:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,225:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,229:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,230:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,231:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,233:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,237:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,238:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,239:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,242:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,246:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,247:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,247:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,249:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,253:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,254:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,255:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,257:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,261:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,262:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,262:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,264:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,268:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,269:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,270:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,272:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,276:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,277:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,277:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,280:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,284:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,285:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,286:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,288:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,292:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,293:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,294:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,296:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,300:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,301:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,302:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,305:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,310:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,311:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,312:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,314:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,319:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,320:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,321:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,324:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,331:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,333:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,333:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,337:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,342:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,343:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,344:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,347:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,352:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,353:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,355:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,357:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,363:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,364:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,365:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,368:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,372:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,373:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,374:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,376:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,380:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,381:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,382:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,384:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,388:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,389:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,390:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,393:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,397:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,398:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,399:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,401:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,405:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,406:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,407:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,409:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,413:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,414:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,415:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,417:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,421:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,422:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,423:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,425:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,429:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,430:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,430:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,436:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,437:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,438:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,441:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,445:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,446:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,446:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,449:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,454:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,455:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,456:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,458:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,462:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,462:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,463:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,466:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,469:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,470:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,471:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,474:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,478:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,479:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,480:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,483:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,486:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,487:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,488:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,490:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,494:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,495:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,496:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,498:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,502:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,503:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,504:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,506:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,510:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,511:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,512:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,515:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,519:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,520:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,521:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,523:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,527:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,528:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,529:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,531:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,534:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,535:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,536:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,539:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,542:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,543:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,544:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,546:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,549:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,550:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,551:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,553:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,556:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,557:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,557:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,559:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,562:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,562:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,563:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,564:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,567:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,568:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,568:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,570:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,573:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,573:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,573:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,575:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,577:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,578:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,578:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,580:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,583:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,583:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,583:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,585:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,588:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,589:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,589:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,591:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,595:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,596:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,598:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,601:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,605:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,606:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,608:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,610:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,614:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,615:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,616:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,618:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,621:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,622:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,622:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,624:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,627:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,627:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,628:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,629:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,632:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,633:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,633:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,635:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,638:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,638:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,639:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,640:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,643:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,643:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,644:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,645:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,648:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,649:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,649:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,650:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,653:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,654:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,654:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,655:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,659:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,659:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,660:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,661:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,664:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,665:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,665:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,666:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,670:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,670:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,670:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,672:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,675:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,676:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,676:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,678:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,681:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,682:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,682:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,684:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,688:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,688:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,689:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,690:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,693:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,694:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,694:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,696:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,699:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,699:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,700:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,701:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,704:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,705:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,705:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,707:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,710:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,711:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,711:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,712:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,716:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,716:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,717:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,718:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,722:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,723:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,724:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,727:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,731:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,733:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,735:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,739:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,742:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,744:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,745:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,749:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,754:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,756:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,757:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,760:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,765:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,766:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,766:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,769:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,773:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,773:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,774:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,776:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,779:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,780:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,781:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,783:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,786:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,787:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,787:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,789:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,792:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,793:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,793:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,795:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,797:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,798:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,798:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,801:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,804:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,805:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,805:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,807:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,811:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,811:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,812:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,813:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,816:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,817:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,817:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,819:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,822:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,822:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,823:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,824:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,828:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,828:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,829:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,830:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,833:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,834:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,834:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,836:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,840:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,842:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,843:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,847:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,851:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,852:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,854:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,857:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,861:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,862:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,863:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,865:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,869:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,869:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,870:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,873:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,879:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,880:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,880:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,889:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,893:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,894:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,894:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,896:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,900:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,900:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,902:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,906:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,906:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,907:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,909:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,912:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,913:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,913:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,915:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,919:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,919:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,920:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,921:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,925:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,925:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,926:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,928:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,931:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,931:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,932:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,934:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,937:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,937:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,938:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,940:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,943:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,944:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,944:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,946:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,949:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,950:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,950:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,952:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,955:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,956:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,956:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,958:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,962:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,962:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,963:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,964:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,968:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,969:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,970:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,971:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,975:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,975:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,976:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,977:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,981:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,982:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,982:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,984:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,987:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,988:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,988:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,990:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,993:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:00,994:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:00,995:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:00,996:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:00,999:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,000:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,000:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,002:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,006:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,006:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,007:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,008:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,012:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,013:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,013:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,015:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,018:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,019:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,019:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,021:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,025:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,025:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,026:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,027:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,031:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,031:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,032:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,033:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,037:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,037:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,038:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,040:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,043:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,043:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,044:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,045:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,049:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,049:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,050:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,052:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,055:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,055:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,056:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,057:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,061:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,061:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,062:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,064:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,067:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,067:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,068:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,070:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,074:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,074:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,076:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,077:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,080:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,081:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,082:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,086:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,092:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,092:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,093:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,095:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,099:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,100:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,100:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,102:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,105:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,106:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,106:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,108:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,111:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,112:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,113:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,114:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,118:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,118:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,119:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,121:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,124:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,125:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,125:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,128:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,132:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,133:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,133:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,135:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,139:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,139:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,140:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,142:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,147:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,147:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,148:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,150:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,153:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,154:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,154:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,156:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,159:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,160:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,160:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,162:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,166:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,166:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,167:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,169:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,172:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,173:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,173:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,175:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,179:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,179:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,180:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,181:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,185:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,186:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,186:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,188:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,191:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,192:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,192:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,194:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,198:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,198:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,199:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,204:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,205:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,205:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,207:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,211:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,211:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,212:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,214:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,217:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,218:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,218:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,220:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,224:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,224:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,225:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,226:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,230:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,231:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,231:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,233:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,236:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,237:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,237:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,239:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,242:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,243:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,243:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,245:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,249:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,249:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,250:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,252:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,255:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,256:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,256:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,258:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,261:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,262:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,262:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,264:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,267:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,268:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,268:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,270:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,273:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,274:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,274:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,276:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,279:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,280:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,280:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,282:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,285:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,286:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,286:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,288:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,292:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,292:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,293:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,294:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,299:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,299:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,300:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,302:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,305:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,306:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,307:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,309:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,312:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,313:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,313:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,316:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,320:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,323:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,324:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,328:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,333:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,335:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,337:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,340:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,345:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,347:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,349:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,352:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,357:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,358:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,359:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,361:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,366:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,367:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,367:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,369:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,374:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,375:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,375:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,377:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,381:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,382:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,384:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,388:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,393:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,394:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,395:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,397:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,401:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,402:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,402:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,405:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,410:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,410:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,411:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,413:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,417:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,418:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,418:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,421:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,425:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,425:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,426:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,428:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,433:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,434:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,435:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,437:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,440:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,441:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,442:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,444:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,448:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,449:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,449:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,451:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,455:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,455:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,456:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,458:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,461:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,462:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,463:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,465:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,468:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,469:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,470:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,472:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,476:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,477:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,478:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,480:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,484:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,485:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,486:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,488:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,493:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,494:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,496:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,500:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,500:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,501:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,503:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,506:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,507:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,508:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,510:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,514:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,515:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,516:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,518:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,522:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,522:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,523:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,525:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,530:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,531:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,531:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,533:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,537:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,538:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,539:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,541:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,546:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,547:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,547:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,550:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,554:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,555:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,556:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,558:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,562:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,563:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,564:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,566:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,569:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,570:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,571:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,573:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,577:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,578:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,578:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,580:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,585:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,586:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,586:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,589:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,593:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,594:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,594:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,597:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,602:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,603:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,605:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,608:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,609:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,610:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,612:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,616:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,616:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,617:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,619:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,623:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,624:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,624:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,626:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,630:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,630:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,631:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,632:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,636:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,636:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,637:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,639:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,642:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,643:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,643:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,645:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,648:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,649:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,650:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,651:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,655:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,656:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,656:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,658:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,661:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,663:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,665:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,668:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,673:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,675:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,677:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,680:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,686:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,689:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,690:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,693:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,698:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,700:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,706:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,711:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,712:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,713:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,716:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,721:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,722:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,722:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,725:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,729:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,730:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,731:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,733:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,737:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,738:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,739:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,741:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,746:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,747:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,748:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,750:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,754:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,755:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,756:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,758:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,761:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,762:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,763:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,765:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,769:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,770:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,770:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,772:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,776:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,777:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,778:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,780:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,783:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,784:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,785:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,787:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,790:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,791:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,792:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,794:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,798:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,799:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,799:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,801:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,805:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,806:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,807:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,809:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,813:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,814:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,815:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,817:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,821:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,822:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,823:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,825:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,828:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,829:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,830:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,832:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,836:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,837:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,838:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,839:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,843:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,844:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,845:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,847:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,851:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,852:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,853:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,855:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,859:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,860:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,860:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,862:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,867:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,869:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,873:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,874:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,874:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,880:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,885:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,885:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,886:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,895:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,900:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,901:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,903:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,907:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,908:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,908:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,910:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,914:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,916:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,917:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,919:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,923:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,924:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,925:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,927:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,930:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,931:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,932:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,934:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,937:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,938:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,939:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,941:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,945:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,946:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,947:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,949:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,953:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,954:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,954:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,957:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,962:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,963:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,964:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,967:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,972:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,973:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,973:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,975:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,979:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,980:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,981:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,983:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,987:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,988:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,988:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,991:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:01,995:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:01,996:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:01,997:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:01,999:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,003:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,004:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,005:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,007:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,011:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,012:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,013:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,015:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,018:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,019:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,020:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,022:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,025:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,026:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,027:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,029:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,033:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,034:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,034:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,036:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,040:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,042:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,044:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,047:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,052:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,053:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,055:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,058:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,063:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,064:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,065:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,067:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,071:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,072:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,072:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,074:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,078:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,078:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,079:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,081:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,085:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,086:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,086:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,090:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,095:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,096:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,097:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,098:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,102:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,102:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,103:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,105:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,108:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,108:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,109:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,111:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,114:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,115:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,115:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,117:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,120:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,121:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,121:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,123:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,126:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,127:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,127:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,129:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,132:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,133:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,133:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,135:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,139:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,139:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,140:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,142:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,145:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,146:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,146:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,148:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,152:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,152:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,153:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,155:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,158:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,159:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,160:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,162:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,165:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,166:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,166:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,168:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,172:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,172:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,173:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,174:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,178:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,179:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,180:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,182:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,185:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,186:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,186:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,188:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,191:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,192:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,192:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,194:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,197:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,198:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,198:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,200:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,204:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,204:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,205:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,207:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,210:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,212:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,213:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,217:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,222:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,224:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,225:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,229:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,233:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,234:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,235:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,237:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,241:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,242:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,242:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,244:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,249:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,250:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,250:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,253:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,256:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,257:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,258:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,260:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,263:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,264:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,265:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,267:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,271:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,272:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,272:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,274:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,278:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,279:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,280:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,282:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,286:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,286:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,287:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,289:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,293:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,294:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,295:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,296:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,300:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,301:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,302:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,304:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,307:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,308:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,309:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,311:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,315:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,316:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,316:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,318:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,322:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,323:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,324:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,326:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,329:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,330:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,331:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,333:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,336:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,337:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,338:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,340:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,344:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,345:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,347:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,350:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,351:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,352:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,353:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,357:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,358:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,359:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,360:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,364:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,365:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,365:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,368:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,371:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,372:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,373:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,375:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,379:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,379:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,380:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,382:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,386:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,387:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,387:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,389:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,393:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,394:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,394:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,397:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,400:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,401:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,402:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,404:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,407:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,408:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,408:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,410:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,413:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,413:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,414:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,415:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,418:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,418:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,419:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,420:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,423:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,424:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,424:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,425:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,428:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,429:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,429:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,431:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,433:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,434:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,434:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,436:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,439:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,439:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,440:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,441:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,445:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,445:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,446:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,448:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,451:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,452:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,452:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,454:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,457:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,457:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,458:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,460:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,463:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,464:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,464:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,466:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,469:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,470:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,470:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,472:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,476:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,476:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,477:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,478:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,481:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,482:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,482:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,484:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,488:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,488:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,488:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,490:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,493:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,494:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,494:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,496:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,499:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,499:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,500:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,501:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,505:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,505:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,506:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,507:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,510:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,511:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,511:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,513:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,516:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,516:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,517:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,518:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,521:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,522:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,522:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,524:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,527:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,527:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,528:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,529:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,532:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,533:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,533:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,535:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,538:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,539:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,539:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,541:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,544:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,544:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,545:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,546:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,549:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,550:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,550:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,552:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,555:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,555:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,556:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,557:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,560:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,560:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,561:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,562:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,565:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,566:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,566:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,567:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,572:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,572:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,572:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,574:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,578:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,578:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,578:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,580:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,583:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,583:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,584:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,585:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,588:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,589:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,589:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,590:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,594:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,595:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,596:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,600:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,601:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,604:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,608:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,614:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,616:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,618:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,622:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,626:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,629:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,630:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,634:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,639:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,640:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,642:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,645:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,650:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,651:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,652:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,655:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,659:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,660:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,660:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,662:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,666:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,667:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,668:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,670:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,674:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,675:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,676:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,678:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,682:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,682:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,683:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,685:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,689:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,690:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,690:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,694:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,697:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,698:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,699:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,701:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,705:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,707:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,709:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,712:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,717:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,719:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,721:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,726:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,730:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,732:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,733:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,736:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,740:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,742:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,742:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,744:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,748:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,748:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,749:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,751:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,755:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,757:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,759:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,762:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,766:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,767:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,767:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,769:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,773:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,774:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,775:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,777:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,780:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,781:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,782:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,784:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,787:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,788:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,789:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,790:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,794:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,795:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,796:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,798:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,802:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,803:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,803:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,805:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,809:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,809:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,810:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,812:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,817:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,818:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,818:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,820:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,824:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,825:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,826:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,828:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,832:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,833:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,833:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,836:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,839:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,840:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,841:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,843:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,847:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,848:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,848:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,850:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,854:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,855:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,855:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,857:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,861:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,861:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,862:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,864:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,867:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,868:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,869:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,871:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,875:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,877:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,879:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,883:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,892:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,894:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,896:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,905:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,910:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,912:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,914:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,917:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,922:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,924:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,925:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,928:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,933:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,935:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,936:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,939:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,943:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,944:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,944:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,946:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,949:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,950:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,950:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,953:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,956:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,957:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,957:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,959:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,963:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,963:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,964:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,965:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,969:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,970:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,970:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,972:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,976:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,977:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,977:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,979:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,982:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,982:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,983:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,984:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,987:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,988:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,988:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,990:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,993:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:02,994:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:02,994:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:02,996:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:02,999:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,000:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,000:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,002:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,005:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,006:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,006:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,008:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,011:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,011:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,012:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,013:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,017:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,018:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,018:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,020:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,023:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,023:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,024:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,025:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,029:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,029:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,030:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,031:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,035:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,036:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,036:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,038:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,042:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,044:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,045:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,048:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,052:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,053:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,054:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,056:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,060:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,061:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,061:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,063:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,067:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,068:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,068:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,071:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,074:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,075:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,075:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,077:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,080:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,081:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,081:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,082:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,086:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,086:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,087:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,088:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,092:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,092:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,093:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,099:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,102:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,103:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,103:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,105:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,108:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,109:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,109:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,111:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,114:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,114:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,115:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,116:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,121:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,121:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,121:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,123:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,127:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,129:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,130:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,133:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,138:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,140:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,142:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,145:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,148:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,150:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,150:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,152:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,156:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,157:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,158:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,159:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,163:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,164:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,165:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,167:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,171:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,171:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,172:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,174:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,178:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,178:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,179:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,182:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,185:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,186:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,186:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,189:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,195:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,198:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,199:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,202:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,208:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,210:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,211:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,214:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,220:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,222:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,223:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,227:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,232:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,233:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,234:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,236:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,240:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,241:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,242:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,244:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,248:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,249:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,250:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,252:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,255:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,256:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,257:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,259:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,263:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,264:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,264:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,266:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,270:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,271:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,271:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,273:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,277:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,278:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,279:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,282:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,285:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,286:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,286:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,288:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,291:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,292:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,292:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,295:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,298:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,298:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,299:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,301:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,304:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,305:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,306:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,308:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,311:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,312:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,313:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,315:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,318:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,319:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,320:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,322:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,326:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,327:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,328:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,330:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,333:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,334:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,335:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,337:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,341:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,342:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,342:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,345:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,348:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,350:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,350:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,352:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,356:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,357:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,358:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,360:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,364:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,365:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,365:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,367:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,371:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,374:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,376:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,379:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,384:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,385:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,387:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,389:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,398:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,399:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,401:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,404:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,409:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,411:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,412:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,416:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,421:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,423:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,424:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,429:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,435:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,436:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,437:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,439:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,445:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,446:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,447:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,449:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,455:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,456:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,458:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,461:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,466:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,467:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,469:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,471:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,475:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,476:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,476:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,478:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,482:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,483:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,483:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,486:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,490:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,490:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,491:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,493:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,497:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,498:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,498:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,501:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,505:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,507:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,508:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,511:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,516:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,518:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,519:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,522:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,526:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,528:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,529:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,532:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,538:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,539:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,540:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,542:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,546:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,547:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,547:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,549:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,552:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,553:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,553:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,555:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,559:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,559:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,560:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,562:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,565:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,565:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,566:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,567:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,570:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,571:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,571:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,572:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,575:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,576:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,576:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,578:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,581:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,584:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,585:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,589:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,593:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,595:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,596:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,599:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,604:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,605:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,606:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,609:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,613:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,614:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,614:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,616:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,620:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,621:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,622:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,624:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,627:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,628:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,628:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,630:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,634:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,634:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,635:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,637:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,640:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,642:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,643:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,647:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,652:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,653:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,654:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,656:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,660:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,661:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,662:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,664:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,669:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,669:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,670:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,672:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,676:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,677:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,677:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,679:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,683:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,683:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,684:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,686:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,690:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,691:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,691:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,693:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,697:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,698:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,699:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,701:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,704:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,705:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,706:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,708:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,711:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,712:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,713:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,715:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,718:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,719:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,720:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,722:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,725:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,726:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,727:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,728:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,732:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,732:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,733:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,735:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,739:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,740:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,740:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,742:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,746:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,747:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,748:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,750:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,755:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,757:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,757:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,760:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,764:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,765:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,766:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,768:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,772:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,772:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,773:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,775:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,778:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,779:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,780:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,782:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,785:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,786:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,787:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,788:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,792:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,793:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,794:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,796:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,799:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,800:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,801:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,803:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,806:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,807:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,808:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,810:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,813:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,814:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,815:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,817:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,820:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,821:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,822:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,824:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,828:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,828:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,829:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,831:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,834:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,835:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,835:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,837:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,841:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,841:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,842:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,843:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,847:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,848:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,848:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,850:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,853:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,853:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,854:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,856:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,860:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,860:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,861:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,862:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,867:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,869:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,872:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,873:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,873:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,875:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,879:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,879:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,880:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,881:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,885:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,885:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,886:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,888:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,891:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,892:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,892:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,900:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,905:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,905:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,906:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,915:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,918:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,919:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,919:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,921:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,925:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,926:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,926:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,928:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,931:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,932:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,932:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,934:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,938:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,938:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,939:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,941:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,945:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,946:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,946:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,949:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,953:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,954:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,955:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,957:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,961:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,961:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,962:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,965:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,969:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,969:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,970:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,972:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,976:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,978:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,979:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,983:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:03,988:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:03,990:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:03,992:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:03,996:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,001:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,003:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,004:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,008:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,014:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,016:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,018:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,021:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,026:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,027:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,028:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,031:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,036:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,037:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,038:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,040:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,044:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,045:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,046:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,049:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,053:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,054:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,054:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,056:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,060:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,062:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,063:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,066:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,070:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,071:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,072:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,074:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,078:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,078:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,079:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,081:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,085:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,087:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,088:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,092:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,097:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,098:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,099:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,105:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,110:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,112:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,114:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,118:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,123:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,125:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,127:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,131:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,136:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,137:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,139:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,143:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,148:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,150:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,152:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,156:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,161:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,163:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,164:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,167:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,172:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,174:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,176:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,180:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,185:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,186:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,188:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,191:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,195:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,196:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,197:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,199:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,203:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,204:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,204:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,206:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,211:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,212:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,214:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,217:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,221:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,223:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,225:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,227:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,232:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,233:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,234:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,237:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,241:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,243:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,243:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,246:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,249:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,250:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,251:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,254:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,258:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,259:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,260:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,263:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,267:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,268:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,269:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,271:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,275:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,276:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,277:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,279:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,284:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,285:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,286:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,288:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,292:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,293:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,295:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,297:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,302:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,303:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,304:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,307:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,311:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,313:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,314:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,316:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,320:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,322:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,323:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,326:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,330:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,331:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,332:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,334:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,338:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,339:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,340:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,342:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,346:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,347:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,348:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,349:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,354:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,355:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,355:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,358:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,362:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,363:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,364:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,366:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,369:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,370:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,371:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,373:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,377:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,378:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,378:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,381:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,385:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,387:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,388:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,392:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,397:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,399:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,400:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,404:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,409:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,410:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,412:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,416:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,419:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,420:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,421:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,424:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,428:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,429:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,430:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,432:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,435:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,436:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,437:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,439:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,442:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,443:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,444:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,446:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,450:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,452:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,453:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,456:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,461:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,462:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,464:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,466:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,470:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,472:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,474:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,476:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,480:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,481:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,482:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,484:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,488:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,488:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,489:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,491:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,495:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,495:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,496:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,498:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,502:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,502:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,503:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,505:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,508:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,509:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,510:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,511:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,515:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,517:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,519:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,523:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,528:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,529:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,531:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,536:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,540:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,541:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,543:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,545:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,549:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,549:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,550:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,552:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,556:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,557:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,557:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,559:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,563:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,564:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,564:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,567:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,570:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,571:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,572:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,574:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,577:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,578:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,579:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,581:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,584:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,585:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,586:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,588:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,592:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,593:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,593:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,595:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,599:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,599:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,600:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,602:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,606:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,607:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,607:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,609:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,613:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,613:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,614:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,616:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,619:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,619:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,620:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,621:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,625:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,625:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,626:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,628:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,631:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,632:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,632:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,633:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,637:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,637:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,638:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,639:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,642:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,643:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,643:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,644:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,647:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,648:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,648:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,650:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,653:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,654:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,654:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,656:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,660:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,662:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,663:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,666:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,671:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,673:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,675:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,678:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,682:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,684:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,685:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,686:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,690:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,691:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,691:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,693:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,697:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,698:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,698:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,700:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,704:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,704:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,705:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,707:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,712:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,713:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,713:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,715:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,719:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,720:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,720:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,722:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,726:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,726:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,727:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,729:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,733:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,734:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,734:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,736:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,739:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,740:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,741:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,742:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,746:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,746:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,747:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,748:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,752:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,753:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,754:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,756:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,760:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,760:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,761:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,763:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,767:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,768:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,768:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,770:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,773:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,774:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,775:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,776:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,782:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,783:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,783:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,785:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,789:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,789:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,790:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,792:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,796:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,797:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,797:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,799:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,802:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,803:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,804:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,806:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,810:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,812:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,814:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,817:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,823:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,825:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,827:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,832:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,836:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,838:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,839:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,842:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,848:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,850:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,852:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,855:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,860:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,862:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,863:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,867:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,872:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,873:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,874:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,876:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,880:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,880:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,881:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,883:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,886:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,886:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,887:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,889:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,892:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,893:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,893:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,895:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,899:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,899:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,906:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,910:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,910:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,911:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,917:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,920:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,921:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,921:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,925:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,929:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,930:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,930:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,932:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,935:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,936:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,936:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,938:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,942:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,942:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,943:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,944:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,947:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,948:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,948:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,950:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,953:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,953:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,953:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,955:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,958:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,958:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,959:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,960:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,963:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,964:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,964:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,965:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,969:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,969:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,970:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,971:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,975:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,977:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,978:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,982:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:04,989:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:04,990:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:04,992:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:04,995:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,000:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,002:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,004:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,007:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,012:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,013:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,015:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,019:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,023:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,025:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,027:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,030:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,036:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,037:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,039:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,041:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,045:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,046:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,047:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,049:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,054:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,055:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,056:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,058:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,062:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,063:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,063:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,066:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,070:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,071:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,071:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,074:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,078:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,079:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,080:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,082:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,086:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,087:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,088:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,090:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,095:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,096:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,096:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,098:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,103:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,104:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,105:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,112:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,116:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,117:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,117:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,120:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,124:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,125:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,126:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,128:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,132:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,134:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,135:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,138:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,143:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,144:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,145:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,148:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,153:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,153:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,154:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,156:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,161:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,161:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,162:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,164:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,168:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,169:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,169:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,172:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,176:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,177:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,177:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,179:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,184:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,184:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,185:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,187:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,191:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,191:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,192:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,195:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,199:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,199:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,200:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,202:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,206:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,207:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,207:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,209:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,215:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,216:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,216:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,218:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,223:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,223:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,224:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,226:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,231:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,232:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,232:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,235:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,240:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,241:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,241:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,244:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,248:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,248:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,249:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,252:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,257:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,258:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,258:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,260:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,264:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,264:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,265:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,267:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,271:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,271:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,272:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,274:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,277:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,278:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,279:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,281:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,286:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,286:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,287:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,290:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,294:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,295:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,296:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,297:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,302:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,303:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,303:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,306:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,311:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,311:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,312:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,314:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,319:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,320:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,320:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,322:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,326:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,327:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,328:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,329:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,334:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,335:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,335:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,337:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,341:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,341:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,342:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,344:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,347:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,348:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,349:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,351:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,355:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,355:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,356:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,358:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,362:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,362:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,363:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,364:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,369:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,369:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,370:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,372:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,376:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,376:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,377:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,379:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,382:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,383:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,383:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,385:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,389:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,390:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,390:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,392:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,396:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,396:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,397:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,399:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,403:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,404:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,405:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,407:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,412:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,412:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,413:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,415:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,419:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,420:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,420:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,422:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,427:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,427:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,428:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,429:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,433:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,434:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,434:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,436:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,440:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,442:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,444:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,447:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,452:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,454:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,455:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,459:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,465:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,466:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,468:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,471:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,477:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,479:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,481:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,484:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,489:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,490:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,491:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,493:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,498:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,499:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,500:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,502:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,507:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,508:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,509:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,511:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,516:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,517:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,518:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,521:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,525:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,525:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,526:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,528:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,532:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,533:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,534:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,536:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,540:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,541:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,541:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,544:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,548:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,549:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,550:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,552:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,556:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,557:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,558:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,560:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,564:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,565:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,565:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,567:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,571:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,572:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,573:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,575:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,579:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,580:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,581:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,583:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,587:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,588:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,588:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,591:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,595:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,595:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,596:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,598:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,602:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,603:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,604:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,606:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,610:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,612:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,614:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,617:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,623:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,624:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,626:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,629:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,635:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,636:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,637:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,639:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,643:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,644:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,645:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,647:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,652:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,653:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,653:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,655:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,660:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,661:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,661:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,663:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,667:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,668:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,669:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,671:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,676:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,677:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,678:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,680:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,684:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,684:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,685:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,687:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,691:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,692:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,692:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,694:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,698:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,699:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,700:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,702:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,706:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,707:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,708:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,710:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,713:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,714:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,715:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,717:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,721:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,722:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,722:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,724:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,728:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,728:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,729:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,731:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,735:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,736:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,736:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,738:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,741:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,742:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,743:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,745:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,748:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,749:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,750:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,752:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,755:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,756:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,757:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,758:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,762:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,763:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,764:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,767:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,770:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,771:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,772:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,774:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,777:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,778:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,779:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,781:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,785:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,786:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,787:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,789:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,793:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,794:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,794:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,796:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,800:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,801:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,802:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,804:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,807:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,808:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,809:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,811:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,814:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,815:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,815:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,817:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,821:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,822:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,822:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,824:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,828:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,828:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,829:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,831:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,835:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,835:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,836:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,842:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,847:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,849:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,851:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,853:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,858:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,860:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,861:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,866:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,870:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,872:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,873:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,877:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,882:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,884:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,885:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,889:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,893:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,895:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,896:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,898:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,902:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,903:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,904:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,905:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,912:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,913:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,914:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,922:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,927:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,927:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,928:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,933:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,937:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,938:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,939:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,941:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,945:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,946:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,946:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,948:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,952:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,953:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,953:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,955:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,959:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,960:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,960:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,962:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,966:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,967:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,967:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,970:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,973:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,974:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,974:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,976:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,979:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,980:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,980:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,982:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,985:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,985:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,986:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,987:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,991:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,992:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,992:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:05,994:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:05,997:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:05,998:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:05,998:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,000:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,004:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,004:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,005:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,006:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,010:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,010:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,011:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,012:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,015:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,016:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,016:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,018:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,022:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,024:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,026:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,029:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,034:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,036:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,037:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,041:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,046:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,048:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,049:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,051:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,055:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,055:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,056:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,058:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,061:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,062:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,063:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,064:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,067:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,068:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,069:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,070:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,073:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,074:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,074:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,076:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,080:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,080:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,081:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,082:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,085:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,085:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,086:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,087:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,091:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,093:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,095:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,098:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,103:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,105:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,106:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,110:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,116:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,117:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,117:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,121:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,125:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,126:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,127:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,128:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,131:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,132:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,133:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,134:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,137:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,138:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,138:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,140:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,143:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,143:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,144:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,145:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,148:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,149:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,149:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,150:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,154:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,154:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,155:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,156:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,159:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,160:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,160:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,162:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,165:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,165:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,166:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,167:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,170:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,171:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,171:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,173:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,176:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,176:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,177:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,178:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,181:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,182:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,182:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,184:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,187:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,188:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,189:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,192:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,193:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,193:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,195:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,198:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,198:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,199:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,200:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,203:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,204:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,204:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,206:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,209:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,209:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,210:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,211:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,214:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,215:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,215:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,217:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,220:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,222:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,223:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,227:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,232:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,233:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,235:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,238:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,243:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,245:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,246:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,250:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,255:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,256:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,258:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,261:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,266:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,267:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,268:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,270:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,273:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,274:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,275:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,276:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,280:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,280:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,281:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,282:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,285:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,286:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,286:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,287:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,290:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,291:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,291:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,292:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,296:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,296:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,297:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,298:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,301:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,302:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,302:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,303:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,306:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,307:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,307:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,308:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,311:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,312:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,312:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,314:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,317:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,318:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,318:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,320:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,324:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,325:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,325:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,327:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,330:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,330:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,331:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,332:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,335:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,336:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,336:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,338:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,341:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,341:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,342:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,343:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,346:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,347:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,347:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,349:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,352:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,352:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,353:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,354:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,357:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,358:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,358:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,359:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,362:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,363:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,363:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,364:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,367:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,368:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,368:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,369:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,373:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,374:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,374:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,376:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,379:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,380:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,380:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,382:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,386:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,386:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,386:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,388:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,392:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,392:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,392:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:06,394:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:06,397:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:06,398:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:06,398:DEBUG:
    Ignoring line no. 24: 35
    


.. parsed-literal::

    7.8 ms ± 560 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


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

    2018-09-14 16:34:07,708:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:07,713:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:07,714:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:07,714:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:07,715:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:07,715:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:07,761:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:07,765:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:07,767:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:07,769:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:07,770:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:07,772:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:07,841:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:07,845:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:07,845:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:07,846:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:07,847:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:07,847:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:07,890:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:07,894:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:07,894:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:07,895:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:07,895:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:07,896:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:07,941:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:07,947:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:07,948:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:07,948:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:07,948:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:07,949:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:07,994:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:07,999:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,000:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,000:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,000:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,001:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,044:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,049:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,049:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,050:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,050:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,051:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,103:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,107:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,107:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,108:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,109:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,109:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,157:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,161:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,161:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,162:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,163:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,163:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,206:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,209:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,210:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,210:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,211:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,211:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,253:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,259:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,260:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,260:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,261:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,261:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,303:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,307:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,308:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,309:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,309:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,310:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,352:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,356:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,357:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,357:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,358:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,359:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,400:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,404:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,405:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,405:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,406:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,406:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,452:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,456:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,457:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,457:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,458:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,458:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,518:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,525:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,527:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,528:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,530:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,531:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,601:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,605:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,606:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,606:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,607:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,607:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,658:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,663:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,664:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,664:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,665:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,665:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,733:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,738:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,739:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,741:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,743:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,745:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,819:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,824:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,825:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,825:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,826:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,826:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,868:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,872:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,873:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,873:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,874:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,874:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,920:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,924:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,925:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,925:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,926:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,926:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:08,971:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:08,975:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:08,975:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:08,976:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:08,976:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:08,977:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,028:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,032:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,033:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,034:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,034:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,035:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,081:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,086:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,087:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,087:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,087:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,088:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,131:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,135:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,136:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,137:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,138:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,138:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,182:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,188:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,189:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,189:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,190:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,233:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,237:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,238:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,238:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,239:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,239:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,281:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,284:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,285:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,285:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,285:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,286:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,332:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,338:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,338:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,339:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,340:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,340:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,384:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,389:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,390:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,390:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,391:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,391:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,438:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,440:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,441:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,442:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,443:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,503:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,507:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,507:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,508:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,508:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,508:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,551:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,555:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,555:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,556:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,556:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,556:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,599:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,603:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,603:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,604:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,604:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,605:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,648:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,652:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,654:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,655:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,656:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,657:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,710:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,714:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,714:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,715:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,715:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,716:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,786:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,791:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,792:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,793:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,793:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,794:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,845:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,850:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,850:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,851:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,851:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,852:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,894:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,899:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,900:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,900:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,900:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,942:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,947:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,947:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,948:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,948:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,949:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:09,992:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:09,996:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:09,996:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:09,997:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:09,997:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:09,997:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,040:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,046:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,046:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,046:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,047:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,047:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,091:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,095:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,097:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,098:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,100:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,101:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,158:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,163:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,164:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,165:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,166:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,167:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,227:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,231:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,231:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,231:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,232:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,232:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,275:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,279:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,280:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,280:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,280:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,281:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,324:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,328:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,329:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,329:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,329:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,330:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,372:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,377:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,378:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,378:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,379:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,379:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,422:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,426:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,426:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,427:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,427:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,428:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,472:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,476:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,477:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,477:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,478:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,478:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,520:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,525:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,525:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,526:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,526:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,527:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,570:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,575:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,575:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,575:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,576:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,576:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,619:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,623:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,623:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,624:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,624:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,624:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,668:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,672:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,674:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,675:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,676:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,677:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,727:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,731:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,733:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,734:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,735:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,736:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,812:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,818:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,818:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,819:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,819:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,820:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,865:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,870:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,870:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,870:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,871:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,871:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,915:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,919:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,919:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,920:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,921:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,921:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:10,966:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:10,970:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:10,972:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:10,973:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:10,975:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:10,976:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,027:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,031:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,032:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,032:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,033:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,033:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,078:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,082:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,083:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,083:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,084:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,085:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,129:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,133:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,133:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,134:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,134:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,135:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,180:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,185:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,185:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,186:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,186:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,187:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,238:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,242:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,243:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,244:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,244:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,245:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,290:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,294:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,295:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,295:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,296:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,296:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,341:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,346:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,347:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,347:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,348:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,348:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,391:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,395:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,396:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,396:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,397:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,397:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,443:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,448:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,450:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,451:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,452:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,454:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,509:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,515:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,517:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,518:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,520:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,521:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,572:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,576:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,577:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,577:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,578:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,578:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,623:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,627:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,628:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,628:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,629:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,629:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,672:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,677:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,678:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,678:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,679:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,680:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,723:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,727:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,729:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,730:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,731:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,732:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,782:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,786:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,788:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,789:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,791:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,792:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,862:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,867:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,868:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,868:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,913:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,918:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,920:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,921:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,922:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,923:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:11,973:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:11,978:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:11,978:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:11,979:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:11,980:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:11,980:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:12,023:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:12,027:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:12,028:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:12,029:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:12,029:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:12,030:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:12,072:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:12,075:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:12,076:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:12,077:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:12,077:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:12,077:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:12,120:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:12,124:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:12,124:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:12,124:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:12,125:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:12,126:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    55.3 ms ± 3.03 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


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

    2018-09-14 16:34:12,377:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:12,381:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:12,382:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:12,382:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:12,382:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:12,383:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:12,434:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:12,438:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:12,439:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:12,439:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:12,440:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:12,440:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:12,493:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:12,497:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:12,497:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:12,498:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:12,498:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:12,499:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:12,552:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:12,556:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:12,556:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:12,557:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:12,557:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:12,557:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:12,609:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:12,613:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:12,614:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:12,614:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:12,615:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:12,615:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:12,667:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:12,672:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:12,672:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:12,673:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:12,673:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:12,674:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:12,726:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:12,730:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:12,731:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:12,731:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:12,731:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:12,732:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:12,787:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:12,791:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:12,792:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:12,792:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:12,793:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:12,793:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:12,849:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:12,853:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:12,853:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:12,853:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:12,854:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:12,855:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:12,924:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:12,928:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:12,929:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:12,929:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:12,930:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:12,930:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:12,984:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:12,989:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:12,989:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:12,990:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:12,990:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:12,990:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,042:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,046:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,046:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,047:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,047:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,048:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,102:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,107:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,108:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,108:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,109:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,109:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,164:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,168:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,169:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,169:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,170:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,170:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,223:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,227:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,229:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,230:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,231:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,232:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,291:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,295:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,297:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,299:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,300:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,301:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,360:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,365:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,365:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,366:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,366:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,367:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,420:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,423:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,424:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,424:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,425:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,425:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,476:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,480:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,481:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,481:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,482:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,482:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,536:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,541:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,543:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,545:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,546:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,547:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,605:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,609:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,610:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,610:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,611:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,611:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,663:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,668:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,670:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,671:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,672:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,673:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,731:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,734:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,735:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,735:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,736:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,736:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,787:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,792:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,793:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,793:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,794:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,794:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,847:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,851:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,852:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,852:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,853:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,853:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,908:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,912:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,914:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:13,916:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:13,917:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:13,918:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:13,995:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:13,999:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:13,999:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,000:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,000:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,001:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,054:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,058:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,058:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,059:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,059:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,059:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,110:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,114:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,115:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,115:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,115:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,116:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,166:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,169:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,170:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,170:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,171:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,171:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,224:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,228:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,228:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,229:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,229:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,230:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,281:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,287:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,287:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,287:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,288:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,288:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,339:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,344:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,344:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,345:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,345:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,398:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,401:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,402:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,402:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,403:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,403:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,457:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,462:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,462:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,463:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,463:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,463:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,515:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,520:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,520:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,521:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,521:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,522:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,574:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,579:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,580:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,580:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,581:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,581:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,635:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,639:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,640:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,640:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,640:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,641:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,706:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,710:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,711:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,711:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,712:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,712:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,765:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,770:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,770:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,771:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,771:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,772:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,824:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,829:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,829:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,830:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,830:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,831:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,884:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,889:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,889:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,890:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,890:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,891:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:14,948:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:14,954:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:14,954:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:14,955:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:14,955:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:14,956:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,031:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,035:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,036:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,036:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,036:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,037:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,093:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,097:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,097:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,098:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,098:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,098:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,152:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,155:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,156:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,157:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,157:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,158:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,211:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,216:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,217:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,218:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,218:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,218:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,269:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,274:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,274:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,275:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,275:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,276:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,329:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,333:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,334:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,334:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,334:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,335:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,388:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,392:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,392:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,393:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,393:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,393:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,444:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,449:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,449:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,450:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,450:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,451:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,505:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,509:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,510:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,510:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,511:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,511:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,564:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,569:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,570:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,570:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,571:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,571:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,627:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,631:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,631:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,632:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,632:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,633:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,686:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,691:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,691:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,692:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,692:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,692:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,757:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,762:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,764:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,765:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,766:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,767:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,827:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,831:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,832:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,833:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,833:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,885:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,889:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,890:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,890:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,891:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,892:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:15,945:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:15,949:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:15,949:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:15,950:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:15,951:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:15,951:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,007:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,011:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,012:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,012:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,013:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,014:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,087:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,092:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,093:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,093:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,094:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,094:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,148:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,152:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,153:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,153:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,154:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,154:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,206:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,209:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,210:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,210:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,211:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,211:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,263:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,267:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,269:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,271:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,272:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,273:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,331:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,335:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,337:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,339:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,341:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,341:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,401:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,404:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,405:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,406:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,406:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,406:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,458:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,462:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,462:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,463:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,464:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,464:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,516:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,520:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,521:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,521:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,522:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,522:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,576:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,581:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,581:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,582:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,582:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,583:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,637:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,640:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,641:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,641:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,642:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,642:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,696:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,700:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,700:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,701:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,702:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,702:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,754:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,757:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,759:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,760:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,762:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,762:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,821:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,824:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,825:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,825:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,825:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,826:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,879:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,886:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,886:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,887:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,888:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,888:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:16,941:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:16,948:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:16,949:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:16,949:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:16,950:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:16,950:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:17,005:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:17,009:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:17,009:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:17,010:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:17,010:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:17,011:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:17,066:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:17,070:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:17,070:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:17,071:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:17,071:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:17,072:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:17,143:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:17,147:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:17,148:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:17,148:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:17,149:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:17,149:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:17,203:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:17,206:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:17,207:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:17,207:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:17,208:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:17,208:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:17,259:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:17,263:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:17,264:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:17,264:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:17,265:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:17,265:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-14 16:34:17,316:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-14 16:34:17,537:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-14 16:34:17,541:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-14 16:34:17,544:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-14 16:34:17,547:DEBUG:
    REACHED DATA BLOCK
    2018-09-14 16:34:17,550:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    65.6 ms ± 9.14 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

