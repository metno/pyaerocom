#!/usr/bin/env python3
"""
small test for the sentinel5p reading
"""

import argparse
import glob
import os
import sys

import numpy as np

from pyaerocom.extras.satellite_l2.sentinel5p import ReadL2Data

default_topo_file = "/lustre/storeB/project/fou/kl/admaeolus/EMEP.topo/MACC14_topo_v1.nc"
# default_gridded_out_file = './gridded.nc'
default_local_temp_dir = "/home/jang/tmp/"

default_min_quality_flag = 0.75


def main():
    options = {}
    obj = ReadL2Data(verbose=True)
    SUPPORTED_GRIDS = list(obj.SUPPORTED_GRIDS)
    DEFAULT_GRID = "CAMS50"

    parser = argparse.ArgumentParser(
        description="command line interface to pyaerocom.io.read_sentinel5p_data\n\n\n"
    )
    parser.add_argument("--file", help="file(s) to read", nargs="+")
    parser.add_argument("-v", "--verbose", help="switch on verbosity", action="store_true")
    # parser.add_argument("--listpaths", help="list the file contents.", action='store_true')
    # parser.add_argument("--readpaths", help="read listed rootpaths of coda supported file. Can be comma separated",
    #                     default='mph,sca_optical_properties')
    parser.add_argument("-o", "--outfile", help="output file")
    parser.add_argument(
        "--outdir", help="output directory; the filename will be extended with the string '.nc'"
    )
    # parser.add_argument("--plotdir", help="directories where the plots will be put; defaults to './'",
    #                     default='./')
    # parser.add_argument("--logfile", help="logfile; defaults to /home/jang/tmp/aeolus2netcdf.log",
    #                     default="/home/jang/tmp/aeolus2netcdf.log")
    parser.add_argument("-O", "--overwrite", help="overwrite output file", action="store_true")
    parser.add_argument(
        "--emep",
        help="flag to limit the read data to the cal/val model domain",
        action="store_true",
    )
    parser.add_argument(
        "--himalayas", help="flag to limit the read data to himalayas", action="store_true"
    )
    # parser.add_argument("--codadef", help="set path of CODA_DEFINITION env variable",
    #                     default='/lustre/storeA/project/aerocom/aerocom1/ADM_CALIPSO_TEST/')
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
    # parser.add_argument("--plotmap", help="flag to plot a map of the data points; files will be put in outdir",
    #                     action='store_true')
    # parser.add_argument("--plotprofile", help="flag to plot the profiles; files will be put in outdir",
    #                     action='store_true')
    parser.add_argument(
        "--variables",
        help="comma separated list of variables to write; default: ec355aer,bs355aer",
        default="ec355aer",
    )
    # parser.add_argument("--retrieval", help="retrieval to read; supported: sca, ica, mca; default: sca",
    #                     default='sca')
    # parser.add_argument("--netcdfcolocate", help="flag to add colocation with a netcdf file",
    #                     action='store_true')
    # parser.add_argument("--modeloutdir",
    #                     help="directory for colocated model files; will have a similar filename as aeolus input file",
    #                     default=os.path.join(os.environ['HOME'], 'tmp'))
    # parser.add_argument("--topofile", help="topography file; defaults to {}.".format(default_topo_file),
    #                     default=default_topo_file)
    parser.add_argument(
        "--gridfile", help="grid data and write it to given output file (in netcdf)."
    )
    parser.add_argument(
        "--gridname",
        help="name of the grid used for gridding. Supported grids are {}, defaults to {}".format(
            ",".join(SUPPORTED_GRIDS), DEFAULT_GRID
        ),
        default=DEFAULT_GRID,
    )
    parser.add_argument(
        "--qflag",
        help=f"min quality flag to keep data. Defaults to {default_min_quality_flag}",
        default=default_min_quality_flag,
    )

    args = parser.parse_args()

    # if args.netcdfcolocate:
    #     options['netcdfcolocate'] = True
    # else:
    #     options['netcdfcolocate'] = False

    # if args.filemask:
    #     options['filemask'] = args.filemask

    if args.qflag:
        options["qflag"] = args.qflag

    if args.gridfile:
        options["gridfile"] = args.gridfile

    if args.gridname:
        options["gridname"] = args.gridname

    # if args.retrieval:
    #     options['retrieval'] = args.retrieval
    #
    # if args.modeloutdir:
    #     options['modeloutdir'] = args.modeloutdir

    if args.dir:
        options["dir"] = args.dir

    if args.outdir:
        options["outdir"] = args.outdir

    # if args.plotdir:
    #     options['plotdir'] = args.plotdir
    # else:
    #     options['plotdir'] = './'

    # if args.plotmap:
    #     options['plotmap'] = True
    # else:
    #     options['plotmap'] = False
    #
    # if args.plotprofile:
    #     options['plotprofile'] = True
    # else:
    #     options['plotprofile'] = False

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

    # if args.listpaths:
    #     options['listpaths'] = True
    # else:
    #     options['listpaths'] = False

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

    # if args.codadef:
    #     options['codadef'] = args.codadef

    # if args.topofile:
    #     options['topofile'] = args.topofile

    # os.environ['CODA_DEFINITION'] = options['codadef']

    bbox = None

    non_archive_files = []
    temp_files_dir = {}
    temp_file_flag = False

    if "files" not in options:
        options["files"] = glob.glob(options["dir"] + "/**/" + options["filemask"], recursive=True)

    vars_to_retrieve = options["variables"].copy()

    data_numpy = obj.read(
        files=options["files"],
        vars_to_retrieve=vars_to_retrieve[0],
        local_temp_dir=options["tempdir"],
        return_as="dict",
    )

    # limit data to EMEP CAMS domain
    if options["emepflag"]:
        bbox = [options["latmin"], options["latmax"], options["lonmin"], options["lonmax"]]
        tmp_data = obj.select_bbox(data_numpy, bbox=bbox)
        if len(tmp_data) > 0:
            data_numpy = tmp_data
            obj.logger.info(f"data object contains {len(tmp_data)} points in emep area! ")
        else:
            obj.logger.info("data object contains no data in emep area! ")
            data_numpy = None
            # continue

    if options["himalayas"]:
        bbox = [options["latmin"], options["latmax"], options["lonmin"], options["lonmax"]]
        tmp_data = obj.select_bbox(data_numpy, bbox=bbox)
        if len(tmp_data) > 0:
            data_numpy = tmp_data
            obj.logger.info(f"file contains {len(tmp_data)} points in himalaya area! ")
        else:
            obj.logger.info(f"file contains no data in himalaya area! ")
            data_numpy = None
            # continue

    if "outfile" in options or "gridfile" in options or "outdir" in options:
        global_attributes = {}
        global_attributes["input files"] = ",".join(obj.files_read)
        global_attributes["info"] = (
            f"file created by pyaerocom.io.read_sentinel5p_data {obj.__version__} "
            f"(https://github.com/metno/pyaerocom) at {np.datetime64('now')}"
        )
        global_attributes["quality"] = f"quality flag of {options['qflag']} applied"

    # obj.to_netcdf_simple(data_to_write=data_numpy, global_attributes=obj.global_attributes, vars_to_write=obj.DEFAULT_VARS,
    #                      netcdf_filename='/home/jang/tmp/to_netcdf_simple.nc')
    # gridded_data = obj.to_grid(data=data, vars=obj.DEFAULT_VARS, )
    # obj.to_netcdf_simple(data_to_write=gridded_data, global_attributes=global_attributes, vars_to_write=obj.DEFAULT_VARS,
    #                      gridded=True,
    #                      netcdf_filename='/home/jang/tmp/to_netcdf_simple_gridded.nc')

    # write L2 ungridded single outfile
    if "outfile" in options:
        # write netcdf
        if os.path.exists(options["outfile"]):
            if options["overwrite"]:
                obj.to_netcdf_simple(
                    netcdf_filename=options["outfile"],
                    data_to_write=data_numpy,
                    global_attributes=global_attributes,
                    vars_to_write=vars_to_retrieve,
                    apply_quality_flag=options["qflag"],
                )
            else:
                sys.stderr.write(f"Error: path {options['outfile']} exists")
        else:
            # obj.to_netcdf_simple(options['outfile'], global_attributes=ancilliary_data['mph'])
            obj.to_netcdf_simple(
                netcdf_filename=options["outfile"],
                data_to_write=data_numpy,
                global_attributes=global_attributes,
                vars_to_write=vars_to_retrieve,
                apply_quality_flag=options["qflag"],
            )

    # write L3 gridded data
    if "gridfile" in options:
        gridded_var_data = obj.to_grid(
            data=data_numpy, vars=vars_to_retrieve, gridtype=options["gridname"]
        )

        obj.to_netcdf_simple(
            netcdf_filename=options["gridfile"],
            vars_to_write=vars_to_retrieve,
            global_attributes=global_attributes,
            data_to_write=gridded_var_data,
            gridded=True,
        )


if __name__ == "__main__":
    main()
