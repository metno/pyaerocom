
Getting started
~~~~~~~~~~~~~~~

This notebook gives an introduction on how to install pyaerocom and run
it on your local machine.

Requirements
^^^^^^^^^^^^

Before installation please make sure you have all required dependencies
installed (`see here for a list of
dependencies <http://aerocom.met.no/pyaerocom/readme.html#requirements>`__).

Installation
^^^^^^^^^^^^

Please download and unzip the `pyaerocom GitHub
repository <https://github.com/metno/pyaerocom>`__ or clone it using

``$ git clone https://github.com/metno/pyaerocom.git``

into a local directory of your choice. Then, navigate into the pyaerocom
root directory where the setup.py file is located. Use

``$ python setup.py install``

to install the package normally or use

``$ python setup.py develop``

to install the package in development mode. The latter leaves the code
editable and while ``install`` installs and freezes the current version
of the code in your Python environment (`see
here <https://packaging.python.org/tutorials/distributing-packages/#working-in-development-mode>`__
or
`here <https://stackoverflow.com/questions/19048732/python-setup-py-develop-vs-install>`__
for more info).

If everything worked out as expected, you should be able to import
pyaerocom from within a Python3 console.

.. code:: ipython3

    import pyaerocom as pya
    print("Installation base directory: %s" %pya.__dir__)
    print("Version: %s" %pya.__version__)


.. parsed-literal::

    2018-08-16 09:20:03,860:INFO:
    Reading aliases ini file: /home/jonasg/github/pyaerocom/pyaerocom/data/aliases.ini


.. parsed-literal::

    Installation base directory: /home/jonasg/github/pyaerocom/pyaerocom
    Version: 0.0.1.dev1


Setting global environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The import of data from the AEROCOM database in pyaerocom is controlled
via an instance of the ``Config`` class.

.. code:: ipython3

    print("Current config: %s" %pya.const.short_str())


.. parsed-literal::

    Current config: 
    Pyaerocom Config
    ----------------
    
    MIN_YEAR: 0
    MAX_YEAR: 20000
    GRID_IO: 
    Pyaerocom GridIO
    ----------------
    
       FILE_TYPE: .nc
       TS_TYPES (list, 5 items)
       ['hourly'
        '3hourly'
        ...
        'monthly'
        'yearly']
    
       DEL_TIME_BOUNDS: True
       SHIFT_LONS: True
       CHECK_TIME_FILENAME: True
       EQUALISE_METADATA: True
       USE_RENAMED_DIR: True
       USE_FILECONVENTION: True
       INCLUDE_SUBDIRS: False
    OBS_WAVELENGTH_TOL_NM: 10.0
    OBS_ALLOW_ALT_WAVELENGTHS: True
    GCOSPERCENTCRIT: 0.1
    GCOSABSCRIT: 0.04
    OBSNET_NONE: NONE
    NOMODELNAME: OBSERVATIONS-ONLY
    REVISION_FILE: Revision.txt
    AERONET_SUN_V2L15_AOD_DAILY_NAME: AeronetSunV2Lev1.5.daily
    AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME: AeronetSun_2.0_NRT
    AERONET_SUN_V2L2_AOD_DAILY_NAME: AeronetSunV2Lev2.daily
    AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME: AeronetSunV2Lev2.AP
    AERONET_SUN_V2L2_SDA_DAILY_NAME: AeronetSDAV2Lev2.daily
    AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME: AeronetSDAV2Lev2.AP
    AERONET_SUN_V3L15_AOD_DAILY_NAME: AeronetSunV3Lev1.5.daily
    AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME: AeronetSunV3Lev1.5.AP
    AERONET_SUN_V3L2_AOD_DAILY_NAME: AeronetSunV3Lev2.daily
    AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME: AeronetSunV3Lev2.AP
    AERONET_SUN_V3L15_SDA_DAILY_NAME: AeronetSDAV3Lev1.5.daily
    AERONET_SUN_V3L15_SDA_ALL_POINTS_NAME: AeronetSDAV3Lev1.5.AP
    AERONET_SUN_V3L2_SDA_DAILY_NAME: AeronetSDAV3Lev2.daily
    AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME: AeronetSDAV3Lev2.AP
    AERONET_INV_V2L15_DAILY_NAME: AeronetInvV2Lev1.5.daily
    AERONET_INV_V2L15_ALL_POINTS_NAME: AeronetInvV2Lev1.5.AP
    AERONET_INV_V2L2_DAILY_NAME: AeronetInvV2Lev2.daily
    AERONET_INV_V2L2_ALL_POINTS_NAME: AeronetInvV2Lev2.AP
    EBAS_MULTICOLUMN_NAME: EBASMC
    EEA_NAME: EEAAQeRep
    EARLINET_NAME: EARLINET
    OBSCONFIG (dict)
    MODELDIRS (list)
       ['/lustre/storeA/project/aerocom/aerocom1/'
        '/lustre/storeA/project/aerocom/aerocom2/'
        ...
        '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-II-IND3/'
        '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-II-IND2/']
    
    MODELBASEDIR: /lustre/storeA/project/aerocom/
    OBSBASEDIR: /lustre/storeA/project/aerocom/
    OBSDATACACHEDIR: /home/jonasg/pyaerocom/_cache
    OUT_BASEDIR: /home/jonasg/pyaerocom
    _config_ini: /home/jonasg/github/pyaerocom/pyaerocom/data/paths.ini
    AERONET_INV_V3L15_DAILY_NAME: AeronetInvV3Lev1.5.daily
    AERONET_INV_V3L2_DAILY_NAME: AeronetInvV3Lev2.daily
    DONOTCACHEFILE: /home/jonasg/pyaerocom/_cache/DONOTCACHE
    PLOT_DIR: /home/jonasg/pyaerocom/plots
    VAR_PARAM: 
    ----------------------
    Pyaerocom AllVariables
    ----------------------
    DEFAULT
    od550aer
    od550lt1aer
    od550gt1aer
    abs550aer
    od440aer
    abs440aer
    ec550aer
    scatc550aer
    bscatc550aer
    ssa440aer
    ssa675aer
    ssa870aer
    ssa1020aer
    ang4487aer
    angabs4487aer
    zdust
    
    Aliases
    .......
    absc550aer = abs550aer


