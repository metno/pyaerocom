
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

    2018-09-21 11:36:46,200:WARNING:
    basemap extension library is not installed (or cannot be imported. Some features will not be available


.. parsed-literal::

    Elapsed time init all variables: 0.026292085647583008 s


.. parsed-literal::

    2018-09-21 11:36:46,944:WARNING:
    geopy library is not available. Aeolus data read not enabled
    2018-09-21 11:36:47,100:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)


.. parsed-literal::

    Elapsed time init pyaerocom: 1.0720207691192627 s
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
                  <pyaerocom.io.ebas_nasa_ames.EbasFlagCol at 0x7f36700d9908>)])



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

    2018-09-21 11:36:47,324:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,330:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,335:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,340:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,345:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,350:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,355:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,359:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,364:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,369:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,373:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,378:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,382:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,388:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,393:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,397:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,402:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,407:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,412:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,417:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,422:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,427:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,433:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,438:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,446:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,454:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,462:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,471:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,479:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,488:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,497:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,506:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,514:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,522:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,529:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,537:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,544:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,551:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,559:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,566:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,574:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,580:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,587:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,608:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,614:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,621:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,628:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,638:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,646:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,652:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,659:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,666:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,673:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,680:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,687:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,694:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,701:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,708:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,715:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,722:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,729:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,738:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,746:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,753:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,761:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,770:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,777:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,786:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,795:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,802:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,810:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,818:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,826:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,833:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,843:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,851:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,859:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,868:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,876:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,883:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,891:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,898:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,906:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,914:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,921:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,927:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,935:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,942:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,950:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,974:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,982:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,989:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:47,996:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,002:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,010:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,017:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,024:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,030:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,037:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,045:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,052:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,059:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,065:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,072:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,079:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,086:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,093:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,099:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,107:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,116:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,123:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,132:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,139:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,146:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,153:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,159:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,166:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,173:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,180:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,186:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,193:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,199:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,205:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,215:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,223:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,230:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,239:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,247:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,255:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,262:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,269:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,276:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,283:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,290:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,297:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,304:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,312:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,319:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,325:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,337:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,351:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,358:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,365:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,372:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,380:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,387:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,395:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,402:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,410:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,418:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,425:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,432:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,440:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,447:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,455:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,463:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,470:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,478:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,484:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,494:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,501:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,509:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,517:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,525:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,533:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,540:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,547:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,554:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,562:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,570:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,578:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,586:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,608:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,615:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,622:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,631:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,640:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,647:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,654:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,661:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,668:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,674:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,682:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,688:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,695:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,702:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,709:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,715:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,722:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,729:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,736:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,742:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,749:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,755:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,762:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,768:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,776:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,783:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,790:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,798:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,805:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,811:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,818:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,825:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,832:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,840:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,847:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,854:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,861:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,868:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,874:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,881:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,888:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,895:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,902:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,909:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,916:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,923:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,929:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,936:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,945:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,952:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,958:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,969:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,982:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,989:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:48,995:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,003:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,009:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,017:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,024:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,031:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,037:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,044:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,052:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,061:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,069:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,078:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,086:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,094:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,102:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,111:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,120:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,129:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,135:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,141:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,147:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,157:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,166:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,175:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,182:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,192:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,198:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,203:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,208:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,217:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,225:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,233:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,241:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,249:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,255:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,263:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,270:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,277:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,285:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,293:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,301:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,310:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,317:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,324:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,331:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,337:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,348:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,354:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,360:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,366:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,373:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,379:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,387:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,394:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,400:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,406:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,412:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,418:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,425:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,431:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,437:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,445:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,451:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,458:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,464:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,470:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,477:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,484:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,490:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,497:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,503:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,510:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,516:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,524:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,531:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,538:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,544:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,551:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,557:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,564:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,570:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,577:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,583:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,589:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,596:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,603:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,609:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,616:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,622:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,630:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,637:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,643:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,649:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,654:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,660:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,666:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,672:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,678:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,684:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,689:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,694:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,700:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,706:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,713:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,721:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,727:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,735:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,741:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,749:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,756:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,764:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,771:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,779:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,786:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,794:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,801:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,810:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,818:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,826:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,833:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,840:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,847:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,854:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,861:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,869:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,875:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,884:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,893:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,900:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,907:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,914:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,920:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,926:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,933:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,939:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,945:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,952:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,958:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,965:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,976:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,989:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:49,996:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,002:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,010:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,017:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,024:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,034:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,042:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,050:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,057:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,064:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,073:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,080:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,087:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,095:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,102:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,108:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,113:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,119:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,125:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,133:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,140:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,146:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,152:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,156:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,162:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,169:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,175:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,180:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,185:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,190:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,195:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,205:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,213:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,219:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,224:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,228:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,234:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,240:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,248:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,253:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,259:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,264:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,270:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,276:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,281:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,286:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,291:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,299:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,305:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,310:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,315:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,320:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,325:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,330:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,335:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,355:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,363:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,371:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,381:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,390:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,398:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,403:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,408:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,413:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,421:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,428:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,434:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,441:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,448:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,457:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,467:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,477:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,485:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,499:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,506:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,512:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,518:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,524:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,530:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,535:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,541:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,549:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,556:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,564:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,571:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,578:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,586:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,608:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,614:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,621:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,628:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,635:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,641:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,645:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,650:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,655:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,659:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,664:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,669:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,673:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,681:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,689:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,697:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,704:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,711:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,718:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,725:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,732:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,739:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,746:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,754:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,763:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,769:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,775:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,780:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,784:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,790:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,796:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,802:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,807:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,811:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,816:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,821:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,828:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,836:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,844:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,852:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,859:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,867:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,873:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,881:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,889:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,896:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,903:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,908:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,916:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,924:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,932:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,940:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,945:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,951:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,956:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,962:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,967:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,972:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,978:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,989:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:50,998:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,003:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,008:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,012:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,018:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,023:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,027:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,032:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,038:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,043:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,047:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,052:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,057:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,063:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,068:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,073:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,078:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,086:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,095:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,102:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,110:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,118:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,126:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,134:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,141:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,148:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,154:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,163:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,172:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,180:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,188:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,196:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,203:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,211:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,218:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,227:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,235:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,243:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,251:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,258:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,265:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,272:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,280:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,287:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,297:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,304:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,310:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,316:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,322:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,327:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,332:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,336:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,341:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,347:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,352:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,359:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,364:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,369:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,374:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,379:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,384:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,390:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,395:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,400:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,405:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,410:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,417:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,422:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,427:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,431:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,436:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,441:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,446:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,451:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,456:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,461:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,469:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,477:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,485:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,498:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,504:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,511:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,519:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,526:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,533:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,540:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,548:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,555:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,562:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,569:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,577:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,584:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,591:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,598:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,605:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,613:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,620:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,627:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,635:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,642:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,649:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,658:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,667:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,675:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,683:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,691:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,701:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,708:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,714:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,720:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,726:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,734:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,742:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,750:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,759:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,767:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,776:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,784:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,792:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,798:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,804:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,811:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,818:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,824:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,832:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,840:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,848:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,856:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,862:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,870:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,878:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,885:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,894:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,902:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,910:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,922:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,931:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,937:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,942:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,947:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,954:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,959:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,964:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,969:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,974:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,979:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,984:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:51,993:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,001:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,009:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,014:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,018:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,023:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,029:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,035:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,040:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,050:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,058:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,063:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,068:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,073:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,078:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,084:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,092:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,098:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,103:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,108:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,113:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,117:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,123:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,129:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,134:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,140:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,146:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,151:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,156:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,161:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,166:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,171:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,176:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,182:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,193:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,199:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,204:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,210:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,215:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,223:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,231:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,238:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,246:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,253:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,260:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,266:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,273:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,280:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,287:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,294:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,301:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,308:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,316:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,325:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,333:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,340:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,348:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,356:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,367:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,374:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,382:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,389:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,397:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,405:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,413:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,421:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,429:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,437:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,445:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,452:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,459:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,466:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,473:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,480:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,488:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,495:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,502:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,510:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,516:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,523:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,528:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,534:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,542:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,547:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,552:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,558:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,563:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,568:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,574:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,580:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,585:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,593:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,599:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,603:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,607:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,612:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,618:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,623:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,628:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,633:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,637:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,642:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,648:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,653:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,659:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,664:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,669:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,675:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,679:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,684:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,688:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,693:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,698:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,704:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,709:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,714:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,719:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,724:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,730:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,736:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,744:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,752:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,760:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,767:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,774:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,782:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,789:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,798:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,806:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,814:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,823:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,839:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,846:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,853:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,860:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,867:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:52,874:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)


