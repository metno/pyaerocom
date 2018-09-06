
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

    2018-09-05 14:07:56,071:INFO:
    Reading aliases ini file: /home/jonasg/github/pyaerocom/pyaerocom/data/aliases.ini
    2018-09-05 14:07:56,850:WARNING:
    geopy library is not available. Aeolus data read not enabled
    2018-09-05 14:07:56,941:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:56,995:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:56,997:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:56,999:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,001:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:07:57,002:DEBUG:
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
                  <pyaerocom.io.ebas_nasa_ames.EbasFlagCol at 0x7f57b7f9ed30>)])



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

    2018-09-05 14:07:57,294:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,298:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,298:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,299:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,300:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,304:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,304:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,305:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,306:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,310:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,311:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,311:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,313:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,317:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,317:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,318:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,319:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,322:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,323:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,323:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,325:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,328:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,329:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,329:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,331:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,334:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,334:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,335:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,336:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,339:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,341:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,343:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,346:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,351:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,353:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,354:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,357:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,362:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,364:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,366:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,369:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,374:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,376:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,378:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,381:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,387:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,390:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,392:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,396:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,402:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,404:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,405:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,408:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,411:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,412:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,413:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,415:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,419:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,419:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,420:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,421:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,425:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,425:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,426:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,428:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,431:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,431:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,432:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,436:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,437:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,437:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,439:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,442:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,443:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,443:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,445:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,449:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,450:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,450:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,452:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,455:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,456:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,456:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,459:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,462:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,462:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,463:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,464:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,467:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,468:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,468:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,470:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,474:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,474:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,475:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,476:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,480:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,480:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,481:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,482:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,485:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,486:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,487:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,488:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,493:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,493:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,495:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,498:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,499:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,499:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,501:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,504:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,505:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,505:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,507:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,510:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,511:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,511:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,513:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,517:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,517:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,518:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,519:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,523:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,524:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,524:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,526:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,529:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,530:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,530:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,532:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,535:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,536:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,536:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,538:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,542:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,543:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,544:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,547:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,551:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,552:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,552:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,554:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,558:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,559:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,559:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,561:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,564:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,565:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,565:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,567:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,571:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,571:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,572:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,574:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,577:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,578:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,578:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,580:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,584:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,585:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,585:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,587:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,590:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,591:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,592:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,593:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,596:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,597:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,598:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,599:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,603:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,603:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,604:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,606:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,609:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,610:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,611:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,612:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,615:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,616:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,616:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,618:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,622:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,622:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,623:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,624:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,628:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,628:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,629:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,631:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,634:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,634:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,635:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,637:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,640:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,641:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,641:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,644:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,647:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,647:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,648:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,650:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,653:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,653:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,654:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,656:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,659:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,659:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,660:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,661:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,665:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,665:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,666:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,668:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,671:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,672:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,672:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,674:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,677:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,678:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,678:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,680:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,684:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,684:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,685:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,686:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,689:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,690:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,691:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,692:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,695:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,696:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,697:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,698:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,702:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,702:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,703:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,705:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,708:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,709:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,709:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,711:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,714:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,715:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,715:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,717:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,721:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,721:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,722:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,724:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,727:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,728:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,728:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,730:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,733:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,734:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,734:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,736:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,740:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,740:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,741:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,742:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,746:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,747:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,747:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,749:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,752:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,753:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,753:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,755:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,759:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,759:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,760:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,761:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,765:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,766:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,766:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,768:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,771:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,772:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,773:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,774:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,777:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,778:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,778:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,780:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,783:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,784:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,785:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,786:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,789:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,790:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,790:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,793:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,796:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,797:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,798:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,799:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,803:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,803:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,804:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,805:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,809:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,810:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,810:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,812:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,815:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,816:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,816:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,818:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,821:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,822:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,822:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,824:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,827:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,828:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,828:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,830:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,833:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,833:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,834:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,835:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,839:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,839:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,840:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,841:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,845:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,845:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,846:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,847:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,851:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,853:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,854:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,859:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,863:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,866:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,867:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,872:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,877:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,878:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,879:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,883:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,888:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,889:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,891:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,905:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,909:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,910:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,910:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,913:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,916:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,917:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,917:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,919:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,922:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,923:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,924:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,925:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,929:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,929:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,930:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,932:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,936:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,936:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,937:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,940:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,946:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,947:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,948:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,951:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,955:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,956:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,956:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,958:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,962:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,962:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,963:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,965:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,969:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,969:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,970:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,972:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,976:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,976:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,977:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,979:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,982:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,983:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,983:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,985:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,988:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,989:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,990:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,992:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:57,995:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:57,995:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:57,996:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:57,997:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,001:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,002:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,002:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,004:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,008:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,008:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,009:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,011:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,015:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,016:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,016:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,018:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,022:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,023:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,023:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,025:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,029:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,029:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,030:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,032:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,035:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,036:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,036:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,038:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,042:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,042:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,043:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,045:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,048:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,049:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,049:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,051:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,054:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,056:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,058:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,061:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,066:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,068:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,069:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,074:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,078:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,080:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,082:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,085:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,088:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,090:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,090:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,093:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,097:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,098:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,099:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,101:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,104:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,105:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,106:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,108:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,112:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,112:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,113:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,115:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,118:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,119:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,120:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,122:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,126:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,128:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,129:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,133:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,137:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,139:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,140:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,143:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,146:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,148:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,148:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,150:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,153:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,154:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,155:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,157:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,160:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,161:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,161:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,163:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,167:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,167:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,168:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,169:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,173:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,173:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,174:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,175:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,179:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,180:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,180:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,182:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,185:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,186:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,187:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,188:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,192:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,193:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,193:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,195:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,198:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,199:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,199:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,204:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,205:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,205:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,207:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,210:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,211:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,211:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,213:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,216:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,217:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,217:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,219:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,222:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,223:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,224:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,225:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,229:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,230:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,230:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,232:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,236:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,236:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,237:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,239:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,242:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,243:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,243:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,245:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,249:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,250:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,250:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,252:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,255:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,255:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,256:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,258:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,261:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,261:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,262:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,264:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,267:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,268:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,268:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,269:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,273:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,273:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,274:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,275:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,278:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,279:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,279:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,280:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,283:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,284:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,284:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,286:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,289:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,290:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,290:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,292:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,295:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,296:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,296:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,301:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,305:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,305:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,306:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,308:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,312:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,313:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,313:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,315:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,318:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,319:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,319:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,321:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,325:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,326:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,326:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,328:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,332:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,334:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,335:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,338:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,344:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,346:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,350:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,354:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,356:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,357:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,360:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,365:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,368:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,370:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,373:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,377:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,379:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,381:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,385:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,390:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,391:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,393:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,396:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,401:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,402:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,403:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,406:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,409:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,410:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,412:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,414:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,418:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,419:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,419:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,422:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,426:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,426:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,427:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,429:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,433:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,434:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,434:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,437:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,440:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,441:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,442:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,444:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,448:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,449:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,449:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,452:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,455:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,456:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,457:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,459:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,463:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,463:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,464:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,466:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,470:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,471:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,471:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,473:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,477:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,478:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,479:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,481:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,485:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,486:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,487:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,489:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,493:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,494:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,496:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,500:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,501:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,502:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,504:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,507:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,508:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,509:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,511:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,515:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,515:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,516:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,518:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,522:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,522:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,523:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,524:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,528:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,529:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,529:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,531:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,534:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,535:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,536:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,537:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,541:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,543:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,545:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,549:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,553:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,555:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,556:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,560:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,564:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,565:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,566:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,568:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,572:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,573:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,575:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,577:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,581:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,582:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,582:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,584:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,588:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,589:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,590:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,591:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,595:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,596:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,597:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,599:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,603:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,603:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,604:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,606:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,610:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,611:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,612:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,614:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,617:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,618:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,619:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,621:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,625:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,626:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,626:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,628:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,632:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,633:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,634:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,636:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,641:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,641:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,642:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,644:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,648:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,649:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,649:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,652:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,656:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,657:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,657:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,659:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,663:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,664:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,665:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,667:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,670:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,671:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,672:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,675:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,678:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,679:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,680:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,681:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,685:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,686:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,687:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,689:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,693:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,694:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,695:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,697:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,700:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,701:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,702:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,704:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,708:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,709:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,709:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,711:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,715:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,716:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,717:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,719:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,722:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,723:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,724:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,726:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,730:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,731:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,733:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,736:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,741:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,742:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,743:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,745:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,748:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,749:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,750:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,752:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,755:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,756:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,756:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,758:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,761:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,764:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,765:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,768:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,771:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,773:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,773:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,775:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,778:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,779:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,780:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,781:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,785:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,786:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,786:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,788:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,791:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,792:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,792:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,794:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,798:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,799:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,799:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,801:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,804:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,805:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,806:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,807:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,811:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,812:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,812:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,814:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,817:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,818:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,819:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,820:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,823:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,824:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,825:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,826:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,829:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,830:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,831:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,833:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,836:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,837:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,837:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,839:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,842:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,843:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,844:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,845:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,848:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,849:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,850:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,851:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,855:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,855:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,856:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,857:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,860:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,861:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,862:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,864:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,867:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,868:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,868:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,870:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,874:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,874:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,875:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,877:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,880:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,881:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,881:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,883:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,886:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,887:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,888:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,890:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,893:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,893:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,894:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,896:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,900:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,901:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,913:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,917:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,917:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,918:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,920:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,923:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,924:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,924:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,926:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,930:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,930:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,931:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,933:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,936:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,937:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,937:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,939:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,942:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,943:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,944:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,945:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,949:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,949:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,950:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,952:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,955:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,956:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,957:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,959:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,962:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,963:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,963:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,965:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,968:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,969:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,970:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,972:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,975:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,976:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,976:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,978:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,983:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,983:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,984:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,986:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,989:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,990:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,991:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,992:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:58,995:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:58,996:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:58,997:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:58,998:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,003:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,004:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,004:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,006:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,009:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,010:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,011:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,012:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,016:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,018:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,019:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,023:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,027:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,029:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,031:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,034:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,038:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,039:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,040:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,043:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,047:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,048:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,049:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,051:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,054:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,055:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,055:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,057:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,061:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,062:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,062:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,064:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,068:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,068:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,069:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,071:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,074:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,075:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,075:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,077:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,080:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,081:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,081:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,083:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,086:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,087:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,088:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,089:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,093:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,093:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,094:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,095:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,098:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,099:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,099:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,101:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,105:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,105:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,106:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,107:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,110:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,111:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,111:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,113:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,116:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,117:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,117:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,119:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,122:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,123:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,123:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,125:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,128:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,128:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,129:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,130:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,134:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,135:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,135:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,136:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,140:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,140:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,141:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,143:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,146:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,146:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,147:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,148:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,151:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,152:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,152:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,154:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,157:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,158:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,158:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,160:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,162:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,163:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,164:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,165:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,168:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,169:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,170:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,171:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,174:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,175:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,175:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,177:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,180:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,181:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,181:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,183:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,186:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,187:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,187:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,189:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,193:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,193:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,194:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,195:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,199:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,199:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,200:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,202:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,205:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,206:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,206:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,208:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,211:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,211:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,212:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,213:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,216:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,217:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,218:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,219:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,222:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,223:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,223:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,225:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,228:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,229:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,229:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,231:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,234:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,235:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,235:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,237:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,241:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,243:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,244:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,249:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,254:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,256:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,259:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,264:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,271:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,272:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,274:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,276:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,280:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,282:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,285:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,288:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,293:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,294:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,295:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,297:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,301:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,302:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,302:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,307:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,311:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,312:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,313:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,314:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,318:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,318:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,319:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,321:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,324:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,325:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,325:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,327:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,330:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,331:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,331:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,333:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,337:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,338:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,338:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,340:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,344:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,344:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,345:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,347:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,350:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,351:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,352:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,353:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,357:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,358:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,358:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,360:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,364:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,365:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,365:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,367:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,370:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,371:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,371:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,373:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,376:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,377:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,377:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,379:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,382:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,383:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,384:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,385:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,388:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,389:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,390:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,391:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,395:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,396:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,398:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,401:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,406:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,407:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,408:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,410:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,414:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,415:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,415:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,417:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,420:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,421:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,421:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,423:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,426:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,426:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,427:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,428:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,432:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,433:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,433:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,435:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,439:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,439:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,440:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,441:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,444:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,445:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,445:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,447:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,451:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,451:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,451:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,453:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,456:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,457:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,457:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,459:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,462:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,463:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,463:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,465:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,468:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,468:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,468:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,470:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,474:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,475:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,475:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,476:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,480:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,480:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,481:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,482:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,485:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,486:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,486:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,487:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,490:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,491:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,491:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,492:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,496:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,496:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,497:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,498:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,502:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,503:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,503:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,505:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,508:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,508:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,508:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,510:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,514:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,514:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,514:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,516:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,519:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,519:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,520:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,521:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,525:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,525:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,526:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,527:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,530:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,531:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,531:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,532:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,536:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,536:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,536:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,538:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,541:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,542:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,542:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,544:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,548:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,548:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,549:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,551:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,554:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,555:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,555:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,557:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,561:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,561:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,562:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,563:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,567:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,567:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,567:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,569:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,573:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,573:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,574:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,575:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,579:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,579:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,580:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,581:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,585:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,586:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,586:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,588:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,591:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,591:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,592:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,594:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,597:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,598:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,598:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,600:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,603:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,604:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,604:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,605:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,608:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,609:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,609:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,611:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,614:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,615:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,615:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,617:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,620:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,621:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,621:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,623:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,626:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,626:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,627:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,628:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,632:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,633:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,633:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,635:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,639:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,639:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,640:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,641:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,646:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,646:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,647:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,648:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,652:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,652:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,653:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,654:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,658:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,658:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,658:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,660:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,664:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,664:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,664:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,666:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,670:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,671:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,673:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,677:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,682:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,683:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,685:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,689:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,694:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,696:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,697:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,699:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,702:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,703:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,704:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,706:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,710:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,710:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,711:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,713:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,716:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,716:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,717:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,718:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,721:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,722:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,722:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,723:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,727:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,727:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,728:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,729:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,732:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,733:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,733:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,735:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,737:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,738:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,738:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,739:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,742:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,743:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,743:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,745:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,748:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,749:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,749:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,751:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,754:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,755:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,755:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,757:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,760:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,761:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,761:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,763:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,766:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,766:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,767:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,768:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,772:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,772:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,773:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,774:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,778:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,778:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,779:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,780:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,783:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,784:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,784:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,786:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,789:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,789:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,790:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,792:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,795:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,796:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,796:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,798:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,801:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,802:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,803:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,804:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,807:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,808:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,808:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,810:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,813:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,813:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,814:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,815:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,818:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,819:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,819:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,821:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,824:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,824:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,825:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,826:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,829:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,830:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,830:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,832:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,835:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,836:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,836:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,837:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,841:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,842:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,842:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,843:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,847:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,847:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,848:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,849:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,853:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,853:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,854:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,855:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,858:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,859:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,859:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,861:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,864:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,865:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,865:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,867:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,870:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,871:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,871:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,872:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,876:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,876:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,877:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,878:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,882:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,882:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,882:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,884:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,887:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,888:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,888:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,889:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,893:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,893:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,894:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,895:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,898:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,899:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,899:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,901:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,904:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,905:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,905:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,909:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,912:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,913:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,913:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,924:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,927:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,928:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,928:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,930:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,934:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,934:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,935:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,936:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,940:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,940:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,941:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,942:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,945:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,946:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,947:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,948:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,951:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,952:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,952:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,954:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,957:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,958:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,958:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,960:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,964:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,964:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,965:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,966:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,970:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,971:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,971:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,972:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,976:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,976:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,977:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,978:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,981:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,982:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,982:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,984:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,988:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,988:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,989:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,990:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,993:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:07:59,994:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:07:59,994:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:07:59,996:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:07:59,999:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,000:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,000:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,002:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,006:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,007:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,007:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,009:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,012:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,013:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,013:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,015:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,018:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,018:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,019:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,020:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,024:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,024:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,024:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,026:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,029:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,030:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,030:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,031:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,034:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,035:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,035:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,037:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,041:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,041:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,042:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,043:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,047:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,047:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,048:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,049:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,053:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,053:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,053:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,055:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,058:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,058:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,059:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,060:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,064:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,064:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,065:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,066:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,069:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,070:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,070:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,071:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,075:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,075:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,076:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,077:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,081:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,081:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,082:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,083:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,087:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,087:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,088:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,089:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,092:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,093:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,093:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,095:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,098:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,098:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,099:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,100:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,103:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,104:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,105:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,106:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,109:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,110:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,110:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,112:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,115:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,115:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,116:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,117:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,121:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,121:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,122:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,124:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,127:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,127:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,128:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,129:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,132:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,133:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,134:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,135:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,138:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,139:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,139:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,140:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,143:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,144:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,144:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,146:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,150:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,150:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,150:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,152:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,156:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,156:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,157:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,158:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,161:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,161:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,162:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,163:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,166:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,167:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,167:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,168:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,172:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,173:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,173:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,174:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,177:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,178:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,178:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,180:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,183:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,183:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,184:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,185:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,188:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,189:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,189:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,190:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,193:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,194:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,194:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,196:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,199:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,199:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,200:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,201:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,204:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,205:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,205:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,206:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,209:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,210:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,210:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,212:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,215:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,215:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,216:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,217:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,220:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,221:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,221:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,223:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,225:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,226:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,226:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,228:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,231:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,231:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,232:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,233:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,236:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,237:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,237:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,239:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,242:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,242:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,243:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,244:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,247:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,248:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,248:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,250:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,254:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,254:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,255:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,256:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,259:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,260:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,261:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,262:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,266:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,268:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,269:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,273:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,278:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,280:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,281:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,285:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,289:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,291:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,292:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,295:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,298:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,300:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,300:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,302:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,305:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,306:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,307:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,309:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,312:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,313:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,314:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,319:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,323:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,324:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,324:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,326:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,331:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,332:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,334:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,337:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,340:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,341:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,342:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,344:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,347:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,348:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,349:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,350:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,353:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,354:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,354:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,356:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,359:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,360:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,360:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,361:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,364:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,365:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,365:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,367:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,370:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,371:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,371:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,372:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,375:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,376:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,376:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,378:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,381:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,381:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,381:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,383:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,386:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,386:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,387:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,388:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,392:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,392:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,393:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,394:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,398:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,398:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,398:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,400:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,403:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,404:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,404:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,406:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,409:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,409:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,409:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,411:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,414:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,415:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,415:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,416:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,419:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,420:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,420:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,422:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,425:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,425:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,426:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,427:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,431:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,431:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,432:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,437:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,437:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,437:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,439:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,442:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,443:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,443:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,444:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,448:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,449:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,449:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,451:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,455:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,457:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,459:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,463:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,468:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,469:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,471:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,474:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,479:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,481:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,483:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,486:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,493:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,496:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,500:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,504:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,506:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,507:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,512:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,516:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,517:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,519:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,521:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,525:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,525:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,526:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,528:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,531:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,532:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,533:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,534:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,538:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,538:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,539:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,541:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,544:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,545:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,545:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,547:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,550:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,551:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,552:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,553:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,557:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,557:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,558:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,560:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,563:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,564:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,564:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,566:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,570:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,570:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,571:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,573:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,576:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,577:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,578:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,580:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,583:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,584:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,584:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,586:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,589:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,590:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,590:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,592:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,595:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,596:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,597:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,598:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,602:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,603:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,604:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,609:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,610:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,610:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,612:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,615:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,616:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,617:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,618:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,622:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,623:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,623:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,625:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,628:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,629:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,630:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,632:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,635:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,636:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,636:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,638:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,641:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,642:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,643:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,645:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,648:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,649:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,649:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,651:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,655:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,656:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,656:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,658:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,662:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,662:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,663:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,666:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,669:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,670:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,670:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,672:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,675:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,676:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,677:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,678:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,682:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,683:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,683:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,685:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,689:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,689:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,690:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,692:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,695:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,695:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,696:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,698:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,701:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,702:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,703:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,704:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,708:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,709:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,709:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,711:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,714:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,715:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,716:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,717:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,721:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,721:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,722:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,724:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,728:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,728:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,729:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,730:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,734:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,734:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,735:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,737:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,740:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,741:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,741:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,743:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,746:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,747:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,747:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,749:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,752:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,753:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,754:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,755:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,758:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,759:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,760:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,761:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,765:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,766:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,767:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,769:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,773:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,774:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,774:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,776:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,780:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,780:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,781:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,783:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,787:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,787:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,788:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,790:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,793:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,794:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,794:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,796:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,799:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,800:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,801:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,802:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,806:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,808:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,810:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,813:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,818:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,819:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,821:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,824:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,829:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,830:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,831:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,834:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,837:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,838:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,839:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,841:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,844:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,845:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,846:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,848:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,852:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,853:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,853:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,855:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,859:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,860:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,861:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,863:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,866:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,867:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,868:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,870:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,873:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,874:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,875:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,877:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,880:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,881:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,882:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,884:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,888:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,888:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,889:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,891:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,895:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,896:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,896:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,899:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,902:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,903:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,904:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,906:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,910:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,912:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,913:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,922:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,933:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,935:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,936:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,939:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,944:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,946:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,948:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,950:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,956:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,957:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,961:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,963:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,968:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,969:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,970:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,973:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,976:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,977:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,978:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,980:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,984:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,984:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,985:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,987:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,990:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,991:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,992:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:00,993:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:00,997:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:00,997:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:00,998:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,000:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,003:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,004:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,004:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,006:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,010:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,010:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,011:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,012:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,016:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,017:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,017:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,019:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,022:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,023:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,023:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,025:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,029:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,029:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,030:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,032:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,035:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,036:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,036:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,038:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,042:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,042:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,043:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,045:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,048:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,049:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,050:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,051:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,055:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,055:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,056:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,058:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,061:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,061:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,062:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,063:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,067:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,067:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,068:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,070:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,073:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,074:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,074:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,076:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,080:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,081:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,081:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,083:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,086:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,087:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,088:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,090:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,093:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,094:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,095:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,096:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,100:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,101:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,101:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,103:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,107:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,107:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,108:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,110:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,113:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,114:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,114:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,116:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,121:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,122:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,123:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,125:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,129:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,130:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,130:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,132:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,136:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,136:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,137:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,139:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,142:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,143:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,143:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,145:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,148:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,149:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,150:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,151:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,155:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,155:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,156:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,158:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,161:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,162:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,162:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,164:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,168:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,169:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,169:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,171:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,174:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,175:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,176:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,178:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,181:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,182:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,183:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,184:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,188:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,189:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,190:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,194:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,194:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,195:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,196:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,200:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,201:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,203:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,207:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,211:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,213:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,215:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,218:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,223:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,224:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,226:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,229:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,234:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,236:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,237:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,240:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,245:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,248:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,249:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,252:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,257:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,259:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,260:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,262:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,267:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,268:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,269:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,271:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,274:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,275:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,275:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,277:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,280:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,281:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,281:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,283:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,286:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,286:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,287:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,288:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,291:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,292:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,292:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,293:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,297:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,297:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,298:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,300:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,303:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,304:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,304:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,305:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,308:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,309:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,309:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,311:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,314:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,315:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,315:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,317:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,320:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,321:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,321:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,327:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,331:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,331:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,332:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,334:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,337:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,338:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,338:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,339:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,343:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,343:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,344:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,345:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,349:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,349:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,350:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,351:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,355:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,356:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,356:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,358:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,361:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,362:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,362:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,364:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,367:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,367:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,368:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,369:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,372:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,372:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,373:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,374:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,378:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,379:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,379:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,381:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,384:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,385:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,385:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,387:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,390:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,391:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,391:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,393:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,396:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,397:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,397:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,399:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,402:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,403:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,403:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,405:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,408:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,409:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,409:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,410:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,414:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,414:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,414:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,416:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,420:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,420:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,420:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,422:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,426:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,426:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,426:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,428:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,431:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,431:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,432:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,433:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,436:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,437:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,437:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,439:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,442:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,442:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,443:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,444:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,447:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,448:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,448:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,450:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,453:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,453:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,454:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,455:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,458:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,459:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,459:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,461:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,465:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,465:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,466:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,467:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,470:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,471:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,471:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,473:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,476:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,477:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,477:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,478:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,482:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,482:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,483:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,484:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,487:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,488:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,488:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,490:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,493:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,494:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,494:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,496:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,500:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,501:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,504:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,507:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,511:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,513:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,514:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,517:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,524:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,525:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,527:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,531:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,535:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,537:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,539:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,544:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,548:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,549:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,550:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,552:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,556:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,556:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,557:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,559:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,562:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,563:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,563:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,565:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,568:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,569:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,569:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,571:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,574:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,575:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,575:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,577:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,580:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,581:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,581:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,584:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,587:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,587:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,588:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,589:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,593:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,593:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,594:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,596:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,599:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,600:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,600:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,602:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,605:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,606:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,606:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,609:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,612:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,613:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,613:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,615:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,618:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,619:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,619:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,621:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,624:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,624:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,625:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,626:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,629:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,630:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,630:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,632:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,635:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,636:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,636:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,638:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,641:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,641:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,642:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,643:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,647:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,649:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,650:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,654:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,658:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,660:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,662:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,666:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,670:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,672:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,674:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,677:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,682:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,684:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,685:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,689:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,693:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,695:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,696:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,699:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,702:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,703:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,703:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,706:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,709:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,710:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,711:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,713:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,717:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,717:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,718:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,720:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,723:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,724:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,725:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,726:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,730:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,730:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,731:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,732:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,736:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,738:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,739:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,743:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,747:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,749:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,750:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,754:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,758:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,760:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,760:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,762:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,765:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,766:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,767:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,769:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,772:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,773:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,773:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,775:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,778:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,778:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,778:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,780:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,783:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,784:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,784:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,786:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,789:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,790:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,791:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,792:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,795:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,796:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,796:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,798:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,802:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,802:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,803:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,804:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,807:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,808:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,808:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,810:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,813:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,814:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,814:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,816:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,820:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,820:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,821:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,822:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,825:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,826:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,826:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,828:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,831:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,832:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,833:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,835:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,838:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,838:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,839:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,840:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,844:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,844:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,845:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,847:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,850:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,851:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,851:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,853:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,856:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,857:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,857:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,859:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,862:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,863:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,863:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,865:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,868:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,869:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,869:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,871:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,874:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,875:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,875:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,877:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,881:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,881:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,882:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,884:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,888:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,888:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,889:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,890:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,894:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,895:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,895:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,897:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,900:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,901:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,901:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,904:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,908:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,909:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,909:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,911:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,916:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,917:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,917:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,919:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,922:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,923:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,924:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,933:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,938:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,939:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,940:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,942:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,945:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,946:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,946:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,948:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,951:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,952:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,953:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,954:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,958:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,959:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,959:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,962:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,966:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,966:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,967:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,969:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,973:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,973:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,974:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,976:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,980:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,981:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,981:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,983:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,987:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,987:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,988:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,990:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:01,994:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:01,995:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:01,995:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:01,997:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,000:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,001:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,002:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,004:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,007:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,008:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,009:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,011:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,015:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,015:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,016:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,018:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,021:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,022:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,023:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,025:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,028:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,029:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,030:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,031:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,035:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,036:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,036:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,038:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,041:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,042:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,043:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,045:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,048:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,049:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,049:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,051:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,055:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,055:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,056:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,058:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,061:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,062:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,062:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,064:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,067:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,068:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,069:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,071:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,074:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,075:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,075:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,077:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,081:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,081:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,082:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,084:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,087:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,088:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,089:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,091:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,094:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,095:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,095:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,097:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,100:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,101:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,101:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,103:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,106:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,107:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,107:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,109:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,113:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,114:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,114:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,116:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,119:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,120:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,120:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,121:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,125:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,125:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,126:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,128:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,130:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,131:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,131:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,133:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,136:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,138:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,139:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,142:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,148:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,149:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,151:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,154:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,159:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,160:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,161:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,164:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,167:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,168:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,169:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,171:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,174:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,175:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,175:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,177:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,181:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,181:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,182:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,183:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,187:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,188:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,188:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,190:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,193:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,194:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,194:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,196:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,200:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,202:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,203:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,207:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,213:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,215:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,216:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,218:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,221:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,222:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,223:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,225:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,228:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,229:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,230:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,231:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,235:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,237:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,238:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,241:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,245:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,245:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,246:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,248:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,253:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,254:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,254:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,256:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,259:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,260:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,260:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,262:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,265:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,265:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,266:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,269:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,272:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,272:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,273:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,274:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,277:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,278:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,278:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,280:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,283:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,283:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,284:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,286:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,289:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,289:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,290:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,292:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,295:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,295:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,295:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,297:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,300:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,300:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,301:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,303:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,306:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,307:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,307:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,308:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,312:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,312:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,313:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,314:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,317:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,318:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,318:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,320:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,323:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,324:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,324:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,327:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,330:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,331:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,331:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,335:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,338:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,339:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,339:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,341:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,345:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,345:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,345:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,347:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,350:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,351:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,351:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,353:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,357:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,357:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,357:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,359:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,363:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,363:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,364:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,365:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,368:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,369:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,369:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,371:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,374:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,374:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,375:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,376:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,380:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,380:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,381:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,382:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,386:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,386:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,387:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,388:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,392:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,392:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,393:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,394:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,398:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,398:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,399:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,401:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,404:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,404:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,405:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,406:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,409:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,410:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,410:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,412:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,415:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,415:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,416:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,417:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,420:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,421:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,421:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,423:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,426:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,427:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,427:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,428:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,431:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,432:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,432:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,434:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,437:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,437:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,438:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,439:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,442:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,443:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,443:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,445:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,448:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,449:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,449:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,451:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,454:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,454:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,455:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,457:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,461:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,461:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,462:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,463:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,466:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,468:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,470:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,474:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,480:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,482:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,483:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,487:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,492:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,494:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,495:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,499:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,503:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,504:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,505:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,508:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,512:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,513:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,514:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,516:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,520:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,522:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,524:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,526:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,531:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,533:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,534:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,537:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,542:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,543:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,544:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,547:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,550:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,552:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,552:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,554:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,557:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,558:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,558:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,560:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,563:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,564:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,564:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,566:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,570:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,570:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,571:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,573:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,576:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,577:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,577:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,579:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,582:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,583:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,583:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,585:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,588:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,589:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,589:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,591:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,595:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,595:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,597:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,601:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,601:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,603:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,606:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,607:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,607:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,609:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,612:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,613:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,613:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,615:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,618:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,619:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,619:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,620:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,624:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,625:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,625:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,627:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,631:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,631:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,632:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,633:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,637:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,637:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,638:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,640:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,643:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,643:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,644:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,645:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,648:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,649:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,649:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,651:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,654:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,654:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,655:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,656:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,660:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,661:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,663:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,666:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,671:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,672:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,674:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,677:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,682:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,684:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,685:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,689:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,694:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,695:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,697:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,700:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,704:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,705:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,705:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,707:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,711:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,712:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,712:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,714:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,717:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,717:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,718:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,720:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,723:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,723:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,724:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,725:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,728:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,729:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,729:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,730:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,733:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,734:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,734:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,736:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,739:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,740:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,740:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,742:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,745:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,745:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,746:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,747:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,750:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,751:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,751:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,753:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,756:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,758:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,759:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,763:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,768:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,770:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,771:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,775:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,779:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,781:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,783:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,786:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,790:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,791:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,791:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,793:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,797:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,798:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,798:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,800:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,804:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,804:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,805:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,806:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,810:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,812:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,813:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,816:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,821:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,823:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,824:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,828:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,833:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,835:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,837:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,840:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,845:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,848:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,850:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,853:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,857:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,859:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,860:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,861:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,865:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,866:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,866:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,868:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,872:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,873:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,873:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,875:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,877:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,878:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,878:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,880:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,883:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,884:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,884:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,885:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,888:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,889:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,889:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,890:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,894:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,894:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,894:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,896:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,899:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,900:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,900:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,902:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,905:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,905:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,906:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,907:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,910:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,911:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,911:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,913:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,916:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,917:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,917:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,919:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,922:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,923:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,923:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,925:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,928:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,928:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,929:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:02,942:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:02,947:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:02,947:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:02,947:DEBUG:
    Ignoring line no. 24: 35
    