You can check if the relevant base directories ``MODELBASEDIR`` and
``OBSBASEDIR`` are valid.

.. code:: ipython3

    print("All paths valid? %s" %pya.const.READY)


.. parsed-literal::

    All paths valid? True


If you work on your local machine and use the external AEROCOM user
server, you might need to change the path settings. Now you have several
options to do this:

1. Change all relevant paths directly in the
   `paths.ini <https://github.com/metno/pyaerocom/blob/master/pyaeroco%20/data/paths.ini>`__
   file of your installation.
2. Create a new config file <myconfig.ini> and iniate your configuration
   in your Python console by calling
   ``pyaerocom.config = pyaerocom.Config(config_file=<myconfig.ini>)``
3. Change the settings directly within the instance of the ``Config``
   class, as follows:

.. code:: ipython3

    cfg = pya.const
    cfg.MODELBASEDIR="path/that/does/not/exist"
    cfg.OBSBASEDIR="path/that/does/not/exist"
    print("All paths valid? %s" %cfg.READY)


.. parsed-literal::

    All paths valid? False


.. parsed-literal::

    /home/jonasg/github/pyaerocom/pyaerocom/config.py:296: UserWarning: Model base directory %s does not exist
      warn("Model base directory %s does not exist")
    /home/jonasg/github/pyaerocom/pyaerocom/config.py:299: UserWarning: Observations base directory %s does not exist
      warn("Observations base directory %s does not exist")


See what’s currently in there.

.. code:: ipython3

    print("Current config: {}".format(pya.const.short_str()))


.. parsed-literal::

    Current config: 
    Pyaerocom Config
    ----------------
    
    MIN_YEAR: 0
    MAX_YEAR: 20000
    GRID_IO: 
    Pyaerocom GridIO
    ----------------
    
       FILE_TYPE: .nc
       TS_TYPES (list, 5 items)
       ['hourly'
        '3hourly'
        ...
        'monthly'
        'yearly']
    
       DEL_TIME_BOUNDS: True
       SHIFT_LONS: True
       CHECK_TIME_FILENAME: True
       EQUALISE_METADATA: True
       USE_RENAMED_DIR: True
       USE_FILECONVENTION: True
       INCLUDE_SUBDIRS: False
    OBS_WAVELENGTH_TOL_NM: 10.0
    OBS_ALLOW_ALT_WAVELENGTHS: True
    GCOSPERCENTCRIT: 0.1
    GCOSABSCRIT: 0.04
    OBSNET_NONE: NONE
    NOMODELNAME: OBSERVATIONS-ONLY
    REVISION_FILE: Revision.txt
    AERONET_SUN_V2L15_AOD_DAILY_NAME: AeronetSunV2Lev1.5.daily
    AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME: AeronetSun_2.0_NRT
    AERONET_SUN_V2L2_AOD_DAILY_NAME: AeronetSunV2Lev2.daily
    AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME: AeronetSunV2Lev2.AP
    AERONET_SUN_V2L2_SDA_DAILY_NAME: AeronetSDAV2Lev2.daily
    AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME: AeronetSDAV2Lev2.AP
    AERONET_SUN_V3L15_AOD_DAILY_NAME: AeronetSunV3Lev1.5.daily
    AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME: AeronetSunV3Lev1.5.AP
    AERONET_SUN_V3L2_AOD_DAILY_NAME: AeronetSunV3Lev2.daily
    AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME: AeronetSunV3Lev2.AP
    AERONET_SUN_V3L15_SDA_DAILY_NAME: AeronetSDAV3Lev1.5.daily
    AERONET_SUN_V3L15_SDA_ALL_POINTS_NAME: AeronetSDAV3Lev1.5.AP
    AERONET_SUN_V3L2_SDA_DAILY_NAME: AeronetSDAV3Lev2.daily
    AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME: AeronetSDAV3Lev2.AP
    AERONET_INV_V2L15_DAILY_NAME: AeronetInvV2Lev1.5.daily
    AERONET_INV_V2L15_ALL_POINTS_NAME: AeronetInvV2Lev1.5.AP
    AERONET_INV_V2L2_DAILY_NAME: AeronetInvV2Lev2.daily
    AERONET_INV_V2L2_ALL_POINTS_NAME: AeronetInvV2Lev2.AP
    EBAS_MULTICOLUMN_NAME: EBASMC
    EEA_NAME: EEAAQeRep
    EARLINET_NAME: EARLINET
    OBSCONFIG (dict)
    MODELDIRS (list)
       ['/lustre/storeA/project/aerocom/aerocom1/'
        '/lustre/storeA/project/aerocom/aerocom2/'
        ...
        '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-II-IND3/'
        '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-II-IND2/']
    
    MODELBASEDIR: path/that/does/not/exist
    OBSBASEDIR: path/that/does/not/exist
    OBSDATACACHEDIR: /home/jonasg/pyaerocom/_cache
    OUT_BASEDIR: /home/jonasg/pyaerocom
    _config_ini: /home/jonasg/github/pyaerocom/pyaerocom/data/paths.ini
    AERONET_INV_V3L15_DAILY_NAME: AeronetInvV3Lev1.5.daily
    AERONET_INV_V3L2_DAILY_NAME: AeronetInvV3Lev2.daily
    DONOTCACHEFILE: /home/jonasg/pyaerocom/_cache/DONOTCACHE
    PLOT_DIR: /home/jonasg/pyaerocom/plots
    VAR_PARAM: 
    ----------------------
    Pyaerocom AllVariables
    ----------------------
    DEFAULT
    od550aer
    od550lt1aer
    od550gt1aer
    abs550aer
    od440aer
    abs440aer
    ec550aer
    scatc550aer
    bscatc550aer
    ssa440aer
    ssa675aer
    ssa870aer
    ssa1020aer
    ang4487aer
    angabs4487aer
    zdust
    
    Aliases
    .......
    absc550aer = abs550aer


