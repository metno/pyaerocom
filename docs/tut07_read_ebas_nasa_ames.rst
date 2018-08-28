
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

    2018-08-28 14:19:49,592:INFO:
    Reading aliases ini file: /home/jonasg/github/cloned/pyaerocom/pyaerocom/data/aliases.ini
    2018-08-28 14:19:50,329:WARNING:
    geopy library is not available. Aeolus data read not enabled
    2018-08-28 14:19:50,376:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,532:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,534:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,536:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,538:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:19:50,539:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

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
                  <pyaerocom.io.ebas_nasa_ames.EbasFlagCol at 0x7f77f7253d30>)])



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

    2018-08-28 14:19:50,767:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,771:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,772:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,772:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,774:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,777:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,778:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,778:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,779:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,783:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,783:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,783:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,785:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,788:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,789:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,789:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,790:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,794:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,795:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,795:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,796:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,800:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,801:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,801:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,803:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,806:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,808:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,810:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,813:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,818:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,820:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,821:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,825:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,832:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,834:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,835:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,839:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,844:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,846:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,847:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,852:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,856:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,858:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,859:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,862:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,868:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,869:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,871:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,875:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,879:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,881:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,883:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,886:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,890:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,891:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,893:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,895:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,900:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,901:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,903:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,907:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,908:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,909:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,911:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,914:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,915:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,916:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,918:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,921:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,922:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,923:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,925:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,928:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,929:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,930:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,932:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,936:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,937:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,938:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,940:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,945:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,946:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,948:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,952:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,958:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,960:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,962:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,966:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,970:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,972:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,974:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,977:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,982:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,983:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,985:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:50,989:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:50,994:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:50,996:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:50,998:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,002:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,006:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,008:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,010:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,014:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,019:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,021:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,023:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,026:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,031:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,033:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,035:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,038:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,044:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,045:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,047:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,051:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,055:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,057:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,058:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,060:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,064:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,066:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,066:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,069:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,074:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,076:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,077:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,079:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,084:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,085:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,086:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,089:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,093:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,094:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,095:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,098:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,101:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,103:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,104:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,106:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,110:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,112:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,113:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,115:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,121:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,123:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,125:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,129:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,133:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,134:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,135:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,138:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,141:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,143:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,144:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,146:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,150:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,150:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,151:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,153:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,156:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,157:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,158:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,160:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,164:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,165:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,166:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,167:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,171:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,171:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,172:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,174:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,178:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,179:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,180:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,181:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,185:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,185:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,186:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,188:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,191:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,192:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,193:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,195:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,198:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,199:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,199:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,205:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,206:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,206:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,208:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,211:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,212:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,212:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,214:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,218:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,219:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,219:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,221:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,226:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,226:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,227:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,229:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,232:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,233:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,233:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,235:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,239:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,240:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,241:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,242:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,246:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,246:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,247:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,249:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,253:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,253:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,254:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,256:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,259:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,260:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,260:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,262:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,266:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,268:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,270:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,274:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,279:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,280:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,282:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,286:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,291:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,293:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,295:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,299:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,303:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,305:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,307:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,310:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,315:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,317:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,318:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,323:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,328:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,330:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,332:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,335:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,341:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,343:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,344:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,347:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,352:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,354:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,356:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,360:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,368:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,370:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,372:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:51,385:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:51,390:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:51,392:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:51,394:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,003:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,009:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,012:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,014:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,017:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,022:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,024:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,025:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,029:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,035:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,038:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,039:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,043:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,047:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,049:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,051:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,054:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,059:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,060:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,062:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,065:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,069:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,071:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,073:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,077:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,082:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,084:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,085:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,089:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,094:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,096:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,098:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,101:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,106:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,108:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,109:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,113:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,117:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,119:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,121:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,124:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,128:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,130:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,131:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,133:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,137:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,138:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,139:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,141:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,144:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,145:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,145:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,147:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,150:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,151:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,151:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,153:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,156:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,157:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,157:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,159:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,163:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,164:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,164:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,165:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,169:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,169:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,170:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,171:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,175:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,176:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,176:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,179:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,182:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,183:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,183:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,185:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,189:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,190:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,190:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,192:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,195:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,195:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,196:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,197:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,201:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,202:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,203:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,204:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,208:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,209:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,209:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,211:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,214:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,215:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,215:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,216:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,220:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,222:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,223:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,227:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,232:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,234:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,235:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,238:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,243:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,245:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,247:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,250:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,255:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,256:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,258:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,261:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,266:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,268:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,270:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,273:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,278:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,279:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,280:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,283:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,287:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,288:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,288:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,290:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,295:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,297:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,299:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,302:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,307:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,309:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,311:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,314:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,319:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,321:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,323:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,327:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,332:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,333:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,334:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,337:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,341:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,342:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,343:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,345:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,349:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,351:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,352:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,354:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,358:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,359:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,360:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,363:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,367:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,368:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,369:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,373:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,376:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,378:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,379:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,381:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,388:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,388:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,389:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,395:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,398:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,399:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,400:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,401:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,405:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,405:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,406:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,408:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,411:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,412:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,412:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,414:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,418:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,418:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,419:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,421:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,424:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,426:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,428:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,432:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,437:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,439:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,440:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,444:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,449:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,451:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,453:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,456:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,461:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,462:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,463:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,467:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,470:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,471:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,472:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,474:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,478:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,479:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,480:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,482:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,486:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,487:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,488:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,490:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,494:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,495:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,496:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,498:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,502:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,503:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,504:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,506:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,510:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,511:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,511:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,513:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,517:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,518:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,519:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,521:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,524:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,525:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,526:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,528:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,532:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,533:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,533:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,535:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,539:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,540:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,541:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,543:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,546:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,547:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,548:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,550:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,554:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,555:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,555:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,557:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,561:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,562:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,563:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,565:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,568:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,569:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,570:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,573:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,578:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,579:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,579:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,582:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,585:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,588:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,589:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,592:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,597:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,599:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,600:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,605:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,611:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,612:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,614:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,618:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,623:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,625:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,626:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,630:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,634:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,636:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,637:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,640:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,645:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,647:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,648:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,652:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,657:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,658:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,660:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,663:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,667:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,668:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,669:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,672:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,676:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,677:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,677:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,681:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,685:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,686:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,686:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,688:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,692:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,693:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,694:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,696:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,700:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,700:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,701:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,703:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,707:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,708:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,708:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,710:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,714:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,715:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,716:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,718:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,721:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,722:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,723:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,725:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,728:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,729:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,730:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,732:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,736:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,736:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,737:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,739:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,743:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,744:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,744:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,747:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,750:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,751:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,752:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,754:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,757:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,758:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,759:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,761:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,764:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,765:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,766:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,768:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,772:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,773:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,773:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,775:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,779:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,780:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,781:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,783:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,786:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,787:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,788:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,790:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,793:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,794:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,795:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,797:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,800:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,801:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,802:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,804:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,807:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,808:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,809:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,811:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,814:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,815:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,816:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,818:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,822:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,822:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,823:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,824:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,828:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,828:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,829:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,830:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,834:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,834:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,835:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,836:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,840:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,841:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,841:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,843:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,846:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,847:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,847:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,849:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,852:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,852:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,853:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,855:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,858:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,859:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,859:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,860:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,864:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,864:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,865:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,866:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,869:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,870:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,870:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,872:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,875:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,876:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,876:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,878:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,881:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,881:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,882:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,883:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,887:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,887:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,888:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,889:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,893:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,893:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,894:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,895:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,899:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,899:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,901:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,906:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,907:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,907:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,909:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,912:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,913:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,913:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,914:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,918:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,919:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,919:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,921:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,924:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,925:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,925:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,927:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,930:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,931:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,931:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,933:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,936:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,937:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,937:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,939:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,942:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,943:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,943:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,945:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,948:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,949:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,949:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,951:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,954:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,955:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,955:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,958:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,961:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,961:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,962:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,964:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,967:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,968:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,968:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,970:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,974:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,975:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,975:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,977:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,981:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,981:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,982:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,984:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,987:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,988:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,988:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,990:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:52,993:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:52,994:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:52,994:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:52,996:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,000:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,001:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,001:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,008:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,012:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,012:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,013:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,015:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,018:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,019:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,019:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,021:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,024:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,025:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,025:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,027:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,031:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,031:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,032:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,033:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,037:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,038:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,038:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,040:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,043:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,044:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,045:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,047:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,050:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,051:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,051:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,053:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,057:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,057:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,058:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,060:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,064:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,064:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,065:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,067:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,071:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,071:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,072:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,073:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,077:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,078:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,078:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,080:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,083:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,084:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,084:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,086:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,089:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,090:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,091:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,092:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,096:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,097:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,097:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,099:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,103:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,104:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,104:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,106:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,110:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,111:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,114:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,117:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,122:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,123:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,125:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,128:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,133:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,135:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,135:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,138:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,142:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,143:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,144:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,145:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,149:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,150:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,150:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,152:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,155:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,156:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,156:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,158:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,161:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,164:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,165:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,167:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,171:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,173:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,174:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,176:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,179:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,180:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,181:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,182:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,186:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,186:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,187:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,189:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,192:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,193:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,194:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,195:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,199:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,200:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,200:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,202:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,206:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,208:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,209:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,212:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,217:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,219:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,220:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,223:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,227:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,229:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,230:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,233:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,239:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,240:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,241:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,244:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,248:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,249:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,249:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,251:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,255:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,255:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,256:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,258:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,261:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,263:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,264:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,268:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,273:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,275:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,276:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,279:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,284:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,285:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,286:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,288:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,292:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,293:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,294:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,296:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,300:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,301:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,301:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,303:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,307:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,308:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,309:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,311:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,314:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,315:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,316:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,318:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,322:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,322:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,323:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,325:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,328:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,329:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,330:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,332:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,335:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,336:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,337:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,339:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,342:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,343:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,344:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,345:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,349:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,350:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,351:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,353:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,357:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,357:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,358:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,361:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,364:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,365:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,366:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,368:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,372:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,373:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,374:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,378:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,382:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,383:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,383:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,389:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,393:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,394:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,395:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,400:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,404:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,405:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,405:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,407:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,411:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,412:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,412:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,414:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,418:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,419:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,420:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,422:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,426:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,428:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,430:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,434:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,438:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,440:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,443:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,446:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,450:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,452:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,454:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,457:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,462:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,464:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,465:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,468:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,473:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,474:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,476:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,479:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,483:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,484:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,485:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,487:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,491:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,492:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,492:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,494:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,497:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,498:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,498:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,500:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,503:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,503:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,504:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,506:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,509:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,509:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,510:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,511:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,515:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,516:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,516:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,518:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,521:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,521:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,522:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,523:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,526:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,527:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,527:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,528:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,532:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,533:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,533:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,534:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,537:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,538:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,538:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,539:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,542:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,543:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,543:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,545:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,548:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,548:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,548:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,550:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,554:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,554:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,554:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,556:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,559:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,560:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,560:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,561:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,565:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,565:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,566:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,567:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,571:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,571:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,572:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,573:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,577:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,577:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,577:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,579:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,584:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,584:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,584:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,586:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,589:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,589:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,589:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,591:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,595:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,595:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,598:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,602:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,602:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,604:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,609:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,609:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,610:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,611:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,615:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,615:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,615:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,617:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,621:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,621:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,622:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,623:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,627:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,629:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,631:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,636:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,640:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,642:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,644:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,647:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,652:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,653:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,655:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,659:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,663:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,665:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,667:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,671:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,676:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,678:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,680:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,682:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,687:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,688:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,688:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,690:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,694:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,695:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,695:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,697:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,700:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,701:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,704:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,708:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,709:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,709:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,711:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,714:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,715:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,715:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,717:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,720:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,721:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,721:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,723:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,727:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,728:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,728:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,730:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,734:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,734:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,735:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,737:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,740:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,741:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,741:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,743:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,747:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,748:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,748:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,750:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,753:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,754:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,754:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,756:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,759:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,760:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,761:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,762:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,766:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,766:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,767:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,769:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,772:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,773:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,773:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,775:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,779:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,780:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,780:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,782:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,785:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,786:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,786:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,788:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,791:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,792:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,792:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,794:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,798:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,799:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,800:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,801:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,805:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,806:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,806:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,808:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,811:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,812:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,813:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,814:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,818:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,818:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,819:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,820:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,824:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,824:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,825:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,827:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,830:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,831:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,831:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,833:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,837:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,838:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,838:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,840:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,844:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,845:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,845:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,847:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,850:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,851:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,851:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,853:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,857:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,858:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,859:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,861:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,865:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,865:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,866:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,868:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,871:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,872:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,873:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,874:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,878:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,879:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,879:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,881:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,885:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,886:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,886:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,888:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,891:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,892:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,893:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,894:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,898:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,899:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,899:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,901:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,904:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,905:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,906:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,908:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,911:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,912:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,912:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,914:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,918:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,919:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,919:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,921:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,926:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,927:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,928:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,929:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,934:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,934:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,935:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,937:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,940:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,941:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,942:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,943:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,947:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,948:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,948:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,951:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,956:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,956:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,957:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,959:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,962:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,963:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,964:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,965:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,969:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,969:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,970:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,972:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,975:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,976:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,977:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,979:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,982:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,983:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,983:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,986:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,989:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,990:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,990:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:53,992:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:53,997:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:53,998:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:53,999:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,001:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,004:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,005:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,006:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,008:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,012:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,012:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,013:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,019:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,023:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,024:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,024:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,026:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,030:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,031:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,032:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,033:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,037:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,038:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,038:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,042:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,046:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,047:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,047:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,049:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,054:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,054:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,055:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,057:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,061:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,061:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,062:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,063:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,067:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,068:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,068:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,070:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,074:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,074:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,075:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,077:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,081:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,081:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,082:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,084:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,087:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,088:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,088:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,090:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,093:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,094:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,095:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,096:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,100:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,101:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,101:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,103:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,106:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,107:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,107:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,109:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,113:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,113:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,114:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,116:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,119:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,119:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,120:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,123:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,126:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,127:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,127:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,129:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,133:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,134:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,134:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,136:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,140:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,140:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,141:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,143:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,146:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,147:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,147:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,149:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,153:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,153:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,154:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,156:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,159:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,160:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,161:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,162:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,166:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,167:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,168:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,169:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,173:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,174:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,174:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,176:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,179:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,180:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,180:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,182:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,187:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,188:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,190:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,193:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,194:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,194:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,196:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,200:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,200:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,201:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,203:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,206:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,206:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,207:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,209:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,212:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,212:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,213:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,215:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,218:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,218:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,219:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,220:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,224:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,225:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,225:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,227:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,231:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,232:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,233:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,234:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,237:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,238:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,238:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,240:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,244:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,244:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,245:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,247:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,251:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,252:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,252:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,255:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,258:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,259:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,259:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,262:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,265:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,266:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,266:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,269:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,272:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,273:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,273:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,277:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,280:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,280:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,281:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,283:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,286:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,287:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,287:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,289:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,293:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,293:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,294:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,296:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,299:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,300:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,300:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,302:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,305:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,306:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,306:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,308:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,311:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,312:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,312:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,314:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,318:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,318:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,319:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,322:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,325:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,326:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,326:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,328:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,332:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,333:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,333:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,335:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,338:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,339:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,339:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,342:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,345:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,346:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,346:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,348:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,352:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,352:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,353:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,355:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,361:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,363:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,365:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,368:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,374:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,377:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,379:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,383:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,388:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,389:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,389:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,396:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,401:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,402:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,402:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,409:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,412:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,413:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,414:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,416:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,420:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,422:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,422:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,424:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,429:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,430:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,430:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:54,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:54,437:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:54,438:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:54,438:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,599:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,604:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,607:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,609:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,612:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,618:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,620:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,622:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,627:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,633:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,635:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,639:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,643:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,647:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,648:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,649:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,650:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,654:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,655:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,655:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,657:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,660:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,661:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,661:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,663:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,665:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,666:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,667:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,669:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,672:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,672:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,673:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,674:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,678:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,679:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,679:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,681:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,684:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,685:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,685:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,688:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,691:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,692:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,692:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,694:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,697:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,698:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,698:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,699:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,703:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,703:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,704:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,706:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,709:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,710:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,711:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,712:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,716:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,716:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,717:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,718:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,722:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,722:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,723:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,724:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,727:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,728:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,728:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,730:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,734:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,734:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,735:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,738:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,742:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,743:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,743:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,745:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,749:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,750:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,750:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,752:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,755:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,756:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,757:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,758:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,761:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,762:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,762:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,764:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,767:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,767:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,768:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,769:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,772:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,773:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,773:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,774:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,777:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,778:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,779:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,780:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,783:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,784:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,784:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,786:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,788:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,789:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,789:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,790:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,794:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,794:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,795:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,796:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,800:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,800:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,801:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,803:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,806:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,806:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,807:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,808:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,812:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,812:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,812:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,814:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,817:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,817:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,818:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,819:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,822:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,823:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,823:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,824:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,827:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,828:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,828:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,829:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,833:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,833:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,834:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,836:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,839:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,839:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,839:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,841:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,844:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,844:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,845:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,846:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,849:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,849:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,850:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,851:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,855:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,855:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,856:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,857:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,861:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,861:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,862:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,863:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,867:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,869:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,872:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,872:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,873:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,874:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,878:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,878:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,879:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,880:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,883:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,884:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,884:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,885:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,888:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,889:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,889:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,891:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,894:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,894:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,895:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,897:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,900:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,901:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,901:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,903:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,906:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,906:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,907:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,908:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,912:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,912:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,913:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,914:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,917:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,918:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,919:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,920:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,923:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,923:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,924:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,925:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,928:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,929:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,929:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,930:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,933:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,934:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,934:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,936:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,939:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,939:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,940:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,941:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,944:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,944:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,945:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,946:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,950:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,950:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,950:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,952:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,955:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,956:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,956:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,958:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,962:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,962:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,963:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,964:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,968:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,968:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,969:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,970:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,974:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,974:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,975:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,976:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,980:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,980:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,981:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,982:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,985:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,986:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,986:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,988:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,991:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,991:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,992:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,993:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:56,997:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:56,997:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:56,998:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:56,999:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,003:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,003:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,003:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,005:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,008:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,009:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,009:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,010:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,014:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,014:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,014:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,016:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,020:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,021:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,021:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,022:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,026:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,026:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,027:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,028:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,031:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,032:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,032:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,033:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,038:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,039:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,039:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,041:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,044:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,044:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,045:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,046:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,049:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,050:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,050:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,051:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,055:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,056:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,058:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,064:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,068:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,072:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,074:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,078:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,083:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,084:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,086:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,089:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,094:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,096:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,097:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,100:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,104:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,105:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,106:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,108:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,111:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,112:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,112:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,115:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,118:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,118:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,119:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,120:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,123:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,124:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,124:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,127:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,130:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,131:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,131:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,133:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,136:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,136:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,138:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,139:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,142:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,143:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,143:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,145:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,149:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,150:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,150:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,152:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,157:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,161:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,164:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,169:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,174:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,175:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,176:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,179:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,183:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,184:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,184:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,186:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,189:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,190:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,190:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,191:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,195:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,195:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,196:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,198:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,201:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,201:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,202:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,204:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,207:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,207:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,208:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,209:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,212:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,213:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,213:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,214:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,218:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,218:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,218:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,220:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,223:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,224:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,224:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,226:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,229:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,229:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,230:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,231:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,234:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,234:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,235:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,236:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,239:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,240:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,240:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,241:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,245:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,246:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,246:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,247:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,251:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,251:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,252:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,253:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,256:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,256:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,257:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,258:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,262:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,262:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,263:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,264:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,267:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,268:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,268:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,270:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,273:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,274:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,274:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,276:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,279:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,280:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,280:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,282:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,285:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,286:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,286:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,287:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,291:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,291:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,292:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,293:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,296:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,297:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,297:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,300:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,304:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,304:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,304:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,306:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,310:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,310:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,311:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,312:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,316:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,316:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,316:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,318:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,321:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,321:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,322:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,324:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,327:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,327:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,328:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,329:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,333:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,334:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,334:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,336:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,339:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,340:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,340:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,342:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,348:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,350:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,351:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,355:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,360:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,362:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,363:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,367:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,372:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,374:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,375:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,379:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,383:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,385:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,386:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,390:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,394:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,395:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,396:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,398:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,404:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,405:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,405:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,407:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,411:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,412:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,412:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,414:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,417:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,418:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,419:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,420:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,424:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,424:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,425:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,427:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,430:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,431:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,431:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,439:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,439:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,440:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,442:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,445:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,446:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,447:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,448:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,452:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,453:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,453:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,455:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,458:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,459:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,459:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,461:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,465:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,466:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,466:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,468:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,471:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,472:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,473:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,476:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,480:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,480:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,481:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,483:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,487:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,490:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,492:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,496:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,501:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,503:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,504:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,508:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,513:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,515:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,517:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,521:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,525:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,527:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,528:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,532:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,537:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,538:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,539:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,541:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,545:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,546:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,547:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,549:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,552:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,553:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,553:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,555:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,560:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,561:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,561:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,563:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,566:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,566:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,567:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,568:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,572:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,573:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,573:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,575:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,579:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,580:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,580:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,583:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,587:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,587:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,588:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,603:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,607:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,608:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,608:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,610:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,613:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,614:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,614:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,616:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,619:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,620:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,620:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,622:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,625:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,626:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,626:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,627:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,631:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,632:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,632:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,634:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,637:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,638:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,638:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,640:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,643:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,644:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,644:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,646:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,650:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,650:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,650:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,652:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,656:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,658:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,660:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,667:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,672:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,675:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,676:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,681:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,685:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,686:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,687:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,689:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,692:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,694:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,695:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,697:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,701:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,702:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,703:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,706:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,707:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,707:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,708:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,712:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,713:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,714:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,715:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,719:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,719:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,720:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,722:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,725:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,726:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,726:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,728:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,733:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,733:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,734:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,736:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,739:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,739:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,740:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,741:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,745:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,746:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,746:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,748:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,752:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,753:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,753:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,755:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,758:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,758:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,759:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,760:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,764:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,764:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,765:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,767:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,771:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,771:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,771:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,773:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,776:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,777:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,777:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,778:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,781:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,782:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,782:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,783:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,787:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,788:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,789:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,796:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,799:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,800:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,801:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,802:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,806:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,806:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,807:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,808:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,811:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,812:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,814:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,816:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,819:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,820:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,820:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,822:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,826:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,826:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,827:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,828:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,832:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,832:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,834:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,837:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,838:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,838:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,840:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,843:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,843:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,844:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,845:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,848:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,849:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,849:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,851:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,855:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,856:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,856:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,857:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,860:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,861:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,861:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,863:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,868:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,871:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,876:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,881:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,883:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,884:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:19:57,888:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:19:57,893:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:19:57,895:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:19:57,896:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,049:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,056:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,059:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,061:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,067:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,073:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,076:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,078:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,083:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,089:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,092:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,093:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,101:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,106:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,107:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,109:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,111:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,114:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,115:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,116:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,118:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,124:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,124:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,125:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,127:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,130:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,131:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,131:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,133:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,136:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,137:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,138:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,140:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,144:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,144:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,145:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,146:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,150:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,151:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,151:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,153:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,157:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,158:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,158:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,161:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,166:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,166:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,167:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,168:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,172:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,172:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,173:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,174:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,178:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,179:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,179:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,181:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,184:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,184:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,185:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,186:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,190:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,192:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,194:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,199:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,205:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,208:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,210:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,214:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,219:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,222:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,224:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,229:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,234:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,235:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,237:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,240:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,244:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,245:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,245:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,247:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,252:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,253:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,253:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,255:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,260:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,261:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,261:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,263:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,267:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,268:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,269:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,271:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,274:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,275:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,276:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,278:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,281:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,282:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,283:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,285:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,288:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,289:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,289:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,291:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,296:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,297:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,297:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,299:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,303:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,304:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,304:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,307:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,311:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,312:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,313:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,315:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,318:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,319:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,319:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,321:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,325:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,326:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,326:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,328:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,332:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,333:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,337:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,340:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,344:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,344:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,346:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,350:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,350:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,351:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,353:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,357:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,358:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,359:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,360:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,364:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,365:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,365:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,367:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,370:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,371:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,371:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,373:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,378:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,378:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,379:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,381:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,385:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,385:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,386:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:01,387:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:01,390:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:01,391:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:01,391:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,456:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,460:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,461:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,461:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,463:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,466:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,467:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,467:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,469:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,473:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,473:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,474:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,475:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,478:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,479:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,479:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,480:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,483:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,484:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,484:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,486:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,489:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,490:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,490:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,492:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,495:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,498:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,500:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,505:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,510:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,513:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,515:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,519:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,524:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,528:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,530:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,533:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,537:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,538:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,539:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,543:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,546:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,548:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,549:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,551:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,556:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,558:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,559:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,562:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,566:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,567:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,568:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,571:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,576:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,577:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,578:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,582:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,586:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,587:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,587:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,589:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,593:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,594:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,594:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,596:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,600:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,600:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,601:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,603:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,606:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,607:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,607:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,610:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,613:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,614:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,615:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,617:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,620:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,623:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,625:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,628:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,633:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,635:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,637:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,641:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,645:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,647:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,648:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,651:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,655:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,657:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,659:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,663:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,670:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,671:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,673:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,676:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,680:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,681:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,683:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,684:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,688:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,689:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,689:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,691:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,694:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,694:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,695:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,696:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,699:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,700:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,700:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,702:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,706:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,706:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,706:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,708:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,713:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,714:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,714:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,716:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,720:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,720:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,721:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,722:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,726:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,727:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,727:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,728:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,732:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,733:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,733:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,735:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,740:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,741:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,741:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,743:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,747:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,747:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,748:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,749:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,753:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,754:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,754:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,755:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,758:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,759:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,759:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,761:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,764:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,764:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,765:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,767:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,770:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,771:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,771:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,773:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,777:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,778:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,778:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,780:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,784:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,784:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,785:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,786:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,790:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,792:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,794:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,798:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,804:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,807:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,809:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,815:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,823:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,825:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,827:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,830:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,834:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,835:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,835:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,839:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,843:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,844:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,844:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,845:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,849:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,849:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,850:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,852:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,855:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,856:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,857:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,858:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,862:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,862:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,863:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,864:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,868:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,868:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,869:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,871:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,874:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,875:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,875:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,877:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,880:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,881:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,881:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,884:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,887:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,888:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,888:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,890:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,894:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,895:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,895:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,897:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,900:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,901:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,901:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,903:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,906:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,907:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,907:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,909:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,912:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,912:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,913:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,914:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,917:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,918:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,919:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,921:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,924:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,925:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,926:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,929:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,933:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,934:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,934:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,936:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,939:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,940:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,941:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,942:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,945:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,946:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,946:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,948:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,952:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,953:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,953:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,955:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,959:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,960:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,960:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,962:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,965:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,966:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,966:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,968:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,973:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,974:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,974:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,976:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,979:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,980:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,980:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,982:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,985:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,986:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,986:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,988:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:02,992:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:02,994:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:02,995:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:02,998:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,003:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,005:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,007:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:03,010:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,015:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,016:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,017:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:03,021:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,026:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,028:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,030:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:03,033:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,037:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,039:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,040:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:03,043:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,048:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,049:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,050:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:03,052:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,055:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,056:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,057:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:03,058:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,063:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,063:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,064:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:03,065:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,069:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,070:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,070:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:03,072:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,075:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,075:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,076:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:03,077:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,080:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,081:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,081:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:03,083:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,086:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,087:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,087:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:03,088:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,092:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,092:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,093:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:03,094:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,097:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,098:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,098:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:03,099:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,103:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,103:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,104:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:03,105:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:03,109:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:03,109:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:03,110:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,550:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,559:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,562:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,565:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,572:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,577:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,580:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,583:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,589:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,596:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,598:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,601:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,605:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,606:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,607:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,614:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,620:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,621:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,622:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,624:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,628:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,629:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,630:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,631:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,635:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,635:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,636:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,637:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,641:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,641:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,642:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,643:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,646:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,647:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,647:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,649:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,653:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,654:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,654:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,656:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,660:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,663:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,665:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,671:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,679:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,683:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,686:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,691:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,697:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,699:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,700:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,702:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,706:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,707:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,708:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,709:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,713:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,714:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,715:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,717:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,720:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,721:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,722:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,724:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,727:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,728:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,729:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,731:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,735:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,736:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,737:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,739:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,742:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,743:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,744:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,746:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,749:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,750:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,751:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,753:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,756:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,757:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,758:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,759:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,763:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,765:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,766:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,771:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,776:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,777:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,778:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,780:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,783:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,784:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,785:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,788:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,791:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,792:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,793:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,795:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,799:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,800:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,800:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,802:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,805:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,806:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,806:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,808:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,813:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,813:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,814:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,815:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,818:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,819:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,819:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,821:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,824:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,825:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,825:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,827:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,830:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,831:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,831:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:04,833:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:04,836:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:04,837:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:04,837:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,648:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,655:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,658:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,661:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,668:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,676:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,678:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,679:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,682:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,686:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,687:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,688:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,689:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,693:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,694:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,694:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,696:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,700:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,701:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,703:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,707:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,708:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,709:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,711:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,715:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,718:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,720:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,724:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,729:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,731:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,733:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,738:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,743:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,745:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,745:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,747:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,751:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,752:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,753:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,755:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,759:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,760:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,760:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,763:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,767:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,768:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,769:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,771:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,776:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,777:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,778:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,780:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,784:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,785:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,785:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,788:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,792:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,793:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,794:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,796:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,800:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,801:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,802:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,804:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,809:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,810:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,810:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,812:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,816:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,817:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,818:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,820:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,823:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,824:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,825:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,827:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,832:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,833:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,835:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,840:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,841:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,841:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,844:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,848:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,849:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,849:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,852:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,855:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,857:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,858:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,860:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,864:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,865:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,866:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,868:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,873:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,874:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,876:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,878:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,881:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,882:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,883:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,884:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,887:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,888:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,888:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,890:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,894:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,894:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,895:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,896:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,901:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,901:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,902:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,903:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,907:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,908:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,908:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,911:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,915:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,918:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,920:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,926:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,932:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,935:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,937:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,943:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,949:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,951:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,953:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,956:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,962:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,964:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,968:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,972:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,977:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,979:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,980:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,982:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,986:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,986:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,987:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,989:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:06,993:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:06,994:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:06,994:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:06,996:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,000:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,000:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,001:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,003:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,008:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,010:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,011:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,015:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,019:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,020:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,020:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,022:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,026:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,027:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,027:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,029:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,032:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,033:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,033:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,035:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,038:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,038:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,039:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,040:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,044:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,044:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,045:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,047:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,050:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,051:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,051:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,053:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,057:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,057:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,057:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,060:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,064:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,064:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,064:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,066:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,069:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,070:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,070:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,072:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,075:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,076:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,076:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,078:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,081:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,082:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,082:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,085:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,088:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,089:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,089:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,091:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,095:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,097:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,099:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,103:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,109:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,112:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,115:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,119:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:07,124:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:07,125:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:07,126:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:07,128:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,699:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,701:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,719:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,722:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,723:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,724:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,726:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,729:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,730:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,730:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,732:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,735:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,736:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,737:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,739:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,742:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,743:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,743:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,745:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,749:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,749:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,750:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,751:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,755:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,756:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,757:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,758:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,761:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,762:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,763:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,765:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,768:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,769:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,769:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,771:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,774:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,775:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,776:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,777:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,780:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,781:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,782:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,783:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,787:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,787:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,788:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,790:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,794:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,795:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,795:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,797:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,802:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,804:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,806:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,811:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,819:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,822:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,825:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,828:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,833:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,834:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,835:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,837:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,841:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,842:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,843:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,845:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,849:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,850:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,851:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,853:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,857:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,859:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,859:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,862:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,867:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,868:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,871:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,874:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,875:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,876:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,878:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,881:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,882:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,883:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,884:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,888:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,889:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,890:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,891:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,895:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,895:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,896:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,897:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,900:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,901:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,901:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,903:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,907:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,908:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,908:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,909:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,913:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,914:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,914:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,916:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,919:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,919:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,920:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,921:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,925:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,926:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,926:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,928:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,932:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,934:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,936:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:08,942:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:08,950:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:08,952:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:08,954:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:10,802:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:10,811:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:10,814:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:10,817:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:10,822:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:10,830:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:10,832:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:10,833:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:10,837:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:10,841:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:10,842:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:10,842:DEBUG:
    Ignoring line no. 24: 35
    


