import logging
import sys

import matplotlib.pyplot as plt
import random
from typing import Tuple
import ellc
import numpy as np
from numpy import ndarray
from numpy.random import default_rng
import astropy.units as u
import astropy.constants as ac
import timesynth


class SantoTestDataGenerator:
    random_number_generator = default_rng()

    def __init__(self, output_dir: str, curves_len_boundaries: Tuple[int],
                 transit_depth_boundaries: Tuple[float],
                 transit_period_avg_std: Tuple[float],
                 white_noise_power_boundaries: Tuple[float],
                 red_noise_frequency_boundaries: Tuple[float],
                 red_noise_power_boundaries: Tuple[float],
                 max_number_of_red_noise: int,
                 curves_count=10000, curves_cadence=120, only_plot=False):
        curves_with_planets = 0
        curves_with_red_noise = 0
        for curve_index in range(0, curves_count):
            curve_len: int = int(random.uniform(curves_len_boundaries[0], curves_len_boundaries[1]))
            flux: ndarray = np.ones((2, curve_len))
            curve_len_days: float = curve_len * curves_cadence / 3600 / 24
            time: ndarray = np.linspace(0, curve_len_days, curve_len)
            white_noise_std: float = random.uniform(white_noise_power_boundaries[0], white_noise_power_boundaries[1])
            flux[0] = flux[0] + np.random.normal(loc=0, scale=white_noise_std, size=curve_len)
            number_of_red_noise = random.uniform(0, 100)
            if number_of_red_noise < 50:
                number_of_red_noise = 0
            elif number_of_red_noise < 75:
                number_of_red_noise = 1
            elif number_of_red_noise < 90:
                number_of_red_noise = 2
            else:
                number_of_red_noise = int(random.uniform(0, max_number_of_red_noise))
            if number_of_red_noise > 0:
                curves_with_red_noise = curves_with_red_noise + 1
                logging.info(f'Curves with red noise = {curves_with_red_noise}/{curve_index}')
            for index in range(0, number_of_red_noise):
                red_noise_freq: float = self.random_number_generator.uniform(red_noise_frequency_boundaries[0],
                                                                             red_noise_frequency_boundaries[1])
                red_noise_power: float = self.random_number_generator.uniform(red_noise_power_boundaries[0],
                                                                              red_noise_power_boundaries[1])
                logging.info(f'Injecting red noise in curve {curve_index} with power={red_noise_power} and '
                             f'freq={red_noise_freq}')
                red_noise = timesynth.noise.RedNoise(std=red_noise_power, tau=red_noise_freq)
                timeseries_rn: ndarray = np.zeros(curve_len)
                for time_index, value in enumerate(time):
                    rn_value = red_noise.sample_next(value, None, None)
                    rn_value = rn_value[0] if isinstance(rn_value, (list, np.ndarray)) else rn_value
                    timeseries_rn[time_index] = rn_value
                flux[0] = flux[0] + timeseries_rn
            number_of_planets = random.uniform(0, 100)
            if number_of_planets < 50:
                number_of_planets = 1
            elif number_of_planets < 80:
                number_of_planets = 2
            else:
                number_of_planets = 3
            curves_with_planets = curves_with_planets + 1
            star_radius = 1
            star_mass = 1
            for index in range(0, number_of_planets):
                period = random.gauss(transit_period_avg_std[0], transit_period_avg_std[1])
                if period < 0.5:
                    period = 0.5
                t0 = time[0] + period / random.uniform(0, 1)
                if t0 > time[-1]:
                    t0 = np.random.uniform(time[0], time[-1])
                depth = random.uniform(transit_depth_boundaries[0], transit_depth_boundaries[1])
                planet_radius = np.sqrt(depth * (star_radius ** 2))
                logging.info(f'Injecting planet in curve {curve_index} with P={period}, D={depth}')
                P1 = period * u.day
                a = np.cbrt((ac.G * star_mass * u.M_sun * P1 ** 2) / (4 * np.pi ** 2)).to(u.au)
                ld = [0.5, 0.5]
                planet_model = ellc.lc(
                    t_obs=time,
                    radius_1=(star_radius * u.R_sun).to(u.au) / a,  # star radius convert from AU to in units of a
                    radius_2=(planet_radius * u.R_sun).to(u.au) / a,
                    # convert from Rearth (equatorial) into AU and then into units of a
                    sbratio=0,
                    incl=90,
                    light_3=0,
                    t_zero=t0,
                    period=period,
                    a=None,
                    q=planet_radius / star_radius * 0.1,
                    f_c=None, f_s=None,
                    ldc_1=ld, ldc_2=None,
                    gdc_1=None, gdc_2=None,
                    didt=None,
                    domdt=None,
                    rotfac_1=1, rotfac_2=1,
                    hf_1=1.5, hf_2=1.5,
                    bfac_1=None, bfac_2=None,
                    heat_1=None, heat_2=None,
                    lambda_1=None, lambda_2=None,
                    vsini_1=None, vsini_2=None,
                    t_exp=None, n_int=None,
                    grid_1='default', grid_2='default',
                    ld_1='quad', ld_2=None,
                    shape_1='sphere', shape_2='sphere',
                    spots_1=None, spots_2=None,
                    exact_grav=False, verbose=1)
                flux = flux + planet_model - 1
            if number_of_planets > 0:
                logging.info(f'Curves with planets = {curves_with_planets}/{curve_index}')
            if only_plot:
                plt.scatter(time, flux[0])
                plt.show()
            else:
                np.savetxt(f'{output_dir}/{curve_index}_model.csv', flux, delimiter=',')
        logging.info(f'Curves with red noise = {curves_with_red_noise}/{curves_count}')
        logging.info(f'Curves with planets = {curves_with_planets}/{curves_count}')


if not isinstance(logging.root, logging.RootLogger):
    logging.root = logging.RootLogger(logging.INFO)

formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
while len(logger.handlers) > 0:
    logger.handlers.pop()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)

SantoTestDataGenerator(output_dir="/data/scratch/ml/santo/training_data/",
                       curves_len_boundaries=(15000, 30000),
                       curves_count=10000,
                       curves_cadence=120,
                       transit_depth_boundaries=(0.0001, 0.05),
                       transit_period_avg_std=(7.5, 6),
                       red_noise_frequency_boundaries=(0.01, 10),
                       red_noise_power_boundaries=(0.001, 0.05),
                       white_noise_power_boundaries=(0.001, 0.05),
                       max_number_of_red_noise=5,
                       only_plot=False)
