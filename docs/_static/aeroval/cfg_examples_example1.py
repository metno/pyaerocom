"""
Example AeroVal configuration file
==================================

Author: Jonas Gliß
Date: 15.10.2021
Minimum pyaerocom version: 0.12.2

IMPORTANT NOTE
--------------
This script requires access to the PPI infrastructure of MET
Norway and cannot be run by external users.
If you work at MET, you can check whether pyaerocom has access to PPI by
running (from the command line):

pya --ppiaccess

What this is about?
-------------------

This example script will show how to create a basic AeroVal evaluation setup
and run the evaluation. The output of this example is available at:

https://aeroval.met.no/evaluation.php?project=examples&exp_name=example1

General evaluation procedure:
-----------------------------

This configuration defines a set of models to be evaluated against a certain
set of observations, within what is called an "Experiment" in AeroVal. The
observations defined specify which variables are supposed to be evaluated
from each of the models. For instance, one "Experiment" could comprise 2
observation data sources (OBS1 and OBS2), each of which measures 2 variables (
OBS1: var1, var2 and OBS2: var1 and var3).
Now if that "Experiment" comprises 2 models (MOD1 and MOD2, which all have
output for var1, var2 and var3) then, this would result in an evaluation
matrix of 4x2 entries (4 OBS / var combinations and 2 models). Each
"pixel" of that matrix corresponds to one evaluation entry (e.g. var1 from
OBS1 is co-located with var1 from MOD1, and so on). Based on the co-located
data objects (pyaerocom.ColocatedData) that are created for each of these
"pixels" of the evaluation matrix, a set of statistical parameters (such as
bias, correlation coefficients, RMS, etc) are computed within certain time
periods that can be defined flexibly by the user (e.g. 2000-2010 and 2010-2020
or a single year, e.g. 2010).

In AeroVal, each of these "pixels" of that matrix is evaluated completely
independently, doing the following steps:

- Create co-located NetCDF file for that model / obs / var entry:
    - Read model data
    - Read obs data
    - Co-locate model with obs data (in space and time) within the time
    period range specified (e.g. 2000-2020 if user specifies output periods
    2000-2010 and 2010-2020).
    - Save co-located data as NetCDF file.
- Convert co-located data to json output files read by the AeroVal frontend

The script below is grouped into the following sections:
---------------------------------------------------------

- Section 1: Global setup for AeroVal output
- Section 2: Default co-location settings
- Section 3: Configuration of observations
- Section 4: Configuration of models
- Section 5: Main script (run analysis)

"""

"""
Section 1: Global setup for AeroVal output
------------------------------------------

The global setup defines:

- Project and experiment ID
- Information about the purpose of the experiment and PI
- Information about the output paths
- Time periods to be evaluated
- Desired output frequencies
- Additional options such as:
    - Whether to compute trends
    - Whether to compute model maps
    - Whether to add seasonal statistics
    - Which regions to use for regional statistics
    - Web display options (e.g. default map zoom)

"""
import os  # needed for specification of path locations below

GLOB_CFG = dict(
    # PI of experiment
    exp_pi="Jonas Gliß",
    # ID of project (will define URL, see below)
    proj_id="examples",
    # ID of experiment (will define URL, see below)
    exp_id="example1",
    # These 2 IDs define where the output data is stored relative to the 2
    # output directories below, and they also define the URL link for this
    # project, e.g. for this example, the web URL for this experiment would be:
    #
    # https://aeroval.met.no/evaluation.php?project=examples&exp_name=example1
    #
    # Base directory for json output files
    json_basedir=os.path.abspath("../../data"),
    # Base directory for co-located data output NetCDF files
    coldata_basedir=os.path.abspath("../../coldata"),
    # E.g. for this experiment, the co-located data files can be found in:
    #
    # ../../coldata/examples/example1
    #
    # And the output json files in:
    #
    # ../../data/examples/example1
    #
    # relative to the location of this script file. Note: if
    #
    # ../../data/examples
    #
    # happens to be a Gitlab (or Github) repository (or Github),
    # then pyaerocom will write all required json files into that
    # repository, which makes it easier to share the results by pushing them
    # to the remote repository. You can then contact e.g. Augustin Mortier (
    # augustinm@met.no) at MET Norway to clone that repository on the
    # AeroVal web server, so it becomes visible at
    #
    # https://aeroval.met.no/evaluation.php?project=examples&exp_name=example1
    # Optional: location a python file containing function definitions that
    # combine some iris.Cube instances to compute new variables. This
    # enables flexible computation of new model variables that are not in
    # the model output. The file has to have a FUNS attribute which is a
    # dictionary mapping names of the functions with the callable objects.
    # Below in Section 4, this is used to compute clear-sky Angstrom
    # Exponent for NorESM2 model from 440nm and 870nm AOD, which are output
    # by the model.
    io_aux_file=os.path.abspath("../eval_py/gridded_io_aux.py"),
    # user defined scales and colormaps like https://github.com/metno/pyaerocom/blob/cb01fc8f39fe8b3f63d4ddd858aa63f5f37a6759/pyaerocom/aeroval/data/var_scale_colmap.ini
    var_scale_colmap_file=os.path.abspath("./var_scale_colmap.ini"),
    # user defined variable names like https://github.com/metno/pyaerocom/blob/10cb76ce388ffc5c43f3f8e86f6dda81b594fb7d/pyaerocom/aeroval/data/var_web_info.ini
    var_web_info_file=os.path.abspath("./var_web_info.ini"),
    # Frequencies for which statistical parameters are computed
    freqs=["daily", "monthly", "yearly"],
    # Main output frequency for AeroVal (some of the AeroVal processing
    # steps are only done for this resolution, since they would create too
    # much output otherwise, such as statistics timeseries or scatter plot in
    # "Overall Evaluation" tab on AeroVal).
    # Note that this frequency needs to be included in previous setting "freqs".
    main_freq="monthly",
    # Time periods for which statistical parameters are computed
    periods=["2010"],
    # Whether or not to add seasonal statistics
    add_seasons=True,
    # Whether or not to add trends output to the analysis. Trends analysis
    # needs at least 7 years of data, so this is skipped here for this
    # single year experiment
    add_trends=False,
    # Whether or not to re-colocate existing co-located data files from the
    # input data or not.
    reanalyse_existing=True,
    # Name of experiment
    exp_name="AeroVal example 1",
    # Description of experiment
    exp_descr=(
        "A simple setup evaluating AOD and Angstrom Exponent of 2 "
        "models (NorESM2 from AeroCom phase 3 control experiment and "
        "CAMS reanalysis dateset) for the year 2010, using AERONET "
        "version 3 sun photometer data as well as data from a merged "
        "satellite product"
    ),
    public=True,
    # Whether or not maps of the model fields are supposed to be computed
    add_model_maps=True,
)