.. parsed-literal::

    6.81 ms ± 303 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


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

    2018-09-21 11:36:53,244:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:53,311:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:53,369:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:53,428:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:53,485:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:53,543:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:53,591:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:53,645:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:53,702:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:53,749:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:53,805:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:53,863:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:53,910:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:53,957:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,005:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,063:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,111:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,169:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,235:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,296:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,344:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,412:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,462:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,509:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,555:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,658:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,725:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,773:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,820:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,868:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:54,914:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,190:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,264:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,334:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,383:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,434:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,502:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,553:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,625:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,672:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,718:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,764:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,811:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,875:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,933:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:55,979:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,035:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,094:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,142:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,189:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,236:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,284:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,356:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,406:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,459:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,505:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,563:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,612:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,660:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,707:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,753:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,801:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,855:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,904:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,950:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:56,999:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,047:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,095:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,144:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,194:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,261:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,318:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,389:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,438:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,488:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,535:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,597:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,644:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,703:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,750:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)


.. parsed-literal::

    56.3 ms ± 9.93 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


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

    2018-09-21 11:36:57,851:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:57,940:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,019:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,087:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,145:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,201:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,279:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,335:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,411:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,473:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,533:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,590:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,649:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,719:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,776:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,887:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:58,951:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,011:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,084:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,251:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,306:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,372:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,439:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,496:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,581:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,653:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,719:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,774:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,888:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:36:59,945:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,003:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,059:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,133:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,191:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,249:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,305:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,383:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,453:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,509:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,565:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,627:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,703:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,761:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,829:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,897:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:00,955:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,012:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,067:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,127:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,186:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,264:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,320:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,375:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,430:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,518:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,591:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,658:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,719:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,789:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,848:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,908:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:01,965:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,025:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,081:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,144:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,204:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,284:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,338:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,393:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,450:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,508:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,582:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,646:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,704:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,765:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,835:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,890:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-21 11:37:02,944:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)


.. parsed-literal::

    63 ms ± 2.2 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