.. parsed-literal::

    6.95 ms ± 416 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)


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

    2018-09-05 14:08:04,284:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:04,289:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:04,291:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:04,292:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:04,293:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:04,294:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:04,350:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:04,355:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:04,356:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:04,358:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:04,360:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:04,361:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:04,413:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:04,416:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:04,417:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:04,417:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:04,417:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:04,418:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:04,461:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:04,465:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:04,466:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:04,467:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:04,469:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:04,470:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:04,522:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:04,526:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:04,526:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:04,527:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:04,527:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:04,528:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:04,574:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:04,577:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:04,578:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:04,578:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:04,579:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:04,580:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:04,623:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:04,627:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:04,628:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:04,629:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:04,632:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:04,633:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:04,682:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:04,685:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:04,685:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:04,686:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:04,687:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:04,687:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:04,729:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:04,733:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:04,733:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:04,734:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:04,734:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:04,735:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:04,780:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:04,785:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:04,786:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:04,788:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:04,789:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:04,791:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:04,843:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:04,846:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:04,847:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:04,847:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:04,848:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:04,848:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:04,894:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:04,898:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:04,899:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:04,899:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:04,899:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:04,900:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:04,952:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:04,956:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:04,957:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:04,957:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:04,958:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:04,959:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,004:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,012:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,012:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,013:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,013:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,014:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,057:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,061:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,061:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,062:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,063:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,063:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,107:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,110:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,111:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,112:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,112:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,113:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,156:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,160:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,161:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,162:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,163:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,163:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,209:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,213:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,213:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,213:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,214:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,214:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,260:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,264:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,264:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,265:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,265:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,266:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,325:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,330:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,332:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,333:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,333:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,334:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,398:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,402:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,402:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,402:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,403:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,403:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,449:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,453:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,454:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,454:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,455:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,455:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,498:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,502:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,503:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,503:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,503:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,504:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,547:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,551:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,551:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,552:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,552:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,553:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,599:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,603:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,604:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,604:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,605:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,605:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,650:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,655:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,658:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,659:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,661:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,662:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,713:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,718:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,720:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,721:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,722:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,723:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,772:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,777:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,778:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,778:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,779:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,779:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,824:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,828:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,828:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,829:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,829:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,830:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,876:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,881:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,881:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,882:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,882:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,883:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,928:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,933:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,933:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,934:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,934:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,936:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:05,977:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:05,981:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:05,982:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:05,982:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:05,983:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:05,984:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,027:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,031:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,031:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,031:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,032:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,032:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,075:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,079:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,079:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,080:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,080:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,081:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,124:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,128:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,129:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,129:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,129:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,130:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,173:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,177:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,177:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,178:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,178:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,179:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,223:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,227:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,228:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,228:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,229:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,229:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,275:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,278:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,279:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,279:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,280:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,280:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,342:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,346:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,347:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,347:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,347:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,348:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,392:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,396:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,397:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,397:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,398:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,398:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,444:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,448:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,448:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,448:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,449:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,451:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,507:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,510:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,511:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,512:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,512:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,513:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,578:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,582:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,582:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,583:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,584:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,584:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,629:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,632:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,632:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,633:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,633:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,634:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,676:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,680:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,681:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,681:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,682:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,682:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,725:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,729:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,729:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,730:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,730:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,731:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,775:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,779:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,779:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,780:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,780:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,781:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,825:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,828:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,829:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,829:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,830:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,830:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,874:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,878:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,879:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,879:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,880:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,880:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,930:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:06,935:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:06,936:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:06,936:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:06,937:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:06,939:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:06,997:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,001:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,002:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,002:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,003:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,003:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,048:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,052:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,053:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,053:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,054:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,054:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,099:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,103:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,104:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,104:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,105:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,105:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,150:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,154:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,154:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,155:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,156:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,156:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,199:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,203:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,204:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,205:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,205:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,205:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,251:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,254:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,255:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,255:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,257:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,257:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,304:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,308:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,309:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,309:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,310:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,311:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,387:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,391:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,392:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,392:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,393:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,393:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,439:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,443:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,444:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,444:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,445:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,445:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,492:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,496:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,497:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,497:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,497:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,498:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,543:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,546:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,547:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,547:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,548:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,548:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,591:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,594:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,594:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,595:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,595:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,596:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,640:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,644:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,645:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,645:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,646:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,646:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,713:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,717:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,718:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,719:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,720:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,720:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,768:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,772:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,774:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,775:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,776:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,777:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,835:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,840:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,841:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,843:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,845:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,846:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,897:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,901:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,903:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,904:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,906:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,906:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:07,962:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:07,967:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:07,968:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:07,971:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:07,973:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:07,974:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:08,031:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:08,034:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:08,035:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:08,035:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:08,036:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:08,036:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:08,081:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:08,084:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:08,085:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:08,085:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:08,086:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:08,086:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:08,131:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:08,135:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:08,136:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:08,138:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:08,140:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:08,141:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:08,203:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:08,207:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:08,208:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:08,208:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:08,209:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:08,209:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:08,252:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:08,256:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:08,256:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:08,257:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:08,257:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:08,258:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:08,301:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:08,304:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:08,305:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:08,305:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:08,306:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:08,307:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:08,351:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:08,355:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:08,356:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:08,357:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:08,357:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:08,357:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:08,416:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:08,420:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:08,422:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:08,424:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:08,425:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:08,427:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:08,498:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:08,502:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:08,502:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:08,503:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:08,503:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:08,504:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:08,548:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:08,552:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:08,553:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:08,553:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:08,554:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:08,554:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:08,597:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:08,601:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:08,602:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:08,602:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:08,603:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:08,603:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:08,646:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:08,650:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:08,652:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:08,653:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:08,655:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:08,656:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:08,710:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:08,714:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:08,714:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:08,715:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:08,715:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:08,716:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    55.2 ms ± 2.68 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


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

    2018-09-05 14:08:08,981:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:08,985:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:08,986:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:08,986:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:08,987:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:08,987:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,041:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,045:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,045:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,045:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,046:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,046:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,099:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,102:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,103:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,103:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,104:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,104:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,156:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,160:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,161:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,161:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,161:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,162:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,216:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,220:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,221:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,221:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,222:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,222:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,279:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,283:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,284:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,284:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,284:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,285:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,338:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,342:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,344:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,345:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,346:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,347:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,427:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,431:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,432:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,432:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,433:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,433:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,490:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,494:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,494:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,494:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,495:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,495:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,547:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,551:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,551:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,552:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,552:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,552:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,605:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,609:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,609:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,610:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,611:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,611:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,668:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,672:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,673:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,673:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,674:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,674:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,729:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,733:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,734:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,734:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,735:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,735:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,792:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,796:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,796:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,797:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,798:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,798:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,854:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,858:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,858:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,858:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,859:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,860:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,913:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,917:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,919:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,920:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,921:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,922:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:09,991:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:09,996:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:09,997:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:09,997:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:09,997:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:09,998:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,054:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,058:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,059:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,059:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,059:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,060:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,112:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,117:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,117:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,118:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,118:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,119:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,172:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,176:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,177:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,177:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,177:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,178:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,246:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,250:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,251:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,251:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,252:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,252:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,304:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,309:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,309:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,310:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,310:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,311:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,362:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,366:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,367:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,367:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,367:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,368:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,440:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,444:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,444:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,445:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,446:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,446:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,509:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,513:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,513:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,513:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,514:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,514:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,567:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,570:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,571:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,571:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,572:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,572:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,623:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,626:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,627:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,627:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,628:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,628:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,680:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,684:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,685:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,685:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,686:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,686:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,737:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,742:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,743:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,745:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,746:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,747:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,807:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,811:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,811:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,812:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,812:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,813:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,873:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,877:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,878:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,878:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,879:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,879:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:10,937:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:10,941:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:10,943:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:10,944:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:10,946:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:10,947:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,011:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,014:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,015:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,015:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,016:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,016:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,071:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,075:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,077:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,079:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,080:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,081:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,142:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,147:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,149:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,150:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,151:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,152:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,215:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,218:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,219:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,219:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,220:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,220:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,276:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,279:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,280:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,280:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,281:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,281:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,338:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,342:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,343:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,343:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,344:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,344:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,401:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,404:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,405:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,405:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,406:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,406:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,477:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,480:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,481:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,481:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,482:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,482:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,537:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,541:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,541:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,542:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,542:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,543:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,594:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,598:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,599:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,599:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,600:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,600:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,652:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,656:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,657:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,657:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,658:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,658:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,713:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,717:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,719:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,720:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,721:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,722:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,782:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,785:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,785:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,786:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,786:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,787:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,844:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,848:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,849:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,849:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,850:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,850:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,901:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,905:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,907:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,908:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,910:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,911:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:11,978:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:11,982:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:11,984:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:11,985:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:11,986:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:11,987:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,047:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,050:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,051:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,051:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,052:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,052:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,106:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,110:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,110:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,111:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,112:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,112:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,163:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,167:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,167:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,168:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,168:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,170:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,221:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,225:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,226:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,226:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,226:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,227:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,281:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,285:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,286:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,286:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,287:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,287:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,339:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,342:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,343:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,343:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,344:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,344:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,396:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,400:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,401:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,401:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,402:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,402:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,459:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,463:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,464:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,464:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,465:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,465:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,537:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,540:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,541:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,541:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,542:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,542:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,594:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,597:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,598:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,598:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,599:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,599:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,651:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,655:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,656:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,656:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,657:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,657:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,708:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,712:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,712:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,713:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,713:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,714:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,766:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,769:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,770:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,770:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,771:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,771:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,822:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,825:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,826:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,826:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,827:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,827:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,878:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,881:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,882:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,882:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,882:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,883:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,935:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,938:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,939:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:12,939:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:12,940:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:12,940:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:12,995:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:12,999:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:12,999:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,000:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,000:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,001:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,055:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,058:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,059:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,059:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,060:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,060:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,114:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,118:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,118:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,119:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,119:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,119:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,174:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,177:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,178:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,178:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,179:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,180:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,235:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,240:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,241:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,241:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,241:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,243:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,300:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,305:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,305:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,305:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,306:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,306:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,358:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,362:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,364:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,365:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,368:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,369:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,431:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,435:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,436:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,436:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,437:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,437:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,494:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,498:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,499:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,499:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,499:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,500:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,570:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,573:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,574:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,574:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,575:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,576:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,628:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,632:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,633:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,633:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,634:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,635:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,686:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,690:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,691:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,691:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,692:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,692:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,756:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,761:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,761:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,762:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,762:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,762:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,814:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,817:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,818:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,819:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,819:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,820:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,871:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,874:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,875:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,875:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,876:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,876:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,928:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,932:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,932:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,933:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,933:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,934:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    
    2018-09-05 14:08:13,990:INFO:
    Reading NASA Ames file:
    /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20080101000000.20160708144500.nephelometer..aerosol.1y.1h.DE09L_tsi_neph_3563.DE09L_nephelometer.lev2.nas
    2018-09-05 14:08:13,994:WARNING:
    Failed to read header row 6.
    2008 01 01 2016 07 08
    
    Error msg: IndexError('list index out of range',)
    2018-09-05 14:08:13,995:DEBUG:
    Ignoring line no. 23: 0
    
    2018-09-05 14:08:13,996:DEBUG:
    Ignoring line no. 24: 35
    
    2018-09-05 14:08:13,996:DEBUG:
    REACHED DATA BLOCK
    2018-09-05 14:08:13,996:DEBUG:
      0.000000   0.041667 999.999 999.999 999.999 9999.999 9999.999 9999.999 9999 999.9 9999.9 0.394999000
    


.. parsed-literal::

    62.6 ms ± 1.74 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

