import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils import fit_func, plot_func

# configuration constants
SAVE_PLOTS = False
MEASURE_ROOM_TEMP = False

# data_path = '/home/avni1alon/alon/Lab/yalab/data/'
# file_path = data_path + 'water_experiment_1_bach_2.csv' # alon
file_path = '..\\Results\\14.5.2020\\exp2.csv'  # yonatan

relevant_cols = 'A:D'
header_row = 1

if MEASURE_ROOM_TEMP:
    data_cols = ['Time (s)', 'Temperature1 (C)', 'Temperature2 (C)']
    col_variable_names = {'Time (s)': 'time', 'Temperature1 (C)': 'temp', 'Temperature2 (C)': 'room_temp'}
else:
    data_cols = ['Time (s)', 'Temperature (C)']
    col_variable_names = {'Time (s)': 'time', 'Temperature (C)': 'temp'}

experiment_data = pd.read_csv(file_path, header=header_row - 1, usecols=data_cols).rename(columns=col_variable_names)

end_temp = 25  # [C]
start_time = 0  # [s]
# assuming that temperature doesn't rise later...
experiment_data = experiment_data[(experiment_data.temp > end_temp) & (experiment_data.time > start_time)]
experiment_data.time -= start_time

if MEASURE_ROOM_TEMP:
    experiment_data['delta_temp'] = experiment_data.temp - experiment_data.room_temp
    temp_to_analyze = 'delta_temp'
else:
    temp_to_analyze = 'temp'

experiment_data.plot(x='time', y=temp_to_analyze, marker='.', linestyle='None', label='Experimental Data', grid=True)

# fit func and plot results
temp_offset = 0 if MEASURE_ROOM_TEMP else end_temp
data_func_to_fit = lambda t, amp, decay_time: amp * np.exp(-t / decay_time) + temp_offset
[amplitude, decay_time], errors = fit_func(data_func_to_fit, experiment_data.time, experiment_data[temp_to_analyze])
fitted_func = lambda t: data_func_to_fit(t, amplitude, decay_time)

time_range = [experiment_data.time.min(), experiment_data.time.max()]
fitted_data_label = 'Function fitted to data \n' \
    f'T(t)=({amplitude:.2f}$\pm${errors[0]:.2f})exp(-t/({decay_time:.0f}$\pm${errors[1]:.0f}))+{end_temp}'
plot_func(fitted_func, time_range, c='k', linestyle='dashed', label=fitted_data_label)

plot_temp_prefix = '$\Delta$' if MEASURE_ROOM_TEMP else ''
plt.xlabel('Time[s]')
plt.ylabel(plot_temp_prefix + 'Temperature[$\degree$C]')
plt.title(plot_temp_prefix + 'T(t) while heating plate is turned off')
plt.legend()
if SAVE_PLOTS:
    plt.savefig(data_path + plot_temp_prefix + 'T(t) while heating plate is turned off.png')

plt.figure()
temp_error = experiment_data[temp_to_analyze] - fitted_func(experiment_data.time)

plt.scatter(experiment_data.time, temp_error)

plt.grid()
plt.gca().set_axisbelow(True)
plt.title('T(t) residuals plot')
plt.xlabel('Time[s]')
plt.ylabel('Temperature Error[$\degree$C]')
if SAVE_PLOTS:
    plt.savefig(data_path + 'T(t) residuals plot.png')

plt.show()
print('Done!')
