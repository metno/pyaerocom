* Land sea masks?

Test improvements
- Most tests now uses a publicly available test dataset
- Added conftest.py for defining session wide test fixtures

Spatial filtering of gridded and ungridded data objects

Reading Data
- Support for reading GHOST data (ReadGhost)
- Support for reading EMEP data (ReadMscwCtm)

ReadGridded
* Improve flexibility related to multiple vert_code matches using new method get_vert_code in Variable class

GriddedData
- Can be converted to xarray or stored as netcdf files
- More robust timeseries extraction
- Constraints can be applied during temporal resampling

ReadUngridded
- Add option only_cached to only read cached data f.e. when working offline
* ReadUngridded can post compute variables with merge method combine

UngriddedData
- Can be filtered by country names
- Can now be saved as pickled objects
- Create UngriddedData from StationData object(s)

CacheHandlerUngridded
- Modified to handle custom filenames
- Added method delete_all_cache_files
- Add option force_use_outdated

Colocation
- Outliers in gridded/gridded colocation are now removed in original resolution
- Ungridded/ungridded colocation routine
- Gridded/gridded colocation now regrids to the lowest of both resolutions
- Add option resample_how
* resample_how option in high level colocation routines

Plotting
- New method plot_nmb_map_colocateddata in plot/mapping.py for plotting bias maps from ColocatedData

Web processing
- compute_model_average_and_diversity now also outputs fields for 1. and 3. quantiles

Aerocom Evaluation
- Store a copy of the config file in experiment output directory
* New method read_ungridded_obsdata
- AerocomEvaluation now applies weighted statistics to gridded/gridded colocated objects in heatmap
- Create json files for daily and monthly heatmaps
- Regional timeseries
- Diurnal processing

API changes:
- Renamed class ReadSulphurAasEtAl to ReadAasEtal
- StationData.resample_timeseries is deprecated (but still works) and usage of new method resample_time is recommended

### Bugfixes

- minor bug fix in mapping.py
- Fix minor bug in AerocomEvaluation.clean_json_files method (crashed when webname of one obsconfig entry was changed)
- Fix minor bug in updated GriddedData.remove_outliers
- Fix bug in TimeResampler (failed to generate resample index if min_num_obs is numerical, after recent update to consider resample_how); increase verbosity in Colocator if colocation fails
- Fix bug in aerocom_evaluation (skip missing heatmaps file (e.g. daily) when updating interface)
- Fix minor bug related to plotting of binary regions
- Fix minor bug due to recent changes in web processing (related to #90)
- Fix a bug in the revised flow for colocation_auto.py to work with GHOST data
- Fix bug in GriddedData._resample_time_xarray (check dimcoords was not in try / except block
- Fix bug related to col_freq vs. ts_type in colocate_gridded_ungridded (fixes #85)
- Fix minor bug in AerocomDataID
- Fix bug in method GriddedData.change_base_year
- Fix bug in mathutils.calc_statistics
- Minor bug fix in readaeronetbase (unit retrieval); Replaced "except:" with "except Exception:" in all Aeronet reading routines
- Fixed minor bug in change_verbosity
- Fixed some bugs and code cleanup in module land_sea_mask which was renamed to helpers_landsea_masks
- Fixed minor bug in GriddedData.to_time_series (if used for single coordinate)
- Fixed minor bug in colocation.py (that was introduced very recently and identified via failing getting started tutorial)
- Fixed minor import bug in filter.py
- Fixed minor bug in extract_latlon_dataarray in helpers.py
- Fixed bug in handling source ts_type in gridded/gridded colocation routine and added new (BETA) helper method correct_model_stp_coldata to colocation.py
- Fix bug in plotting routine regions
- Fixed bug related to column selection for wavelength range which identified data columns as valid if there was only one column match for var of interest
- Fixed bug in ColocatedData.calc_nmb_array
- Generalised and cleaned up filter_region method and fixed bug (wrong return value) therein; added new (BETA)  methods to ColocatedData: calc_nmb_array, _iter_stats, unstack, stack, flatten_latlondim_station_name
- Fixed bug in helpers.resample_time_dataarray (only relevant for multiyear datasets)
- Fixed minor bug in colocate_gridded_ungridded
- Fix bug with import of const
- Fixed bug related to import of const from pyaercom
- Fixed bug for reding multiple regions using xarray
- Fixed minor bug in AerocomEvaluation cleanup method
- Fixed bug in NAFRICA
- Fixed bug arising from HTAP regions being available in regions.ini now that lead to crash in method regions.find_closest_region_coord
- Fixed minor bug in reordering of dimensions of GriddedData when one dimension definition was missing
- Fixed minor bug in GriddedData.load_input
- Minor bug fix (introduced in last commit)
- Fixed minor bug in colocation routine arising in cases where model data var_name is not known by AeroCom
- Fixed minor bug in trends computation for storage of metadata in TrendsEngine)
- Gliss	Fixed minor bug in trends computation helper routine
- Fixed bug in GriddedData.crop due to time bounds not removed correctly (Abisko, pyaerocom-testdata)

