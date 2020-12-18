Created automatically via:

```bash
git diff --name-status v0.8.0 HEAD
```

And modified afterwards.

## New modules

### New feature modules
-	pyaerocom/combine_vardata_ungridded.py

### New ini files

-	pyaerocom/data/emep_variables.ini
-	pyaerocom/data/paths_local_database.ini
-	pyaerocom/helpers_landsea_masks.py
-	pyaerocom/io/read_ghost.py
-	pyaerocom/io/read_mscw_ctm.py
-	pyaerocom/molmasses.py
-	pyaerocom/trends_engine.py
-	pyaerocom/web/helpers_evaluation_iface.py
-	pyaerocom/web/helpers_trends_iface.py
-	pyaerocom/web/utils.py

### Others

-	.github/workflows/CI.yml
-	changelog/CHANGELOG_v080_v0100.rst
-	changelog/v0100_release_summary.md
-	pyaerocom/_conftest_helpers.py
-	pyaerocom/_init_helpers.py
-	pyaerocom/conftest.py
-	pyaerocom/io/ghost_meta_keys.py
-	pyaerocom/scripts/cli.py
-	pyaerocom/scripts/highlevel_utils.py
-	pyaerocom/scripts/read_colocation_files.py
-	pyaerocom/testdata_access.py
-	pyaerocom/web/const.py

### New test-modules

-	pyaerocom/web/test/test_aerocom_evaluation.py
-	pyaerocom/web/test/test_helpers.py
-	pyaerocom/web/test/test_helpers_evaluation_iface.py
-	pyaerocom/io/test/test_aerocom_browser.py
-	pyaerocom/io/test/test_cachehandler_ungridded.py
-	pyaerocom/io/test/test_ebas_varinfo.py
-	pyaerocom/io/test/test_ghost_meta_keys.py
-	pyaerocom/io/test/test_read_aasetal.py
-	pyaerocom/io/test/test_read_ebas.py
-	pyaerocom/io/test/test_read_ghost.py
-	pyaerocom/io/test/test_read_mscw_ctm.py
-	pyaerocom/io/test/test_utils.py
-	pyaerocom/test/test_colocation.py
-	pyaerocom/test/test_colocation_auto.py
-	pyaerocom/test/test_combine_vardata_ungridded.py
-	pyaerocom/test/test_config.py
-	pyaerocom/test/test_filter.py
-	pyaerocom/test/test_helpers_landsea_masks.py
-	pyaerocom/test/test_metastandards.py
-	pyaerocom/test/test_molmasses.py
-	pyaerocom/test/test_obs_io.py
-	pyaerocom/test/test_testdata_access.py
-	pyaerocom/test/test_trends_engine.py
-	pyaerocom/test/test_variable.py
-	pyaerocom/test/test_zz_unsorted_highlevel.py

