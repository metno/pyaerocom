#!/usr/bin/env python3
################################################################
# read_aeolus_l2a_data.py
#
# read binary ESA L2A files of the ADM Aeolus mission
#
# this file is part of the pyaerocom package
#
#################################################################
# Created 20190104 by Jan Griesfeller for Met Norway
#
# Last changed: See git log
#################################################################

# Copyright (C) 2019 met.no
# Contact information:
# Norwegian Meteorological Institute
# Box 43 Blindern
# 0313 OSLO
# NORWAY
# E-mail: jan.griesfeller@met.no
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA

"""
object to read colocation netcdf files

"""
import os
import glob
import numpy as np

import logging
import time
import geopy.distance
from pyaerocom.io.read_aeolus_l2a_data import ReadL2Data

# import coda

class ReadCoLocationData(ReadL2Data):
    __version__ = "0.01"
    DATASET_NAME = 'co-location data'

    def __init__(self, index_pointer=0, dataset_to_read=None, loglevel=logging.INFO, verbose=False):
        super().__init__(dataset_to_read)
        # self.verbose = verbose
        # self.metadata = {}
        # self.data = []
        # self.index = len(self.metadata)
        # self.files = []
        # self.index_pointer = index_pointer
        # # that's the flag to indicate if the location of a data point in self.data has been
        # # stored in rads in self.data already
        # # trades RAM for speed
        # self.rads_in_array_flag = False
        #
        # if loglevel is not None:
        #     self.logger = logging.getLogger(__name__)
        #     if self.logger.hasHandlers():
        #         # Logger is already configured, remove all handlers
        #         self.logger.handlers = []
        #     # self.logger = logging.getLogger('pyaerocom')
        #     default_formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
        #     console_handler = logging.StreamHandler()
        #     console_handler.setFormatter(default_formatter)
        #     self.logger.addHandler(console_handler)
        #     self.logger.setLevel(loglevel)
        #     self.logger.debug('init')

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.metadata[float(self.index)]

    def __str__(self):
        stat_names = []
        for key in self.metadata:
            stat_names.append(self.metadata[key]['station name'])

        return ','.join(stat_names)

    ###################################################################################
    def ndarr2data(self, file_data):
        """small helper routine to put the data read by the read_file method into
        the ndarray of self.data"""

        # start_read = time.perf_counter()
        # return all data points
        num_points = len(file_data)
        if self.index_pointer == 0:
            self.data = file_data
            self.index_pointer = num_points

        else:
            # append to self.data
            # add another array chunk to self.data
            self.data = np.append(self.data, np.zeros([num_points, self._COLNO], dtype=np.float_),
                                  axis=0)

            # copy the data
            self.data[self.index_pointer:, :] = file_data
            self.index_pointer = self.index_pointer + num_points

            # end_time = time.perf_counter()
            # elapsed_sec = end_time - start_read
            # temp = 'time for single file read seconds: {:.3f}'.format(elapsed_sec)
            # self.logger.warning(temp)

    ###################################################################################
    ###################################################################################
    def ndarrappend(self, file_data, target_data):
        """small helper routine to put / append the data read by the read_file method into
        a numpy array of the right size"""

        # start_read = time.perf_counter()
        # return all data points
        num_points = len(file_data)
        if len(target_data) == 0:
            target_data = file_data

        else:
            # append to target_data
            index_pointer = len(target_data)
            target_data = np.append(target_data, np.zeros([num_points, self._COLNO], dtype=np.float_),
                                    axis=0)
            # copy file data to target_data
            target_data[index_pointer:, :] = file_data

            # end_time = time.perf_counter()
            # elapsed_sec = end_time - start_read
            # temp = 'time for single file read seconds: {:.3f}'.format(elapsed_sec)
            # self.logger.warning(temp)
        return target_data

    ###################################################################################

    def read_colocation_file(self, filename, vars_to_read=['ec355aer'], engine='xarray'):
        """method to read one file

        >>> import read_colocation_files
        >>> obj=read_colocation_files.ReadCoLocationData()
        >>> aeolus_file = '/lustre/storeB/project/fou/kl/admaeolus/data.rev.TD01/netcdf_emep_domain/AE_TD01_ALD_U_N_2A_20181130T032226039_005423993_001574_0001.DBL.nc'
        >>> model_file = '/lustre/storeB/project/fou/kl/admaeolus/EMEPmodel.colocated/AE_TD01_ALD_U_N_2A_20181130T032226039_005423993_001574_0001.DBL.colocated.nc'
        >>> aeolus_data = obj.read_colocation_file(aeolus_file)
        >>> model_data = obj.read_colocation_file(model_file)

        >>> import xarray as xr
        >>> aeolus_data = xr.open_dataset(aeolus_file)
        >>> model_data = xr.open_dataset(model_file)

        """

        vars_to_read_arr = [self._TIME_NAME, self._LATITUDENAME, self._LONGITUDENAME, self._ALTITUDENAME,
                            self._UPPERALTITUDENAME]
        vars_to_read_arr.extend(vars_to_read)

        if engine == 'xarray':
            # read data using xarray
            import xarray as xr
            file_data = xr.open_dataset(filename)
            file_data.close()
            num_points = len(file_data[self._TIME_NAME])
            ret_data = np.empty([num_points, self._COLNO], dtype=np.float_)
            ret_data[:] = np.nan
            for var in vars_to_read_arr:
                if var == self._TIME_NAME:
                    # convert time to datetime64
                    # xarray represents the time as datetime64[ns], but we use datetime64[s]
                    # internally
                    ret_data[:, self.INDEX_DICT[var]] = file_data[var].data.astype('datetime64[s]')
                else:
                    ret_data[:, self.INDEX_DICT[var]] = file_data[var].data

            return ret_data

        elif engine == 'netcdf4':
            # read data using netcdf 4 python
            pass
        else:
            # print error message and return
            return []
            pass

    ###################################################################################

    def plot_profile(self, data_dict, plotfilename, vars_to_plot=['ec355aer'], title=None,
                     retrieval_name=None,
                     plot_range=(0., 2000.),
                     plot_nbins=20.,
                     linear_time=False):
        """plot sample profile plot

        """
        import matplotlib.pyplot as plt
        from scipy import interpolate
        from matplotlib.colors import BoundaryNorm
        from matplotlib.ticker import MaxNLocator

        height_step_no = self._HEIGHTSTEPNO
        target_height_no = 2001
        target_heights = np.arange(0, target_height_no) * 10
        # target_heights = np.flip(target_heights)
        plot_row_no = len(data_dict)
        # enable TeX
        # plt.rc('text', usetex=True)
        # plt.rc('font', family='serif')
        fig, _axs = plt.subplots(nrows=plot_row_no, ncols=1, constrained_layout=True)
        # fig.subplots_adjust(hspace=0.3)
        try:
            axs = _axs.flatten()
        except Exception:
            axs = [_axs]

        plot_handle = []
        levels = []
        cmap = []
        norm = []
        yticks = []
        times = {}
        times_no = {}
        unique_times = {}
        unique_indexes = {}
        unique_height_step_no = {}
        time_step_no = {}

        vars_to_plot_arr = [self._ALTITUDENAME]
        vars_to_plot_arr.extend(vars_to_plot)
        for plot_index, data_name in enumerate(data_dict):
            # read returning a ndarray
            data = data_dict[data_name]

            times[data_name] = data[:, self._TIMEINDEX]
            times_no[data_name] = len(times)
            plot_data = {}
            plot_data_masks = {}
            unique_times[data_name], unique_indexes[data_name], unique_height_step_no[data_name] = \
                np.unique(times[data_name], return_index=True, return_counts=True)
            time_step_no[data_name] = len(unique_times[data_name])

            target_x = np.arange(0, time_step_no[data_name])

            for data_var in vars_to_plot_arr:
                # plot_data[data_var] = \
                #     self.data[:, self.INDEX_DICT[data_var]]
                plot_data_masks[data_var] = np.isnan(data[:, self.INDEX_DICT[data_var]])

            # in case of a cut out area, there might not be all the height steps
            # in self.data (since the Aeolus line of sight is tilted 35 degrees)
            # or due to the fact the the slection removes points where longitude or
            # latitude are NaN
            # unfortunately the number of height steps per time code is not necessarily equal
            # to self._HEIGHTSTEPNO anymore
            # e.g. due to an area based selection or due to NaNs in the profile
            # we therefore have to go through the times and look for changes

            # idx_time = times[0]
            # time_cut_start_index = 0
            # time_cut_end_index = 0
            time_index_dict = {}
            for idx, time in enumerate(unique_times[data_name]):
                time_index_dict[time] = np.arange(unique_indexes[data_name][idx],
                                                  unique_indexes[data_name][idx] + unique_height_step_no[data_name][
                                                      idx])
            #     if time == idx_time:
            #         time_cut_end_index = idx
            #     else:
            #         time_cut_end_index = idx
            #         time_index_dict[idx_time] = np.arange(time_cut_start_index, time_cut_end_index )
            #         time_cut_start_index = idx
            #         idx_time = time
            # time_index_dict[idx_time] = np.arange(time_cut_start_index, time_cut_end_index + 1)
            # time_index_dict[idx_time] = np.arange(unique_indexes[data_name]time_cut_start_index, time_cut_end_index + 1)

            for var in vars_to_plot:
                # this loop has not been optimised for several variables
                out_arr = np.zeros([time_step_no[data_name], target_height_no])
                out_arr[:] = np.nan
                for time_step_idx, unique_time in enumerate(unique_times[data_name]):
                    var_data = data[time_index_dict[unique_time], self.INDEX_DICT[var]]
                    var_data = data_dict[data_name][time_index_dict[unique_time], self.INDEX_DICT[var]]
                    # scipy.interpolate cannot cope with nans in the data
                    # work only on profiles with a nansum > 0

                    nansum = np.nansum(var_data)
                    if nansum > 0:
                        height_data = data_dict[data_name][time_index_dict[unique_time], self.INDEX_DICT['altitude']]
                        if np.isnan(np.sum(var_data)):
                            height_data = height_data[~plot_data_masks[var][time_index_dict[unique_time]]]
                            var_data = var_data[~plot_data_masks[var][time_index_dict[unique_time]]]

                        try:
                            f = interpolate.interp1d(height_data, var_data, kind='nearest', bounds_error=False,
                                                     fill_value=np.nan)
                            interpolated = f(target_heights)
                            out_arr[time_step_idx, :] = interpolated
                        except ValueError:

                            # this happens when height_data and var_data have only one entry
                            # set out_arr[time_step_idx,:] to NaN in this case for now
                            # breakpoint()
                            out_arr[time_step_idx, :] = np.nan

                    elif nansum == 0:
                        # set all heights of the plotted profile to 0 since nothing was detected
                        out_arr[time_step_idx, :] = 0.

                # levels = MaxNLocator(nbins=15).tick_values(np.nanmin(out_arr), np.nanmax(out_arr))
                # levels = MaxNLocator(nbins=20).tick_values(0., 2000.)
                levels = MaxNLocator(nbins=plot_nbins).tick_values(plot_range[0], plot_range[1])
                # cmap = plt.get_cmap('PiYG')
                cmap = plt.get_cmap('autumn_r')
                norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

                plot_handle.append(axs[plot_index].pcolormesh(out_arr.transpose(), cmap=cmap, norm=norm))
                yticks.append(plot_handle[plot_index].axes.get_yticks())
                yticklabels = plot_handle[plot_index].axes.set_yticklabels(yticks[-1] / 100.)
                plot_handle[plot_index].axes.set_xlabel('time step number')
                plot_handle[plot_index].axes.set_ylabel('height [km]')
                if title:
                    plot_handle[plot_index].axes.set_title(title, fontsize='small')
                else:
                    plot_handle[plot_index].axes.set_title(data_name)
                # plot_simple2.axes.set_aspect(0.05)
                # plt.show()
                plt.annotate('start={}'.format(unique_times[data_name][0].astype('datetime64[s]')),
                             (-0.12, -0.24),
                             xycoords=plot_handle[plot_index].axes.transAxes,
                             fontsize=8,
                             horizontalalignment='left')
                plt.annotate('end={}'.format(unique_times[data_name][-1].astype('datetime64[s]')),
                             (1.02, -0.24),
                             xycoords=plot_handle[plot_index].axes.transAxes,
                             fontsize=8,
                             horizontalalignment='right')

        clb = plt.colorbar(plot_handle[0], ax=axs, orientation='vertical', fraction=0.05,
                           aspect=30)
        if retrieval_name:
            clb.set_label('{} [{}] {} retrieval'.format(var, self.TEX_UNITS[var], retrieval_name),
                          )
        else:
            clb.ax.set_title('{} [{}]'.format(var, self.TEX_UNITS[var]), fontsize='small', orientation='vertical')
        plt.savefig(plotfilename, dpi=300)
        plt.close()
        # print('test')

    ###################################################################################
    def plot_profile_independent(self, data_dict, plotfilename, vars_to_plot=['ec355aer'], title=None,
                                 retrieval_name=None,
                                 plot_range=(0., 2000.),
                                 plot_nbins=20.,
                                 linear_time=False,
                                 optimised_time=True,
                                 plot_orbit_info=True,
                                 plot_stat_info=True,
                                 zero_to_nans=False,
                                 colorbar='coolwarm'):

        """plot sample profile plot with
        all time steps found in data dict regardless in which dict

        """
        import matplotlib.pyplot as plt
        SMALL_SIZE = 9
        MEDIUM_SIZE = 10
        BIGGER_SIZE = 12

        # plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
        # plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
        # plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
        # plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
        from scipy import interpolate
        from matplotlib.colors import BoundaryNorm
        from matplotlib.ticker import MaxNLocator

        filling_zero_val = -1.E6
        intermediate_height_no = 50
        # height step size in meters for plotting
        height_step_size = 10.

        target_height_no = 2001
        target_heights = np.arange(0, target_height_no) * height_step_size
        # target_heights = np.flip(target_heights)
        plot_row_no = len(data_dict)
        fig, _axs = plt.subplots(nrows=plot_row_no, ncols=1, constrained_layout=True)
        # fig.subplots_adjust(hspace=0.3)
        try:
            axs = _axs.flatten()
        except Exception:
            axs = [_axs]

        plot_handle = []
        levels = []
        cmap = []
        norm = []
        stat_info = {}
        yticks = []
        times = {}
        times_no = {}
        unique_times = {}
        unique_indexes = {}
        unique_height_step_no = {}
        time_step_no = {}

        # plot all time steps found in data_dict and put the non existent ones to nan
        orbit_dummy_dict = {}   #for testing
        for plot_index, data_name in enumerate(data_dict):
            try:
                times_existing = np.append(times_existing, data_dict[data_name][:, self._TIMEINDEX], axis=0)
            except NameError:
                times_existing = data_dict[data_name][:, self._TIMEINDEX]

        # if 'aeolus' in data_name:
            # determine the borders of the different orbits
            # the orbit number is stored in data_dict[data_name][:,self._DISTINDEX]
            orbit_data = data_dict[data_name][:, self._DISTINDEX]
            orbits = np.unique(orbit_data)
            orbit_dict = {}
            for orbit in orbits:
                dummy = np.where(orbit_data == orbit)
                orbit_time = data_dict[data_name][dummy[0][0], self._TIMEINDEX]
                orbit_dict[orbit_time] = {}
                orbit_dict[orbit_time]['orbit'] = int(orbit_data[dummy[0][0]])
                orbit_dict[orbit_time]['index'] = int(dummy[0][0])
                # orbit_dict[int(dummy[0][0])] = int(orbit_data[dummy[0][0]])
                orbit_dummy_dict[data_name] = orbit_dict
            # pass
        print(orbit_dummy_dict)

        time_step_size = 12.
        plot_xlabel_flag = True
        if linear_time:
            # print also the time gaps
            plot_times = np.arange(np.min(times_existing), np.max(times_existing), np.float_(time_step_size))
        elif optimised_time:
            # print data with optimised time gaps
            # that is a number of time steps after each orbit with no data
            plot_xlabel_flag = False
            time_steps_to_add = 25
            plot_times = np.array([], dtype=np.int_)
            for idx, orbit in enumerate(orbits):
                dummy = np.where(orbit_data == orbit)
                orbit_times = np.unique(data_dict[data_name][dummy[0], self._TIMEINDEX])
                plot_times = np.append(plot_times, orbit_times, axis=0)
                if idx == len(orbits)-1:
                    continue
                dummy_times = np.arange(orbit_times[-1]+time_step_size,
                                        orbit_times[-1]+(time_step_size * time_steps_to_add),
                                        np.float_(time_step_size))
                plot_times = np.append(plot_times, dummy_times, axis=0)
            pass
        else:
            plot_times = np.unique(times_existing)

        plot_time_steps = len(plot_times)

        target_x = np.arange(0, plot_time_steps)

        vars_to_plot_arr = [self._ALTITUDENAME]
        vars_to_plot_arr.extend(vars_to_plot)
        for plot_index, data_name in enumerate(data_dict):
            plot_out_arr = np.empty([plot_time_steps, target_height_no])
            plot_out_arr[:] = np.nan
            # set up an list whose list index contains the index of the corresponding data time
            time_index_array = np.empty(plot_time_steps)
            time_index_array[:] = -1
            data = data_dict[data_name]
            times[data_name] = data_dict[data_name][:, self._TIMEINDEX]
            times_no[data_name] = len(times)
            unique_times[data_name], unique_indexes[data_name], unique_height_step_no[data_name] = \
                np.unique(times[data_name], return_index=True, return_counts=True)
            time_step_no[data_name] = len(unique_times[data_name])

            # create an index array to connect plot_times and times[data_name]
            # if the # of time steps do not match
            matched_indexes = 0
            if plot_time_steps != times_no[data_name]:
                # plot times do not match over both data sets
                for time_idx, _time in enumerate(plot_times):
                    dummy = np.where(unique_times[data_name] == _time)
                    if len(dummy[0]) == 1:
                        # print(type(dummy[0]))
                        time_index_array[time_idx] = dummy[0]

                    if _time in orbit_dict:
                        orbit_dict[_time]['plotindex'] = time_idx
                        orbit_dummy_dict[data_name][_time]['plotindex'] = time_idx
            else:
                time_index_array = np.arange(plot_time_steps)

            # read returning a ndarray

            plot_data = {}
            plot_data_masks = {}

            for data_var in vars_to_plot_arr:
                # plot_data[data_var] = \
                #     self.data[:, self.INDEX_DICT[data_var]]
                plot_data_masks[data_var] = np.isnan(data[:, self.INDEX_DICT[data_var]])

            # in case of a cut out area, there might not be all the height steps
            # in self.data (since the Aeolus line of sight is tilted 35 degrees)
            # or due to the fact the the selection removes points where longitude or
            # latitude are NaN
            # unfortunately the number of height steps per time code is not necessarily equal
            # to self._HEIGHTSTEPNO anymore
            # e.g. due to an area based selection or due to NaNs in the profile
            # we therefore have to go through the times and look for changes

            time_index_dict = {}
            for idx, time in enumerate(unique_times[data_name]):
                time_index_dict[time] = np.arange(unique_indexes[data_name][idx],
                                                  unique_indexes[data_name][idx] + unique_height_step_no[data_name][
                                                      idx])

            for var in vars_to_plot:
                # this loop has not been optimised for several variables
                for time_step_idx, unique_time in enumerate(plot_times):
                    # check if the time is in time_index_dict[unique_time]
                    if unique_time not in time_index_dict:
                        print('time not found in {} data: {}'.format(data_name, unique_time.astype('datetime64[s]')))
                        continue

                    matched_indexes += 1
                    # var_data = data[time_index_dict[unique_time],self.INDEX_DICT[var]]
                    var_data = data_dict[data_name][time_index_dict[unique_time], self.INDEX_DICT[var]]
                    # scipy.interpolate cannot cope with nans in the data
                    # work only on profiles with a nansum > 0
                    # in addition, it needs at least two value pairs

                    nansum = np.nansum(var_data)
                    if nansum > 0 and len(var_data) > 1:
                        height_data = data_dict[data_name][time_index_dict[unique_time], self.INDEX_DICT[self._ALTITUDENAME]]
                        if np.isnan(np.sum(var_data)):
                            # lower_height_data = lower_height_data[~plot_data_masks[var][time_index_dict[unique_time]]]
                            height_data = height_data[~plot_data_masks[var][time_index_dict[unique_time]]]
                            var_data = var_data[~plot_data_masks[var][time_index_dict[unique_time]]]

                        if len(height_data) < 10.:
                            try:
                                lower_height_data = data_dict[data_name][time_index_dict[unique_time],self.INDEX_DICT[self._UPPERALTITUDENAME]]
                            except TypeError:
                                pass

                            if np.isnan(np.sum(var_data)):
                                lower_height_data = lower_height_data[
                                    ~plot_data_masks[var][time_index_dict[unique_time]]]

                            # make sure that gaps in the input profile are also present in the profile created by
                            # a nearest neighbour interpolation (used for better looking plots)
                            plot_heights_temp = np.zeros(intermediate_height_no)
                            plot_val_temp = np.zeros(intermediate_height_no)
                            temp_height_index = 0
                            zero_filled_flag = False
                            # note that the order of heights is from top to bottom
                            for height_level in range(len(height_data)):
                                # if the former height level has been surrounded by filling_zero_val
                                # we also have to surround the actual height with filling_zero_val
                                # to make the nearest neighbour interpolation right
                                if zero_filled_flag:
                                    zero_filled_flag = False
                                    plot_heights_temp[temp_height_index] = height_data[height_level] + height_step_size
                                    plot_val_temp[temp_height_index] = filling_zero_val
                                    temp_height_index += 1

                                plot_heights_temp[temp_height_index] = height_data[height_level]
                                plot_val_temp[temp_height_index] = var_data[height_level]
                                temp_height_index += 1
                                #if the height is not the same as the lower height in the profile
                                #we want to extend the profile before interpolation
                                if lower_height_data[height_level] in height_data:
                                    plot_heights_temp[temp_height_index] = lower_height_data[height_level] + height_step_size/10.
                                    plot_val_temp[temp_height_index] = var_data[height_level]
                                    temp_height_index += 1
                                else:
                                    plot_heights_temp[temp_height_index] = lower_height_data[height_level]
                                    plot_val_temp[temp_height_index] = var_data[height_level]
                                    temp_height_index += 1
                                    if height_level < len(height_data)-1:
                                        plot_heights_temp[temp_height_index] = lower_height_data[height_level] - height_step_size/10.
                                        plot_val_temp[temp_height_index] = filling_zero_val
                                        temp_height_index += 1
                                        zero_filled_flag = True

                            plot_heights_temp = plot_heights_temp[0:temp_height_index]
                            plot_val_temp = plot_val_temp[0:temp_height_index]
                            height_data = plot_heights_temp[0:temp_height_index]
                            var_data = plot_val_temp[0:temp_height_index]
                            pass

                        try:
                            # f = interpolate.interp1d(height_data, var_data, kind='nearest', bounds_error=False,
                            #                          fill_value=0.)
                            f = interpolate.interp1d(height_data, var_data, kind='nearest', bounds_error=False,
                                                     fill_value=np.nan)
                            interpolated = f(target_heights)
                            plot_out_arr[time_step_idx, :] = interpolated
                        except ValueError:

                            # this happens when height_data and var_data have only one entry
                            # set out_arr[time_step_idx,:] to NaN in this case for now
                            # breakpoint()
                            plot_out_arr[time_step_idx, :] = np.nan

                    elif nansum == 0:
                        # set all heights of the plotted profile to 0 since nothing was detected
                        plot_out_arr[time_step_idx, :] = 0.

                    # plot_data[data_name] = plot_out_arr.copy()

                # now remove the very negative values used to make the interpolation work
                plot_out_arr[np.where(plot_out_arr == filling_zero_val)] = np.nan

                self.logger.info('{} time steps matched'.format(matched_indexes))
                # levels = MaxNLocator(nbins=15).tick_values(np.nanmin(out_arr), np.nanmax(out_arr))
                # levels = MaxNLocator(nbins=20).tick_values(0., 2000.)
                levels = MaxNLocator(nbins=plot_nbins).tick_values(plot_range[0], plot_range[1])
                # cmap = plt.get_cmap('PiYG')
                cmap = plt.get_cmap(colorbar)
                norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

                if zero_to_nans:
                    # set all zeros to NaNs
                    pass
                    self.logger.info('setting zeros to NaNs for plotting...')
                    # plot_out_arr = np.where(plot_out_arr == 0., plot_out_arr, np.nan)
                    plot_out_arr = np.where(plot_out_arr == 0., np.nan, plot_out_arr)

                plot_handle.append(axs[plot_index].pcolormesh(plot_out_arr.transpose(), cmap=cmap, norm=norm))
                # plot the orbit info
                if plot_orbit_info:
                    plt_y = [1700., 2000.]
                    for idx, orbit_time in enumerate(orbit_dict):
                        plt_x = [orbit_dict[orbit_time]['plotindex'], orbit_dict[orbit_time]['plotindex']]
                        axs[plot_index].plot(plt_x, plt_y, color='black')
                        if idx % 2 == 0:
                            anno_y_val = 1825.
                        else:
                            anno_y_val = 1700.

                        axs[plot_index].annotate(orbit_dict[orbit_time]['orbit'],
                                                 (orbit_dict[orbit_time]['plotindex']+1, anno_y_val),
                                                 color='black', fontsize='xx-small')

                if plot_stat_info:
                    stat_info[data_name] = {}
                    stat_info[data_name]['plot_median'] = np.nanmedian(plot_out_arr)
                    stat_info[data_name]['plot_mean'] = np.nanmean(plot_out_arr)
                    stat_info[data_name]['median'] = np.nanmedian(data_dict[data_name][:, self.INDEX_DICT[data_var]])
                    stat_info[data_name]['mean'] = np.nanmean(data_dict[data_name][:, self.INDEX_DICT[data_var]])
                    stat_info[data_name]['min'] = np.nanmin(data_dict[data_name][:, self.INDEX_DICT[data_var]])
                    stat_info[data_name]['max'] = np.nanmax(data_dict[data_name][:, self.INDEX_DICT[data_var]])

                # plt_x = [30.,30.]
                yticks.append(plot_handle[plot_index].axes.get_yticks())
                yticklabels = plot_handle[plot_index].axes.set_yticklabels(yticks[-1] / 100.)
                if plot_xlabel_flag:
                    plot_handle[plot_index].axes.set_xlabel('time step number',fontsize='xx-small')
                else:
                    plot_handle[plot_index].axes.set_xlabel(' ')

                plot_handle[plot_index].axes.set_ylabel('height [km]',fontsize='xx-small')
                if title:
                    plot_handle[plot_index].axes.set_title(title, fontsize='x-small')
                else:
                    plot_handle[plot_index].axes.set_title(data_name, fontsize='x-small')
                # plot_simple2.axes.set_aspect(0.05)
                # plt.show()
                plt.annotate('start={}'.format(plot_times[0].astype('datetime64[s]')),
                             (-0.12, -0.22),
                             xycoords=plot_handle[plot_index].axes.transAxes,
                             fontsize=8,
                             horizontalalignment='left')
                plt.annotate('end={}'.format(plot_times[-1].astype('datetime64[s]')),
                             (1.02, -0.22),
                             xycoords=plot_handle[plot_index].axes.transAxes,
                             fontsize=8,
                             horizontalalignment='right')
                # add lines to indicte where the different orbits are
                orbit_data = data_dict[data_name][:, self._DISTINDEX]
                # plt.annotate('{}'.format(orbit_data[0]),
                #              (0., 15000.),
                #              # xycoords=plot_handle[plot_index].axes.transAxes,
                #              fontsize=8,
                #              horizontalalignment='left')

        if plot_stat_info:
            # plot few statistics info
            for data_name in data_dict:
                if 'aeolus' in data_name:
                    plt.annotate('aeolus median={0:.4f}'.format(stat_info[data_name]['median']),
                         (-0.12, -0.29),
                         # xycoords='figure fraction',
                         xycoords=plot_handle[0].axes.transAxes,
                         fontsize=8,
                         horizontalalignment='left')
                    plt.annotate('aeolus mean={0:.2f}'.format(stat_info[data_name]['mean']),
                         (-0.12, -0.36),
                         # xycoords='figure fraction',
                         xycoords=plot_handle[0].axes.transAxes,
                         fontsize=8,
                         horizontalalignment='left')
                    plt.annotate('aeolus max={0:.2f}'.format(stat_info[data_name]['max']),
                         (-0.12, -0.43),
                         # xycoords='figure fraction',
                         xycoords=plot_handle[0].axes.transAxes,
                         fontsize=8,
                         horizontalalignment='left')
                else:
                    plt.annotate('model median={0:.4f}'.format(stat_info[data_name]['median']),
                         (1.02, -0.29),
                         xycoords=plot_handle[0].axes.transAxes,
                         fontsize=8,
                         horizontalalignment='right')
                    plt.annotate('model mean={0:.2f}'.format(stat_info[data_name]['mean']),
                         (1.02, -0.36),
                         xycoords=plot_handle[0].axes.transAxes,
                         fontsize=8,
                         horizontalalignment='right')
                    plt.annotate('model max={0:.2f}'.format(stat_info[data_name]['max']),
                         (1.02, -0.43),
                         xycoords=plot_handle[0].axes.transAxes,
                         fontsize=8,
                         horizontalalignment='right')

        clb = plt.colorbar(plot_handle[0], ax=axs, orientation='vertical', fraction=0.05,
                           aspect=30,)
        if retrieval_name:
            clb.set_label('{} [{}] {} retrieval'.format(var, self.TEX_UNITS[var], retrieval_name, fontsize='xx-small'),
                          )
        else:
            clb.ax.set_title('{} [{}]'.format(var, self.TEX_UNITS[var]), fontsize='xx-small', orientation='vertical')
        plt.savefig(plotfilename, dpi=300)
        plt.close()

    ###################################################################################
    def plot_location_map(self, plotfilename, data_dict, title=None):
        """small routine to plot the satellite track on a map

        >>> import matplotlib.pyplot as plt
        >>> from mpl_toolkits.basemap import Basemap
        >>> lats=obj.data[:,obj._LATINDEX]
        >>> lons=obj.data[:,obj._LONINDEX]
        >>> m = Basemap(projection='merc',lon_0=0)
        >>> x, y = m(lons,lats)
        >>> m.drawmapboundary(fill_color='#99ffff')
        >>> m.fillcontinents(color='#cc9966',lake_color='#99ffff')
        >>> m.scatter(x,y,3,marker='o',color='k')
        >>> plt.show()
        """

        import matplotlib.pyplot as plt
        from mpl_toolkits.basemap import Basemap
        import matplotlib as mpl
        import matplotlib.cm as cm

        lat_low = -90.
        lat_high = 90.
        lon_low = -180.
        lon_high = 180.

        lat_low = 25.
        lat_high = 80.
        lon_low = -35.
        lon_high = 55.

        m = Basemap(projection='cyl', llcrnrlat=lat_low, urcrnrlat=lat_high,
                    llcrnrlon=lon_low, urcrnrlon=lon_high, resolution='c', fix_aspect=False)

        for data_name in data_dict:
            # plot only the aeolus data
            if 'aeolus' not in data_name:
                continue
            # height_data = data_dict[data_name][:,self.INDEX_DICT['altitude']]
            height_data = data_dict[data_name][:, self.INDEX_DICT['ec355aer']]
            height_data_mask = np.isnan(height_data)
            # [~plot_data_masks

            lats = np.round(data_dict[data_name][~height_data_mask, self._LATINDEX] * 100.) / 100.
            lons = np.round(data_dict[data_name][~height_data_mask, self._LONINDEX] * 100.) / 100.
            orbit_data = data_dict[data_name][~height_data_mask, self._DISTINDEX]
            x, y = m(lons, lats)
            m.drawmeridians(np.arange(-180, 220, 40), labels=[0, 0, 0, 1], fontsize=10)
            m.drawparallels(np.arange(-90, 120, 30), labels=[1, 1, 0, 0], fontsize=10)
            # axis = plt.axis([LatsToPlot.min(), LatsToPlot.max(), LonsToPlot.min(), LonsToPlot.max()])
            # ax = plots[0].axes
            m.drawcoastlines()

            # plot each aeolus orbit with a different color
            orbits = np.unique(orbit_data)
            # colors = cm.rainbow(np.linspace(0, 1, len(orbits)))
            orbit_number = orbits.max() - orbits.min()
            # cmap = plt.get_cmap('viridis',orbit_number)
            # cmap = plt.get_cmap('cool', orbit_number)
            cmap = plt.get_cmap('jet', orbit_number+1)
            norm = mpl.colors.Normalize(vmin=orbits.min(), vmax=orbits.max()+1)
            sm = cm.ScalarMappable(norm=norm, cmap=cmap)
            sm.set_array([])

            # for orbit in orbits:
            plots = []
            for orbit in orbits:
                dummy = np.where(orbit_data == orbit)
                # plot = m.scatter(x[dummy], y[dummy], 4, marker='o', color=c)
                plot = m.scatter(x[dummy], y[dummy], 4, marker='o', color=cmap(norm(orbit)))
                plots.append(plot)

            if title:
                plt.title(title)

            clb = m.colorbar(sm, ax=plots[0].axes, pad=0.30, label='orbit #')
            # clb.set_label('orbit #')
            plt.savefig(plotfilename, dpi=300)
            plt.close()

    ###################################################################################

