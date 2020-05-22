import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from utils import plot_line, fit_func

SAVE_PLOTS = False

data_path = '/home/avni1alon/alon/Lab/yalab/data/'
file_path = data_path + 'water_experiment_1_bach_2.csv'  # alon
# file_path = '..\\Results\\13.5.2020\\ex1 grouped - 13.5.2020.csv'  # yonatan

relevant_cols = 'A:D'
header_row = 1
plt.figure('sonar position')

experiment_data = pd.read_csv(file_path, header=header_row - 1,
                              usecols=['Time (s)', 'Position (m)', 'Temperature (C)']) \
    .rename(columns={'Time (s)': 'time', 'Position (m)': 'pos', 'Temperature (C)': 'temp'})
axes = plt.gca()

## plot real data
experiment_data.plot(x='time', y='pos', label='Raw position data', ax=axes, linestyle='None', marker='.')

# smoothen the position data via applying a rolling average
rolling_window_size = 30
experiment_data['pos_error'] = experiment_data.pos.rolling(window=rolling_window_size, center=True).std()
experiment_data.pos = experiment_data.pos.rolling(window=rolling_window_size, center=True).mean()
experiment_data = experiment_data.dropna().reset_index(drop=True)
experiment_data.plot(x='time', y='pos', label='Smoothened position data', ax=axes, grid=True, linestyle='None',
                     marker='x')

plt.title('Height over time')
plt.ylabel('Distance from sonar[m]')
plt.xlabel('Time[s]')
plt.legend()
if SAVE_PLOTS:
    plt.savefig(data_path + 'Height over time.png')

# normalize the position
experiment_data['real_h'] = experiment_data.pos - 0.033

# linear fit for position over time
start_fit_time = 5000  # [s]

linear_fit_data = experiment_data[experiment_data.time > start_fit_time]

linear_func = lambda t, a, b: a * t + b
[slope, intercept], errors = fit_func(linear_func, linear_fit_data.time, linear_fit_data.real_h)
print(slope, intercept, errors)

end_time = linear_fit_data.time.max()

# plot linear fit
fig_name = 'Linear fit to data'
plt.figure(fig_name)
axes = plt.gca()
experiment_data.plot(x='time', y='real_h', label='Experimental data', grid=True, ax=axes, marker='.',
                     linestyle='None')
plt.errorbar(experiment_data.time, experiment_data.real_h, experiment_data.pos_error, alpha=0.1, capsize=2,
             ecolor='r')
fit_label = f'Linear fit\n({slope:.2e}$\pm${errors[0]:.2e})t+{intercept:.2e}$\pm${errors[1]:.2e}'
plot_line(slope, intercept, x_range=[start_fit_time, end_time], fig=fig_name, plot_axes=False, label=fit_label, c='k',
          zorder=12)

# add camera dots
experiment_data['c_pos'] = [0.125,0.125,0.125,0.1225,0.12,0.115,0.11,0.10625,0.1025,0.1,0.09,0.0875,0.085,0.08375,0.0825]
experiment_data['c_time'] = [0,1800,3600,5400,7200,9000,10800,12600,14400,16200,18000,19800,21600,23400,25200]
experiment_data.plot.scatter(x='c_time', y='c_pos', style=['o', 'rx'], s=12)

plt.title('Linear fit to part of height over time data')
plt.ylabel('$\Delta$h[m]')
plt.xlabel('Time[s]')
plt.legend()
if SAVE_PLOTS:
    plt.savefig(data_path + 'Linear fit to part of height over time data.png')

plt.figure('Residuals plot')
sns.residplot(linear_fit_data.time, linear_fit_data.real_h)

plt.title('Residuals plot for linear fit')
plt.ylabel('$\Delta$h error[m]')
plt.xlabel('Time[s]')
if SAVE_PLOTS:
    plt.savefig(data_path + 'Residuals plot.png')

# plt.show()
print('Done!')
