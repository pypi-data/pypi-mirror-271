import logging
import os
import sys

import matplotlib.pyplot as plt
import foldedleastsquares
import wotan
from lcbuilder.helper import LcbuilderHelper
from numpy.random import default_rng
from exoml.ete6.ete6_generator import Ete6ModelGenerator
from exoml.ml.encoding.time_position import value_encode_times
from sklearn.utils import shuffle
import numpy as np
import pandas as pd


class WatsonPlanetModelGenerator(Ete6ModelGenerator):
    def __init__(self, injected_objects_df, lcs_dir, star_filename, lc_filename,
                 batch_size, input_sizes, transits_mask=None, zero_epsilon=1e-7,
                 measurements_per_point=2, plot_inputs=False):
        super().__init__(zero_epsilon, shuffle_batch=False)
        self.injected_objects_df = injected_objects_df
        self.lcs_dir = lcs_dir
        self.star_filename = star_filename
        self.lc_filename = lc_filename
        self.batch_size = batch_size
        self.input_sizes = input_sizes
        self.transit_masks = transits_mask
        self.random_number_generator = default_rng()
        self.measurements_per_point = measurements_per_point
        self.plot_inputs = plot_inputs

    def __len__(self):
        return (np.ceil(len(self.injected_objects_df) / float(self.batch_size))).astype(int)

    def class_weights(self):
        return {0: 1, 1: 1}

    def _plot_df(self, df, type, scenario):
        fig, axs = plt.subplots(2, 3, figsize=(12, 6), constrained_layout=True)
        axs[0][0].scatter(df['#time'], df['flux'])
        axs[0][1].scatter(df['#time'], df['centroid_x'])
        axs[0][2].scatter(df['#time'], df['centroid_y'])
        axs[1][0].scatter(df['#time'], df['bck_flux'])
        axs[1][1].scatter(df['#time'], df['motion_x'])
        axs[1][2].scatter(df['#time'], df['motion_y'])
        plt.title(type + " " + scenario)
        plt.show()
        plt.clf()
        plt.close()

    def _plot_input(self, input_array, input_err_array, type, scenario, save_dir=None):
        if self.plot_inputs:
            transposed_err_array = []
            transposed_array = np.transpose(input_array)
            fig, axs = plt.subplots(2, 2, figsize=(24, 12), constrained_layout=True)
            current_array = transposed_array[0]
            current_array_mask = np.argwhere((~np.isnan(current_array)) & (current_array > self.zero_epsilon)).flatten()
            current_array = current_array[current_array_mask]
            time_array = current_array
            axs[0][0].scatter(np.arange(0, len(current_array)), current_array)
            # axs[0][0].set_ylim(np.mean(current_array) - 6 * np.std(current_array), np.mean(current_array) + 6 * np.std(current_array))
            axs[0][0].set_title("Time")
            current_array = transposed_array[1]
            current_array_mask = np.argwhere((~np.isnan(current_array)) & (current_array > self.zero_epsilon)).flatten()
            current_array = current_array[current_array_mask]
            if input_err_array is not None:
                transposed_err_array = np.transpose(input_err_array)
                axs[0][1].errorbar(time_array[current_array_mask], current_array, ls='none',
                                   yerr=transposed_err_array[1][current_array_mask], color="orange", alpha=0.5)
            axs[0][1].scatter(time_array[current_array_mask], current_array)
            if len(transposed_array) > 2:
                current_array = transposed_array[2]
                current_array_mask = np.argwhere(
                    (~np.isnan(current_array)) & (current_array > self.zero_epsilon)).flatten()
                current_array = current_array[current_array_mask]
                if input_err_array is not None:
                    axs[1][0].errorbar(time_array[current_array_mask], transposed_array[2], ls='none',
                                       yerr=transposed_err_array[2][current_array_mask], color="orange", alpha=0.5)
                axs[1][0].scatter(time_array[current_array_mask], current_array)
            #axs[0][1].set_ylim(np.mean(current_array) - 6 * np.std(current_array), np.mean(current_array) + 6 * np.std(current_array))
            axs[0][1].set_title("Flux")
            axs[1][0].set_title("Flux 1")
            # current_array = transposed_array[8]
            # current_array_mask = np.argwhere((~np.isnan(current_array)) & (current_array > self.zero_epsilon)).flatten()
            # current_array = current_array[current_array_mask]
            # axs[1][1].errorbar(time_array[current_array_mask], current_array,
            #                    yerr=transposed_err_array[8][current_array_mask], color="orange", alpha=0.5)
            # axs[1][1].scatter(time_array[current_array_mask], current_array)
            # # axs[1][1].set_ylim(np.mean(current_array) - 6 * np.std(current_array),
            # #                    np.mean(current_array) + 6 * np.std(current_array))
            # axs[1][1].set_title("Flux 2")
            # current_array = transposed_array[9]
            # current_array_mask = np.argwhere((~np.isnan(current_array)) & (current_array > self.zero_epsilon)).flatten()
            # current_array = current_array[current_array_mask]
            # axs[2][0].errorbar(time_array[current_array_mask], current_array,
            #                    yerr=transposed_err_array[9][current_array_mask], color="orange", alpha=0.5)
            # axs[2][0].scatter(time_array[current_array_mask], current_array)
            # # axs[2][0].set_ylim(np.mean(current_array) - 6 * np.std(current_array),
            # #                    np.mean(current_array) + 6 * np.std(current_array))
            # axs[2][0].set_title("Flux 3")
            # current_array = transposed_array[10]
            # current_array_mask = np.argwhere((~np.isnan(current_array)) & (current_array > self.zero_epsilon)).flatten()
            # current_array = current_array[current_array_mask]
            # axs[2][1].errorbar(time_array[current_array_mask], current_array,
            #                    yerr=transposed_err_array[10][current_array_mask], color="orange", alpha=0.5)
            # axs[2][1].scatter(time_array[current_array_mask], current_array)
            # # axs[2][1].set_ylim(np.mean(current_array) - 6 * np.std(current_array),
            # #                    np.mean(current_array) + 6 * np.std(current_array))
            # axs[2][1].set_title("Flux 4")
            # current_array = transposed_array[11]
            # current_array_mask = np.argwhere((~np.isnan(current_array)) & (current_array > self.zero_epsilon)).flatten()
            # current_array = current_array[current_array_mask]
            # axs[3][0].errorbar(time_array[current_array_mask], current_array,
            #                    yerr=transposed_err_array[11][current_array_mask], color="orange", alpha=0.5)
            # axs[3][0].scatter(time_array[current_array_mask], current_array)
            # # axs[3][0].set_ylim(np.mean(current_array) - 6 * np.std(current_array),
            # #                    np.mean(current_array) + 6 * np.std(current_array))
            # axs[3][0].set_title("Flux 5")
            # current_array = transposed_array[6]
            # current_array_mask = np.argwhere((~np.isnan(current_array)) & (current_array > self.zero_epsilon)).flatten()
            # current_array = current_array[current_array_mask]
            # axs[3][1].errorbar(time_array[current_array_mask], current_array,
            #                    yerr=transposed_err_array[6][current_array_mask], color="orange", alpha=0.5)
            # axs[3][1].scatter(time_array[current_array_mask], current_array)
            # # axs[3][1].set_ylim(np.mean(current_array) - 6 * np.std(current_array), np.mean(current_array) + 6 * np.std(current_array))
            # axs[3][1].set_title("Bck Flux")
            # current_array = transposed_array[2]
            # current_array_mask = np.argwhere((~np.isnan(current_array)) & (current_array > self.zero_epsilon)).flatten()
            # current_array = current_array[current_array_mask]
            # axs[4][0].errorbar(time_array[current_array_mask], current_array,
            #                    yerr=transposed_err_array[2][current_array_mask], color="orange", alpha=0.5)
            # axs[4][0].scatter(time_array[current_array_mask], current_array)
            # # axs[4][0].set_ylim(np.mean(current_array) - 6 * np.std(current_array), np.mean(current_array) + 6 * np.std(current_array))
            # axs[4][0].set_title("Centroid X")
            # current_array = transposed_array[3]
            # current_array_mask = np.argwhere((~np.isnan(current_array)) & (current_array > self.zero_epsilon)).flatten()
            # current_array = current_array[current_array_mask]
            # axs[4][1].errorbar(time_array[current_array_mask], current_array,
            #                    yerr=transposed_err_array[3][current_array_mask], color="orange", alpha=0.5)
            # axs[4][1].scatter(time_array[current_array_mask], current_array)
            # # axs[4][1].set_ylim(np.mean(current_array) - 6 * np.std(current_array), np.mean(current_array) + 6 * np.std(current_array))
            # axs[4][1].set_title("Centroid Y")
            # current_array = transposed_array[4]
            # current_array_mask = np.argwhere((~np.isnan(current_array)) & (current_array > self.zero_epsilon)).flatten()
            # current_array = current_array[current_array_mask]
            # axs[5][0].errorbar(time_array[current_array_mask], current_array,
            #                    yerr=transposed_err_array[4][current_array_mask], color="orange", alpha=0.5)
            # axs[5][0].scatter(time_array[current_array_mask], current_array)
            # # axs[5][0].set_ylim(np.mean(current_array) - 6 * np.std(current_array), np.mean(current_array) + 6 * np.std(current_array))
            # axs[5][0].set_title("Motion Y")
            # current_array = transposed_array[5]
            # current_array_mask = np.argwhere((~np.isnan(current_array)) & (current_array > self.zero_epsilon)).flatten()
            # current_array = current_array[current_array_mask]
            # axs[5][1].errorbar(time_array[current_array_mask], current_array,
            #                    yerr=transposed_err_array[5][current_array_mask], color="orange", alpha=0.5)
            # axs[5][1].scatter(time_array[current_array_mask], current_array)
            # # axs[5][1].set_ylim(np.mean(current_array) - 6 * np.std(current_array), np.mean(current_array) + 6 * np.std(current_array))
            # axs[5][1].set_title("Motion Y")
            fig.suptitle(type + " " + scenario)
            if save_dir:
                if not os.path.exists(save_dir):
                    os.mkdir(save_dir)
                plt.savefig(f'{save_dir}/{type}_{scenario}.png')
            else:
                plt.show()
            plt.clf()
            plt.close()

    def plot_single_data(self, lc_df, target_row):
        fig, axs = plt.subplots(1, 1, figsize=(8, 4), constrained_layout=True)
        axs.scatter(lc_df['#time'], lc_df['flux_0'])
        axs.set_ylim(0.5 - target_row['tce_depth'] / 0.5e6, 0.505)
        plt.show()
        plt.clf()
        plt.close()

    def mask_other_signals(self, data_df, transits_mask, time_key='#time'):
        if transits_mask is not None:
            for item_mask in transits_mask:
                mask = foldedleastsquares.transit_mask(data_df[time_key].to_numpy(), item_mask['P'],
                                                       2 * item_mask['D'] / 60 / 24, item_mask['T0'])
                data_df = data_df[~mask]
        return data_df

    def __getitem__(self, idx):
        max_index = (idx + 1) * self.batch_size
        max_index = len(self.injected_objects_df) if max_index > len(self.injected_objects_df) else max_index
        target_indexes = np.arange(idx * self.batch_size, max_index, 1)
        injected_objects_df = self.injected_objects_df.iloc[target_indexes]
        if self.shuffle_batch:
            injected_objects_df = shuffle(injected_objects_df)
        star_array = np.empty((len(target_indexes), 3, 1))
        star_neighbours_array = np.empty((len(target_indexes), self.input_sizes[1], 1))
        #[period, planet radius, number of transits, ratio of good transits, transit depth, transit_offset_pos - transit_offset_err]
        scalar_values = np.empty((len(target_indexes), 8, 1))
        global_flux_array = np.empty((len(target_indexes), self.input_sizes[2], self.measurements_per_point))
        folded_flux_even_array = np.empty((len(target_indexes), self.input_sizes[3], self.measurements_per_point))
        folded_flux_odd_array = np.empty((len(target_indexes), self.input_sizes[3], self.measurements_per_point))
        folded_flux_even_subhar_array = np.empty((len(target_indexes), self.input_sizes[3], self.measurements_per_point))
        folded_flux_odd_subhar_array = np.empty((len(target_indexes), self.input_sizes[3], self.measurements_per_point))
        folded_flux_even_har_array = np.empty((len(target_indexes), self.input_sizes[3], self.measurements_per_point))
        folded_flux_odd_har_array = np.empty((len(target_indexes), self.input_sizes[3], self.measurements_per_point))
        global_flux_array_err = np.empty((len(target_indexes), self.input_sizes[2], self.measurements_per_point))
        folded_flux_even_array_err = np.empty((len(target_indexes), self.input_sizes[3], self.measurements_per_point))
        folded_flux_odd_array_err = np.empty((len(target_indexes), self.input_sizes[3], self.measurements_per_point))
        folded_flux_even_subhar_array_err = np.empty((len(target_indexes), self.input_sizes[3], self.measurements_per_point))
        folded_flux_odd_subhar_array_err = np.empty((len(target_indexes), self.input_sizes[3], self.measurements_per_point))
        folded_flux_even_har_array_err = np.empty((len(target_indexes), self.input_sizes[3], self.measurements_per_point))
        folded_flux_odd_har_array_err = np.empty((len(target_indexes), self.input_sizes[3], self.measurements_per_point))
        folded_centroids_array = np.empty((len(target_indexes), self.input_sizes[3], 3))
        folded_centroids_array_err = np.empty((len(target_indexes), self.input_sizes[3], 3))
        folded_og_array = np.empty((len(target_indexes), self.input_sizes[3], 2))
        folded_og_array_err = np.empty((len(target_indexes), self.input_sizes[3], 2))
        batch_data_values = np.empty((len(target_indexes), 1))
        i = 0
        for df_index, target_row in injected_objects_df.iterrows():
            #TODO refactor to use mission for object_id
            object_id = target_row['object_id'].split(' ')
            mission_id = object_id[0]
            target_id = int(object_id[1])
            period = target_row['period']
            epoch = target_row['epoch']
            duration = target_row['duration(h)'] / 24
            duration_to_period = duration / period
            batch_data_values[i] = [0]
            file_prefix = self.lcs_dir + '/' #+ mission_id + '_' + str(target_id)
            #TODO refactor to use mission for _lc files
            lc_filename = self.lc_filename
            centroids_filename = file_prefix + 'centroids.csv'
            og_filename = file_prefix + 'og_dg.csv'
            lc_df = pd.read_csv(lc_filename, usecols=['#time', 'flux'], low_memory=True)
            centroids_df = pd.read_csv(centroids_filename, usecols=['time', 'centroids_ra', 'centroids_dec'],
                                                low_memory=True)
            og_df = pd.read_csv(og_filename, usecols=['time', 'og_flux', 'halo_flux', 'core_flux'], low_memory=True)
            if lc_df is None:
                logging.warning("No curve for target " + file_prefix)
                raise ValueError("No curve for target " + file_prefix)
            lc_df = lc_df.sort_values(by=['#time'])
            lc_df = self.mask_other_signals(lc_df, transits_mask=self.transit_masks, time_key='#time')
            centroids_df = self.mask_other_signals(centroids_df, transits_mask=self.transit_masks, time_key='time')
            og_df = self.mask_other_signals(og_df, transits_mask=self.transit_masks, time_key='time')
            lc_df['flux'] = wotan.flatten(lc_df['#time'].to_numpy(), lc_df['flux'].to_numpy(), duration * 4, method='biweight')
            centroids_df = centroids_df.sort_values(by=['time'])
            centroids_df['centroids_ra'] = wotan.flatten(centroids_df['time'].to_numpy(), centroids_df['centroids_ra'].to_numpy(), duration * 4, method='biweight')
            centroids_df['centroids_dec'] = wotan.flatten(centroids_df['time'].to_numpy(), centroids_df['centroids_dec'].to_numpy(), duration * 4, method='biweight')
            centroids_df['time'] = self.fold(centroids_df['time'].to_numpy(), period, epoch + period / 2)
            og_df = og_df.sort_values(by=['time'])
            og_df['halo_flux'] = wotan.flatten(og_df['time'].to_numpy(), og_df['halo_flux'].to_numpy(), duration * 4, method='biweight')
            og_df['core_flux'] = wotan.flatten(og_df['time'].to_numpy(), og_df['core_flux'].to_numpy(), duration * 4, method='biweight')
            og_df['og_flux'] = og_df['halo_flux'] - og_df['core_flux']
            og_df = og_df.drop(columns=['halo_flux', 'core_flux'])
            og_df['time'] = self.fold(og_df['time'].to_numpy(), period, epoch + period / 2)
            centroids_df = centroids_df.sort_values(by=['time'])
            og_df = og_df.sort_values(by=['time'])
            centroids_df = self._prepare_input_centroids(centroids_df)
            og_df = self._prepare_input_og(og_df)
            og_df = og_df[(og_df['time'] > 0.5 - duration_to_period * 3) & (
                    og_df['time'] < 0.5 + duration_to_period * 3)]
            centroids_df = centroids_df[(centroids_df['time'] > 0.5 - duration_to_period * 3) & (
                    centroids_df['time'] < 0.5 + duration_to_period * 3)]
            folded_centroids_array[i], folded_centroids_array_err[i] = self.bin_by_time(centroids_df.to_numpy(), self.input_sizes[3], target_row['object_id'])
            folded_og_array[i], folded_og_array_err[i] = self.bin_by_time(og_df.to_numpy(), self.input_sizes[3], target_row['object_id'])
            #TODO refactor to use mission for star files
            star_df = pd.read_csv(self.star_filename, usecols=['Teff', 'radius', 'mass', 'ra', 'dec'],
                                  index_col=False)
            star_neighbours_df = pd.read_csv(self.star_filename,
                                             usecols=['Teff', 'lum', 'v', 'j', 'k', 'h', 'radius', 'mass'], index_col=False)
            star_neighbours_df = self._prepare_input_neighbour_stars(star_neighbours_df)
            star_df, ra, dec = self._prepare_input_star(star_df)
            lc_df, good_transits_count, transits_count = self._prepare_input_lc(lc_df, period, epoch, duration,
                                                                                time_key='#time', flux_key='flux')
            not_null_times_args = np.argwhere(lc_df['#time'].to_numpy() > 0).flatten()
            lc_df = lc_df.iloc[not_null_times_args]
            offset_filename = file_prefix + 'source_offsets.csv'
            offset_df = pd.read_csv(offset_filename, low_memory=True)
            row = offset_df[offset_df['name'] == 'mean'].iloc[0]
            offset_ra = row['ra']
            offset_dec = row['dec']
            offset_ra_err = row['ra_err']
            offset_dec_err = row['dec_err']
            offset_err = offset_ra_err if offset_ra_err > offset_dec_err else offset_dec_err
            offset_err = offset_err * 60 * 60
            target_dist = np.sqrt((offset_ra - ra) ** 2 + (offset_dec - dec) ** 2)
            offset_err = offset_err if offset_err > 0 else target_dist * 2
            offset_err = offset_err if offset_err < 1 else 1 - self.zero_epsilon
            good_transits_count_norm = good_transits_count / 20
            good_transits_count_norm = good_transits_count_norm if good_transits_count_norm < 1 else 1 - self.zero_epsilon
            good_transits_ratio = good_transits_count / transits_count if transits_count > 0 else self.zero_epsilon
            good_transits_ratio = good_transits_ratio if good_transits_ratio < 1 else 1 - self.zero_epsilon
            planet_radius = target_row['radius(earth)'] / 300
            planet_radius = planet_radius if planet_radius < 1 else 1 - self.zero_epsilon
            depth = target_row['depth_primary'] / 1e3
            depth = depth if depth < 1 else 1 - self.zero_epsilon
            scalar_values[i] = np.transpose([[period / 1200 if period < 1200 else 1, duration / 15, depth,
                                              planet_radius, good_transits_count_norm,
                                              good_transits_ratio,
                                              target_dist if not np.isnan(target_dist) else self.zero_epsilon,
                                              offset_err]])
            #['ld_a', 'ld_b', 'Teff', 'lum', 'logg', 'radius', 'mass', 'v', 'j', 'h', 'k'])
            neighbours_array = star_neighbours_df.to_numpy().flatten()
            #star_neighbours_array[i] = np.transpose([neighbours_array if len(neighbours_array) == 9 * 15 \
            #    else neighbours_array + np.zeros(9 * 15 - len(neighbours_array))])
            star_array[i] = np.transpose([star_df.to_numpy()])
            time = lc_df['#time'].to_numpy()
            # Global flux
            # Shifting data 1/4 so that main transit and possible occultation don't get cut by the borders
            lc_df_sorted_fold = lc_df.copy()
            lc_df_sorted_fold['#time'] = self.fold(time, period, epoch + period / 4)
            lc_df_sorted_fold = lc_df_sorted_fold.sort_values(by=['#time'])
            global_flux_array[i], global_flux_array_err[i] = \
                self.bin_by_time(lc_df_sorted_fold.to_numpy(), self.input_sizes[2], target_row['object_id'])
            # Focus flux even
            lc_df_focus = lc_df.copy()
            lc_df_focus['#time'] = self.fold(time, period, epoch)
            lc_df_focus = lc_df_focus.sort_values(by=['#time'])
            lc_df_focus = lc_df_focus[(lc_df_focus['#time'] > 0.5 - duration_to_period * 3) &
                                      (lc_df_focus['#time'] < 0.5 + duration_to_period * 3)]
            folded_flux_even_array[i], folded_flux_even_array_err[i] = \
                self.bin_by_time(lc_df_focus.to_numpy(), self.input_sizes[3], target_row['object_id'])
            # Focus flux odd
            lc_df_focus = lc_df.copy()
            lc_df_focus['#time'] = self.fold(time, period, epoch + period / 2)
            lc_df_focus = lc_df_focus.sort_values(by=['#time'])
            lc_df_focus = lc_df_focus[(lc_df_focus['#time'] > 0.5 - duration_to_period * 3) &
                                      (lc_df_focus['#time'] < 0.5 + duration_to_period * 3)]
            folded_flux_odd_array[i], folded_flux_odd_array_err[i] = \
                self.bin_by_time(lc_df_focus.to_numpy(), self.input_sizes[4], target_row['object_id'])
            # Focus flux harmonic even
            lc_df_focus = lc_df.copy()
            lc_df_focus['#time'] = self.fold(time, period * 2, epoch)
            lc_df_focus = lc_df_focus.sort_values(by=['#time'])
            lc_df_focus = lc_df_focus[(lc_df_focus['#time'] > 0.5 - duration_to_period * 3) &
                                      (lc_df_focus['#time'] < 0.5 + duration_to_period * 3)]
            folded_flux_even_har_array[i], folded_flux_even_har_array_err[i] = \
                self.bin_by_time(lc_df_focus.to_numpy(), self.input_sizes[7], target_row['object_id'])
            # Focus flux harmonic odd
            lc_df_focus = lc_df.copy()
            lc_df_focus['#time'] = self.fold(time, period * 2, epoch + period)
            lc_df_focus = lc_df_focus.sort_values(by=['#time'])
            lc_df_focus = lc_df_focus[(lc_df_focus['#time'] > 0.5 - duration_to_period * 3) &
                                      (lc_df_focus['#time'] < 0.5 + duration_to_period * 3)]
            folded_flux_odd_har_array[i], folded_flux_odd_har_array_err[i] = \
                self.bin_by_time(lc_df_focus.to_numpy(), self.input_sizes[8], target_row['object_id'])
            # Focus flux sub-harmonic even
            lc_df_focus = pd.DataFrame(columns=['#time', 'flux'])
            time, flux0, _ = LcbuilderHelper.mask_transits(time,
                                                            lc_df.copy()['flux'].to_numpy(), period, duration * 2,
                                                            epoch)
            lc_df_focus['#time'] = time
            lc_df_focus['flux'] = flux0
            lc_df_focus['#time'] = self.fold(time, period / 2, epoch)
            lc_df_focus = lc_df_focus.sort_values(by=['#time'])
            lc_df_focus = lc_df_focus[(lc_df_focus['#time'] > 0.5 - duration_to_period * 3) &
                                      (lc_df_focus['#time'] < 0.5 + duration_to_period * 3)]
            folded_flux_even_subhar_array[i], folded_flux_even_subhar_array_err[i] = \
                self.bin_by_time(lc_df_focus.to_numpy(), self.input_sizes[5], target_row['object_id'])
            # Focus flux sub-harmonic odd
            lc_df_focus = pd.DataFrame(columns=['#time', 'flux'])
            lc_df_focus['#time'] = time
            lc_df_focus['flux'] = flux0
            lc_df_focus['#time'] = self.fold(time, period / 2, epoch + period / 4)
            lc_df_focus = lc_df_focus.sort_values(by=['#time'])
            lc_df_focus = lc_df_focus[(lc_df_focus['#time'] > 0.5 - duration_to_period * 3) &
                                      (lc_df_focus['#time'] < 0.5 + duration_to_period * 3)]
            folded_flux_odd_subhar_array[i], folded_flux_odd_subhar_array_err[i] = \
                self.bin_by_time(lc_df_focus.to_numpy(), self.input_sizes[6], target_row['object_id'])
            self.assert_in_range(object_id, scalar_values[i], None)
            self.assert_in_range(object_id, global_flux_array[i], global_flux_array_err[i])
            self.assert_in_range(object_id, star_array[i], None)
            self.assert_in_range(object_id, folded_flux_even_array[i], folded_flux_even_array_err[i])
            self.assert_in_range(object_id, folded_flux_odd_array[i], folded_flux_odd_array_err[i])
            self.assert_in_range(object_id, folded_flux_even_subhar_array[i], folded_flux_even_subhar_array_err[i])
            self.assert_in_range(object_id, folded_flux_odd_subhar_array[i], folded_flux_odd_subhar_array_err[i])
            self.assert_in_range(object_id, folded_flux_even_har_array[i], folded_flux_even_har_array_err[i])
            self.assert_in_range(object_id, folded_flux_odd_har_array[i], folded_flux_odd_har_array_err[i])
            self.assert_in_range(object_id, folded_centroids_array[i], folded_centroids_array_err[i])
            self.assert_in_range(object_id, folded_og_array[i], folded_og_array_err[i])
            inputs_save_dir = f'{self.lcs_dir}/iatson/'
            self._plot_input(global_flux_array[i], global_flux_array_err[i], target_row['object_id'], "global", save_dir=inputs_save_dir)
            self._plot_input(folded_flux_even_array[i], folded_flux_even_array_err[i], target_row['object_id'], "even", save_dir=inputs_save_dir)
            self._plot_input(folded_flux_odd_array[i], folded_flux_odd_array_err[i], target_row['object_id'], "odd", save_dir=inputs_save_dir)
            self._plot_input(folded_flux_even_har_array[i], folded_flux_even_har_array_err[i], target_row['object_id'], "even_har", save_dir=inputs_save_dir)
            self._plot_input(folded_flux_odd_har_array[i], folded_flux_odd_har_array_err[i], target_row['object_id'], "odd_har", save_dir=inputs_save_dir)
            # self._plot_input(folded_flux_even_subhar_array[i], folded_flux_even_subhar_array_err[i], target_row['object_id'], "even_subhar")
            # self._plot_input(folded_flux_odd_subhar_array[i], folded_flux_odd_subhar_array_err[i], target_row['object_id'], "odd_subhar")
            self._plot_input(folded_og_array[i], folded_og_array_err[i], target_row['object_id'], "OG", save_dir=inputs_save_dir)
            self._plot_input(folded_centroids_array[i], folded_centroids_array_err[i], target_row['object_id'], "CENTROIDS", save_dir=inputs_save_dir)
            i = i + 1
        filter_channels = np.array([0, 1, 6, 7, 8, 9, 10, 11])
        return [scalar_values[:, [0, 1, 2, 3, 4, 5]], scalar_values[:, [6, 7]],
                star_array, #Only Teff, Rad and Mass
                # star_neighbours_array,
                global_flux_array,
                folded_flux_even_array,
                folded_flux_odd_array,
                # folded_flux_even_subhar_array,
                # folded_flux_odd_subhar_array,
                folded_flux_even_har_array,
                folded_flux_odd_har_array,
                folded_centroids_array, folded_og_array], \
            batch_data_values
        # return [star_array,
        #         #star_neighbours_array,
        #         global_flux_array, global_flux_array_err,
        #         folded_flux_even_array, folded_flux_even_array_err,
        #         folded_flux_odd_array, folded_flux_odd_array_err,
        #         folded_flux_even_subhar_array, folded_flux_even_subhar_array_err,
        #         folded_flux_odd_subhar_array, folded_flux_odd_subhar_array_err,
        #         folded_flux_even_har_array, folded_flux_even_har_array_err,
        #         folded_flux_odd_har_array, folded_flux_odd_har_array_err,
        #         folded_centroids_array, folded_centroids_array_err, folded_og_array, folded_og_array_err], \
        #     batch_data_values
