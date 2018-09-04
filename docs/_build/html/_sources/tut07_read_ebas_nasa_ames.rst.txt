
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

    2018-09-04 14:18:09,885:INFO:
    Reading aliases ini file: /home/jonasg/github/pyaerocom/pyaerocom/data/aliases.ini
    2018-09-04 14:18:10,646:WARNING:
    geopy library is not available. Aeolus data read not enabled
    2018-09-04 14:18:10,686:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,690:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,691:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,692:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,692:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:10,693:DEBUG:
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
                  <pyaerocom.io.ebas_nasa_ames.EbasFlagCol at 0x7fb24032c588>)])



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

    2018-09-04 14:18:10,889:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,894:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,896:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,898:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,904:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,908:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,908:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,909:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,911:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,915:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,915:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,916:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,918:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,921:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,922:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,923:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,924:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,927:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,928:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,929:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,930:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,934:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,934:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,935:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,936:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,940:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,940:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,941:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,942:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,946:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,947:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,947:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,949:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,953:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,954:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,954:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,956:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,959:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,960:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,961:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,962:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,967:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,967:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,968:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,969:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,973:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,974:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,974:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,976:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,979:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,980:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,981:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,982:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,986:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,987:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,987:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,989:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:10,993:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:10,994:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:10,994:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:10,996:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,000:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,001:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,001:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,003:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,006:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,007:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,007:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,009:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,012:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,013:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,014:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,015:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,020:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,021:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,021:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,023:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,026:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,027:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,028:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,029:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,036:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,037:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,037:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,039:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,042:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,043:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,044:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,045:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,049:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,050:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,050:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,052:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,055:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,056:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,057:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,059:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,062:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,063:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,064:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,065:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,068:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,069:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,070:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,072:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,075:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,075:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,076:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,078:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,081:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,082:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,082:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,084:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,087:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,088:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,089:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,090:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,094:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,096:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,098:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,101:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,106:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,107:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,109:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,112:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,116:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,117:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,119:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,123:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,127:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,128:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,129:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,131:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,136:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,136:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,137:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,139:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,142:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,143:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,144:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,146:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,149:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,151:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,153:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,156:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,161:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,163:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,164:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,168:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,172:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,173:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,174:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,175:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,179:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,180:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,181:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,182:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,186:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,187:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,187:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,189:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,192:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,193:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,193:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,195:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,198:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,198:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,199:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,204:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,204:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,205:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,206:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,210:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,211:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,211:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,213:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,216:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,217:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,217:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,219:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,222:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,223:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,223:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,225:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,228:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,229:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,229:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,231:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,235:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,236:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,236:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,238:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,241:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,242:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,242:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,244:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,247:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,248:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,248:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,250:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,254:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,254:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,255:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,256:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,259:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,260:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,261:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,263:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,266:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,267:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,267:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,269:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,272:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,273:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,273:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,275:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,278:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,278:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,279:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,280:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,283:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,284:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,284:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,286:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,290:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,291:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,291:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,292:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,296:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,297:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,297:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,299:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,303:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,303:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,304:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,305:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,309:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,309:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,310:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,311:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,314:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,315:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,315:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,317:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,320:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,321:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,321:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,323:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,326:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,327:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,327:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,328:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,331:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,332:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,332:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,334:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,337:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,337:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,337:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,339:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,342:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,343:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,343:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,345:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,349:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,351:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,353:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,356:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,360:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,362:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,364:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,369:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,374:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,376:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,378:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,383:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,387:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,389:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,389:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,392:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,395:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,396:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,397:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,399:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,402:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,403:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,403:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,405:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,407:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,408:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,408:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,410:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,413:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,413:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,413:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,415:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,418:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,419:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,419:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,421:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,424:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,425:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,425:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,427:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,431:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,431:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,432:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,437:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,437:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,438:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,439:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,442:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,443:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,443:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,445:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,449:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,450:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,450:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,452:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,456:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,456:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,457:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,459:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,462:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,463:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,463:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,464:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,468:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,468:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,469:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,470:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,473:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,474:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,475:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,476:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,479:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,480:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,480:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,482:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,484:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,485:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,485:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,487:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,490:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,491:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,491:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,492:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,495:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,496:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,496:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,498:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,501:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,502:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,502:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,504:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,507:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,507:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,508:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,509:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,512:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,513:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,513:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,514:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,518:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,518:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,519:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,520:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,523:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,524:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,524:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,526:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,529:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,530:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,530:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,531:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,535:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,535:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,536:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,537:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,540:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,541:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,541:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,543:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,546:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,547:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,547:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,548:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,552:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,553:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,553:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,555:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,559:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,559:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,560:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,561:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,564:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,565:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,565:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,567:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,571:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,571:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,571:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,573:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,576:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,576:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,577:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,578:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,582:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,582:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,582:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,584:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,588:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,589:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,589:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,591:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,594:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,595:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,596:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,600:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,600:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,601:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,602:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,605:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,605:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,606:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,607:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,611:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,611:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,612:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,613:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,616:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,617:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,617:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,619:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,622:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,622:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,622:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,624:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,627:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,627:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,628:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,629:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,632:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,632:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,633:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,634:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,637:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,638:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,638:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,640:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,643:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,644:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,644:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,645:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,649:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,651:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,653:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,656:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,661:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,663:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,664:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,669:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,674:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,676:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,678:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,694:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,699:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,701:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,703:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,707:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,712:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,714:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,715:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,718:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,723:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,724:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,724:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,726:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,730:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,731:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,731:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,733:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,736:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,737:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,737:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,739:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,742:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,743:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,743:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,745:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,748:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,749:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,749:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,751:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,754:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,755:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,755:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,757:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,761:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,761:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,762:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,763:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,767:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,767:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,768:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,769:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,773:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,774:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,776:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,779:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,784:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,785:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,786:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,788:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,792:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,793:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,793:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,795:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,799:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,799:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,800:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,801:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,804:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,805:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,805:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,807:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,810:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,811:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,811:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,813:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,817:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,817:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,818:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,819:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,822:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,823:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,823:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,825:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,828:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,829:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,831:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,834:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,839:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,840:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,841:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,843:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,847:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,848:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,848:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,850:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,853:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,854:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,854:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,856:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,859:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,860:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,860:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,861:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,865:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,865:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,866:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,867:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,870:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,871:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,871:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,873:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,876:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,877:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,877:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,879:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,882:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,883:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,883:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,885:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,888:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,888:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,889:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,890:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,894:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,895:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,897:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,900:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,906:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,907:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,908:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,915:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,919:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,919:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,920:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,922:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,926:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,927:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,927:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,929:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,933:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,934:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,935:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,937:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,940:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,941:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,941:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,943:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,946:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,946:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,947:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,948:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,952:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,952:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,953:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,954:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,958:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,958:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,958:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,960:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,963:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,964:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,964:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,966:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,969:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,969:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,969:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,971:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,974:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,975:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,975:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,977:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,981:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,982:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,982:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,984:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,987:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,987:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,988:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,990:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,993:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:11,994:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:11,994:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:11,996:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:11,999:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,000:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,000:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,001:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,005:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,006:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,006:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,008:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,012:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,013:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,013:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,014:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,018:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,019:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,019:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,021:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,025:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,026:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,029:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,032:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,037:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,039:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,040:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,045:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,050:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,052:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,053:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,057:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,063:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,064:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,066:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,070:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,074:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,075:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,076:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,079:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,082:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,083:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,084:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,086:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,089:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,090:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,091:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,092:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,096:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,096:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,097:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,099:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,102:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,103:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,103:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,105:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,108:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,109:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,110:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,111:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,114:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,115:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,116:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,117:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,121:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,122:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,122:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,124:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,128:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,128:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,129:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,131:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,134:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,135:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,135:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,137:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,142:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,142:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,143:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,145:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,149:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,151:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,153:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,157:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,162:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,163:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,165:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,169:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,174:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,175:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,177:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,179:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,183:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,184:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,185:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,187:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,190:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,191:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,192:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,194:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,198:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,199:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,199:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,205:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,205:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,206:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,208:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,211:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,212:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,213:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,216:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,219:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,220:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,220:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,223:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,226:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,227:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,228:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,230:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,234:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,234:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,235:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,237:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,241:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,242:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,242:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,244:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,250:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,251:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,252:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,254:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,258:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,259:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,259:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,261:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,265:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,265:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,266:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,268:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,272:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,273:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,274:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,275:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,279:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,280:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,280:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,282:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,286:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,286:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,287:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,289:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,293:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,294:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,294:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,297:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,300:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,301:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,302:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,304:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,307:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,308:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,309:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,311:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,315:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,315:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,316:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,318:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,321:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,322:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,323:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,325:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,328:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,329:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,330:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,331:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,335:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,336:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,336:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,338:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,341:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,342:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,343:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,344:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,348:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,348:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,349:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,351:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,354:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,355:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,355:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,357:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,361:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,362:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,362:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,364:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,367:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,368:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,368:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,370:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,373:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,374:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,374:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,376:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,379:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,380:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,381:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,383:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,386:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,387:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,388:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,390:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,394:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,394:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,395:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,397:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,400:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,401:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,401:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,403:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,406:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,407:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,407:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,409:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,412:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,413:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,414:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,416:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,420:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,420:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,421:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,423:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,426:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,427:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,427:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,429:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,432:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,433:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,434:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,436:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,440:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,441:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,443:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,447:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,452:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,455:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,457:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,461:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,465:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,466:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,468:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,470:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,474:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,476:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,476:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,479:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,484:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,485:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,486:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,488:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,494:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,495:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,497:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,501:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,502:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,503:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,506:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,510:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,511:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,512:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,514:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,519:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,520:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,521:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,523:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,527:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,528:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,529:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,532:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,536:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,537:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,538:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,541:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,544:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,546:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,547:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,549:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,554:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,556:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,557:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,562:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,566:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,567:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,568:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,571:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,575:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,576:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,577:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,579:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,583:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,583:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,584:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,586:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,590:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,591:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,591:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,593:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,596:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,597:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,597:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,599:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,602:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,603:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,604:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,605:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,608:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,609:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,610:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,611:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,615:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,615:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,616:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,617:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,621:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,621:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,622:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,624:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,627:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,627:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,628:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,629:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,633:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,634:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,636:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,640:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,645:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,647:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,649:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,653:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,658:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,659:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,661:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,664:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,670:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,671:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,673:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,676:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,681:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,683:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,684:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,687:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,695:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,697:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,699:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,707:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,713:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,714:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,716:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,720:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,724:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,725:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,727:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,729:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,732:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,733:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,733:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,735:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,738:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,739:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,739:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,741:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,745:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,746:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,746:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,748:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,752:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,752:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,753:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,754:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,757:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,758:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,758:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,760:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,763:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,763:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,764:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,765:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,768:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,768:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,769:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,770:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,773:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,774:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,774:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,776:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,780:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,780:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,781:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,782:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,785:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,786:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,786:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,788:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,793:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,794:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,794:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,795:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,799:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,800:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,800:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,801:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,804:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,805:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,805:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,807:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,810:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,811:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,811:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,812:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,815:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,816:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,816:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,817:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,820:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,821:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,821:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,823:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,826:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,827:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,827:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,829:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,832:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,833:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,833:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,835:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,838:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,838:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,838:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,840:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,843:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,844:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,844:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,845:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,849:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,849:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,850:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,851:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,854:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,855:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,855:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,857:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,860:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,860:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,861:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,863:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,866:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,868:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,871:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,872:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,873:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,874:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,877:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,877:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,877:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,879:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,882:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,883:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,883:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,884:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,887:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,888:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,888:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,890:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,894:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,895:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,895:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,897:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,900:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,901:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,901:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,903:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,906:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,907:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,907:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,909:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,912:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,912:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,913:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,914:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,918:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,918:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,919:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,925:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,928:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,928:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,929:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,931:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,934:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,935:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,936:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,938:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,941:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,942:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,942:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,944:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,947:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,948:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,948:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,950:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,953:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,954:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,954:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,956:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,960:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,960:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,961:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,963:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,966:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,966:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,967:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,968:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,972:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,972:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,973:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,975:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,978:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,979:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,979:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,981:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,984:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,985:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,986:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,988:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,992:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,993:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,993:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:12,994:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:12,998:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:12,999:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:12,999:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,001:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,005:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,006:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,006:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,008:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,013:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,013:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,014:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,016:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,019:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,020:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,020:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,022:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,025:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,026:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,026:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,028:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,031:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,032:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,032:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,034:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,037:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,037:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,038:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,040:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,043:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,044:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,045:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,046:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,049:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,050:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,050:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,052:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,055:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,056:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,057:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,058:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,061:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,062:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,063:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,064:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,067:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,068:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,068:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,070:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,073:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,074:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,075:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,076:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,080:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,080:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,081:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,082:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,086:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,086:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,087:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,088:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,091:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,092:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,093:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,094:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,097:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,098:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,099:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,100:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,103:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,104:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,105:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,106:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,109:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,110:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,110:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,112:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,115:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,116:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,116:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,118:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,121:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,122:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,122:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,124:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,127:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,128:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,128:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,130:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,132:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,133:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,134:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,135:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,138:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,139:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,139:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,141:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,144:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,145:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,145:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,147:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,150:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,151:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,151:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,153:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,156:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,157:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,157:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,159:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,162:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,163:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,163:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,165:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,168:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,169:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,169:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,171:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,174:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,174:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,175:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,176:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,179:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,180:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,181:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,182:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,185:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,185:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,186:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,187:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,190:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,191:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,191:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,193:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,196:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,196:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,196:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,198:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,200:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,201:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,201:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,203:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,205:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,206:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,206:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,208:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,211:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,211:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,211:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,213:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,216:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,217:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,217:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,218:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,221:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,222:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,222:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,223:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,226:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,227:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,227:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,229:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,231:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,232:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,232:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,234:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,237:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,238:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,238:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,240:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,243:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,243:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,244:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,245:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,248:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,249:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,250:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,251:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,255:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,255:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,255:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,257:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,260:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,261:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,261:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,263:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,266:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,267:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,267:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,269:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,272:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,273:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,273:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,274:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,278:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,278:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,279:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,280:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,283:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,284:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,284:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,286:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,289:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,289:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,290:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,291:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,294:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,295:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,295:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,297:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,300:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,300:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,300:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,302:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,305:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,306:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,306:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,307:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,311:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,311:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,312:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,313:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,316:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,316:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,317:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,318:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,321:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,321:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,322:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,323:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,326:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,327:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,327:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,328:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,331:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,332:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,332:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,334:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,336:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,337:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,337:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,339:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,341:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,342:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,342:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,344:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,347:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,348:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,348:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,349:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,352:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,353:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,353:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,355:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,358:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,359:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,362:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,365:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,370:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,372:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,374:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,378:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,383:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,386:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,387:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,391:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,395:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,397:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,399:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,404:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,408:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,410:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,411:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,415:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,420:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,422:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,423:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,425:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,430:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,430:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,431:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,436:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,437:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,438:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,439:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,444:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,444:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,445:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,446:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,449:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,450:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,450:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,451:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,455:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,455:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,456:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,457:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,460:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,461:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,461:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,462:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,466:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,466:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,467:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,468:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,471:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,472:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,472:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,474:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,476:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,477:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,477:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,479:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,481:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,482:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,482:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,484:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,487:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,487:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,488:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,489:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,493:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,493:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,495:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,498:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,498:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,499:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,500:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,504:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,504:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,505:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,506:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,509:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,510:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,510:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,512:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,515:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,515:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,515:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,517:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,520:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,520:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,521:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,522:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,525:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,526:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,526:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,528:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,532:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,532:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,533:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,534:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,538:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,539:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,539:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,540:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,544:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,544:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,545:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,546:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,549:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,550:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,550:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,552:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,556:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,557:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,557:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,558:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,562:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,562:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,562:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,564:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,568:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,570:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,571:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,576:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,581:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,583:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,586:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,589:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,595:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,597:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,601:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,605:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,607:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,608:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,612:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,616:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,617:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,618:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,620:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,624:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,624:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,625:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,627:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,631:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,632:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,633:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,635:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,639:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,639:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,640:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,642:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,646:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,647:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,647:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,649:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,653:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,653:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,654:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,656:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,659:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,660:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,661:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,662:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,666:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,666:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,667:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,668:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,671:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,672:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,672:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,674:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,677:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,678:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,678:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,680:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,683:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,684:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,684:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,686:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,689:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,690:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,691:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,696:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,700:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,701:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,701:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,703:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,706:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,707:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,707:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,715:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,718:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,719:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,719:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,721:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,724:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,725:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,725:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,727:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,730:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,731:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,731:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,733:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,736:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,737:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,737:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,739:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,743:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,743:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,744:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,746:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,750:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,750:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,751:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,752:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,756:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,757:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,757:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,759:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,762:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,763:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,763:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,765:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,768:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,769:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,770:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,771:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,775:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,775:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,776:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,777:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,780:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,781:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,781:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,783:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,786:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,786:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,787:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,788:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,791:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,792:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,792:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,794:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,798:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,798:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,799:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,800:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,804:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,804:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,805:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,806:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,809:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,810:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,810:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,812:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,815:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,816:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,816:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,818:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,822:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,822:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,823:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,825:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,828:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,828:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,829:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,830:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,834:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,834:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,835:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,836:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,839:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,840:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,841:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,842:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,845:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,846:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,847:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,848:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,852:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,852:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,853:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,854:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,858:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,858:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,859:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,860:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,863:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,864:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,864:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,866:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,870:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,870:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,871:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,873:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,876:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,877:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,877:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,880:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,883:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,884:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,884:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,886:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,890:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,890:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,891:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,892:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,895:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,896:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,897:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,898:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,902:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,902:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,903:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,904:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,908:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,910:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,912:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,915:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,920:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,922:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,923:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,930:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,935:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,937:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,938:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,942:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,946:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,947:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,948:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,950:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,953:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,954:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,955:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,956:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,959:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,960:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,960:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,962:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,965:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,966:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,966:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,968:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,972:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,972:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,972:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,974:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,977:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,978:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,978:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,980:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,983:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,984:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,984:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,985:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,989:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,989:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,990:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,991:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,994:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:13,995:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:13,995:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:13,997:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:13,999:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,000:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,000:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,002:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,004:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,005:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,005:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,006:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,009:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,010:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,010:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,011:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,015:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,016:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,016:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,017:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,021:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,021:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,022:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,023:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,026:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,027:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,027:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,028:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,032:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,032:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,033:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,034:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,038:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,038:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,038:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,040:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,043:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,043:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,044:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,045:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,049:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,049:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,050:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,051:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,054:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,054:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,055:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,056:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,059:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,060:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,060:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,062:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,066:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,066:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,066:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,068:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,072:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,072:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,073:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,074:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,078:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,078:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,079:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,080:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,083:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,084:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,084:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,086:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,090:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,090:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,091:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,092:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,096:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,096:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,097:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,098:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,102:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,102:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,103:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,104:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,108:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,110:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,111:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,114:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,119:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,121:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,122:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,127:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,133:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,135:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,137:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,141:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,146:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,148:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,150:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,153:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,158:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,159:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,162:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,166:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,170:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,171:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,173:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,175:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,179:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,180:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,181:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,183:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,188:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,188:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,190:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,194:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,195:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,196:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,198:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,202:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,202:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,203:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,205:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,209:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,211:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,213:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,216:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,221:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,222:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,224:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,227:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,232:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,234:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,235:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,238:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,243:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,244:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,245:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,247:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,251:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,252:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,252:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,254:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,257:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,257:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,258:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,259:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,262:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,263:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,263:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,265:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,268:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,269:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,269:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,271:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,274:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,276:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,278:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,281:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,287:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,288:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,290:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,295:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,299:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,301:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,303:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,307:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,312:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,314:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,316:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,319:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,324:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,326:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,328:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,331:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,335:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,337:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,338:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,340:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,344:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,344:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,346:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,349:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,350:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,350:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,352:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,355:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,356:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,356:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,358:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,361:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,362:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,362:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,364:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,367:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,368:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,368:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,370:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,373:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,373:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,374:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,375:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,378:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,379:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,379:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,381:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,385:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,385:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,386:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,387:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,391:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,391:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,392:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,393:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,397:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,397:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,398:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,399:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,402:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,403:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,403:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,405:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,409:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,409:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,410:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,411:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,415:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,416:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,416:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,417:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,420:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,421:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,421:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,423:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,426:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,427:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,427:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,429:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,432:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,433:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,433:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,435:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,438:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,439:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,439:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,441:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,444:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,444:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,445:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,446:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,449:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,450:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,450:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,451:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,455:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,455:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,456:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,457:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,460:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,461:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,461:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,463:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,466:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,466:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,467:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,468:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,471:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,472:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,472:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,474:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,477:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,477:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,478:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,479:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,482:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,483:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,483:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,485:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,488:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,489:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,489:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,490:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,494:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,494:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,495:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,496:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,500:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,500:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,501:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,502:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,506:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,506:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,507:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,508:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,512:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,512:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,513:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,514:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,518:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,518:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,519:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,521:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,524:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,525:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,525:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,527:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,530:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,531:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,532:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,534:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,537:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,538:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,538:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,540:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,544:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,545:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,546:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,547:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,550:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,551:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,552:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,554:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,557:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,558:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,558:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,560:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,563:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,564:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,564:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,567:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,570:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,570:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,571:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,572:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,575:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,576:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,577:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,578:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,582:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,583:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,583:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,585:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,588:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,589:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,589:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,591:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,596:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,597:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,601:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,606:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,608:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,609:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,612:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,617:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,618:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,618:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,620:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,624:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,624:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,625:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,627:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,630:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,630:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,631:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,632:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,636:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,637:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,637:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,639:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,642:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,643:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,643:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,644:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,648:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,648:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,649:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,650:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,653:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,653:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,654:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,655:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,659:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,661:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,663:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,667:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,672:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,674:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,675:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,679:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,684:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,685:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,687:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,690:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,696:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,698:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,699:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,707:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,710:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,711:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,712:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,720:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,724:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,725:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,725:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,727:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,731:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,732:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,733:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,735:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,738:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,739:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,740:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,742:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,746:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,746:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,747:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,749:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,752:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,753:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,753:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,755:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,758:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,759:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,759:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,761:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,764:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,765:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,765:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,766:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,770:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,770:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,771:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,773:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,775:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,776:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,776:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,778:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,781:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,782:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,782:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,784:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,787:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,787:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,788:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,789:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,792:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,793:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,793:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,795:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,802:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,802:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,803:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,804:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,808:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,808:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,809:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,810:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,814:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,814:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,815:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,816:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,820:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,820:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,821:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,822:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,825:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,826:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,827:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,829:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,832:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,832:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,833:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,834:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,838:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,839:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,839:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,841:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,844:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,846:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,848:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,852:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,857:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,859:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,860:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,863:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,867:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,868:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,869:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,871:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,874:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,875:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,876:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,877:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,880:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,881:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,881:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,883:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,886:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,887:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,887:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,889:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,893:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,894:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,896:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,899:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,903:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,904:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,904:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,907:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,910:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,911:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,912:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,913:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,916:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,917:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,918:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,919:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,922:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,922:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,923:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,924:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,927:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,928:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,928:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,930:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,934:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,934:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,934:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,941:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,944:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,945:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,945:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,948:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,951:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,952:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,952:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,954:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,956:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,957:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,957:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,959:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,962:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,963:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,963:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,965:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,969:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,969:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,969:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,971:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,974:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,975:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,975:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,977:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,980:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,980:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,981:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,982:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,986:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,986:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,986:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,988:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,991:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,992:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,992:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:14,994:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:14,998:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:14,998:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:14,999:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,000:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,004:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,004:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,005:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,006:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,010:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,010:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,011:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,012:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,015:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,016:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,016:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,017:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,021:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,021:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,022:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,023:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,027:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,028:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,028:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,029:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,032:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,033:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,033:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,035:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,038:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,038:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,039:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,041:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,044:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,044:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,045:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,046:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,049:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,050:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,050:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,051:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,054:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,056:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,056:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,058:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,062:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,062:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,063:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,064:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,068:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,069:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,069:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,070:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,074:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,075:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,075:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,076:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,079:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,080:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,080:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,082:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,085:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,086:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,086:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,088:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,092:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,092:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,093:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,094:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,098:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,099:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,099:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,101:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,104:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,105:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,105:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,107:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,111:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,111:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,112:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,113:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,117:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,117:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,118:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,119:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,122:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,123:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,124:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,125:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,130:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,130:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,131:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,132:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,135:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,136:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,136:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,138:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,142:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,143:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,143:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,145:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,148:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,149:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,149:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,151:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,155:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,157:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,159:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,164:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,173:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,175:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,178:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,180:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,184:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,185:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,185:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,187:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,191:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,191:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,193:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,194:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,198:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,198:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,199:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,200:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,203:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,204:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,204:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,206:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,210:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,211:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,211:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,213:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,216:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,217:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,217:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,219:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,223:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,224:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,224:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,226:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,230:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,230:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,231:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,232:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,235:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,236:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,236:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,238:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,241:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,241:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,242:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,244:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,248:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,248:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,249:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,250:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,254:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,254:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,255:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,256:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,260:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,260:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,261:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,262:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,265:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,266:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,266:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,268:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,271:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,272:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,272:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,274:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,277:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,278:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,279:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,280:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,283:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,284:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,285:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,286:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,289:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,290:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,291:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,292:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,296:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,297:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,297:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,299:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,302:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,303:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,303:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,305:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,308:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,309:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,309:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,310:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,314:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,314:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,314:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,316:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,319:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,320:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,320:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,322:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,328:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,329:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,332:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,335:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,338:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,339:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,340:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,342:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,346:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,347:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,348:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,350:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,354:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,355:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,356:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,358:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,362:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,362:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,363:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,365:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,370:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,370:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,371:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,373:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,377:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,378:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,378:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,379:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,383:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,384:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,384:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,386:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,390:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,391:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,391:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,392:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,396:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,397:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,397:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,399:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,403:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,404:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,405:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,406:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,409:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,410:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,410:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,412:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,415:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,416:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,417:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,419:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,423:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,424:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,425:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,426:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,429:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,430:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,431:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,437:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,438:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,438:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,440:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,443:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,444:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,445:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,446:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,450:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,450:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,451:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,453:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,456:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,457:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,457:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,458:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,462:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,462:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,463:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,464:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,468:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,469:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,469:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,471:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,474:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,475:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,475:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,477:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,480:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,481:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,482:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,483:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,487:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,487:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,488:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,489:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,493:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,493:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,495:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,498:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,499:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,499:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,501:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,504:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,504:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,505:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,506:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,509:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,510:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,510:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,512:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,515:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,516:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,516:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,518:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,522:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,522:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,523:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,525:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,529:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,529:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,530:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,531:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,535:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,535:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,536:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,538:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,541:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,542:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,542:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,544:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,548:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,549:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,549:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,551:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,554:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,555:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,555:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,557:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,560:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,561:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,561:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,562:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,565:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,566:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,566:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,568:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,571:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,572:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,572:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,573:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,577:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,577:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,578:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,580:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,583:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,584:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,584:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,586:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,590:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,592:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,594:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,598:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,604:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,606:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,608:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,613:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,618:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,620:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,623:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,627:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,633:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,634:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,635:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,638:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,641:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,642:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,643:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,645:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,648:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,649:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,649:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,651:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,654:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,654:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,655:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,656:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,660:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,660:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,660:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,662:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,665:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,666:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,667:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,669:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,673:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,673:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,674:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,675:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,678:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,679:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,680:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,681:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,685:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,685:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,686:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,688:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,692:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,692:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,693:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,694:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,697:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,698:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,698:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,701:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,704:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,704:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,705:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,706:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,710:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,711:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,711:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,717:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,721:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,721:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,722:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,730:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,734:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,736:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,738:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,742:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,749:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,751:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,752:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,757:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,763:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,765:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,767:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,772:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,776:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,778:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,778:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,781:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,784:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,785:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,786:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,787:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,790:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,791:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,792:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,793:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,797:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,797:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,798:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,799:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,802:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,803:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,803:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,805:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,808:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,809:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,809:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,811:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,814:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,815:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,815:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,817:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,820:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,820:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,821:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,823:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,827:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,827:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,828:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,830:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,833:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,834:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,835:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,836:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,839:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,840:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,841:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,842:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,845:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,846:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,846:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,848:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,851:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,852:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,852:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,854:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,857:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,858:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,858:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,860:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,863:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,864:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,864:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,866:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,869:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,869:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,870:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,871:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,875:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,875:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,876:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,877:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,880:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,881:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,881:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,883:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,886:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,887:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,887:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,888:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,892:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,893:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,893:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,895:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,898:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,900:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,903:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,907:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,912:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,915:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,916:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,920:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,924:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,927:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,929:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,933:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,938:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,940:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,941:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,949:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,955:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,957:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,958:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,962:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,968:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,970:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,971:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,974:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,978:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,979:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,980:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,982:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,985:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,986:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,987:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,989:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,992:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,993:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,993:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:15,995:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:15,998:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:15,999:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:15,999:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,001:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,004:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,004:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,005:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,007:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,010:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,011:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,011:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,013:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,016:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,017:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,017:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,019:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,022:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,022:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,023:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,025:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,028:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,029:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,029:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,031:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,035:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,035:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,036:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,038:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,041:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,042:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,043:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,044:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,047:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,048:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,048:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,050:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,053:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,054:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,054:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,056:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,059:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,060:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,060:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,062:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,065:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,066:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,066:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,068:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,071:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,072:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,072:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,074:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,077:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,077:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,078:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,079:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,082:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,083:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,083:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,085:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,088:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,089:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,089:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,091:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,095:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,095:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,096:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,097:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,101:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,102:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,102:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,103:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,107:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,107:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,108:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,110:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,113:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,113:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,114:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,115:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,118:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,119:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,120:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,123:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,126:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,127:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,127:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,128:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,131:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,132:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,132:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,134:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,138:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,138:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,139:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,140:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,144:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,145:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,145:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,147:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,150:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,151:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,152:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,153:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,156:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,157:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,157:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,159:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,162:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,162:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,163:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,165:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,168:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,168:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,169:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,170:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,174:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,174:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,175:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,176:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,180:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,182:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,184:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,188:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,195:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,197:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,199:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,204:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,208:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,210:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,213:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,217:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,222:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,223:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,224:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,227:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,231:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,231:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,232:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,234:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,239:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,240:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,241:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,243:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,247:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,248:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,248:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,250:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,255:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,257:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,259:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,262:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,268:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,269:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,270:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,272:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,276:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,277:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,278:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,279:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,283:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,284:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,285:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,286:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,290:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,290:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,291:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,292:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,295:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,296:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,296:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,297:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,300:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,301:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,301:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,303:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,306:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,306:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,307:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,308:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,311:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,312:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,312:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,313:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,317:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,317:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,317:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,319:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,322:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,323:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,323:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,325:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,328:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,328:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,329:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,330:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,333:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,333:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,334:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,335:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,339:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,339:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,340:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,341:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,344:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,344:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,345:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,346:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,349:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,350:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,350:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,352:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,355:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,356:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,356:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,358:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,361:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,361:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,362:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,363:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,367:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,367:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,367:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,369:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,372:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,373:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,373:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,375:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,378:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,378:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,379:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,380:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,384:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,385:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,385:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,386:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,390:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,390:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,390:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,392:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,395:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,396:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,396:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,398:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,401:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,402:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,402:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,404:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,407:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,408:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,408:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,410:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,413:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,413:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,414:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,415:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,419:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,419:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,420:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,421:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,424:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,425:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,425:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,427:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,430:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,431:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,431:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,436:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,437:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,437:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,439:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,442:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,443:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,443:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,445:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,448:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,449:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,449:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,451:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,455:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,455:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,455:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,457:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,460:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,460:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,461:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,463:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,466:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,467:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,467:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,468:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,471:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,472:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,472:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,474:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,477:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,477:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,478:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,479:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,482:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,483:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,483:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,484:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,487:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,488:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,488:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,489:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,493:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,493:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,495:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,498:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,499:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,499:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,501:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,504:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,505:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,505:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,506:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,509:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,510:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,510:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,512:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,515:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,515:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,516:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:16,517:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:16,521:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:16,521:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:16,521:DEBUG:
    Ignoring line no. 24: 35
    


