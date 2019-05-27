
Tutorial showing how to read EBAS NASA Ames files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This low-level tutorial shows how to read an EBAS NASA Ames file using
the class
`EbasNasaAmesFile <https://pyaerocom.met.no/api.html?highlight=ebasnasaamesfile#pyaerocom.io.ebas_nasa_ames.EbasNasaAmesFile>`__
of pyaerocom and how to access the import data and metadata.

**NOTE**: variable names and names of metadata attributes below use the
EBAS conventions and **not the AeroCom naming conventions**, since the
purpose of the ``EbasNasaAmesFile`` reading routine is to solely import
the content of the original data files (provided by EBAS) into a python
interface. If you intend to use EBAS data for AeroCom purposes
(e.g. model intercomparison), please use the
`ReadEbas <https://pyaerocom.met.no/api.html?highlight=readebas#pyaerocom.io.read_ebas.ReadEbas>`__
routine (or the
`ReadUngridded <https://pyaerocom.met.no/api.html?highlight=readebas#module-pyaerocom.io.readungridded>`__
factory class) which is doing the mapping to AeroCom naming conventions.

Please see
`here <https://ebas-submit.nilu.no/Submit-Data/Getting-started>`__ for
information related to the EBAS NASA Ames file format.

.. code:: ipython3

    import pyaerocom as pya
    import glob


.. parsed-literal::

    Initating pyaerocom configuration
    Checking database access...
    Checking access to: /lustre/storeA
    Access to lustre database: True
    Init data paths for lustre
    Expired time: 0.019 s


.. code:: ipython3

    ebasdir = pya.const.EBASMC_DATA_DIR
    ebasdir




.. parsed-literal::

    '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/'



.. code:: ipython3

    files = glob.glob('{}DE0043G*2010*nephelometer*lev2.nas'.format(ebasdir))

.. code:: ipython3

    print('No. of files found: {}'.format(len(files)))


.. parsed-literal::

    No. of files found: 2


.. code:: ipython3

    files[0]




.. parsed-literal::

    '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data/data/DE0043G.20100201000000.20150304123917.nephelometer..pm10.11mo.1h.DE09L_TSI_Neph_3563.DE09L_scatt_NEPH.lev2.nas'



Read the first file that was found:

.. code:: ipython3

    mc = pya.io.EbasNasaAmesFile(file=files[0],
                                 only_head=False,          #set True if you only want to import header
                                 replace_invalid_nan=True, #replace invalid values with NaNs
                                 convert_timestamps=True,  #compute datetime64 timestamps from numerical values
                                 decode_flags=True)        #decode all flags (e.g. 0.111222333 -> 111 222 333)
                                 
    print(mc)


