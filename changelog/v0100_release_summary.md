# pyaerocom version 0.10.0

This release comes with many new features, major improvements and a more stable API. Please see the individual points below for major changes.

**PLEASE NOTE**: the below listed updates comprise the most important updates but do not represent a list of ***all*** changes applied.

## New feature modules

Modules that contain new features. See [here](https://github.com/metno/pyaerocom/blob/master/changelog/diff_files_v080_v0100.md) for a list of all file modifications between version 0.8.0 and 0.10.0.

-	**pyaerocom/combine_vardata_ungridded.py**: Colocation of ungridded data
-	**pyaerocom/helpers_landsea_masks.py**: Access and helpers for land-sea mask filtering
-	**pyaerocom/io/read_ghost.py**: reading routine for GHOST dataset (provided by Barcelona Supercomputing Center, BSC)
-	**pyaerocom/io/read_mscw_ctm.py**: Reading interface for EMEP data
-	**pyaerocom/molmasses.py**: helpers related to access of molecular masses for species
-	**pyaerocom/trends_engine.py**: Interface for computing trends using the method by [Mortier et al., 2020](https://acp.copernicus.org/articles/20/13355/2020/acp-20-13355-2020.html).
-	**pyaerocom/web/helpers_evaluation_iface.py**: helper methods for conversion of `ColocatedData` to json files for [Aerocom Evaluation interface](https://aerocom-evaluation.met.no/main.php?project=aerocom&exp=glissetal-2020)
-	**pyaerocom/web/helpers_trends_iface.py**: helper methods for conversion of `ColocatedData` to json files for [Aerocom trends interface](https://aerocom-trends.met.no/)
-	**pyaerocom/web/utils.py**: High-level methods based on results from standard Aerocom analysis. Currently. this contains a method `compute_model_average_and_diversity` which can be used to compute ensemble median or mean modeldata (e.g. used to compute AEROCOM-MEDIAN and MEAN in [Gliss et al., 2020 (ACPD, accepted for pubclication in ACP](https://acp.copernicus.org/preprints/acp-2019-1214/)).

## Updates related to supported observation data-sets and naming conventions

- Support for reading GHOST data.
- Support for reading of EMEP model data.

## Reading of data

- `ReadGridded`
  - Improve flexibility related to multiple vert_code matches using new method get_vert_code in Variable class.

- `ReadUngridded`
  - Add option only_cached to only read cached data f.e. when working offline
  - ReadUngridded can post compute variables with merge method combine

- **New**: Class `ReadMscvCtm` for reading of EMEP model data

## Main data objects
- `GriddedData`
  - Can be converted to xarray or stored as netcdf files.
  - More robust time-series extraction.
  - Constraints can be applied during temporal resampling (i.e. hierarchical `min_num_obs` or `how`).
  - Improving automatic retrieval of lowest layer for profile data using CF attr. "positive".
  - Method `mean` now uses area weighted mean by default.
  - New methods: `years_avail`, `split_years`, `mean_at_coords`, `filter_altitude`, `filter_region`, `apply_region_mask`, `aerocom_savename`, `to_xarray`, `area_weighted_mean`


- `UngriddedData`
  - Can be filtered by country names
  - Can now be saved as pickled objects
  - Create UngriddedData from StationData object(s)
  - Colocation of UngriddedData is now possible (relevant code is in new module `combine_vardata_ungridded.py`)
  - Support for wildcards in station data conversion methods.
  - New attrs. (incl. decorators): `last_meta_idx`, `nonunique_station_names`, `countries_available`
  - New methods: `from_station_data` (static method), `check_set_country`, `check_convert_var_units`, `filter_altitude`, `filter_region`, `apply_region_mask`, `colocate_vardata`, `save_as`, `from_cache` (static method)

- `ColocatedData`
  - Implement method to compute regional time-series.
  - Support automatic assignments of countries for each site.
  - Support computation of area weighted statistics in `calc_statistics`.
  - New attributes: `has_time_dim`, `has_latlon_dims`, `countries_available`, `country_codes_available`, `area_weights`
  - New methods: `get_country_codes`, `calc_area_weights`, `flatten_latlondim_station_name`, `stack`, `unstack`, `check_set_countries`, `filter_altitude`, `apply_country_filter`, `set_zeros_nan`, `apply_region_mask`, `filter_region`, `get_regional_timeseries`

- `StationData`
  - Computation of climatological time-series
  - Improved handling of metadata access (`get_meta`) and merging of metadata
  - `resample_timeseries` was renamed to `resample_time` (but old version still works.)
  - new method `StationData.copy`


## Colocation of data

### Low-level colocation routines (`colocation.py`)
  - Outliers in gridded/gridded colocation are now removed in original resolution.
  - Gridded/gridded colocation now re-grids to the lowest of both resolutions.
  - Add option resample_how, which can also be applied hierarchical, like `min_num_obs` (e.g. used to resample O3max).
  - `resample_how` option in high level colocation routines.
  - Option to use obs climatology for gridded / ungridded colocation.
  - New helper method `correct_model_stp_coldata` in `colocation.py` which applies STP correction to a colocated data object containing obs at STP based on station altitude and temperature derived from ERA Interim data (BETA feature only working for 2010 data and with access to METNo infrastructure).
  - Some bug fixes for certain edge cases.

### High-level colocation routines (`colocation_auto.py`)

Affects classes `ColocationSetup` and `Colocator`

- Support new EMEP reading routine.
- Model and obsdata directories can be specified explicitly.
- Option `model_to_stp` (BETA feature which will not work in most cases, see above).
- New attrs. `obs_add_meta`, `resample_how`.
- New methods (`Colocator`): `read_model_data`, `read_ungridded`

## Filtering of data

  - Implement filtering of binary masks for `GriddedData`, `UngriddedData` and `ColocatedData`
  - Harmonise API of spatial filtering in data classes (i.e. method `filter_region` that can handle rectangular and binary region masks)
  - Automatic access to HTAP binary land-sea masks
  - Handling of binary and rectangular regions in `Filter` class.

## Other updates

- **config.py** (`Config` class)
  - Major improvements and API changes, e.g. related to automatic setup and adding new data search directories and ungridded observations.
  - In particular, attrs. `BASEDIR`, `MODELBASEDIR`, `OBSBASEDIR` are deprecated.
  - Instead, methods `add_data_search_dir` and `add_ungridded_obs` can be used to register data locations.

- **geodesy.py**: new methods `calc_latlon_dists`, `find_coord_indices_within_distance`, `get_country_info_coords`.
- New methods in `helpers.py`, the most relevant ones are `extract_latlon_dataarray`, `make_dummy_cube_latlon`, `numpy_to_cube`, `sort_ts_types`, `calc_climatology`
- New methods in `mathutils.py`: `weighted_sum`, `sum`, `weighted_mean`, `weighted_cov`, `weighted_corr`, `corr` (which were implemented in `calc_statistics`), `vmrx_to_concx`, `concx_to_vmrx`
- New class `AerocomDataID` in **metastandards.py** (is used in `ReadGridded` to separate data ID into metadata based on AeroCom 3 conventions.)  
- New helper classes `ObsVarCombi` and `AuxInfoUngridded` in `obs_io.py`.
- `region.py`: New method `Region.plot` and support for binary regions.
- `TimeResampler`: implement handling of `how` to specify aggregating kernel (e.g. mean, max, min, std...)
- New and interactive tutorials, for details see [pyaerocom-tutorials repo](https://github.com/metno/pyaerocom-tutorials).
- **NEW**: colocation routine for ungridded data, the relevant code is in ne module `test_combine_vardata_ungridded.py`). NOTE: currently only implemented to create colocated `UngriddedData` objects, a routine that outputs `ColocatedData` object will come in v0.11.0.
- **tstype.py** (class `TsType`)
  - Implement setter method for `mulfac`
  - New attrs (incl. @property decorators): `TO_NUMPY`, `RS_OFFSETS` (not in use), `TSTR_TO_CF`, `datetime64_str`, `timedelta64_str`, `cf_base_unit`, `next_lower`, `next_higher`
  - New methods: `to_timedelta64`, `valid`, `to_numpy_freq`
  - Rename method `to_pandas` to `to_pandas_freq`
- **variable.py**
  - Define wildcard based lookup of default vertical codes for variable families (in `VarNameInfo`) and related class method `get_default_vert_code` (experimental)
  - new helper function `get_emep_variables`
  - `Variable` class
    - New attrs (incl. @property decorators): `var_name_aerocom`, `default_vert_code`, `var_name_input`, `is_3d`, `is_wavelength_dependent`, `is_dry`, `is_alias`
    - New methods: `get_default_vert_code`, `__eq__`
  - `VarCollection` class
    - support adding new variables (in addition to the ones defined in an ini file)
    - New methods: `add_var`, `get_var`

## Plotting (`pyaerocom.plot` sub-package)

- New method `plot_nmb_map_colocateddata` in plot/mapping.py for plotting bias maps from `ColocatedData`

## Aerocom Evaluation web processing tools

- Store a copy of the config file in experiment output directory.
- New method `AerocomEvaluation.read_ungridded_obsdata`.
- Option `weighted_stats` in `AerocomEvaluation` (if active, weighted statistics are applied to gridded/gridded colocated objects in heatmap
- Create json files for daily and monthly heat-maps
- Support also country based regional statistics (`AerocomEvaluation.regions_how`)
- Regional time-series are now computed automatically for all regions.
- Support evaluation of diurnal (hourly data).
- utility function `compute_model_average_and_diversity` now also outputs fields for 1. and 3. quantiles (median) and std. (mean)

## Major API changes:

- Renamed class ReadSulphurAasEtAl to ReadAasEtal
- StationData.resample_timeseries is deprecated (but still works) and usage of new method resample_time is recommended

## Testing and CI

- Most tests now uses a publicly available test dataset.
- Implemented automatic CI testing in Github actions.
- Added conftest.py for defining session wide test fixtures.
- Many more tests resulting in largely improved test coverage, [see here]([here](https://github.com/metno/pyaerocom/blob/master/changelog/diff_files_v080_v0100.md).

## Bug fixes

- Fix bug related to merging of `StationData` in case of overlapping time-series (issue [106](https://github.com/metno/pyaerocom/issues/106)).
- Fix minor bug in AerocomEvaluation.clean_json_files method (crashed when webname of one obsconfig entry was changed)
- Fix bug in aerocom_evaluation (skip missing heatmaps file (e.g. daily) when updating interface)
- Fix bug related to col_freq vs. ts_type in colocate_gridded_ungridded (issue 85)
- Fix minor bug in AerocomDataID
- Fix bug in method GriddedData.change_base_year
- Fix bug in mathutils.calc_statistics
- Fixed bug in handling source ts_type in gridded/gridded colocation routine
- ReadEbas: Fixed bug related to column selection for wavelength range which identified data columns as valid if there was only one column match for var of interest
- Fixed minor bug in reordering of dimensions of GriddedData when one dimension definition was missing
- Fixed bug in GriddedData.crop due to time bounds not removed correctly
