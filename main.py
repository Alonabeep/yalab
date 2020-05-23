import pandas as pd

import matplotlib.pyplot as plt

from temp_pos_analysis import read_experiment_data as plot_temp_over_time_data
from sonar_pos_analysis import plot_water_height_data, get_real_water_height

DEFAULT_FILE_PATH = '..\\Results\\20.5.2020\\ex1.csv'  # yonatan

DEFAULT_HEADER_ROW = 1


def read_experiment_data(file_path=DEFAULT_FILE_PATH, header_row=DEFAULT_HEADER_ROW):
    experiment_data = pd.read_csv(file_path, header=header_row - 1,
                                  usecols=['Time (s)', 'Position (m)', 'Temperature (C)']) \
        .rename(columns={'Time (s)': 'time', 'Position (m)': 'pos', 'Temperature (C)': 'temp'})

    return experiment_data


if __name__ == '__main__':
    exp_data = read_experiment_data()

    fig, axs = plt.subplots(2)

    get_real_water_height(exp_data)
    plot_water_height_data(exp_data, axs[0], fit_func_to_data=True)

    plt.show()
