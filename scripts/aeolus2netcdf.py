#!/usr/bin/env python3
"""
read binary ESA L2B files of the ADM Aeolus mission
"""
import argparse
import glob
import logging
import os
import pathlib
import sys
import tarfile

import coda
import xarray as xr

from pyaerocom.extras.satellite_l2.aeolus_l2a import ReadL2Data

default_topo_file = "/lustre/storeB/project/fou/kl/admaeolus/EMEP.topo/MACC14_topo_v1.nc"
netcdf_indir = "/lustre/storeB/project/fou/kl/admaeolus/EMEPmodel"


def main():
    options = {}

    obj = ReadL2Data(verbose=True)
    SUPPORTED_GRIDS = list(obj.SUPPORTED_GRIDS)
    DEFAULT_GRID = "MODEL"

    parser = argparse.ArgumentParser(
        description="command line interface to aeolus2netcdf.py\n\n\n"
    )
    parser.add_argument("--file", help="file(s) to read", nargs="+")
    parser.add_argument("-v", "--verbose", help="switch on verbosity", action="store_true")
    # parser.add_argument("--listpaths", help="list the file contents.", action='store_true')
    # parser.add_argument("--readpaths", help="read listed rootpaths of DBL file. Can be comma separated",
    #                     default='mph,sca_optical_properties')
    parser.add_argument("-o", "--outfile", help="output file")
    parser.add_argument(
        "--outdir",
        help="output directory; the filename will be extended with the string '.nc'; defaults to './'",
        default="./",
    )
    parser.add_argument(
        "--logfile",
        help="logfile; defaults to /home/jang/tmp/aeolus2netcdf.log",
        default="/home/jang/tmp/aeolus2netcdf.log",
    )
    parser.add_argument("-O", "--overwrite", help="overwrite output file", action="store_true")
    parser.add_argument(
        "--emep",
        help="flag to limit the read data to the cal/val model domain",
        action="store_true",
    )
    parser.add_argument(
        "--himalayas", help="flag to limit the read data to himalayas", action="store_true"
    )
    parser.add_argument(
        "--codadef",
        help="set path of CODA_DEFINITION env variable",
        default="/lustre/storeA/project/aerocom/aerocom1/ADM_CALIPSO_TEST/",
    )
    parser.add_argument("--latmin", help="min latitude to return", default=np.float_(30.0))
    parser.add_argument("--latmax", help="max latitude to return", default=np.float_(76.0))
    parser.add_argument("--lonmin", help="min longitude to return", default=np.float_(-30.0))
    parser.add_argument("--lonmax", help="max longitude to return", default=np.float_(45.0))
    parser.add_argument(
        "--dir",
        help="work on all files below this directory",
        default="/lustre/storeB/project/fou/kl/admaeolus/data.rev.2A02/download/AE_OPER_ALD_U_N_2A_*",
    )
    # parser.add_argument("--filemask", help="file mask to find data files",
    #                     default='*AE_OPER_ALD_U_N_2A_*')
    parser.add_argument(
        "--tempdir",
        help="directory for temporary files",
        default=os.path.join(os.environ["HOME"], "tmp"),
    )
    parser.add_argument(
        "--plotmap",
        help="flag to plot a map of the data points; files will be put in outdir",
        action="store_true",
    )
    parser.add_argument(
        "--plotprofile",
        help="flag to plot the profiles; files will be put in outdir",
        action="store_true",
    )
    parser.add_argument(
        "--variables",
        help="comma separated list of variables to write; default: ec355aer,bs355aer",
        default="ec355aer",
    )
    parser.add_argument(
        "--retrieval",
        help="retrieval to read; supported: sca, ica, mca; default: sca",
        default="sca",
    )
    parser.add_argument(
        "--netcdfcolocate",
        help="flag to add L2 colocation with a netcdf file",
        action="store_true",
    )
    parser.add_argument(
        "--gridfile", help="grid data and write it to given output file (L3 in netcdf)."
    )
    parser.add_argument(
        "--gridname",
        help="name of the grid used for gridding. Supported grids are {}, defaults to {}. "
        "MODEL means gridding to model altitude field".format(
            ",".join(SUPPORTED_GRIDS), DEFAULT_GRID
        ),
        default=DEFAULT_GRID,
    )
    parser.add_argument(
        "--modeloutdir",
        help="directory for colocated model files; will have a similar filename as input file",
        default=os.path.join(os.environ["HOME"], "tmp"),
    )
    parser.add_argument(
        "--topofile",
        help=f"topography file; defaults to {default_topo_file}.",
        default=default_topo_file,
    )
    parser.add_argument(
        "--modelindir",
        help=f"model directory for reading; defaults to {netcdf_indir}.",
        default=netcdf_indir,
    )

    parser.add_argument("--aeoluslistfile", help=f"text file with input files from aeolus.")

    args = parser.parse_args()

    if args.netcdfcolocate:
        options["netcdfcolocate"] = True
    else:
        options["netcdfcolocate"] = False

    if args.aeoluslistfile:
        options["aeoluslistfile"] = args.aeoluslistfile

    if args.modelindir:
        options["modelindir"] = args.modelindir

    if args.gridfile:
        options["gridfile"] = args.gridfile

    if args.gridname:
        options["gridname"] = args.gridname
        if options["gridname"] == "MODEL":
            INTERPOL_TO_MODEL_GRID_FLAG = True
        else:
            INTERPOL_TO_MODEL_GRID_FLAG = False

    try:
        if args.retrieval:
            options["retrieval"] = args.retrieval
    except AttributeError:
        options["retrieval"] = "sca"

    if args.modeloutdir:
        options["modeloutdir"] = args.modeloutdir

    if args.logfile:
        options["logfile"] = args.logfile
        logging.basicConfig(filename=options["logfile"], level=logging.INFO)

    if args.dir:
        options["dir"] = args.dir

    if args.outdir:
        options["outdir"] = args.outdir

    if args.plotmap:
        options["plotmap"] = True
    else:
        options["plotmap"] = False

    if args.plotprofile:
        options["plotprofile"] = True
    else:
        options["plotprofile"] = False

    if args.tempdir:
        options["tempdir"] = args.tempdir

    if args.latmin:
        options["latmin"] = np.float_(args.latmin)

    if args.latmax:
        options["latmax"] = np.float_(args.latmax)

    if args.lonmin:
        options["lonmin"] = np.float_(args.lonmin)

    if args.lonmax:
        options["lonmax"] = np.float_(args.lonmax)

    if args.emep:
        options["emepflag"] = args.emep
        options["latmin"] = float(30.0)
        options["latmax"] = float(76.0)
        options["lonmin"] = float(-30.0)
        options["lonmax"] = float(45.0)
    else:
        options["emepflag"] = False

    if args.himalayas:
        options["himalayas"] = args.himalayas
        options["latmin"] = float(10.0)
        options["latmax"] = float(50.0)
        options["lonmin"] = float(60.0)
        options["lonmax"] = float(110.0)
    else:
        options["himalayas"] = False

    # if args.readpaths:
    #     options['readpaths'] = args.readpaths.split(',')

    if args.variables:
        options["variables"] = args.variables.split(",")

    if args.file:
        options["files"] = args.file

    try:
        if args.listpaths:
            options["listpaths"] = True
        else:
            options["listpaths"] = False
    except AttributeError:
        options["listpaths"] = False

    if args.verbose:
        options["verbose"] = True
    else:
        options["verbose"] = False

    if args.overwrite:
        options["overwrite"] = True
    else:
        options["overwrite"] = False

    if args.outfile:
        options["outfile"] = args.outfile

    if args.codadef:
        options["codadef"] = args.codadef

    if args.topofile:
        options["topofile"] = args.topofile

    os.environ["CODA_DEFINITION"] = options["codadef"]

    bbox = None
    global_attributes = None

    if "files" not in options:
        if "aeoluslistfile" not in options:
            options["files"] = glob.glob(
                options["dir"] + "/**/" + options["filemask"], recursive=True
            )
        else:
            options["files"] = []
            with open(options["aeoluslistfile"]) as fh:
                options["files"] = [line.rstrip("\n") for line in fh]

    for file_idx, filename in enumerate(options["files"]):
        print(filename)
        suffix = pathlib.Path(filename).suffix
        temp_file_flag = False
        if suffix == ".TGZ":
            # untar *.DBL file first
            tarhandle = tarfile.open(filename)
            files_in_tar = tarhandle.getnames()
            for file_in_tar in files_in_tar:
                if pathlib.Path(file_in_tar).suffix == ".DBL":
                    # extract file to tmp path
                    member = tarhandle.getmember(file_in_tar)
                    tarhandle.extract(member, path=options["tempdir"], set_attrs=False)
                    filename = os.path.join(options["tempdir"], file_in_tar)
                    tarhandle.close()
                    temp_file_flag = True
                    break
        elif suffix != ".DBL":
            print(f"ignoring file {filename}")
            continue

        if options["listpaths"]:
            coda_handle = coda.open(filename)
            root_field_names = coda.get_field_names(coda_handle)
            for field in root_field_names:
                print(field)
            coda.close(coda_handle)
        else:
            obj = ReadL2Data(verbose=True)
            # read sca retrieval data
            vars_to_read = options["variables"].copy()
            data_numpy_tmp = obj.read_file(
                filename,
                vars_to_retrieve=vars_to_read,
                return_as="numpy",
                read_retrieval=options["retrieval"],
            )
            # obj.ndarr2data(filedata_numpy)
            # read additional data
            if file_idx > 0:
                # append data_numpy_tmp to data_numpy
                data_numpy = np.append(data_numpy, data_numpy_tmp, axis=0)
            else:
                data_numpy = data_numpy_tmp

            ancilliary_data = obj.read_data_fields(filename, fields_to_read=["mph"])
            if temp_file_flag:
                obj.logger.info(f"removing temp file {filename}")
                os.remove(filename)

    # apply emep options for cal / val
    if options["emepflag"]:
        bbox = [options["latmin"], options["latmax"], options["lonmin"], options["lonmax"]]
        tmp_data = obj.select_bbox(data=data_numpy, bbox=bbox)
        if len(tmp_data) > 0:
            data_numpy = tmp_data
            obj.logger.info(f"file {filename} contains {len(tmp_data)} points in emep area! ")
        else:
            obj.logger.info(f"file {filename} contains no data in emep area! ")
            data_numpy = None
            # continue

    if options["himalayas"]:
        bbox = [options["latmin"], options["latmax"], options["lonmin"], options["lonmax"]]
        tmp_data = obj.select_bbox(data=data_numpy, bbox=bbox)
        if len(tmp_data) > 0:
            data_numpy = tmp_data
            obj.logger.info(f"file {filename} contains {len(tmp_data)} points in himalaya area! ")
        else:
            obj.logger.info(f"file {filename} contains no data in himalaya area! ")
            data_numpy = None
            # continue

    if "outfile" in options or "gridfile" in options or "outdir" in options:
        # if not global_attributes:
        #     global_attributes = {}
        global_attributes = ancilliary_data["mph"]
        global_attributes["Aeolus_Retrieval"] = obj.RETRIEVAL_READ
        global_attributes["input files"] = ",".join(obj.files_read)
        global_attributes["info"] = (
            "file created by pyaerocom.io.read_aeolus_l2a_data "
            + obj.__version__
            + " (https://github.com/metno/pyaerocom) at "
            + np.datetime64("now").astype("str")
        )
        global_attributes["quality"] = "quality flags for extinction applied"

    # single outfile
    if "outfile" in options:
        if len(options["files"]) == 1:
            # write netcdf
            if os.path.exists(options["outfile"]):
                if options["overwrite"]:
                    obj.to_netcdf_simple(
                        netcdf_filename=options["outfile"],
                        data_to_write=data_numpy,
                        global_attributes=global_attributes,
                        vars_to_write=[vars_to_read[0], obj._UPPERALTITUDENAME],
                    )
                else:
                    sys.stderr.write("Error: path {} exists".format(options["outfile"]))
            else:
                obj.to_netcdf_simple(
                    netcdf_filename=options["outfile"],
                    data_to_write=data_numpy,
                    global_attributes=global_attributes,
                    vars_to_write=[vars_to_read[0], obj._UPPERALTITUDENAME],
                )
        else:
            sys.stderr.write(
                "error: multiple input files, but only on output file given\n"
                "Please use the --outdir option instead\n"
            )

    # outdir
    # if 'outdir' in options and 'outfile' not in options:
    #     outfile_name = os.path.join(options['outdir'], os.path.basename(filename) + '.nc')
    #     obj.logger.info('writing file {}'.format(outfile_name))
    #     if os.path.exists(outfile_name):
    #         if options['overwrite']:
    #             obj.to_netcdf_simple(netcdf_filename=outfile_name, data_to_write=data_numpy,
    #                                  global_attributes=global_attributes, vars_to_write=vars_to_read)
    #         else:
    #             sys.stderr.write('Error: file {} exists'.format(options['outfile']))
    #     else:
    #         obj.to_netcdf_simple(netcdf_filename=outfile_name, data_to_write=data_numpy,
    #                              global_attributes=global_attributes, vars_to_write=vars_to_read)
    #

    # work with emep data and do some colocation
    if options["netcdfcolocate"]:
        start_time = time.perf_counter()

        netcdf_indir = "/lustre/storeB/project/fou/kl/admaeolus/EMEPmodel"

        # read topography since that needs to be added to the ground following height of the model
        obj.logger.info("reading topography file {}".format(options["topofile"]))
        topo_data = xr.open_dataset(options["topofile"])

        # truncate Aeolus times to hour

        aeolus_times_rounded = (
            data_numpy[:, obj._TIMEINDEX].astype("datetime64[s]").astype("datetime64[h]")
        )
        aeolus_times = data_numpy[:, obj._TIMEINDEX].astype("datetime64[s]")
        unique_aeolus_times, unique_aeolus_time_indexes = np.unique(
            aeolus_times, return_index=True
        )
        aeolus_profile_no = len(unique_aeolus_times)
        # aeolus_profile_no = int(len(aeolus_times)/obj._HEIGHTSTEPNO)
        last_netcdf_file = ""
        for time_idx in range(len(unique_aeolus_time_indexes)):
            ae_year, ae_month, ae_dummy = (
                aeolus_times[unique_aeolus_time_indexes[time_idx]].astype("str").split("-")
            )
            ae_day, ae_dummy = ae_dummy.split("T")
            file_name = f"CWF_12ST-{ae_year}{ae_month}{ae_day}_hourInst.nc"
            file_name = os.path.join(netcdf_indir, file_name)
            if not os.path.exists(file_name):
                obj.logger.info(f"file does not exist: {file_name}. skipping colocation ...")
                continue
            # read netcdf file if it has not yet been loaded
            if file_name != last_netcdf_file:
                obj.logger.info(f"reading and co-locating on model file {file_name}")
                last_netcdf_file = file_name
                nc_data = xr.open_dataset(file_name)
                nc_times = nc_data.time.data.astype("datetime64[h]")
                nc_latitudes = nc_data["lat"].data
                nc_longitudes = nc_data["lon"].data
                nc_lev_no = len(nc_data["lev"])
                nc_colocated_data = np.zeros(
                    [aeolus_profile_no * nc_lev_no, obj._COLNO], dtype=np.float_
                )

            # locate current rounded Aeolus time in netcdf file
            nc_ts_no = np.where(nc_times == unique_aeolus_times[time_idx].astype("datetime64[h]"))
            if len(nc_ts_no) != 1:
                # something is wrong here!
                pass

            # locate current profile's location index in lats and lons
            # Has to be done on original aeolus data
            for aeolus_profile_index in range(aeolus_profile_no):
                data_idx = unique_aeolus_time_indexes[aeolus_profile_index]
                try:
                    data_idx_end = unique_aeolus_time_indexes[aeolus_profile_index + 1]
                except:
                    data_idx_end = len(aeolus_times)

                data_idx_arr = np.arange(data_idx_end - data_idx) + data_idx

                aeolus_lat = np.nanmean(data_numpy[data_idx_arr, obj._LATINDEX])
                aeolus_lon = np.nanmean(data_numpy[data_idx_arr, obj._LONINDEX])
                aeolus_altitudes = data_numpy[data_idx_arr, obj._ALTITUDEINDEX]
                diff_dummy = nc_latitudes - aeolus_lat
                min_lat_index = np.argmin(np.abs(diff_dummy))
                diff_dummy = nc_longitudes - aeolus_lon
                min_lon_index = np.argmin(np.abs(diff_dummy))

                nc_data_idx = aeolus_profile_index * nc_lev_no
                nc_index_arr = np.arange(nc_lev_no) + nc_data_idx
                nc_colocated_data[nc_index_arr, obj.INDEX_DICT[obj._EC355NAME]] = nc_data[
                    "EXT_350nm"
                ].data[nc_ts_no, :, min_lat_index, min_lon_index]
                # nc_data['EXT_350nm'].data[nc_ts_no,:,min_lat_index,min_lon_index].reshape(nc_lev_no)
                nc_colocated_data[nc_index_arr, obj._ALTITUDEINDEX] = (
                    nc_data["Z_MID"].data[nc_ts_no, :, min_lat_index, min_lon_index]
                    + topo_data["topography"].data[0, min_lat_index, min_lon_index]
                )
                nc_colocated_data[nc_index_arr, obj._LATINDEX] = nc_data["lat"].data[min_lat_index]
                nc_colocated_data[nc_index_arr, obj._LONINDEX] = nc_data["lon"].data[min_lon_index]
                # nc_data['Z_MID'].data[nc_ts_no,:,min_lat_index,min_lon_index].reshape(nc_lev_no)
                nc_colocated_data[nc_index_arr, obj._TIMEINDEX] = data_numpy[
                    data_idx, obj._TIMEINDEX
                ]

        end_time = time.perf_counter()
        elapsed_sec = end_time - start_time
        temp = f"time for colocation all time steps [s]: {elapsed_sec:.3f}"
        if "nc_colocated_data" in locals():
            obj.logger.info(temp)
            obj.logger.info(
                "{} is colocated model output directory".format(options["modeloutdir"])
            )
            model_file_name = os.path.join(
                options["modeloutdir"], os.path.basename(filename) + ".colocated.nc"
            )
            # obj.to_netcdf_simple(model_file_name, data_to_write=nc_colocated_data)
            obj.to_netcdf_simple(
                netcdf_filename=model_file_name,
                data_to_write=nc_colocated_data,
                vars_to_write=vars_to_read,
            )
        pass

    # plot the profile
    if options["plotprofile"]:
        plotfilename = os.path.join(
            options["outdir"],
            os.path.basename(filename) + "." + options["retrieval"] + ".profile.png",
        )
        obj.logger.info(f"profile plot file: {plotfilename}")
        # title = '{} {}'.format(options['retrieval'], os.path.basename(filename))
        title = f"{os.path.basename(filename)}"
        obj.plot_profile_v3(
            plotfilename,
            title=title,
            data_to_plot=data_numpy,
            retrieval_name=options["retrieval"],
            plot_range=(-200, 200.0),
            plot_nbins=40,
        )
        # obj.plot_profile_v3(plotfilename, title=title, data_to_plot=data_numpy,
        #                                     retrieval_name=options['retrieval'],
        #                                     plot_range=(0.,200.))

    # plot the map
    if options["plotmap"]:
        plotmapfilename = os.path.join(options["outdir"], os.path.basename(filename) + ".map.png")
        obj.logger.info(f"map plot file: {plotmapfilename}")
        # title = os.path.basename(filename)
        obj.plot_location_map(
            plotmapfilename, data=data_numpy, bbox=bbox, title=os.path.basename(filename)
        )
        # obj.plot_location_map(plotmapfilename)

    # write L3 gridded data
    if "gridfile" in options:

        vars_to_copy = [obj._ALTITUDENAME, obj._LONGITUDENAME, obj._LATITUDENAME, ""]
        vars_to_read = options["variables"].copy()
        netcdf_indir = options["modelindir"]
        aeolus_times_rounded = (
            data_numpy[:, obj._TIMEINDEX].astype("datetime64[s]").astype("datetime64[h]")
        )
        aeolus_times = data_numpy[:, obj._TIMEINDEX].astype("datetime64[s]")
        unique_aeolus_times, unique_aeolus_time_indexes = np.unique(
            aeolus_times, return_index=True
        )
        aeolus_profile_no = len(unique_aeolus_times)
        # aeolus_profile_no = int(len(aeolus_times)/obj._HEIGHTSTEPNO)
        last_netcdf_file = ""
        for time_idx in range(len(unique_aeolus_time_indexes)):
            ae_year, ae_month, ae_dummy = (
                aeolus_times[unique_aeolus_time_indexes[time_idx]].astype("str").split("-")
            )
            ae_day, ae_dummy = ae_dummy.split("T")
            file_name = f"CWF_12ST-{ae_year}{ae_month}{ae_day}_hourInst.nc"
            file_name = os.path.join(netcdf_indir, file_name)
            if not os.path.exists(file_name):
                obj.logger.info(f"file does not exist: {file_name}. skipping colocation ...")
                continue
            # read netcdf file if it has not yet been loaded
            if file_name != last_netcdf_file:
                obj.logger.info(f"reading and preparing model data for gridding file {file_name}")
                # read model file
                if len(last_netcdf_file) == 0:
                    model_data_temp = obj.read_model_file(file_name, topofile=options["topofile"])
                    model_data = model_data_temp
                else:
                    model_data = xr.concat(
                        [model_data, model_data_temp], obj._TIME_NAME, data_vars="minimal"
                    )
                last_netcdf_file = file_name

        if INTERPOL_TO_MODEL_GRID_FLAG:
            # grid to model grid with altitude being a 4d field
            gridded_var_data = obj.to_model_grid(
                data=data_numpy, vars=vars_to_read, model_data=model_data
            )
        else:
            # grid to static grid
            gridded_var_data = obj.to_grid(
                data=data_numpy, vars=vars_to_read, gridtype=options["gridname"]
            )

        obj.to_netcdf_simple(
            netcdf_filename=options["gridfile"],
            vars_to_write=vars_to_read,
            global_attributes=global_attributes,
            data_to_write=gridded_var_data,
            gridded=True,
        )


if __name__ == "__main__":
    main()