"""
Section 2: Default co-location settings
---------------------------------------

The following specifies some settings to be used for co-location. Note
that this does note cover all possible settings, but only the ones that
deviate from the default co-location settings.
For all co-location options (and their defaults), see here:
https://pyaerocom.readthedocs.io/en/latest/api.html?highlight=ColocationSetup#pyaerocom.colocation_auto.ColocationSetup

Note that all of the available co-location settings can also be specified
for model and obs entries individually below.
"""
DEFAULT_COLOCATION_SETUP = dict(
    # Default frequency of co-located data objects.
    # NOTE: the output resolution of the co-located data files needs to be at
    # least as high as the highest output resolution for the statistical
    # results specified in parameter "freqs" above, since all statistical
    # results (stored in the output json files) are computed based on the
    # co-located NetCDF files.
    ts_type="daily",
    # Time resample setup: the following setup will perform resampling
    # from daily to monthly in 2 steps, 1. daily to weekly (requiring at
    # least 5 valid daily values per week) and 2. weekly to monthly,
    # requiring at least 3 weekly values per week. This corresponds to a
    # conservative resampling approach, requiring ca 75% coverage of
    # measurements. Note that min_num_obs may also be a simple integer,
    # specifying the minimum number of observations to resample the input
    # data to the co-location frequency, disregarding the frequency of the
    # input data (e.g. if min_num_obs is=5 and ts_type="monthly" and input
    # data is in hourly resolution, then this translated to "at least 5
    # hourly values per month", however, if input data is in daily resolution
    # then this translated to "at least 5 daily values per month").
    min_num_obs=dict(weekly=dict(daily=5), monthly=dict(weekly=3)),
    # How to aggregate the data when resampling (linked with min_num_obs and
    # can be setup in a similar way). This setting defaults to "mean",
    # however, here we use a sligthly more complicated setup that does
    # "median" and is synched with the stepwise min_num_obs regime.
    resample_how=dict(weekly=dict(daily="median"), monthly=dict(weekly="median")),
)

"""
Section 3: Configuration of observations
----------------------------------------

Each obs entry needs at least an obs ID specified, a list of variables
that are supposed to be analysed and a specification of the vertical type
of the data (e.g. Column, Surface).
You may search for observational data via the pyaerocom CLI. E.g. to search
for observations containing the strings "Aeronet" and "Sun" and "V3" you may
search from the command line via:

pya --browse *Aeronet*Sun*V3*

This will list all data IDs matching this request and will also show
variables that are provided by each of the datasets that match the search.
"""

# Define a filter for the AERONET obs dataset that excludes data from
# stations that start with DRAGON and use only sites that are located
# between 0 m and 1000 m a.s.l.
AERONET_SITE_FILTER = dict(station_name="DRAGON*", negate="station_name", altitude=[0, 1000])

