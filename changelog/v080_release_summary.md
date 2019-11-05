This release comprises major improvements, changes and many new features compared to the last release (comprising about 10 months of development time). Thus, below we only summarise the most important changes. For a list of all changes, please see the changelog file of this release (in subdirectory changelog).

- New sub-package `web` (tools for high-level web processing)
  - Contains frameworks and routines for high level analysis of data and computation of json files both for AeroCom evaluation and trends web interfaces.
  - Includes 2 simple command line interfaces *pyaeroeval* and *pyaerotrends* for web processing
  - Main classes:
    - `AerocomEvaluation` for processing of data displayed at https://aerocom-evaluation.met.no/
    - `TrendsEvaluation` for data displayed at https://aerocom-trends.met.no/

- Gridded reading (`ReadGridded` class and methods used therein)
  - `data_dir` can be provided directly on input in `ReadGridded` (e.g. for working locally with no database access). However, data files are required to be in AeroCom naming convention.
  - og550gtaer is now primarily computed via od550aer-od550lt1aer
  - easy file filtering for all attributes accessible via filename (e.g. model, variable, year, vertical type)
  - option to compute variables during runtime for custom methods
  - Clean up of outdated methods
  - improved logic of processing work-flow, especially for computation of variables and handling of 4D files, e.g.
    - use ModelLevel files if Surface is requested but not available
    - Compute mass concentration fields (`concXX`) from mass mixing ratios (`mmrXX`) and density (`rho`) fields
  - Reading of climatological data (i.e. year 9999 in filename). Remark: tricky, because pandas cannot handle timestamps with year 9999  
  - More flexible options for reading of iris cubes (`iris_io.py`)
  - Improved check and correction of invalid time dimensions in source files

- Ungridded reading (Reading of observations)
    - EBAS: implemented framekwork for computation of variables from variables that can be read (or computed)
    - EBAS: evaluate and use flag columns (flagged data added to new flag column in `UngriddedData` object)
    - EBAS: support all occurring sampling frequencies (e.g. weekly, 2daily, etc.)
    - EBAS: default now reads raw (i.e. as is in NASA Ames files), but writes all relevant information for filtering (e.g. datalevel, flags) into output `UngriddedData` object, which can then be filtered flexibly after reading
    - New reading routine for GAW ascii format
    - New reading routine for data subset from trends paper by Aas et al.
    - Updated EARLINET reading routine after major changes in format (Feb. 2019)
    - More flexible handling of cached data objects in `ReadUngridded` (cf. changes in caching strategy below)

- Data classes
  - `StationData`
    - Merging of multiple instances possible (including metadata merging and handling of overlapping data)
    - Removed attrs. stat_lon, stat_lat, stat_alt
    - Support trends computation and visualisation
    - Support profile data

  - `UngriddedData`
    - Support for flags and error data
    - Outlier removal
    - More flexible and robust conversion into StationData
    - More advanced filtering and subsetting (e.g. extract single variable)
    - Methods for merging of several instances
    - Added __iter__ method (looping over data object -> returns StationData at each index, BETA)

  - `GriddedData`
    - More flexible subsetting (e.g. sel method)
    - Method to automatically infer surface level for 3D data
    - Cleaned up attributes: now everything is stored within underlying cube (i.e. attr. `suppl_info` is deperecated)
    - Added CF attributes such as `standard_name` and `long_name`
    - WORK IN PROGRESS: altitude access for 4D fields via `get_altitude` method (cleaned up and refactored old code due to below mentioned updates in mod `vert_coords.py`)
    - option to add metadata when converting to timeseries (`StationData`) at distinct locations

  - `ColocatedData`
    - Updated I/O and naming conventions
    - Region filtering
    - time resampling
  - All data classes contain many more helper and analysis methods and attributes, that are not explicitely mentioned here, for details see changelog

- Colocation: Improved flexibility and robustness of colocation routines (modules `colocation.py`, `colocation_auto.py`), e.g.
  - more control on individual outlier removal for both input datasets
  - hierarchical resampling
  - option for outlier removal
  - option for unit harmonisation
  - option for colocating time before downsampling
  - option to ignore certain station names (for gridded / ungridded colocation)
  - colocation with climatology data
  - High level interface (`Colocator` class) for automatic colocation, e.g. used in `AerocomEvaluation` class for web processing.

- Other changes:
  - Updated method `calc_statistics`: biases (NMB, MNMB) and FGE are now computed only from positive values
  - New modules `units_helpers.py` providing custom unit conversion, e.g. for non-CF conform units in data files (e.g. sulphur specific mass concentration data: ug S m-3)
  - Improved caching stragegy (now single variable instances of `UngriddedData` are cached)
  - Easier installation options
  - Support for simple geographical calculations
  - New helpers and processing methods in `region.py`
  - Support for more variables
  - Advanced and unified time resampling in `TimeResampler` class
  - More CF-compliant (e.g. `units` attr. in data classes)
  - More flexible and unified handling (and sharing) of metadata among different data objects
  - Methods for trends computation (class `TrendsEngine`)
  - Major improvements in ungridded caching using single variable cache files for I/O
  - Bug fixes
  - New class `TsType` for handling and comparing temporal resolutions (in new mod `tstype.py`)
  - More flexible tests (using pytest markers that check access to database)
  - Worked on implementation of vertical coordinate to altitude conversion methods (WORK IN PROGRESS, mod. `vert_coords.py`)

- API changes:
  - `Station` class is deprecated
  - `ReadGriddedMulti` is deprecated (but still works)
  - sconc variables are deprecated (but still work): use conc instead (e.g. concso4 instead of sconcso4)
  - Renaming of classes / modules:
    - `AllVariables` to `VarCollection`
    - `unit` to `units`
    - Moved `GridIO` class from `config.py` to dedicated new module `grid_io.py`
    - Global setup dictionaries for time conversion moved from `helpers.py` to `time_config.py`

- Not finished / under development / coming soon
  - Handling of vertical model coordinates
  - Colocation of profile data
  - Filtering by land / sea masks
  - Computation of regional average time series in data objects

- Planned major changes for v0.9.0:
  - API refactor: StationData based on xarray.Dataset (currently variable data can be either numpy array, pandas Series or xarray)
  - Include filtering using land / sea masks (should work for `GriddedData`, `UngriddedData`, `ColocatedData`)
  - 4D data (ModelLevel):
    - conversion of vertical level coordinates to altitude
    - profile colocation (would add additional vertical dimension to `Colocateddata`)
    - Retrieval of aerosol layer height (PRODUCT)
    - Default vertical domains for vertical aggregation (particularly for web interfaces, e.g. 0-2km, 2-6km, >6km)