.. parsed-literal::

    6.99 ms ± 315 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


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

    2018-09-04 14:18:17,859:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:17,864:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:17,866:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:17,866:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:17,868:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:17,868:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:17,930:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:17,934:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:17,935:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:17,935:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:17,936:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:17,936:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:17,979:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:17,983:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:17,984:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:17,984:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:17,985:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:17,985:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,035:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,040:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,041:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,043:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,045:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,046:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,094:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,099:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,099:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,099:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,100:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,100:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,144:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,148:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,149:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,149:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,150:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,150:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,195:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,200:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,201:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,201:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,202:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,202:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,245:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,248:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,249:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,249:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,250:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,250:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,294:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,298:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,299:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,299:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,300:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,300:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,343:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,347:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,347:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,348:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,348:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,349:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,391:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,395:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,396:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,397:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,397:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,398:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,440:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,444:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,446:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,448:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,449:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,450:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,508:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,512:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,513:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,513:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,514:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,514:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,558:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,562:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,563:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,563:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,563:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,564:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,608:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,612:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,612:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,613:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,613:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,613:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,657:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,662:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,663:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,663:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,664:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,664:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,709:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,714:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,714:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,715:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,715:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,716:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,759:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,763:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,764:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,764:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,764:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,765:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,809:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,813:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,813:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,814:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,814:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,814:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,877:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,883:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,883:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,883:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,884:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,884:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,929:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,933:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,935:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,936:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,938:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:18,939:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:18,990:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:18,995:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:18,996:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:18,998:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:18,999:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,000:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,051:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,056:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,058:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,059:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,061:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,063:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,123:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,127:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,127:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,128:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,128:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,130:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,175:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,179:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,179:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,179:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,180:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,180:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,226:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,230:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,230:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,231:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,231:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,232:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,276:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,279:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,279:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,280:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,280:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,281:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,323:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,327:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,327:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,328:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,328:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,328:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,372:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,375:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,376:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,376:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,377:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,377:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,423:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,427:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,427:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,428:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,429:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,429:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,472:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,476:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,477:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,477:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,478:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,478:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,521:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,525:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,526:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,528:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,529:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,530:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,580:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,584:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,585:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,585:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,586:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,586:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,630:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,635:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,636:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,638:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,639:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,640:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,689:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,694:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,694:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,694:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,695:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,695:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,739:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,743:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,744:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,744:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,745:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,745:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,788:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,792:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,792:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,793:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,793:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,794:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,838:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,842:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,842:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,843:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,843:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,844:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,907:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,911:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,912:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,912:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,912:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,914:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:19,958:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:19,962:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:19,963:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:19,963:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:19,964:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:19,964:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,009:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,014:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,015:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,015:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,015:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,016:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,060:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,065:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,065:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,065:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,066:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,067:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,109:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,113:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,113:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,114:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,114:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,114:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,158:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,162:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,163:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,164:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,164:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,165:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,208:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,212:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,212:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,213:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,213:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,214:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,260:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,264:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,266:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,267:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,269:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,270:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,320:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,325:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,325:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,326:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,326:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,327:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,370:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,375:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,376:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,376:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,377:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,377:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,420:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,425:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,425:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,426:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,426:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,427:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,470:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,474:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,474:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,475:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,475:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,476:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,521:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,525:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,527:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,528:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,530:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,531:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,582:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,586:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,586:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,587:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,587:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,588:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,632:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,635:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,636:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,637:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,637:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,638:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,680:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,685:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,686:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,688:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,689:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,690:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,745:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,750:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,750:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,750:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,751:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,751:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,794:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,799:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,799:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,799:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,800:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,800:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,844:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,848:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,848:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,848:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,849:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,849:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,898:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,902:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,902:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,903:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,903:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,904:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:20,959:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:20,963:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:20,965:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:20,967:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:20,969:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:20,971:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,039:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,044:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,044:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,045:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,045:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,046:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,088:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,092:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,093:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,093:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,093:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,094:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,140:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,144:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,145:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,146:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,146:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,146:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,189:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,194:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,194:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,194:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,195:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,195:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,239:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,243:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,244:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,244:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,245:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,245:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,288:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,292:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,292:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,293:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,293:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,293:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,337:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,341:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,342:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,342:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,343:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,344:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,387:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,391:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,392:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,392:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,393:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,393:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,436:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,439:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,440:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,440:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,441:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,441:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,483:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,486:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,487:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,487:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,488:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,488:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,533:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,536:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,537:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,537:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,538:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,538:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,581:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,584:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,585:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,585:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,587:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,587:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,630:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,634:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,635:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,635:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,636:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,636:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,683:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,687:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,688:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,688:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,689:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,689:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,732:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,736:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,737:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,738:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,738:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,739:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,783:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,786:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,787:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,788:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,788:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,789:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,834:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,837:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,837:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,838:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,838:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,839:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,881:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,884:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,885:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,886:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,886:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,887:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,935:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,938:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,939:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,940:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,940:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,941:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:21,992:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:21,996:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:21,997:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:21,997:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:21,997:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:21,998:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:22,039:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:22,043:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:22,043:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:22,044:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:22,044:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:22,045:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:22,088:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:22,091:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:22,091:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:22,092:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:22,092:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:22,093:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    52.8 ms ± 2.23 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


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

    2018-09-04 14:18:22,341:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:22,357:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:22,359:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:22,360:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:22,362:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:22,363:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:22,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:22,441:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:22,441:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:22,442:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:22,442:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:22,443:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:22,495:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:22,500:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:22,500:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:22,501:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:22,501:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:22,502:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:22,555:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:22,559:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:22,560:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:22,560:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:22,560:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:22,561:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:22,620:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:22,624:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:22,625:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:22,625:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:22,626:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:22,626:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:22,679:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:22,683:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:22,683:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:22,684:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:22,684:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:22,685:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:22,740:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:22,744:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:22,745:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:22,745:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:22,746:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:22,746:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:22,800:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:22,803:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:22,804:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:22,804:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:22,805:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:22,805:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:22,856:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:22,860:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:22,861:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:22,861:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:22,862:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:22,862:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:22,916:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:22,921:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:22,922:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:22,922:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:22,923:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:22,923:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:22,983:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:22,987:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:22,987:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:22,988:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:22,989:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:22,989:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,056:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,060:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,061:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,061:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,061:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,062:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,116:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,119:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,120:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,120:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,121:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,121:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,173:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,177:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,178:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,178:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,179:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,179:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,231:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,235:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,235:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,236:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,236:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,237:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,292:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,296:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,297:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,297:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,298:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,298:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,350:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,354:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,354:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,355:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,355:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,356:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,409:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,413:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,413:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,414:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,415:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,415:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,470:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,474:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,474:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,475:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,475:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,475:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,529:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,532:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,533:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,534:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,534:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,535:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,597:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,600:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,601:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,601:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,602:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,602:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,662:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,666:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,667:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,667:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,667:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,668:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,731:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,734:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,735:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,735:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,736:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,736:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,795:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,799:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,800:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,800:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,801:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,802:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,895:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,900:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,900:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,901:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,901:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:23,977:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:23,981:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:23,981:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:23,982:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:23,982:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:23,982:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,039:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,042:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,043:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,043:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,044:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,044:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,119:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,124:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,125:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,125:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,125:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,126:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,178:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,182:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,183:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,183:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,183:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,184:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,235:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,239:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,240:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,240:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,241:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,241:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,292:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,296:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,297:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,297:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,298:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,298:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,351:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,355:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,355:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,356:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,356:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,356:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,408:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,411:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,412:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,412:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,413:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,413:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,465:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,469:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,471:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,472:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,473:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,474:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,532:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,535:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,536:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,537:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,537:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,537:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,591:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,595:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,595:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,596:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,597:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,649:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,653:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,654:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,654:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,655:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,655:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,707:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,711:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,711:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,712:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,712:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,713:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,767:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,770:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,771:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,771:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,772:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,772:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,830:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,834:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,834:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,835:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,835:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,836:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,889:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,892:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,893:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,893:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,893:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,894:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:24,945:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:24,948:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:24,949:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:24,949:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:24,950:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:24,950:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,002:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,005:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,006:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,006:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,007:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,007:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,063:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,067:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,067:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,067:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,068:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,068:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,133:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,137:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,139:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,140:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,142:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,143:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,204:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,205:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,205:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,206:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,206:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,260:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,264:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,265:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,265:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,266:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,266:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,319:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,323:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,323:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,324:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,324:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,325:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,377:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,381:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,381:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,382:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,382:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,383:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,434:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,438:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,440:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,442:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,443:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,444:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,503:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,507:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,507:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,507:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,508:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,508:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,562:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,566:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,566:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,567:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,567:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,568:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,620:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,625:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,626:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,627:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,628:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,629:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,693:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,696:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,697:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,697:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,697:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,698:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,750:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,755:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,755:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,756:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,757:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,757:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,809:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,812:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,813:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,813:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,814:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,814:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,866:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,870:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,870:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,871:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,871:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,872:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,924:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,928:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,929:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,931:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:25,932:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:25,933:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:25,994:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:25,998:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:25,999:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:25,999:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,000:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,000:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,052:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,056:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,057:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,058:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,059:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,060:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,115:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,120:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,120:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,121:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,121:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,122:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,190:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,195:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,195:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,196:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,196:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,197:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,252:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,255:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,256:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,256:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,257:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,257:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,309:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,312:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,313:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,313:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,314:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,314:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,367:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,370:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,371:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,371:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,372:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,372:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,424:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,428:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,429:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,429:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,431:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,431:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,484:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,488:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,489:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,489:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,490:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,490:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,544:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,548:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,548:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,549:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,549:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,550:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,601:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,605:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,606:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,606:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,606:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,607:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,660:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,664:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,665:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,665:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,666:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,666:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,719:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,722:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,723:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,723:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,723:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,724:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,780:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,784:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,785:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,786:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,786:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,786:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,844:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,849:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,851:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,852:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,853:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,855:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,914:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,917:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,918:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,919:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,919:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,919:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:26,973:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:26,977:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:26,978:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:26,978:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:26,979:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:26,979:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:27,031:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:27,034:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:27,035:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:27,035:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:27,036:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:27,036:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:27,090:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:27,094:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:27,095:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:27,095:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:27,096:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:27,096:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:27,155:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:27,160:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:27,160:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:27,161:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:27,162:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:27,162:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:27,227:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:27,231:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:27,232:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:27,232:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:27,233:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:27,233:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:27,285:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:27,289:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:27,291:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:27,292:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:27,293:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:27,295:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-04 14:18:27,364:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-04 14:18:27,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-04 14:18:27,604:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-04 14:18:27,607:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-04 14:18:27,610:DEBUG:
    REACHED DATA BLOCK
    2018-09-04 14:18:27,614:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    66.5 ms ± 10.7 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