# Define a python dictionary containing observation datasets to be used and
# the associated variables.
OBS_CFG = {
    # This entry is for the AERONET Sun version 3, daily dataset and will
    # provides total AOD (od550aer) and Angstrom Exponent (ang4487aer) to be
    # compared with the models.
    # AERONET is a ground based measurement network of sun photometer
    # measurements, for more info see here:
    # https://aeronet.gsfc.nasa.gov/
    #
    # This dataset will be read by pyaerocom as "UngriddedData" since the
    # measurements are performed at AERONET site locations, and the input
    # data are provided as CSV files "per site location".
    #
    # This dataset will appear as AERONET in the AeroVal interface.
    "AERONET": dict(
        # obs_id tells pyaerocom where to find the data
        obs_id="AeronetSunV3Lev2.daily",
        # Which variables to use from AERONET, here we use total AOD (
        # od550aer) and Angstrom Exponent (ang4487aer).
        obs_vars=["od550aer", "ang4487aer"],
        # What vertical type do the variables represent (columnar)
        obs_vert_type="Column",
        # Metadata filters applied to the observations AFTER reading them
        # (as UngriddedData) and BEFORE co-locating them with the models.
        obs_filters={**AERONET_SITE_FILTER},
    ),
    # 2nd obs entry is a merged satellite AOD dataset, for more info see here:
    # https://acp.copernicus.org/articles/20/2031/2020/
    #
    # This dataset will be read by pyaerocom as "GriddedData" as it is
    # provided as gridded NetCDF file (near global coverage).
    #
    "MERGED-SAT": dict(
        # ID is linked with data location
        obs_id="MODIS6.1terra",
        # Which variables to use
        obs_vars=["od550aer"],
        # Which vertical code
        obs_vert_type="Column",
        # Since these data are gridded observations with near global
        # coverage, the underlying co-location routine will be
        # gridded OBS / gridded MOD. The following parameter defines to
        # which lat / lon resolution both MOD and OBS should be regridded
        # for co-location (5 degrees is a good compromise for a global
        # dataset, between spatial resolution and required storage of the
        # output files).
        regrid_res_deg=5,
    ),
}


"""
Section 4: Configuration of models
----------------------------------

Each model entry needs at least a model ID specified. If the model data is
available in the AeroCom database (in AeroCom file format) you may search
for data via the pyaerocom CLI. E.g. to search for model IDs containing
the strings "ECMWF" and "CAMS" you may search from the command line via:

pya --browse *ECMWF*CAMS*

"""
MODEL_CFG = {
    # The key "CAMS-REAN" is how this model will be named in AeroVal
    "CAMS-REAN": dict(
        # Data ID of model data (tells pyaerocom where the data is located)
        model_id="ECMWF_CAMS_REAN"
    ),
    # The key "NorESM2" is how this model will be named in AeroVal
    "NorESM2": dict(
        # Data ID of model run (tells pyaerocom where the data is located)
        model_id="NorESM2-met2010_AP3-CTRL",
        # if model
        model_use_vars={
            # if obs var is od550aer, use od550csaer from the model
            # (od550csaer refers to clear-sky AOD)
            "od550aer": "od550csaer",
            # if obs var is ang4487aer, use ang4487csaer from the model
            "ang4487aer": "ang4487csaer",
        },
        model_read_aux={
            # Clear-sky AE is actually not available from the model so,
            # it is computed from clear-sky AOD at 440nm and 870 nm.
            # The function "calc_ae" is defined in "io_aux_file" (see
            # global setup above).
            "ang4487csaer": dict(vars_required=["od440csaer", "od870csaer"], fun="calc_ae")
        },
    ),
}


"""
Section 5: Main script (run analysis)
-------------------------------------
"""
# Combine all settings into one dictionary called CFG
CFG = {**GLOB_CFG, **DEFAULT_COLOCATION_SETUP}

# Add obs config
CFG["obs_cfg"] = OBS_CFG
# Add model config
CFG["model_cfg"] = MODEL_CFG


def main():
    """
    Create EvalSetup and pass to ExperimentProcessor and run analysis
    """
    from pyaerocom.aeroval import EvalSetup, ExperimentProcessor

    CFG["raise_exceptions"] = True
    stp = EvalSetup(**CFG)
    ana = ExperimentProcessor(stp)

    # The following command is optional:
    # it checks deletes all output files associated with this experiment,
    # that is, for this experiment, everything under:
    # ../../coldata/examples/example1
    # ../../data/examples/example1
    ana.exp_output.delete_experiment_data()

    # The following command is optional:
    # it checks all output json files associated with
    # this proj_id and exp_id for outdated data. This is useful if e.g.
    # model or observation entries are removed or renamed and the experiment
    # is rerun. It can also be run independently of the actual processing.
    # It is especially useless to call this one if
    # ana.exp_output.delete_experiment_data() is called before =)
    # Anyways, good to know that it exists.
    ana.exp_output.clean_json_files()

    # Run the experiment
    # This co-locates all "pixels" of the evaluation matrix and creates all
    # json files needed for AeroVal. It should end with printing something
    # like:
    # Processing finished.
    ana.run()


if __name__ == "__main__":
    main()
