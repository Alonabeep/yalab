import matplotlib.pyplot as plt
import pandas as pd

from cooling_temperature_analysis import plot_room_temp, plot_cooling_time
from sonar_pos_analysis import plot_water_height_data, get_real_water_height
from temp_pos_analysis import plot_temp_over_time_data
from utils import fit_and_plot_line

DATA_PATH = '/home/avni1alon/alon/Lab/yalab/data/'  # alon
DEFAULT_FILE_PATH = DATA_PATH + 'water_experiment_4_Run_2.csv'  # alon
# DEFAULT_FILE_PATH = '..\\Results\\18.5.2020\\exp2 - cooling over night.csv'  # yonatan

DEFAULT_HEADER_ROW = 1
ROOM_TEMP = 23.8


def read_experiment_data(file_path=DEFAULT_FILE_PATH, header_row=DEFAULT_HEADER_ROW, measure_room_temp=False,
                         cooling_measurement=False):
    data_cols = ['Time (s)', 'Temperature (C)', 'Position (m)']
    col_variable_names = {'Time (s)': 'time', 'Temperature (C)': 'temp', 'Position (m)': 'pos'}
    if measure_room_temp:
        data_cols.append('Temperature2')
        col_variable_names['Temperature2'] = 'room_temp'
    if cooling_measurement:
        data_cols.remove('Position (m)')
        col_variable_names.pop('Position (m)')

    experiment_data = pd.read_csv(file_path, header=header_row - 1, usecols=data_cols) \
        .rename(columns=col_variable_names)

    return experiment_data


def load_camera_data():
    camera_water_height1 = [0.125, 0.125, 0.125, 0.1225, 0.12, 0.115, 0.11, 0.10625, 0.1025, 0.1, 0.09, 0.0875, 0.085,
                            0.08375, 0.0825]
    camera_time1 = list(range(0, 11 * 1800, 1800)) + [19755, 20355, 20955, 21555]
    camera_water_height2 = [0.12375, 0.11875, 0.12375, 0.1175, 0.1125, 0.1075, 0.10375, 0.1, 0.09125, 0.0875, 0.0825,
                            0.075, 0.07]
    camera_time2 = [2230, 3730, 5230, 6730, 8230, 9730, 11230, 12730, 14230, 15730, 17230, 18730, 20230]
    camera_water_height3 = [0.10875, 0.1, 0.09, 0.08, 0.07, 0.06]
    camera_time3 = list(range(0, 6 * 1500, 1500))
    return camera_water_height1, camera_time1, camera_water_height2, camera_time2, camera_water_height3, camera_time3