As you can see, ``MODELBASEDIR`` and ``OBSBASEDIR`` contain the invalid
paths, but e.g. the list containing model directories (``MODELDIRS``)
still has the original settings. This is because, these are written in
the method ``load_config(config_file)`` or the wrapper method
``reload()`` which does the same. Now reload the config_file and print.

.. code:: ipython3

    cfg.reload()
    print("Current config: {}".format(pya.const.short_str()))


.. parsed-literal::

    Current config: 
    Pyaerocom Config
    ----------------
    
    MIN_YEAR: 0
    MAX_YEAR: 20000
    GRID_IO: 
    Pyaerocom GridIO
    ----------------
    
       FILE_TYPE: .nc
       TS_TYPES (list, 5 items)
       ['hourly'
        '3hourly'
        ...
        'monthly'
        'yearly']
    
       DEL_TIME_BOUNDS: True
       SHIFT_LONS: True
       CHECK_TIME_FILENAME: True
       EQUALISE_METADATA: True
       USE_RENAMED_DIR: True
       USE_FILECONVENTION: True
       INCLUDE_SUBDIRS: False
    OBS_WAVELENGTH_TOL_NM: 10.0
    OBS_ALLOW_ALT_WAVELENGTHS: True
    GCOSPERCENTCRIT: 0.1
    GCOSABSCRIT: 0.04
    OBSNET_NONE: NONE
    NOMODELNAME: OBSERVATIONS-ONLY
    REVISION_FILE: Revision.txt
    AERONET_SUN_V2L15_AOD_DAILY_NAME: AeronetSunV2Lev1.5.daily
    AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME: AeronetSun_2.0_NRT
    AERONET_SUN_V2L2_AOD_DAILY_NAME: AeronetSunV2Lev2.daily
    AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME: AeronetSunV2Lev2.AP
    AERONET_SUN_V2L2_SDA_DAILY_NAME: AeronetSDAV2Lev2.daily
    AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME: AeronetSDAV2Lev2.AP
    AERONET_SUN_V3L15_AOD_DAILY_NAME: AeronetSunV3Lev1.5.daily
    AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME: AeronetSunV3Lev1.5.AP
    AERONET_SUN_V3L2_AOD_DAILY_NAME: AeronetSunV3Lev2.daily
    AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME: AeronetSunV3Lev2.AP
    AERONET_SUN_V3L15_SDA_DAILY_NAME: AeronetSDAV3Lev1.5.daily
    AERONET_SUN_V3L15_SDA_ALL_POINTS_NAME: AeronetSDAV3Lev1.5.AP
    AERONET_SUN_V3L2_SDA_DAILY_NAME: AeronetSDAV3Lev2.daily
    AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME: AeronetSDAV3Lev2.AP
    AERONET_INV_V2L15_DAILY_NAME: AeronetInvV2Lev1.5.daily
    AERONET_INV_V2L15_ALL_POINTS_NAME: AeronetInvV2Lev1.5.AP
    AERONET_INV_V2L2_DAILY_NAME: AeronetInvV2Lev2.daily
    AERONET_INV_V2L2_ALL_POINTS_NAME: AeronetInvV2Lev2.AP
    EBAS_MULTICOLUMN_NAME: EBASMC
    EEA_NAME: EEAAQeRep
    EARLINET_NAME: EARLINET
    OBSCONFIG (dict)
    MODELDIRS (list)
       ['/lustre/storeA/project/aerocom/aerocom1/'
        '/lustre/storeA/project/aerocom/aerocom2/'
        ...
        '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-II-IND3/'
        '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-II-IND2/']
    
    MODELBASEDIR: /lustre/storeA/project/aerocom/
    OBSBASEDIR: /lustre/storeA/project/aerocom/
    OBSDATACACHEDIR: /home/jonasg/pyaerocom/_cache
    OUT_BASEDIR: /home/jonasg/pyaerocom
    _config_ini: /home/jonasg/github/pyaerocom/pyaerocom/data/paths.ini
    AERONET_INV_V3L15_DAILY_NAME: AeronetInvV3Lev1.5.daily
    AERONET_INV_V3L2_DAILY_NAME: AeronetInvV3Lev2.daily
    DONOTCACHEFILE: /home/jonasg/pyaerocom/_cache/DONOTCACHE
    PLOT_DIR: /home/jonasg/pyaerocom/plots
    VAR_PARAM: 
    ----------------------
    Pyaerocom AllVariables
    ----------------------
    DEFAULT
    od550aer
    od550lt1aer
    od550gt1aer
    abs550aer
    od440aer
    abs440aer
    ec550aer
    scatc550aer
    bscatc550aer
    ssa440aer
    ssa675aer
    ssa870aer
    ssa1020aer
    ang4487aer
    angabs4487aer
    zdust
    
    Aliases
    .......
    absc550aer = abs550aer


The ``reload`` (and ``load_config``) method actually checks if the
currently defined base directories exist, and if not, it uses the ones
that are defined in the
`paths.ini <http://aerocom.met.no/pyaerocom/config_files.html#paths-and-directories>`__
file. This is the why the above configuration is the intial one. If you
choose valid paths, this should work.