if __name__ == '__main__':
    import logging

    default_plot_file = './out.png'
    default_retrieval = 'sca'
    default_topo_file = '/lustre/storeB/project/fou/kl/admaeolus/EMEP.topo/MACC14_topo_v1.nc'
    default_model_dir_start = '/lustre/storeB/project/fou/kl/admaeolus/EMEPmodel.colocated.'
    default_aeolus_dir_start = '/lustre/storeB/project/fou/kl/admaeolus/data.rev.TD01/netcdf_emep_domain_'
    default_model_dir = default_model_dir_start + default_retrieval
    default_aeolus_dir = default_aeolus_dir_start + default_retrieval

    import argparse
    import numpy as np

    options = {}
    parser = argparse.ArgumentParser(
        description='command line interface to aeolus2netcdf.py\n\n\n')
    parser.add_argument("--retrieval", help="retrieval name; can be sca, mca or ica; defaults to sca",
                        default=default_retrieval)
    parser.add_argument("--aeolusfile", help="aeolus file to read")
    parser.add_argument("--modelfile", help="model file to read")
    parser.add_argument("-v", "--verbose", help="switch on verbosity",
                        action='store_true')
    parser.add_argument("--starttime",
                        help="startdate as time string understood by numpy's datetime64; defaults to None; example: 2018-12-11T00:00:00",
                        default=None)
    parser.add_argument("--endtime",
                        help="enddate as time string; defaults to None.",
                        default=None)
    # parser.add_argument("--outdir", help="output directory; the filename will be extended with the string '.nc'")
    parser.add_argument("--logfile", help="logfile; defaults to /home/jang/tmp/aeolus2netcdf.log",
                        default="/home/jang/tmp/plot_colocation_files.log")

    # parser.add_argument("-O", "--overwrite", help="overwrite output file", action='store_true')
    # parser.add_argument("--emep", help="flag to limit the read data to the cal/val model domain", action='store_true')
    parser.add_argument("--zerotonans", help="flag to plot zeros as NaNs", action='store_true')
    # parser.add_argument("--latmin", help="min latitude to return", default=np.float_(30.))
    # parser.add_argument("--latmax", help="max latitude to return", default=np.float_(76.))
    # parser.add_argument("--lonmin", help="min longitude to return", default=np.float_(-30.))
    # parser.add_argument("--lonmax", help="max longitude to return", default=np.float_(45.))
    parser.add_argument("--aeolusdir",
                        help="base directory of the aeolus files; defaults to {}/".format(default_aeolus_dir),
                        default=default_aeolus_dir)
    parser.add_argument("--modeldir",
                        help="base directory of the model files; defaults to {}/".format(default_model_dir),
                        default=default_model_dir)
    # parser.add_argument("--tempdir", help="directory for temporary files",
    #                     default=os.path.join(os.environ['HOME'], 'tmp'))
    parser.add_argument("--plotmapfile", help="filename of the map plot of the data points;")
    # parser.add_argument("--plotprofile", help="flag to plot the profiles; files will be put in outdir",
    #                     action='store_true')
    parser.add_argument("--plotfile", help="plot file name (abs. path); defaults to {}.".format(default_plot_file), )
    # default=default_plot_file)
    parser.add_argument("--variables", help="comma separated list of variables to write; default: ec355aer,bs355aer",
                        default='ec355aer,bs355aer')

    args = parser.parse_args()

    if args.zerotonans:
        options['zerotonans'] = True
    else:
        options['zerotonans'] = False

    if args.plotmapfile:
        options['plotmapfile'] = args.plotmapfile

    if args.plotfile:
        options['plotfile'] = args.plotfile

    if args.aeolusfile:
        options['aeolusfile'] = args.aeolusfile

    if args.modelfile:
        options['modelfile'] = args.modelfile

    if args.aeolusdir:
        options['aeolusdir'] = args.aeolusdir

    if args.modeldir:
        options['modeldir'] = args.modeldir

    if args.retrieval:
        options['retrieval'] = args.retrieval
        # adjust also the model dir in addition
        options['modeldir'] = default_model_dir_start + options['retrieval']
        options['aeolusdir'] = default_aeolus_dir_start + options['retrieval']
        options['modeldir'] = default_model_dir_start + options['retrieval']+'_test'
        options['aeolusdir'] = default_aeolus_dir_start + options['retrieval']+'_test'

    if args.logfile:
        options['logfile'] = args.logfile
        logging.basicConfig(filename=options['logfile'], level=logging.INFO)

    if args.starttime:
        options['starttime'] = np.datetime64(args.starttime).astype('datetime64[s]')

    if args.endtime:
        options['endtime'] = np.datetime64(args.endtime).astype('datetime64[s]')

    if args.variables:
        options['variables'] = args.variables.split(',')

    if args.verbose:
        options['verbose'] = True
    else:
        options['verbose'] = False

    # import read_data_fieldaeolus_l2a_data
    import os
    import sys
    import glob
    import pathlib
    import xarray as xr
    import numpy as np

    model_name = 'EMEP_MSC-W'
    aeolus_name = 'aeolus TD01'
    obj = ReadCoLocationData()
    data_dict = {}
    orbit_number_list = []
    if 'starttime' in options:
        model_data_temp = []
        aeolus_data_temp = []
        # search all nc files matching the the days
        dates_to_search_for = np.arange(options['starttime'], options['endtime'], dtype='datetime64[D]')
        for _date in dates_to_search_for:
            search_mask = "*_ALD_U_N_2A_{}*.nc".format(_date.astype('str').replace('-', ''))

            obj.logger.info(
                'searching for model files in directory {}. This might take a while...'.format(options['modeldir']))
            model_files = glob.glob(os.path.join(options['modeldir'], '**', search_mask),
                                    recursive=True)

            for model_file in sorted(model_files):
                obj.logger.info('reading model file: {}'.format(model_file))
                data_temp = obj.read_colocation_file(model_file)
                orbit = os.path.basename(model_file).split('_')[-2]
                data_temp[:, obj._DISTINDEX] = np.int_(orbit)
                # obj.ndarr2data(data_temp)
                model_data_temp = obj.ndarrappend(data_temp, model_data_temp)

            # model_data_temp = obj.data.copy()

            obj.logger.info(
                'searching for aeolus files in directory {}. This might take a while...'.format(options['aeolusdir']))
            aeolus_files = glob.glob(os.path.join(options['aeolusdir'], '**', search_mask),
                                     recursive=True)
            for aeolus_file in sorted(aeolus_files):
                obj.logger.info('reading aeolus file: {}'.format(aeolus_file))
                orbit = os.path.basename(aeolus_file).split('_')[-2]
                orbit_number_list.append(int(orbit))
                data_temp = obj.read_colocation_file(aeolus_file)
                data_temp[:, obj._DISTINDEX] = np.int_(orbit)
                # obj.ndarr2data(data_temp)
                aeolus_data_temp = obj.ndarrappend(data_temp, aeolus_data_temp)

            # aeolus_data_temp = obj.data.copy()

        data_dict[aeolus_name] = aeolus_data_temp
        data_dict[model_name] = model_data_temp
        pass
    else:
        obj.logger.info('reading aeolus file: {}'.format(options['aeolusfile']))

        data_dict[aeolus_name] = obj.read_colocation_file(options['aeolusfile'])
        obj.logger.info('reading model file: {}'.format(options['modelfile']))
        data_dict[model_name] = obj.read_colocation_file(options['modelfile'])

    # adjust extinction value
    data_dict[model_name][:, obj.INDEX_DICT['ec355aer']] = data_dict[model_name][:, obj.INDEX_DICT['ec355aer']] * 1E6

    if 'plotfile' in options:
        obj.logger.info('plotting profile to file: {}...'.format(options['plotfile']))
        obj.plot_profile_independent(data_dict, options['plotfile'], retrieval_name=options['retrieval'],
                                     plot_range=(-200., 200.),
                                     plot_nbins=40,
                                     zero_to_nans=options['zerotonans'])
        obj.logger.info('plotting done')

    if 'plotmapfile' in options:
        obj.logger.info('plotting map to file: {}...'.format(options['plotmapfile']))
        # create title with the start and end time
        for plot_index, data_name in enumerate(data_dict):
            try:
                times_existing = np.append(times_existing, data_dict[data_name][:, obj._TIMEINDEX], axis=0)
            except NameError:
                times_existing = data_dict[data_name][:, obj._TIMEINDEX]
        plot_times = np.unique(times_existing)
        title = 'dates: {}'.format(plot_times[0].astype('datetime64[s]')) + \
                ' to {}'.format(plot_times[-1].astype('datetime64[s]')) + \
                '\norbits: {} to {}'.format(min(orbit_number_list), max(orbit_number_list))
        obj.plot_location_map(options['plotmapfile'], data_dict, title=title)
        obj.logger.info('plotting map done')
