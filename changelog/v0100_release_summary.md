* Land sea masks?
* Filter class?
- Renamed class ReadSulphurAasEtAl to ReadAasEtal (old name still works) and fixed some bugs and did some cleanup in that class

Test improvements
* Replace many tests relying on lustre to work with test dataset.
* Added conftest.py for defining session wide test fixtures and updated/reafctured all relevant tests accordingly


Reading Data
- New class for reading GHOST data (ReadGhost)

- Support for reading EMEP data (ReadMscwCtm)


GriddedData
* GriddedData.to_xarray
* GriddedData timeseries extraction is now more robust against memory errors and uses xarray
* GriddedData.to_netcdf
* GriddedData.resample_time can now also apply resampling constraints;

UngriddedData
* UngriddedData.filter_region can now also handle country names
* Remove option to provide filter_name in UngriddedData.plot_station_coordinates (filtering should be done before)
* New property method countries_available in UngriddedData
* Implement save_as and from_cache in UngriddedData
* UngriddedData: Add beta version of method from_station_data

StationData
- API CHANGE): StationData.resample_timeseries is deprecated (but still works) and usage of new method resample_time is recommended (which returns instance of StationData other than pd.Series); new method copy in StationData

ColocatedData
* _filter_country, apply_country_filter, countries_available, check_set_countries, _get_stat_coords and implement country filtering in filter_region
* get_country_codes

Helpers
* Added new method make_datetime_index in helpers.py
* Added method read_obsdata in AerocomEvaluation class
* Added lowlevel method calc_climatology in helpers.py;
* Added new method calc_climatology to StationData

Climatology

CacheHanglerUngridded
* Add option force_use_outdated
* Modify CacheHandlerUngridded so that it can also handle custom filenames
* Added method delete_all_cache_files in CacheHanglerUngridded

ReadGridded
* Improve flexibility related to multiple vert_code matches using new method get_vert_code in Variable class

ReadUngridded
* Add option only_cached
* Add input option data_dir to ReadUngridded
* ReadUngridded can now also handle post computation with merge method combine
* Major update to ReadUngridded: incorporate logic for post-computation of variables (BETA)


Colocation
* Refined time resampling strategy in colocate_gridded_ungridded (resampling constraints are now applied also in main loop)
* (UNDER DEVELOPMENT): add new attr. resample_how to ColocationSetup (not being used so far, related to #88)
* resample_how option in high level colocation routines
* Add flexible selection of model reader
* Add option of setting gridded reader for observations in Colocator
* MAJOR ANALYSIS CHANGE: outliers in gridded / gridded colocation are now removed in original resolution
* Finish first draft of ungridded / ungridded base colocation routine
* Updated gridded/gridded colocation so that it regrids to the lowest of both resolutions


Config
* add_ungridded_post_dataset

Plotting
* New method in plot/mapping.py for plotting bias maps from ColocatedData

Aerocom Evaluation
* Added method for reordering experiments in menu.json for Aerocom Evaluation interface
* New method read_ungridded_obsdata
* AerocomEvaluation now applies weighted statistics to gridded/gridded colocated objects, in heatmap
* (UNDER DEVELOPMENT): add new attrs. resample_how to AerocomEvalation (not being used so far, related to #88) and regions_how, which is used in processing of json files from colocateddata (upcoming commit, related to #90)
* store config in experiment directory
* Daily and monthly heatmaps
* Regional timeseries
* Diurnal processing
* web_interface_name option for obs_config in web processing
* Added support for country-regional diurnal time series
Added functionality in mathutils to compute weighted statistics

web
* web/utils/compute_model_average_and_diversity now also outputs fields for 1. and 3. quantiles

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

