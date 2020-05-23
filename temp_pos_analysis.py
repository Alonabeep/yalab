import matplotlib.pyplot as plt
import numpy as np

from utils import fit_func, plot_func

# DEFAULT_FILE_PATH = '/home/avni1alon/alon/Lab/data/try.csv' # alon
DEFAULT_FILE_PATH = '..\\Results\\13.5.2020\\ex1 grouped - 13.5.2020.csv'  # yonatan

DEFAULT_HEADER_ROW = 1


def plot_temp_over_time_data(exp_data, axes, fit_func_to_data=True, start_fit_time=0, temp_amplitude=None,
                             start_fit_temp=None, linearize=False, ylabel=None):
    fit_data = exp_data[exp_data.time > start_fit_time]
    if start_fit_temp is None:
        start_fit_temp = fit_data.temp.iat[0]

    if temp_amplitude is None:
        temp_amplitude = exp_data.temp.max() - exp_data.temp.min()

    if fit_func_to_data:
        def temp_over_time_func(t, decay_time):
            return temp_amplitude * (1 - np.exp(-t / decay_time)) + start_fit_temp

        [decay_time], errors = fit_func(temp_over_time_func, fit_data.time, fit_data.temp, p0=[1500])
        print(temp_amplitude, decay_time, errors)
        fitted_data_label = 'Function fitted to data \n' \
            f'T(t)={temp_amplitude:.1f}(1-exp(-t/({decay_time:.0f}$\pm${errors[0]:.0f})))+' \
            f'{start_fit_temp}'
        if not linearize:
            func_to_plot = lambda t: temp_over_time_func(t, decay_time)
            plot_range = [start_fit_time, fit_data.time.iat[-1]]
        else:
            exp_data['linearized_time'] = 1 - np.exp(-exp_data.time / decay_time)
            func_to_plot = lambda linear_t: temp_amplitude * linear_t + start_fit_temp
            plot_range = [0, exp_data.linearized_time.max() + 1e-3]

        plot_func(func_to_plot, axes=axes, x_range=plot_range, c='k', label=fitted_data_label, zorder=12)

    exp_data.plot(x='time' if not linearize else 'linearized_time', y='temp', grid=True, linestyle='None',
                  marker='.', label='Experimental data', ax=axes)
    axes.legend()
    axes.set_xlabel('Time[s]')
    axes.set_ylabel('Temperature[$\degree$C]' if ylabel is None else ylabel)
    axes.set_title('T(t) while heating plate is turned on')

    if linearize:
        axes.set_xticks([])
        max_tick_time = round(decay_time * 2, -2)
        tick_time_interval = 350

        unnormalized_time, real_time = zip(*[(1 - np.exp(-t / decay_time), int(t)) for t in
                                             np.linspace(0, max_tick_time,
                                                         num=int(max_tick_time / tick_time_interval))])
        plt.xticks(unnormalized_time, real_time)