.. code:: ipython3

    cfg = pya.const
    cfg.MODELBASEDIR="."
    cfg.OBSBASEDIR="."
    print("All paths valid? %s" %cfg.READY)
    cfg.reload()
    print("Current config: %s" %cfg.short_str())


.. parsed-literal::

    All paths valid? True
    Current config: 
    Pyaerocom Config
    ----------------
    
    MIN_YEAR: 0
    MAX_YEAR: 20000
    GRID_IO: 
    Pyaerocom GridIO
    ----------------
    
       FILE_TYPE: .nc
       TS_TYPES (list, 5 items)
       ['hourly'
        '3hourly'
        ...
        'monthly'
        'yearly']
    
       DEL_TIME_BOUNDS: True
       SHIFT_LONS: True
       CHECK_TIME_FILENAME: True
       EQUALISE_METADATA: True
       USE_RENAMED_DIR: True
       USE_FILECONVENTION: True
       INCLUDE_SUBDIRS: False
    OBS_WAVELENGTH_TOL_NM: 10.0
    OBS_ALLOW_ALT_WAVELENGTHS: True
    GCOSPERCENTCRIT: 0.1
    GCOSABSCRIT: 0.04
    OBSNET_NONE: NONE
    NOMODELNAME: OBSERVATIONS-ONLY
    REVISION_FILE: Revision.txt
    AERONET_SUN_V2L15_AOD_DAILY_NAME: AeronetSunV2Lev1.5.daily
    AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME: AeronetSun_2.0_NRT
    AERONET_SUN_V2L2_AOD_DAILY_NAME: AeronetSunV2Lev2.daily
    AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME: AeronetSunV2Lev2.AP
    AERONET_SUN_V2L2_SDA_DAILY_NAME: AeronetSDAV2Lev2.daily
    AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME: AeronetSDAV2Lev2.AP
    AERONET_SUN_V3L15_AOD_DAILY_NAME: AeronetSunV3Lev1.5.daily
    AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME: AeronetSunV3Lev1.5.AP
    AERONET_SUN_V3L2_AOD_DAILY_NAME: AeronetSunV3Lev2.daily
    AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME: AeronetSunV3Lev2.AP
    AERONET_SUN_V3L15_SDA_DAILY_NAME: AeronetSDAV3Lev1.5.daily
    AERONET_SUN_V3L15_SDA_ALL_POINTS_NAME: AeronetSDAV3Lev1.5.AP
    AERONET_SUN_V3L2_SDA_DAILY_NAME: AeronetSDAV3Lev2.daily
    AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME: AeronetSDAV3Lev2.AP
    AERONET_INV_V2L15_DAILY_NAME: AeronetInvV2Lev1.5.daily
    AERONET_INV_V2L15_ALL_POINTS_NAME: AeronetInvV2Lev1.5.AP
    AERONET_INV_V2L2_DAILY_NAME: AeronetInvV2Lev2.daily
    AERONET_INV_V2L2_ALL_POINTS_NAME: AeronetInvV2Lev2.AP
    EBAS_MULTICOLUMN_NAME: EBASMC
    EEA_NAME: EEAAQeRep
    EARLINET_NAME: EARLINET
    OBSCONFIG (dict)
    MODELDIRS (list)
       ['.aerocom1/'
        '.aerocom2/'
        ...
        '.aerocom-users-database/AEROCOM-PHASE-II-IND3/'
        '.aerocom-users-database/AEROCOM-PHASE-II-IND2/']
    
    MODELBASEDIR: .
    OBSBASEDIR: .
    OBSDATACACHEDIR: /home/jonasg/pyaerocom/_cache
    OUT_BASEDIR: /home/jonasg/pyaerocom
    _config_ini: /home/jonasg/github/pyaerocom/pyaerocom/data/paths.ini
    AERONET_INV_V3L15_DAILY_NAME: AeronetInvV3Lev1.5.daily
    AERONET_INV_V3L2_DAILY_NAME: AeronetInvV3Lev2.daily
    DONOTCACHEFILE: /home/jonasg/pyaerocom/_cache/DONOTCACHE
    PLOT_DIR: /home/jonasg/pyaerocom/plots
    VAR_PARAM: 
    ----------------------
    Pyaerocom AllVariables
    ----------------------
    DEFAULT
    od550aer
    od550lt1aer
    od550gt1aer
    abs550aer
    od440aer
    abs440aer
    ec550aer
    scatc550aer
    bscatc550aer
    ssa440aer
    ssa675aer
    ssa870aer
    ssa1020aer
    ang4487aer
    angabs4487aer
    zdust
    
    Aliases
    .......
    absc550aer = abs550aer


This is it! Note, however, that we just inserted the current directory
which is not where the data actually is. Thus, before continuing, we
have to reload the config as it was at the beginning:

.. code:: ipython3

    cfg.reload(keep_basedirs=False)
    print(cfg.short_str())


