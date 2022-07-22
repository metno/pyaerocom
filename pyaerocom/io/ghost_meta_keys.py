"""
Metadata keys from GHOST that only depend on station dimension

THESE SHOULD BE ALWAYS THE SAME ACCORDING TO INFORMATION INFORMATION
PROVIDED BY BSC
"""

GHOST_META_KEYS = [
    "EDGAR_v4.3.2_annual_average_BC_emissions",
    "EDGAR_v4.3.2_annual_average_CO_emissions",
    "EDGAR_v4.3.2_annual_average_NH3_emissions",
    "EDGAR_v4.3.2_annual_average_NMVOC_emissions",
    "EDGAR_v4.3.2_annual_average_NOx_emissions",
    "EDGAR_v4.3.2_annual_average_OC_emissions",
    "EDGAR_v4.3.2_annual_average_PM10_emissions",
    "EDGAR_v4.3.2_annual_average_SO2_emissions",
    "EDGAR_v4.3.2_annual_average_biogenic_PM2.5_emissions",
    "EDGAR_v4.3.2_annual_average_fossilfuel_PM2.5_emissions",
    "ESDAC_Iwahashi_landform_classification",
    "ESDAC_Meybeck_landform_classification",
    "ESDAC_modal_Iwahashi_landform_classification_25km",
    "ESDAC_modal_Iwahashi_landform_classification_5km",
    "ESDAC_modal_Meybeck_landform_classification_25km",
    "ESDAC_modal_Meybeck_landform_classification_5km",
    "ETOPO1_altitude",
    "ETOPO1_max_altitude_difference_5km",
    "GHOST_version",
    "GPW_average_population_density_25km",
    "GPW_average_population_density_5km",
    "GPW_max_population_density_25km",
    "GPW_max_population_density_5km",
    "GPW_population_density",
    "GSFC_coastline_proximity",
    "Joly-Peuch_classification_code",
    "Koppen-Geiger_classification",
    "Koppen-Geiger_modal_classification_25km",
    "Koppen-Geiger_modal_classification_5km",
    "MODIS_MCD12C1_v6_IGBP_land_use",
    "MODIS_MCD12C1_v6_LAI",
    "MODIS_MCD12C1_v6_UMD_land_use",
    "MODIS_MCD12C1_v6_modal_IGBP_land_use_25km",
    "MODIS_MCD12C1_v6_modal_IGBP_land_use_5km",
    "MODIS_MCD12C1_v6_modal_LAI_25km",
    "MODIS_MCD12C1_v6_modal_LAI_5km",
    "MODIS_MCD12C1_v6_modal_UMD_land_use_25km",
    "MODIS_MCD12C1_v6_modal_UMD_land_use_5km",
    "NOAA-DMSP-OLS_v4_average_nighttime_stable_lights_25km",
    "NOAA-DMSP-OLS_v4_average_nighttime_stable_lights_5km",
    "NOAA-DMSP-OLS_v4_max_nighttime_stable_lights_25km",
    "NOAA-DMSP-OLS_v4_max_nighttime_stable_lights_5km",
    "NOAA-DMSP-OLS_v4_nighttime_stable_lights",
    "OMI_level3_column_annual_average_NO2",
    "OMI_level3_column_cloud_screened_annual_average_NO2",
    "OMI_level3_tropospheric_column_annual_average_NO2",
    "OMI_level3_tropospheric_column_cloud_screened_annual_average_NO2",
    "UMBC_anthrome_classification",
    "UMBC_modal_anthrome_classification_25km",
    "UMBC_modal_anthrome_classification_5km",
    "WMO_region",
    "WWF_TEOW_biogeographical_realm",
    "WWF_TEOW_biome",
    "WWF_TEOW_terrestrial_ecoregion",
    "administrative_country_division_1",
    "administrative_country_division_2",
    "altitude",
    "area_classification",
    "associated_networks",
    "city",
    "climatology",
    "contact_email_address",
    "contact_institution",
    "contact_name",
    "country",
    "daily_passing_vehicles",
    "data_level",
    "daytime_traffic_speed",
    "distance_to_building",
    "distance_to_junction",
    "distance_to_kerb",
    "distance_to_source",
    "land_use",
    "latitude",
    "longitude",
    "main_emission_source",
    "measurement_altitude",
    "measurement_methodology",
    "measurement_scale",
    "measuring_instrument_calibration_scale",
    "measuring_instrument_documented_absorption_cross_section",
    "measuring_instrument_documented_accuracy",
    "measuring_instrument_documented_flow_rate",
    "measuring_instrument_documented_lower_limit_of_detection",
    "measuring_instrument_documented_measurement_resolution",
    "measuring_instrument_documented_precision",
    "measuring_instrument_documented_span_drift",
    "measuring_instrument_documented_uncertainty",
    "measuring_instrument_documented_upper_limit_of_detection",
    "measuring_instrument_documented_zero_drift",
    "measuring_instrument_documented_zonal_drift",
    "measuring_instrument_further_details",
    "measuring_instrument_inlet_information",
    "measuring_instrument_manual_name",
    "measuring_instrument_name",
    "measuring_instrument_process_details",
    "measuring_instrument_reported_absorption_cross_section",
    "measuring_instrument_reported_accuracy",
    "measuring_instrument_reported_flow_rate",
    "measuring_instrument_reported_lower_limit_of_detection",
    "measuring_instrument_reported_measurement_resolution",
    "measuring_instrument_reported_precision",
    "measuring_instrument_reported_span_drift",
    "measuring_instrument_reported_uncertainty",
    "measuring_instrument_reported_units",
    "measuring_instrument_reported_upper_limit_of_detection",
    "measuring_instrument_reported_zero_drift",
    "measuring_instrument_reported_zonal_drift",
    "measuring_instrument_sampling_type",
    "network",
    "network_maintenance_details",
    "network_miscellaneous_details",
    "network_provided_volume_standard_pressure",
    "network_provided_volume_standard_temperature",
    "network_qa_details",
    "network_sampling_details",
    "network_uncertainty_details",
    "population",
    "primary_sampling_further_details",
    "primary_sampling_instrument_documented_flow_rate",
    "primary_sampling_instrument_manual_name",
    "primary_sampling_instrument_name",
    "primary_sampling_instrument_reported_flow_rate",
    "primary_sampling_process_details",
    "primary_sampling_type",
    "principal_investigator_email_address",
    "principal_investigator_institution",
    "principal_investigator_name",
    "process_warnings",
    "representative_radius",
    "sample_preparation_further_details",
    "sample_preparation_process_details",
    "sample_preparation_techniques",
    "sample_preparation_types",
    "sampling_height",
    "station_classification",
    "station_name",
    "station_reference",
    "station_timezone",
    "street_type",
    "street_width",
    "terrain",
]