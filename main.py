import matplotlib.pyplot as plt
import pandas as pd

from sonar_pos_analysis import plot_water_height_data, get_real_water_height
from temp_pos_analysis import plot_temp_over_time_data

DEFAULT_FILE_PATH = '..\\Results\\20.5.2020\\ex1.csv'  # yonatan

DEFAULT_HEADER_ROW = 1


def read_experiment_data(file_path=DEFAULT_FILE_PATH, header_row=DEFAULT_HEADER_ROW):
    experiment_data = pd.read_csv(file_path, header=header_row - 1,
                                  usecols=['Time (s)', 'Position (m)', 'Temperature (C)']) \
        .rename(columns={'Time (s)': 'time', 'Position (m)': 'pos', 'Temperature (C)': 'temp'})

    return experiment_data


if __name__ == '__main__':
    exp_data = read_experiment_data()

    temp_amplitude = exp_data.temp.max() - exp_data.temp.min()
    # start the linear fit only when the temperature reaches its 90th percentile
    temp_start_fit_threshold = exp_data.temp.min() + 0.9 * temp_amplitude
    start_fit_time = exp_data.time[exp_data.temp > temp_start_fit_threshold].iat[0]

    fig, axs = plt.subplots(2, sharex=True)

    get_real_water_height(exp_data)
    plot_water_height_data(exp_data, axs[0], fit_func_to_data=True, start_fit_time=start_fit_time)

    plot_temp_over_time_data(exp_data, axs[1])

    # make them have the same x axis
    plt.subplots_adjust(hspace=0)
    for ax in axs:
        ax.set_title('')

    plt.show()