.. parsed-literal::

    Pyaerocom EbasNasaAmesFile
    --------------------------
    
       num_head_lines: 91
       num_head_fmt: 1001
       data_originator: Flentje, Harald
       sponsor_organisation: DE09L, Deutscher Wetterdienst, DWD, Met. Obs., Hohenspeissenberg, , 82283, Hohenspeissenberg, Germany
       submitter: Flentje, Harald
       project_association: ACTRIS EMEP GAW-WDCA
       vol_num: 1
       vol_totnum: 1
       ref_date: 2010-01-01T00:00:00
       revision_date: 2015-03-04T00:00:00
       freq: 0.041667
       descr_time_unit: days from file reference point
       num_cols_dependent: 23
       mul_factors (list, 23 items)
       [1.0
        1.0
        ...
        1.0
        1.0]
    
       vals_invalid (list, 23 items)
       [999.999999
        9999.0
        ...
        9999.999999
        9.999]
    
       descr_first_col: end_time of measurement, days from the file reference point
    
       Column variable definitions
       -------------------------------
       EbasColDef: name=starttime, unit=days, is_var=False, is_flag=False, flag_col=23, 
       EbasColDef: name=endtime, unit=days, is_var=False, is_flag=False, flag_col=23, 
       EbasColDef: name=pressure, unit=hPa, is_var=True, is_flag=False, flag_col=23, location=instrument internal, statistics=arithmetic mean, matrix=instrument, detection_limit=, detection_limit_expl.=, measurement_uncertainty=, measurement_uncertainty_expl.=, 
       EbasColDef: name=relative_humidity, unit=%, is_var=True, is_flag=False, flag_col=23, location=instrument internal, statistics=arithmetic mean, matrix=instrument, detection_limit=, detection_limit_expl.=, measurement_uncertainty=, measurement_uncertainty_expl.=, 
       EbasColDef: name=temperature, unit=K, is_var=True, is_flag=False, flag_col=23, location=instrument internal, statistics=arithmetic mean, matrix=instrument, detection_limit=, detection_limit_expl.=, measurement_uncertainty=, measurement_uncertainty_expl.=, 
       EbasColDef: name=aerosol_light_backscattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=450.0 nm, statistics=arithmetic mean, 
       EbasColDef: name=aerosol_light_backscattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=450.0 nm, statistics=percentile:15.87, 
       EbasColDef: name=aerosol_light_backscattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=450.0 nm, statistics=percentile:84.13, 
       EbasColDef: name=aerosol_light_backscattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=550.0 nm, statistics=arithmetic mean, 
       EbasColDef: name=aerosol_light_backscattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=550.0 nm, statistics=percentile:15.87, 
       EbasColDef: name=aerosol_light_backscattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=550.0 nm, statistics=percentile:84.13, 
       EbasColDef: name=aerosol_light_backscattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=700.0 nm, statistics=arithmetic mean, 
       EbasColDef: name=aerosol_light_backscattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=700.0 nm, statistics=percentile:15.87, 
       EbasColDef: name=aerosol_light_backscattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=700.0 nm, statistics=percentile:84.13, 
       EbasColDef: name=aerosol_light_scattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=450.0 nm, statistics=arithmetic mean, 
       EbasColDef: name=aerosol_light_scattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=450.0 nm, statistics=percentile:15.87, 
       EbasColDef: name=aerosol_light_scattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=450.0 nm, statistics=percentile:84.13, 
       EbasColDef: name=aerosol_light_scattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=550.0 nm, statistics=arithmetic mean, 
       EbasColDef: name=aerosol_light_scattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=550.0 nm, statistics=percentile:15.87, 
       EbasColDef: name=aerosol_light_scattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=550.0 nm, statistics=percentile:84.13, 
       EbasColDef: name=aerosol_light_scattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=700.0 nm, statistics=arithmetic mean, 
       EbasColDef: name=aerosol_light_scattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=700.0 nm, statistics=percentile:15.87, 
       EbasColDef: name=aerosol_light_scattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=700.0 nm, statistics=percentile:84.13, 
       EbasColDef: name=numflag, unit=no unit, is_var=False, is_flag=True, flag_col=None, 
    
       EBAS meta data
       ------------------
       decode_flags: True
       data_definition: EBAS_1.1
       set_type_code: TU
       timezone: UTC
       file_name: DE0043G.20100201000000.20150304123917.nephelometer..pm10.11mo.1h.DE09L_TSI_Neph_3563.DE09L_scatt_NEPH.lev2.nas
       file_creation: 20190320041619
       startdate: 20100201000000
       revision_date: 20150304123917
       version: 1
       version_description: initial revision
       data_level: 2
       period_code: 11mo
       resolution_code: 1h
       sample_duration: 1h
       orig._time_res.: 10mn
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
       measurement_height: 15.0 m
       regime: IMG
       component: 
       unit: 1/Mm
       matrix: pm10
       laboratory_code: DE09L
       instrument_type: nephelometer
       instrument_name: TSI_Neph_3563
       instrument_manufacturer: TSI
       instrument_model: 3563
       method_ref: DE09L_scatt_NEPH
       standard_method: cal-gas=CO2+AIR_truncation-correction=Anderson1998
       inlet_type: Impactor--direct
       inlet_description: PM10 at ambient humidity inlet, Digitel, flow 170 l/min
       humidity/temperature_control: Nafion dryer
       volume_std._temperature: 273.15 K
       volume_std._pressure: 1013.25 hPa
       detection_limit: 0.3 1/Mm
       detection_limit_expl.: Determined only by instrument counting statistics, no detection limit flag used
       measurement_uncertainty: 0.3 1/Mm
       measurement_uncertainty_expl.: Determined only by instrument counting statistics, no detection limit flag used
       zero/negative_values: Zero values may appear due to statistical variations at very low concentrations
       originator: Flentje, Harald, Harald.Flentje@dwd.de, , , , , , , ,
       submitter: Flentje, Harald, Harald.Flentje@dwd.de, , , , , , , ,
       acknowledgement: Request acknowledgement details from data originator
       comment: Angstrom-based Anderson & Ogren 1998 corr used for truncation correction
    
       Data
       --------
    [[3.10000000e+01 3.10416660e+01            nan ...            nan
                 nan 9.99000000e-01]
     [3.10416670e+01 3.10833330e+01            nan ...            nan
                 nan 9.99000000e-01]
     [3.10833330e+01 3.11249990e+01            nan ...            nan
                 nan 9.99000000e-01]
     ...
     [3.64875000e+02 3.64916666e+02 9.04000000e+02 ... 1.35433110e+01
      1.62446480e+01 1.00000000e-01]
     [3.64916667e+02 3.64958333e+02 9.04000000e+02 ... 1.13367710e+01
      1.42932090e+01 1.00000000e-01]
     [3.64958333e+02 3.64999999e+02 9.03000000e+02 ... 1.13635590e+01
      1.40839410e+01 1.00000000e-01]]
    Colnum: 24
    Timestamps: 8016


