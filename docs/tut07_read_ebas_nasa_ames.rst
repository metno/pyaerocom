
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

    2018-08-16 09:22:02,154:INFO:
    Reading aliases ini file: /home/jonasg/github/pyaerocom/pyaerocom/data/aliases.ini
    2018-08-16 09:22:03,057:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,108:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,111:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,113:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,115:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:03,116:DEBUG:
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
                  <pyaerocom.io.ebas_nasa_ames.EbasFlagCol at 0x7efe2c018710>)])



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
          <th>2008-01-01 00:30:00.000</th>
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
          <th>2008-01-01 01:29:59.500</th>
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
          <th>2008-01-01 02:29:59.500</th>
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
          <th>2008-01-01 03:30:00.000</th>
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
          <th>2008-01-01 04:29:59.500</th>
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
          <th>2008-01-01 05:29:59.500</th>
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
          <th>2008-01-01 06:30:00.000</th>
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
          <th>2008-01-01 07:29:59.500</th>
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
          <th>2008-01-01 08:29:59.500</th>
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
          <th>2008-01-01 09:30:00.000</th>
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
          <th>2008-01-01 10:29:59.500</th>
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
          <th>2008-01-01 11:29:59.500</th>
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
          <th>2008-01-01 12:30:00.000</th>
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
          <th>2008-01-01 13:29:59.500</th>
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
          <th>2008-01-01 14:29:59.500</th>
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
          <th>2008-01-01 15:30:00.000</th>
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
          <th>2008-01-01 16:29:59.500</th>
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
          <th>2008-01-01 17:29:59.500</th>
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
          <th>2008-01-01 18:30:00.000</th>
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
          <th>2008-01-01 19:29:59.500</th>
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
          <th>2008-01-01 20:29:59.500</th>
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
          <th>2008-01-01 21:30:00.000</th>
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
          <th>2008-01-01 22:29:59.500</th>
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
          <th>2008-01-01 23:29:59.500</th>
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
          <th>2008-01-02 00:30:00.000</th>
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
          <th>2008-01-02 01:29:59.500</th>
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
          <th>2008-01-02 02:29:59.500</th>
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
          <th>2008-01-02 03:30:00.000</th>
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
          <th>2008-01-02 04:29:59.500</th>
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
          <th>2008-01-02 05:29:59.500</th>
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
          <th>2008-12-30 18:30:00.000</th>
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
          <th>2008-12-30 19:29:58.500</th>
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
          <th>2008-12-30 20:29:59.500</th>
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
          <th>2008-12-30 21:30:00.000</th>
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
          <th>2008-12-30 22:29:58.500</th>
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
          <th>2008-12-30 23:29:59.500</th>
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
          <th>2008-12-31 00:30:00.000</th>
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
          <th>2008-12-31 01:29:58.500</th>
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
          <th>2008-12-31 02:29:59.500</th>
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
          <th>2008-12-31 03:30:00.000</th>
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
          <th>2008-12-31 04:29:58.500</th>
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
          <th>2008-12-31 05:29:59.500</th>
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
          <th>2008-12-31 06:30:00.000</th>
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
          <th>2008-12-31 07:29:58.500</th>
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
          <th>2008-12-31 08:29:59.500</th>
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
          <th>2008-12-31 09:30:00.000</th>
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
          <th>2008-12-31 10:29:58.500</th>
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
          <th>2008-12-31 11:29:59.500</th>
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
          <th>2008-12-31 12:30:00.000</th>
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
          <th>2008-12-31 13:29:58.500</th>
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
          <th>2008-12-31 14:29:59.500</th>
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
          <th>2008-12-31 15:30:00.000</th>
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
          <th>2008-12-31 16:29:58.500</th>
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
          <th>2008-12-31 17:29:59.500</th>
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
          <th>2008-12-31 18:30:00.000</th>
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
          <th>2008-12-31 19:29:58.500</th>
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
          <th>2008-12-31 20:29:59.500</th>
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
          <th>2008-12-31 21:30:00.000</th>
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
          <th>2008-12-31 22:29:58.500</th>
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
          <th>2008-12-31 23:29:59.500</th>
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

    2018-08-16 09:22:03,387:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,393:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,394:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,395:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,398:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,402:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,402:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,403:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,404:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,408:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,409:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,409:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,411:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,415:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,415:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,416:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,417:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,421:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,422:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,422:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,424:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,428:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,428:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,429:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,430:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,434:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,436:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,437:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,441:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,446:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,448:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,450:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,454:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,459:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,461:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,463:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,466:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,472:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,474:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,475:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,479:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,484:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,485:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,486:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,489:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,493:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,495:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,496:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,498:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,502:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,504:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,505:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,508:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,512:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,513:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,514:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,516:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,519:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,520:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,521:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,524:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,528:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,529:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,529:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,531:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,536:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,536:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,537:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,538:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,542:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,543:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,543:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,545:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,549:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,549:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,550:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,551:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,555:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,555:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,556:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,558:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,562:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,564:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,566:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,569:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,574:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,576:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,577:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,581:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,586:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,587:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,587:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,589:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,593:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,595:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,597:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,599:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,604:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,605:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,606:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,608:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,612:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,612:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,613:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,615:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,619:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,621:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,622:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,626:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,632:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,633:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,635:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,638:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,643:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,645:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,647:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,650:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,656:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,658:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,660:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,664:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,668:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,669:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,670:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,672:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,676:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,677:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,678:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,681:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,685:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,687:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,688:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,689:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,694:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,694:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,695:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,696:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,700:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,700:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,701:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,702:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,706:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,707:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,707:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,709:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,713:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,714:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,714:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,716:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,720:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,720:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,721:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,722:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,726:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,726:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,727:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,729:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,733:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,734:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,736:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,738:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,742:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,743:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,743:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,746:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,750:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,751:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,751:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,753:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,758:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,758:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,759:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,761:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,765:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,766:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,766:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,768:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,772:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,772:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,773:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,775:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,779:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,781:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,783:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,787:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,793:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,795:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,796:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,801:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,805:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,808:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,810:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,813:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,820:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,821:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,822:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,824:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,828:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,829:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,830:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,832:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,837:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,838:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,838:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,840:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,845:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,845:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,846:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,848:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,852:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,855:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,857:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,860:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,865:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,866:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,869:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,873:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,874:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,875:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,877:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,881:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,882:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,882:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,885:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,888:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,889:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,890:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,892:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,897:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,898:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,898:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,900:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,905:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,906:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,907:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,909:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,913:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,914:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,915:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,917:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,921:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,922:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,923:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,925:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,930:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,931:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,931:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,933:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,938:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,939:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,939:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,941:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,945:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,946:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,947:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,949:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,953:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,954:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,955:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,957:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,961:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,962:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,963:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,965:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,969:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,970:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,971:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,973:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,977:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,978:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,978:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,980:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,985:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,986:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,986:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,988:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:03,992:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:03,994:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:03,996:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:03,999:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,004:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,006:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,007:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,011:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,018:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,019:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,021:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,029:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,034:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,035:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,036:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,041:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,046:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,047:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,048:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,051:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,055:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,056:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,057:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,059:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,064:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,065:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,066:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,070:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,074:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,076:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,077:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,079:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,084:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,085:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,086:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,088:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,092:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,093:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,094:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,097:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,101:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,102:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,103:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,106:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,110:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,111:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,112:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,115:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,119:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,120:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,121:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,123:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,127:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,128:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,128:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,130:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,134:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,135:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,136:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,141:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,146:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,147:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,148:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,150:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,154:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,156:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,157:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,161:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,166:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,167:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,168:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,170:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,174:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,175:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,176:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,178:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,183:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,184:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,185:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,188:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,192:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,193:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,194:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,196:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,199:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,200:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,202:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,207:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,211:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,212:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,212:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,214:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,218:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,219:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,219:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,221:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,225:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,226:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,227:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,229:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,234:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,236:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,238:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,240:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,245:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,246:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,248:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,250:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,254:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,255:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,256:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,257:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,261:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,262:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,262:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,264:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,268:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,269:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,270:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,272:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,275:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,276:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,277:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,279:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,282:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,283:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,284:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,285:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,289:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,290:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,290:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,292:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,296:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,296:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,297:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,299:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,303:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,304:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,304:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,306:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,310:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,310:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,311:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,313:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,316:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,317:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,318:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,319:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,323:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,324:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,324:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,326:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,330:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,330:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,331:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,332:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,336:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,337:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,337:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,339:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,343:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,344:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,346:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,350:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,350:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,351:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,352:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,356:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,356:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,357:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,359:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,363:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,363:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,364:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,366:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,369:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,370:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,370:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,372:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,376:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,376:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,377:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,378:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,382:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,383:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,383:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,384:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,388:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,389:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,389:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,395:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,398:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,400:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,402:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,405:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,410:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,411:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,413:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,416:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,420:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,422:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,422:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,424:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,428:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,429:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,429:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,431:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,435:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,436:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,436:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,438:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,441:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,442:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,442:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,444:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,448:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,448:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,449:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,450:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,454:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,457:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,459:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,464:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,471:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,472:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,473:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,475:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,479:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,480:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,481:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,485:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,489:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,490:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,490:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,492:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,496:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,497:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,497:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,499:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,505:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,507:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,509:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,514:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,518:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,520:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,520:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,522:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,526:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,527:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,527:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,529:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,533:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,533:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,534:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,535:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,539:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,540:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,542:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,545:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,550:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,552:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,553:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,555:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,559:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,560:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,561:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,563:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,568:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,569:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,570:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,572:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,576:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,577:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,577:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,579:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,583:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,584:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,584:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,585:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,590:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,592:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,593:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,596:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,602:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,603:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,605:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,609:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,610:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,611:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,612:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,616:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,617:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,617:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,619:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,623:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,623:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,624:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,626:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,630:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,630:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,631:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,633:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,636:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,637:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,638:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,639:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,643:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,644:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,644:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,646:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,650:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,651:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,651:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,653:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,657:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,659:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,661:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,664:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,669:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,671:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,673:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,676:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,680:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,682:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,683:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,685:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,689:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,690:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,692:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,694:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,699:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,700:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,704:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,708:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,709:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,710:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,712:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,715:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,716:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,716:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,718:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,722:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,722:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,723:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,724:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,727:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,728:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,729:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,731:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,735:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,736:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,736:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,738:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,742:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,744:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,746:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,749:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,753:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,754:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,756:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,758:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,761:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,762:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,763:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,765:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,769:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,770:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,771:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,772:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,776:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,777:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,778:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,779:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,783:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,784:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,784:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,786:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,789:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,790:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,790:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,792:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,796:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,796:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,797:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,798:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,802:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,802:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,803:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,804:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,808:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,808:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,808:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,810:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,814:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,815:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,817:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,820:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,826:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,827:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,828:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,832:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,836:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,837:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,838:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,839:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,844:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,845:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,846:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,849:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,853:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,854:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,854:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,856:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,860:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,860:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,861:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,862:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,867:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,869:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,872:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,873:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,874:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,876:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,880:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,881:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,881:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,883:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,887:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,887:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,888:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,889:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,892:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,893:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,893:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,895:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,901:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,902:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,906:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,911:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,913:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,914:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,917:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,924:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,925:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,927:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,929:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,933:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,934:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,934:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,936:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,940:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,941:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,941:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,943:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,946:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,947:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,947:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,949:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,953:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,953:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,954:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,955:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,959:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,961:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,962:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,965:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,970:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,972:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,973:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,977:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,982:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,984:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,985:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,988:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:04,993:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:04,995:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:04,995:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:04,998:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,001:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,002:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,003:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,005:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,009:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,009:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,010:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,012:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,015:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,016:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,016:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,020:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,024:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,025:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,027:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,036:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,041:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,043:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,044:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,050:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,054:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,056:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,056:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,059:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,062:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,063:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,064:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,065:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,069:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,069:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,070:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,071:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,075:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,076:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,076:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,077:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,081:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,082:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,082:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,084:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,088:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,088:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,088:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,090:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,094:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,096:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,097:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,100:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,105:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,106:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,107:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,109:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,113:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,114:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,114:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,116:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,119:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,120:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,120:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,122:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,126:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,126:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,127:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,128:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,132:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,134:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,135:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,138:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,142:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,143:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,144:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,146:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,150:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,150:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,151:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,153:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,156:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,156:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,157:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,158:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,162:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,162:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,163:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,164:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,168:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,168:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,169:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,170:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,174:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,177:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,179:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,184:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,191:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,192:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,193:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,195:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,198:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,199:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,200:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,206:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,210:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,211:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,212:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,214:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,217:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,218:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,219:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,220:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,224:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,227:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,229:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,233:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,238:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,240:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,241:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,243:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,247:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,248:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,249:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,250:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,254:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,257:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,259:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,262:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,267:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,268:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,268:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,270:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,274:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,275:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,280:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,282:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,286:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,287:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,288:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,289:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,293:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,293:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,294:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,295:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,300:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,301:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,303:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,307:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,313:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,315:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,316:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,319:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,322:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,324:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,326:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,329:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,333:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,334:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,334:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,337:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,341:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,341:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,342:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,343:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,347:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,348:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,349:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,350:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,354:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,355:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,355:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,357:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,360:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,361:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,362:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,363:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,367:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,367:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,368:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,369:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,373:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,373:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,374:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,375:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,379:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,381:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,382:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,386:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,391:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,393:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,396:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,405:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,409:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,410:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,410:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,412:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,416:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,418:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,419:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,422:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,426:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,427:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,428:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,430:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,434:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,436:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,437:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,439:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,444:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,445:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,446:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,448:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,452:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,452:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,453:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,454:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,457:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,458:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,458:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,460:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,463:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,463:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,464:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,465:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,469:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,470:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,470:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,472:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,475:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,475:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,476:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,477:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,480:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,481:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,481:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,483:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,486:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,487:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,487:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,489:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,492:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,493:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,494:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,497:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,498:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,498:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,500:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,503:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,503:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,504:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,505:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,509:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,511:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,512:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,516:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,522:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,525:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,527:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,531:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,535:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,536:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,537:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,539:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,542:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,543:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,545:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,550:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,555:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,556:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,557:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,558:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,562:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,562:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,563:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,564:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,568:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,571:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,572:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,577:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,582:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,584:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,585:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,588:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,593:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,594:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,594:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,596:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,600:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,601:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,601:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,603:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,606:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,607:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,607:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,609:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,612:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,613:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,614:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,616:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,620:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,620:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,621:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,622:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,626:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,626:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,627:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,629:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,632:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,634:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,636:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,638:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,643:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,645:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,647:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,650:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,654:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,655:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,655:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,657:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,661:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,662:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,662:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,664:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,667:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,668:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,668:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,670:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,674:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,676:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,677:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,680:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,685:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,687:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,688:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,690:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,694:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,695:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,696:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,698:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,701:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,702:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,704:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,707:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,708:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,708:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,710:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,714:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,715:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,717:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,720:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,724:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,726:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,727:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,730:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,734:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,735:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,736:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,738:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,743:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,743:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,744:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,746:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,749:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,750:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,750:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,752:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,755:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,756:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,757:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,758:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,762:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,762:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,763:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,765:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,768:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,769:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,770:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,772:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,776:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,778:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,780:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,783:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,787:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,788:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,789:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,791:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,794:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,795:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,796:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,797:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,801:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,801:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,801:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,803:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,807:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,807:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,808:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,809:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,813:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,814:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,815:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,816:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,820:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,820:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,820:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,822:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,825:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,825:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,826:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,827:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,831:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,832:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,833:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,836:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,837:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,837:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,839:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,842:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,842:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,842:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,844:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,847:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,848:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,848:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,850:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,853:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,854:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,854:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,855:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,858:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,860:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,862:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,866:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,871:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,872:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,873:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,876:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,881:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,883:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,884:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,886:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,890:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,891:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,891:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,893:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,896:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,897:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,897:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,899:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,902:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,903:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,903:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,905:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,908:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,910:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,912:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,915:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,919:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,920:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,921:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,923:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,927:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,928:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,929:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,931:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,935:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,936:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,937:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,939:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,943:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,944:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,945:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,947:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,950:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,951:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,952:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,954:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,958:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,958:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,959:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,961:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,965:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,965:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,966:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,968:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,971:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,972:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,973:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,975:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,979:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,980:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,982:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,985:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:05,990:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:05,992:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:05,993:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:05,997:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,001:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,002:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,003:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,005:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,009:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,011:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,012:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,014:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,017:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,018:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,020:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,022:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,029:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,030:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,031:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,033:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,037:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,040:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,041:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,050:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,056:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,057:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,058:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,060:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,064:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,066:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,068:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,071:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,076:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,077:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,078:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,080:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,084:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,086:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,088:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,090:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,095:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,097:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,098:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,101:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,105:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,106:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,107:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,109:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,114:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,115:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,117:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,119:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,123:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,124:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,125:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,127:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,131:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,133:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,133:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,136:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,140:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,141:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,142:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,144:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,148:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,148:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,149:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,151:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,155:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,155:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,156:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,158:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,161:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,161:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,162:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,163:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,167:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,168:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,168:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,169:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,172:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,173:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,173:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,175:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,178:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,178:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,179:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,180:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,184:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,185:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,187:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,190:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,195:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,196:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,198:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,205:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,206:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,207:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,210:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,214:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,215:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,216:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,219:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,223:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,223:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,224:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,225:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,228:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,230:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,231:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,235:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,239:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,240:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,240:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,242:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,246:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,247:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,248:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,249:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,253:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,253:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,254:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,256:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,259:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,259:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,260:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,261:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,264:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,265:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,266:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,267:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,270:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,271:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,272:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,273:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,276:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,277:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,277:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,278:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,282:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,282:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,283:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,284:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,287:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,288:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,289:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,291:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,294:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,295:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,295:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,299:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,303:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,304:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,305:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,307:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,311:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,311:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,312:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,314:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,317:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,318:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,318:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,320:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,323:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,324:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,324:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,326:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,330:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,331:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,331:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,333:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,337:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,340:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,343:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,347:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,352:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,354:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,356:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,359:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,363:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,364:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,365:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,367:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,370:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,371:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,372:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,373:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,377:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,377:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,378:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,379:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,383:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,384:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,384:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,387:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,390:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,392:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,393:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,394:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,400:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,402:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,402:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,404:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,409:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,410:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,410:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,415:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,419:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,420:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,420:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,422:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,425:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,426:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,427:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,429:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,434:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,435:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,435:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,437:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,441:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,441:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,442:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,444:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,447:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,447:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,448:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,449:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,453:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,453:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,454:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,455:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,459:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,462:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,464:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,467:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,473:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,474:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,475:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,477:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,481:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,482:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,482:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,485:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,489:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,490:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,491:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,493:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,497:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,498:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,499:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,501:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,505:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,506:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,507:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,509:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,513:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,514:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,515:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,517:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,521:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,523:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,525:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,528:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,532:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,532:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,533:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,535:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,539:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,543:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,544:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,546:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,550:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,550:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,551:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,552:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,555:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,556:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,556:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,558:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,561:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,562:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,562:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,564:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,567:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,568:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,568:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,570:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,573:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,574:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,574:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,576:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,580:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,580:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,580:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,582:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,585:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,586:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,586:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,588:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,591:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,592:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,592:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,594:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,597:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,598:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,598:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,600:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,603:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,605:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,607:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,610:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,616:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,617:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,619:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,622:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,628:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,629:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,630:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,632:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,636:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,637:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,637:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,639:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,643:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,644:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,644:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,646:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,650:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,651:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,651:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,653:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,657:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,658:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,658:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,660:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,663:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,664:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,665:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,666:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,670:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,671:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,671:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,673:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,677:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,677:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,678:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,679:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,683:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,683:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,684:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,686:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,689:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,692:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,693:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,694:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,698:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,698:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,705:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,710:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,711:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,712:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,714:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,718:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,719:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,719:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,721:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,725:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,726:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,727:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,729:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,734:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,735:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,735:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,738:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,741:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,742:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,743:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,745:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,749:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,752:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,754:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,759:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,764:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,765:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,766:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,769:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,772:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,773:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,774:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,776:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,780:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,781:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,781:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,783:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,787:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,787:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,788:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,790:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,794:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,796:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,797:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,801:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,807:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,809:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,811:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,814:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,817:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,818:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,819:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,821:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,825:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,825:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,826:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,828:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,832:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,832:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,833:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,834:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,838:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,838:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,839:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,840:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,844:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,846:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,847:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,850:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,854:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,855:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,855:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,857:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,861:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,862:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,863:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,864:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,868:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,869:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,870:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,871:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,874:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,875:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,876:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,879:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,883:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,884:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,885:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,887:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,891:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,891:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,892:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,894:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,897:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,901:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,903:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,906:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,910:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,911:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,912:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,914:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,918:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,919:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,920:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,922:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,926:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,927:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,927:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,930:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,934:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,935:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,935:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,938:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,941:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,943:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,943:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,946:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,950:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,951:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,951:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,954:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,958:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,959:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,959:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,962:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,965:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,967:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,968:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,970:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,973:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,974:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,975:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,978:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,981:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,982:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,983:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,986:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,989:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,990:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:06,991:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:06,993:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:06,997:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:06,999:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,001:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,004:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,009:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,010:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,012:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,015:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,020:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,021:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,022:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,025:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,029:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,030:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,031:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,035:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,040:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,041:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,042:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,044:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,048:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,050:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,051:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,061:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,066:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,067:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,068:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,070:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,074:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,075:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,077:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,079:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,083:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,085:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,087:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,091:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,096:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,097:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,098:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,101:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,105:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,106:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,106:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,108:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,112:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,115:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,116:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,120:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,125:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,127:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,128:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,130:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,134:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,135:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,136:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,138:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,141:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,142:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,143:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,145:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,149:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,150:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,150:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,152:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,155:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,156:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,157:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,158:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,162:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,165:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,167:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,169:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,173:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,174:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,175:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,177:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,180:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,181:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,182:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,183:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,187:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,188:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,189:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,193:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,193:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,194:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,195:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,199:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,201:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,202:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,205:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,209:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,209:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,210:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,212:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,216:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,216:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,217:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,218:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,222:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,222:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,223:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,224:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,228:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,229:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,230:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,232:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,236:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,237:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,237:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,239:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,243:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,244:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,244:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,246:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,249:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,250:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,250:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,252:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,256:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,256:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,256:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,258:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,262:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,262:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,263:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,265:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,268:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,269:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,269:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,271:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,275:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,276:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,276:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,278:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,282:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,282:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,283:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,285:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,288:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,289:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,290:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,292:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,295:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,296:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,297:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,299:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,303:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,304:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,305:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,307:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,311:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,312:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,312:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,314:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,317:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,318:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,318:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,320:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,323:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,324:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,324:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,325:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,329:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,330:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,330:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,332:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,336:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,336:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,336:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,338:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,341:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,342:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,342:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,343:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,347:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,347:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,348:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,349:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,353:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,353:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,353:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,355:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,359:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,361:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,363:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,367:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,371:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,373:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,375:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,379:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,384:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,386:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,388:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,392:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,397:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,399:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,400:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,403:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,406:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,407:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,408:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,409:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,413:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,414:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,415:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,418:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,425:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,427:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,428:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,431:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,436:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,437:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,439:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,442:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,446:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,448:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,449:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,451:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,455:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,456:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,456:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,458:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,462:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,462:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,463:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,464:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,468:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,469:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,469:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,471:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,474:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,475:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,475:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,477:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,480:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,481:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,481:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,483:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,486:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,487:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,487:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,489:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,493:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,493:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,495:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,499:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,499:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,500:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,501:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,505:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,505:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,506:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,508:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,511:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,512:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,513:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,514:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,518:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,518:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,519:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,520:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,524:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,526:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,529:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,534:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,541:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,545:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,547:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,549:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,553:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,554:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,556:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,558:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,562:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,563:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,564:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,566:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,570:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,570:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,571:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,573:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,577:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,577:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,578:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,580:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,584:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,586:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,587:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,589:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,593:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,595:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,596:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,598:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,602:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,603:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,606:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,610:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,610:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,611:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,613:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,617:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,618:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,619:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,621:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,625:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,625:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,626:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,628:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,632:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,633:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,633:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,635:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,639:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,640:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,640:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,642:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,646:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,647:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,648:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,649:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,653:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,655:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,657:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,660:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,666:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,667:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,668:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,671:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,675:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,675:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,676:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,678:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,681:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,682:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,683:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,684:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,688:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,689:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,689:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,691:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,695:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,695:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,696:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,698:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,701:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,702:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,704:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,708:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,708:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,709:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,710:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,714:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,716:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,717:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,720:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,726:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,729:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,732:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,737:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,744:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,746:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,747:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,749:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,754:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,755:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,756:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,758:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,762:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,762:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,763:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,764:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,767:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,768:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,769:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,770:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,773:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,776:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,777:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,781:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,786:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,788:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,790:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,793:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,798:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,799:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,800:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,803:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,806:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,807:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,808:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,810:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,814:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,814:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,815:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,817:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,820:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,821:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,821:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,823:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,827:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,827:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,828:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,830:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,834:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,835:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,837:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,840:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,846:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,849:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,850:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,853:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,858:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,859:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,859:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,861:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,865:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,866:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,866:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,868:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,871:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,872:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,873:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,874:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,878:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,878:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,879:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,881:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,884:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,885:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,886:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,887:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,891:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,892:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,892:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,894:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,897:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,900:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,902:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,907:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,914:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,915:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,918:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,921:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,925:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,926:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,926:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,928:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,932:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,934:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,935:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,937:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,941:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,942:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,943:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,945:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,949:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,952:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,953:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,955:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,959:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,960:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,961:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,964:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,968:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,969:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,969:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,971:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,974:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,974:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,975:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,976:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,980:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,980:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,981:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,982:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,985:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,986:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,986:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,988:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,991:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,992:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:07,992:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:07,993:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:07,997:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:07,999:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,001:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,004:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,009:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,010:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,011:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,013:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,017:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,019:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,020:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,023:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,027:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,028:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,028:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,030:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,034:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,035:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,035:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,037:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,040:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,041:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,042:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,045:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,049:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,049:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,049:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,051:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,055:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,056:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,056:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,058:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,061:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,061:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,062:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,073:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,077:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,077:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,077:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,079:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,083:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,086:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,088:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,091:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,097:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,099:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,100:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,104:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,109:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,111:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,112:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,116:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,121:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,124:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,126:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,129:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,133:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,134:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,134:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,137:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,140:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,141:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,141:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,143:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,147:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,148:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,148:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,150:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,154:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,154:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,155:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,157:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,160:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,161:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,161:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,163:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,166:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,167:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,168:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,169:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,173:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,174:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,174:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,176:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,180:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,180:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,182:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,184:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,188:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,189:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,190:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,194:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,196:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,198:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,206:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,208:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,209:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,212:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,216:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,216:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,217:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,219:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,223:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,224:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,224:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,226:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,230:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,231:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,231:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,234:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,238:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,239:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,239:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,241:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,245:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,246:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,246:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,247:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,251:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,251:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,252:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,254:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,258:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,258:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,259:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,260:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,264:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,266:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,268:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,271:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,277:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,279:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,281:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,284:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,289:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,290:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,291:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,293:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,298:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,299:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,299:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,302:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,307:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,308:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,309:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,311:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,314:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,315:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,316:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,319:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,323:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,325:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,327:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,329:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,334:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,335:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,336:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,338:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,345:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,345:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,347:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,352:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,352:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,353:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,354:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,357:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,358:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,358:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,360:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,363:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,364:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,365:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,366:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,369:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,370:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,370:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,372:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,375:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,376:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,376:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,378:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,381:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,382:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,382:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,384:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,387:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,388:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,388:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,390:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,393:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,393:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,394:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,395:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,398:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,399:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,399:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,400:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,404:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,406:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,410:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,414:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,421:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,423:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,425:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,438:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,442:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,444:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,447:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,451:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,452:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,453:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,455:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,459:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,460:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,460:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,462:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,466:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,466:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,467:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,469:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,473:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,473:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,474:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,476:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,479:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,480:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,480:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,482:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,485:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,486:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,487:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,489:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,493:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,493:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,495:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,499:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,501:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,503:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,507:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,512:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,514:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,516:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,520:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,525:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,527:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,529:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,532:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,536:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,537:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,538:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,540:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,544:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,545:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,547:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,549:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,553:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,554:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,555:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,558:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,562:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,563:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,564:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,566:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,570:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,571:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,572:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,575:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,579:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,580:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,581:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,583:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,587:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,590:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,591:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,594:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,600:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,602:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,604:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,607:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,613:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,614:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,615:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,619:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,623:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,624:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,625:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,627:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,631:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,632:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,632:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,635:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,640:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,641:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,642:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,644:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,647:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,648:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,649:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,650:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,655:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,657:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,658:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,661:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,665:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,666:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,667:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,669:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,673:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,675:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,677:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,679:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,683:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,684:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,684:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,686:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,690:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,691:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,691:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,693:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,697:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,700:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,706:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,711:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,712:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,713:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,715:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,719:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,719:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,720:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,722:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,725:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,726:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,727:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,730:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,734:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,735:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,736:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,738:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,742:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,742:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,743:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,744:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,748:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,749:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,749:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,751:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,754:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,756:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,757:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,760:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,764:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,765:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,765:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,768:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,771:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,772:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,773:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,774:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,778:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,781:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,782:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,786:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,792:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,794:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,796:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,800:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,805:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,807:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,808:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,811:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,815:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,815:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,816:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,818:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,822:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,822:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,823:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,825:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,828:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,829:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,829:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,831:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,834:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,836:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,837:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,840:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,844:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,844:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,845:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,847:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,851:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,852:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,852:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,854:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,858:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,859:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,861:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,863:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,868:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,868:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,869:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,871:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,875:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,876:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,876:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,878:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,882:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,882:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,883:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,884:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,888:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,888:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,889:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,890:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,894:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,894:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,894:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,896:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,900:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,900:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,900:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,902:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,907:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,909:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,911:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,914:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,918:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,919:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,920:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,922:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,926:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,927:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,927:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,929:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,932:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,934:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,936:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,938:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,943:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,945:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,946:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,949:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,954:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,955:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,956:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,958:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,962:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,964:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,966:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,969:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,974:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,976:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,977:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,981:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,985:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,986:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,987:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,989:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,993:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:08,993:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:08,994:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:08,996:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:08,999:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,000:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,000:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,002:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,006:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,007:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,007:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,009:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,012:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,013:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,013:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,015:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,019:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,022:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,024:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,028:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,033:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,034:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,036:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,039:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,044:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,045:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,046:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,051:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,055:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,056:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,056:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,058:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,062:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,063:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,064:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,066:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,069:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,070:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,071:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,081:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,086:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,086:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,087:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,089:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,093:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,093:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,094:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,096:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,100:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,101:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,102:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,103:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,107:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,108:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,109:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,111:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,115:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,116:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,116:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,118:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,123:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,124:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,124:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,126:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,130:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,131:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,132:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,134:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,138:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,139:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,139:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,141:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,145:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,146:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,147:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,149:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,153:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,154:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,155:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,157:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,162:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,162:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,163:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,165:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,169:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,170:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,170:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,173:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,176:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,178:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,178:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,183:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,188:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,189:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,190:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,194:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,196:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,200:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,202:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,206:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,207:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,207:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,209:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,212:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,213:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,213:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,215:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,219:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,221:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,222:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,224:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,229:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,231:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,232:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,235:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,240:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,241:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,242:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,244:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,248:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,248:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,249:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,250:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,254:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,256:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,257:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,259:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,263:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,264:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,265:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,267:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,270:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,271:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,272:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,273:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,277:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,277:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,278:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,280:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,283:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,283:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,284:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,285:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,289:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,289:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,290:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,291:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,295:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,295:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,296:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,297:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,301:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,302:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,302:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,304:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,308:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,308:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,309:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,311:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,315:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,316:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,316:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,318:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,321:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,322:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,322:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,324:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,327:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,327:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,328:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,330:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,334:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,334:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,335:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,336:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,340:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,341:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,341:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,342:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,346:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,347:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,347:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,349:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,352:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,354:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,356:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,361:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,366:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,368:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,370:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,374:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,378:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,382:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,383:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,385:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,389:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,390:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,391:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,393:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,397:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,397:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,398:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,400:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,403:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,404:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,404:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,406:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,409:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,410:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,410:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,412:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,415:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,416:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,417:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,418:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,422:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,423:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,423:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,425:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,429:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,429:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,430:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,432:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,435:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,436:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,437:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,442:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,446:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,446:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,447:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,449:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,452:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,455:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,456:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,461:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,466:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,468:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,469:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,473:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,478:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,479:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,480:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,482:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,486:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,487:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,488:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,490:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,494:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,495:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,495:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,497:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,501:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,502:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,503:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,505:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,508:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,509:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,510:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,512:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,515:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,516:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,517:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,519:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,523:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,523:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,524:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,525:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,529:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,530:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,530:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,532:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,535:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,536:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,537:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,538:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,542:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,542:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,543:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,545:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,548:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,549:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,550:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,552:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,556:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,557:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,558:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,560:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,564:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,565:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,566:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,568:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,573:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,574:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,575:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,578:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,582:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,583:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,583:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,585:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,589:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,590:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,590:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,592:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,595:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,596:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,597:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,599:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,603:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,605:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,608:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,613:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,621:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,623:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,625:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,629:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,634:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,635:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,636:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,638:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,642:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,643:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,643:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,645:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,649:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,649:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,650:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,652:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,656:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,656:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,657:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,658:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,662:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,665:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,667:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,671:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,677:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,679:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,681:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,684:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,689:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,690:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,691:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,693:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,697:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,697:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,698:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,700:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,704:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,706:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,708:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,711:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,715:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,716:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,717:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,719:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,723:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,724:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,724:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,726:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,730:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,731:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,732:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,736:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,742:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,743:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,744:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,746:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,749:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,750:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,751:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,753:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,757:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,758:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,759:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,761:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,766:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,766:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,767:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,768:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,772:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,774:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,776:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,784:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,791:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,793:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,793:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,796:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,800:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,801:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,802:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,804:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,808:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,809:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,809:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,811:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,816:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,816:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,817:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,819:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,823:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,823:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,824:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,825:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,829:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,830:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,830:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,832:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,835:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,836:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,836:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,838:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,842:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,842:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,843:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,844:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,848:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,849:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,849:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,851:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,855:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,855:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,856:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,857:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,861:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,861:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,862:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,863:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,867:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,868:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,869:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,870:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,874:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,874:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,875:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,877:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,880:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,880:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,881:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,882:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,886:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,887:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,887:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,889:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,892:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,893:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,893:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,895:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,901:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,903:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,908:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,913:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,916:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,917:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,921:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,925:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,926:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,927:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,929:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,933:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,934:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,935:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,936:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,940:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,941:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,941:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,943:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,946:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,947:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,947:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,949:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,952:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,953:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,953:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,955:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,958:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,961:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,962:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,965:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,969:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,970:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,970:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,972:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,976:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,977:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,977:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,979:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,983:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,983:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,983:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,985:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,989:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,989:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,989:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:09,991:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:09,994:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:09,996:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:09,998:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:10,001:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:10,007:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:10,009:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:10,010:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:10,014:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:10,019:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:10,021:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:10,023:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:10,027:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:10,031:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:10,032:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:10,033:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:10,035:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:10,040:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:10,041:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:10,042:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:10,044:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:10,048:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:10,049:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:10,050:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:10,053:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:10,056:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:10,057:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:10,058:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:10,061:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:10,065:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:10,066:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:10,066:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:10,067:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:10,071:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:10,071:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:10,072:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:10,073:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:10,076:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:10,077:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:10,077:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:10,088:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:10,092:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:10,092:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:10,093:DEBUG:
    Ignoring line no. 24: 35
    


