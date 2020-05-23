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


def plot_temp_over_time_data(experiment_data, axes, fit_func_to_data=True, start_fit_time=0, linearize=False):
    temp_amplitude = experiment_data.temp.max() - experiment_data.temp.min()

    start_fit_time = 0
    fit_data = experiment_data[experiment_data.time > start_fit_time]
    start_fit_temp = fit_data.temp.iat[0]

    if fit_func_to_data:
        def temp_over_time_func(t, decay_time):
            return temp_amplitude * (1 - np.exp(-(t - start_fit_time) / decay_time)) + start_fit_temp

        [decay_time], errors = fit_func(temp_over_time_func, fit_data.time, fit_data.temp)
        print(temp_amplitude, decay_time, errors)
        fitted_data_label = 'Function fitted to data \n' \
            f'T(t)={temp_amplitude:.1f}(1-exp(-t/({decay_time:.0f}$\pm${errors[0]:.0f})))+' \
            f'{start_fit_temp}'
        if not linearize:
            func_to_plot = lambda t: temp_over_time_func(t, decay_time)
            plot_range = [start_fit_time, fit_data.time.iat[-1]]
        else:
            experiment_data['linearized_time'] = 1 - np.exp(-experiment_data.time / decay_time)
            func_to_plot = lambda linear_t: temp_amplitude * linear_t + start_fit_temp
            plot_range = [0, 1]

        plot_func(func_to_plot, axes=axes, x_range=plot_range, c='k', label=fitted_data_label, zorder=12)

    experiment_data.plot(x='time' if not linearize else 'linearized_time', y='temp', grid=True, linestyle='None',
                         marker='.', label='Experimental data', ax=axes)
    axes.legend()
    axes.set_xlabel('Time[s]' if not linearize else f'1-exp(-t/{decay_time:.2f})')
    axes.set_ylabel('Temperature[$\degree$C]')
    axes.set_title('T(t) while heating plate is turned on')