.. parsed-literal::

    
    Pyaerocom Config
    ----------------
    
    MIN_YEAR: 0
    MAX_YEAR: 20000
    GRID_IO: 
    Pyaerocom GridIO
    ----------------
    
       FILE_TYPE: .nc
       TS_TYPES (list, 5 items)
       ['hourly'
        '3hourly'
        ...
        'monthly'
        'yearly']
    
       DEL_TIME_BOUNDS: True
       SHIFT_LONS: True
       CHECK_TIME_FILENAME: True
       EQUALISE_METADATA: True
       USE_RENAMED_DIR: True
       USE_FILECONVENTION: True
       INCLUDE_SUBDIRS: False
    OBS_WAVELENGTH_TOL_NM: 10.0
    OBS_ALLOW_ALT_WAVELENGTHS: True
    GCOSPERCENTCRIT: 0.1
    GCOSABSCRIT: 0.04
    OBSNET_NONE: NONE
    NOMODELNAME: OBSERVATIONS-ONLY
    REVISION_FILE: Revision.txt
    AERONET_SUN_V2L15_AOD_DAILY_NAME: AeronetSunV2Lev1.5.daily
    AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME: AeronetSun_2.0_NRT
    AERONET_SUN_V2L2_AOD_DAILY_NAME: AeronetSunV2Lev2.daily
    AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME: AeronetSunV2Lev2.AP
    AERONET_SUN_V2L2_SDA_DAILY_NAME: AeronetSDAV2Lev2.daily
    AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME: AeronetSDAV2Lev2.AP
    AERONET_SUN_V3L15_AOD_DAILY_NAME: AeronetSunV3Lev1.5.daily
    AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME: AeronetSunV3Lev1.5.AP
    AERONET_SUN_V3L2_AOD_DAILY_NAME: AeronetSunV3Lev2.daily
    AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME: AeronetSunV3Lev2.AP
    AERONET_SUN_V3L15_SDA_DAILY_NAME: AeronetSDAV3Lev1.5.daily
    AERONET_SUN_V3L15_SDA_ALL_POINTS_NAME: AeronetSDAV3Lev1.5.AP
    AERONET_SUN_V3L2_SDA_DAILY_NAME: AeronetSDAV3Lev2.daily
    AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME: AeronetSDAV3Lev2.AP
    AERONET_INV_V2L15_DAILY_NAME: AeronetInvV2Lev1.5.daily
    AERONET_INV_V2L15_ALL_POINTS_NAME: AeronetInvV2Lev1.5.AP
    AERONET_INV_V2L2_DAILY_NAME: AeronetInvV2Lev2.daily
    AERONET_INV_V2L2_ALL_POINTS_NAME: AeronetInvV2Lev2.AP
    EBAS_MULTICOLUMN_NAME: EBASMC
    EEA_NAME: EEAAQeRep
    EARLINET_NAME: EARLINET
    OBSCONFIG (dict)
    MODELDIRS (list)
       ['/lustre/storeA/project/aerocom/aerocom1/'
        '/lustre/storeA/project/aerocom/aerocom2/'
        ...
        '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-II-IND3/'
        '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-II-IND2/']
    
    MODELBASEDIR: /lustre/storeA/project/aerocom/
    OBSBASEDIR: /lustre/storeA/project/aerocom/
    OBSDATACACHEDIR: /home/jonasg/pyaerocom/_cache
    OUT_BASEDIR: /home/jonasg/pyaerocom
    _config_ini: /home/jonasg/github/pyaerocom/pyaerocom/data/paths.ini
    AERONET_INV_V3L15_DAILY_NAME: AeronetInvV3Lev1.5.daily
    AERONET_INV_V3L2_DAILY_NAME: AeronetInvV3Lev2.daily
    DONOTCACHEFILE: /home/jonasg/pyaerocom/_cache/DONOTCACHE
    PLOT_DIR: /home/jonasg/pyaerocom/plots
    VAR_PARAM: 
    ----------------------
    Pyaerocom AllVariables
    ----------------------
    DEFAULT
    od550aer
    od550lt1aer
    od550gt1aer
    abs550aer
    od440aer
    abs440aer
    ec550aer
    scatc550aer
    bscatc550aer
    ssa440aer
    ssa675aer
    ssa870aer
    ssa1020aer
    ang4487aer
    angabs4487aer
    zdust
    
    Aliases
    .......
    absc550aer = abs550aer


Now with everything being set up correctly, we can start analysing the
data. The following tutorials focus on the reading, plotting and
analysis of model data. Tutorials for observational data will follow
soon, as well as tutorials that show how to merge and compare model with
observational data. Before you can work with the data, you may want to
find out what data is available. The following section shows how to do
this.

Finding data directories of model or observation data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let’s presume you want to access data from a certain model or
observation and you want to check if it is available. Let’s assume you
are interested in data from a control run (*CTRL*) of the CAM Oslo model
but you do not know the exact model version or run ID. Then, you can
browse existing data directories using a wildcard search, simply by (we
put it in a try/except block, since with wildcard browse it will not
find a unique ID and thus raise an Exception):

.. code:: ipython3

    try:
        pya.search_data_dir_aerocom("CAM*CTRL*")
    except OSError as e:
        print(repr(e))


.. parsed-literal::

    2018-08-16 09:20:04,741:INFO:
    Searching database for CAM*CTRL*
    2018-08-16 09:20:04,851:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,170:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,175:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,180:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,185:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,189:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,193:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,197:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,201:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,205:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,210:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,231:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,236:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,241:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,246:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,250:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,255:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,259:INFO:
    Checking if renamed directory exists


.. parsed-literal::

    OSError("Found multiple matches for search pattern CAM*CTRL*. Please choose from ['CAMS_REANCTRL', 'CAM5-Oslo_FAMIPWARMCnudge-emi2000.A2.CTRL', 'CAM4-Oslo_Vprelim.A2.CTRL', 'CAM5-MAM3-PNNL.A2.CTRL', 'CAM4-Oslo-Vcmip5online.A2.CTRL', 'CAM4-Oslo-Vcmip5.A2.CTRL', 'CAM4-Oslo-Vcmip5emi2000.A2.CTRL', 'CAM5.1-MAM3-PNNL.A2.CTRL', 'CAM3.A2.CTRL', 'CAM4-Oslo.A2.CTRL', 'BCC_AGCM2.0.1_CAM.A2.CTRL', 'ECMWF-IFS-CY42R1-CAMS-RA-CTRL_AP3-CTRL2016-PD', 'ECMWF-IFS-CY43R1-CAMS-NITRATE-DEV_AP3-CTRL2016-PD', 'CAM5.4_CTRL2016', 'CAM5_CTRL2016', 'CAM5.3-Oslo_CTRL2016', 'CAM5.3-Oslo_AP3-CTRL2016-PD', 'CAM5.3-Oslo_AP3-CTRL2016-PI']",)