The NASA Ames files are strucured in the same way as they are
represented by in the instance of the EbasNasaAmesFile class.

-  A header with global metadata
-  One row that specifies multiplication factors for each data column
   (``mul_factors``)
-  One row that specifies NaN-equivalent values for each data column
   (``vals_invalid``)
-  A number of rows specifying metainformation for each data column in
   the file (i.e. 12 rows, if the data has 12 columns)
-  Dataset specific metadata
-  Data block: rows are timestamps, columns are different columns
   specified in the header (cf. 2 points above)

   -  Represented by 2D numpy array (``data`` attribute) where first
      index is row and second index is column

For details related to the file format `see
here <https://ebas-submit.nilu.no/Submit-Data/Data-Reporting/Templates/Category/Aerosol/Aerosol-Optical-Depth>`__.

.. code:: ipython3

    print(mc.shape)


.. parsed-literal::

    (8016, 24)


Data array
^^^^^^^^^^

The data is imported as a 2D numpy array which is accessible via the
``data`` attribute:

.. code:: ipython3

    mc.data




.. parsed-literal::

    array([[3.10000000e+01, 3.10416660e+01,            nan, ...,
                       nan,            nan, 9.99000000e-01],
           [3.10416670e+01, 3.10833330e+01,            nan, ...,
                       nan,            nan, 9.99000000e-01],
           [3.10833330e+01, 3.11249990e+01,            nan, ...,
                       nan,            nan, 9.99000000e-01],
           ...,
           [3.64875000e+02, 3.64916666e+02, 9.04000000e+02, ...,
            1.35433110e+01, 1.62446480e+01, 1.00000000e-01],
           [3.64916667e+02, 3.64958333e+02, 9.04000000e+02, ...,
            1.13367710e+01, 1.42932090e+01, 1.00000000e-01],
           [3.64958333e+02, 3.64999999e+02, 9.03000000e+02, ...,
            1.13635590e+01, 1.40839410e+01, 1.00000000e-01]])



The first index corresponds to the individual measurements (rows in
file) and the second index corresponds to the individual columns that
are stored in the file.

Column information
^^^^^^^^^^^^^^^^^^

Detailed information about each column can be accessed via the
``var_defs`` attribute, the first two columns are always the start and
stop timestamps:

.. code:: ipython3

    mc.var_defs[0]




.. parsed-literal::

    EbasColDef: name=starttime, unit=days, is_var=False, is_flag=False, flag_col=23, 



.. code:: ipython3

    mc.var_defs[1]




.. parsed-literal::

    EbasColDef: name=endtime, unit=days, is_var=False, is_flag=False, flag_col=23, 



After the start / stop columns follow the individual data columns.