def plot_single_experiment(data_path):
    exp_data = read_experiment_data(data_path)

    camera_water_height1, camera_time1, camera_water_height2, camera_time2, camera_water_height3, camera_time3 = load_camera_data()

    temp_amplitude = exp_data.temp.max() - exp_data.temp.min()
    # start the linear fit only when the temperature reaches its 90th percentile
    temp_start_fit_threshold = exp_data.temp.min() + 0.9 * temp_amplitude
    start_fit_time = exp_data.time[exp_data.temp > temp_start_fit_threshold].iat[0]

    fig, axs = plt.subplots(2, sharex=True)

    get_real_water_height(exp_data)
    plot_water_height_data(exp_data, axes=axs[0], label_fit=True, fit_func_to_data=True, start_fit_time=start_fit_time,
                           show_camera_height=False, save_plots=False)

    plot_temp_over_time_data(exp_data, axs[1])

    '''
    # make them have the same x axis
    plt.subplots_adjust(hspace=0)
    for ax in axs:
        ax.set_title('')
    '''

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

    markers = ['.', 'x', '+']
    camera_markers = ['o', 'X', 'P']
    colors = ['b', 'g', 'orange']
    camera_colors = ['y', 'r', 'm']
    fit_line = ['--', '-.', ':']
    linestyles = ['--', '-.', ':']

    camera_water_height = [[0.096,
                            0.096,
                            0.096,
                            0.09408,
                            0.09216,
                            0.08832,
                            0.08448,
                            0.0816,
                            0.07872,
                            0.0768,
                            0.06912,
                            0.0672,
                            0.06528,
                            0.06432,
                            0.06336],
                           [0.09504,
                            0.0912,
                            0.09504,
                            0.09024,
                            0.0864,
                            0.08256,
                            0.07968,
                            0.0768,
                            0.07008,
                            0.0672,
                            0.06336,
                            0.0576,
                            0.05376],
                           [0.08352,
                            0.0768,
                            0.06912,
                            0.06144,
                            0.05376,
                            0.04608]]
    camera_time = [[0,
                    1800,
                    3600,
                    5400,
                    7200,
                    9000,
                    10800,
                    12600,
                    14400,
                    16200,
                    18000,
                    19755,
                    20355,
                    20955,
                    21555],
                   [2230,
                    3730,
                    5230,
                    6730,
                    8230,
                    9730,
                    11230,
                    12730,
                    14230,
                    15730,
                    17230,
                    18730,
                    20230],
                   [4930,
                    6430,
                    7930,
                    9430,
                    10930,
                    12430]]
    # ignore time offset because all of them started at same height
    for exp_num, [data_path, time_offset] in enumerate(experiments_data_paths):
        exp_data = read_experiment_data(data_path)

        get_real_water_height(exp_data)

        plot_water_height_data(exp_data, axes, fit_func_to_data=True, c=colors.pop(0), marker=markers.pop(0),
                               fit_line=fit_line.pop(0), label_fit=True, temp_label=True)

        if exp_num == 1:
            camera_time[exp_num] = [t - 2230 for t in camera_time[exp_num]]

        camera_marker = camera_markers.pop(0)
        camera_color = camera_colors.pop(0)
        axes.scatter(camera_time[exp_num], camera_water_height[exp_num], zorder=99, c=camera_color,
                     marker=camera_marker,
                     label=f'Camera data for {round(exp_data.temp.quantile(0.6)):.0f}$\degree$ measurement')

        earliest_ind = next((i for i, t in enumerate(camera_time[exp_num]) if t > 3000))
        relevant_camera_time = camera_time[exp_num][earliest_ind:]
        relevant_height = camera_water_height[exp_num][earliest_ind:]
        print(fit_and_plot_line(relevant_camera_time, relevant_height, fig=12, plot_axes=False,
                                linestyle=linestyles.pop(0)))
        plt.scatter(relevant_camera_time, relevant_height, zorder=99, c=camera_color,
                    marker=camera_marker,
                    label=f'Camera data for {round(exp_data.temp.quantile(0.6)):.0f}$\degree$ measurement')
        plt.grid(zorder=-12)
        plt.xlabel('Time[s]')
        plt.ylabel('Height of water[m]')
        plt.title('Height of water for different measurements based on camera')
        plt.legend()

        plt.figure('other')
        camera_sonar_error = [
            exp_data.water_height[(exp_data.time < t + 200) & (exp_data.time > t - 200)].mean() -
            camera_water_height[exp_num][camera_time[exp_num].index(t)]
            for cam_height, t in zip(camera_water_height[exp_num], camera_time[exp_num])]
        plt.scatter(camera_time[exp_num], camera_sonar_error,
                    label=f'Error for {round(exp_data.temp.quantile(0.6)):.0f}$\degree$ measurement', zorder=12,
                    c=camera_color, marker=camera_marker)
        plt.xlabel('Time[s]')
        plt.ylabel('Sonar height data minus camera height data[m]')
        plt.title('Sonar height data error relative to camera data')
        plt.grid(zorder=-1)

    plt.legend()
    axes.legend()
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


def plot_cooling_graphs_on_same_plot(experiments_data_paths, END_TEMP=25):
    plt.figure()
    axes = plt.gca()

    linestyles = ['--', ':', '-.']
    for data_path in experiments_data_paths:
        exp_data = read_experiment_data(data_path, cooling_measurement=True)

        plot_cooling_time(exp_data, axes, plot_delta_temp=True, log_plot=True, end_temp=END_TEMP, fit_func_to_data=True,
                          temp_label=True, func_linestyle=linestyles.pop(0))

    plt.xlabel('Time[s]')
    plt.ylabel(f'Water temperature -{END_TEMP}$\degree$[$\degree$C]')
    plt.show()


if __name__ == '__main__':
    # plot_cooling_and_heating_times(DEFAULT_FILE_PATH, '..\\Results\\18.5.2020\\exp1 - last run only.csv')

    plot_single_experiment(DEFAULT_FILE_PATH)

    # experiments_data = [('..\\Results\\13.5.2020\\ex1 grouped - 13.5.2020.csv', 0),
    #                     ('..\\Results\\18.5.2020\\exp1 - last run only.csv', 2100),
    #                     ('..\\Results\\20.5.2020\\ex1.csv', 0)]

    # compare_several_experiments_temperature(experiments_data)
    # compare_several_experiments_height(experiments_data)

    # cooling_experiments_data = ['..\\Results\\18.5.2020\\exp2 - cooling over night.csv',
    #                             '..\\Results\\14.5.2020\\exp2.csv']
    #
    # plot_cooling_graphs_on_same_plot(cooling_experiments_data)