Reading the aerosol optical detph at 550nm using a specified model ID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The resulting list shows possible options that were found in the
database. Let’s choose the *CAM5.3-Oslo_CTRL2016* run and import the
data. In the following cell, we directly instantiate a read class for
data import since we know the model and run ID from the previous cell
(the read class basically includes the above used search method.

.. code:: ipython3

    read = pya.io.ReadGridded("CAM5.3-Oslo_CTRL2016")


.. parsed-literal::

    2018-08-16 09:20:05,414:INFO:
    Searching database for CAM5.3-Oslo_CTRL2016
    2018-08-16 09:20:05,633:INFO:
    Checking if renamed directory exists
    2018-08-16 09:20:05,634:INFO:
    Found match for ID CAM5.3-Oslo_CTRL2016
    2018-08-16 09:20:05,789:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550dust_Column_2006_daily.nc
    2018-08-16 09:20:05,791:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od440aer_Column_2008_daily.nc
    2018-08-16 09:20:05,793:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550dryaer_Column_2008_3hourly.nc
    2018-08-16 09:20:05,795:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od870aer_Column_2008_daily.nc
    2018-08-16 09:20:05,797:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550aerh2o_Column_2008_daily.nc
    2018-08-16 09:20:05,799:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550dust_Column_2010_3hourly.nc
    2018-08-16 09:20:05,801:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550aerh2o_Column_2010_3hourly.nc
    2018-08-16 09:20:05,802:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550aerh2o_Column_2010_daily.nc
    2018-08-16 09:20:05,803:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od870aer_Column_2008_3hourly.nc
    2018-08-16 09:20:05,805:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_abs550aer_Column_2006_daily.nc
    2018-08-16 09:20:05,806:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550dryaer_Column_2010_daily.nc
    2018-08-16 09:20:05,808:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550lt1aer_Column_2010_3hourly.nc
    2018-08-16 09:20:05,809:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od440aer_Column_2006_daily.nc
    2018-08-16 09:20:05,811:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550lt1aer_Column_2006_3hourly.nc
    2018-08-16 09:20:05,813:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550lt1aer_Column_2008_3hourly.nc
    2018-08-16 09:20:05,814:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550aer_Column_2006_daily.nc
    2018-08-16 09:20:05,815:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550lt1aer_Column_2010_daily.nc
    2018-08-16 09:20:05,817:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550dryaer_Column_2006_3hourly.nc
    2018-08-16 09:20:05,818:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od440aer_Column_2006_3hourly.nc
    2018-08-16 09:20:05,819:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550dryaer_Column_2010_3hourly.nc
    2018-08-16 09:20:05,821:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_abs550aer_Column_2008_daily.nc
    2018-08-16 09:20:05,822:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od870aer_Column_2010_daily.nc
    2018-08-16 09:20:05,824:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od870aer_Column_2006_daily.nc
    2018-08-16 09:20:05,825:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od440aer_Column_2010_3hourly.nc
    2018-08-16 09:20:05,827:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od870aer_Column_2010_3hourly.nc
    2018-08-16 09:20:05,828:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550aer_Column_2010_daily.nc
    2018-08-16 09:20:05,830:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550dust_Column_2006_3hourly.nc
    2018-08-16 09:20:05,832:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_abs550aer_Column_2010_3hourly.nc
    2018-08-16 09:20:05,833:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_abs550aer_Column_2006_3hourly.nc
    2018-08-16 09:20:05,834:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_abs550aer_Column_2010_daily.nc
    2018-08-16 09:20:05,836:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550lt1aer_Column_2008_daily.nc
    2018-08-16 09:20:05,838:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550dryaer_Column_2006_daily.nc
    2018-08-16 09:20:05,839:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550dust_Column_2008_daily.nc
    2018-08-16 09:20:05,840:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550aerh2o_Column_2006_daily.nc
    2018-08-16 09:20:05,841:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550aer_Column_2006_3hourly.nc
    2018-08-16 09:20:05,842:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550aer3d_ModelLevel_2010_3hourly.nc
    2018-08-16 09:20:05,843:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od870aer_Column_2006_3hourly.nc
    2018-08-16 09:20:05,844:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550aerh2o_Column_2006_3hourly.nc
    2018-08-16 09:20:05,845:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550aer_Column_2010_3hourly.nc
    2018-08-16 09:20:05,846:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550aer_Column_2008_daily.nc
    2018-08-16 09:20:05,846:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550aerh2o_Column_2008_3hourly.nc
    2018-08-16 09:20:05,847:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550dryaer_Column_2008_daily.nc
    2018-08-16 09:20:05,848:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od440aer_Column_2010_daily.nc
    2018-08-16 09:20:05,849:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550lt1aer_Column_2006_daily.nc
    2018-08-16 09:20:05,849:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550dust_Column_2008_3hourly.nc
    2018-08-16 09:20:05,850:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_abs550aer_Column_2008_3hourly.nc
    2018-08-16 09:20:05,851:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550aer_Column_2008_3hourly.nc
    2018-08-16 09:20:05,851:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_deltaz3d_ModelLevel_2010_3hourly.nc
    2018-08-16 09:20:05,852:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od440aer_Column_2008_3hourly.nc
    2018-08-16 09:20:05,852:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_od550dust_Column_2010_daily.nc
    2018-08-16 09:20:05,853:DEBUG:
    Read file /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed/aerocom3_CAM5.3-Oslo_CTRL2016_humidity3d_ModelLevel_2010_3hourly.nc


Okay, let’s see what is in there.

.. code:: ipython3

    print(read)


.. parsed-literal::

    
    Pyaerocom ReadGridded
    ---------------------
    Model ID: CAM5.3-Oslo_CTRL2016
    Data directory: /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed
    Available variables: ['abs550aer', 'deltaz3d', 'humidity3d', 'od440aer', 'od550aer', 'od550aer3d', 'od550aerh2o', 'od550dryaer', 'od550dust', 'od550lt1aer', 'od870aer']
    Available years: [2006, 2008, 2010]
    Available time resolutions ['3hourly', 'daily']


Let’s load results for the aerosol optical depth (*od550aer*) for march
2010. The read function take a string or a list of strings as input for
specifying one or more variables that are supposed to be read. Thus, the
return type of this method is **always a tuple, even if we only provide
one variable** (as in the following example) and as a result, the loaded
data object has to be accessed using the first index of the tuple.

.. code:: ipython3

    data = read.read("od550aer", start_time="1 march 2010", stop_time="31 march 2010")[0]


.. parsed-literal::

    2018-08-16 09:20:05,914:DEBUG:
    FOUND MATCH: aerocom3_CAM5.3-Oslo_CTRL2016_od550aer_Column_2010_3hourly.nc
    2018-08-16 09:20:19,790:WARNING:
    Invalid time dimension.
    Error message: ValueError("Time match error, nominal dates for test array[0 1 2 7] (unit=days since 2004-01-01 00:00:00): ['2010-01-01T00' '2010-01-01T03' '2010-01-01T06' '2010-01-01T21']\nReceived values after conversion: ['2010-01-01T00' '2010-01-01T00' '2010-01-01T00' '2010-01-01T00']",)
    2018-08-16 09:20:19,791:WARNING:
    Invalid time axis in file aerocom3_CAM5.3-Oslo_CTRL2016_od550aer_Column_2010_3hourly.nc. Attempting to correct.
    2018-08-16 09:20:20,333:INFO:
    Rolling longitudes to -180 -> 180 definition
    2018-08-16 09:20:20,338:INFO:
    Applying temporal cropping of result cube
    2018-08-16 09:20:20,338:INFO:
    Cropping along time axis based on Timestamps


Accessing the data and plotting a map
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The loaded data is of type *GriddedData* and can now be used for further
analysis. It’s string representation contains a useful summary of what
is in there.

.. code:: ipython3

    print(data)


.. parsed-literal::

    pyaerocom.GriddedData: CAM5.3-Oslo_CTRL2016
    Grid data: Aerosol optical depth at 550nm / (1) (time: 248; latitude: 192; longitude: 288)
         Dimension coordinates:
              time                            x              -               -
              latitude                        -              x               -
              longitude                       -              -               x
         Attributes:
              Conventions: CF-1.0
              NCO: 4.3.7
              Version: $Name$
              case: optINSITUnRemote
              history: Wed Feb  8 11:55:24 2017: ncatted -O -a units,od550aer,o,c,1 TMPmnth_od550aer.2010-01.nc
    Wed...
              host: r10i0n0
              initial_file: /work/shared/noresm/inputdata/atm/cam/inic/fv/cami-mam3_0000-01-01_0.9...
              logname: kirkevag
              nco_openmp_thread_number: 1
              revision_Id: $Id$
              source: CAM
              title: UNSET
              topography_file: /work/shared/noresm/inputdata/noresm-only/inputForNudging/ERA_f09f09_3...


The data comprises 31 time stamps, as expected, since we picked one
month and the dataset is daily. Now, for instance, we can crop the data
using a predefined region (e.g. South America) and plot the first day of
the dataset.

.. code:: ipython3

    fig = data.crop(region="SAMERICA").quickplot_map(time_idx=0)



.. image:: tut00_get_started/tut00_get_started_28_0.png


We might also be interested in the weighted area average for the month
that we extracted.

.. code:: ipython3

    weighted_mean = data.area_weighted_mean()
    weighted_mean


.. parsed-literal::

    /home/jonasg/anaconda3/lib/python3.6/site-packages/iris/analysis/cartography.py:377: UserWarning: Using DEFAULT_SPHERICAL_EARTH_RADIUS.
      warnings.warn("Using DEFAULT_SPHERICAL_EARTH_RADIUS.")




.. parsed-literal::

    masked_array(data=[0.13707124521646233, 0.1373723321458452,
                       0.13640485953205256, 0.13661781887097216,
                       0.13832752529888542, 0.13943940046228157,
                       0.13906411166070964, 0.13903393246626614,
                       0.1389572414826536, 0.1387749384645807,
                       0.13859131867159108, 0.1392616918989809,
                       0.14148057496888855, 0.14422837963496726,
                       0.14485939091969455, 0.14382647033828228,
                       0.1429247987684401, 0.14132091948668582,
                       0.13963221183937138, 0.13899722350877253,
                       0.1397316309699972, 0.140429463344697,
                       0.13979820277861796, 0.13931129118926358,
                       0.1382730558010573, 0.13705837683541341,
                       0.13626943214697504, 0.13656861866930264,
                       0.13828947462737487, 0.13862655803764867,
                       0.13801004090860575, 0.13816556759043425,
                       0.13891506072795737, 0.13885491398159325,
                       0.13791297848698755, 0.13786872604208614,
                       0.1383256634671104, 0.13802173506964452,
                       0.13734295888393036, 0.13670887870882611,
                       0.13583143441388867, 0.134603109796585,
                       0.1333276946610027, 0.13244025688660607,
                       0.13297618583370702, 0.13337864744931724,
                       0.13325346476065494, 0.13273727817161787,
                       0.13272747346724398, 0.1333092276404929,
                       0.1333797519133725, 0.13433262445580588,
                       0.13693531065433906, 0.13957995569444528,
                       0.13962851699132414, 0.13859857966249953,
                       0.13791145087797585, 0.13739929473269538,
                       0.13723982261191392, 0.1380459466011261,
                       0.13946419690290854, 0.14042819240907664,
                       0.13931406757480316, 0.13866676878977408,
                       0.13822170463985428, 0.13778772182438,
                       0.13651838547716436, 0.13615014242990736,
                       0.13744348000076528, 0.13995109480361492,
                       0.1411970413507769, 0.14199804429653667,
                       0.14258413847594195, 0.14220802982119984,
                       0.14140121976767336, 0.14120394722823995,
                       0.14162688135139243, 0.14188006322900268,
                       0.1414684469806162, 0.14223318292711828,
                       0.14334570700875637, 0.14337269717823287,
                       0.1421074317050635, 0.14175130499968785,
                       0.14035452134831083, 0.1388756394628699,
                       0.13762539366487916, 0.13717837639346694,
                       0.13737289737903915, 0.13747045610992034,
                       0.13745494956066656, 0.1378100303636898,
                       0.1382755441221473, 0.13892579338926514,
                       0.13933988912083564, 0.14051427623407034,
                       0.142736023510284, 0.14312065245179398,
                       0.14234607987063616, 0.14275634737217646,
                       0.1437991330395562, 0.14502984115661513,
                       0.14599941360148747, 0.14601582462470347,
                       0.14640728011839496, 0.14610034153933943,
                       0.14537368722625044, 0.14578767727711434,
                       0.14607726598563622, 0.14605008459289356,
                       0.1460609898662843, 0.14703622375646566,
                       0.1478730521106064, 0.14803795993760244,
                       0.14711712713761174, 0.14729376248796983,
                       0.14851956275002343, 0.14967160487601566,
                       0.14983351441403536, 0.1495072510640238,
                       0.14926850286432325, 0.14944789863237368,
                       0.14876039934421642, 0.1488120453274109,
                       0.1498588856911828, 0.15175075392107956,
                       0.15258806488973015, 0.15286511152135315,
                       0.15386619169423127, 0.15464113549871336,
                       0.15379449982944376, 0.1543578549941653,
                       0.15808873311045932, 0.16173720799971888,
                       0.16307998367790294, 0.16233174812565518,
                       0.1622602797752089, 0.16177535638150164,
                       0.16164991550698743, 0.16343753440952663,
                       0.16855594710934646, 0.1719380617102505,
                       0.173537727285836, 0.17268164846620168,
                       0.17202374731742412, 0.17073150361330935,
                       0.1704552789189035, 0.17349453196470094,
                       0.17750026098212954, 0.17998882407680658,
                       0.18054660903180453, 0.17991221467411075,
                       0.17879081786543402, 0.17698044738876634,
                       0.17481216302184016, 0.1751095588835362,
                       0.17730235300005773, 0.17828917633948513,
                       0.17798693352549597, 0.1772903761042442,
                       0.17719593452088098, 0.1767203402146187,
                       0.17450815886422721, 0.17625358243592468,
                       0.17887701620267582, 0.1808136330474918,
                       0.1813785961957623, 0.18172509147369986,
                       0.18184876453017618, 0.18271725245843057,
                       0.18252036797692608, 0.183265249795722,
                       0.1844909214607128, 0.18434110595951833,
                       0.1836490864781075, 0.1819315626374836,
                       0.18101720818481568, 0.17955118573504456,
                       0.17735986473912252, 0.17627436278489908,
                       0.17619709057120855, 0.17565989305918675,
                       0.173237661796461, 0.17174118540853084,
                       0.1715433743879658, 0.17103179349744851,
                       0.17009143210388886, 0.17036903993748823,
                       0.1701968332986933, 0.16931755448903732,
                       0.16809969031904087, 0.16694191454539364,
                       0.16614923082470998, 0.16574702124976093,
                       0.16442009711927774, 0.163817742262745,
                       0.16433976044469292, 0.16499539122759532,
                       0.16405480998741243, 0.1628713751723746,
                       0.16180210801804973, 0.16132300069909628,
                       0.16076469208509833, 0.1619812080249729,
                       0.16568802507402378, 0.16834462196868816,
                       0.1688091207855011, 0.16874451605557048,
                       0.16918274517630819, 0.16976238755144346,
                       0.16853813844367546, 0.1689505218199379,
                       0.17008794466862398, 0.1713995695153675,
                       0.17160758485378236, 0.1719104396714293,
                       0.17141519454588505, 0.17098573396603006,
                       0.17014341748677245, 0.17124457916107655,
                       0.17343997831072036, 0.17267167552123458,
                       0.17119276567171318, 0.17110151528151052,
                       0.17129777088602452, 0.1706512286992157,
                       0.1697909385002585, 0.1701305419449026,
                       0.17177346958794434, 0.17199251637814433,
                       0.1717777280458928, 0.17140460031838234,
                       0.1708872614290405, 0.16939067518025105,
                       0.16730749171621387, 0.16687632033654826,
                       0.16768823626524956, 0.16777431113498986,
                       0.16696977975746236, 0.1663374313210154,
                       0.16650691596502723, 0.16594519982156614,
                       0.1651931704892058, 0.1651909843511451,
                       0.16565543871393762, 0.1660138264006659,
                       0.16468225292020627, 0.16419141107042712],
                 mask=[False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False,
                       False, False, False, False, False, False, False, False],
           fill_value=1e+20)



.. code:: ipython3

    import pandas as pd
    pd.Series(weighted_mean, data.time_stamps()).plot()




.. parsed-literal::

    <matplotlib.axes._subplots.AxesSubplot at 0x7f45e4703b38>




.. image:: tut00_get_started/tut00_get_started_31_1.png


The following notebook introduces in more detail how pyaerocom handles
regions and where they can be defined. In the subsequent tutorial, the
``ReadGridded`` class is introduced, that was usesed above to import
model data in a flexible way based on variable name, time range and
temporal resolution. The loaded data for each model and variable is then
stored in the analysis class ``GriddedData`` which we use in the end of
this notebook and which will be introduced in a later tutorial.