.. code:: ipython3

    mc.var_defs[2]




.. parsed-literal::

    EbasColDef: name=pressure, unit=hPa, is_var=True, is_flag=False, flag_col=23, location=instrument internal, statistics=arithmetic mean, matrix=instrument, detection_limit=, detection_limit_expl.=, measurement_uncertainty=, measurement_uncertainty_expl.=, 



.. code:: ipython3

    mc.var_defs[3]




.. parsed-literal::

    EbasColDef: name=relative_humidity, unit=%, is_var=True, is_flag=False, flag_col=23, location=instrument internal, statistics=arithmetic mean, matrix=instrument, detection_limit=, detection_limit_expl.=, measurement_uncertainty=, measurement_uncertainty_expl.=, 



.. code:: ipython3

    mc.var_defs[4]




.. parsed-literal::

    EbasColDef: name=temperature, unit=K, is_var=True, is_flag=False, flag_col=23, location=instrument internal, statistics=arithmetic mean, matrix=instrument, detection_limit=, detection_limit_expl.=, measurement_uncertainty=, measurement_uncertainty_expl.=, 



.. code:: ipython3

    mc.var_defs[5]




.. parsed-literal::

    EbasColDef: name=aerosol_light_backscattering_coefficient, unit=1/Mm, is_var=True, is_flag=False, flag_col=23, wavelength=450.0 nm, statistics=arithmetic mean, 



