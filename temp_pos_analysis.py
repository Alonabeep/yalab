import numpy as np
import pandas as pd

from utils import fit_func, plot_func

# DEFAULT_FILE_PATH = '/home/avni1alon/alon/Lab/data/try.csv' # alon
DEFAULT_FILE_PATH = '..\\Results\\13.5.2020\\ex1 grouped - 13.5.2020.csv'  # yonatan

DEFAULT_HEADER_ROW = 1


def read_experiment_data(file_path=DEFAULT_FILE_PATH, header_row=DEFAULT_HEADER_ROW):
    experiment_data = pd.read_csv(file_path, header=header_row - 1,
                                  usecols=['Time (s)', 'Position (m)', 'Temperature (C)']) \
        .rename(columns={'Time (s)': 'time', 'Position (m)': 'pos', 'Temperature (C)': 'temp'})

    return experiment_data


def plot_temp_over_time_data(experiment_data, axes, fit_func_to_data=True, start_fit_time=0):
    experiment_data.plot(x='time', y='temp', grid=True, linestyle='None', marker='.', label='Experimental data',
                         ax=axes)

    start_fit_time = 0
    fit_data = experiment_data[experiment_data.time > start_fit_time]
    start_fit_temp = fit_data.temp.iat[0]

    if fit_func_to_data:
        def temp_over_time_func(t, amplitude, decay_time):
            return amplitude * (1 - np.exp(-(t - start_fit_time) / decay_time)) + start_fit_temp

        [amplitude, decay_time], errors = fit_func(temp_over_time_func, fit_data.time, fit_data.temp)
        print(amplitude, decay_time, errors)
        fitted_data_label = 'Function fitted to data \n' \
            f'T(t)=({amplitude:.2f}$\pm${errors[0]:.2f})(1-exp(-t/({decay_time:.0f}$\pm${errors[1]:.0f})))+' \
            f'{start_fit_temp}'
        plot_func(lambda t: temp_over_time_func(t, amplitude, decay_time), axes=axes,
                  x_range=[start_fit_time, fit_data.time.iat[-1]], c='k', label=fitted_data_label)

    axes.legend()
    axes.set_xlabel('Time[s]')
    axes.set_ylabel('Temperature[$\degree$C]')
    axes.set_title('T(t) while heating plate is turned on')
