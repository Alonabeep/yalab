import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sonar_pos_analysis import plot_water_height_data, get_real_water_height, smoothen_height_data, \
    plot_basic_height_data
from temp_pos_analysis import plot_temp_over_time_data
from temperature_analysis import plot_room_temp

DEFAULT_FILE_PATH = '..\\Results\\18.5.2020\\exp2 - cooling over night.csv'  # yonatan

DEFAULT_HEADER_ROW = 1
ROOM_TEMP = 23.8


def read_experiment_data(file_path=DEFAULT_FILE_PATH, header_row=DEFAULT_HEADER_ROW, measure_room_temp=False):
    data_cols = ['Time (s)', 'Temperature (C)']
    col_variable_names = {'Time (s)': 'time', 'Temperature (C)': 'temp'}
    if measure_room_temp:
        data_cols.append('Temperature2')
        col_variable_names['Temperature2'] = 'room_temp'

    experiment_data = pd.read_csv(file_path, header=header_row - 1, usecols=data_cols) \
        .rename(columns=col_variable_names)

    return experiment_data


def plot_single_experiment(data_path):
    exp_data = read_experiment_data(data_path)

    temp_amplitude = exp_data.temp.max() - exp_data.temp.min()
    # start the linear fit only when the temperature reaches its 90th percentile
    temp_start_fit_threshold = exp_data.temp.min() + 0.9 * temp_amplitude
    start_fit_time = exp_data.time[exp_data.temp > temp_start_fit_threshold].iat[0]

    fig, axs = plt.subplots(2, sharex=True)

    get_real_water_height(exp_data)
    plot_water_height_data(exp_data, axs[0], fit_func_to_data=True, start_fit_time=start_fit_time)

    # smoothen_height_data(exp_data)
    # plot_basic_height_data(exp_data, axs[0])

    plot_temp_over_time_data(exp_data, axs[1])

    # make them have the same x axis
    plt.subplots_adjust(hspace=0)
    for ax in axs:
        ax.set_title('')

    plt.show()


def compare_several_experiments_temperature(experiments_data_paths):
    plt.figure()
    axes = plt.gca()

    for data_path, time_offset in experiments_data_paths:
        exp_data = read_experiment_data(data_path)
        exp_data.time += time_offset

        if time_offset > 0:
            temp_amplitude = exp_data.temp.max() - ROOM_TEMP
            plot_temp_over_time_data(exp_data, axes, temp_amplitude=temp_amplitude, start_fit_temp=ROOM_TEMP)
        else:
            plot_temp_over_time_data(exp_data, axes)

    plt.show()


def compare_several_experiments_height(experiments_data_paths):
    plt.figure()
    axes = plt.gca()

    # ignore time offset because all of them started at same height
    for data_path, time_offset in experiments_data_paths:
        exp_data = read_experiment_data(data_path)

        get_real_water_height(exp_data)

        plot_water_height_data(exp_data, axes, fit_func_to_data=True)

    plt.show()


def plot_cooling_and_heating_times(cooling_data_path, heating_data_path, min_time=2500, max_time=12000):
    fig, axs = plt.subplots(2, sharex=True)

    cooling_data = read_experiment_data(cooling_data_path, measure_room_temp=True)
    heating_data = read_experiment_data(heating_data_path)

    cooling_data = cooling_data[(cooling_data.time > min_time) & (cooling_data.time < max_time)]
    heating_data = heating_data[(heating_data.time > min_time) & (heating_data.time < max_time)]

    plot_room_temp(cooling_data, axs[0], ylabel='Room temperature[$\degree$C]', c='red', marker='x')
    plot_temp_over_time_data(heating_data, axs[1], fit_func_to_data=False, ylabel='Water temperature[$\degree$C]')

    plt.subplots_adjust(hspace=0)

    for ax in axs:
        ax.get_legend().remove()
        ax.set_title('')
        for t in range(min_time, max_time, 1250):
            ax.axvline(t, c='k', linestyle='--')

    axs[0].set_title('Comparison between room and water temperature fluctuations')

    plt.show()


if __name__ == '__main__':
    plot_cooling_and_heating_times(DEFAULT_FILE_PATH, '..\\Results\\18.5.2020\\exp1 - last run only.csv')

    # plot_single_experiment(DEFAULT_FILE_PATH)

    # experiments_data = [('..\\Results\\13.5.2020\\ex1 grouped - 13.5.2020.csv', 0),
    #                     ('..\\Results\\18.5.2020\\exp1 - last run only.csv', 2100),
    #                     ('..\\Results\\20.5.2020\\ex1.csv', 0)]
    #
    # compare_several_experiments_temperature(experiments_data)
    # compare_several_experiments_height(experiments_data)