.. parsed-literal::

    8.2 ms ± 196 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


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

    2018-08-16 09:22:11,583:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:11,588:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:11,589:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:11,589:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:11,590:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:11,590:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:11,641:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:11,646:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:11,646:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:11,646:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:11,647:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:11,647:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:11,695:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:11,699:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:11,700:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:11,701:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:11,702:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:11,703:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:11,766:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:11,770:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:11,771:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:11,771:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:11,772:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:11,773:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:11,831:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:11,835:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:11,836:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:11,836:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:11,837:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:11,837:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:11,894:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:11,897:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:11,899:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:11,901:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:11,902:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:11,903:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:11,956:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:11,960:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:11,961:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:11,961:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:11,962:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:11,962:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,011:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,016:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,016:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,017:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,017:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,018:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,067:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,071:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,071:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,071:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,072:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,072:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,118:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,122:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,123:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,124:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,127:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,128:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,178:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,182:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,184:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,186:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,187:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,188:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,244:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,248:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,248:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,249:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,249:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,250:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,298:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,302:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,303:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,304:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,305:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,306:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,365:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,370:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,372:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,373:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,374:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,375:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,436:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,439:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,440:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,440:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,441:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,441:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,489:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,494:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,495:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,496:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,496:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,497:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,546:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,550:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,551:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,551:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,552:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,552:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,614:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,619:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,620:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,621:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,622:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,623:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,681:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,685:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,686:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,687:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,687:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,688:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,741:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,745:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,745:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,746:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,746:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,747:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,792:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,797:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,797:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,798:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,798:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,798:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,844:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,848:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,848:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,849:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,849:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,850:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,915:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,920:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,922:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,923:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,924:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,925:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:12,976:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:12,979:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:12,980:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:12,980:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:12,981:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:12,981:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,026:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,030:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,031:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,031:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,031:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,032:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,075:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,079:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,081:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,082:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,083:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,084:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,150:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,154:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,156:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,157:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,158:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,159:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,212:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,215:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,216:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,216:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,217:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,217:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,271:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,274:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,275:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,275:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,276:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,276:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,323:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,327:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,327:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,328:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,328:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,329:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,388:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,393:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,395:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,397:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,398:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,400:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,467:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,471:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,472:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,472:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,472:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,473:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,520:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,524:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,528:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,529:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,530:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,531:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,591:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,595:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,595:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,596:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,596:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,597:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,657:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,661:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,662:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,662:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,663:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,664:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,715:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,719:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,721:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,722:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,723:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,724:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,780:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,784:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,785:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,787:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,788:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,789:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,838:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,842:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,843:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,843:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,844:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,844:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,897:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,902:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,902:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,903:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,903:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,903:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,949:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:13,953:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:13,954:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:13,954:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:13,955:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:13,955:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:13,998:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,002:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,004:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,006:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,007:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,008:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,058:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,064:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,064:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,065:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,065:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,065:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,109:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,113:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,113:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,114:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,114:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,115:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,175:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,179:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,181:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,182:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,183:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,185:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,241:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,245:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,246:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,246:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,247:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,248:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,316:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,320:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,321:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,321:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,322:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,322:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,368:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,373:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,375:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,377:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,378:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,379:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,449:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,453:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,453:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,453:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,454:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,454:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,509:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,514:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,514:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,515:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,515:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,516:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,570:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,574:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,575:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,576:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,576:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,577:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,622:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,626:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,626:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,627:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,627:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,628:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,690:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,694:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,695:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,696:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,696:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,697:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,749:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,753:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,753:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,754:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,754:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,755:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,801:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,805:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,807:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,808:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,809:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,810:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,860:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,865:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,867:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,868:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,869:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,870:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,921:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,925:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,925:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,926:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,926:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,927:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:14,972:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:14,976:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:14,977:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:14,977:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:14,978:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:14,978:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,021:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,025:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,025:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,026:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,026:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,027:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,071:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,075:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,075:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,076:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,076:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,077:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,120:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,124:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,126:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,127:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,128:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,129:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,178:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,182:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,184:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,185:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,187:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,188:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,245:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,249:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,250:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,250:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,250:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,251:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,305:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,309:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,310:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,310:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,311:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,311:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,356:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,361:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,361:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,361:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,362:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,362:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,414:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,418:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,419:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,420:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,421:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,421:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,469:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,473:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,473:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,474:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,474:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,475:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,521:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,525:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,525:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,525:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,526:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,526:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,569:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,574:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,574:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,574:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,575:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,575:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,618:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,622:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,622:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,623:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,623:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,623:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,675:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,679:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,681:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,682:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,683:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,684:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,756:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,760:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,760:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,761:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,761:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,762:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,809:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,813:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,814:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,814:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,815:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,815:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,861:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,866:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,867:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,868:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,914:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,918:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,920:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,922:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,923:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,924:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:15,974:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:15,979:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:15,980:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:15,980:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:15,981:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:15,981:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:16,026:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:16,030:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:16,030:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:16,031:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:16,031:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:16,032:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:16,075:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:16,079:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:16,081:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:16,082:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:16,084:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:16,085:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:16,136:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:16,140:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:16,140:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:16,141:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:16,141:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:16,142:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:16,188:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:16,192:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:16,192:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:16,193:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:16,193:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:16,194:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:16,240:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:16,245:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:16,246:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:16,248:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:16,249:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:16,250:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:16,315:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:16,319:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:16,321:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:16,322:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:16,323:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:16,324:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    59 ms ± 2.26 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


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

    2018-08-16 09:22:16,600:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:16,604:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:16,604:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:16,605:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:16,605:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:16,606:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:16,660:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:16,664:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:16,666:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:16,667:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:16,668:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:16,670:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:16,734:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:16,738:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:16,738:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:16,739:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:16,739:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:16,740:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:16,825:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:16,829:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:16,831:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:16,832:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:16,834:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:16,836:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:16,911:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:16,915:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:16,917:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:16,918:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:16,920:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:16,921:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:16,984:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:16,989:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:16,989:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:16,989:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:16,990:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:16,990:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:17,043:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:17,047:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:17,048:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:17,048:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:17,048:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:17,049:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:17,101:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:17,105:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:17,107:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:17,108:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:17,109:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:17,110:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:17,180:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:17,184:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:17,186:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:17,187:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:17,188:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:17,190:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:17,255:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:17,259:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:17,261:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:17,262:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:17,263:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:17,264:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:17,323:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:17,327:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:17,327:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:17,328:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:17,328:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:17,329:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:17,379:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:17,383:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:17,385:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:17,386:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:17,388:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:17,388:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:17,467:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:17,471:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:17,471:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:17,471:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:17,472:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:17,472:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:17,528:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:17,532:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:17,532:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:17,532:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:17,533:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:17,533:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:17,585:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:17,589:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:17,590:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:17,590:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:17,591:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:17,591:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:17,644:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:17,648:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:17,649:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:17,649:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:17,649:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:17,650:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:17,713:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:17,718:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:17,719:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:17,721:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:17,722:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:17,723:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:17,792:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:17,796:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:17,796:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:17,797:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:17,797:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:17,798:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:17,878:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:17,882:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:17,883:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:17,883:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:17,883:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:17,884:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:17,951:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:17,955:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:17,956:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:17,956:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:17,957:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:17,957:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,011:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,015:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,016:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,016:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,017:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,017:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,079:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,084:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,084:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,085:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,085:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,086:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,142:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,147:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,147:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,148:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,148:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,148:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,200:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,204:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,206:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,207:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,209:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,210:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,278:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,282:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,283:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,283:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,284:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,284:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,340:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,344:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,346:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,348:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,350:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,351:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,424:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,429:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,430:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,432:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,433:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,434:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,510:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,514:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,514:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,515:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,515:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,516:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,570:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,574:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,574:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,575:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,575:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,576:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,631:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,635:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,635:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,636:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,636:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,637:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,688:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,692:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,694:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,696:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,697:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,699:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,773:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,777:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,777:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,778:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,778:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,778:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,832:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,836:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,837:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,837:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,838:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,839:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,923:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,928:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,929:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,929:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,930:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,930:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:18,985:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:18,989:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:18,989:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:18,990:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:18,990:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:18,991:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:19,043:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:19,047:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:19,049:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:19,051:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:19,053:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:19,054:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:19,114:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:19,118:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:19,119:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:19,119:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:19,120:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:19,120:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:19,173:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:19,178:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:19,179:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:19,181:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:19,183:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:19,184:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:19,261:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:19,266:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:19,266:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:19,267:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:19,267:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:19,268:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:19,323:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:19,328:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:19,330:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:19,331:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:19,333:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:19,335:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:19,412:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:19,417:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:19,418:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:19,419:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:19,420:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:19,420:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:19,480:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:19,484:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:19,486:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:19,488:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:19,489:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:19,490:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:19,552:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:19,556:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:19,556:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:19,557:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:19,557:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:19,558:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:19,609:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:19,613:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:19,614:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:19,615:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:19,615:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:19,616:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:19,676:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:19,680:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:19,681:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:19,682:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:19,684:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:19,685:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:19,759:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:19,763:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:19,764:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:19,764:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:19,764:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:19,765:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:19,819:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:19,823:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:19,825:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:19,826:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:19,828:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:19,829:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:19,895:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:19,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:19,901:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:19,902:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:19,904:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:19,905:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:19,993:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:19,998:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,000:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,002:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,004:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,006:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:20,107:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:20,111:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,111:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,112:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,112:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,113:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:20,167:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:20,171:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,172:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,172:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,173:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,173:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:20,231:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:20,236:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,236:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,237:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,238:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,238:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:20,295:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:20,300:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,302:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,303:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,304:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,305:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:20,363:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:20,368:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,369:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,369:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,369:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,370:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:20,422:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:20,427:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,427:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,427:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,428:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,428:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:20,485:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:20,490:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,491:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,492:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,493:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,493:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:20,553:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:20,558:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,559:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,561:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,563:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,564:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:20,625:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:20,628:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,629:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,629:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,630:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,630:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:20,681:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:20,685:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,686:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,686:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,687:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,687:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:20,745:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:20,748:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,749:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,749:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,750:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,750:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:20,805:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:20,809:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,809:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,810:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,810:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,811:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:20,865:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:20,869:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,871:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,872:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,873:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,874:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:20,936:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:20,940:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:20,942:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:20,944:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:20,945:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:20,947:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,039:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,043:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,044:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,044:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,044:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,045:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,100:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,105:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,106:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,108:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,109:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,110:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,172:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,177:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,178:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,179:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,180:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,181:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,246:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,250:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,251:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,251:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,252:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,252:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,306:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,310:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,311:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,311:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,312:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,312:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,363:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,367:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,368:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,368:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,369:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,369:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,421:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,425:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,426:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,426:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,427:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,428:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,480:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,484:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,486:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,488:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,488:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,489:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,548:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,552:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,553:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,553:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,554:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,554:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,607:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,612:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,612:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,613:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,613:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,614:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,668:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,673:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,674:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,676:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,678:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,679:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,753:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,757:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,757:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,758:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,758:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,759:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,824:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,828:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,830:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,831:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,833:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,834:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,894:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,898:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,899:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,900:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,901:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,901:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:21,953:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:21,956:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:21,957:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:21,957:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:21,958:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:21,958:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:22,010:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:22,014:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:22,016:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:22,017:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:22,019:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:22,021:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:22,118:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:22,122:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:22,123:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:22,123:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:22,124:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:22,125:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-08-16 09:22:22,180:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-08-16 09:22:22,183:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-08-16 09:22:22,184:DEBUG:
    Ignoring line no. 23: 0
    
    2018-08-16 09:22:22,185:DEBUG:
    Ignoring line no. 24: 35
    
    2018-08-16 09:22:22,185:DEBUG:
    REACHED DATA BLOCK
    2018-08-16 09:22:22,186:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    69.5 ms ± 3.2 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