.. parsed-literal::

    The slowest run took 9.25 times longer than the fastest. This could mean that an intermediate result is being cached.
    26.3 ms ± 20.3 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)


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

    2018-08-28 14:20:12,246:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:12,856:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:12,859:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:12,862:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:12,865:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:12,867:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:12,960:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:12,963:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:12,964:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:12,964:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:12,965:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:12,968:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:13,018:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:13,022:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:13,024:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:13,025:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:13,026:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:13,027:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:13,091:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:13,096:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:13,097:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:13,098:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:13,098:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:13,098:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:13,143:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:13,146:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:13,147:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:13,147:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:13,148:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:13,148:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:13,197:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:13,201:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:13,202:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:13,202:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:13,203:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:13,203:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:14,322:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:14,326:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:14,327:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:14,327:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:14,328:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:14,328:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:14,378:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:14,382:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:14,385:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:14,386:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:14,388:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:14,390:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    The slowest run took 21.48 times longer than the fastest. This could mean that an intermediate result is being cached.
    213 ms ± 364 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


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

    2018-08-28 14:20:14,478:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:14,482:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:14,482:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:14,483:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:14,483:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:14,484:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:14,541:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:14,545:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:14,546:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:14,546:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:14,547:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:14,547:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:14,604:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:14,611:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:14,612:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:14,613:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:14,613:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:14,613:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:14,670:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:14,673:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:14,674:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:14,675:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:14,676:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:14,676:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:14,729:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:14,734:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:14,734:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:14,735:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:14,735:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:14,736:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:14,791:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:14,795:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:14,796:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:14,796:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:14,797:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:14,797:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:14,851:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:14,858:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:14,859:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:14,859:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:14,859:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:14,860:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:14,912:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:14,916:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:14,916:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:14,917:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:14,917:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:14,918:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:14,969:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:14,972:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:14,973:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:14,973:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:14,973:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:14,974:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,029:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,032:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,033:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,033:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,034:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,034:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,087:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,091:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,091:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,091:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,092:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,092:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,144:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,147:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,148:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,148:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,149:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,149:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,205:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,206:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,207:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,207:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,208:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,263:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,268:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,268:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,269:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,269:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,270:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,339:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,344:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,346:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,347:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,348:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,417:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,422:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,422:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,423:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,423:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,424:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,474:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,478:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,478:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,479:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,479:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,480:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,533:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,538:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,540:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,541:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,543:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,544:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,613:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,618:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,619:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,619:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,620:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,620:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,681:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,686:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,688:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,691:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,693:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,695:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,767:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,771:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,771:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,772:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,773:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,773:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,826:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,831:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,832:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,832:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,832:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,884:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,888:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,888:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,889:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,889:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,889:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:15,941:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:15,946:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:15,948:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:15,950:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:15,953:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:15,959:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,032:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,037:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,038:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,038:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,039:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,039:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,094:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,100:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,100:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,101:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,101:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,102:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,155:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,159:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,159:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,160:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,160:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,162:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,217:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,221:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,222:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,223:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,223:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,224:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,277:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,281:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,282:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,282:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,283:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,283:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,353:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,357:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,358:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,358:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,359:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,359:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,418:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,422:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,425:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,427:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,429:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,431:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,510:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,515:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,515:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,516:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,516:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,517:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,570:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,576:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,576:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,577:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,577:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,578:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,633:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,637:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,640:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,641:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,643:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,644:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,704:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,707:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,708:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,708:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,708:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,709:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,769:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,773:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,773:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,773:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,774:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,774:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,827:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,832:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,832:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,832:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,833:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,887:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,892:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,894:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,895:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,897:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,898:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:16,959:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:16,963:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:16,964:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:16,964:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:16,964:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:16,965:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:17,018:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:17,021:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:17,022:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:17,022:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:17,023:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:17,023:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:17,076:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:17,080:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:17,081:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:17,081:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:17,081:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:17,082:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:17,134:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:17,138:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:17,138:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:17,139:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:17,139:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:17,139:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:17,191:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:17,195:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:17,197:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:17,198:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:17,200:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:17,201:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:17,263:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:17,267:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:17,269:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:17,270:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:17,271:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:17,272:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:17,332:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:17,336:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:17,337:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:17,338:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:17,338:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:17,338:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:17,407:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:17,411:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:17,412:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:17,412:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:17,412:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:17,413:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:17,464:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:17,468:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:17,468:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:17,469:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:17,469:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:17,470:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:17,524:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:17,527:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:17,528:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:17,528:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:17,529:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:17,529:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:17,589:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:17,592:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:17,593:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:17,593:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:17,594:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:17,594:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:17,646:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:17,650:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:17,652:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:17,653:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:17,655:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:17,656:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:17,714:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:17,722:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:17,723:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:17,723:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:17,724:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:17,724:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:18,291:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:18,308:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:18,309:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:18,309:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:18,310:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:18,310:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:18,368:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:18,373:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:18,375:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:18,376:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:18,377:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:18,378:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:18,458:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:18,462:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:18,462:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:18,463:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:18,463:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:18,464:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:18,518:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:18,522:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:18,523:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:18,523:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:18,524:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:18,524:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:18,577:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:18,580:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:18,581:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:18,581:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:18,582:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:18,582:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:18,635:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:18,641:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:18,642:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:18,642:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:18,643:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:18,643:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:18,714:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:18,718:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:18,718:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:18,719:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:18,719:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:18,719:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:18,782:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:18,788:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:18,789:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:18,789:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:18,790:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:18,790:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:18,847:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:18,852:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:18,852:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:18,852:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:18,853:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:18,853:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:18,905:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:18,909:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:18,909:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:18,910:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:18,910:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:18,911:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:18,965:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:18,969:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:18,969:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:18,970:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:18,970:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:18,971:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,024:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,028:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,028:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,029:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,029:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,029:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,083:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,087:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,089:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,091:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,092:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,092:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,151:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,156:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,156:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,156:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,157:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,157:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,210:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,214:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,215:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,215:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,216:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,216:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,270:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,275:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,276:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,276:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,277:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,277:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,341:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,346:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,346:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,347:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,347:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,347:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,401:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,405:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,405:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,406:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,407:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,407:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,483:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,487:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,487:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,488:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,488:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,489:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,546:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,550:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,552:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,554:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,555:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,556:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,617:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,622:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,624:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,625:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,627:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,628:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,686:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,690:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,692:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,695:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,696:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,697:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,757:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,761:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,762:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,763:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,763:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,764:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,814:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,818:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,818:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,819:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,820:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,820:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,872:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,876:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,876:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,877:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,877:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,878:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,931:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,935:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,935:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,936:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,936:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,936:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:19,989:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:19,992:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:19,993:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:19,993:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:19,994:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:19,994:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:20,045:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:20,049:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:20,050:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:20,050:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:20,050:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:20,051:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:20,102:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:20,106:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:20,107:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:20,107:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:20,108:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:20,108:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-28 14:20:20,160:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-28 14:20:20,165:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-28 14:20:20,166:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-28 14:20:20,166:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-28 14:20:20,167:DEBUG:
    REACHED DATA BLOCK
    2018-08-28 14:20:20,167:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    72.5 ms ± 17.8 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

