import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils import fit_func, plot_func

file_path = '..\\Results\\14.5.2020\\exp2.csv'

relevant_cols = 'A:D'
header_row = 1

experiment_data = pd.read_csv(file_path, header=header_row - 1, usecols=['Time (s)', 'Temperature (C)']) \
    .rename(columns={'Time (s)': 'time', 'Temperature (C)': 'temp'})

end_temp = 22.9  # [C]
experiment_data = experiment_data[experiment_data.temp > end_temp]  # assuming that temperature doesn't rise later...

experiment_data.plot(x='time', y='temp', marker='.', linestyle='None', label='Experimental Data')

# fit func and plot results
data_func_to_fit = lambda t, amp, decay_time: amp * np.exp(-t / decay_time) + end_temp
[amplitude, decay_time], errors = fit_func(data_func_to_fit, experiment_data.time, experiment_data.temp)

time_range = [0, experiment_data.time.max()]
fitted_data_label = 'Function fitted to data \n' \
    f'({amplitude:.2f}$\pm${errors[0]:.2f})exp(-t/({decay_time:.0f}$\pm${errors[1]:.0f}))+{end_temp}'
plot_func(lambda t: data_func_to_fit(t, amplitude, decay_time), time_range, c='k', linestyle='dashed',
          label=fitted_data_label)

plt.xlabel('Time[s]')
plt.ylabel('Temperature[$\degree$C]')
plt.title('T(t) while heating plate is turned off')
plt.legend()

plt.show()
