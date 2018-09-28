
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

    2018-09-28 18:27:13,977:WARNING:
    basemap extension library is not installed (or cannot be imported. Some features will not be available
    OBS directory path /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSun2.0.SDA.AP/renamed does not exist
    OBS directory path /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev2.0.AP/renamed does not exist
    OBS directory path /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSun2.0.SDA.AP/renamed does not exist
    OBS directory path /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev2.0.AP/renamed does not exist
    2018-09-28 18:27:14,789:WARNING:
    geopy library is not available. Aeolus data read not enabled


.. parsed-literal::

    Installation base directory: /home/jonasg/github/pyaerocom/pyaerocom
    Version: 0.3.0


Setting-up the paths for data import and output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The import of data from the AEROCOM database in pyaerocom is controlled
via an instance of the ``Config`` class. The attribute ``const`` of
pyaerocom returns the current configuration.

.. code:: ipython3

    print(pya.const)


.. parsed-literal::

    
    Pyaerocom Config
    ----------------
    
    _config_ini: /home/jonasg/github/pyaerocom/pyaerocom/data/paths.ini
    _modelbasedir: /lustre/storeA/project/aerocom/
    _obsbasedir: /lustre/storeA/project/aerocom/
    _cachedir: /home/jonasg/pyaerocom/_cache
    _outputdir: /home/jonasg/pyaerocom
    _caching_active: True
    _var_param: None
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
       CORRECT_TIME_FILENAME: True
       CHECK_DIM_COORDS: False
       EQUALISE_METADATA: True
       USE_RENAMED_DIR: True
       INCLUDE_SUBDIRS: False
    OBSCONFIG (dict)
    MODELDIRS (list)
       ['/lustre/storeA/project/aerocom/aerocom1/'
        '/lustre/storeA/project/aerocom/aerocom2/'
        ...
        '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-II-IND3/'
        '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-II-IND2/']
    
    WRITE_FILEIO_ERR_LOG: True
    AERONET_SUN_V2L15_AOD_DAILY_NAME: AeronetSunV2Lev1.5.daily
    AERONET_SUN_V2L15_AOD_ALL_POINTS_NAME: AeronetSun_2.0_NRT
    AERONET_SUN_V2L2_AOD_DAILY_NAME: AeronetSunV2Lev2.daily
    AERONET_SUN_V2L2_AOD_ALL_POINTS_NAME: AeronetSunV2Lev2.AP
    AERONET_SUN_V2L2_SDA_DAILY_NAME: AeronetSDAV2Lev2.daily
    AERONET_SUN_V2L2_SDA_ALL_POINTS_NAME: AeronetSDAV2Lev2.AP
    AERONET_INV_V2L15_DAILY_NAME: AeronetInvV2Lev1.5.daily
    AERONET_INV_V2L15_ALL_POINTS_NAME: AeronetInvV2Lev1.5.AP
    AERONET_INV_V2L2_DAILY_NAME: AeronetInvV2Lev2.daily
    AERONET_INV_V2L2_ALL_POINTS_NAME: AeronetInvV2Lev2.AP
    AERONET_SUN_V3L15_AOD_DAILY_NAME: AeronetSunV3Lev1.5.daily
    AERONET_SUN_V3L15_AOD_ALL_POINTS_NAME: AeronetSunV3Lev1.5.AP
    AERONET_SUN_V3L2_AOD_DAILY_NAME: AeronetSunV3Lev2.daily
    AERONET_SUN_V3L2_AOD_ALL_POINTS_NAME: AeronetSunV3Lev2.AP
    AERONET_SUN_V3L2_SDA_DAILY_NAME: AeronetSDAV3Lev2.daily
    AERONET_SUN_V3L2_SDA_ALL_POINTS_NAME: AeronetSDAV3Lev2.AP
    AERONET_INV_V3L15_DAILY_NAME: AeronetInvV3Lev1.5.daily
    AERONET_INV_V3L2_DAILY_NAME: AeronetInvV3Lev2.daily
    EBAS_MULTICOLUMN_NAME: EBASMC
    EEA_NAME: EEAAQeRep
    EARLINET_NAME: EARLINET
    DONOTCACHEFILE: /home/jonasg/pyaerocom/_cache/jonasg/DONOTCACHE


You can check if the relevant base directories ``MODELBASEDIR`` and
``OBSBASEDIR`` are valid.

.. code:: ipython3

    print("Base paths valid? %s" %pya.const.READY)


.. parsed-literal::

    OBS directory path /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSun2.0.SDA.AP/renamed does not exist
    OBS directory path /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev2.0.AP/renamed does not exist


.. parsed-literal::

    Base paths valid? True


The base directory for the databse search is:

.. code:: ipython3

    pya.const.BASEDIR




.. parsed-literal::

    '/lustre/storeA/project/aerocom/'



And the search directories for model and obs data are relative to the
base directory. They can be accessed via:

.. code:: ipython3

    pya.const.MODELDIRS




.. parsed-literal::

    ['/lustre/storeA/project/aerocom/aerocom1/',
     '/lustre/storeA/project/aerocom/aerocom2/',
     '/lustre/storeA/project/aerocom/aerocom-users-database/C3S-Aerosol',
     '/lustre/storeA/project/aerocom/aerocom-users-database/ECLIPSE',
     '/lustre/storeA/project/aerocom/aerocom-users-database/SATELLITE-DATA/',
     '/lustre/storeA/project/aerocom/aerocom-users-database/CCI-Aerosol/CCI_AEROSOL_Phase2/',
     '/lustre/storeA/project/aerocom/aerocom-users-database/ACCMIP/',
     '/lustre/storeA/project/aerocom/aerocom-users-database/ECMWF/',
     '/lustre/storeA/project/aerocom/aerocom2/EMEP_COPERNICUS/',
     '/lustre/storeA/project/aerocom/aerocom2/EMEP/',
     '/lustre/storeA/project/aerocom/aerocom2/EMEP_GLOBAL/',
     '/lustre/storeA/project/aerocom/aerocom2/EMEP_SVN_TEST/',
     '/lustre/storeA/project/aerocom/aerocom2/NorESM_SVN_TEST/',
     '/lustre/storeA/project/aerocom/aerocom2/INCA/',
     '/lustre/storeA/project/aerocom/aerocom-users-database/HTAP-PHASE-I/',
     '/lustre/storeA/project/aerocom/aerocom-users-database/HTAP-PHASE-II/',
     '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-I/',
     '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-II/',
     '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/',
     '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III-Trend/',
     '/lustre/storeA/project/aerocom/aerocom-users-database/CCI-Aerosol/CCI_AEROSOL_Phase1/',
     '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-II-IND3/',
     '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-II-IND2/']



And:

.. code:: ipython3

    pya.const.OBSDIRS




.. parsed-literal::

    ['/lustre/storeA/project/aerocom/',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunNRT',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetRaw2.0/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSun2.0AllPoints/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSun2.0.SDA.daily/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSun2.0.SDA.AP/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev1.5.daily/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev1.5.AP/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev2.0.daily/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev2.0.AP/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Aeronet.SDA.V3L1.5.daily/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Aeronet.SDA.V3L2.0.daily/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Aeronet.Inv.V2L1.5.daily/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Aeronet.Inv.V2L2.0.daily/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Aeronet.Inv.V3L1.5.daily/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Aeronet.Inv.V3L2.0.daily/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/EEA_AQeRep/renamed',
     '/lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/Earlinet/data']



On init, these are set to default directories (assuming to have access
to the Aerocom database). All subdirectories (relative to ``BASEDIR``)
that are not available are removed. So, what is returned when calling
the previous commands, is the directories that are accessible. If you
work locally and do not resemble this database structure, these 2 lists
will be likely empty. See below for instructions on how to set up
pyaerocom when working locally.

Browsing the database
^^^^^^^^^^^^^^^^^^^^^

Based on the defined paths, pyaerocom searches for data. Now, assuming
there is access to the database, you can use the ``browse_database``
method to search for available model or observational data using
`wildcard search <https://en.wikipedia.org/wiki/Wildcard_character>`__.
For instance, if you are interseted in data from MET Oslo, you can
e.g. search:

.. code:: ipython3

    pya.browse_database('CAM5*Oslo*')


.. parsed-literal::

    Found more than 20 matches for based on input string CAM5*Oslo*:
    
    Matches: ['CAM53-Oslo_cdaeb5e_MG15CLM45_7oct2016IHK_2006-2014', 'CAM53-Oslo_7310_MG15CLM45_5feb2017IHK_53OSLO_PI_UNTUNED', 'CAM5-Oslo_TEST-emi2000', 'CAM53-Oslo_re9f8_MG15CLM45_4feb2016AK_PD_MG15MegVadSOA', 'CAM53-Oslo_r470Nudge_150315AG_BF1NudgePD2000', 'CAM53-Oslo_7310_MG15CLM45_5feb2017AG_7310Nudge2000', 'CAM53-Oslo_r610Nudge_011015AK_SOA_r610_PD', 'CAM53-Oslo_6b76dca_MG15CLM45_22aug2016AK_PDaug16UVPSndg', 'CAM53-Oslo_7310_MG15CLM45_5feb2017IHK_53OSLO_PD_UNTUNED', 'CAM53-Oslo_r34afMG15CLM45_160120AG_34af_megan_2000_NDG', 'CAM53-Oslo_r773bNudge_151215AG_PD_DMS_733b', 'CAM53-Oslo_r512Nudge_150315AK_PD2000nudged', 'CAM53-Oslo_r670Nudge_011115AG_R670_PD', 'CAM53-Oslo_7310_MG15CLM45_5feb2017AG_7310AMIP1850V', 'CAM53-Oslo_cdaeb5e_MG15CLM45_7oct2016IHK_ERA_2001-2015', 'CAM53-Oslo_20161109AK_ERAndg', 'CAM5.3-Oslo_MG15CLM45_10jun2017_AK_2005-2010', 'CAM53-Oslo_7310_MG15CLM45_5feb2017AG_7310AMIP20002', 'CAM5-Oslo_FAMIPWARMCnudge-emi2000.A2.CTRL', 'CAM5.3-Oslo_INSITU', 'CAM5.3-Oslo_CTRL2016', 'CAM5.3-Oslo_AP3-CTRL2016-PD', 'CAM5.3-Oslo_AP3-CTRL2016-PI']
    
    To receive more detailed information, please specify search ID more accurately


Then, if you find something you are interested in, you can read the data
using the ``pyaerocom.ReadGridded`` class (which will be introduced in
more detail later). For instance:

.. code:: ipython3

    reader = pya.io.ReadGridded('CAM5.3-Oslo_CTRL2016')

The print() method get’s you some more info about what is in there, that
is, available variables, years and temporal resolutions:

.. code:: ipython3

    print(reader)


.. parsed-literal::

    
    Pyaerocom ReadGridded
    ---------------------
    Model ID: CAM5.3-Oslo_CTRL2016
    Data directory: /lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III/CAM5.3-Oslo_CTRL2016/renamed
    Available variables: ['abs550aer', 'deltaz3d', 'humidity3d', 'od440aer', 'od550aer', 'od550aer3d', 'od550aerh2o', 'od550dryaer', 'od550dust', 'od550lt1aer', 'od870aer']
    Available years: [2006, 2008, 2010]
    Available time resolutions ['3hourly', 'daily']


Working locally (Changing the paths)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you work on your local machine and you use the external AEROCOM user
server, you might need to change the path settings. The easiest way to
do this is to update the base directory where pyaerocom searches for
models.

.. code:: ipython3

    pya.const.BASEDIR = '/home/'


.. parsed-literal::

    Model directory base path does not exist and will be removed from search tree: /home/aerocom1/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom2/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/C3S-Aerosol
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/ECLIPSE
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/SATELLITE-DATA/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/CCI-Aerosol/CCI_AEROSOL_Phase2/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/ACCMIP/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/ECMWF/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom2/EMEP_COPERNICUS/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom2/EMEP/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom2/EMEP_GLOBAL/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom2/EMEP_SVN_TEST/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom2/NorESM_SVN_TEST/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom2/INCA/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/HTAP-PHASE-I/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/HTAP-PHASE-II/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/AEROCOM-PHASE-I/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/AEROCOM-PHASE-II/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/AEROCOM-PHASE-III/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/AEROCOM-PHASE-III-Trend/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/CCI-Aerosol/CCI_AEROSOL_Phase1/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/AEROCOM-PHASE-II-IND3/
    Model directory base path does not exist and will be removed from search tree: /home/aerocom-users-database/AEROCOM-PHASE-II-IND2/
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/AeronetSunNRT does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/AeronetRaw2.0/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/AeronetSun2.0AllPoints/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/AeronetSun2.0.SDA.daily/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/AeronetSun2.0.SDA.AP/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev1.5.daily/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev1.5.AP/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev2.0.daily/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev2.0.AP/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/Aeronet.SDA.V3L1.5.daily/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/Aeronet.SDA.V3L2.0.daily/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/ does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/Aeronet.Inv.V2L1.5.daily/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/ does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/Aeronet.Inv.V2L2.0.daily/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/ does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/Aeronet.Inv.V3L1.5.daily/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/Aeronet.Inv.V3L2.0.daily/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/EBASMultiColumn/data does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/EEA_AQeRep/renamed does not exist
    OBS directory path /home/aerocom1/AEROCOM_OBSDATA/Earlinet/data does not exist


Now, since there is actually nothing below this base directory that
matches the predefined search patterns, the list specifying search
directories is empty.

.. code:: ipython3

    pya.const.MODELDIRS




.. parsed-literal::

    []



Reading the aerosol optical detph at 550nm using a specified model ID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The resulting list shows possible options that were found in the
database. Let’s choose the *CAM5.3-Oslo_CTRL2016* run and import the
data. In the following cell, we directly instantiate a read class for
data import since we know the model and run ID from the previous cell
(the read class basically includes the above used search method).

Before we can read from the database, we have to reset the paths in the
configuration.

.. code:: ipython3

    pya.const.reload(keep_basedirs=False)
    pya.const.READY


.. parsed-literal::

    OBS directory path /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSun2.0.SDA.AP/renamed does not exist
    OBS directory path /lustre/storeA/project/aerocom/aerocom1/AEROCOM_OBSDATA/AeronetSunV3Lev2.0.AP/renamed does not exist




.. parsed-literal::

    True



.. code:: ipython3

    read = pya.io.ReadGridded("CAM5.3-Oslo_CTRL2016")

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

    data = read.read("od550aer", start="1 march 2010", stop="31 march 2010")[0]

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



.. image:: tut00_get_started/tut00_get_started_33_0.png


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

    <matplotlib.axes._subplots.AxesSubplot at 0x7f2d7825dda0>




.. image:: tut00_get_started/tut00_get_started_36_1.png


The following notebook introduces in more detail how pyaerocom handles
regions and where they can be defined. In the subsequent tutorial, the
``ReadGridded`` class is introduced, that was usesed above to import
model data in a flexible way based on variable name, time range and
temporal resolution. The loaded data for each model and variable is then
stored in the analysis class ``GriddedData`` which we use in the end of
this notebook and which will be introduced in a later tutorial.
