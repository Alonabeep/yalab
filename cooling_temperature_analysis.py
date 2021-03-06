import matplotlib.pyplot as plt
import numpy as np

from utils import fit_func, plot_func


def plot_cooling_time(exp_data, axes, plot_delta_temp=False, fit_func_to_data=False, end_temp=25, start_time=0,
                      save_plots=False, data_path=None, log_plot=False, temp_label=False, func_linestyle='--'):
    # assuming that temperature doesn't rise later...
    relevant_data = exp_data[(exp_data.temp > end_temp) & (exp_data.time > start_time)]
    relevant_data.time -= start_time

    if plot_delta_temp:
        relevant_data['delta_temp'] = relevant_data.temp - (relevant_data.room_temp
                                                            if 'room_temp' in relevant_data.columns else end_temp)
        temp_to_analyze = 'delta_temp'
    else:
        temp_to_analyze = 'temp'

    if temp_label:
        data_label = f'{round(relevant_data.temp.iat[0]):.0f}$\degree$ initial temperature data'
    else:
        data_label = 'Experimental data'
    relevant_data.plot(x='time', y=temp_to_analyze, marker='.', linestyle='None', label=data_label, grid=True,
                       logy=log_plot, ax=axes)

    if fit_func_to_data:
        # fit func and plot results
        temp_offset = 0 if plot_delta_temp else end_temp
        data_func_to_fit = lambda t, amp, decay_time: amp * np.exp(-t / decay_time) + temp_offset
        [amplitude, decay_time], errors = fit_func(data_func_to_fit, relevant_data.time, relevant_data[temp_to_analyze])
        fitted_func = lambda t: data_func_to_fit(t, amplitude, decay_time)

        time_range = [relevant_data.time.min(), relevant_data.time.max()]
        fitted_data_label = 'Function fitted to data \n' \
            f'T(t)=({amplitude:.2f}$\pm${errors[0]:.2f})exp(-t/({decay_time:.0f}$\pm${errors[1]:.0f}))+{end_temp}'
        plot_func(fitted_func, time_range, c='k', linestyle=func_linestyle, label=fitted_data_label)

        plot_temp_prefix = '$\Delta$' if plot_delta_temp else ''
        axes.set_xlabel('Time[s]')
        axes.set_ylabel(plot_temp_prefix + 'Temperature[$\degree$C]')
        axes.set_title(plot_temp_prefix + 'T(t) while heating plate is turned off')
        axes.legend()
        if save_plots:
            plt.savefig(data_path + plot_temp_prefix + 'T(t) while heating plate is turned off.png')


def plot_room_temp(exp_data, axes, ylabel=None, **kwargs):
    exp_data.plot(x='time', y='room_temp', ax=axes, linestyle='None', label='Room temperature', grid=True, **kwargs)

    axes.set_xlabel('Time[s]')
    axes.set_ylabel('Temperature[$\degree$C]' if ylabel is None else ylabel)
    axes.set_title('Room temperature over time')

# TODO: create function
# plt.figure()
# temp_error = experiment_data[temp_to_analyze] - fitted_func(experiment_data.time)
#
# plt.scatter(experiment_data.time, temp_error)
#
# plt.grid()
# plt.gca().set_axisbelow(True)
# plt.title('T(t) residuals plot')
# plt.xlabel('Time[s]')
# plt.ylabel('Temperature Error[$\degree$C]')
# if SAVE_PLOTS:
#     plt.savefig(data_path + 'T(t) residuals plot.png')
#
# plt.show()
# print('Done!')