In addition to the data columns in the files (such as time stamps, or
measured values of a certain variable) there is **at least one** flag
column in the data array and each data column has assigned one flag
column (cf. output above where the index of the flag column for each
data column is provided ``flag_col=23``, i.e. column 23 is the flag
column assigned to each of the 5 data columns that were displayed
exemplary above:

.. code:: ipython3

    mc.var_defs[23]




.. parsed-literal::

    EbasColDef: name=numflag, unit=no unit, is_var=False, is_flag=True, flag_col=None, 



The ``is_var`` attribute specifies, whether this column contains actual
variable data or if it is a flag column. A NASA Ames file can have one
or more flag columns that can be used to identify valid or invalid
measurments. Each flag in a flag column comprises a floating point
number that has encoded up to 3 3-digit numerical flags which are
specified here:

https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/ebas_flags.csv

More info about the flags follows below. You can see, that the column 4
printed above has assigned column 12 (index 11) as flag column.

If you want to see an overview of all available columns in the file you
may use the following command:

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
    flag_col: 23
    
    Column 1
    Pyaerocom EbasColDef
    --------------------
    name: endtime
    unit: days
    is_var: False
    is_flag: False
    flag_col: 23
    
    Column 2
    Pyaerocom EbasColDef
    --------------------
    name: pressure
    unit: hPa
    is_var: True
    is_flag: False
    flag_col: 23
    location: instrument internal
    statistics: arithmetic mean
    matrix: instrument
    detection_limit: 
    detection_limit_expl.: 
    measurement_uncertainty: 
    measurement_uncertainty_expl.: 
    
    Column 3
    Pyaerocom EbasColDef
    --------------------
    name: relative_humidity
    unit: %
    is_var: True
    is_flag: False
    flag_col: 23
    location: instrument internal
    statistics: arithmetic mean
    matrix: instrument
    detection_limit: 
    detection_limit_expl.: 
    measurement_uncertainty: 
    measurement_uncertainty_expl.: 
    
    Column 4
    Pyaerocom EbasColDef
    --------------------
    name: temperature
    unit: K
    is_var: True
    is_flag: False
    flag_col: 23
    location: instrument internal
    statistics: arithmetic mean
    matrix: instrument
    detection_limit: 
    detection_limit_expl.: 
    measurement_uncertainty: 
    measurement_uncertainty_expl.: 
    
    Column 5
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_backscattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 450.0 nm
    statistics: arithmetic mean
    
    Column 6
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_backscattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 450.0 nm
    statistics: percentile:15.87
    
    Column 7
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_backscattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 450.0 nm
    statistics: percentile:84.13
    
    Column 8
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_backscattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 550.0 nm
    statistics: arithmetic mean
    
    Column 9
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_backscattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 550.0 nm
    statistics: percentile:15.87
    
    Column 10
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_backscattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 550.0 nm
    statistics: percentile:84.13
    
    Column 11
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_backscattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 700.0 nm
    statistics: arithmetic mean
    
    Column 12
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_backscattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 700.0 nm
    statistics: percentile:15.87
    
    Column 13
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_backscattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 700.0 nm
    statistics: percentile:84.13
    
    Column 14
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_scattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 450.0 nm
    statistics: arithmetic mean
    
    Column 15
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_scattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 450.0 nm
    statistics: percentile:15.87
    
    Column 16
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_scattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 450.0 nm
    statistics: percentile:84.13
    
    Column 17
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_scattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 550.0 nm
    statistics: arithmetic mean
    
    Column 18
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_scattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 550.0 nm
    statistics: percentile:15.87
    
    Column 19
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_scattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 550.0 nm
    statistics: percentile:84.13
    
    Column 20
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_scattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 700.0 nm
    statistics: arithmetic mean
    
    Column 21
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_scattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 700.0 nm
    statistics: percentile:15.87
    
    Column 22
    Pyaerocom EbasColDef
    --------------------
    name: aerosol_light_scattering_coefficient
    unit: 1/Mm
    is_var: True
    is_flag: False
    flag_col: 23
    wavelength: 700.0 nm
    statistics: percentile:84.13
    
    Column 23
    Pyaerocom EbasColDef
    --------------------
    name: numflag
    unit: no unit
    is_var: False
    is_flag: True
    flag_col: None
    


You can see that all variable columns were assigned the same flag
column, since there is only one flag column at the end (index 23). This
would be different if there were multiple flag columns (e.g. one for
each variable).

Access flag information
^^^^^^^^^^^^^^^^^^^^^^^

You can access the flags for each column using the ``flag_col_info``
attribute of the file (and the key of the respective flag column, that
you want to access, here->11).

.. code:: ipython3

    flagcol = mc.flag_col_info[23]
    flagcol




.. parsed-literal::

    <pyaerocom.io.ebas_nasa_ames.EbasFlagCol at 0x7fa85f47f4e0>



The raw flags can be accessed via:

.. code:: ipython3

    flagcol.raw_data




.. parsed-literal::

    array([0.999, 0.999, 0.999, ..., 0.1  , 0.1  , 0.1  ])



And the processed flags are in stored in a (Nx3) numpy array where N is
the total number of timestamps.

.. code:: ipython3

    flagcol.decoded




.. parsed-literal::

    array([[999,   0,   0],
           [999,   0,   0],
           [999,   0,   0],
           ...,
           [100,   0,   0],
           [100,   0,   0],
           [100,   0,   0]])



For instance, access the flags of the 5 timestamp:

.. code:: ipython3

    flagcol.decoded[4]




.. parsed-literal::

    array([999,   0,   0])



This timestamp contains 1 (of the possible up to 3) flags: 999.

Validity of a combination of the flags can be directly accessed via:

.. code:: ipython3

    flagcol.valid[4]




.. parsed-literal::

    False



This flag (999) evaluates to an invalid measurement. Looking into `the
flag definition
file <https://github.com/metno/pyaerocom/blob/master/pyaerocom/data/ebas_flags.csv>`__
we see that these two flags have the following meaning:

-  999,‘Missing measurement, unspecified reason’,‘M’

where the last string specifies if this flag is valid (V) or invalid (I)
or missing (M).

Convert object to pandas Dataframe
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    df = mc.to_dataframe()
    df.head()




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
          <th>starttime_days</th>
          <th>endtime_days</th>
          <th>pressure_hPa_instrument_arithmetic mean</th>
          <th>relative_humidity_%_instrument_arithmetic mean</th>
          <th>temperature_K_instrument_arithmetic mean</th>
          <th>aerosol_light_backscattering_coefficient_1/Mm_450.0nm_arithmetic mean</th>
          <th>aerosol_light_backscattering_coefficient_1/Mm_450.0nm_percentile:15.87</th>
          <th>aerosol_light_backscattering_coefficient_1/Mm_450.0nm_percentile:84.13</th>
          <th>aerosol_light_backscattering_coefficient_1/Mm_550.0nm_arithmetic mean</th>
          <th>aerosol_light_backscattering_coefficient_1/Mm_550.0nm_percentile:15.87</th>
          <th>...</th>
          <th>aerosol_light_scattering_coefficient_1/Mm_450.0nm_arithmetic mean</th>
          <th>aerosol_light_scattering_coefficient_1/Mm_450.0nm_percentile:15.87</th>
          <th>aerosol_light_scattering_coefficient_1/Mm_450.0nm_percentile:84.13</th>
          <th>aerosol_light_scattering_coefficient_1/Mm_550.0nm_arithmetic mean</th>
          <th>aerosol_light_scattering_coefficient_1/Mm_550.0nm_percentile:15.87</th>
          <th>aerosol_light_scattering_coefficient_1/Mm_550.0nm_percentile:84.13</th>
          <th>aerosol_light_scattering_coefficient_1/Mm_700.0nm_arithmetic mean</th>
          <th>aerosol_light_scattering_coefficient_1/Mm_700.0nm_percentile:15.87</th>
          <th>aerosol_light_scattering_coefficient_1/Mm_700.0nm_percentile:84.13</th>
          <th>numflag_no unit</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2010-02-01 00:29:59</th>
          <td>31.000000</td>
          <td>31.041666</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.999</td>
        </tr>
        <tr>
          <th>2010-02-01 01:29:59</th>
          <td>31.041667</td>
          <td>31.083333</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.999</td>
        </tr>
        <tr>
          <th>2010-02-01 02:29:59</th>
          <td>31.083333</td>
          <td>31.124999</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.999</td>
        </tr>
        <tr>
          <th>2010-02-01 03:29:59</th>
          <td>31.125000</td>
          <td>31.166666</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.999</td>
        </tr>
        <tr>
          <th>2010-02-01 04:29:59</th>
          <td>31.166667</td>
          <td>31.208333</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>...</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.999</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 24 columns</p>
    </div>



You may also apply selection constraints when converting to a DataFrame
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: ipython3

    scattering = mc.to_dataframe('aerosol_light_scattering_coefficient', statistics='arithmetic mean')
    scattering




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
          <th>aerosol_light_scattering_coefficient_1/Mm_450.0nm_arithmetic mean</th>
          <th>aerosol_light_scattering_coefficient_1/Mm_550.0nm_arithmetic mean</th>
          <th>aerosol_light_scattering_coefficient_1/Mm_700.0nm_arithmetic mean</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>2010-02-01 00:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 01:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 02:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 03:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 04:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 05:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 06:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 07:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 08:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 09:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 10:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 11:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 12:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 13:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 14:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 15:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 16:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 17:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 18:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 19:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 20:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 21:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 22:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-01 23:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-02 00:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-02 01:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-02 02:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-02 03:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-02 04:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>2010-02-02 05:29:59</th>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>2010-12-30 18:29:59</th>
          <td>53.430790</td>
          <td>35.308300</td>
          <td>20.360300</td>
        </tr>
        <tr>
          <th>2010-12-30 19:29:59</th>
          <td>36.300732</td>
          <td>23.530550</td>
          <td>14.807830</td>
        </tr>
        <tr>
          <th>2010-12-30 20:29:59</th>
          <td>35.503689</td>
          <td>22.803770</td>
          <td>12.677280</td>
        </tr>
        <tr>
          <th>2010-12-30 21:29:59</th>
          <td>33.409031</td>
          <td>21.931190</td>
          <td>12.509151</td>
        </tr>
        <tr>
          <th>2010-12-30 22:29:59</th>
          <td>32.129929</td>
          <td>21.236471</td>
          <td>12.093370</td>
        </tr>
        <tr>
          <th>2010-12-30 23:29:59</th>
          <td>28.423731</td>
          <td>18.567791</td>
          <td>10.626820</td>
        </tr>
        <tr>
          <th>2010-12-31 00:29:59</th>
          <td>41.814079</td>
          <td>27.366261</td>
          <td>15.529949</td>
        </tr>
        <tr>
          <th>2010-12-31 01:29:59</th>
          <td>30.993240</td>
          <td>20.264280</td>
          <td>11.713341</td>
        </tr>
        <tr>
          <th>2010-12-31 02:29:59</th>
          <td>29.103260</td>
          <td>19.418760</td>
          <td>11.360280</td>
        </tr>
        <tr>
          <th>2010-12-31 03:29:59</th>
          <td>22.745249</td>
          <td>15.086280</td>
          <td>8.639771</td>
        </tr>
        <tr>
          <th>2010-12-31 04:29:59</th>
          <td>23.487450</td>
          <td>15.794790</td>
          <td>9.212736</td>
        </tr>
        <tr>
          <th>2010-12-31 05:29:59</th>
          <td>16.424900</td>
          <td>11.154480</td>
          <td>6.603766</td>
        </tr>
        <tr>
          <th>2010-12-31 06:29:59</th>
          <td>13.479550</td>
          <td>9.255769</td>
          <td>5.481015</td>
        </tr>
        <tr>
          <th>2010-12-31 07:29:59</th>
          <td>17.258570</td>
          <td>11.956240</td>
          <td>8.506770</td>
        </tr>
        <tr>
          <th>2010-12-31 08:29:59</th>
          <td>12.597250</td>
          <td>8.628826</td>
          <td>5.281767</td>
        </tr>
        <tr>
          <th>2010-12-31 09:29:59</th>
          <td>15.833030</td>
          <td>10.717130</td>
          <td>6.477723</td>
        </tr>
        <tr>
          <th>2010-12-31 10:29:59</th>
          <td>14.618210</td>
          <td>9.979239</td>
          <td>5.987522</td>
        </tr>
        <tr>
          <th>2010-12-31 11:29:59</th>
          <td>15.715250</td>
          <td>10.630589</td>
          <td>6.477187</td>
        </tr>
        <tr>
          <th>2010-12-31 12:29:59</th>
          <td>25.136570</td>
          <td>17.360041</td>
          <td>10.710710</td>
        </tr>
        <tr>
          <th>2010-12-31 13:29:59</th>
          <td>29.165520</td>
          <td>20.273100</td>
          <td>12.399899</td>
        </tr>
        <tr>
          <th>2010-12-31 14:29:59</th>
          <td>26.211281</td>
          <td>18.200649</td>
          <td>11.271250</td>
        </tr>
        <tr>
          <th>2010-12-31 15:29:59</th>
          <td>38.909950</td>
          <td>26.989658</td>
          <td>16.587891</td>
        </tr>
        <tr>
          <th>2010-12-31 16:29:59</th>
          <td>31.470299</td>
          <td>21.862089</td>
          <td>13.784870</td>
        </tr>
        <tr>
          <th>2010-12-31 17:29:59</th>
          <td>18.475222</td>
          <td>12.039280</td>
          <td>7.012848</td>
        </tr>
        <tr>
          <th>2010-12-31 18:29:59</th>
          <td>32.092010</td>
          <td>21.740810</td>
          <td>13.151670</td>
        </tr>
        <tr>
          <th>2010-12-31 19:29:59</th>
          <td>29.312950</td>
          <td>19.707840</td>
          <td>13.096900</td>
        </tr>
        <tr>
          <th>2010-12-31 20:29:59</th>
          <td>28.166000</td>
          <td>19.270330</td>
          <td>11.515220</td>
        </tr>
        <tr>
          <th>2010-12-31 21:29:59</th>
          <td>36.854919</td>
          <td>25.116589</td>
          <td>14.893980</td>
        </tr>
        <tr>
          <th>2010-12-31 22:29:59</th>
          <td>30.724499</td>
          <td>21.249210</td>
          <td>12.814990</td>
        </tr>
        <tr>
          <th>2010-12-31 23:29:59</th>
          <td>28.431919</td>
          <td>20.387381</td>
          <td>12.723750</td>
        </tr>
      </tbody>
    </table>
    <p>8016 rows × 3 columns</p>
    </div>



.. code:: ipython3

    scattering.plot(figsize=(16,8))




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x7fa85ede8da0>




.. image:: add02_read_ebas_nasa_ames/add02_read_ebas_nasa_ames_40_1.png

