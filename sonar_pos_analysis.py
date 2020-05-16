import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from utils import plot_line, fit_func

# file_path = '/home/avni1alon/alon/Lab/data/try.csv' # alon
file_path = '..\\Results\\13.5.2020\\ex1 grouped - 13.5.2020.csv'  # yonatan

relevant_cols = 'A:D'
header_row = 1
plt.figure('sonar position')

experiment_data = pd.read_csv(file_path, header=header_row - 1,
                              usecols=['Time (s)', 'Position (m)', 'Temperature (C)']) \
    .rename(columns={'Time (s)': 'time', 'Position (m)': 'pos', 'Temperature (C)': 'temp'})

axes = plt.gca()

## plot real data
experiment_data.plot(x='time', y='pos', label='Raw position data', ax=axes)

# smoothen the position data via applying a rolling average
experiment_data.pos = experiment_data.pos.rolling(window=20, center=True).mean()
experiment_data = experiment_data.dropna().reset_index(drop=True)
experiment_data.plot(x='time', y='pos', label='Smoothened position data', ax=axes, grid=True)

# normalize the position
experiment_data['delta_h'] = experiment_data.pos[0] - experiment_data.pos

# linear fit for position over time
start_fit_time = 5000  # [s]
start_fit_index = pd.Index(experiment_data.time).get_loc(start_fit_time)

linear_fit_data = experiment_data[experiment_data.time > start_fit_time]

linear_func = lambda t, a, b: a * t + b
[slope, intercept], errors = fit_func(linear_func, linear_fit_data.time, linear_fit_data.delta_h)
print(slope, intercept, errors)

end_time = linear_fit_data.time.max()

# plot linear fit
fig_name = 'Linear fit to data'
plt.figure(fig_name)
axes = plt.gca()
experiment_data.plot(x='time', y='delta_h', label='Experimental data', grid=True, ax=axes, marker='.', linestyle='None')
fit_label = f'Linear fit\n({slope:.2e}$\pm${errors[0]:.2e})t+{intercept:.2e}$\pm${errors[1]:.2e}'
plot_line(slope, intercept, x_range=[start_fit_time, end_time], fig=fig_name, plot_axes=False, label=fit_label, c='k')

plt.xlabel('Time[s]')
plt.ylabel('$\Delta$h[m]')
plt.legend()

plt.figure('Residuals plot')
line = [linear_func(t, slope, intercept) for t in range(start_fit_time, end_time, 10)]
sns.residplot(experiment_data["time"], experiment_data["pos"])

plt.show()