## Modified modules
-	.gitignore
-	README.rst
-	VERSION.md
-	docs/Makefile
-	docs/api.rst
-	docs/conf.py
-	docs/index.rst
-	docs/make.bat
-	pyaerocom/__init__.py
-	pyaerocom/_lowlevel_helpers.py
-	pyaerocom/colocateddata.py
-	pyaerocom/colocation.py
-	pyaerocom/colocation_auto.py
-	pyaerocom/config.py
-	pyaerocom/data/_create_var_csv_from_htap2_exceltab.py
-	pyaerocom/data/aliases.ini
-	pyaerocom/data/coords.ini
-	pyaerocom/data/data_sources.ini
-	pyaerocom/data/ebas_config.ini
-	pyaerocom/data/paths.ini
-	pyaerocom/data/paths_testdata.ini
-	pyaerocom/data/paths_user_server.ini
-	pyaerocom/data/regions.ini
-	pyaerocom/data/test_files.ini
-	pyaerocom/data/variables.ini
-	pyaerocom/exceptions.py
-	pyaerocom/filter.py
-	pyaerocom/geodesy.py
-	pyaerocom/grid_io.py
-	pyaerocom/griddeddata.py
-	pyaerocom/helpers.py
-	pyaerocom/interactive/__init__.py
-	pyaerocom/interactive/ipywidgets.py
-	pyaerocom/io/__init__.py
-	pyaerocom/io/aerocom_browser.py
-	pyaerocom/io/aux_read_cubes.py
-	pyaerocom/io/cachehandler_ungridded.py
-	pyaerocom/io/ebas_file_index.py
-	pyaerocom/io/ebas_nasa_ames.py
-	pyaerocom/io/ebas_varinfo.py
-	pyaerocom/io/fileconventions.py
-	pyaerocom/io/helpers.py
-	pyaerocom/io/helpers_units.py
-	pyaerocom/io/iris_io.py
-	pyaerocom/io/read_aasetal.py
-	pyaerocom/io/read_aeolus_l2a_data.py
-	pyaerocom/io/read_aeronet_invv2.py
-	pyaerocom/io/read_aeronet_invv3.py
-	pyaerocom/io/read_aeronet_sdav2.py
-	pyaerocom/io/read_aeronet_sdav3.py
-	pyaerocom/io/read_aeronet_sunv2.py
-	pyaerocom/io/read_aeronet_sunv3.py
-	pyaerocom/io/read_airbase.py
-	pyaerocom/io/read_earlinet.py
-	pyaerocom/io/read_ebas.py
-	pyaerocom/io/read_gaw.py
-	pyaerocom/io/read_sentinel5p_data.py
-	pyaerocom/io/readaeronetbase.py
-	pyaerocom/io/readgridded.py
-	pyaerocom/io/readsatellitel2base.py
-	pyaerocom/io/readungridded.py
-	pyaerocom/io/readungriddedbase.py
-	pyaerocom/io/test/test_read_aeronet_invv3.py
-	pyaerocom/io/test/test_read_aeronet_sdav2.py
-	pyaerocom/io/test/test_read_aeronet_sdav3.py
-	pyaerocom/io/test/test_read_aeronet_sunv2.py
-	pyaerocom/io/test/test_read_aeronet_sunv3.py
-	pyaerocom/io/test/test_read_earlinet.py
-	pyaerocom/io/test/test_readgridded.py
-	pyaerocom/io/test/test_readungridded.py
-	pyaerocom/io/testfiles.py
-	pyaerocom/io/utils.py
-	pyaerocom/mathutils.py
-	pyaerocom/metastandards.py
-	pyaerocom/obs_io.py
-	pyaerocom/plot/__init__.py
-	pyaerocom/plot/_sorted_out/plot_map_OLD.py
-	pyaerocom/plot/config.py
-	pyaerocom/plot/heatmaps.py
-	pyaerocom/plot/helpers.py
-	pyaerocom/plot/mapping.py
-	pyaerocom/plot/plotcoordinates.py
-	pyaerocom/plot/plotmaps.py
-	pyaerocom/plot/plotscatter.py
-	pyaerocom/plot/plotscatter_v0.py
-	pyaerocom/plot/plotseries.py
-	pyaerocom/plot/plotsitelocation.py
-	pyaerocom/region.py
-	pyaerocom/scripts/__init__.py
-	pyaerocom/scripts/main.py
-	pyaerocom/stationdata.py
-	pyaerocom/test/__init__.py
-	pyaerocom/test/synthetic_data.py
-	pyaerocom/test/test_colocateddata.py
-	pyaerocom/test/test_dms_gaw.py
-	pyaerocom/test/test_ebas_sample_stats.py
-	pyaerocom/test/test_geodesy.py
-	pyaerocom/test/test_griddeddata.py
-	pyaerocom/test/test_helpers.py
-	pyaerocom/test/test_mathutils.py
-	pyaerocom/test/test_obsdata_versions.py
-	pyaerocom/test/test_stationdata.py
-	pyaerocom/test/test_tstype.py
-	pyaerocom/test/test_ungriddeddata.py
-	pyaerocom/test/test_units_helpers.py
-	pyaerocom/time_config.py
-	pyaerocom/time_resampler.py
-	pyaerocom/trends_helpers.py
-	pyaerocom/tstype.py
-	pyaerocom/ungriddeddata.py
-	pyaerocom/units_helpers.py
-	pyaerocom/utils.py
-	pyaerocom/variable.py
-	pyaerocom/vert_coords.py
-	pyaerocom/vertical_profile.py
-	pyaerocom/web/__init__.py
-	pyaerocom/web/aerocom_evaluation.py
-	pyaerocom/web/cli/main_aerocom_evaluation.py
-	pyaerocom/web/cli/main_trends_evaluation.py
-	pyaerocom/web/helpers.py
-	pyaerocom/web/obs_config_default.py
-	pyaerocom/web/trends_evaluation.py
-	pyaerocom/web/var_groups.py
-	pyaerocom/web/web_naming_conventions.py
-	pyaerocom_env.yml
-	pytest.ini
-	setup.py

## Deleted modules
-	docs/api_testsuite.rst
-	docs/config_files.rst
-	docs/tutorials.rst
-	pyaerocom/io/test/test_aas_et_al.py
-	pyaerocom/test/settings.py
